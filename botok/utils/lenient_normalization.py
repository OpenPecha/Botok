import re

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


def normalize_punctuation(s, use_gter_shad=False, original_eol=True):
    # normalize spaces
    s = re.sub(r"\s+", " ", s)
    # we don't want to keep double tshegs (I suppose)
    s = s.replace("\u0fd2", "\u0f0b")
    # normalize end of line characters
    s = re.sub(r"(?:\r\n|\n)", "\n", s)
    if not original_eol:
        # 0f11 is just a normal shad that appears in some cases at the beginning of a page,
        # mostly when there is just one syllable before the shad on the first line, but it
        # has no semantic significance, it should be turned into a normal shad when combining
        # multiple texts
        s = s.replace("\u0f11", "\u0f0d")
        # remove all yig mgo: 0f01+diacritic?, 0f02-0f07, 0fd0-0fd1, 0fd3-0fd4
        # as well as their surrounding punctuation: space, 0f0d-0f11, 0f14
        s = re.sub(
            r"[ \u0f0d-\u0f11\u0f14]*[\u0f01-\u0f07\u0fd0\u0fd1\u0fd3\u0fd4]+[ \u0f0d-\u0f11\u0f14\u0f71-\u0f87]*",
            "",
            s,
        )
        # remove all punctuation at beginning of line
        s = re.sub(r"(^|[\n])[\u0f0b-\u0f14]+", "\\1", s)
        # ensure tsheg at end of line after normal letters, except after ཀ, ག and ཤ
        # (where the absence of a tsheg should be interpreted as the presence of a shad)
        s = re.sub(
            r"([\u0f41\u0f43-\u0f63\u0f65-\u0f6c][\u0f71-\u0fbc]*) *($|[\n])",
            "\\1\u0f0b\\2",
            s,
        )
        # ensure space after ཀ, ག and ཤ at end of line so that it merges well with the following one
        # remove line breaks and spaces at beginning of lines
        s = re.sub(r"([ཀགཤ][\u0f71-\u0f87]*)\n", "\\1 \n", s)
        s = re.sub(r"(?:\n) *", "", s)
    s = s.replace("\u0f14", "\u0f0d")
    # replace shads with surrounding spaces by a simple shad with a space after
    s = re.sub(r"[ \u0f0d]+", "\u0f0d ", s)
    # tshegs are sometimes used as padding, no need to keep it
    s = re.sub(r"[\u0f0b][\u0f0b]+", "\u0f0b", s)
    # remove tshegs before punctuation, including shad (no tsheg before gter shad)
    s = re.sub(r"[\u0f0b]([\u0f0d-\u0f14])", "\\1", s)
    # ensure space after shad
    s = re.sub(r"[\u0f0d]([^ ])", "\u0f0d \\1", s)
    # no tsheg after visarga
    s = s.replace("\u0f7f\u0f0b", "\u0f7f")
    if use_gter_shad:
        s = s.replace("\u0f0d", "\u0f14")
    else:
        # add tshegs before shad in some circumstances (after ང)
        s = re.sub(r"(ང[\u0f71-\u0f87]*)[\u0f0d]", "\\1\u0f0b\u0f0d", s)
        # remove shad after ཀ, ག and ཤ
        s = re.sub(r"([ཀགཤ][\u0f71-\u0f87]*)[\u0f0d]", "\\1", s)
    # normalize non-Tibetan punctuation into Chinese punctuation or Western punctuation (option?)
    # 〈〈?, 〈〈, 《, «, 〉〉?, », 》, 〉〉, ( ), ;, comma, dot, etc.
    # TODO
    # remove spaces: NO_SPACE_AFTER_PATTERN = re.compile(r"(?:\s|[༌་])$")
    # TODO
    return s

def test_normalize_old_tib(s):
    assert normalize_old_tib("དྲངསྟེ") == "དྲངས་ཏེ"
    assert normalize_old_tib("གཅལྟོ") == "ཅལད་ཏོ"
    assert normalize_old_tib("གགྀ་") == "གག་གྀ་"