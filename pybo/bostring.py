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
    cons = "ཀཁགངཅཆཇཉཏཐདནཔཕབམཙཚཛཝཞཟའཡརལཤསཧཨཪ"
    CONS = 1
    sub_cons = "ྐྒྔྕྗྙྟྡྣྤྦྨྩྫྭྱྲླྷ"
    SUB_CONS = 2
    vow = "ིེོུ"
    VOW = 3
    tsek = "་༌"
    TSEK = 4
    skrt_cons = "གྷཊཋཌཌྷཎདྷབྷཛྷཥཀྵ྅"
    SKRT_CONS = 5
    skrt_sub_cons = "ྑྖྠྥྪྮྯྰྴྶྸྺྻྼཱྒྷྚྛྜྜྷྞྡྷྦྷྫྷྵྐྵ"
    SKRT_SUB_CONS = 6
    skrt_vow = "ཱཱིུྲྀཷླྀཹ྄ཱཻཽྀྀྂྃ྆"
    SKRT_VOW = 7
    skrt_long_vow = "ཿ"
    SKRT_LONG_VOW = 17
    normal_punct = "༄༅༆༈།༎༏༐༑༔༴༼༽"
    PUNCT = 8
    numerals = "༠༡༢༣༤༥༦༧༨༩"
    NUM = 9
    in_syl_marks = "༵༷༸ཾ"
    IN_SYL_MARK = 10
    special_punct = "༁༂༃༒༇༉༊༺༻༾༿࿐࿑࿓࿔"
    SPECIAL_PUNCT = 11
    symbols = "ༀ༓༕༖༗༘༙༚༛༜༝༞༟༪༫༬༭༮༯༰༱༲༳༶༹྇ྈྉྊྋྌྍྎྏ྾྿࿀࿁࿂࿃࿄࿅࿆࿇࿈࿉࿊࿋࿌࿎࿏࿒࿕࿖࿗࿘࿙࿚"
    SYMBOLS = 12
    non_bo_non_skrt = "ཫཬ"
    NON_BO_NON_SKRT = 13
    OTHER = 14
    # all spaces from the unicode tables
    spaces = ["\t", " ", " ", "᠎", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "​", " ", " ", "　", "﻿"]
    SPACE = 15

    def __init__(self, string):
        self.char_markers = {BoString.CONS: 'cons',
                             BoString.SUB_CONS: 'sub-cons',
                             BoString.VOW: 'vow',
                             BoString.TSEK: 'tsek',
                             BoString.SKRT_CONS: 'skrt-cons',
                             BoString.SKRT_SUB_CONS: 'skrt-sub-cons',
                             BoString.SKRT_VOW: 'skrt-vow',
                             BoString.SKRT_LONG_VOW: 'skrt-long-vow',
                             BoString.PUNCT: 'punct',
                             BoString.NUM: 'num',
                             BoString.IN_SYL_MARK: 'in-syl-mark',
                             BoString.SPECIAL_PUNCT: 'special-punct',
                             BoString.SYMBOLS: 'symbol',
                             BoString.NON_BO_NON_SKRT: 'no-bo-no-skrt',
                             BoString.OTHER: 'other',
                             BoString.SPACE: 'space'}

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
            if char in BoString.cons:
                self.base_structure[i] = BoString.CONS
            elif char in BoString.sub_cons:
                self.base_structure[i] = BoString.SUB_CONS
            elif char in BoString.vow:
                self.base_structure[i] = BoString.VOW
            elif char in BoString.tsek:
                self.base_structure[i] = BoString.TSEK
            elif char in BoString.skrt_cons:
                self.base_structure[i] = BoString.SKRT_CONS
            elif char in BoString.skrt_sub_cons:
                self.base_structure[i] = BoString.SKRT_SUB_CONS
            elif char in BoString.skrt_vow:
                self.base_structure[i] = BoString.SKRT_VOW
            elif char in BoString.skrt_long_vow:
                self.base_structure[i] = BoString.SKRT_LONG_VOW
            elif char in BoString.normal_punct:
                self.base_structure[i] = BoString.PUNCT
            elif char in BoString.numerals:
                self.base_structure[i] = BoString.NUM
            elif char in BoString.in_syl_marks:
                self.base_structure[i] = BoString.IN_SYL_MARK
            elif char in BoString.special_punct:
                self.base_structure[i] = BoString.SPECIAL_PUNCT
            elif char in BoString.symbols:
                self.base_structure[i] = BoString.SYMBOLS
            elif char in BoString.non_bo_non_skrt:
                self.base_structure[i] = BoString.NON_BO_NON_SKRT
            elif char in BoString.spaces:
                self.base_structure[i] = BoString.SPACE
            else:
                self.base_structure[i] = BoString.OTHER

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