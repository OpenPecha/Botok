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


CATEGORIES = (
    [Cats.Other]  # 0F00
    + [Cats.Base]  # 0F01, often followed by 0f083
    + [Cats.Other] * 22  # 0F02-0F17
    + [Cats.BottomVowel] * 2  # 0F18-0F19
    + [Cats.Other] * 6  # 0F1A-0F1F
    + [Cats.Base]
    * 20  # 0F20-0F33, numbers can be followed by 0f18, 0f19 or exceptionally by vowels
    + [Cats.Other]  # 0F34
    + [Cats.BottomMark]  # 0F35
    + [Cats.Other]  # 0F36
    + [Cats.BottomMark]  # OF37
    + [Cats.Other]  # 0F38
    + [Cats.Subscript]  # 0F39, kind of cheating but works
    + [Cats.Other] * 4  # 0F3A-0F3D
    + [Cats.RightMark]  # 0F3E
    + [Cats.Other]  # 0F3F, not quite sure
    + [Cats.Base] * 45  # 0F40-0F6C
    + [Cats.Other] * 4  # 0F6D-0F70
    + [Cats.BottomVowel]  # 0F71
    + [Cats.TopVowel]  # 0F72
    + [Cats.TopVowel]  # 0F73
    + [Cats.BottomVowel] * 2  # 0F74-0F75
    + [Cats.TopVowel] * 8  # 0F76-0F7D
    + [Cats.TopMark]  # 0F7E
    + [Cats.RightMark]  # 0F7F
    + [Cats.TopVowel] * 2  # 0F80-0F81
    + [Cats.TopMark] * 2  # 0F82-0F83
    + [Cats.BottomMark]  # 0F84
    + [Cats.Other]  # 0F85
    + [Cats.TopMark] * 2  # 0F86-0F87
    + [Cats.Base] * 2  # 0F88-0F89
    + [Cats.Base]  # 0F8A always followed by 0f82 (required by the Unicode spec)
    + [Cats.Other]  # 0F8B
    + [Cats.Base]  # 0F8C
    + [Cats.Subscript] * 48  # 0F8D-0FBC
)


def charcat(c):
    """Returns the category for a single char string"""
    o = ord(c)
    if 0x0F00 <= o <= 0x0FBC:
        return CATEGORIES[o - 0x0F00]
    return Cats.Other


# debug:
# for i, c in enumerate(CATEGORIES):
#    print("%x : %d" % (0x0F00 + i , c.value))


def unicode_reorder(txt):
    # case of a syllable starting with a diacritic (ex: a vowel or subscript)
    # we push it after the first main letter
    # txt = re.sub(r"^([\u0f71-\u0f84\u0f8d-\u0fbc]+)([\u0f40-\u0f6c])", r"\2", txt)
    # return txt, True
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
        newindices = sorted(range(i, j), key=lambda e: (charcats[e].value, e))
        replaces = "".join(txt[n] for n in newindices)
        res.append(replaces)
        i = j
    return "".join(res), valid


def normalize_unicode(s, form="nfd"):
    # first, unify Unicode form:
    # http://www.unicode.org/faq/normalization.html
    # https://unicode.org/reports/tr15/
    # https://unicode.org/charts/normalization/chart_Tibetan.html
    # although for some reason this chart considers 0f0c -> 0f0b in NFD
    #
    # deprecated or discouraged characters
    s = s.replace("\u0f73", "\u0f71\u0f72")  # use is discouraged
    s = s.replace("\u0f75", "\u0f71\u0f74")  # use is discouraged
    s = s.replace("\u0f77", "\u0fb2\u0f71\u0f80")  # deprecated
    s = s.replace("\u0f79", "\u0fb3\u0f71\u0f80")  # deprecated
    s = s.replace("\u0f81", "\u0f71\u0f80")  # use is discouraged
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
    s, valid = unicode_reorder(s)
    # ra doesn't transform into a small rago before anything else than (most) subjoined,
    # so 0f65 should be replaced with 0f62 in that case
    s = re.sub("\u0f65([^\u0f90-\u0f97\u0f9a-\u0fac\u0fae\u0faf\u0fb4-\u0fbc])", r"ར\1", s)
    s = normalize_invalid_start_string(s)
    return s

def debug_to_unicode(s):
    res = ""
    for c in s:
        res += "\\u%x " % ord(c)
    return res


def assert_conv(orig, expected, expectedValid=True):
    resultStr = normalize_unicode(orig)
    assert resultStr == expected, "{} -> {} but {} expected".format(
        debug_to_unicode(orig), debug_to_unicode(resultStr), debug_to_unicode(expected)
    )
    #assert resultValid == expectedValid, "{} valid? -> {} but {} expected".format(
    #    debug_to_unicode(orig), resultValid, expectedValid
    #)


def is_vowel(char):
    if re.search(r"[\u0f71-\u0f84]", char):
        return True
    return False


def is_suffix(char):
    if re.search(r"[\u0f90-\u0fbc]", char):
        return True
    return False


def normalize_invalid_start_string(s):
    # we put the vowel in second place if the string starts with a vowel
    if is_vowel(s[0]) and not is_vowel(s[1]) and not is_suffix(s[1]):
        return s[1] + s[0] + (s[2:] if len(s) > 2 else "")
    if is_suffix(s[0]):
        return s[1:]
    return s


def test_normalize_unicode():
    assert_conv("\u0F7B\u0F56", "\u0F56\u0F7B", False)
    assert_conv("\u0f40\u0f77", "\u0f40\u0fb2\u0f71\u0f80", False)
    assert_conv("\u0f40\u0f7e\u0f7c\u0f74\u0f71", "\u0f40\u0f74\u0f71\u0f7c\u0f7e")
    assert_conv("\u0f58\u0f74\u0fb0\u0f83", "\u0f58\u0fb0\u0f74\u0f83")
    assert_conv("\u0F51\u0FB7\u0F74\u0FB0", "\u0F51\u0FB7\u0fb0\u0F74")
    assert_conv("\u0F66\u0F7C\u0FB1", "\u0F66\u0FB1\u0F7C")
    assert_conv("\u0F0B\u0F7E", "\u0F0B\u0F7E", False)
    assert_conv("\u0f65\u0f99\u0f7a\u0f7a", "\u0f62\u0f99\u0f7a\u0f7a")
    assert_conv("\u0f01\u0f83", "\u0f01\u0f83") # should be valid


if __name__ == "__main__":
    test_normalize_unicode()