import re
import unicodedata
from enum import Enum
from .unicode_normalization import normalize_unicode

# Normalize all line breaks to '\n'
_LINEBREAKS_RE = re.compile(r"\r\n?|\u0085|\u2028|\u2029")

# Zero-width and invisible characters to remove (includes BOM everywhere)
_ZERO_WIDTH_STRIP = dict.fromkeys(map(ord, [
    "\u200B",  # ZERO WIDTH SPACE
    "\u2060",  # WORD JOINER
    "\uFEFF",  # ZERO WIDTH NO-BREAK SPACE / BOM (remove even mid-text)
    "\u180E",  # MONGOLIAN VOWEL SEPARATOR (deprecated)
    "\u034F",  # COMBINING GRAPHEME JOINER
]))

# Map all Unicode spaces (and horizontal ASCII whitespace) to ASCII space
_UNICODE_SPACES = [
    "\u00A0",  # NO-BREAK SPACE
    "\u1680", "\u2000", "\u2001", "\u2002", "\u2003", "\u2004",
    "\u2005", "\u2006", "\u2007", "\u2008", "\u2009", "\u200A",
    "\u202F", "\u205F", "\u3000",  # narrow, medium, ideographic spaces
    "\t", "\x0b", "\x0c"           # TAB, VT, FF
]
_SPACE_TO_ASCII = {ord(ch): " " for ch in _UNICODE_SPACES}


def normalize_spaces(
    text: str,
    collapse_internal_spaces: bool = True,
    tibetan_specific: bool = True,
) -> str:
    """
    Normalize spaces in text.

    Steps:
      1. Collapse multiple newlines to one.
      2. Remove spaces next to newlines.
      3. Collapse multiple spaces to one.
      4. Apply Tibetan-specific space normalization rules.

    Tibetan-specific rules:
      - Remove space after tsheg (U+0F0B, U+0F0C, U+0FD2) if followed by
        initial letter (U+0F40-U+0F6C) or shad (U+0F0D-U+0F11)
      - Remove space between final letter (U+0F40-U+0FBC) and tsheg
    """
    if not text:
        return ""

    s = text

    # 1) Collapse multiple newlines
    s = re.sub(r"\n{2,}", "\n", s)

    # 2) Remove spaces next to newlines
    s = re.sub(r"[ ]+\n", "\n", s)
    s = re.sub(r"\n[ ]+", "\n", s)

    # 3) Collapse space runs
    if collapse_internal_spaces:
        s = re.sub(r" {2,}", " ", s)

    # 4) Tibetan-specific space normalization
    if tibetan_specific:
        # Remove space after tsheg if followed by initial letter or shad
        s = re.sub(r"([\u0f0b\u0f0c\u0fd2]) +([\u0f40-\u0f6c\u0f0d-\u0f11])", r"\1\2", s)
        # Remove space between final letter and tsheg
        s = re.sub(r"([\u0f40-\u0fbc]) +([\u0f0b\u0f0c\u0fd2])", r"\1\2", s)

    return s

def normalize_corpus(
    text: str,
    strip_control: bool = True,
    collapse_internal_spaces: bool = True,
) -> str:
    """
    General-purpose Unicode normalization.

    Steps:
      1. Normalize to NFC.
      2. Convert all line breaks to '\n'.
      3. Remove zero-width / invisible characters (incl. all BOMs).
      4. Map Unicode spaces and tabs to plain ASCII space.
      5. Optionally remove control characters (except newline).
      6. Normalize spaces (including Tibetan-specific rules).
      7. Apply Tibetan Unicode normalization.

    Keeps ZWJ/ZWNJ (joiners) intact.
    """
    if not text:
        return ""

    # 1) NFC normalization
    s = unicodedata.normalize("NFC", text)

    # 2) Normalize line breaks
    s = _LINEBREAKS_RE.sub("\n", s)

    # 3) Remove zero-width & BOM
    s = s.translate(_ZERO_WIDTH_STRIP)

    # 4) Normalize spaces to ASCII space
    s = s.translate(_SPACE_TO_ASCII)

    # 5) Optionally strip control characters (but keep newline)
    if strip_control:
        s = "".join(
            ch for ch in s
            if ch == "\n" or (unicodedata.category(ch)[0] != "C")
        )

    # 6) Normalize spaces
    s = normalize_spaces(s, collapse_internal_spaces=collapse_internal_spaces)

    # 7) Tibetan Unicode normalization
    s = normalize_unicode(s)
    # no graphical distinction between 0f0b and 0f0c
    s = s.replace("\u0f0c", "\u0f0b")
    # double shad is just two shad
    s = s.replace("\u0f0e", "\u0f0d\u0f0d")

    return s


def _run_sanity_checks() -> None:
    """Lightweight checks exercising each normalization rule."""

    def _assert_equal(actual: str, expected: str, label: str) -> None:
        if actual != expected:
            raise AssertionError(f"{label} failed: {actual!r} != {expected!r}")

    # normalize_spaces: collapse newlines/spaces and trim around newlines
    _assert_equal(
        normalize_spaces("a\n\n b  \n c"),
        "a\nb\nc",
        "normalize_spaces basic spacing",
    )

    # normalize_spaces: Tibetan-specific spacing around tsheg and finals
    tibetan_sample = "\u0f0b \u0f40 \u0f66 \u0f0b"  # tsheg, initial, final, tsheg
    _assert_equal(
        normalize_spaces(tibetan_sample),
        "\u0f0b\u0f40 \u0f66\u0f0b",
        "normalize_spaces tibetan spacing",
    )

    # normalize_corpus: line breaks, zero-width strip, space mapping, control strip,
    # Tibetan Unicode tweaks (0f0c→0f0b, 0f0e→double shad)
    corpus_sample = "a\u00a0\u200b b\r\nc\u0f0c\u0f0e\u0001"
    _assert_equal(
        normalize_corpus(corpus_sample),
        "a b\nc\u0f0b\u0f0d\u0f0d",
        "normalize_corpus full pipeline",
    )


if __name__ == "__main__":
    _run_sanity_checks()
    print("corpus_normalization sanity checks passed")