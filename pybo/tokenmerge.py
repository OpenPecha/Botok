# coding: utf-8
import copy
from .third_party import replace_token_attributes


class TokenMerge:
    """

    """
    def __init__(self, token1, token2, token_changes=None):
        self.token1 = token1
        self.token2 = token2
        self.merged = copy.deepcopy(token1)
        self.token_changes = token_changes

    def merge(self):
        self.merge_attrs()
        self.replace_attrs()
        self.merged.get_pos_n_aa()
        return self.merged

    def replace_attrs(self):
        """
        Replaces the content of attributes that were found in the cql query.
        If no query is provided, the values of the first token are kept.
        """
        if self.token_changes:
            replace_token_attributes(self.merged, self.token_changes)

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
        self.merged.len += self.token2.len

    def __merge_syls(self):
        """
        Updates indices and add the syls to the merged object
        Re-joins the host-syllable and affixed particle syllables into a single one;
        then, affix is True and affixed also, so cleaned_content gets its tsek.
        """
        first_syl = True
        if self.token2.syls:
            for syl in self.token2.syls:
                if syl:
                    new_syl = [i + self.token1.len for i in syl]

                    # token1 is a host syllable and token2 its affixed syllable
                    if first_syl and (self.token1.affixed and not self.token1.affix) \
                            and (not self.token2.affixed and self.token2.affix):
                        self.merged.syls[-1] += new_syl
                        self.merged.affix = True
                        first_syl = False
                    else:
                        self.merged.syls.append(new_syl)
