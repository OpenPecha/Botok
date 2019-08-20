# coding: utf-8
from ..textunits.bostring import BoString
from ..vars import chunk_values
from ..vars import CharMarkers as a
from ..vars import ChunkMarkers as u


class ChunkFrameworkBase:
    def __init__(self, string, ignore_chars=None):
        self.bs = BoString(string, ignore_chars=ignore_chars)

    @staticmethod
    def merge_chunks(chunks, merge_condition_func):
        """

        :param chunks: full list of chunks
        :param merge_condition_func: function that takes start-end indices of the sub-string of both
                                        previous and current chunks, does a test and returns a bool
        """
        num = 0
        while num <= len(chunks) - 1:
            current = chunks[num]
            if num - 1 >= 0:
                previous = chunks[num - 1]
                if merge_condition_func(previous, current):
                    inc = 0
                    while not previous:
                        inc += 1
                        previous = chunks[num - 1 - inc]

                    new = (previous[0], previous[1], previous[2] + current[2])
                    chunks[num - 1 - inc] = (
                        previous[0],
                        previous[1],
                        previous[2] + current[2],
                    )
                    del chunks[num]
                    num -= 1

            num += 1
        return chunks

    @staticmethod
    def merge_condition(chunk, condition_func):
        start, end = chunk[1], chunk[1] + chunk[2]
        count = 0
        i = start
        while i < end:
            if condition_func(i):
                count += 1
            i += 1
        return count == end - start

    @staticmethod
    def pipe_chunk(chunks, piped_chunk_func, to_chunk_marker: int, yes: int):
        """
        Re-chunks in place the chunks produced by a previous chunking method.

        :param chunks: the chunks from a previous chunking method
        :param piped_chunk_func: new chunking method to apply
        :param to_chunk_marker: chunk-mark to identify which chunks will be re-chunked
        :param yes: new chunk-mark to be used for matching chunks (leave empty to use default value)
                    The new chunks not passing the internal test will keep the previous chunk-mark.
        :type chunks: list of tuples containing each 3 ints
        :type piped_chunk_func: callable
        :type yes: int
        """
        for i, chunk in enumerate(chunks):
            if chunk[0] == to_chunk_marker:
                new = piped_chunk_func(chunk[1], chunk[1] + chunk[2], yes=yes)
                if new:
                    del chunks[i]
                    for j, n_chunk in enumerate(new):
                        if n_chunk[0] != yes:
                            chunks.insert(i + j, (chunk[0], n_chunk[1], n_chunk[2]))
                        else:
                            chunks.insert(i + j, n_chunk)
        return chunks

    def chunk_using(self, condition_func, start, end, yes, no):
        if not start and not end:
            start, end = 0, self.bs.len

        indices = self.chunk(start, end, condition_func)
        return [(yes, i[1], i[2]) if i[0] else (no, i[1], i[2]) for i in indices]

    @staticmethod
    def chunk(start_idx, end_idx, condition_func):
        """
        The method that actually creates groups of characters satisfying the test method
        and not satisfying it from the given range within the input string.

        :param start_idx: first char of the range to be chunked
        :param end_idx: last char
        :param condition_func: test method
        :type start_idx: int
        :type end_idx: int
        :type condition_func: callable
        :return: the chunk indices with True/False instead of the chunk markers
        :rtype: list of tuples containing each: a bool (matched/not the test method) and the indices
        """
        chunked = []
        start = start_idx
        length = 0
        prev_state = -1
        current_state = -1
        for i in range(start_idx, end_idx):
            current_state = condition_func(i)
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

    def clean_chunks(self, chunks):
        chunks = self.merge_spaces(chunks)
        return self.merge_similar_chunks(chunks)

    def merge_skippable_punct(self, chunks):
        i = 0
        while i <= len(chunks) - 1:
            current = chunks[i]
            # first element
            if i == 0 and len(chunks) - 1 >= 1:
                to_del = True
                for char_idx in range(current[1], current[1] + current[2]):
                    if not self.__is_skippable_punct(char_idx):
                        to_del = False

                if to_del:
                    new_chunk = (
                        chunks[i + 1][0],
                        current[1],
                        chunks[i + 1][1] + chunks[i + 1][2],
                    )
                    chunks[i + 1] = new_chunk
                    del chunks[i]
                    i -= 1

            # remaining ones
            if i - 1 >= 0:
                to_del = True
                for char_idx in range(current[1], current[1] + current[2]):
                    if not self.__is_skippable_punct(char_idx):
                        to_del = False

                if to_del:
                    new_chunk = (
                        chunks[i - 1][0],
                        chunks[i - 1][1],
                        current[2] + chunks[i - 1][2],
                    )
                    chunks[i - 1] = new_chunk
                    del chunks[i]
                    i -= 1
            i += 1
        return self.merge_similar_chunks(chunks)

    def __is_skippable_punct(self, char_idx):
        return self.bs.base_structure[char_idx] == a.TSEK or self.__is_space(char_idx)

    def merge_spaces(self, chunks):
        return self.merge_chunks(chunks, self.__is_space_mergeable)

    def __is_space_mergeable(self, previous, current):
        # previous needs to be there as a placeholder
        return self.merge_condition(current, self.__is_space)

    def __is_space(self, char_idx):
        """
        Tests whether the character at the given index is a valid Unicode space or not.
        """
        return self.bs.base_structure[char_idx] == a.TRANSPARENT

    def merge_similar_chunks(self, chunks):
        return self.merge_chunks(chunks, self.__is_similar_chunks)

    @staticmethod
    def __is_similar_chunks(previous, current):
        # the chunk markers of both are similar.
        return (
            previous[0] != u.TEXT.value
            and current[0] != u.TEXT.value
            and previous[0] == current[0]
        )

    def get_readable(self, indices, gen=False):
        out = self.get_markers(indices)
        return self.get_chunked(out, gen=gen)

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
            return (
                (i, self.bs.string[start : start + length])
                for i, start, length in indices
            )
        return [
            (i, self.bs.string[start : start + length]) for i, start, length in indices
        ]

    @staticmethod
    def get_markers(indices):
        """
        Replaces the int representation of the chunk-mark by its str counterpart.

        :param indices: indices containing ints as markers
        :type indices: list of tuples containing each an int and the indices or the substring
        :return: the chunks where the chunk-mark is the human-readable description
        :rtype: list of tuples containing each a str and the indices or the substring
        """
        return [tuple([chunk_values[i[0]]] + list(i[1:])) for i in indices]
