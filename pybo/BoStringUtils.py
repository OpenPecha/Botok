"""
``BoStringUtils``
=================

Pre-processing tools for Tibetan language, both efficient and extensible.



PyBoChunk:  Chunks a string in units corresponding to the characteristics
            of Tibetan language.
            Produced chunk types: bo, non-bo, punct or syl
            (subclass of BoChunk)

BoChunk:    Produces chunks/groups of characters sharing similar properties.
            (subclass of BoString)

BoString:   Character-based analysis of a string from the point of view
            of Tibetan Language.



PyBoTextChunks: Facility class to produce a list of chunks to be used
                as input for ``BoTokenizer``.
"""


class BoString:
    """
    This class is the foundational building block of pre-processing.

    It implements the natural groups of characters a user makes when looking at
    a string of text in his native language.

    Implementation:
    ---------------

        - all the characters in the Unicode Tables for Tibetan are organized in lists
            hard-coded as string variables in ``__attribute_basic_types()``.
        - upon instanciation, __init__().base_structure is populated with the indices of every
            char in the input string(key) and the group constant to which it belongs(values)
        - human-readable description of the group constant can be accessed in __init__().char_markers

    :Example:

    >>> from pybo.BoStringUtils import BoString

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
                Be sure to create the corresponding constants in __init__() and the corresponding
                entries in __init__().char_markers.
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
        Populates self.base_structure.
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

        :param start_idx:
                        starting index of the slice
        :param slice_len:
                        length of the slice we want to export
        :param for_substring:
                        if True, indices start at 0, Else the indices
                        of the original string are kept.
        :type start_idx: int
        :type slice_len: int
        :return: the slice of __init__().base_structure described in the params
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


class BoChunk(BoString):
    """
    This class is a framework to split a given string into chunks of characters sharing similar properties.
    Fine chunking is possible by piping any number of chunking methods as desired.

    Building on top of ``BoString`` that acts as the provider of the group to which each character belongs,
    this class manipulates these groups in order to produce chunks.
    Thus, the finer the groups of characters encoded in BoString, the greater the capacities of this class
    to produce refined chunking.

    By default, this classes provides methods that should cater standard chunking needs for Tibetan language.

    :Example:

    >>> from pybo.BoStringUtils import BoChunk

    >>> bo_str = ' བཀྲ་ཤིས་  tr བདེ་ལེགས།'
    >>> bc = BoChunk(bo_str)

    # 1. Initial chunking
    >>> chunks = bc.chunk_bo_chars()  # uses default chunk-marks here, but override them in the pipeline

    >>> chunks  # actual chunks. each chunk is tuple containing: (chunk-marker, starting_index, chunk_length)
    [(100, 0, 11), (101, 11, 2), (100, 13, 10)]
    >>> bc.get_markers(chunks)  # shows the human-readable description of the constant
    [('bo', 0, 11), ('non-bo', 11, 2), ('bo', 13, 10)]
    >>> bc.get_chunked(chunks)  # shows the substring for each chunk
    [(100, ' བཀྲ་ཤིས་  '), (101, 'tr'), (100, ' བདེ་ལེགས།')]

    # 2. First piped chunking: re-chunks tibetan chunks into tibetan text and tibetan punctuation.
    >>> bc.pipe_chunk(chunks, bc.chunk_punct, to_chunk=bc.BO_MARKER, yes=bc.PUNCT_MARKER)

    >>> chunks
    [(100, 0, 11), (101, 11, 2), (100, 13, 9), (102, 22, 1)]
    >>> bc.get_markers(chunks)
    [('bo', 0, 11), ('non-bo', 11, 2), ('bo', 13, 9), ('punct', 22, 1)]
    >>> bc.get_chunked(chunks)
    [(100, ' བཀྲ་ཤིས་  '), (101, 'tr'), (100, ' བདེ་ལེགས'), (102, '།')]

    # 3. Second piped chunking: re-chunks tibetan text into syllables, keeping the same chunk-marker.
    >>> bc.pipe_chunk(chunks, bc.syllabify, to_chunk=bc.BO_MARKER, yes=bc.BO_MARKER)

    >>> chunks
    [(100, 0, 5), (100, 5, 4), (100, 9, 2), (101, 11, 2), (100, 13, 5), (100, 18, 4), (102, 22, 1)]
    >>> bc.get_markers(chunks)
    [('bo', 0, 5), ('bo', 5, 4), ('bo', 9, 2), ('non-bo', 11, 2), ('bo', 13, 5), ('bo', 18, 4), ('punct', 22, 1)]
    >>> bc.get_chunked(chunks)
    [(100, ' བཀྲ་'), (100, 'ཤིས་'), (100, '  '), (101, 'tr'), (100, ' བདེ་'), (100, 'ལེགས'), (102, '།')]

    # 4. Formatting the resultant chunks into an easily usable structure
    >>> chunks = bc.get_markers(chunks)         # exchange the constants for the human-readable description
    >>> final_result = bc.get_chunked(chunks)   # exchange the indices for the substrings of each chunk
    >>> final_result
    [('bo', ' བཀྲ་'), ('bo', 'ཤིས་'), ('bo', '  '), ('non-bo', 'tr'), ('bo', ' བདེ་'), ('bo', 'ལེགས'), ('punct', '།')]



    The Framework
    =============
    This class is meant to be extended as easily as it gets by creating custom chunking components.
    A "chunking kit" comprises:
                        - a chunking method
                        - a test method
                        - marker constants (if the existing one can't be used)
                        - a human-friendly description of the chunk type in the form of
                          an entry in ``__init__().chunk_markers``(in case a new constant was created).


    Chunking Methods (exposed)
    --------------------------
    A chunking method parses the characters in the slice of the input string as described
    in its arguments("start" and "end"). It produces consecutive groups of characters that
    pass the test that is used internally and that don't pass it.

    It is expected that they all share the same syntax except for the test method it calls
    internally.


    Test methods (hidden)
    -----------------------
    A test method contains the logic behind a chunking method.
    It leverages the character groups provided by ``BoString`` to encode the semantic properties the chunks
    are expected to possess.

    For example, ``__is_bo_unicode()`` passes for every character within the Tibetan Unicode Table.
    It does so by checking that the group of the character at the given index is not OTHER.


    Piped Chunking
    --------------
    Finely chunking a string is possible by piping as many chunking methods as necessary in a specific order.

    This is done by using ``pipe_chunk()`` that takes as arguments:
            - the output of a previous chunking method,
            - a new chunking method and
            - a chunk-marker to identify on which chunks the new method should be applied.
    It will replace in place every chunk matching the chunk-marker with the results of the new chunking method.

    For example, a standard pipeline for Tibetan would be:
            chunk "input_str" into "bo"/"non-bo" | chunk "bo" into "punct"/"bo-text" | chunk "bo-text" into "syllables"

    The result would be a succession of chunks that are either tibetan syllables with their punctuation,
    non-syllabic punctuation or non-Tibetan characters.


    Custom Chunking Methods
    -----------------------
    - signature: ``chunk_xxxx(start=None, end=None, yes=<int>, no=<int>)``
                 where the ints in "yes" and "no" are the hard-coded values of the chunk's types.
    - body: ``return self.__chunk_using(self.<private_test_method>, start, end, yes, no)``
             where "private_test_method" is the custom test method where the chunking logic is encoded.


    Custom Test Methods
    -------------------
    - signature: ``__is_xxx(char_idx)``

    - body: ``return <conditions>``
            where each condition follows this pattern:
            ``self.base_structure[char_idx] <equals or not> <character group>``


    Naming conventions
    ------------------
    - chunking methods start with "chunk_xxx".
    - test methods start with "__is_xxx".
    - chunk type constants end in "_MARKER" to be differenciated from ``BoString`` constants
    """
    def __init__(self, string):
        BoString.__init__(self, string)
        self.BO_MARKER = 100
        self.NON_BO_MARKER = 101
        self.PUNCT_MARKER = 102
        self.NON_PUNCT_MARKER = 103
        self.SPACE_MARKER = 104
        self.NON_SPACE_MARKER = 105
        self.SYL_MARKER = 106
        self.chunk_markers = {self.BO_MARKER: 'bo',
                              self.NON_BO_MARKER: 'non-bo',
                              self.PUNCT_MARKER: 'punct',
                              self.NON_PUNCT_MARKER: 'non-punct',
                              self.SPACE_MARKER: 'space',
                              self.NON_SPACE_MARKER: 'non-space',
                              self.SYL_MARKER: 'syl'}

    def chunk_bo_chars(self, start=None, end=None, yes=100, no=101):
        """
        Chunks input into Tibetan valid characters("bo") or something else("non-bo").

        :param start: starting index in ``__init__().string``
        :param end: ending index in ``__init__().string``
        :param yes: chunk-mark to apply to chunks passing the test
        :param no: chunk-mark to apply those not passing the test
        :type start: int
        :type end: int
        :type yes: int (hard-coded value of BO_MARKER)
        :type no: int (hard-coded value of NON_BO_MARKER)
        :return: the resulting chunks
        :rtype: list of tuples containing each 3 ints: chunk-mark, starting_index, chunk_length
        """
        return self.__chunk_using(self.__is_bo_unicode, start, end, yes, no)

    def __is_bo_unicode(self, char_idx):
        """
        Tests whether the character at the given index is found within the Tibetan Unicode Table.

        :param char_idx: index of the character to test
        :type char_idx: int
        """
        return self.base_structure[char_idx] != self.OTHER

    def chunk_punct(self, start=None, end=None, yes=102, no=103):
        """
        Chunks input into Tibetan text("punct") or non-Tibetan("non-punct").

        :type yes: int (hard-coded value of PUNCT_MARKER)
        :type no: int (hard-coded value of NON_PUNCT_MARKER)
        """
        return self.__chunk_using(self.__is_punct, start, end, yes, no)

    def __is_punct(self, char_idx):
        """
        Tests whether the character at the given index is a Tibetan punctuation or not.
        """
        return self.base_structure[char_idx] == self.PUNCT or \
            self.base_structure[char_idx] == self.SPECIAL_PUNCT

    def chunk_spaces(self, start=None, end=None, yes=104, no=105):
        """
        Chunks input into any valid Unicode spaces("space") or something else("non-space").

        :type yes: int (hard-coded value of SPACE_MARKER)
        :type no: int (hard-coded value of NON_SPACE_MARKER)
        """
        return self.__chunk_using(self.__is_space, start, end, yes, no)

    def __is_space(self, char_idx):
        """
        Tests whether the character at the given index is a valid Unicode space or not.
        """
        return self.base_structure[char_idx] == self.SPACE

    def syllabify(self, start=None, end=None, yes=106):
        """
        Chunks valid Tibetan text(expected input) into syllables(tsek is included if present).

        :type yes: int (hard-coded value of SYL_MARKER)
        """
        if not start and not end:
            start, end = 0, self.len

        indices = self.__chunk(start, end, self.__is_tsek)
        for num, i in enumerate(indices):
            if i[0] and num - 1 >= 0 and not indices[num - 1][0]:
                indices[num - 1] = (indices[num - 1][0], indices[num - 1][1], indices[num - 1][2] + i[2])

        return [(yes, i[1], i[2]) for i in indices if not i[0]]

    def __is_tsek(self, char_idx):
        """
        Tests whether the character at the given index in a tsek or not.
        Used as test to find syllable boundaries by ``syllabify()``.
        """
        return self.base_structure[char_idx] == self.TSEK

    def get_chunked(self, indices, gen=False):
        """
        Replaces the indices in every chunk tuple with the corresponding substring.

        :param indices: the output of a previous chunking method
        :param gen: if True, returns a generator with the chunks, a list otherwise
        :type indices: list of tuples each containing 3 ints
        :type gen: bool
        :return: the marker/substring pairs in a list
        :rtype: list of tuples each containing: a chunk-mark(int or str), a substring
        """
        if gen:
            return ((i, self.string[start:start + length]) for i, start, length in indices)
        return [(i, self.string[start:start + length]) for i, start, length in indices]

    def get_markers(self, indices):
        """
        Replaces the int representation of the chunk-mark by its str counterpart.

        :param indices: indices containing ints as markers
        :type indices: list of tuples containing each an int and the indices or the substring
        :return: the chunks where the chunk-mark is the human-readable description
        :rtype: list of tuples containing each a str and the indices or the substring
        """
        return [tuple([self.chunk_markers[i[0]]] + list(i[1:])) for i in indices]

    @staticmethod
    def pipe_chunk(indices, piped_chunk, to_chunk: int, yes: int):
        """
        Re-chunks in place the chunks produced by a previous chunking method.

        :param indices: the chunks from a previous chunking method
        :param piped_chunk: new chunking method to apply
        :param to_chunk: chunk-mark to identify which chunks will be re-chunked
        :param yes: new chunk-mark to be used for matching chunks (leave empty to use default value)
                    The new chunks not passing the internal test will keep the previous chunk-mark.
        :type indices: list of tuples containing each 3 ints
        :type piped_chunk: callable
        :type yes: int
        """
        for i, chunk in enumerate(indices):
            if chunk[0] == to_chunk:
                new = piped_chunk(chunk[1], chunk[1]+chunk[2], yes=yes)
                if new:
                    del indices[i]
                    for j, n_chunk in enumerate(new):
                        if n_chunk[0] != yes:
                            indices.insert(i+j, (chunk[0], n_chunk[1], n_chunk[2]))
                        else:
                            indices.insert(i+j, n_chunk)

    def __chunk_using(self, condition, start, end, yes, no):
        if not start and not end:
            start, end = 0, self.len

        indices = self.__chunk(start, end, condition)
        return [(yes, i[1], i[2]) if i[0] else (no, i[1], i[2]) for i in indices]

    @staticmethod
    def __chunk(start_idx, end_idx, condition):
        """
        The method that actually creates groups of characters satisfying the test method
        and not satisfying it from the given range within the input string.

        :param start_idx: first char of the range to be chunked
        :param end_idx: last char
        :param condition: test method
        :type start_idx: int
        :type end_idx: int
        :type condition: callable
        :return: the chunk indices with True/False instead of the chunk markers
        :rtype: list of tuples containing each: a bool (matched/not the test method) and the indices
        """
        chunked = []
        start = start_idx
        length = 0
        prev_state = -1
        current_state = -1
        for i in range(start_idx, end_idx):
            current_state = condition(i)
            if prev_state == -1:
                prev_state = current_state

            if current_state == prev_state:
                length += 1
            else:
                chunked.append((prev_state, start, length))
                prev_state = current_state
                start += length
                length = 1
        # final element
        if length != 0:
            if current_state == prev_state:
                if start + length < end_idx:
                    length += 1
            chunked.append((prev_state, start, length))
        return chunked


class PyBoChunk(BoChunk):
    """
    Produces bo, non-bo, punct and syl chunks

    note: Following Tibetan usage, it does not consider space as a punctuation mark.
    Spaces get attached to the chunk preceding them.
    """
    def __init__(self, string):
        BoChunk.__init__(self, string)

    def chunk(self, indices=True, gen=False):
        chunks = self.chunk_bo_chars()
        self.pipe_chunk(chunks, self.chunk_punct, to_chunk=self.BO_MARKER, yes=self.PUNCT_MARKER)
        self.pipe_chunk(chunks, self.syllabify, to_chunk=self.BO_MARKER, yes=self.SYL_MARKER)
        self.__attach_space_chunks(chunks)
        if not indices:
            return self.get_chunked(chunks, gen=gen)
        return chunks

    def __attach_space_chunks(self, indices):
        """
        Deletes space-only chunks and puts their content in the previous chunk
        :param indices: contains space-only chunks
        """
        for num, i in enumerate(indices):
            if num - 1 >= 0 and self.__only_contains_spaces(i[1], i[1] + i[2]):
                indices[num - 1] = (indices[num - 1][0], indices[num - 1][1], indices[num - 1][2] + i[2])
                indices[num] = False

        c = 0
        while c < len(indices):
            if not indices[c]:
                del indices[c]
            else:
                c += 1

    def __only_contains_spaces(self, start, end):
        spaces_count = 0
        i = start
        while i < end:
            if self.base_structure[i] == self.SPACE:
                spaces_count += 1
            i += 1
        return spaces_count == end - start


class PyBoTextChunks(PyBoChunk):
    """
    Serves content to BoTrie
    """
    def __init__(self, string):
        PyBoChunk.__init__(self, string)
        self.chunks = self.serve_syls_to_trie()

    def serve_syls_to_trie(self):
        chunks = []
        for chunk in self.chunk():
            if chunk[0] == self.SYL_MARKER:
                text_chars = self.__get_text_chars(chunk[1], chunk[1]+chunk[2])
                chunks.append((text_chars, chunk))
            else:
                chunks.append((None, chunk))
        return chunks

    def __get_text_chars(self, start_idx, end_idx):
        """
        Gives the list of indices of the text chars in the given span.
        """
        return [i for i in range(start_idx, end_idx) if self.__is_syl_text(i)]

    def __is_syl_text(self, char_idx):
        return self.base_structure[char_idx] != self.TSEK and \
               self.base_structure[char_idx] != self.SPACE
