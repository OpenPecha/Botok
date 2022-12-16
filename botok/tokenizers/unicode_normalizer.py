import re
from enum import Enum

class Cats(Enum):
    Other = 0
    Base = 1
    Subscript = 2
    BottomVowel = 3
    BottomMark = 4
    TopVowel = 5
    TopMark = 6
    RightMark = 7

CATEGORIES =  ([Cats.Other]           # 0F00
             + [Cats.Base]            # 0F01, often followed by 0f083
             + [Cats.Other] * 22      # 0F02-0F17
             + [Cats.BottomVowel] * 2 # 0F18-0F19
             + [Cats.Other] * 6       # 0F1A-0F1F
             + [Cats.Base] * 20       # 0F20-0F33, numbers can be followed by 0f18, 0f19 or exceptionally by vowels
             + [Cats.Other]           # 0F34
             + [Cats.BottomMark]      # 0F35
             + [Cats.Other]           # 0F36
             + [Cats.BottomMark]      # OF37
             + [Cats.Other]           # 0F38
             + [Cats.Subscript]       # 0F39, kind of cheating but works
             + [Cats.Other] * 4       # 0F3A-0F3D
             + [Cats.RightMark]       # 0F3E
             + [Cats.Other]           # 0F3F, not quite sure
             + [Cats.Base] * 45       # 0F40-0F6C
             + [Cats.Other] * 4       # 0F6D-0F70
             + [Cats.BottomVowel]     # 0F71
             + [Cats.TopVowel]        # 0F72
             + [Cats.TopVowel]        # 0F73
             + [Cats.BottomVowel] * 2 # 0F74-0F75
             + [Cats.TopVowel] * 8    # 0F76-0F7D
             + [Cats.TopMark]         # 0F7E
             + [Cats.RightMark]       # 0F7F
             + [Cats.TopVowel] * 2    # 0F80-0F81
             + [Cats.TopMark] * 2     # 0F82-0F83
             + [Cats.BottomMark]      # 0F84
             + [Cats.Other]           # 0F85
             + [Cats.TopMark] * 2     # 0F86-0F87
             + [Cats.Base] * 2        # 0F88-0F89
             + [Cats.Base]            # 0F8A always followed by 0f82 (required by the Unicode spec)
             + [Cats.Other]           # 0F8B
             + [Cats.Base]            # 0F8C
             + [Cats.Subscript] * 48  # 0F8D-0FBC
             )

def charcat(c):
    ''' Returns the category for a single char string'''
    o = ord(c)
    if 0x0F00 <= o <= 0x0FBC:
        return CATEGORIES[o-0x0F00]
    return Cats.Other

# debug:
#for i, c in enumerate(CATEGORIES):
#    print("%x : %d" % (0x0F00 + i , c.value))

def unicode_reorder(txt):
    # inpired from code for Khmer Unicode provided by SIL
    # https://docs.microsoft.com/en-us/typography/script-development/tibetan#reor
    # https://docs.microsoft.com/en-us/typography/script-development/use#glyph-reordering
    charcats = [charcat(c) for c in txt]
    # find subranges of base+non other and sort components in the subrange
    i = 0
    res = []
    valid = True
    while i < len(charcats):
        c = charcats[i]
        if c != Cats.Base:
            if c.value > Cats.Base.value:
                valid = False
            res.append(txt[i])
            i += 1
            continue
        # scan for end of component
        j = i + 1
        while j < len(charcats) and charcats[j].value > Cats.Base.value:
            j += 1
        # sort syllable based on character categories
        # sort the char indices by category then position in string
        newindices = sorted(range(i, j), key=lambda e:(charcats[e].value, e))
        replaces = "".join(txt[n] for n in newindices)
        res.append(replaces)
        i = j
    return "".join(res), valid

def normalize_unicode(s, form="nfd", graphical_normalization = True):
    # first, unify Unicode form:
    # http://www.unicode.org/faq/normalization.html
    # https://unicode.org/reports/tr15/
    # https://unicode.org/charts/normalization/chart_Tibetan.html
    # although for some reason this chart considers 0f0c -> 0f0b in NFD
    #
    # deprecated or discouraged characters
    s = s.replace("\u0f73", "\u0f71\u0f72") # use is discouraged
    s = s.replace("\u0f75", "\u0f71\u0f74") # use is discouraged
    s = s.replace("\u0f77", "\u0fb2\u0f71\u0f80") # deprecated
    s = s.replace("\u0f79", "\u0fb3\u0f71\u0f80") # deprecated
    s = s.replace("\u0f81", "\u0f71\u0f80") # use is discouraged
    if form == "nfd":
        s = s.replace("\u0f43", "\u0f42\u0fb7")
        s = s.replace("\u0f4d", "\u0f4c\u0fb7")
        s = s.replace("\u0f52", "\u0f51\u0fb7")
        s = s.replace("\u0f57", "\u0f56\u0fb7")
        s = s.replace("\u0f5c", "\u0f5b\u0fb7")
        s = s.replace("\u0f69", "\u0f40\u0fb5")
        s = s.replace("\u0f76", "\u0fb2\u0f80")
        s = s.replace("\u0f78", "\u0fb3\u0f80")
        s = s.replace("\u0f93", "\u0f92\u0fb7")
        s = s.replace("\u0f9d", "\u0f9c\u0fb7")
        s = s.replace("\u0fa2", "\u0fa1\u0fb7")
        s = s.replace("\u0fa7", "\u0fa6\u0fb7")
        s = s.replace("\u0fac", "\u0fab\u0fb7")
        s = s.replace("\u0fb9", "\u0f90\u0fb5")
    else:
        s = s.replace("\u0f42\u0fb7", "\u0f43")
        s = s.replace("\u0f4c\u0fb7", "\u0f4d")
        s = s.replace("\u0f51\u0fb7", "\u0f52")
        s = s.replace("\u0f56\u0fb7", "\u0f57")
        s = s.replace("\u0f5b\u0fb7", "\u0f5c")
        s = s.replace("\u0f40\u0fb5", "\u0f69")
        s = s.replace("\u0fb2\u0f80", "\u0f76")
        s = s.replace("\u0fb3\u0f80", "\u0f78")
        s = s.replace("\u0f92\u0fb7", "\u0f93")
        s = s.replace("\u0f9c\u0fb7", "\u0f9d")
        s = s.replace("\u0fa1\u0fb7", "\u0fa2")
        s = s.replace("\u0fa6\u0fb7", "\u0fa7")
        s = s.replace("\u0fab\u0fb7", "\u0fac")
        s = s.replace("\u0f90\u0fb5", "\u0fb9")
    # 0f00 has not been marked as a composed character in Unicode
    # This is something that is now seen as a mistake, but it cannot be
    # changed because of Unicode change policies.
    s = s.replace("\u0f00", "\u0f68\u0f7c\u0f7e")
    # ra does't transform into a small rago before nya, so using 0f65
    # does not change its graphical representation in that case
    s = s.replace("\u0f65\u0f99", "\u0f62\u0f99")
    if graphical_normalization:
        s = normalize_graphical(s)
    s, valid = unicode_reorder(s)
    return s, valid

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
    # Zero-width characters have no graphical impact on Tibetan:
    s = re.sub("([\u0f00-\u0fda])[\u200b-\u200d\u2060\ufeff]", r"\1", s)
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
    # no graphical distinction between 0f0b and 0f0c
    s = s.replace("\u0f0c", "\u0f0b")
    # double shad is just two shad
    s = s.replace("\u0f0e", "\u0f0d\u0f0d")
    # 0f11 is just a normal shad that appears in some cases at the beginning of a page,
    # mostly when there is just one syllable before the shad on the first line, but it
    # has no semantic significance, it should be turned into a normal shad when combining
    # multiple texts
    s = s.replace("\u0f11", "\u0f0d")
    # we don't want to keep double tshegs (I suppose)
    s = s.replace("\u0fd2", "\u0f0b")
    # normalize end of line characters
    s = re.sub(r"(?:\r\n|\n)", "\n", s)
    if original_eol:
        # remove all yig mgo: 0f01+diacritic?, 0f02-0f07, 0fd0-0fd1, 0fd3-0fd4
        # as well as their surrounding punctuation: space, 0f0d-0f11, 0f14
        s = re.sub(r"[ \u0f0d-\u0f11\u0f14]*[\u0f01-\u0f07\u0fd0\u0fd1\u0fd3\u0fd4]+[ \u0f0d-\u0f11\u0f14\u0f71-\u0f87]*", "", s)
        # remove all punctuation at beginning of line
        s = re.sub(r"(^|[\n])[\u0f0b-\u0f14]+", "\\1", s)
        # ensure tsheg at end of line after normal letters, except after ཀ, ག and ཤ
        # (where the absence of a tsheg should be interpreted as the presence of a shad)
        s = re.sub(r"([\u0f41\u0f43-\u0f63\u0f65-\u0f6c][\u0f71-\u0fbc]*) *($|[\n])", "\\1\u0f0b\\2", s)
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

def normalize_unusual(s):
    #
    # some symbols are not doubled outside of exceptional shorthands. See
    # A Handbook of Abbreviations by the Dzongkha Development Commission:
    # https://www.dzongkha.gov.bt/uploads/files/publications/A_handbook_of_Dzongkha_and_Ch%C3%B6k%C3%A9_abbreviations_e78335551931b7bb0ea4666213f57824.pdf
    # these characters are 0f71-0f87, 0f35, 0f37, 0f39 0fad, 0fb1 and 0fb2
    # TODO
    #
    # tsheg + vowel should be vowel + tsheg in most cases, although this
    # heuristic can fail
    # TODO
    #
    # remove tsheg and diacritics at beginning of lines
    # TODO
    return s

def debug_to_unicode(s):
    res = ""
    for c in s:
        res += "\\u%x " % ord(c)
    return res

def assert_conv(orig, expected, expectedValid = True):
    resultStr, resultValid = normalize_unicode(orig)
    assert resultStr == expected, "%s -> %s but %s expected" % (debug_to_unicode(orig), debug_to_unicode(resultStr), debug_to_unicode(expected))
    assert resultValid == expectedValid, "%s valid? -> %s but %s expected" % (debug_to_unicode(orig), resultValid, expectedValid)

def test_normalize_unicode():
    assert_conv("\u0f77", "\u0fb2\u0f71\u0f80", False)
    assert_conv("\u0f40\u0f7e\u0f7c\u0f74\u0f71", "\u0f40\u0f74\u0f71\u0f7c\u0f7e")
    assert_conv("\u0f58\u0f74\u0fb0\u0f83", "\u0f58\u0f74\u0f71\u0f83")
    assert_conv("\u0F51\u0FB7\u0F74\u0FB0", "\u0F51\u0FB7\u0F74\u0f71")
    assert_conv("\u0F66\u0F7C\u0FB1", "\u0F66\u0FB1\u0F7C")
    assert_conv("\u0F0B\u0F7E", "\u0F0B\u0F7E", False)
    assert_conv("\u0f65\u0f99\u0f7a\u0f7a", "\u0f62\u0f99\u0f7b")
    assert_conv("\u0f01\u0f83", "\u0f01\u0f83") # should be valid

if __name__ == "__main__":
    test_normalize_unicode()
    #with open("allstacks.txt") as f:
    #    for l in f.readlines():
    #        l = l[:-1]
    #        res, valid = normalize_unicode(l)
    #        if l != res:
    #            print("transform '%s' into '%s'" % (l, res))
    #        if not valid:
    #            print("'%s' not valid" % l)
