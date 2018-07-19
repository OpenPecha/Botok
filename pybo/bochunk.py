# coding: utf-8
from .bostring import BoString


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

    >>> from pybo.bochunk import BoChunk

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
        self.SYMBOL_MARKER = 107
        self.NON_SYMBOL_MARKER = 108
        self.NUMBER_MARKER = 109
        self.NON_NUMBER_MARKER = 110
        self.chunk_markers = {self.BO_MARKER: 'bo',
                              self.NON_BO_MARKER: 'non-bo',
                              self.PUNCT_MARKER: 'punct',
                              self.NON_PUNCT_MARKER: 'non-punct',
                              self.SPACE_MARKER: 'space',
                              self.NON_SPACE_MARKER: 'non-space',
                              self.SYL_MARKER: 'syl',
                              self.SYMBOL_MARKER: 'sym',
                              self.NON_SYMBOL_MARKER: 'non-sym',
                              self.NUMBER_MARKER: 'num',
                              self.NON_NUMBER_MARKER: 'non-num'}

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
        # if a tsek or a space is right after
        if char_idx \
                and (self.base_structure[char_idx-1] == self.SYMBOLS
                     or self.base_structure[char_idx-1] == self.NUM
                     or self.base_structure[char_idx-1] == self.OTHER
                     or self.base_structure[char_idx-1] == self.PUNCT
                     or self.base_structure[char_idx-1] == self.SPECIAL_PUNCT
                     or self.base_structure[char_idx-1] == self.TSEK
                     or self.base_structure[char_idx - 1] == self.SPACE) \
                and (self.base_structure[char_idx] == self.TSEK
                     or self.base_structure[char_idx] == self.SPACE
                     or self.base_structure[char_idx] == self.PUNCT):
            return True

        return self.base_structure[char_idx] == self.PUNCT \
            or self.base_structure[char_idx] == self.SPECIAL_PUNCT

    def chunk_symbol(self, start=None, end=None, yes=107, no=108):
        """
        Chunks input into Tibetan text("sym") or non-Tibetan("non-sym").

        :type yes: int (hard-coded value of SYM_MARKER)
        :type no: int (hard-coded value of NON_SYM_MARKER)
        """
        return self.__chunk_using(self.__is_sym, start, end, yes, no)

    def __is_sym(self, char_idx):
        """
        Tests whether the character at the given index is a Tibetan symbols or not.
        """
        return self.base_structure[char_idx] == self.SYMBOLS

    def chunk_number(self, start=None, end=None, yes=109, no=110):
        """
        Chunks input into Tibetan text("num") or non-Tibetan("non-num").

        :type yes: int (hard-coded value of NUM_MARKER)
        :type no: int (hard-coded value of NON_NUM_MARKER)
        """
        return self.__chunk_using(self.__is_num, start, end, yes, no)

    def __is_num(self, char_idx):
        """
        Tests whether the character at the given index is a number  or not.
        """
        return self.base_structure[char_idx] == self.NUM

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

        indices = self.__chunk(start, end, self.__is_tsek_or_long_skrt_vowel)
        for num, i in enumerate(indices):
            if i[0] and num - 1 >= 0 and not indices[num - 1][0]:
                indices[num - 1] = (indices[num - 1][0], indices[num - 1][1], indices[num - 1][2] + i[2])

        return [(yes, i[1], i[2]) for i in indices if not i[0]]

    def __is_tsek_or_long_skrt_vowel(self, char_idx):
        """
        Tests whether the character at the given index is an unambiguous end-marker or not.
        Used as test to find syllable boundaries by ``syllabify()``.
        ::note:
        """
        return self.base_structure[char_idx] == self.TSEK or \
            self.base_structure[char_idx] == self.SKRT_LONG_VOW

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
