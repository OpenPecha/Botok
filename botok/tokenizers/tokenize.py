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
        max_match = []

        cur_node = self.trie.head
        cur_chunk_idx = 0

        while cur_chunk_idx < len(self.pre_processed.chunks):
            max_match_walker = cur_chunk_idx
            # >>> WALKING THE TRIE >>>
            while max_match_walker < len(self.pre_processed.chunks):
                cur_syl, cur_chunk = self.pre_processed.chunks[max_match_walker]

                # 1. CHUNK IS SYLLABLE
                if cur_syl:
                    syl = ''.join([self.pre_processed.bs.string[i] for i in cur_syl])
                    cur_node = self.trie.walk(syl, cur_node)
                    if cur_node:
                        max_match.append(max_match_walker)
                        cur_chunk_idx += 1

                        # CAN'T CONTINUE WALKING
                        if cur_node.is_match() and not cur_node.can_walk():
                            break;
                        max_match_walker += 1
                    # OOV
                    else:
                        tokens.append(
                            self.chunks_to_token([max_match_walker], {}, ttype=w.NON_WORD.name)
                        )
                        cur_node = self.trie.head
                        cur_chunk_idx += 1
                        break
                # 2. CHUNK IS NON-SYLLABLE
                else:
                    tokens.append(
                            self.chunks_to_token([max_match_walker], {})
                        )
                    cur_chunk_idx += 1
                    break
            if max_match:
                tokens.append(
                    self.chunks_to_token(max_match, cur_node.data)
                )
                max_match = []
                cur_node = self.trie.head

        self.pre_processed = None

        return tokens

    def add_found_word_or_non_word(
        self, c_idx, match_data, syls, tokens, has_decremented=False
    ):
        # there is a match
        if c_idx in match_data.keys():
            data = match_data[c_idx]
            ttype = (
                w.OOV.name
                if "senses" not in data
                or len([True for m in data["senses"] if "pos" in m]) <= 0
                else None
            )
            tokens.append(self.chunks_to_token(syls, data, ttype=ttype))
        elif any(match_data.values()):
            non_max_idx = sorted(match_data.keys())[-1]
            non_max_syls = []
            for syl in syls:
                if syl <= non_max_idx:
                    non_max_syls.append(syl)
            data = match_data[non_max_idx]
            ttype = (
                w.OOV.name
                if "senses" not in data
                or len([True for m in data["senses"] if "pos" in m]) <= 0
                else None
            )
            tokens.append(self.chunks_to_token(non_max_syls, data, ttype=ttype))
            c_idx = non_max_idx
        else:
            # add first syl in syls as non-word
            tokens.append(self.chunks_to_token([syls[0]], {}, ttype=w.OOV.name))

            # decrement chunk-idx for a new attempt to find a match
            if syls:
                c_idx -= len(syls[1:]) - 1
            if (
                has_decremented
                or (
                    c_idx < len(self.pre_processed.chunks)
                    and self.pre_processed.chunks[c_idx][0] is None
                )
                or len(syls) > 1
            ):
                c_idx -= 1
        return c_idx

    def chunks_to_token(self, syls, data, ttype=None):
        if len(syls) == 1:
            # chunk format: ([char_idx1, char_idx2, ...], (type, start_idx, len_idx))
            token_syls = [self.pre_processed.chunks[syls[0]][0]]
            token_type = self.pre_processed.chunks[syls[0]][1][0]
            token_start = self.pre_processed.chunks[syls[0]][1][1]
            token_length = self.pre_processed.chunks[syls[0]][1][2]
            syl_start_end = [
                (
                    self.pre_processed.chunks[syls[0]][1][1],
                    self.pre_processed.chunks[syls[0]][1][2],
                )
            ]
            if ttype:
                if "senses" not in data:
                    data["senses"] = [{"pos": ttype}]
                else:
                    for m in data["senses"]:
                        if "pos" not in m:
                            m["pos"] = ttype

            return self.create_token(
                token_type, token_start, token_length, token_syls, syl_start_end, data
            )
        elif len(syls) > 1:
            token_syls = [self.pre_processed.chunks[idx][0] for idx in syls]
            token_type = self.pre_processed.chunks[syls[-1]][1][0]
            token_start = self.pre_processed.chunks[syls[0]][1][1]
            token_length = 0
            syl_start_end = []
            for i in syls:
                token_length += self.pre_processed.chunks[i][1][2]
                syl_start_end.append(
                    (
                        self.pre_processed.chunks[i][1][1],
                        self.pre_processed.chunks[i][1][2],
                    )
                )
            if ttype:
                if "senses" not in data:
                    data["senses"] = [{"pos": ttype}]
                else:
                    for m in data["senses"]:
                        if "pos" not in m:
                            m["pos"] = ttype

            return self.create_token(
                token_type, token_start, token_length, token_syls, syl_start_end, data
            )
        else:
            raise ValueError(str(syls) + "should contain at least 1 token")

    def create_token(self, ttype, start, length, syls, syl_start_end, data):
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
        token.text = self.pre_processed.bs.string[start : start + length]
        token.chunk_type = u[ttype]
        token.start = start
        token.len = length
        if syls != [None]:
            token.syls_idx = [[s - start for s in syl] for syl in syls]
            token.syls_start_end = [
                {"start": s - start, "end": s - start + l} for s, l in syl_start_end
            ]
        char_groups = self.pre_processed.bs.export_groups(
            start, length, for_substring=True
        )
        token.char_types = [a[char_groups[idx]] for idx in sorted(char_groups.keys())]
        for k, v in data.items():
            token[k] = v
        token.skrt = (
            self.is_sanskrit(char_groups, token.text) if not token.skrt else token.skrt
        )
        return token

    def is_sanskrit(self, char_groups, word):
        return self._has_skrt_char(char_groups) or has_skrt_syl(word)

    def _has_skrt_char(self, char_groups):
        return (
            A.SKRT_VOW in char_groups.values()
            or A.SKRT_CONS in char_groups.values()
            or A.SKRT_SUB_CONS in char_groups.values()
        )

    @staticmethod
    def debug(debug, to_print):
        if debug:
            print(to_print, flush=True)
