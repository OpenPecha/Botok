# coding: utf-8
from .chunkframework import ChunkFramework
from ..vars import ChunkMarkers as c
from ..vars import CharMarkers as a


class Chunks(ChunkFramework):
    """
    Produces chunks of the following types: bo, non-bo, punct and syl chunks

    Implements the following chunking pipeline:
            chunk "input_str" into BO / OTHER
            | chunk BO into PUNCT / BO
            | chunk BO into SYM / BO
            | chunk BO into NUM / BO
            | chunk BO into TEXT (syllables)
            | chunk OTHER into CJK / OTHER
            | chunk OTHER into LATIN / OTHER

    .. note:: Following Tibetan usage, it does not consider space as a punctuation mark.
    Spaces get attached to the chunk preceding them.
    """

    def __init__(self, string, ignore_chars=None):
        ChunkFramework.__init__(self, string, ignore_chars=ignore_chars)

    def make_chunks(self, indices=True, gen=False, space_as_punct=False):
        chunks = self.chunk_bo_chars()
        if space_as_punct:
            chunks = self.pipe_chunk(
                chunks, self.chunk_spaces, to_chunk_marker=c.BO.value, yes=c.PUNCT.value
            )
        chunks = self.pipe_chunk(
            chunks, self.chunk_punct, to_chunk_marker=c.BO.value, yes=c.PUNCT.value
        )
        chunks = self.pipe_chunk(chunks, self.chunk_symbol, c.BO.value, c.SYM.value)
        chunks = self.pipe_chunk(chunks, self.chunk_number, c.BO.value, c.NUM.value)
        if not space_as_punct:
            chunks = self.merge_skippable_punct(
                chunks
            )  # ensure we have correctly built syls
        chunks = self.pipe_chunk(chunks, self.syllabify, c.BO.value, c.TEXT.value)
        chunks = self.pipe_chunk(chunks, self.adjust_syls, c.TEXT.value, c.TEXT.value)
        chunks = self.pipe_chunk(chunks, self.chunk_cjk, c.OTHER.value, c.CJK.value)
        chunks = self.pipe_chunk(chunks, self.chunk_latin, c.OTHER.value, c.LATIN.value)
        if not space_as_punct:
            chunks = self.merge_skippable_punct(chunks)
        if not indices:
            return self.get_chunked(chunks, gen=gen)
        return chunks


class TokChunks(Chunks):
    """
    This class uses the chunks produced by ``Chunks`` to identify Tibetan syllables and clean them.
    Thus produces pre-processed Tibetan text that can be further processed.

    Every chunk produced by ``Chunks`` is wrapped into a tuple containing:
            - either None or a list containing the cleaned syllable
              (the indices to every non-space and non-tsek char in every syllable chunk)
            - the chunk itself

    """

    def __init__(self, string, ignore_chars=None, space_as_punct=False):
        super().__init__(string, ignore_chars=ignore_chars)
        self.chunks = None
        self.space_as_punct = space_as_punct

    def serve_syls_to_trie(self):
        chunks = []
        for chunk in self.make_chunks(space_as_punct=self.space_as_punct):
            if chunk[0] == c.TEXT:
                syl = self.__get_text_chars(chunk[1], chunk[1] + chunk[2])
                chunks.append((syl, chunk))
            else:
                chunks.append((None, chunk))
        self.chunks = chunks

    def get_syls(self):
        syls = []
        for chunk in self.make_chunks(space_as_punct=self.space_as_punct):
            if chunk[0] == c.TEXT:
                char_idxs = self.__get_text_chars(chunk[1], chunk[1] + chunk[2])
                syls.append("".join([self.bs.string[i] for i in char_idxs]))
        return syls

    def __get_text_chars(self, start_idx, end_idx):
        """
        Removes all the spaces and tseks from a given syllable by only keeping the characters that
        pass ``__is_syl_text()``.

        :param start_idx: starting index of the syllable-chunk to clean
        :param end_idx: its ending index
        :type start_idx: int
        :type end_idx: int
        :return: a list of indices corresponding to the chars of the cleaned syllable
        """
        return [i for i in range(start_idx, end_idx) if self.__is_syl_text(i)]

    def __is_syl_text(self, char_idx):
        """
        Tests whether the character at the given index is part of the cleaned syllable or not.
        """
        return (
            self.bs.base_structure[char_idx] != a.TSEK
            and self.bs.base_structure[char_idx] != a.TRANSPARENT
            and self.bs.base_structure[char_idx] != a.SKRT_LONG_VOW
        ) or self.bs.base_structure[char_idx] == a.SKRT_LONG_VOW
