# coding: utf-8
import copy
from .third_party import replace_token_attributes


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
        if len(self.token.syls) > 1:
            self.__find_idx()
            self.split_on_idx()
            self.replace_attrs()

            return self.first, self.second
        else:
            return [self.token]

    def replace_attrs(self):
        if self.token_changes:
            tokens = [self.first, self.second]
            replace_token_attributes(tokens, self.token_changes)
            self.first, self.second = tokens

    def split_on_idx(self):
        self.first = copy.deepcopy(self.token)
        self.second = copy.deepcopy(self.token)
        self.__split_contents()
        self.__split_char_groups()
        self.__split_indices()
        self.__split_syls()

    def __find_idx(self):
        self.idx = self.token.syls[self.idx][0]

    def __split_contents(self):
        content = self.first.content
        self.first.content = content[0:self.idx]
        self.second.content = content[self.idx:]

    def __split_char_groups(self):
        # split in two
        c_g_1, c_g_2 = {}, {}
        for idx, group in self.first.char_groups.items():
            if idx < self.idx:
                c_g_1[idx] = group
            else:
                c_g_2[idx] = group

        # set indices to start from 0 for the second part
        c_g_2 = {n: c_g_2[i] for n, i in enumerate(sorted(c_g_2))}

        self.first.char_groups = c_g_1
        self.second.char_groups = c_g_2

    def __split_indices(self):
        self.first.len = len(self.first.content)
        self.second.len = len(self.second.content)
        self.second.start = self.second.start + self.idx

    def __split_syls(self):
        syls = self.first.syls
        # empty syls
        self.first.syls = []
        self.second.syls = []

        if syls:
            for syl in syls:
                if syl[-1] < self.idx:
                    self.first.syls.append(syl)

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
                        self.first.syls.append(part1)
                    if part2:
                        self.second.syls.append(part2)
