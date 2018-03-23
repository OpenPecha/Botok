class TokenSplit:
    """
    A class to split Token objects produced by Tokenizer


    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.matcher = BoMatcher()

    def split_affixed_particles(self):
        self.__split(self.tokens, self.matcher)

    @staticmethod
    def __split(tokens, matcher):
        def split_token(token, idx):
            """
            :param token: Token to split
            :param split_idx: index at which the token should be split
            :return: the two new tokens
            """
            return 'new1', 'new2'

        t = 0
        while t <= len(tokens) - 1:
            fulfilled, split_idx = matcher(tokens, t)
            if fulfilled:
                # split at split_idx
                new1, new2 = split_token(tokens[t], split_idx)

                # replace the original token with the two new ones
                tokens[t:t + 1] = [new1, new2]

                t += 1  # increment once more to account for the newly split token
            t += 1


class BoMatcher:
    def __init__(self, query):
        """

        :param query: subset of CQL (see parse() for the supported format)

        """
        self.parsed_query = self.parse(query)

    def match(self, tokens):
        """

        :param tokens:  list of token objects.
                        tokens can be of any type as long as they allow to access
                        the attributes with a dict-like syntax: token['attr']
        """

        matching_indices = []
        for token_count in range(len(tokens) - 1):
            if self.match_slice(tokens[token_count:len(self.parsed_query)]):
                matching_indices.append(token_count)
        return matching_indices

    def match_slice(self, slice_of_tokens):
        """
        tests the query in self.parsed_query on a given slice of the token list

        :param slice_of_tokens: a sublist of tokens to be tested
        :return: True if the tests for all the attributes pass, False otherwise
        """
        # sanity check
        if len(self.parsed_query) == len(slice_of_tokens):

            match = []  # content: boolean. each is the final result for one token slot
            for slot_count in range(len(self.parsed_query)):

                slot_match = []  # content: boolean. one per attribute within one slot
                for to_check in self.parsed_query[slot_count]:

                    attr, op, value = to_check
                    if attr in slice_of_tokens[slot_count]:
                        if op == '=' and slice_of_tokens[slot_count][attr] == value:
                                slot_match.append(True)
                        elif op == '!=' and slice_of_tokens[slot_count][attr] != value:
                            slot_match.append(True)
                        else:
                            slot_match.append(False)
                    else:
                        slot_match.append(False)  # attr was not in current token

                if False in slot_match:
                    match.append(False)
                else:
                    match.append(True)

            return False not in match
        else:
            return False  # slice of tokens was not the right size

    @staticmethod
    def parse(query):
        """
        Parses a query using a subset of CQL into a Python structure.

        Tries to be as effective as possible by splitting on unambiguous
        parts of the query.

        :param query:
                    formatted in the following way:
                        - ' ': tokens
                        - ' & ': token attributes
                        - 'xxx': attribute key
                        - '=' or '!=': attribute operator
                        - '"yyy"': attribute value.
        :return:
                    '[text="abc" & pos="NOUN"] [pos!="ADJ"]'
                    yields: [[("text", "=", "abc"),
                              ("pos", "=", "NOUN")],

                             [("pos", "!=", "ADJ")]]
        """
        parsed_query = []
        token_slots = [a.replace('[', '').replace(']', '') for a in query.split('] [')]
        for slot in token_slots:
            parsed_slot = []
            attributes = slot.split(' & ')
            for a in attributes:
                if '!=' in a:
                    attr, value = a.split('!=')
                    value = value[1:-1]
                    parsed_slot.append((attr, '!=', value))
                else:
                    attr, value = a.split('=')
                    value = value[1:-1]
                    parsed_slot.append((attr, '=', value))
            parsed_query.append(parsed_slot)
        return parsed_query


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
             'tag': 'Punct'},
            {''}]
    q = '[lemma="this" & tag="Det"] [tag!="ADJ"]'

    matcher = BoMatcher(q)
    parsed = matcher.parse(q)
    print(parsed)
    print(matcher.match(test))
