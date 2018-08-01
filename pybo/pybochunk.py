# coding: utf-8
from .bochunk import BoChunk


class PyBoChunk(BoChunk):
    """
    Produces chunks of the following types: bo, non-bo, punct and syl chunks

    Implements the following chunking pipeline:
            chunk "input_str" into "bo"/"non-bo"
            | chunk "bo" into "punct"/"bo"
            | chunk "bo" into "sym"/"bo"
            | chunk "bo" into "num"/"bo"
            | chunk "bo" into syllables
            | delete chunks containing spaces and transfer their content to the previous chunk

    .. note:: Following Tibetan usage, it does not consider space as a punctuation mark.
    Spaces get attached to the chunk preceding them.
    """
    def __init__(self, string):
        BoChunk.__init__(self, string)

    def chunk(self, indices=True, gen=False):
        chunks = self.chunk_bo_chars()
        self.pipe_chunk(chunks, self.chunk_punct, to_chunk=self.BO_MARKER, yes=self.PUNCT_MARKER)
        self.pipe_chunk(chunks, self.chunk_symbol, to_chunk=self.BO_MARKER, yes=self.SYMBOL_MARKER)
        self.pipe_chunk(chunks, self.chunk_number, to_chunk=self.BO_MARKER, yes=self.NUMBER_MARKER)
        self.pipe_chunk(chunks, self.syllabify, to_chunk=self.BO_MARKER, yes=self.SYL_MARKER)
        self.__attach_space_chunks(chunks)
        if not indices:
            return self.get_chunked(chunks, gen=gen)
        return chunks

    def __attach_space_chunks(self, indices):
        """
        Deletes space-only chunks and puts their content in the previous chunk

        :param indices: output from a previous chunking method containing space-only chunks
        :type indices: list of tuples containing each 3 ints
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
        """
        Tests whether the character group of all the chars in the range between start and end is SPACE.
        """
        spaces_count = 0
        i = start
        while i < end:
            if self.base_structure[i] == self.SPACE:
                spaces_count += 1
            i += 1
        return spaces_count == end - start
