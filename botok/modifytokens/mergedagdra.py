# coding: utf-8
from .tokenmerge import TokenMerge
from ..vars import TSEK, DAGDRA


class MergeDagdra:
    """
    A class to merge pa/po/ba/bo tokens in a token list produced by BoTokenizer

    """

    def __init__(self):
        pass

    def merge(self, tokens):
        """
        Merges the tokens containing either pa/po/ba/bo

        :param tokens: list of Token objects
        """
        if len(tokens) <= 1:
            pass
        elif len(tokens) == 2:
            token0, token1 = tokens
            if token1.text_cleaned in DAGDRA:
                # split token containing the affixed particle
                merged = self.merge_with_previous_token(token0, token1)
                del tokens[1]
                tokens[0] = merged
        else:
            t = 0
            while t <= len(tokens) - 1:
                if t + 1 > len(tokens) - 1:
                    break
                token0, token1 = tokens[t], tokens[t + 1]
                clean_word = (
                    token1.text_cleaned + TSEK
                    if not token1.text_cleaned.endswith(TSEK)
                    else token1.text_cleaned
                )
                if (
                    token0.chunk_type == "TEXT"
                    and token1.chunk_type == "TEXT"
                    and clean_word in DAGDRA
                ):
                    # split token containing the affixed particle
                    merged = self.merge_with_previous_token(token0, token1)

                    # replace the original token with the two new ones
                    tokens[t: t + 2] = [merged]
                t += 1

    def merge_with_previous_token(self, token0, token1):
        merged = TokenMerge(token0, token1).merge()
        merged.has_merged_dagdra = True
        return merged
