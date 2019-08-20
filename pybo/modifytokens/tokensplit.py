# coding: utf-8
import copy

from ..third_party.cqlparser import replace_token_attributes


class TokenSplit:
    """
    Takes a token object and divide it into two using an index of the content.

    The affected attributes are:
        - token.content     : the string is split at the index
        - token.char_groups : the dict items are redistributed
        - token.start       : second token only. now equals "start + index"
        - token.len      : length of new content
        - token.syls        : syls are redistributed and split if necessary

    """

    def __init__(self, token, split_idx, token_changes=None):
        self.token = token
        self.first = None
        self.second = None
        self.token_changes = token_changes
        self.idx = split_idx

    def split(self):
        self.split_on_idx()
        self.replace_attrs()

        return self.first, self.second

    def replace_attrs(self):
        if self.token_changes:
            tokens = [self.first, self.second]
            replace_token_attributes(tokens, self.token_changes)
            self.first, self.second = tokens

    def split_on_idx(self):
        self.first = copy.deepcopy(self.token)
        self.second = copy.deepcopy(self.token)
        self.__split_contents()
        self.__split_indices()
        self.__split_syls_idx()
        self.__split_char_types()
        self.__split_affixation()

    def __split_contents(self):
        text = self.first.text
        self.first.text = text[0 : self.idx]
        self.second.text = text[self.idx :]

    def __split_char_types(self):
        char_types = self.first.char_types
        self.first.char_types = char_types[: self.idx]
        self.second.char_types = char_types[self.idx :]

    def __split_indices(self):
        self.first.len = len(self.first.text)
        self.second.len = len(self.second.text)
        self.second.start = self.second.start + self.idx

    def __split_syls_idx(self):
        syls = self.first.syls_idx
        # empty syls
        self.first.syls_idx = []
        self.second.syls_idx = []

        if syls:
            for syl in syls:
                if syl[-1] < self.idx:
                    self.first.syls_idx.append(syl)

                else:
                    # separate the syl in two
                    part1, part2 = [], []
                    for i in syl:
                        if i < self.idx:
                            part1.append(i)
                        else:
                            part2.append(i - self.idx)

                    # add them if non-empty
                    if part1:
                        self.first.syls_idx.append(part1)
                    if part2:
                        self.second.syls_idx.append(part2)

    def __split_affixation(self):
        if self.token.affixation:
            del self.first.affixation["len"]
            del self.first.affixation["type"]
            del self.second.affixation["aa"]
