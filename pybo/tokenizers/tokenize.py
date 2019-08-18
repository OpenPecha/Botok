# coding: utf-8
from .token import Token
from ..vars import NAMCHE, TSEK
from ..vars import chunk_values as u
from ..vars import char_values as a
from ..vars import CharMarkers as A
from ..vars import WordMarkers as w
from ..third_party.has_skrt_syl import has_skrt_syl


class Tokenize:
    """
    Expects a BoTrie instance as trie
    """
    def __init__(self, trie):
        self.pre_processed = None
        self.trie = trie

    def tokenize(self, pre_processed, debug=False):
        """

        :param pre_processed: PyBoTextChunks of the text to be tokenized
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
        while c_idx <= len(self.pre_processed.chunks):
            syl, chunk = self.pre_processed.chunks[c_idx]
            syl = ''.join([self.pre_processed.bs.string[s] for s in syl])
            self.debug(debug, syl)


            c_idx += 1

        return tokens

    def add_found_word_or_non_word(self, c_idx, match_data, syls, tokens, has_decremented=False):
        # there is a match
        if c_idx in match_data.keys():
            data = match_data[c_idx]
            ttype = w.OOV.name if 'entries' not in data or len([True for m in data['entries'] if 'pos' in m]) <= 0 else None
            tokens.append(self.chunks_to_token(syls, data, ttype=ttype))
        elif any(match_data.values()):
            non_max_idx = sorted(match_data.keys())[-1]
            non_max_syls = []
            for syl in syls:
                if syl <= non_max_idx:
                    non_max_syls.append(syl)
            data = match_data[non_max_idx]
            ttype = w.OOV.name if 'entries' not in data or len([True for m in data['entries'] if 'pos' in m]) <= 0 else None
            tokens.append(self.chunks_to_token(non_max_syls, data, ttype=ttype))
            c_idx = non_max_idx
        else:
            # add first syl in syls as non-word
            tokens.append(self.chunks_to_token([syls[0]], {}, ttype=w.OOV.name))

            # decrement chunk-idx for a new attempt to find a match
            if syls:
                c_idx -= len(syls[1:]) - 1
            if has_decremented \
               or (c_idx < len(self.pre_processed.chunks)
                   and self.pre_processed.chunks[c_idx][0] is None) \
               or len(syls) > 1:
                c_idx -= 1
        return c_idx

    def chunks_to_token(self, syls, data, ttype=None):
        if len(syls) == 1:
            # chunk format: ([char_idx1, char_idx2, ...], (type, start_idx, len_idx))
            token_syls = [self.pre_processed.chunks[syls[0]][0]]
            token_type = self.pre_processed.chunks[syls[0]][1][0]
            token_start = self.pre_processed.chunks[syls[0]][1][1]
            token_length = self.pre_processed.chunks[syls[0]][1][2]
            if ttype:
                if 'entries' not in data:
                    data['entries'] = [{'pos': ttype}]
                else:
                    for m in data['entries']:
                        if 'pos' not in m:
                            m['pos'] = ttype

            return self.create_token(token_type, token_start, token_length, token_syls, data)
        elif len(syls) > 1:
            token_syls = [self.pre_processed.chunks[idx][0] for idx in syls]
            token_type = self.pre_processed.chunks[syls[-1]][1][0]
            token_start = self.pre_processed.chunks[syls[0]][1][1]
            token_length = 0
            for i in syls:
                token_length += self.pre_processed.chunks[i][1][2]
            if ttype:
                if 'entries' not in data:
                    data['entries'] = [{'pos': ttype}]
                else:
                    for m in data['entries']:
                        if 'pos' not in m:
                            m['pos'] = ttype

            return self.create_token(token_type, token_start, token_length, token_syls, data)
        else:
            raise ValueError(str(syls) + 'should contain at least 1 token')

    def create_token(self, ttype, start, length, syls, data):
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
        token.text = self.pre_processed.bs.string[start:start + length]
        token.chunk_type = u[ttype]
        token.start = start
        token.len = length
        if syls != [None]:
            token.syls_idx = [[s - start for s in syl] for syl in syls]
        char_groups = self.pre_processed.bs.export_groups(start, length, for_substring=True)
        token.char_types = [a[char_groups[idx]] for idx in sorted(char_groups.keys())]
        for k, v in data.items():
            token[k] = v
        token.skrt = self.is_sanskrit(char_groups, token.text) if not token.skrt else token.skrt
        return token

    def is_sanskrit(self, char_groups, word):
        return self._has_skrt_char(char_groups) or has_skrt_syl(word)

    def _has_skrt_char(self, char_groups):
        return A.SKRT_VOW in char_groups.values() or \
               A.SKRT_CONS in char_groups.values() or \
               A.SKRT_SUB_CONS in char_groups.values()

    @staticmethod
    def debug(debug, to_print):
        if debug:
            print(to_print, flush=True)
