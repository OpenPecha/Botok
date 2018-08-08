# coding: utf-8
from .token import Token
from .splitaffixed import SplitAffixed
from .helpers import AFFIX_SEP
# import bophono


class Tokenizer:
    """
    Expects a PyBoTrie instance as trie
    """
    def __init__(self, trie):
        self.pre_processed = None
        self.trie = trie
        self.WORD = 1000
        self.OOV = 1001

        # self.bophono_options = {
        #     'aspirateLowTones': True,
        #     'prefixStrategy': 'always'
        # }

    def tokenize(self, pre_processed, split_affixes=True, phono=False, debug=False):
        """

        :param pre_processed: PyBoTextChunks of the text to be tokenized
        :param split_affixes: splits affixed particles inside tokens if True,
                              else keeps affixed tokens
        :param debug: prints debug info in True
        :return: a list of Token objects
        """
        # self.phono_switch = phono
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
                if chunk[0][-1] < pre_processed.len - 1 and self.pre_processed.string[chunk[0][-1]+1] == "ཿ":
                    syl = [self.pre_processed.string[idx] for idx in chunk[0]] + ['ཿ']
                else:
                    syl = [self.pre_processed.string[idx] for idx in chunk[0]] + ['་']
                self.debug(debug, syl)

                # >>> WALKING THE TRIE >>>
                s_idx = 0
                while s_idx <= len(syl)-1:
                    # beginning of current syllable
                    if s_idx == 0:
                        self.debug(debug, syl[s_idx])
                        current_node = self.trie.walk(syl[s_idx], current_node)
                        if current_node and current_node.is_match():
                            match_data[c_idx] = (current_node.data, current_node.freq, current_node.skrt)

                    # continuing to walk
                    elif current_node and current_node.can_walk():
                        self.debug(debug, syl[s_idx])
                        current_node = self.trie.walk(syl[s_idx], current_node)
                        if current_node and current_node.is_match():
                            match_data[c_idx] = (current_node.data, current_node.freq, current_node.skrt)
                # <<<<<<<<<<<<<<<<<<<<<<<<

                        elif not current_node:
                            if syls:
                                if not has_decremented:
                                    c_idx -= 1
                                    has_decremented = True
                                went_to_max = True
                            else:
                                is_non_word = True

                    # CAN'T CONTINUE WALKING
                    else:
                        # a. potential word(syls) is not empty
                        if syls:
                            # couldn't walk this syl until the end.
                            # decrementing chunk-idx for a new attempt to find a match
                            if not (has_decremented or went_to_max):
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
                    # This syllabe does not exist in the Trie
                    tokens.append(self.chunks_to_token(non_word, "non-word"))
                    match_data = {}
                    syls = []

                else:
                    if went_to_max:
                        if not has_decremented:
                            c_idx -= 1
                        else:
                            c_idx = self.add_found_word_or_non_word(c_idx, match_data, syls, tokens, has_decremented)
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
                    continue

                tokens.append(self.chunks_to_token([c_idx]))

            # END OF INPUT
            # if we reached end of input and there is a non-max-match
            if len(self.pre_processed.chunks) - 1 == c_idx:
                if any(match_data.values()) and current_node and not current_node.leaf:
                    c_idx = self.add_found_word_or_non_word(c_idx, match_data, syls, tokens)
                    syls = []
                    current_node = None
                if has_decremented:
                    c_idx -= 1

            c_idx += 1

        # a potential token was left
        if syls:
            self.add_found_word_or_non_word(c_idx, match_data, syls, tokens)

        self.pre_processed = None

        if split_affixes:
            SplitAffixed().split(tokens)
        return tokens

    def add_found_word_or_non_word(self, c_idx, match_data, syls, tokens, has_decremented=False):
        # there is a match
        if c_idx in match_data.keys():
            tokens.append(self.chunks_to_token(syls, tag=match_data[c_idx][0], freq=match_data[c_idx][1], skrt=match_data[c_idx][2]))
        elif any(match_data.values()):
            non_max_idx = sorted(match_data.keys())[-1]
            non_max_syls = []
            for syl in syls:
                if syl <= non_max_idx:
                    non_max_syls.append(syl)
            tokens.append(self.chunks_to_token(non_max_syls,
                                               tag=match_data[non_max_idx][0],
                                               freq=match_data[non_max_idx][1],
                                               skrt=match_data[non_max_idx][2]))
            c_idx = non_max_idx
        else:
            # add first syl in syls as non-word
            tokens.append(self.chunks_to_token([syls[0]], self.OOV))

            # decrement chunk-idx for a new attempt to find a match
            if syls:
                c_idx -= len(syls[1:]) - 1
            if has_decremented or (c_idx < len(self.pre_processed.chunks) and self.pre_processed.chunks[c_idx][0] == None)  or len(syls) > 1:
                c_idx -= 1
        return c_idx

    def chunks_to_token(self, syls, tag=None, freq=None, skrt=None, ttype=None):
        if len(syls) == 1:
            # chunk format: ([char_idx1, char_idx2, ...], (type, start_idx, len_idx))
            token_syls = [self.pre_processed.chunks[syls[0]][0]]
            token_type = self.pre_processed.chunks[syls[0]][1][0]
            token_start = self.pre_processed.chunks[syls[0]][1][1]
            token_length = self.pre_processed.chunks[syls[0]][1][2]
            if ttype:
                token_type = ttype

            return self.create_token(token_type, token_start, token_length, token_syls, tag, freq, skrt)
        elif len(syls) > 1:
            token_syls = [self.pre_processed.chunks[idx][0] for idx in syls]
            token_type = self.pre_processed.chunks[syls[-1]][1][0]
            token_start = self.pre_processed.chunks[syls[0]][1][1]
            token_length = 0
            for i in syls:
                token_length += self.pre_processed.chunks[i][1][2]
            if ttype:
                token_type = ttype

            return self.create_token(token_type, token_start, token_length, token_syls, tag, freq, skrt)
        else:
            return None  # should raise an error instead?

    def create_token(self, ttype, start, length, syls, tag=None, freq=None, skrt=None):
        """
        :param ttype: token type
        :param start: start index in input string
        :param length: length of the substring from the input string corresponding to this token
        :param syls: syl representation coming from PyBoTextChunks.
                        the indices are modified to be usable on the substring corresponding to this token
        :param tag: the POS retrieved from the chunk or from the trie
        :param freq: the frequency retrieved from from the trie
        :return: a Token object with all the above information
        """
        token = Token()
        token.content = self.pre_processed.string[start:start+length]
        # if self.phono_switch:
        #     token.phono = bophono.UnicodeToApi(options=self.bophono_options).get_api(token.content)
        token.chunk_type = ttype
        token.type = token.chunk_markers[ttype]
        token.start = start
        token.len = length
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
            token.get_pos_n_aa()
        if AFFIX_SEP in token.tag and not AFFIX_SEP * 3 in token.tag:
            token.affix = True
            token.affixed = True
        token.char_groups = self.pre_processed.export_groups(start, length, for_substring=True)
        token.char_types = [token.char_markers[token.char_groups[idx]] for idx in sorted(token.char_groups.keys())]
        if skrt:
            token.skrt = True
        else:
            token.skrt = self.sanskrit(token)
        if freq:
            token.freq = freq
        else:
            token.freq = None
        return token

    def sanskrit(self, token):
        return self._has_skrt_syl(token) or self._has_skrt_char(token)

    def _has_skrt_char(self, token):
        return self.pre_processed.SKRT_VOW in token.char_groups.values() or \
               self.pre_processed.SKRT_CONS in token.char_groups.values() or \
               self.pre_processed.SKRT_SUB_CONS in token.char_groups.values()

    def _has_skrt_syl(self, token):
        """
        Generates the pre-processed syl str, then tests whether it is a
        Sanskrit syl.

        :param token: token to test
        :return: True if the token contains a Sanskrit syllable, False otherwise
        """
        has_skrt = False
        if token.syls:
            for syl in token.syls:
                clean_syl = ''.join([token.content[s] for s in syl])
                if self.pre_processed._is_skrt_syl(clean_syl):
                    has_skrt = True
        return has_skrt

    @staticmethod
    def debug(debug, to_print):
        if debug:
            print(to_print)
