class BoString:
    """
    Basic Class for Tibetan Strings.
    Leverages the intuitive groups of Tibetan characters in the Unicode
    tables to meaningfully chunk a given input string.

    Contains:
             - self.string: the input string
             - self.base_structure: a dict of the following structure:
                    key: char index in self.string
                    value: a dict (to allow further insertion of information):
                                key: BASE (a simple constant)
                                value: CHAR_GROUP
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
        # all spaces from the unicode tables
        self.spaces = [" ", " ", "᠎", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "​", " ", " ", "　", "﻿"]

        self.string = string
        self.len = len(string)
        self.base_structure = {}
        self.__attribute_basic_types()

    def __attribute_basic_types(self):
        """
        Attributes a group to every character.
        Finer the groups, greater the fine-grained chunking capacities of TibStringUtil

        note: the strings below attempt to regroup the Tibetan Unicode Table meaningfully.
              adapt it to your needs.
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


class BoChunk(BoString):
    """
    Generates chunks by using the group attributed to every char by TibString
    Piped-chunking enables to easily use complex chunking criteria. (see test file)

    chunking functions output:
                    [(string chunk_marker, int start_index, int length), ...]
    get_chunked output:
                    [( string chunk_marker, string substring), ...]

    Adapting to specific needs is straightforward:
        - copy/adapt a test method ('__is_...()' )
        - copy/adapt a chunking method ('chunk_...()')
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
        self.markers = {self.BO_MARKER: 'bo',
                        self.NON_BO_MARKER: 'non-bo',
                        self.PUNCT_MARKER: 'punct',
                        self.NON_PUNCT_MARKER: 'non-punct',
                        self.SPACE_MARKER: 'space',
                        self.NON_SPACE_MARKER: 'non-space',
                        self.SYL_MARKER: 'syl'}

    def chunk_bo_chars(self, start=None, end=None, yes=100, no=101):
        if not start and not end:
            start, end = 0, self.len

        indices = self.__chunk(start, end, self.__is_bo_unicode)
        return [(yes, i[1], i[2]) if i[0] else (no, i[1], i[2]) for i in indices]

    def chunk_punct(self, start=None, end=None, yes=102, no=103):
        if not start and not end:
            start, end = 0, self.len

        indices = self.__chunk(start, end, self.__is_punct)
        return [(yes, i[1], i[2]) if i[0] else (no, i[1], i[2]) for i in indices]

    def chunk_spaces(self, start=None, end=None, yes=104, no=105):
        if not start and not end:
            start, end = 0, self.len

        indices = self.__chunk(start, end, self.__is_space)
        return [(yes, i[1], i[2]) if i[0] else (no, i[1], i[2]) for i in indices]

    def syllabify(self, start=None, end=None, yes=106):
        """
        expects only valid Tibetan strings
        """
        if not start and not end:
            start, end = 0, self.len

        indices = self.__chunk(start, end, self.__is_tsek)
        for num, i in enumerate(indices):
            if i[0] and num - 1 >= 0 and not indices[num - 1][0]:
                indices[num - 1] = (indices[num - 1][0], indices[num - 1][1], indices[num - 1][2] + i[2])
        indices = [i for i in indices if not i[0]]

        return [(yes, i[1], i[2]) for i in indices]

    def get_chunked(self, indices, gen=False):
        """

        :param indices: the chunk indices (the output of chunking methods)
        :param gen: a generator of the output
        :return: the marker/substring pairs in a list
        """
        if gen:
            return ((t, self.string[start:start + length]) for t, start, length in indices)
        return [(t, self.string[start:start + length]) for t, start, length in indices]

    def get_markers(self, indices):
        """

        :param indices: indices containing ints as markers
        :return: same indices with the corresponding marker strings
        """
        return [tuple([self.markers[i[0]]] + list(i[1:])) for i in indices]

    def attach_space_syls(self, indices):
        """
        Deletes space-only chunks and puts their content in the previous chunk
        :param indices: contains space-only chunks
        """
        for num, i in enumerate(indices):
            if num - 1 >= 0 and self.__only_contains_spaces(i[1], i[1]+i[2]):
                indices[num - 1] = (indices[num - 1][0], indices[num - 1][1], indices[num - 1][2] + i[2])
                indices[num] = False

        c = 0
        while c < len(indices):
            if not indices[c]:
                del indices[c]
            else:
                c += 1

    def __is_punct(self, char_idx):
        return self.base_structure[char_idx] == self.PUNCT or \
               self.base_structure[char_idx] == self.SPECIAL_PUNCT or \
               self.base_structure[char_idx] == self.UNDERSCORE

    def __is_tsek(self, char_idx):
        return self.base_structure[char_idx] == self.TSEK

    def __is_bo_unicode(self, char_idx):
        return self.base_structure[char_idx] != self.OTHER

    def __is_space(self, char_idx):
        return self.base_structure[char_idx] == self.SPACE

    def __only_contains_spaces(self, start, end):
        spaces_count = 0
        i = start
        while i < end:
            if self.base_structure[i] == self.SPACE:
                spaces_count += 1
            i += 1
        return spaces_count == end - start

    @staticmethod
    def pipe_chunk(indices, piped_chunk, to_chunk: int, yes: int):
        """
        re-chunks in place the chunk indices produced by a previous chunk method.

        :param list indices: the chunk indices from a previous chunking method
        :param method piped_chunk: chunk method to apply
        :param string to_chunk: chunk-marker to find chunks to be re-chunked
        :param string yes: marker to be used for matching chunks (no marker left to default)
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

    @staticmethod
    def __chunk(start_idx, end_idx, condition):
        """
        Creates groups of characters satisfying the condition (test method) and
        not satisfying it from the given range within the input string

        :param start_idx: first char of the range to be chunked
        :param end_idx: last char
        :param condition: test method
        :return: the chunk indices with True/False instead of the chunk markers
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
    Produces bo, non-bo, spaces, punct and syl chunks
    """
    def __init__(self, string):
        BoChunk.__init__(self, string)

    def chunk(self, indices=True, gen=False):
        chunks = self.chunk_bo_chars()
        self.pipe_chunk(chunks, self.chunk_punct, to_chunk=self.BO_MARKER, yes=self.PUNCT_MARKER)
        self.pipe_chunk(chunks, self.syllabify, to_chunk=self.BO_MARKER, yes=self.SYL_MARKER)
        self.attach_space_syls(chunks)
        if not indices:
            return self.get_chunked(chunks, gen=gen)
        return chunks
