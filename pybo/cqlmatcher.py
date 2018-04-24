# coding: utf-8
from .third_party import Query


class CQLMatcher:
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

    matcher = CQLMatcher(q)
    matched = matcher.match(test)
    print(matched)
