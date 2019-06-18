# coding: utf-8
from .third_party import Query
from .tokenmerge import TokenMerge


class MergingMatcher:
    def __init__(self, query, replace_idx, token_list, token_changes=None):
        self.matcher = Query(query)
        self.span = len(self.matcher.tokenexprs) - 1
        self.token_list = token_list

        self.replace_idx = replace_idx - 1
        self.token_changes = token_changes

    def merge_on_matches(self):
        merged_list = []
        i = 0
        while i < len(self.token_list):
            if self.__matches(i):
                # find the index of the token to split
                idx = i + self.replace_idx

                # add new tokens that precede the one to split
                for r in range(i, idx):
                    merged_list.append(self.token_list[r])
                    i += 1

                # split the token and add them to the new list
                merged_list.append(self.__merge(self.token_list[idx], self.token_list[idx + 1]))
                i += 1
            else:
                merged_list.append(self.token_list[i])

            i += 1

        return merged_list

    def __matches(self, i):
        return i + self.span <= len(self.token_list) \
               and self.matcher(self.token_list[i:i + self.span + 1])

    def __merge(self, token1, token2):
        ts = TokenMerge(token1, token2, self.token_changes)
        return ts.merge()
