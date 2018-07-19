# coding: utf-8
from .pybochunk import PyBoChunk


class PyBoTextChunks(PyBoChunk):
    """
    This class uses the chunks produced by ``PyBoChunk`` to identify Tibetan syllables and clean them.
    Thus produces pre-processed Tibetan text that can be further processed.

    Every chunk produced by ``PyBoChunk`` is wrapped into a tuple containing:
            - either None or a list containing the cleaned syllable
              (the indices to every non-space and non-tsek char in every syllable chunk)
            - the chunk itself

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
        return self.base_structure[char_idx] != self.TSEK \
            and self.base_structure[char_idx] != self.SPACE \
            and self.base_structure[char_idx] != self.SKRT_LONG_VOW
