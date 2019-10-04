# coding: utf8
from .chunkframeworkbase import ChunkFrameworkBase
from ..vars import CharMarkers as a, ChunkMarkers as u, VOWELS, NO_SHAD_CONS


class ChunkFramework(ChunkFrameworkBase):
    """
    This class is a framework to split a given string into chunks of characters sharing similar properties.
    Fine chunking is possible by piping any number of chunking methods as desired.

    Building on top of ``BoString`` that acts as the provider of the group to which each character belongs,
    this class manipulates these groups in order to produce chunks.
    Thus, the finer the groups of characters encoded in BoString, the greater the capacities of this class
    to produce refined chunking.

    By default, this classes provides methods that should cater standard chunking needs for Tibetan language.

    :Example:

    >>> from botok.chunks.chunkframework import ChunkFramework

    >>> bo_str = ' བཀྲ་ཤིས་  tr བདེ་ལེགས།'
    >>> bc = ChunkFramework(bo_str)

    # 1. Initial chunking
    >>> chunks = bc.chunk_bo_chars()  # uses default chunk-marks here, but override them in the pipeline

    >>> chunks  # actual chunks. each chunk is tuple containing: (chunk-marker, starting_index, chunk_length)
    [(100, 0, 11), (101, 11, 2), (100, 13, 10)]
    >>> bc.get_markers(chunks)  # shows the human-readable description of the constant
    [('bo', 0, 11), ('non-bo', 11, 2), ('bo', 13, 10)]
    >>> bc.get_chunked(chunks)  # shows the substring for each chunk
    [(100, ' བཀྲ་ཤིས་  '), (101, 'tr'), (100, ' བདེ་ལེགས།')]

    # 2. First piped chunking: re-chunks tibetan chunks into tibetan text and tibetan punctuation.
    >>> bc.pipe_chunk(chunks, bc.chunk_punct, to_chunk_marker=u.BO, yes=u.PUNCT)

    >>> chunks
    [(100, 0, 11), (101, 11, 2), (100, 13, 9), (102, 22, 1)]
    >>> bc.get_markers(chunks)
    [('bo', 0, 11), ('non-bo', 11, 2), ('bo', 13, 9), ('punct', 22, 1)]
    >>> bc.get_chunked(chunks)
    [(100, ' བཀྲ་ཤིས་  '), (101, 'tr'), (100, ' བདེ་ལེགས'), (102, '།')]

    # 3. Second piped chunking: re-chunks tibetan text into syllables, keeping the same chunk-marker.
    >>> bc.pipe_chunk(chunks, bc.syllabify, to_chunk_marker=u.BO, yes=u.BO)

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

    def chunk_bo_chars(self, start=None, end=None, yes=u.BO.value, no=u.OTHER.value):
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
        return self.chunk_using(self.__is_bo_unicode, start, end, yes, no)

    def __is_bo_unicode(self, char_idx):
        """
        Tests whether the character at the given index is found within the Tibetan Unicode Table.

        :param char_idx: index of the character to test
        :type char_idx: int
        """
        return (
            self.bs.base_structure[char_idx] != a.OTHER
            and self.bs.base_structure[char_idx] != a.LATIN
            and self.bs.base_structure[char_idx] != a.CJK
        )

    def chunk_latin(self, start=None, end=None, yes=u.LATIN.value, no=u.OTHER.value):
        return self.chunk_using(self.__is_latin, start, end, yes, no)

    def __is_latin(self, char_idx):
        return (
            self.bs.base_structure[char_idx] == a.LATIN
            or self.bs.base_structure[char_idx] == a.TRANSPARENT
        )

    def chunk_cjk(self, start=None, end=None, yes=u.CJK.value, no=u.OTHER.value):
        return self.chunk_using(self.__is_cjk, start, end, yes, no)

    def __is_cjk(self, char_idx):
        return (
            self.bs.base_structure[char_idx] == a.CJK
            or self.bs.base_structure[char_idx] == a.TRANSPARENT
        )

    def chunk_punct(
        self, start=None, end=None, yes=u.PUNCT.value, no=u.NON_PUNCT.value
    ):
        """
        Chunks input into Tibetan text("punct") or non-Tibetan("non-punct").

        :type yes: int (hard-coded value of PUNCT_MARKER)
        :type no: int (hard-coded value of NON_PUNCT_MARKER)
        """
        return self.chunk_using(self.__is_punct, start, end, yes, no)

    def __is_punct(self, char_idx):
        """
        Tests whether the character at the given index is a Tibetan punctuation or not.
        """
        # if a tsek or a space is right after
        if (
            char_idx
            and (
                self.bs.base_structure[char_idx - 1] == a.SYMBOL
                or self.bs.base_structure[char_idx - 1] == a.NUMERAL
                or self.bs.base_structure[char_idx - 1] == a.OTHER
                or self.bs.base_structure[char_idx - 1] == a.NORMAL_PUNCT
                or self.bs.base_structure[char_idx - 1] == a.SPECIAL_PUNCT
                or self.bs.base_structure[char_idx - 1] == a.TSEK
                or self.bs.base_structure[char_idx - 1] == a.TRANSPARENT
            )
            and (
                self.bs.base_structure[char_idx] == a.TSEK
                or self.bs.base_structure[char_idx] == a.TRANSPARENT
                or self.bs.base_structure[char_idx] == a.NORMAL_PUNCT
            )
        ):
            return True

        return (
            self.bs.base_structure[char_idx] == a.NORMAL_PUNCT
            or self.bs.base_structure[char_idx] == a.SPECIAL_PUNCT
            or self.bs.base_structure[char_idx] == a.TRANSPARENT
        )

    def chunk_symbol(self, start=None, end=None, yes=u.SYM.value, no=u.NON_SYM.value):
        """
        Chunks input into Tibetan text("sym") or non-Tibetan("non-sym").

        :type yes: int (hard-coded value of SYM_MARKER)
        :type no: int (hard-coded value of NON_SYM_MARKER)
        """
        return self.chunk_using(self.__is_sym, start, end, yes, no)

    def __is_sym(self, char_idx):
        """
        Tests whether the character at the given index is a Tibetan symbols or not.
        """
        return (
            self.bs.base_structure[char_idx] == a.SYMBOL
            or self.bs.base_structure[char_idx] == a.TRANSPARENT
        )

    def chunk_number(self, start=None, end=None, yes=u.NUM.value, no=u.NON_NUM.value):
        """
        Chunks input into Tibetan text("num") or non-Tibetan("non-num").

        :type yes: int (hard-coded value of NUM_MARKER)
        :type no: int (hard-coded value of NON_NUM_MARKER)
        """
        return self.chunk_using(self.__is_num, start, end, yes, no)

    def __is_num(self, char_idx):
        """
        Tests whether the character at the given index is a number  or not.
        """
        return (
            self.bs.base_structure[char_idx] == a.NUMERAL
            or self.bs.base_structure[char_idx] == a.TRANSPARENT
        )

    def chunk_spaces(
        self, start=None, end=None, yes=u.SPACE.value, no=u.NON_SPACE.value
    ):
        """
        Chunks input into any valid Unicode spaces("space") or something else("non-space").

        :type yes: int (hard-coded value of SPACE_MARKER)
        :type no: int (hard-coded value of NON_SPACE_MARKER)
        """
        return self.chunk_using(self.__is_space, start, end, yes, no)

    def __is_space(self, char_idx):
        """
        Tests whether the character at the given index is a valid Unicode space or not.
        """
        return self.bs.base_structure[char_idx] == a.TRANSPARENT

    def syllabify(self, start=None, end=None, yes=u.TEXT.value):
        """
        Chunks valid Tibetan text(expected input) into syllables(tsek is included if present).

        :type yes: int (hard-coded value of SYL_MARKER)
        """
        if not start and not end:
            start, end = 0, self.bs.len

        indices = self.chunk(start, end, self.__is_tsek_or_long_skrt_vowel)
        for num, i in enumerate(indices):
            if i[0] and num - 1 >= 0 and not indices[num - 1][0]:
                indices[num - 1] = (
                    indices[num - 1][0],
                    indices[num - 1][1],
                    indices[num - 1][2] + i[2],
                )

        return [(yes, i[1], i[2]) for i in indices if not i[0]]

    def __is_tsek_or_long_skrt_vowel(self, char_idx):
        """
        Tests whether the character at the given index is an unambiguous end-marker or not.
        Used as test to find syllable boundaries by ``syllabify()``.
        ::note:
        """
        return (
            self.bs.base_structure[char_idx] == a.TSEK
            or self.bs.base_structure[char_idx] == a.SKRT_LONG_VOW
        )

    def adjust_syls(self, start=None, end=None, yes=u.TEXT.value):
        """
        if there is a space in the chunk:
                test if the preceding is ཀ ག ཤ eventually followed by a vowel
                test if both parts are valid syllables (Bosyl)
                if tests pass:
                        split in two syllables after space.
        :param chunks:
        :param start:
        :param end:
        :param yes:
        :return:
        """
        indices = self.chunk(start, end, self.__is_transparent)
        truc = self.bs.string[start:end]
        for num, i in enumerate(indices):
            chunk = self.bs.string[i[1] : i[1] + i[2]]
            if len(indices) - 1 > num > 0 and indices[num][0]:
                _, s, e = indices[num - 1]
                text = self.bs.string[s : s + e]
                if (
                    len(text) >= 2 and text[-1] in VOWELS and text[-2] in NO_SHAD_CONS
                ) or (len(text) >= 1 and text[-1] in NO_SHAD_CONS):
                    indices[num - 1] = (
                        yes,
                        indices[num - 1][1],
                        indices[num - 1][2] + i[2],
                    )
                else:
                    indices[num - 1] = (
                        indices[num - 1][0],
                        indices[num - 1][1],
                        indices[num - 1][2] + indices[num][2] + indices[num + 1][2],
                    )
                    indices[num + 1] = (None, indices[num + 1][1], indices[num + 1][2])
            elif indices[num][0] is False:
                indices[num] = (yes, i[1], i[2])
            elif (num == 0 or num == len(indices) - 1) and indices[num][0] is True:
                indices[num] = (u.PUNCT.value, i[1], i[2])

        # remove all chunks that were added
        indices = [i for i in indices if i[0] is not True and i[0] is not None]

        return indices if len(indices) > 1 else list()

    def __is_transparent(self, char_idx):
        return self.bs.base_structure[char_idx] == a.TRANSPARENT
