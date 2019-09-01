# coding: utf-8
from .charcategories import get_char_category
from ..vars import CharMarkers as a
from ..vars import char_values


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

    >>> from botok.textunits.bostring import BoString
    >>> from botok.vars import CharMarkers

    >>> bo_str = ' བཀྲ་ཤིས་  tr བདེ་ལེགས།'
    >>> bs = BoString(bo_str)

    >>> bs.base_structure  # key: character index, value: character group
    {0: 15, 1: 1, 2: 1, 3: 2, 4: 4, 5: 1, 6: 3, 7: 1, 8: 4, 9: 15, 10: 15, 11: 14,
    12: 14, 13: 15, 14: 1, 15: 1, 16: 3, 17: 4, 18: 1, 19: 3, 20: 1, 21: 1, 22: 8}

    >>> bs.get_categories()
    {0: 'space', 1: 'cons', 2: 'cons', 3: 'sub-cons', 4: 'tsek', 5: 'cons', 6: 'vow',
    7: 'cons', 8: 'tsek', 9: 'space', 10: 'space', 11: 'other', 12: 'other',
    13: 'space', 14: 'cons', 15: 'cons', 16: 'vow', 17: 'tsek', 18: 'cons', 19: 'vow',
    20: 'cons', 21: 'cons', 22: 'punct'}

    .. note:: You may want to refine the groups that are implemented to have a finer analysis.
                Be sure to create the corresponding constants in ``__init__()`` and the corresponding
                entries in ``__init__().char_markers``.
    """

    def __init__(self, string, ignore_chars=None):
        if ignore_chars is None:
            ignore_chars = []
        self.ignore_chars = ignore_chars
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
            cat = get_char_category(char)
            if char in self.ignore_chars:
                self.base_structure[
                    i
                ] = (
                    a.TRANSPARENT.value
                )  # spaces chars are allowed anywhere, thus ignored
            else:
                self.base_structure[i] = cat

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

        >>> bo_str = ' བཀྲ་ཤིས་  tr བདེ་ལེགས།'
        >>> bs = BoString(bo_str)

        >>> bs.export_groups(2, 5)
        {0: 1, 1: 2, 2: 4, 3: 1, 4: 3}

        >>> bs.export_groups(2, 5, for_substring=False)
        {2: 1, 3: 2, 4: 4, 5: 1, 6: 3}

        """
        if for_substring:
            return {
                n: self.base_structure[i]
                for n, i in enumerate(range(start_idx, start_idx + slice_len))
            }
        else:
            return {
                i: self.base_structure[i]
                for i in range(start_idx, start_idx + slice_len)
            }

    def get_categories(self, struct=None):
        if struct is None or not isinstance(struct, dict):
            return {k: char_values[v] for k, v in self.base_structure.items()}
        else:
            return {k: char_values[v] for k, v in struct.items()}
