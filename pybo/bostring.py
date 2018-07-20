# coding: utf-8
from re import search


class BoString:
    """
    This class is the foundational building block of pre-processing.

    It implements the natural groups of characters a user makes when looking at
    a text in his native language.

    Implementation:
    ---------------

        - all the characters in the Unicode Tables for Tibetan are organized in lists
            hard-coded as string variables in ``__attribute_basic_types()``.
        - upon instanciation, ``__init__().base_structure`` is populated with the indices of every
            char in the input string(key) and the group constant to which it belongs(values)
        - human-readable description of the group constant can be accessed in ``__init__().char_markers``

    :Example:

    >>> from pybo.bostring import BoString

    >>> bo_str = ' བཀྲ་ཤིས་  tr བདེ་ལེགས།'
    >>> bs = BoString(bo_str)

    >>> bs.base_structure  # key: character index, value: character group
    {0: 15, 1: 1, 2: 1, 3: 2, 4: 4, 5: 1, 6: 3, 7: 1, 8: 4, 9: 15, 10: 15, 11: 14,
    12: 14, 13: 15, 14: 1, 15: 1, 16: 3, 17: 4, 18: 1, 19: 3, 20: 1, 21: 1, 22: 8}

    >>> {k: bs.char_markers[v] for k, v in bs.base_structure.items()}
    {0: 'space', 1: 'cons', 2: 'cons', 3: 'sub-cons', 4: 'tsek', 5: 'cons', 6: 'vow',
    7: 'cons', 8: 'tsek', 9: 'space', 10: 'space', 11: 'other', 12: 'other',
    13: 'space', 14: 'cons', 15: 'cons', 16: 'vow', 17: 'tsek', 18: 'cons', 19: 'vow',
    20: 'cons', 21: 'cons', 22: 'punct'}

    .. note:: You may want to refine the groups that are implemented to have a finer analysis.
                Be sure to create the corresponding constants in ``__init__()`` and the corresponding
                entries in ``__init__().char_markers``.
    """
    def __init__(self, string):
        self.cons = "ཀཁགངཅཆཇཉཏཐདནཔཕབམཙཚཛཝཞཟའཡརལཤསཧཨཪ"
        self.CONS = 1
        self.sub_cons = "ྐྒྔྕྗྙྟྡྣྤྦྨྩྫྭྱྲླྷ"
        self.SUB_CONS = 2
        self.vow = "ིེོུ"
        self.VOW = 3
        self.tsek = "་༌"
        self.TSEK = 4
        self.skrt_cons = "གྷཊཋཌཌྷཎདྷབྷཛྷཥཀྵ྅"
        self.SKRT_CONS = 5
        self.skrt_sub_cons = "ྑྖྠྥྪྮྯྰྴྶྸྺྻྼཱྒྷྚྛྜྜྷྞྡྷྦྷྫྷྵྐྵ"
        self.SKRT_SUB_CONS = 6
        self.skrt_vow = "ཱཱིུྲྀཷླྀཹ྄ཱཻཽྀྀྂྃ྆"
        self.SKRT_VOW = 7
        self.skrt_long_vow = "ཿ"
        self.SKRT_LONG_VOW = 17
        self.normal_punct = "༄༅༆༈།༎༏༐༑༔༴༼༽"
        self.PUNCT = 8
        self.numerals = "༠༡༢༣༤༥༦༧༨༩"
        self.NUM = 9
        self.in_syl_marks = "༵༷༸ཾ"
        self.IN_SYL_MARK = 10
        self.special_punct = "༁༂༃༒༇༉༊༺༻༾༿࿐࿑࿓࿔"
        self.SPECIAL_PUNCT = 11
        self.symbols = "ༀ༓༕༖༗༘༙༚༛༜༝༞༟༪༫༬༭༮༯༰༱༲༳༶༹྇ྈྉྊྋྌྍྎྏ྾྿࿀࿁࿂࿃࿄࿅࿆࿇࿈࿉࿊࿋࿌࿎࿏࿒࿕࿖࿗࿘࿙࿚"
        self.SYMBOLS = 12
        self.non_bo_non_skrt = "ཫཬ"
        self.NON_BO_NON_SKRT = 13
        self.OTHER = 14
        # all spaces from the unicode tables
        self.spaces = ["\t", " ", " ", "᠎", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "​", " ", " ", "　", "﻿"]
        self.SPACE = 15
        self.char_markers = {self.CONS: 'cons',
                             self.SUB_CONS: 'sub-cons',
                             self.VOW: 'vow',
                             self.TSEK: 'tsek',
                             self.SKRT_CONS: 'skrt-cons',
                             self.SKRT_SUB_CONS: 'skrt-sub-cons',
                             self.SKRT_VOW: 'skrt-vow',
                             self.SKRT_LONG_VOW: 'skrt-long-vow',
                             self.PUNCT: 'punct',
                             self.NUM: 'num',
                             self.IN_SYL_MARK: 'in-syl-mark',
                             self.SPECIAL_PUNCT: 'special-punct',
                             self.SYMBOLS: 'symbol',
                             self.NON_BO_NON_SKRT: 'no-bo-no-skrt',
                             self.OTHER: 'other',
                             self.SPACE: 'space'}

        self.string = string
        self.len = len(string)
        self.base_structure = {}
        self.__attribute_basic_types()

    def __attribute_basic_types(self):
        """
        Populates ``__init__().base_structure``.
        """
        for i in range(len(self.string)):
            char = self.string[i]
            if char in self.cons:
                self.base_structure[i] = self.CONS
            elif char in self.sub_cons:
                self.base_structure[i] = self.SUB_CONS
            elif char in self.vow:
                self.base_structure[i] = self.VOW
            elif char in self.tsek:
                self.base_structure[i] = self.TSEK
            elif char in self.skrt_cons:
                self.base_structure[i] = self.SKRT_CONS
            elif char in self.skrt_sub_cons:
                self.base_structure[i] = self.SKRT_SUB_CONS
            elif char in self.skrt_vow:
                self.base_structure[i] = self.SKRT_VOW
            elif char in self.skrt_long_vow:
                self.base_structure[i] = self.SKRT_LONG_VOW
            elif char in self.normal_punct:
                self.base_structure[i] = self.PUNCT
            elif char in self.numerals:
                self.base_structure[i] = self.NUM
            elif char in self.in_syl_marks:
                self.base_structure[i] = self.IN_SYL_MARK
            elif char in self.special_punct:
                self.base_structure[i] = self.SPECIAL_PUNCT
            elif char in self.symbols:
                self.base_structure[i] = self.SYMBOLS
            elif char in self.non_bo_non_skrt:
                self.base_structure[i] = self.NON_BO_NON_SKRT
            elif char in self.spaces:
                self.base_structure[i] = self.SPACE
            else:
                self.base_structure[i] = self.OTHER

    def export_groups(self, start_idx, slice_len, for_substring=True):
        """
        Export the base groups for a slice of the input string

        :param start_idx: starting index of the slice
        :param slice_len: length of the slice we want to export
        :param for_substring: if True, indices start at 0, Else the indices of the original string are kept.
        :type start_idx: int
        :type slice_len: int
        :return: the slice of ``__init__().base_structure`` described in the parameters
        :rtype: dict

        :Example:

        # reuses the variables declared in the Class docstring
        >>> bs.export_groups(2, 5)
        {0: 1, 1: 2, 2: 4, 3: 1, 4: 3}

        >>> bs.export_groups(2, 5, for_substring=False)
        {2: 1, 3: 2, 4: 4, 5: 1, 6: 3}

        """
        if for_substring:
            return {n: self.base_structure[i] for n, i in enumerate(range(start_idx, start_idx + slice_len))}
        else:
            return {i: self.base_structure[i] for i in range(start_idx, start_idx + slice_len)}

    @staticmethod
    def _is_skrt_syl(syl):
        """
        Checks whether a given syllable is Sanskrit.
        Uses the regexes of Paul Hackett from his Visual Basic script

        :param syl: syllable__ to test
        :return: True if it is Sanskrit, False otherwise

        .. note:: the original comments are preserved
        .. Todo:: find source
        """
        # Now do Sanskrit: Skt.vowels, [g|d|b|dz]+_h, hr, shr, Skt
        regex1 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཱཱཱིུ-ཹཻཽ-ྃ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[གཌདབཛྒྜྡྦྫ][ྷ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|" \
                 r"[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཤཧ][ྲ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|" \
                 r"[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[གྷཊ-ཎདྷབྷཛྷཥཀྵ-ཬཱཱཱིུ-ཹཻཽ-ྃྒྷྚ-ྞྡྷྦྷྫྷྵྐྵ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
        # more Sanskrit: invalid superscript-subscript pairs
        regex2 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཀཁགང-ཉཏ-དན-བམ-ཛཝ-ཡཤཧཨ][ྐ-ྫྷྮ-ྰྴ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
        # tsa-phru mark used in Chinese transliteration
        regex3 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[༹][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
        return search(regex1, syl) or search(regex2, syl) or search(regex3, syl)