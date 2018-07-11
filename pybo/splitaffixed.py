from .token import Token
from .helpers import AFFIX_SEP


class SplitAffixed:
    """
    A class to split Token objects produced by BoTokenizer.Tokenizer
    if they contain affixed particles

    .. note: should be rewritten with the inspiration of TokenSplit and
            TokenMerge. Could be a function instead of a class
    """

    def __init__(self):
        pass

    def split(self, tokens):
        """
        Splits in place the tokens containing affixed particles

        :param tokens: list of Token objects
        """
        def affixed_matcher(token):
            return AFFIX_SEP in token.tag and AFFIX_SEP * 3 not in token.tag

        t = 0
        while t <= len(tokens) - 1:
            if affixed_matcher(tokens[t]):
                # split token containing the affixed particle
                token1, token2 = self.split_token(tokens[t])

                # replace the original token with the two new ones
                tokens[t: t + 1] = [token1, token2]
                t += 1  # increment once more to account for the newly split token
            t += 1

    def split_token(self, token):
        def split_contents(content, split_idx):
            return content[:split_idx], content[split_idx:]

        def split_char_types(char_types, split_idx):
            return char_types[:split_idx], char_types[split_idx:]

        def split_char_groups(char_groups, split_idx):
            token_groups, affix_groups = {}, {}
            for idx, group in sorted(char_groups.items()):
                if idx < split_idx:
                    token_groups[idx] = group
                else:
                    affix_groups[idx] = group
            return token_groups, affix_groups

        def split_lengths(length, split_idx):
            return split_index, length - split_idx

        def split_syls(syls, split_idx):
            t_syls, a_syls = [], []
            for syl in syls:
                if syl[-1] < split_idx:
                    t_syls.append(syl)
                else:
                    token_part, affix_part = [], []
                    for i in syl:
                        if i < split_idx:
                            token_part.append(i)
                        else:
                            affix_part.append(i - split_idx)
                    t_syls.append(token_part)
                    a_syls.append(affix_part)
            return t_syls, a_syls

        pos, split_index, affix_type, aa = self.get_affix_info(token)
        token_content, affix_content = split_contents(token.content, split_index)
        token_char_groups, affix_char_groups = split_char_groups(token.char_groups, split_index)
        token_len, affix_length = split_lengths(token.len, split_index)
        token_tag, affix_tag = '{}{}{}{}'.format(pos, AFFIX_SEP, AFFIX_SEP, AFFIX_SEP), \
                               '{}{}{}{}{}'.format('PART', AFFIX_SEP, affix_type, AFFIX_SEP, AFFIX_SEP, aa)
        token_start, affix_start = token.start, token.start + token_len
        token_syls, affix_syls = split_syls(token.syls, split_index)
        token_char_types, affix_char_types = split_char_types(token.char_types, split_index)

        # un-affixed token object
        t = Token()
        t.content = token_content
        t.chunk_type = token.chunk_type
        t.type = token.type
        t.start = token_start
        t.len = token_len
        t.syls = token_syls
        t.tag = token_tag
        t.freq = token.freq
        t.skrt = token.skrt
        t.char_groups = token_char_groups
        t.char_types = token_char_types
        t.affix = False
        t.affixed = True
        if aa:
            t.aa_word = True
        t.get_pos_n_aa()

        # affix token object
        a = Token()
        a.content = affix_content
        a.chunk_type = token.chunk_type
        a.type = token.type
        a.start = affix_start
        a.len = affix_length
        a.syls = affix_syls
        a.tag = affix_tag
        # The affixed part frequency is not added for the moment in Pybo
        a.char_groups = affix_char_groups
        a.char_types = affix_char_types
        a.affix = True
        a.affixed = False
        a.get_pos_n_aa()

        return t, a

    def get_affix_info(self, token):
        pos, affix_type, affix_len, aa = token.tag.split(AFFIX_SEP)
        start_index = token.syls[-1][-int(affix_len)]
        return pos, start_index, affix_type, aa
