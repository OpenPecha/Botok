# coding: utf-8
import copy
from .third_party.cql import Query


class TokenSplit:
    """
    Takes a token object and divide it into two using an index of the content.

    The affected attributes are:
        - token.content     : the string is split at the index
        - token.char_groups : the dict items are redistributed
        - token.start       : second token only. now equals "start + index"
        - token.length      : length of new content
        - token.syls        : syls are redistributed and split if necessary

    """
    def __init__(self, token, split_idx, token_changes=None):
        self.first = copy.deepcopy(token)
        self.second = copy.deepcopy(token)
        self.token1_changes, self.token2_changes = self.__parse_query(token_changes)
        self.idx = split_idx

    def split(self):
        self.split_on_idx()
        self.replace_attrs()

        return self.first, self.second

    def split_on_idx(self):
        self.__split_contents()
        self.__split_char_groups()
        self.__split_indices()
        self.__split_syls()

    def replace_attrs(self):

        if self.token1_changes:
            for attr, value in self.token1_changes.items():
                setattr(self.first, attr, value)

        if self.token2_changes:
            for attr, value in self.token2_changes.items():
                setattr(self.second, attr, value)

    @staticmethod
    def __parse_query(query):
        def cql2dict(tokenexpr):
            """
            Expects the following syntax:
                '[attribute1="value1" & attribute2="value2" (& ...)]'
            """
            changes = {}
            for attrexprs in tokenexpr:
                key = attrexprs.attribute
                value = attrexprs.valueexpr[0]
                changes[key] = value
            return changes

        if query:
            parsed = Query(query)
            assert len(parsed.tokenexprs) == 2
            return cql2dict(parsed.tokenexprs[0]), cql2dict(parsed.tokenexprs[1])
        else:
            return None, None

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
        self.first.length = len(self.first.content)
        self.second.length = len(self.second.content)
        self.second.start = self.second.start + self.idx

    def __split_syls(self):
        syls = self.first.syls
        # empty syls
        self.first.syls = []
        self.second.syls = []

        if syls:
            for syl in syls:
                if syl[-1] <= self.idx:
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
