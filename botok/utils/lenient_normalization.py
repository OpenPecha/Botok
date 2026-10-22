import re
from bisect import bisect_left

NEEDS_A = {
    "ག": {
        "ཅ": True,
        "ཉ": True,
        "ཏ": True,
        "ད": True,
        "ན": True,
        "ཙ": True,
        "ཞ": True,
        "ཟ": True,
        "ཡ": True,
        "ཤ": True,
        "ས": True,
    },
    "ད": {"ཀ": True, "ག": True, "ང": True, "པ": True, "བ": True, "མ": True},
    "བ": {
        "ཀ": True,
        "ག": True,
        "ཅ": True,
        "ཏ": True,
        "ད": True,
        "ཙ": True,
        "ཞ": True,
        "ཟ": True,
        "ཤ": True,
        "ས": True,
    },
    "མ": {
        "ཁ": True,
        "ག": True,
        "ང": True,
        "ཆ": True,
        "ཇ": True,
        "ཉ": True,
        "ཐ": True,
        "ད": True,
        "ན": True,
        "ཚ": True,
        "ཛ": True,
    },
    "འ": {
        "ཁ": True,
        "ག": True,
        "ཆ": True,
        "ཇ": True,
        "ཐ": True,
        "ད": True,
        "ཕ": True,
        "བ": True,
        "ཚ": True,
        "ཛ": True,
    },
}


def remove_affixes(s):
    # usual suffixes
    lens = len(s)
    s = re.sub(
        r"([\u0f40-\u0fbc])(?:འིའོ|འིའམ|འིའང|འོའམ|འོའང|འིས|འི|འོ|འམ|འང|འས|འད|འར)$",
        r"\1",
        s,
    )
    if len(s) != lens and len(s) > 1:
        # if a substitution has been made, make sure to add a suffix འ in the relevant cases:
        if s[-2] in NEEDS_A and s[-1] in NEEDS_A[s[-2]]:
            s += "འ"
    # remove འ suffix when not warranted
    if (
        len(s) > 2
        and s[-1] == "འ"
        and (s[-3] not in NEEDS_A or s[-2] not in NEEDS_A[s[-3]])
    ):
        s = s[:-1]
    s = s.replace("འུར", "འུ")
    s = s.replace("འུས", "འུ")
    # da drag
    s = re.sub(r"([^གམ][ནལར])ད$", r"\1", s)
    return s
    

# Normalization of Old Tibetan shorthands

# from Tibetan-nlp: Traditionally in Classical Tibetan, syllables are separated by a tsheg.
# In Old Tibetan texts, syllable margins are not so clear and often a syllable (verb, noun and so on)
# is merged together with the following case marker or converb
# (For example: སྟགི > སྟག་གི,  དུསུ > དུས་སུ,  བཀུམོ > བཀུམ་མོ).
# Rule: Split merged syllables for cases as དྲངསྟེ > དྲངས་ཏེ
#  ([ཀ-ྼ])སྟེ   -> $1ས་
OLD_TIB_P1 = re.compile(r"([ཀ-ྼ])སྟེ")

# from Tibetan-nlp:
# Rule: Split merged syllables for cases as གཅལྟོ > གཅལད་ཏོ
# ([ཀ-ྼ][ནལར])ྟ([ེོ])", "$1་ཏ$2
OLD_TIB_P2 = re.compile(r"([ཀ-ྼ][ནལར])ྟ([ེོ])")

# from Tibetan-nlp:
# Rule: Split merged syllables for cases with genitive as གགྀ་ > གག་གྀ་, པགི་ > པག་གི་
# (I need to include this rule otherwise these cases are not taken into account by the
# generic rules where the condition {2-6}C will skip them.
# On the other hand, in the generic rule, using a condition as {1-6}C
# will introduce errors since the rule will split words as "bshi"
# ([ཀ-ྼ])ག([ིྀ][^ཀ-ྼ])", "$1ག་ག$2
# the first character shouldn't be a valid prefix of ག  (which are ད, བ, མ and འ), see
# https://github.com/tibetan-nlp/tibcg3/issues/4
OLD_TIB_P3 = re.compile(r"([ཀ-ཐདྷ-ཕབྷཙ-ཟཡ-ྼ])ག([ིྀ][^ཀ-ྼ])")

# from Tibetan-nlp:
# Rule: Split merged syllables
# see also https://github.com/tibetan-nlp/tibcg3/issues/6
OLD_TIB_P4 = re.compile(r"([ཀ-ྼ][ཀ-ྼ]+)([ཀ-ཟཡ-ཬ])([ོེིྀུ])")


def normalize_old_tib(s):
    """
    Normalizes Old Tibetan strings into classical Tibetan
    /! should be applied before tokenization as it introduces tshegs
    """
    s = OLD_TIB_P1.sub(r"\1ས་ཏེ", s)
    s = OLD_TIB_P2.sub(r"\1་ཏ\2", s)
    s = OLD_TIB_P3.sub(r"\1ག་ག\2", s)
    s = OLD_TIB_P4.sub(r"\1\2་\2\3", s)
    s = s.replace("ོེ", "ོའི")
    s = s.replace("བགྱིསྣ", "བགྱིས་ན")
    s = s.replace("རབལ", "རབ་ལ")
    s = s.replace("མཆིསྣ", "མཆིས་ན")
    # s = s.replace("མོལ", "མོ་ལ") indicated in the doc, but would conflict with other things
    s = s.replace("ཐོགསླ", "ཐོག་སླ")
    s = s.replace("ལྕེབསའོ", "ལྕེབས་སོ")
    s = s.replace("གཤེགསའོ", "གཤེགས་སོ")
    s = s.replace("བཏགསའོ", "བཏགས་སོ")
    s = s.replace("ལསྩོགསྟེ", "ལ་སྩོགས་སྟེ")
    # builder.add("མའང", "མ་འང") indicated but more or less useless
    s = s.replace("མྱི", "མི")
    s = s.replace("མྱེ", "མེ")
    s = s.replace("གསྩན", "གསན")
    s = s.replace("གསྩང", "གསང")
    s = s.replace("སྩོགས", "སོགས")
    s = s.replace("སྩུབ", "སུབ")
    s = s.replace("སྩང", "སང")
    s = s.replace("སྩངས", "སངས")
    s = s.replace("གསྩུག", "གསུག")
    s = s.replace("བསྩག", "བསག")
    s = s.replace("མཀ", "མཁ")
    s = s.replace("མཅ", "མཆ")
    s = s.replace("མཏ", "མཐ")
    s = s.replace("མཙ", "མཚ")
    s = s.replace("འཀ", "འཁ")
    s = s.replace("འཅ", "འཆ")
    s = s.replace("འཏ", "འཐ")
    s = s.replace("འཔ", "འཕ")
    s = s.replace("འཙ", "འཚ")
    s = s.replace("དཁ", "དཀ")
    s = s.replace("དཕ", "དཔ")
    s = s.replace("གཆ", "གཅ")
    s = s.replace("གཐ", "གཏ")
    s = s.replace("གཚ", "གཙ")
    s = s.replace("བཁ", "བཀ")
    s = s.replace("བཆ", "བཅ")
    s = s.replace("བཐ", "བཏ")
    s = s.replace("བཚ", "བཙ")
    s = s.replace("སྑ", "སྐ")
    s = s.replace("སྠ", "སྟ")
    s = s.replace("སྥ", "སྤ")
    s = s.replace("སྪ", "སྩ")
    s = s.replace("རྑ", "རྐ")
    s = s.replace("རྪ", "རྩ")
    s = s.replace("རྠ", "རྟ")
    s = s.replace("ལྑ", "ལྐ")
    s = s.replace("ལྖ", "ལྕ")
    s = s.replace("ལྠ", "ལྟ")
    s = s.replace("ལྥ", "ལྤ")
    s = s.replace("པྱག", "ཕྱག")
    s = s.replace("པྱི", "ཕྱི")
    s = s.replace("པོ་ཉ", "ཕོ་ཉ")
    s = s.replace("དམག་ཕོན", "དམག་དཔོན")
    s = s.replace("པོག་པ", "ཕོག་པ")
    s = s.replace("ཕོ་བྲང", "པོ་བྲང")
    s = s.replace("བལ་ཕོ", "བལ་པོ")
    s = s.replace("ཕལ་ཕོ", "ཕལ་པོ")
    s = s.replace("རྩང་ཅེན", "རྩང་ཆེན")
    s = s.replace("ལོ་ཕར", "ལོ་པར")
    s = s.replace("བློན་ཅེ", "བློན་ཆེ")
    s = s.replace("ཞལ་ཅེ", "ཞལ་ཆེ")
    s = s.replace("མེར་ཁེ", "མེར་ཀེ")
    s = s.replace("ལོ་ཆིག", "ལོ་གཅིག")
    s = s.replace("ཆེད་པོ", "ཆེན་པོ")
    s = s.replace("ཅེད་པོ", "ཆེན་པོ")
    s = s.replace("ཅེན་པོ", "ཆེན་པོ")
    return s

def normalize_lenient(s):
    # remove some marks
    s = re.sub(r"[\u0f35\u0f37\u0f39]", "", s)
    # retroflex -> dental
    s = s.replace("ཊ", "ཏ")
    s = s.replace("ཋ", "ཐ")
    s = s.replace("ཌ", "ད")
    s = s.replace("ཎ", "ན")
    s = s.replace("ྚ", "ྟ")
    s = s.replace("ྛ", "ྠ")
    s = s.replace("ྜ", "ྡ")
    s = s.replace("ྞ", "ྣ")
    s = s.replace("ཥ", "ཤ")
    s = s.replace("ྵ", "ྴ")  # requires NFD
    # normalize non-semantic graphical variation
    s = s.replace("ྻ", "ྱ")
    s = s.replace("ྼ", "ྲ")
    s = s.replace("ཪ", "ར")
    # a common Sanskrit normalization is r+repeated consonnant
    s = re.sub(r"ར([\u0f90-\u0fbc])\1", r"ར\1", s)
    # anusvara / anunasika normalization
    s = s.replace("\u0f82", "\u0f7e")
    s = s.replace("\u0f83", "\u0f7e")
    s = s.replace("\u0f86", "\u0f7e")
    # normalize gigus
    s = s.replace("\u0f80", "\u0f72")  # requires NFD
    # remove achung and wasur
    s = s.replace("ཱ", "")
    s = s.replace("ྺ", "")
    s = s.replace("ྭ", "")
    return s

def remove_punctuation(s):
    # we assume that Unicode normalization already took place
    s = re.sub(r"[\s\u0f0b\u0fd2]", "", s)
    return s


def normalize_ngatadara(s):
    """
    The Tibetan letters ང, ཏ, ད and ར are often difficult to differentiate
    visually in block prints or poor quality manuscripts, and are often
    confused in manual inputs or OCRs. This function detects some common cases
    of confusion and fixes them. Note that this function assumes that the text
    is Classical Tibetan or the commonly found Sanskrit words, it may very well
    not work for uncommon Sanskrit words.
    """
    s = re.sub(r"(?:དྙ|ངྙ|ཏྙ)", r"རྙ", s)
    s = re.sub(r"^བལྔ", "བལྡ", s)
    s = re.sub(r"(?:ངྲ|རྲ)", "དྲ", s)
    s = re.sub(r"^འ[རངཏ]([\u0f40-\u0fbc])", r"འད\1", s)
    # case where prefix da is read as ra, nga or ta, with a special case for second suffix sa
    s = re.sub(r"^[རངཏ]([བམཀགཔང])([\u0f40-\u0f65\u0f67-\u0fbc])", r"ད\1\2", s)
    s = re.sub(r"(?:དླ|ཏླ|ངླ)", r"རླ", s)
    # TODO: common mistakes in Sanskrit stacks
    # d+n, ng+n -> t+n
    # ng+ng | d+ng | ng+d -> d+d
    return s

def normalize_graphical(s):
    """
    These substitutions normalize things that have the same
    graphical representation
    """
    # no graphical distinction between 0f0b and 0f0c
    s = s.replace("\u0f0c", "\u0f0b")
    # double shad is just two shad
    s = s.replace("\u0f0e", "\u0f0d\u0f0d")
    # the distinction between 0f38 and 0f27 is semantic but rarely
    # distinguished graphically and often completely missed by inputters
    s = s.replace("\u0f38", "\u0f27")
    # /!\ some fonts don't display these combinations in the exact same way
    # but since there's no semantic distinction and the graphical variation
    # is unclear, it seems safe
    s = s.replace("\u0f7a\u0f7a", "\u0f7b")
    s = s.replace("\u0f7c\u0f7c", "\u0f7d")
    s = s.replace("༇", "࿓།࿒།")
    # the diference between 0f71 and 0fb0 is often very ambiguous when
    # looking at original sources. We normalize them in order to
    # make the data coherent:
    # no 0f71 in the middle of stacks, only 0fb0
    s = re.sub(r"[\u0f71]([\u0f8d-\u0fac\u0fae\u0fb0\u0fb3-\u0fbc])", "\u0fb0\\1", s)
    # no 0fb0 at the end of stacks, only 0f71
    s = re.sub(r"[\u0fb0]([^\u0f8d-\u0fac\u0fae\u0fb0\u0fb3-\u0fbc]|$)", "\u0f71\\1", s)
    # things we do not normalize:
    # 0f74+0f71 -> 0f71+0f74, because the combination appears sometimes in the sources
    # for instance སུྰ in https://adarsha.dharma-treasure.org/kdbs/jiangkangyur/pbs/2618229
    # same for 0fb1+0f71 since the combination also appears
    # for instance སཱྱ on https://adarsha.dharma-treasure.org/kdbs/jiangkangyur?pbId=2627013
    return s


# Punctuation normalization
#
# The output follows modern Tibetan typography, see
# https://www.w3.org/TR/tlreq/ (§7.1.2), https://www.unicode.org/L2/L2025/25207-shay.pdf
# and https://digitaltibetan.github.io/DigitalTibetan/docs/tibetan_formatting.html :
#   - single shad followed by a space (X། Y), double shad followed by the text (X། །Y)
#   - a final ཀ, ག or ཤ (also with a vowel, not with a subscript or superscript) carries
#     the first shad: ག Y (single), ག །Y (double)
#   - tsheg before a shad only after ང (ང་།)
#   - yig mgo only at the beginning of the text (༄༅། །)
# Every rule is a regex substitution; positions are tracked so that offsets in the
# original string can be mapped to the normalized one (see remap_offsets()).

_P_LETTER = "\u0f40-\u0fbc"
_P_ROOT = "\u0f40-\u0f6c"
_P_VOWELS = "\u0f71-\u0f87"
_P_VOWELS_NO_VISARGA = "\u0f71-\u0f7e\u0f80-\u0f87"
_P_YIG_MGO = "\u0f01-\u0f08\u0f09\u0f0a\u0fd0\u0fd1\u0fd3\u0fd4"  # includes sbrul shad 0f08
_P_OPENING = "\u0f04\u0f05\u0f0d \u0f0d"


def _p_at_eol(m):
    return m.end() == len(m.string) or m.string[m.end()] == "\n"


def _p_yig_mgo(m):
    return _P_OPENING if m.group(1) is not None else ""


def _p_join_lines(m):
    # used when original_eol=False: a line ending in ཀ/ག/ཤ without tsheg carries a shad,
    # a line ending in another letter is closed by a tsheg
    prev = m.string[m.start() - 1] if m.start() else ""
    nxt = m.string[m.end()] if m.end() < len(m.string) else ""
    if m.group(1):
        return m.group(1) + (" " if nxt else "")
    if re.match(f"[{_P_LETTER}]", prev) and re.match(f"[{_P_ROOT}]", nxt):
        return "\u0f0b"
    return ""


def _p_gter_shad(m):
    # the shads of the opening ༄༅། ། stay
    return m.group(0) if m.string.startswith(_P_OPENING) and m.start() < len(_P_OPENING) else "\u0f14"


def _p_shad_cluster(m):
    ka_ga_sha, space, shads = m.group(1), m.group(2), m.group(3)
    n = 1 if shads == "\u0f0d" else 2
    if ka_ga_sha:
        # the stroke of ཀ/ག/ཤ is the first shad: ག། and ག་། are a single shad, ག ། a double
        n = min(2, n + bool(space))
        return ka_ga_sha + (" \u0f0d" if n == 2 else "" if _p_at_eol(m) else " ")
    return shads + (" " if n == 1 and not _p_at_eol(m) else "")


# (name, pattern, replacement). Order matters.
_PUNCT_RULES_START = (
    ("tsheg_variants", "[\u0f0c\u0fd2]", "\u0f0b"),
    ("shad_variants", "[\u0f0f\u0f10\u0f11\u0f12]", "\u0f0d"),
    ("nyis_shad", "\u0f0e", "\u0f0d\u0f0d"),
    ("line_breaks", r"\r\n?", "\n"),
    ("spaces", r"[ \t\u00a0\u2000-\u200b\u3000]+", " "),
    ("space_around_newline", r" *\n *", "\n"),
    ("tsheg_runs", "\u0f0b{2,}", "\u0f0b"),
    ("space_after_tsheg", f"\u0f0b +(?=[{_P_LETTER}\u0f0d])", "\u0f0b"),
    ("space_before_tsheg", f"(?<=[{_P_LETTER}]) +\u0f0b", "\u0f0b"),
    ("yig_mgo", f"(\\A\\s*)?(?:[{_P_YIG_MGO}][{_P_YIG_MGO}{_P_VOWELS}]*[ \u0f0b\u0f0d]*)+", _p_yig_mgo),
)
_PUNCT_RULE_JOIN = ("join_lines", f"([ཀགཤ][{_P_VOWELS_NO_VISARGA}]*)?\n+", _p_join_lines)
_PUNCT_RULE_GTER = ("gter_shad", "(?<=[^\\s\u0f0d]) *\u0f0d(?: \u0f0d)?", _p_gter_shad)
_PUNCT_RULES_END = (
    ("double_shad", "\u0f0d(?: *\u0f0d)+", "\u0f0d \u0f0d"),
    ("tsheg_before_shad",
     f"(?<!ང)(?<!ང[{_P_VOWELS_NO_VISARGA}])\u0f0b+(?=\u0f0d)|\u0f0b+(?=\u0f14)", ""),
    ("shad_spacing",
     f"(?:([ཀགཤ][{_P_VOWELS_NO_VISARGA}]*)|(?<=[^\\s\u0f0d]))( *)(\u0f0d(?: \u0f0d)?) *",
     _p_shad_cluster),
    ("nga_tsheg_shad", f"(ང[{_P_VOWELS_NO_VISARGA}]*)(?=\u0f0d)", "\\1\u0f0b"),
    ("gter_tsheg", "\u0f14(?: *\u0f14)* *", "\u0f14 "),
    ("visarga_tsheg", "\u0f7f\u0f0b", "\u0f7f"),
    ("trailing_space", r" +(?=\n|\Z)", ""),
)


def _punct_rules(use_gter_shad, original_eol):
    rules = list(_PUNCT_RULES_START)
    if not original_eol:
        rules.append(_PUNCT_RULE_JOIN)
    rules += _PUNCT_RULES_END[:1]  # double_shad
    if use_gter_shad:
        rules.append(_PUNCT_RULE_GTER)
    rules += _PUNCT_RULES_END[1:]
    return [(name, re.compile(p), r) for name, p, r in rules]


_PUNCT_COMPILED = {(g, e): _punct_rules(g, e) for g in (False, True) for e in (False, True)}


def normalize_punctuation(s, use_gter_shad=False, original_eol=True, return_positions=False):
    """
    Normalize Tibetan punctuation (see the rules above).

    - original_eol: keep line breaks (default); if False, lines are joined
    - use_gter_shad: write shads as gter tsheg ༔ (no ཀ/ག/ཤ convention then)
    - return_positions: return (text, pos, counts) where pos[j] is the offset in s
      that produced character j of text (with a final sentinel len(s), non-decreasing)
      and counts the number of changes made by each rule
    """
    pos = list(range(len(s) + 1))
    counts = {}
    for name, rx, repl in _PUNCT_COMPILED[(use_gter_shad, original_eol)]:
        out, new_pos, last, n = [], [], 0, 0
        for m in rx.finditer(s):
            r = repl(m) if callable(repl) else m.expand(repl)
            if r == m.group(0):
                continue
            out.append(s[last:m.start()])
            new_pos.extend(pos[last:m.start()])
            out.append(r)
            new_pos.extend([pos[m.start()]] * len(r))
            last = m.end()
            n += 1
        if n:
            out.append(s[last:])
            new_pos.extend(pos[last:len(s)])
            new_pos.append(pos[len(s)])
            s, pos = "".join(out), new_pos
            counts[name] = n
    if return_positions:
        return s, pos, counts
    return s


def remap_offsets(offsets, pos):
    """Map offsets in the original string to offsets in the normalized string,
    using the pos list returned by normalize_punctuation(..., return_positions=True)."""
    n = len(pos) - 1
    return [min(bisect_left(pos, o, 0, n), n) for o in offsets]

def test_normalize_old_tib(s):
    assert normalize_old_tib("དྲངསྟེ") == "དྲངས་ཏེ"
    assert normalize_old_tib("གཅལྟོ") == "ཅལད་ཏོ"
    assert normalize_old_tib("གགྀ་") == "གག་གྀ་"