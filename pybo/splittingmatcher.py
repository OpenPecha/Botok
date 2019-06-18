# coding: utf-8
from .third_party import Query
from .tokensplit import TokenSplit


class SplittingMatcher:
    def __init__(self, query, replace_idx, split_idx, token_list, token_changes=None):
        self.matcher = Query(query)
        self.span = len(self.matcher.tokenexprs) - 1
        self.token_list = token_list

        self.replace_idx = replace_idx - 1
        self.split_idx = split_idx
        self.token_changes = token_changes

    def split_on_matches(self):
        split_list = []

        i = 0
        while i < len(self.token_list):
            if self.__matches(i, self.token_list):
                # find the index of the token to split
                idx = i + self.replace_idx

                # add new tokens that precede the one to split
                for r in range(i, idx):
                    split_list.append(self.token_list[r])
                    i += 1

                # split the token and add them to the new list
                split_list.extend(self.__split(self.token_list[idx]))

            else:
                split_list.append(self.token_list[i])
            i += 1

        return split_list

    def __matches(self, i, token_list):
        return i + self.span <= len(token_list) \
            and self.matcher(self.token_list[i:i + self.span + 1])

    def __split(self, token):
        ts = TokenSplit(token, self.split_idx, self.token_changes)
        return ts.split()
