"""
Standard-Tibetan syllable validation and stack splitting.

This is a Python port of the ``isStandardTibetan`` / ``nextStackBreak`` logic
from the BDRC lucene-bo library:
https://github.com/buda-base/lucene-bo/blob/master/src/main/java/io/bdrc/lucene/bo/CommonHelpers.java

A syllable is *standard* if its onset (leading consonant cluster) matches one
of the entries in ``_ONSET_SET`` and the remainder matches a vowel+coda from
``_VOWEL_CODA_SET`` (or there is no remainder at all, which is valid).

Non-standard syllables are typically Sanskrit transliterations that use
additional vowel marks (e.g., U+0F71 ā-chen) not found in Classical Tibetan.
"""

# ---------------------------------------------------------------------------
# Valid onsets (consonant clusters that can begin a standard Tibetan syllable)
# ---------------------------------------------------------------------------
_ONSET_SET: frozenset[str] = frozenset({
    # ka family
    "ཀ", "ཀྱ", "ཀྲ", "ཀླ",
    "དཀ", "དཀྱ", "དཀྲ",
    "བཀ", "བཀྱ", "བཀྲ", "བཀླ",
    "རྐ", "རྐྱ", "ལྐ",
    "སྐ", "སྐྱ", "སྐྲ",
    "བརྐ", "བརྐྱ", "བསྐ", "བསྐྱ", "བསྐྲ",
    # kha family
    "ཁ", "ཁྱ", "ཁྲ",
    "མཁ", "མཁྱ", "མཁྲ",
    "འཁ", "འཁྱ", "འཁྲ",
    # ga family
    "ག", "གྱ", "གྲ", "གླ",
    "དག", "དགྱ", "དགྲ",
    "བག", "བགྱ", "བགྲ",
    "མག", "མགྱ", "མགྲ",
    "འག", "འགྱ", "འགྲ",
    "རྒ", "རྒྱ", "ལྒ",
    "སྒ", "སྒྱ", "སྒྲ",
    "བརྒ", "བརྒྱ", "བསྒ", "བསྒྱ", "བསྒྲ",
    # nga family
    "ང",
    "དང", "མང",
    "རྔ", "ལྔ", "སྔ", "བརྔ", "བསྔ",
    # ca family
    "ཅ", "གཅ", "བཅ", "ལྕ",
    # cha family
    "ཆ", "མཆ", "འཆ",
    # ja family
    "ཇ", "མཇ", "འཇ", "རྗ", "ལྗ", "བརྗ",
    # nya family
    "ཉ", "གཉ", "མཉ", "རྙ", "སྙ", "བརྙ", "བསྙ",
    # ta family
    "ཏ", "གཏ", "བཏ",
    "རྟ", "ལྟ", "སྟ",
    "བརྟ", "བལྟ", "བསྟ",
    # tha family
    "ཐ", "མཐ", "འཐ",
    # da family
    "ད", "དྲ",
    "གད", "བད", "མད",
    "འད", "འདྲ",
    "རྡ", "ལྡ", "སྡ",
    "བརྡ", "བལྡ", "བསྡ",
    # na family
    "ན", "གན", "མན", "རྣ", "སྣ", "བརྣ", "བསྣ",
    # pa family
    "པ", "པྱ", "པྲ",
    "དཔ", "དཔྱ", "དཔྲ",
    "ལྤ",
    "སྤ", "སྤྱ", "སྤྲ",
    # pha family
    "ཕ", "ཕྱ", "ཕྲ",
    "འཕ", "འཕྱ", "འཕྲ",
    # ba family
    "བ", "བྱ", "བྲ", "བླ",
    "དབ", "དབྱ", "དབྲ",
    "འབ", "འབྱ", "འབྲ",
    "རྦ", "ལྦ",
    "སྦ", "སྦྱ", "སྦྲ",
    # ma family
    "མ", "མྱ",
    "དམ", "དམྱ",
    "རྨ", "རྨྱ",
    "སྨ", "སྨྱ",
    # tsa family
    "ཙ", "གཙ", "བཙ", "རྩ", "སྩ", "བརྩ", "བསྩ",
    # tsha family
    "ཚ", "མཚ", "འཚ",
    # dza family
    "ཛ", "མཛ", "འཛ", "རྫ", "བརྫ",
    # wa
    "ཝ",
    # zha family
    "ཞ", "གཞ", "བཞ",
    # za family
    "ཟ", "ཟླ", "གཟ", "བཟ", "བཟླ",
    # 'a
    "འ",
    # ya family
    "ཡ", "གཡ",
    # ra family
    "ར", "རླ", "བརླ",
    # la
    "ལ",
    # sha family
    "ཤ", "གཤ", "བཤ",
    # sa family
    "ས", "སྲ", "སླ", "གས", "བས", "བསྲ", "བསླ",
    # ha family
    "ཧ", "ཧྲ", "ལྷ",
    # a (vowel carrier)
    "ཨ",
    # additional / extended clusters
    "བགླ",
    "མྲ", "སྨྲ",
    "ཏྲ", "ཐྲ",
    "སྣྲ",
    # wa-zur clusters
    "ཀྭ", "བཀྭ", "ཁྭ", "གྭ", "གྲྭ",
    "བཅྭ", "ཉྭ",
    "ཏྭ", "ཐྭ", "དྭ", "དྲྭ",
    "ཕྱྭ", "མྭ",
    "ཙྭ", "རྩྭ", "ཚྭ", "ཛྭ",
    "ཞྭ", "ཟྭ",
    "རྭ", "ལྭ", "ལྷྭ", "ཤྭ",
    "སྟྭ", "སྭ", "བསྭ",
    "ཧྭ",
})

# ---------------------------------------------------------------------------
# Valid vowel + final consonant (coda) suffixes
# ---------------------------------------------------------------------------
_VOWEL_CODA_SET: frozenset[str] = frozenset({
    # no vowel / no coda
    "",
    # coda only (a-vowel implicit)
    "འ", "ག", "གས", "ང", "ངས", "ད", "ན", "བ", "བས", "མ", "མས", "ལ",
    # a-vowel + particle
    "འི", "འིའོ", "འོ", "འང", "འམ", "ར", "ས",
    # i vowel
    "ི",
    "ིག", "ིགས", "ིང", "ིངས", "ིད", "ིན", "ིབ", "ིབས", "ིམ", "ིམས", "ིལ",
    "ིའི", "ིའིའོ", "ིའོ", "ིའང", "ིའམ", "ིར", "ིས",
    # u vowel
    "ུ",
    "ུག", "ུགས", "ུང", "ུངས", "ུད", "ུན", "ུབ", "ུབས", "ུམ", "ུམས", "ུལ",
    "ུའི", "ུའིའོ", "ུའོ", "ུའང", "ུའམ", "ུར", "ུས",
    # e vowel
    "ེ",
    "ེག", "ེགས", "ེང", "ེངས", "ེད", "ེན", "ེབ", "ེབས", "ེམ", "ེམས", "ེལ",
    "ེའི", "ེའིའོ", "ེའོ", "ེའང", "ེའམ", "ེར", "ེས",
    # o vowel
    "ོ",
    "ོག", "ོགས", "ོང", "ོངས", "ོད", "ོན", "ོབ", "ོབས", "ོམ", "ོམས", "ོལ",
    "ོའི", "ོའིའོ", "ོའོ", "ོའང", "ོའམ", "ོར", "ོས",
    # 'u (contracted u, from འུ)
    "འུ", "འུའི", "འུའིའོ", "འུའོ", "འུའང", "འུའམ", "འུར", "འུས",
    # i + 'u combinations
    "ིའུ", "ིའུའི", "ིའུའིའོ", "ིའུའོ", "ིའུའང", "ིའུའམ", "ིའུར", "ིའུས",
    # u + 'u combinations
    "ུའུ", "ུའུའི", "ུའུའིའོ", "ུའུའོ", "ུའུའང", "ུའུའམ", "ུའུར", "ུའུས",
    # e + 'u combinations
    "ེའུ", "ེའུའི", "ེའུའིའོ", "ེའུའོ", "ེའུའང", "ེའུའམ", "ེའུར", "ེའུས",
    # o + 'u combinations
    "ོའུ", "ོའུའི", "ོའུའིའོ", "ོའུའོ", "ོའུའང", "ོའུའམ", "ོའུར", "ོའུས",
})

_MAX_ONSET_LEN: int = max(len(s) for s in _ONSET_SET if s)   # 4
_MAX_VCODA_LEN: int = max(len(s) for s in _VOWEL_CODA_SET if s)  # 7


def _find_longest_prefix(text: str, start: int, candidates: frozenset, max_len: int) -> int:
    """Return end-position of the longest prefix of ``text[start:]`` that is
    in *candidates*, or ``-1`` if no prefix matches."""
    end = len(text)
    for length in range(min(max_len, end - start), 0, -1):
        if text[start : start + length] in candidates:
            return start + length
    return -1


def is_standard_tibetan(syllable: str) -> bool:
    """Return ``True`` if *syllable* (without trailing tsheg) is formed
    according to Standard Tibetan orthographic rules.

    The algorithm matches the Java ``isStandardTibetan`` in CommonHelpers:
    1. The onset (leading consonant cluster) must be in ``_ONSET_SET``.
    2. The remainder must be in ``_VOWEL_CODA_SET`` (including empty string).
    """
    if not syllable:
        return False
    onset_end = _find_longest_prefix(syllable, 0, _ONSET_SET, _MAX_ONSET_LEN)
    if onset_end == -1:
        return False
    if onset_end == len(syllable):
        return True
    coda_end = _find_longest_prefix(syllable, onset_end, _VOWEL_CODA_SET, _MAX_VCODA_LEN)
    return coda_end == len(syllable)


def _keepinstack(cp: int) -> bool:
    """Return ``True`` for code-points that are part of the current stack
    (i.e., combining / subjoined marks), not a new base consonant.

    Matches the Java ``keepinstack`` helper in CommonHelpers.
    """
    return (0x0F71 <= cp <= 0x0F87) or (0x0F8D <= cp <= 0x0FBC) or cp == 0x0F39


def split_into_stacks(syllable: str) -> list[str]:
    """Split a Tibetan syllable (without trailing tsheg) into its constituent
    stacks (akṣaras).

    Each stack is a base consonant followed by its subjoined consonants and
    vowel marks.  For standard Tibetan syllables this returns a list with a
    single element; for Sanskrit transliterations it may return multiple.

    Example::

        split_into_stacks("ཨཱཪྱ")  →  ["ཨཱ", "ཪྱ"]
    """
    stacks: list[str] = []
    i = 0
    n = len(syllable)
    while i < n:
        j = i + 1
        while j < n and _keepinstack(ord(syllable[j])):
            j += 1
        stacks.append(syllable[i:j])
        i = j
    return stacks
