from __future__ import annotations

import re


ENGLISH_MARKERS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is", "of",
    "on", "or", "that", "the", "this", "to", "with", "work", "experience", "skills",
    "education", "responsibilities", "requirements", "required", "preferred", "developed",
    "managed", "built", "engineer", "developer", "role", "team", "using",
}
TURKISH_MARKERS = {
    "bir", "bu", "ve", "ile", "için", "olan", "olarak", "görev", "deneyim", "gereksinimler",
    "aranan", "nitelikler", "iş", "pozisyon", "takım", "çalışma", "yönetim", "geliştirme",
}


def language_signal(text: str) -> dict[str, float | int]:
    words = re.findall(r"[A-Za-zÀ-ž']+", text.lower())
    if not words:
        return {"english": 0, "turkish": 0, "ascii_ratio": 0.0, "word_count": 0}
    english = sum(1 for word in words if word in ENGLISH_MARKERS)
    turkish = sum(1 for word in words if word in TURKISH_MARKERS)
    ascii_letters = sum(1 for char in text if char.isascii() and char.isalpha())
    all_letters = sum(1 for char in text if char.isalpha()) or 1
    return {
        "english": english,
        "turkish": turkish,
        "ascii_ratio": ascii_letters / all_letters,
        "word_count": len(words),
    }


def is_probably_english(text: str, *, minimum_words: int = 12) -> bool:
    signal = language_signal(text)
    if signal["word_count"] < minimum_words:
        return False
    if signal["turkish"] > signal["english"] and signal["turkish"] >= 2:
        return False
    return bool(signal["english"] >= 2 and signal["ascii_ratio"] >= 0.82)

