# coding: utf8
from ..chunks.chunks import TokChunks


class ChunkTokenizer(TokChunks):
    def __init__(self, string):
        super().__init__(string)

    def tokenize(self):
        tokens = self.make_chunks()
        return self.get_readable(tokens)
