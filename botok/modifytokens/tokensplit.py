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

    def split(self, mode="char"):
        """
        :param mode: can either be "syl" or "char" to split on a syllable index or a character index.
        """
        if mode != "char" and mode != "syl":
            raise SyntaxError("splitting mode should either be 'syl' or 'char'. ")

        # in syllable-mode, if there is only one syllable, return the word without splitting it.
        if mode == "syl" and len(self.token.syls) == 1:
            return [self.token]

        self.split_on_idx(mode=mode)
        self.replace_attrs()

        return [self.first, self.second]

    def replace_attrs(self):
        if self.token_changes:
            tokens = [self.first, self.second]
            replace_token_attributes(tokens, self.token_changes)
            self.first, self.second = tokens

    def split_on_idx(self, mode):
        self.first = copy.deepcopy(self.token)
        self.second = copy.deepcopy(self.token)

        if mode == "syl":
            self.idx = self.token.syls_start_end[self.idx - 1]["end"]

        self.__split_contents()
        self.__split_indices()
        self.__split_syls_idx()
        self.__split_syls_start_end(mode)
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

    def __split_syls_start_end(self, mode):
        if not self.token.syls_start_end:
            return

        to_split_idx = 0
        for num, s in enumerate(self.token.syls_start_end):
            if s["start"] <= self.idx <= s["end"]:
                to_split_idx = num
                break  # ensure to exit on first match

        start = self.token.syls_start_end[:to_split_idx]
        end = self.token.syls_start_end[to_split_idx + 1 :]
        to_split = self.token.syls_start_end[to_split_idx]

        if mode == "char":
            start.append({"start": to_split["start"], "end": self.idx})
            end.append({"start": self.idx, "end": to_split["end"]})

        if mode == "syl":
            start.append(to_split)

        self.first.syls_start_end = start
        self.second.syls_start_end = end

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
            self.first.affixation.pop("len", '')
            self.first.affixation.pop("type", '')
            self.second.affixation.pop("aa", '')
