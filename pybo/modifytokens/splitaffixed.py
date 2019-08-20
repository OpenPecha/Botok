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
        # check that splitting is possible (affixation attribute exists)
        # and that there is no meaning that has "affixed: False".
        # ie, check that the inflected form can't be the affixed form of a word and the unaffixed form of another word
        if tokens[t].affixation and not [
            True for m in tokens[t].entries if "affixed" in m and not m["affixed"]
        ]:
            # split token containing the affixed particle
            split_idx = tokens[t].syls_idx[-1][-tokens[t].affixation["len"]]
            changes = (
                '[affix_host="True"] '
                '[pos="PART" & affix="True" & skrt="False" & freq="None" & entries="None"]'
            )
            ts = TokenSplit(tokens[t], split_idx, token_changes=changes)
            token1, token2 = ts.split()
            if token2.entries is None:
                token2.entries = []

            # replace the original token with the two new ones
            tokens[t : t + 1] = [token1, token2]

            t += 1  # increment once more to account for the newly split token
        t += 1
