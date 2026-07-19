from __future__ import annotations

import io
import zipfile


def make_docx(paragraphs: list[str]) -> bytes:
    escaped = []
    for paragraph in paragraphs:
        safe = (
            paragraph.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
        escaped.append(f"<w:p><w:r><w:t>{safe}</w:t></w:r></w:p>")
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{''.join(escaped)}</w:body></w:document>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '</Types>'
    )
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("word/document.xml", document)
    return buffer.getvalue()


SAMPLE_CV_PARAGRAPHS = [
    "Alex Morgan",
    "Software Engineer",
    "Professional Summary",
    "Software engineer focused on reliable backend systems and accessible web products.",
    "Experience",
    "Built Python REST APIs for customer-facing services.",
    "Designed PostgreSQL schemas and improved query performance.",
    "Used Docker and GitHub Actions for continuous delivery.",
    "Education",
    "Bachelor of Science in Computer Science, 2020",
    "Skills",
    "Python, PostgreSQL, REST, Docker, GitHub Actions, HTML, CSS",
]


SAMPLE_JOB = """Backend Software Engineer
Responsibilities
- Build and maintain reliable REST APIs for customer-facing products.
- Collaborate with product and engineering teams.
Required Qualifications
- Professional experience with Python and PostgreSQL.
- Experience designing REST APIs and using Git.
Preferred Qualifications
- Docker and Kubernetes experience.
- Familiarity with AWS services.
"""

