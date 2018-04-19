import copy
from .third_party import Query


class BoMatcher:
    def __init__(self, query):
        """
        Creates a matcher object to be later executed against a list of tokens with BoMatcher.match()

        :param query: CQL compliant query string
        :type query: string

        """
        self.query = Query(query)

    def match(self, tokens_list):
        """
        Runs cql.Query on a slice of the list of tokens for every index in the list.

        :param tokens_list: output of BoTokenizer
        :type tokens_list: list of Token objects
        :return: a list of matching slices of tokens_list
        :rtype: list of tuples with each two values: beginning and end indices
        """
        slice_len = len(self.query.tokenexprs) - 1
        matches = []
        for i in range(len(tokens_list) - 1):
            if i + slice_len <= len(tokens_list) and self.query(tokens_list[i:i + slice_len + 1]):
                matches.append((i, i + slice_len))
        return matches


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
    def __init__(self, token, split_idx, token1_changes=None, token2_changes=None):
        self.first = copy.deepcopy(token)
        self.second = copy.deepcopy(token)
        self.token1_changes = token1_changes
        self.token2_changes = token2_changes
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

    def replace_attrs(self):
        def cql2dict(query):
            """
            Expects the following syntax:
                '[attribute1="value1" & attribute2="value2" (& ...)]'
            """
            changes = {}
            for t_exprs in query.tokenexprs:
                for a_exprs in t_exprs:
                    key = a_exprs.attribute
                    value = a_exprs.valueexpr[0]
                    changes[key] = value
            return changes

        if self.token1_changes:
            changes1 = cql2dict(Query(self.token1_changes))
            for attr, value in changes1.items():
                setattr(self.first, attr, value)

        if self.token2_changes:
            changes2 = cql2dict(Query(self.token2_changes))
            for attr, value in changes2.items():
                setattr(self.second, attr, value)


class MatchSplit:
    def __init__(self, match_query, token_list):
        self.match_query = match_query
        self.token_list = token_list
        self.matcher = BoMatcher(match_query)
        self.token_split = TokenSplit

    def main(self):
        matches = self.matcher.match(self.token_list)
        for m in matches:
            print(m)


if __name__ == '__main__':
    test = [{'word': 'This',
             'lemma': 'this',
             'tag': 'Det'},
            {'word': 'is',
             'lemma': 'be',
             'tag': 'Verb'},
            {'word': 'it',
             'lemma': 'it',
             'tag': 'Pron'},
            {'word': '.',
             'lemma': '.',
             'tag': 'Punct'}]
    q = '[lemma="this" & tag="Det"] [tag!="ADJ"]'

    matcher = BoMatcher(q)
    matched = matcher.match(test)
    print(matched)
