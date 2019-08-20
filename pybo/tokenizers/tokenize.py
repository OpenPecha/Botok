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
        match_data = (
            {}
        )  # keys: c_idx, values: trie data (for last and second-last matches)

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
                syl = [self.pre_processed.bs.string[c] for c in chunk[0]]  # get letters
                syl = syl + [TSEK] if syl[-1] != NAMCHE else syl  # add tsek
                self.debug(debug, syl)

                # >>> WALKING THE TRIE >>>
                s_idx = 0
                while s_idx <= len(syl) - 1:
                    # beginning of current syllable
                    if s_idx == 0:
                        self.debug(debug, syl[s_idx])
                        current_node = self.trie.walk(syl[s_idx], current_node)
                        if current_node and current_node.is_match():
                            match_data[c_idx] = current_node.data

                    # continuing to walk
                    elif current_node and current_node.can_walk():
                        self.debug(debug, syl[s_idx])
                        current_node = self.trie.walk(syl[s_idx], current_node)
                        if current_node and current_node.is_match():
                            match_data[c_idx] = current_node.data
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
                                has_decremented = (
                                    True
                                )  # ensures we only decrement once per syl
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
                    tokens.append(
                        self.chunks_to_token(non_word, {}, ttype=w.NON_WORD.name)
                    )
                    match_data = {}
                    syls = []

                else:
                    if went_to_max:
                        if not has_decremented:
                            c_idx -= 1
                        else:
                            c_idx = self.add_found_word_or_non_word(
                                c_idx, match_data, syls, tokens, has_decremented
                            )
                            match_data = {}
                            syls = []
                        went_to_max = False

                    else:
                        syls.append(c_idx)
                        # end of input and the end of syllable is reached
                        if c_idx == len(self.pre_processed.chunks) - 1 and s_idx == len(
                            syl
                        ):
                            c_idx = self.add_found_word_or_non_word(
                                c_idx, match_data, syls, tokens, has_decremented
                            )
                            match_data = {}
                            syls = []
                            s_idx += 1

            # 2. CHUNK IS NON-SYLLABLE
            else:
                # if there is a word that was not added
                if syls:
                    # the word to add ends at c_idx - 1 since we reached the non-syllable chunk
                    c_idx = (
                        self.add_found_word_or_non_word(
                            c_idx - 1, match_data, syls, tokens
                        )
                        + 1
                    )
                    match_data = {}
                    syls = []
                    current_node = None
                    continue

                tokens.append(self.chunks_to_token([c_idx], {}))

            # END OF INPUT
            # if we reached end of input and there is a non-max-match
            if len(self.pre_processed.chunks) - 1 == c_idx:
                if any(match_data.values()) and current_node and not current_node.leaf:
                    c_idx = self.add_found_word_or_non_word(
                        c_idx, match_data[c_idx], syls, tokens
                    )
                    syls = []
                    current_node = None
                if has_decremented:
                    c_idx -= 1

            c_idx += 1

        # a potential token was left
        if syls:
            self.add_found_word_or_non_word(c_idx, match_data[c_idx], syls, tokens)

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
                if "entries" not in data
                or len([True for m in data["entries"] if "pos" in m]) <= 0
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
                if "entries" not in data
                or len([True for m in data["entries"] if "pos" in m]) <= 0
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
            if ttype:
                if "entries" not in data:
                    data["entries"] = [{"pos": ttype}]
                else:
                    for m in data["entries"]:
                        if "pos" not in m:
                            m["pos"] = ttype

            return self.create_token(
                token_type, token_start, token_length, token_syls, data
            )
        elif len(syls) > 1:
            token_syls = [self.pre_processed.chunks[idx][0] for idx in syls]
            token_type = self.pre_processed.chunks[syls[-1]][1][0]
            token_start = self.pre_processed.chunks[syls[0]][1][1]
            token_length = 0
            for i in syls:
                token_length += self.pre_processed.chunks[i][1][2]
            if ttype:
                if "entries" not in data:
                    data["entries"] = [{"pos": ttype}]
                else:
                    for m in data["entries"]:
                        if "pos" not in m:
                            m["pos"] = ttype

            return self.create_token(
                token_type, token_start, token_length, token_syls, data
            )
        else:
            raise ValueError(str(syls) + "should contain at least 1 token")

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
        token.text = self.pre_processed.bs.string[start : start + length]
        token.chunk_type = u[ttype]
        token.start = start
        token.len = length
        if syls != [None]:
            token.syls_idx = [[s - start for s in syl] for syl in syls]
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
