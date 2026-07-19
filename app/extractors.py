from __future__ import annotations

import io
import re
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path, PurePosixPath
from typing import Any
from xml.etree import ElementTree

from .errors import ValidationError
from .language import is_probably_english


MAX_PDF_PAGES = 30
MAX_DOCX_ENTRIES = 1_000
MAX_DOCX_UNCOMPRESSED = 20 * 1024 * 1024


@dataclass(frozen=True)
class SourceBlock:
    id: str
    text: str
    page: int | None
    paragraph: int
    section: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExtractedCV:
    filename: str
    media_type: str
    text: str
    blocks: list[SourceBlock]
    sections: dict[str, list[str]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "filename": self.filename,
            "media_type": self.media_type,
            "text": self.text,
            "blocks": [block.to_dict() for block in self.blocks],
            "sections": self.sections,
        }


SECTION_PATTERNS = [
    ("summary", re.compile(r"^(professional\s+)?summary|profile|objective$", re.I)),
    ("experience", re.compile(r"^(work\s+)?experience|employment|professional experience$", re.I)),
    ("education", re.compile(r"^education|academic background$", re.I)),
    ("skills", re.compile(r"^(technical\s+)?skills|core competencies|technologies$", re.I)),
    ("projects", re.compile(r"^projects|selected projects$", re.I)),
    ("certifications", re.compile(r"^certifications?|licenses?$", re.I)),
]


def _section_for(text: str) -> str | None:
    cleaned = re.sub(r"[:\s]+$", "", text.strip())
    if len(cleaned) > 45:
        return None
    for name, pattern in SECTION_PATTERNS:
        if pattern.fullmatch(cleaned):
            return name
    return None


def _build_cv(filename: str, media_type: str, paragraphs: list[tuple[str, int | None]]) -> ExtractedCV:
    blocks: list[SourceBlock] = []
    sections: dict[str, list[str]] = {"header": []}
    current_section = "header"
    for index, (raw_text, page) in enumerate(paragraphs, start=1):
        text = re.sub(r"\s+", " ", raw_text).strip()
        if not text:
            continue
        section = _section_for(text)
        if section:
            current_section = section
            sections.setdefault(section, [])
            continue
        sections.setdefault(current_section, []).append(text)
        blocks.append(SourceBlock(f"cv-{len(blocks) + 1}", text, page, index, current_section))
    full_text = "\n".join(block.text for block in blocks)
    if len(full_text) < 80 or len(blocks) < 3:
        raise ValidationError("cv_unreadable", "The CV does not contain enough readable text.")
    if not is_probably_english(full_text):
        raise ValidationError("cv_not_english", "Please upload an English CV. The content is not translated automatically.")
    return ExtractedCV(filename, media_type, full_text, blocks, sections)


def _extract_docx(filename: str, data: bytes) -> ExtractedCV:
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as exc:
        raise ValidationError("invalid_docx", "The DOCX file is damaged or has an invalid signature.") from exc
    with archive:
        infos = archive.infolist()
        if len(infos) > MAX_DOCX_ENTRIES or sum(info.file_size for info in infos) > MAX_DOCX_UNCOMPRESSED:
            raise ValidationError("docx_too_complex", "The DOCX file expands beyond the safe processing limit.")
        for info in infos:
            path = PurePosixPath(info.filename)
            if path.is_absolute() or ".." in path.parts:
                raise ValidationError("invalid_docx_path", "The DOCX file contains an unsafe path.")
        names = {info.filename for info in infos}
        if "[Content_Types].xml" not in names or "word/document.xml" not in names:
            raise ValidationError("invalid_docx", "The file is not a supported DOCX document.")
        try:
            root = ElementTree.fromstring(archive.read("word/document.xml"))
        except ElementTree.ParseError as exc:
            raise ValidationError("invalid_docx_xml", "The DOCX document content cannot be read.") from exc
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paragraphs: list[tuple[str, int | None]] = []
    for paragraph in root.iter(namespace + "p"):
        text = "".join(node.text or "" for node in paragraph.iter(namespace + "t"))
        if text.strip():
            paragraphs.append((text, None))
    return _build_cv(filename, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", paragraphs)


def _extract_pdf(filename: str, data: bytes) -> ExtractedCV:
    if not data.startswith(b"%PDF-"):
        raise ValidationError("invalid_pdf", "The PDF file has an invalid signature.")
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(data), strict=True)
    except Exception as exc:
        raise ValidationError("invalid_pdf", "The PDF is damaged, encrypted, or cannot be read safely.") from exc
    if reader.is_encrypted:
        raise ValidationError("encrypted_pdf", "Encrypted PDF files are not supported.")
    if len(reader.pages) > MAX_PDF_PAGES:
        raise ValidationError("pdf_too_long", f"The PDF exceeds the {MAX_PDF_PAGES}-page limit.")
    paragraphs: list[tuple[str, int | None]] = []
    try:
        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            for line in page_text.splitlines():
                if line.strip():
                    paragraphs.append((line, page_number))
    except Exception as exc:
        raise ValidationError("pdf_text_error", "Text could not be extracted from the PDF.") from exc
    return _build_cv(filename, "application/pdf", paragraphs)


def extract_cv(filename: str, data: bytes, *, max_bytes: int) -> ExtractedCV:
    safe_name = Path(filename).name
    if not safe_name or safe_name in {".", ".."}:
        raise ValidationError("invalid_filename", "The CV filename is invalid.")
    if not data:
        raise ValidationError("empty_file", "The selected CV file is empty.")
    if len(data) > max_bytes:
        raise ValidationError("file_too_large", "The CV exceeds the upload size limit.")
    extension = Path(safe_name).suffix.lower()
    if extension == ".pdf":
        return _extract_pdf(safe_name, data)
    if extension == ".docx":
        if not data.startswith(b"PK"):
            raise ValidationError("invalid_docx", "The DOCX file has an invalid signature.")
        return _extract_docx(safe_name, data)
    raise ValidationError("unsupported_file", "Only PDF and DOCX CV files are supported.")

