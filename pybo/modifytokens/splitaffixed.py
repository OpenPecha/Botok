# coding: utf-8
from .tokensplit import TokenSplit


class SplitAffixed:
    """
    A class to split Token objects produced by BoTokenizer.Tokenizer
    if they contain affixed particles

    .. note: should be rewritten with the inspiration of TokenSplit and
            TokenMerge. Could be a function instead of a class
    """
    def split(self, tokens):
        """
        Splits in place the tokens containing affixed particles

        :param tokens: list of Token objects
        """
        t = 0
        while t <= len(tokens) - 1:
            if tokens[t].affixation:
                # split token containing the affixed particle
                split_idx = tokens[t].syls_idx[-1][-tokens[t].affixation['len']]
                changes = '[affix="False"] ' \
                          '[pos="PART" & affix_host="False" & skrt="False" & freq="None"]'
                ts = TokenSplit(tokens[t], split_idx, token_changes=changes)
                token1, token2 = ts.split()

                # replace the original token with the two new ones
                tokens[t: t + 1] = [token1, token2]

                t += 1  # increment once more to account for the newly split token
            t += 1
