from pathlib import Path
import csv
from collections import defaultdict

from ..vars import CharMarkers as c

# Get the categories of Tibetan characters from the csv file
categories = defaultdict(list)
table_path = Path(__file__).parent.parent / "resources/bo_uni_table.csv"
for row in list(csv.reader(table_path.open(encoding="utf-8-sig")))[1:]:
    char = row[1].replace("—", "")
    cat = c[row[2]].value
    categories[cat].append(char)

# all unicode chars liable to be used as spaces or that allowed in a valid Tibetan string
# yet that will be ignored when read by a human.
transparent = [
    " ",  # \U32 SPACE
    "᠎",  # \U6158 MONGOLIAN VOWEL SEPARATOR
    " ",  # \U8192 EN QUAD
    " ",  # \U8193 EM QUAD
    " ",  # \U8194 EN SPACE
    " ",  # \U8195 EM SPACE
    " ",  # \U8196 THREE-PER-EM SPACE
    " ",  # \U8197 FOUR-PER-EM SPACE
    " ",  # \U8198 SIX-PER-EM SPACE
    " ",  # \U8199 FIGURE SPACE
    " ",  # \U8200 PUNCTUATION SPACE
    " ",  # \U8201 THIN SPACE
    " ",  # \U8202 HAIR SPACE
    "​",  # \U8203 ZERO WIDTH SPACE
    " ",  # \U8239 NARROW NO-BREAK SPACE
    " ",  # \U8287 MEDIUM MATHEMATICAL SPACE
    "　",  # \U12288 IDEOGRAPHIC SPACE
    "﻿",  # \U65279 ZERO WIDTH NO-BREAK SPACE
    "\t",  # Tabulation
    "\n",  # carriage return can happen in the middle of a word
]


def get_char_category(char):
    # source for codepoints: https://jrgraphix.net/research/unicode.php
    if char in transparent:
        return c.TRANSPARENT.value

    # Tibetan range
    if "\u0f00" <= char <= "\u0fff":
        for cat, chars in categories.items():
            if char in chars:
                return cat
        raise ValueError(
            f'The char "{char}" is expected to be in the tibetan table, but is not.'
        )

    # CJK range
    elif (
        "\u2e80" <= char <= "\ufaff"
        or "\ufe30" <= char <= "\ufe4f"
        or eval('"\u20000"') <= char <= eval('"\u2fa1f"')
    ):
        return c.CJK.value

    # LATIN range
    # 1. 0020 - 036f:  Latin Basic + Latin-1 Supplement + Latin Extended-A + Latin Extended-B
    # IPA Extensions + Spacing Modifier Letters + Combining Diacritical Marks
    # 2. 1e00 - 20cf: Latin Extended Additional + Superscripts and Subscripts + Currency Symbols
    elif "\u0020" <= char <= "\u036f" or "\u1e00" <= char <= "\u20cf":
        return c.LATIN.value

    else:
        return c.OTHER.value
