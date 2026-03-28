import re
import unicodedata
from enum import Enum
from .unicode_normalization import normalize_unicode
from .standard_tibetan import is_standard_tibetan, split_into_stacks

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

    # 0) Map Unicode line endings to '\n', Unicode spaces/tabs to ASCII space
    s = _LINEBREAKS_RE.sub("\n", s)
    s = s.translate(_ZERO_WIDTH_STRIP)
    s = s.translate(_SPACE_TO_ASCII)

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

# U+0FD2 is excluded (NYIS TSHEG → converted to U+0F0B earlier).
# U+0FD5-U+0FD8 are svasti/auspicious signs, structurally identical to yig-mgo.
_YIG_MGO_START = r"\u0F01-\u0F07\u0F09\u0F0A\u0FD0\u0FD1\u0FD3-\u0FD8"
_PUNCT        = r"\u0F0D-\u0F14"
_LETTER       = r"\u0F40-\u0FBC"

# Compiled patterns for normalize_for_perplexity
_MULTI_TSHEG_RE      = re.compile(r"\u0F0B{2,}")
_LETTER_BEFORE_NL_RE = re.compile(rf"([{_LETTER}])\n")
_YIG_MGO_RE          = re.compile(rf"[{_YIG_MGO_START}]+[{_PUNCT}]*")
# Tibetan digits U+0F20-U+0F33, ASCII digits, comma as thousands-separator
_DIGIT_RUN_RE        = re.compile(r"[0-9\u0F20-\u0F33][0-9\u0F20-\u0F33,]*")
# Keep only Tibetan block (U+0F00-U+0FFF), ASCII space, and the digit placeholder D
_NON_TIBETAN_RE      = re.compile(r"[^\u0F00-\u0FFF D]")
_PUNCT_OR_SPACE_RE   = re.compile(rf"[{_PUNCT} ]+")
_LETTER_SPACE_RE     = re.compile(rf"([{_LETTER}]) ")
_LETTER_SPACE_REPL   = r"\1" + "\u0F0B "  # backreference + literal tsheg + space
# space_after_tshegs: any punct-containing run → single shad surrounded by spaces
_PUNCT_RUN_RE        = re.compile(rf"[ ]*[{_PUNCT}][{_PUNCT} ]*")
_MULTI_SPACE_RE      = re.compile(r" {2,}")
# Split on tsheg or space while capturing the delimiter
_TSHEG_OR_SPACE_RE   = re.compile(r"(\u0F0B| )")
# space_after_tshegs: insert a space after any tsheg not already followed by one
_TSHEG_NO_SPACE_RE   = re.compile(r"\u0F0B(?! )")


def _process_sskt(text: str, space_sskt: bool, fold_sskt: bool) -> str:
    """Process non-standard (Sanskrit) syllables at the tsheg-delimited level.

    Tshegs (U+0F0B) are the syllable separators within a sentence; spaces
    mark sentence/clause boundaries.  The function walks each tsheg-delimited
    piece and, for non-standard syllables:

    * ``space_sskt``: expands the syllable into its constituent stacks, each
      followed by a tsheg, with spaces between stacks.
    * ``fold_sskt``: accumulates consecutive non-standard syllables and
      replaces the whole run with the placeholder ``S``.
    """
    parts = _TSHEG_OR_SPACE_RE.split(text)
    # parts alternates: [content₀, delim₀, content₁, delim₁, …, contentₙ]
    out: list[str] = []
    in_sskt_run = False

    def flush_sskt() -> None:
        nonlocal in_sskt_run
        if in_sskt_run:
            out.append(" S")
            in_sskt_run = False

    n = len(parts)
    for i in range(0, n, 2):
        content = parts[i]
        delim   = parts[i + 1] if i + 1 < n else ""

        if not content:
            if delim == " " and fold_sskt:
                flush_sskt()
            if delim:
                out.append(delim)
            continue

        has_tibetan = any(0x0F40 <= ord(c) <= 0x0FBC for c in content)

        if not has_tibetan:
            if fold_sskt:
                flush_sskt()
            out.append(content)
            if delim:
                out.append(delim)
            continue

        std = is_standard_tibetan(content)

        if std:
            if fold_sskt and in_sskt_run:
                flush_sskt()
                out.append(" ")
            out.append(content)
            if delim:
                out.append(delim)
        else:
            if fold_sskt:
                in_sskt_run = True
                if delim == " ":
                    flush_sskt()
                    out.append(delim)
            elif space_sskt:
                stacks = split_into_stacks(content)
                out.append(" ".join(s + "\u0F0B" for s in stacks))
                if delim == " ":
                    out.append(delim)
                # tsheg delimiter absorbed as the tsheg of the last stack
            else:
                out.append(content)
                if delim:
                    out.append(delim)

    if fold_sskt:
        flush_sskt()

    result = "".join(out)
    return _MULTI_SPACE_RE.sub(" ", result)


def normalize_for_perplexity(
    text: str,
    space_after_tshegs: bool = False,
    space_sskt: bool = False,
    fold_sskt: bool = False,
) -> str:
    """
    Normalize Tibetan text for perplexity calculation.

    Parameters
    ----------
    text:
        Input text.
    space_after_tshegs:
        If ``True``, punctuation sequences are replaced by a shad (``།``)
        surrounded by spaces instead of a plain space, making sentence
        boundaries explicit.  Each syllable then ends with ``་ `` (tsheg +
        space).
    space_sskt:
        If ``True``, non-standard (Sanskrit) syllables are split into their
        constituent stacks, each receiving its own tsheg.  Recommended
        together with ``space_after_tshegs``.
    fold_sskt:
        If ``True``, consecutive runs of non-standard (Sanskrit) syllables
        are collapsed to the single placeholder token ``S``.  Takes
        precedence over ``space_sskt`` when both are set.

    Steps applied after ``normalize_corpus``:
      1.  Replace NYIS TSHEG (U+0FD2) with TSHEG (U+0F0B); fold runs of
          consecutive TSHEGs to one.
      2.  Remove honorific particles U+0F35 / U+0F37 and TSA-PHRU (U+0F39).
      3.  Normalize nasalization marks: NYI ZLA (U+0F82) and SNA LDAN
          (U+0F83) → RJES SU NGA RO (U+0F7E).
      4.  Where a Tibetan letter (U+0F40-U+0FBC) is followed by a newline,
          insert a space to preserve the syllable boundary.
      5.  Remove all remaining newlines.
      6.  Remove yig-mgo opening marks (U+0F01-U+0F07, U+0F09, U+0F0A,
          U+0FD0, U+0FD1, U+0FD3-U+0FD8 incl. svasti signs) together with
          any trailing punctuation (U+0F0D-U+0F14).
      7.  Replace runs of digits (Tibetan U+0F20-U+0F33 and ASCII 0-9,
          with commas) with the placeholder ``D``.
      8.  Strip any character outside the Tibetan Unicode block (U+0F00-
          U+0FFF), keeping spaces and the ``D`` placeholder.
      9.  Collapse punctuation / space runs:
            - default: to a single space.
            - space_after_tshegs: punct-containing runs → `` ། ``
              (shad surrounded by spaces); remaining space runs collapsed.
      9b. (space_sskt / fold_sskt) Process non-standard syllable tokens.
      10. Ensure every syllable-final letter before a space carries a TSHEG:
          letter + space → letter + U+0F0B + space.
      11. Strip leading/trailing whitespace.
    """
    text = normalize_corpus(text)

    # 1) NYIS TSHEG → TSHEG, then collapse runs of TSHEG to one
    text = text.replace("\u0FD2", "\u0F0B")
    text = _MULTI_TSHEG_RE.sub("\u0F0B", text)

    # 2) Remove honorific particles and TSA-PHRU flourish
    text = text.translate({ord("\u0F35"): None, ord("\u0F37"): None, ord("\u0F39"): None})

    # 3) Normalize nasalization marks to RJES SU NGA RO (U+0F7E)
    text = text.replace("\u0F82", "\u0F7E").replace("\u0F83", "\u0F7E")

    # 4) Letter before newline → letter + space + newline
    text = _LETTER_BEFORE_NL_RE.sub(r"\1 \n", text)

    # 5) Drop all newlines
    text = text.replace("\n", "")

    # 6) Drop yig-mgo / svasti opening marks (+ optional trailing punctuation)
    text = _YIG_MGO_RE.sub("", text)

    # 7) Replace digit runs (Tibetan + ASCII, with commas) → placeholder D
    text = _DIGIT_RUN_RE.sub("D", text)

    # 8) Strip characters outside the Tibetan block (keep D placeholder and spaces)
    text = _NON_TIBETAN_RE.sub(" ", text)

    # 9) Collapse punctuation / space runs
    if space_after_tshegs:
        text = _PUNCT_RUN_RE.sub(" \u0F0D ", text)
        text = _MULTI_SPACE_RE.sub(" ", text)
    else:
        text = _PUNCT_OR_SPACE_RE.sub(" ", text)

    # 9b) Sanskrit syllable handling
    if space_sskt or fold_sskt:
        text = _process_sskt(text, space_sskt, fold_sskt)

    # 9c) In space_after_tshegs mode, guarantee a space follows every tsheg
    if space_after_tshegs:
        text = _TSHEG_NO_SPACE_RE.sub("\u0F0B ", text)

    # 10) Ensure syllable-final letters carry a TSHEG before any space
    text = _LETTER_SPACE_RE.sub(_LETTER_SPACE_REPL, text)

    return text.strip()

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