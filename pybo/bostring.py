# coding: utf-8


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
        self.CONS = 1
        self.SUB_CONS = 2
        self.VOW = 3
        self.TSEK = 4
        self.SKRT_CONS = 5
        self.SKRT_SUB_CONS = 6
        self.SKRT_VOW = 7
        self.PUNCT = 8
        self.NUM = 9
        self.IN_SYL_MARK = 10
        self.SPECIAL_PUNCT = 11
        self.SYMBOLS = 12
        self.NON_BO_NON_SKRT = 13
        self.OTHER = 14
        self.SPACE = 15
        self.UNDERSCORE = 16  # used to mark spaces in input when segmented by pytib
        self.char_markers = {self.CONS: 'cons',
                             self.SUB_CONS: 'sub-cons',
                             self.VOW: 'vow',
                             self.TSEK: 'tsek',
                             self.SKRT_CONS: 'skrt-cons',
                             self.SKRT_SUB_CONS: 'skrt-sub-cons',
                             self.SKRT_VOW: 'skrt-vow',
                             self.PUNCT: 'punct',
                             self.NUM: 'num',
                             self.IN_SYL_MARK: 'in-syl-mark',
                             self.SPECIAL_PUNCT: 'special-punct',
                             self.SYMBOLS: 'symbol',
                             self.NON_BO_NON_SKRT: 'no-bo-no-skrt',
                             self.OTHER: 'other',
                             self.SPACE: 'space',
                             self.UNDERSCORE: 'underscore'}

        # all spaces from the unicode tables
        self.spaces = [" ", " ", "᠎", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "​", " ", " ", "　", "﻿"]

        self.string = string
        self.len = len(string)
        self.base_structure = {}
        self.__attribute_basic_types()

    def __attribute_basic_types(self):
        """
        Populates ``__init__().base_structure``.
        """
        cons = "ཀཁགངཅཆཇཉཏཐདནཔཕབམཙཚཛཝཞཟའཡརལཤསཧཨཪ"
        sub_cons = "ྐྒྔྕྗྙྟྡྣྤྦྨྩྫྭྱྲླྷ"
        vow = "ིེོུ"
        tsek = "་༌"
        skrt_cons = "གྷཊཋཌཌྷཎདྷབྷཛྷཥཀྵ྅"
        skrt_sub_cons = "ྑྖྠྥྪྮྯྰྴྶྸྺྻྼཱྒྷྚྛྜྜྷྞྡྷྦྷྫྷྵྐྵ"
        skrt_vow = "ཱཱིུྲྀཷླྀཹ྄ཱཻཽྀྀྂྃ྆ཿ"
        normal_punct = "༄༅༆༈།༎༏༐༑༔༴༼༽"
        numerals = "༠༡༢༣༤༥༦༧༨༩"
        in_syl_marks = "༵༷༸ཾ"
        special_punct = "༁༂༃༒༇༉༊༺༻༾༿࿐࿑࿓࿔"
        symbols = "ༀ༓༕༖༗༘༙༚༛༜༝༞༟༪༫༬༭༮༯༰༱༲༳༶༹྇ྈྉྊྋྌྍྎྏ྾྿࿀࿁࿂࿃࿄࿅࿆࿇࿈࿉࿊࿋࿌࿎࿏࿒࿕࿖࿗࿘࿙࿚"
        non_bo_non_skrt = "ཫཬ"
        for i in range(len(self.string)):
            char = self.string[i]
            if char in cons:
                self.base_structure[i] = self.CONS
            elif char in sub_cons:
                self.base_structure[i] = self.SUB_CONS
            elif char in vow:
                self.base_structure[i] = self.VOW
            elif char in tsek:
                self.base_structure[i] = self.TSEK
            elif char in skrt_cons:
                self.base_structure[i] = self.SKRT_CONS
            elif char in skrt_sub_cons:
                self.base_structure[i] = self.SKRT_SUB_CONS
            elif char in skrt_vow:
                self.base_structure[i] = self.SKRT_VOW
            elif char in normal_punct:
                self.base_structure[i] = self.PUNCT
            elif char in numerals:
                self.base_structure[i] = self.NUM
            elif char in in_syl_marks:
                self.base_structure[i] = self.IN_SYL_MARK
            elif char in special_punct:
                self.base_structure[i] = self.SPECIAL_PUNCT
            elif char in symbols:
                self.base_structure[i] = self.SYMBOLS
            elif char in non_bo_non_skrt:
                self.base_structure[i] = self.NON_BO_NON_SKRT
            elif char in self.spaces:
                self.base_structure[i] = self.SPACE
            elif char == '_':
                self.base_structure[i] = self.UNDERSCORE
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
