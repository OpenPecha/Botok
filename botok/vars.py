# coding: utf-8
from enum import IntEnum, Enum

OOV = "OOV"
NON_WORD = "NON_WORD"
TSEK = "་"
NAMCHE = "ཿ"
SHAD = "།"
AA = "འ"
HASH = "#"
VOWELS = ["ི"]
NO_SHAD_CONS = ["ཀ", "ག", "ཤ"]
DAGDRA = ["པ་", "པོ་", "བ་", "བོ་"]

CharMarkers = IntEnum(
    "CharMarkers",
    [
        # regular Tibetan
        "CONS",
        "SUB_CONS",
        "VOW",
        "TSEK",
        # punctuation
        "NORMAL_PUNCT",
        "SPECIAL_PUNCT",
        # others
        "NUMERAL",
        "SYMBOL",
        "IN_SYL_MARK",
        "NON_BO_NON_SKRT",
        # lexica_skrt
        "SKRT_CONS",
        "SKRT_SUB_CONS",
        "SKRT_VOW",
        "SKRT_LONG_VOW",
        # other languages
        "CJK",
        "LATIN",
        # misc
        "OTHER",
        "TRANSPARENT",
    ],
    start=1,
)
char_values = {c.value: c.name for c in CharMarkers}

ChunkMarkers = IntEnum(
    "ChunkMarkers",
    [
        # languages
        "BO",
        "LATIN",
        "CJK",
        "OTHER",
        # tibetan textual content
        "TEXT",
        # tibetan non-textual content
        "PUNCT",
        "NON_PUNCT",
        "SPACE",
        "NON_SPACE",
        "SYM",
        "NON_SYM",
        "NUM",
        "NON_NUM",
    ],
    start=100,
)
chunk_values = {c.value: c.name for c in ChunkMarkers}

WordMarkers = IntEnum("WordMarkers", ["WORD", "OOV", "NON_WORD"], start=1000)
word_values = {w.value: w.name for w in WordMarkers}

Ids = Enum("Ids", ["profile", "prep", "tok", "mod", "form"])
