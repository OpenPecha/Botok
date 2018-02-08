class TibString:
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
        self.BASE = 0
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
        self.OTHER = 13
        self.SPACE = 14
        self.UNDERSCORE = 15  # used to mark spaces in input when segmented by pytib
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
        sub_cons = "ྐྑྒྔྕྖྗྙྟྠྡྣྤྥྦྨྩྪྫྭྮྯྰྱྲླྴྶྷྸྺྻྼཱ"
        vow = "ིེོུ"
        tsek = "་༌"
        skrt_cons = "གྷཊཋཌཌྷཎདྷབྷཛྷཥཀྵཫཬ྅"
        skrt_sub_cons = "ྒྷྚྛྜྜྷྞྡྷྦྷྫྷྵྐྵ"
        skrt_vow = "ཱཱིུྲྀཷླྀཹ྄ཱཻཽྀྀྂྃ྆ཿ"
        normal_punct = "༄༅༆༈།༎༏༐༑༔༴༼༽"
        numerals = "༠༡༢༣༤༥༦༧༨༩"
        in_syl_marks = "༵༷༸ཾ"
        special_punct = "༁༂༃༒༇༉༊༺༻༾༿࿐࿑࿓࿔"
        symbols = "ༀ༓༕༖༗༘༙༚༛༜༝༞༟༪༫༬༭༮༯༰༱༲༳༶༹྇ྈྉྊྋྌྍྎྏ྾྿࿀࿁࿂࿃࿄࿅࿆࿇࿈࿉࿊࿋࿌࿎࿏࿒࿕࿖࿗࿘࿙࿚"
        for i in range(len(self.string)):
            char = self.string[i]
            if char in cons:
                self.base_structure[i] = {self.BASE: self.CONS}
            elif char in sub_cons:
                self.base_structure[i] = {self.BASE: self.SUB_CONS}
            elif char in vow:
                self.base_structure[i] = {self.BASE: self.VOW}
            elif char in tsek:
                self.base_structure[i] = {self.BASE: self.TSEK}
            elif char in skrt_cons:
                self.base_structure[i] = {self.BASE: self.SKRT_CONS}
            elif char in skrt_sub_cons:
                self.base_structure[i] = {self.BASE: self.SKRT_SUB_CONS}
            elif char in skrt_vow:
                self.base_structure[i] = {self.BASE: self.SKRT_VOW}
            elif char in normal_punct:
                self.base_structure[i] = {self.BASE: self.PUNCT}
            elif char in numerals:
                self.base_structure[i] = {self.BASE: self.NUM}
            elif char in in_syl_marks:
                self.base_structure[i] = {self.BASE: self.IN_SYL_MARK}
            elif char in special_punct:
                self.base_structure[i] = {self.BASE: self.SPECIAL_PUNCT}
            elif char in symbols:
                self.base_structure[i] = {self.BASE: self.SYMBOLS}
            elif char in self.spaces:
                self.base_structure[i] = {self.BASE: self.SPACE}
            elif char == '_':
                self.base_structure[i] = {self.BASE: self.UNDERSCORE}
            else:
                self.base_structure[i] = {self.BASE: self.OTHER}


class TibStringChunk(TibString):
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
        TibString.__init__(self, string)

    def chunk_tib_chars(self, start=None, end=None, yes='bo', no='non-bo'):
        if not start and not end:
            start, end = 0, self.len

        indices = self.__chunk(start, end, self.__is_tib_unicode)
        return [(yes, i[1], i[2]) if i[0] else (no, i[1], i[2]) for i in indices]

    def chunk_segmented_tib(self, start=None, end=None, yes='bo', no='non-bo'):
        if not start and not end:
            start, end = 0, self.len

        indices = self.__chunk(start, end, self.__is_segmented_tib)
        return [(yes, i[1], i[2]) if i[0] else (no, i[1], i[2]) for i in indices]

    def chunk_punct(self, start=None, end=None, yes='punct', no=None):
        if not start and not end:
            start, end = 0, self.len

        indices = self.__chunk(start, end, self.__is_punct)
        return [(yes, i[1], i[2]) if i[0] else (no, i[1], i[2]) for i in indices]

    def chunk_spaces(self, start=None, end=None, yes='space', no='chars'):
        if not start and not end:
            start, end = 0, self.len

        indices = self.__chunk(start, end, self.__is_space)
        return [(yes, i[1], i[2]) if i[0] else (no, i[1], i[2]) for i in indices]

    def syllabify(self, start=None, end=None, yes='syl'):
        # expects only tibetan text
        if not start and not end:
            start, end = 0, self.len

        indices = self.__chunk(start, end, self.__is_tsek)
        for num, i in enumerate(indices):
            if i[0] and num-1 >= 0 and not indices[num-1][0]:
                indices[num-1] = (indices[num-1][0], indices[num-1][1], indices[num-1][2] + i[2])

        return [(yes, i[1], i[2]) for i in indices if not i[0]]

    def get_chunked(self, indices, gen=False):
        """

        :param indices: the chunk indices (the output of chunking methods)
        :param gen: a generator of the output
        :return: the marker/substring pairs in a list
        """
        if gen:
            return ((t, self.string[start:start + length]) for t, start, length in indices)
        return [(t, self.string[start:start + length]) for t, start, length in indices]

    def __is_punct(self, string_idx):
        return self.base_structure[string_idx][self.BASE] == self.PUNCT or \
               self.base_structure[string_idx][self.BASE] == self.SPECIAL_PUNCT or \
               self.base_structure[string_idx][self.BASE] == self.UNDERSCORE

    def __is_tsek(self, string_idx):
        return self.base_structure[string_idx][self.BASE] == self.TSEK

    def __is_tib_unicode(self, string_idx):
        return self.base_structure[string_idx][self.BASE] != self.OTHER

    def __is_segmented_tib(self, string_idx):
        return self.base_structure[string_idx][self.BASE] != self.OTHER or \
               self.base_structure[string_idx][self.BASE] == self.UNDERSCORE

    def __is_space(self, string_idx):
        return self.base_structure[string_idx][self.BASE] == self.SPACE

    @staticmethod
    def pipe_chunk(indices, piped_chunk, to_chunk, yes):
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


class PyBoChunk(TibStringChunk):
    """
    Produces bo, non-bo, spaces, punct and syl chunks
    """
    def __init__(self, string):
        TibStringChunk.__init__(self, string)

    def chunk(self, indices=True, gen=False):
        chunks = self.chunk_tib_chars(yes='bo')
        self.pipe_chunk(chunks, self.chunk_spaces, to_chunk='bo', yes='space')
        self.pipe_chunk(chunks, self.chunk_punct, to_chunk='bo', yes='punct')
        self.pipe_chunk(chunks, self.syllabify, to_chunk='bo', yes='syl')
        if not indices:
            return self.get_chunked(chunks, gen=gen)
        return chunks
