import re
from enum import Enum

def normalize_unicode(s, normalization_type="graphical"):
    # combined characters, using NFD representation:
    s = s.replace("\u0f00", "\u0f68\u0f7c\u0f7e")
    s = s.replace("\u0f43", "\u0f42\u0fb7")
    s = s.replace("\u0f4d", "\u0f4c\u0fb7")
    s = s.replace("\u0f52", "\u0f51\u0fb7")
    s = s.replace("\u0f57", "\u0f56\u0fb7")
    s = s.replace("\u0f5c", "\u0f5b\u0fb7")
    s = s.replace("\u0f69", "\u0f40\u0fb5")
    s = s.replace("\u0f73", "\u0f71\u0f72")
    s = s.replace("\u0f75", "\u0f71\u0f74")
    s = s.replace("\u0f76", "\u0fb2\u0f80")
    s = s.replace("\u0f77", "\u0fb2\u0f71\u0f80")
    s = s.replace("\u0f78", "\u0fb3\u0f80")
    s = s.replace("\u0f79", "\u0fb3\u0f71\u0f80")
    s = s.replace("\u0f81", "\u0f71\u0f80")
    s = s.replace("\u0f93", "\u0f92\u0fb7")
    s = s.replace("\u0f9d", "\u0f9c\u0fb7")
    s = s.replace("\u0fa2", "\u0fa1\u0fb7")
    s = s.replace("\u0fa7", "\u0fa6\u0fb7")
    s = s.replace("\u0fac", "\u0fab\u0fb7")
    s = s.replace("\u0fb9", "\u0f90\u0fb5")
    if normalization_type == "graphical":
        s = s.replace("\u0f0c", "\u0f0b")
        s = s.replace("\u0f38", "\u0f27")
        s = s.replace("\u0f0e", "\u0f0d\u0f0d")
    # ra does't transform into a small rago before nya
    s = s.replace("\u0f65\u0f99", "\u0f62\u0f99")
    # no achung in the middle of stacks, only full a
    s = re.sub(r"[\u0f71]([\u0f8d-\u0fbc])", "\u0fb0\\1", s)
    # no full a at the end of stacks, only achung
    s = re.sub(r"[\u0fb0]([^\u0f8d-\u0fbc]|$)", "\u0f71\\1", s)
    # reorder
    s, valid = reorder_bo(s)
    return s, valid

class Cats(Enum):
    Other = 0
    Base = 1
    Subscript = 2
    Achung = 3
    Chabkyu = 4
    BottomMark = 5
    TopVowel = 6
    TopMark = 7
    RightMark = 8

CATEGORIES =  ([Cats.Other]          # 0F00
             + [Cats.Base]           # 0F01, kind of cheating for diacritics
             + [Cats.Other] * 51     # 0F02-0F34
             + [Cats.BottomMark]     # 0F35
             + [Cats.Other]          # 0F36
             + [Cats.BottomMark]     # OF37
             + [Cats.Other]          # 0F38
             + [Cats.Subscript]      # 0F39, kind of cheating but works
             + [Cats.Other] * 4      # 0F3A-0F3D
             + [Cats.RightMark]      # 0F3E
             + [Cats.Other]          # 0F3F, not quite sure
             + [Cats.Base] * 45      # 0F40-0F6C
             + [Cats.Other] * 4      # 0F6D-0F70
             + [Cats.Achung]         # 0F71
             + [Cats.TopVowel]       # 0F72
             + [Cats.Achung]         # 0F73
             + [Cats.Chabkyu] * 2    # 0F74-0F75
             + [Cats.TopVowel] * 8   # 0F76-0F7D
             + [Cats.TopMark]        # 0F7E
             + [Cats.RightMark]      # 0F7F
             + [Cats.TopVowel] * 2   # 0F80-0F81
             + [Cats.TopMark] * 2    # 0F82-0F83
             + [Cats.BottomMark]     # 0F84
             + [Cats.Other]          # 0F85
             + [Cats.TopMark] * 2    # 0F86-0F87
             + [Cats.Base] * 2       # 0F88-0F89
             + [Cats.Other] * 2      # 0F8A-0F8B
             + [Cats.Base]           # 0F8C
             + [Cats.Subscript] * 48 # 0F8D-0FBC
             + [Cats.Subscript] * 48 # 0F8D-0FBC
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

# inpired from code for Khmer Unicode provided by SIL
def reorder_bo(txt):
    charcats = [charcat(c) for c in txt]
    #print(["%x" % ord(c) for c in txt])
    #print(charcats)
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

def debug_to_unicode(s):
    res = ""
    for c in s:
        res += "\\u%x " % ord(c)
    return res

def assert_conv(orig, expected, expectedValid = True):
    resultStr, resultValid = normalize_unicode(orig)
    assert(resultStr == expected)
    assert(resultValid == expectedValid)

def test_normalize_unicode():
    assert_conv("\u0f77", "\u0fb2\u0f71\u0f80", False)
    assert_conv("\u0f40\u0f7e\u0f7c\u0f74\u0f71", "\u0f40\u0f71\u0f74\u0f7c\u0f7e")
    #assert_conv("\u0f66\u0f71\u0fb1", "\u0f66\u0fb1\u0f71")
    assert_conv("\u0f58\u0f74\u0fb0\u0f83", "\u0f58\u0f71\u0f74\u0f83")
    assert_conv("\u0F51\u0FB7\u0F74\u0FB0", "\u0F51\u0FB7\u0f71\u0F74")
    assert_conv("\u0F66\u0F7C\u0FB1", "\u0F66\u0FB1\u0F7C")
    assert_conv("\u0F0B\u0F7E", "\u0F0B\u0F7E", False)

if __name__ == "__main__":
    test_normalize_unicode()
