from .third_party import Query, replace_token_attributes


class ReplacingMatcher:
    def __init__(self, query, replace_idx, token_list, token_changes=None):
        self.matcher = Query(query)
        self.span = len(self.matcher.tokenexprs) - 1
        self.replace_idx = replace_idx - 1
        self.token_list = token_list
        self.token_changes = token_changes

    def replace_on_matches(self):
        i = 0
        while i < len(self.token_list):
            if self.__matches(i):
                # find the index of the token to split
                idx = i + self.replace_idx
                replace_token_attributes(self.token_list[idx], self.token_changes)
            i += 1

    def __matches(self, i):
        return i + self.span <= len(self.token_list) \
            and self.matcher(self.token_list[i:i + self.span + 1])
