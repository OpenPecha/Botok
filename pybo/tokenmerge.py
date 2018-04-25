# coding: utf-8
import copy
from .third_party import parse_cql_query


class TokenMerge:
    """

    """
    def __init__(self, token1, token2, token_changes=None):
        self.token1 = token1
        self.token2 = token2
        self.merged = copy.deepcopy(token1)
        self.token_changes = parse_cql_query(token_changes)
        if token_changes:
            assert len(self.token_changes) == 1

    def merge(self):
        self.merge_attrs()
        self.replace_attrs()

        return self.merged

    def replace_attrs(self):
        """
        Replaces the content of attributes that were found in the cql query.
        If no query is provided, the values of the first token are kept.
        """
        if self.token_changes:
            for attr, value in self.token_changes[0].items():
                setattr(self.merged, attr, value)

    def merge_attrs(self):
        self.__merge_contents()
        self.__merge_char_groups()
        self.__merge_indices()
        self.__merge_syls()

    def __merge_contents(self):
        self.merged.content += self.token2.content

    def __merge_char_groups(self):
        last_idx = sorted(self.merged.char_groups.keys(), reverse=True)[0] + 1
        for idx in self.token2.char_groups.keys():
            new_idx = last_idx + idx
            self.merged.char_groups[new_idx] = self.token2.char_groups[idx]

    def __merge_indices(self):
        self.merged.length += self.token2.length

    def __merge_syls(self):
        """
        Updates indices and add the syls to the merged object
        Re-joins the host-syllable and affixed particle syllables into a single one
        """
        for num, syl in enumerate(self.token2.syls):
            new_syl = [i + self.token1.length for i in syl]

            # token1 is a host syllable and token2 its affixed syllable
            if num == 0 and (self.token1.affixed == True and self.token1.affix == False) and \
                    (self.token2.affixed == False and self.token2.affix == True):
                self.merged.syls[-1] += new_syl
            else:
                self.merged.syls.append(new_syl)
