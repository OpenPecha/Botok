from pybo import *
import copy


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
    Takes a token object and devide it into two.

    By default, makes a clone of the object, then applies any modification
    as defined in the replacement command
    """
    def __init__(self, token, split_idx):
        self.first = copy.deepcopy(token)
        self.second = copy.deepcopy(token)
        self.idx = split_idx

    def split(self):
        self.split_contents()
        self.split_char_groups()

        return self.first, self.second

    def split_contents(self):
        content = self.first.content
        self.first.content = content[0:self.idx]
        self.second.content = content[self.idx:]

    def split_char_groups(self):
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
    matches = matcher.match(test)
    print(matches)
