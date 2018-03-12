class TokenSplit:
    """
    A class to split Token objects produced by Tokenizer


    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.matcher = BoMatcher()

    def split_affixed_particles(self):
        self.__split(self.tokens, self.matcher.match_affixed)

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
    """
    Matchers for a list of tokens produced by BoTokenizer

    A matcher is composed of:
        - a method calling __match_using()

        - a "__has_(...)" or "__is_(...)" method that decides whether
            the match will return True or False

        - a "__get_(...)_idx" method that implements the strategy
            to get the index where splitting will happen

    Is meant to be CQL compliant.
    """

    def __init__(self):
        pass

    def parse(self, query):
        conditions = query.split(' ')
        return True

    def match_affixed(self, tokens, current_idx):
        return self.__match_using(self.__has_affix, self.__get_affixed_idx, tokens, current_idx )

    @staticmethod
    def __has_affix(tokens, current_idx):
        """
        Checks whether the given token contains an affixed particle
        """
        AFFIX_SEP = 'ᛃ'
        return AFFIX_SEP in tokens[current_idx].tag and \
            AFFIX_SEP * 3 not in tokens[current_idx].tag

    @staticmethod
    def __get_affixed_idx(token):
        AFFIX_SEP = 'ᛃ'
        return token.length - int(token.tag.split(AFFIX_SEP)[2])

    @staticmethod
    def __match_using(condition, get_idx, tokens, current_idx):
        contains = condition(tokens, current_idx)

        idx = -1
        if contains:
            idx = get_idx(tokens[current_idx])

        return contains, idx
