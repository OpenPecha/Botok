
class Token:
    def __init__(self):
        self.content = None
        self.chunk_type = None
        self.char_groups = None
        self.start = 0
        self.length = None
        self.syls = None
        self.tag = None
        self.pos = None
        self.char_markers = {1: 'cons', 2: 'sub-cons', 3: 'vow', 4: 'tsek', 5: 'skrt-cons', 6: 'skrt-sub-cons',
                             7: 'skrt-vow', 8: 'punct', 9: 'num', 10: 'in-syl-mark', 11: 'special-punct', 12: 'symbol',
                             13: 'no-bo-no-skrt', 14: 'other', 15: 'space', 16: 'underscore'}
        self.chunk_markers = {100: 'bo', 101: 'non-bo', 102: 'punct', 103: 'non-punct', 104: 'space', 105: 'non-space',
                              106: 'syl', 1000: 'word', 1001: 'non-word'}

    def __getitem__(self, item):
        mapping = {'content': self.content,
                   'chunk_type': self.chunk_type,
                   'start': self.start,
                   'length': self.length,
                   'syls': self.syls,
                   'tag': self.tag,
                   'pos': self.pos}
        if item in mapping:
            return mapping[item]
        else:
            return None

    def get_pos(self):
        affix_sep = 'ᛃ'
        if affix_sep in self.tag:
            self.pos = self.tag.split(affix_sep)[0]
        else:
            self.pos = self.tag

    @property
    def cleaned_content(self):
        """
        Will add a tsek at every syllable.
        Warning: Since it is unaware (at the moment) of syllables that have been
        separated from their affixed particles, it will add a tsek in the middle
        """
        if self.syls:
            return ''.join([''.join([self.content[idx] for idx in syl] + ['་']) for syl in self.syls])
        else:
            return None

    def __repr__(self):
        out = 'content: "'+self.content+'"'
        out += '\nchar types: '
        out += '|'+'|'.join([self.char_markers[self.char_groups[idx]]
                            for idx in sorted(self.char_groups.keys())])+'|'
        out += '\ntype: ' + self.chunk_markers[self.chunk_type]
        out += '\nstart in input: ' + str(self.start)
        out += '\nlength: ' + str(self.length)
        out += '\nsyl chars in content'
        if self.syls:
            out += '(' + ' '.join([''.join([self.content[char] for char in syl]) for syl in self.syls]) + '): '
        else:
            out += ': '
        out += str(self.syls)
        out += '\ntag: ' + self.tag
        out += '\nPOS: ' + self.pos
        return out


class SplitAffixed:
    """
    A class to split Token objects produced by BoTokenizer.Tokenizer
    if they contain affixed particles


    """

    def __init__(self):
        self.tag_sep = 'ᛃ'

    def split(self, tokens):
        """
        Splits in place the tokens containing affixed particles

        :param tokens: list of Token objects
        """
        def affixed_matcher(token):
            return self.tag_sep in token.tag and self.tag_sep * 3 not in token.tag

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
                if syl[-1] <= split_idx:
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
        token_length, affix_length = split_lengths(token.length, split_index)
        token_tag, affix_tag = '{}{}{}'.format(pos, self.tag_sep, self.tag_sep), \
                               '{}{}{}{}{}'.format('PART', self.tag_sep, affix_type, self.tag_sep, aa)
        token_start, affix_start = token.start, token.start + token_length
        token_syls, affix_syls = split_syls(token.syls, split_index)

        # un-affixed token object
        t = Token()
        t.content = token_content
        t.chunk_type = token.chunk_type
        t.start = token_start
        t.length = token_length
        t.syls = token_syls
        t.tag = token_tag
        t.char_groups = token_char_groups

        # affix token object
        a = Token()
        a.content = affix_content
        a.chunk_type = token.chunk_type
        a.start = affix_start
        a.length = affix_length
        a.syls = affix_syls
        a.tag = affix_tag
        a.char_groups = affix_char_groups

        return t, a

    def get_affix_info(self, token):
        pos, affix_type, affix_len, aa = token.tag.split(self.tag_sep)
        start_index = len(token.content) - 1 - int(affix_len)
        return pos, start_index, affix_type, aa


class Tokenizer:
    """
    Expects a PyBoTrie instance as trie
    """
    def __init__(self, trie):
        self.pre_processed = None
        self.trie = trie
        self.WORD = 1000
        self.NON_WORD = 1001

    def tokenize(self, pre_processed, split_affixes=True, debug=False):
        """

        :param pre_processed: PyBoTextChunks of the text to be tokenized
        :param split_affixes: splits affixed particles inside tokens if True,
                              else keeps affixed tokens
        :param debug: prints debug info in True
        :return: a list of Token objects
        """
        self.pre_processed = pre_processed
        tokens = []
        syls = []
        match_data = {}  # keys: c_idx, values: trie data (for last and second-last matches)

        current_node = None
        went_to_max = False

        c_idx = 0
        while c_idx < len(self.pre_processed.chunks):
            has_decremented = False
            is_non_word = False
            chunk = self.pre_processed.chunks[c_idx]

            # 1. CHUNK IS SYLLABLE
            if chunk[0]:
                # syl is extracted from input string, tsek added for the trie
                syl = [self.pre_processed.string[idx] for idx in chunk[0]] + ['་']
                self.debug(debug, syl)

                # >>> WALKING THE TRIE >>>
                s_idx = 0
                while s_idx <= len(syl)-1:
                    # beginning of current syllable
                    if s_idx == 0:
                        self.debug(debug, syl[s_idx])

                        # begining of current word
                        if not current_node:
                            current_node = self.trie.walk(syl[s_idx], self.trie.head)
                            if current_node and current_node.is_match():
                                match_data[c_idx] = current_node.data

                        # walking resumed after previous syllable
                        else:
                            current_node = self.trie.walk(syl[s_idx], current_node)
                            if current_node and current_node.is_match():
                                match_data[c_idx] = current_node.data
                        s_idx += 1

                    # continuing to walk
                    elif current_node and current_node.can_walk():
                        self.debug(debug, syl[s_idx])
                        current_node = self.trie.walk(syl[s_idx], current_node)
                        if current_node and current_node.is_match():
                            match_data[c_idx] = current_node.data
                # <<<<<<<<<<<<<<<<<<<<<<<<

                        if not current_node and syls:
                            if not has_decremented:
                                c_idx -= 1
                                has_decremented = True
                            went_to_max = True
                        s_idx += 1

                    # CAN'T CONTINUE WALKING
                    else:

                        # a. potential word(syls) is not empty
                        if syls:
                            # need to finish looping over current syl
                            if went_to_max:
                                s_idx += 1
                                continue

                            # couldn't walk this syl until the end.
                            # decrementing chunk-idx for a new attempt to find a match
                            if not has_decremented:
                                c_idx -= 1
                                has_decremented = True  # ensures we only decrement once per syl
                            went_to_max = True

                        # b. current word is empty
                        else:
                            # there is only a non-word
                            is_non_word = True
                        s_idx += 1

                # FINISHED LOOPING OVER CURRENT SYL
                if is_non_word:
                    # non-word syls are turned into independant tokens
                    non_word = [c_idx]
                    tokens.append(self.chunks_to_token(non_word, self.NON_WORD))
                    match_data = {}
                    syls = []

                else:

                    if went_to_max:
                        if not has_decremented:
                            c_idx -= 1

                        else:
                            c_idx = self.add_found_word_or_non_word(c_idx, match_data, syls, tokens)
                            match_data = {}
                            syls = []
                        went_to_max = False

                    else:
                        syls.append(c_idx)

            # 2. CHUNK IS NON-SYLLABLE
            else:
                # if there is a word that was not added
                if syls:
                    # the word to add ends at c_idx - 1 since we reached the non-syllable chunk
                    c_idx = self.add_found_word_or_non_word(c_idx - 1, match_data, syls, tokens) + 1
                    match_data = {}
                    syls = []
                    current_node = None

                tokens.append(self.chunks_to_token([c_idx]))

            # END OF INPUT
            # if we reached end of input and there is a non-max-match
            if len(self.pre_processed.chunks) - 1 == c_idx:
                if match_data and current_node and not current_node.leaf:
                    c_idx = self.add_found_word_or_non_word(c_idx, match_data, syls, tokens)
                    syls = []
                    current_node = None
            c_idx += 1

        # a potential token was left
        if syls:
            self.add_found_word_or_non_word(c_idx, match_data, syls, tokens)

        self.pre_processed = None

        if split_affixes:
            SplitAffixed().split(tokens)
        return tokens

    def add_found_word_or_non_word(self, c_idx, match_data, syls, tokens):
        # there is a match
        if c_idx in match_data.keys():
            tokens.append(self.chunks_to_token(syls, tag=match_data[c_idx]))
        elif match_data:
            non_max_idx = sorted(match_data.keys())[-1]
            non_max_syls = []
            for syl in syls:
                if syl <= non_max_idx:
                    non_max_syls.append(syl)
            tokens.append(self.chunks_to_token(non_max_syls, tag=match_data[non_max_idx]))
            c_idx = non_max_idx
        else:
            # add first syl in syls as non-word
            tokens.append(self.chunks_to_token([syls[0]], self.NON_WORD))

            # decrement chunk-idx for a new attempt to find a match
            if syls:
                c_idx -= len(syls[1:]) - 1
        return c_idx

    def chunks_to_token(self, syls, tag=None, ttype=None):
        if len(syls) == 1:
            # chunk format: ([char_idx1, char_idx2, ...], (type, start_idx, len_idx))
            token_syls = [self.pre_processed.chunks[syls[0]][0]]
            token_type = self.pre_processed.chunks[syls[0]][1][0]
            token_start = self.pre_processed.chunks[syls[0]][1][1]
            token_length = self.pre_processed.chunks[syls[0]][1][2]
            if ttype:
                token_type = ttype

            return self.create_token(token_type, token_start, token_length, token_syls, tag)
        elif len(syls) > 1:
            token_syls = [self.pre_processed.chunks[idx][0] for idx in syls]
            token_type = self.pre_processed.chunks[syls[-1]][1][0]
            token_start = self.pre_processed.chunks[syls[0]][1][1]
            token_length = 0
            for i in syls:
                token_length += self.pre_processed.chunks[i][1][2]
            if ttype:
                token_type = ttype

            return self.create_token(token_type, token_start, token_length, token_syls, tag)
        else:
            return None  # should raise an error instead?

    def create_token(self, ttype, start, length, syls, tag=None):
        """

        :param ttype: token type
        :param start: start index in input string
        :param length: length of the substring from the input string corresponding to this token
        :param syls: syl representation coming from PyBoTextChunks.
                        the indices are modified to be usable on the substring corresponding to this token
        :param tag: the POS retrieved from the chunk or from the trie
        :return: a Token object with all the above information
        """
        token = Token()
        token.content = self.pre_processed.string[start:start+length]
        token.chunk_type = ttype
        token.start = start
        token.length = length
        if syls != [None]:
            token.syls = []
            for syl in syls:
                token.syls.append([i-start for i in syl])
        if not tag:
            token.tag = token.chunk_markers[ttype]
        else:
            if type(tag) == int:
                token.tag = token.chunk_markers[tag]
            else:
                token.tag = tag
        if token.tag:
            token.get_pos()
        token.char_groups = self.pre_processed.export_groups(start, length, for_substring=True)
        return token

    @staticmethod
    def debug(debug, to_print):
        if debug:
            print(to_print)
