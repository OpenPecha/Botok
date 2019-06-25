# coding: utf-8
from .tokensplit import TokenSplit


def split_affixed(tokens):
    """
    Splits in place the tokens containing affixed particles
    tokens have to be Token objects produced by BoTokenizer.Tokenizer

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
