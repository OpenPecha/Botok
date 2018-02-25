from BoStringUtils import PyBoTextChunks
from BoTrie import PyBoTrie


class Word:
    def __init__(self):
        self.content = None
        self.chunk_type = None
        self.char_groups = None
        self.start_in_input = 0
        self.length = None
        self.syls = None
        self.partOfSpeech = None
        self.tagIsOn = False
        self.level = 0
        self.char_markers = {1: 'cons', 2: 'sub-cons', 3: 'vow', 4: 'tsek', 5: 'skrt-cons', 6: 'skrt-sub-cons',
                             7: 'skrt-vow', 8: 'punct', 9: 'num', 10: 'in-syl-mark', 11: 'special-punct', 12: 'symbol',
                             13: 'no-bo-no-skrt', 14: 'other', 15: 'space', 16: 'underscore'}
        self.chunk_markers = {100: 'bo', 101: 'non-bo', 102: 'punct', 103: 'non-punct', 104: 'space', 105: 'non-space',
                              106: 'syl', 1000: 'word', 1001: 'non-word'}

    @property
    def to_string(self):
        out = 'content: "'+self.content+'"'
        out += '\nchar types: '
        out += '|'+'|'.join([self.char_markers[self.char_groups[idx]]
                            for idx in sorted(self.char_groups.keys())])+'|'
        out += '\ntype: ' + self.chunk_markers[self.chunk_type]
        out += '\nstart in input: ' + str(self.start_in_input)
        out += '\nlength: ' + str(self.length)
        out += '\nsyl chars in content'
        if self.syls:
            out += '(' + ' '.join([''.join([self.content[char] for char in syl]) for syl in self.syls]) + '): '
        else:
            out += ': '
        out += str(self.syls)
        out += '\nPOS: ' + self.partOfSpeech
        return out

    @property
    def cleaned_content(self):
        return ''

    @property
    def end(self):
        return self.start_in_input + len(self.content)

    @property
    def partOfSpeechEnd(self):
        return self.end + self.partOfSpeechLen

    @property
    def partOfSpeechLen(self):
        return len(self.partOfSpeech) + 1  # plus one for '/'


class Tokenizer:
    """
    Tokenizes Tibetan text.

    Leverages BoStringUtils as pre-processing, BoTrie as
    """
    def __init__(self, string):
        self.string = string  # another copy of string lives in pre_process
        self.pre_processed = PyBoTextChunks(string)
        self.trie = PyBoTrie('POS')
        self.WORD = 1000
        self.NON_WORD = 1001

    def tokenize(self, debug=False):
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

            c_idx += 1

        # a potential token was left
        if syls:
            self.add_found_word_or_non_word(c_idx, match_data, syls, tokens)

        return tokens

    def add_found_word_or_non_word(self, c_idx, match_data, syls, tokens):
        # there is a match
        if c_idx in match_data.keys():
            tokens.append(self.chunks_to_token(syls, pos=match_data[c_idx]))
        else:
            # add first syl in syls as non-word
            tokens.append(self.chunks_to_token([syls[0]], self.NON_WORD))

            # decrement chunk-idx for a new attempt to find a match
            if syls:
                c_idx -= len(syls[1:]) - 1
        return c_idx

    def chunks_to_token(self, syls, pos=None, ttype=None):
        if len(syls) == 1:
            # chunk format: ([char_idx1, char_idx2, ...], (type, start_idx, len_idx))
            token_syls  = [self.pre_processed.chunks[syls[0]][0]]
            token_type   = self.pre_processed.chunks[syls[0]][1][0]
            token_start  = self.pre_processed.chunks[syls[0]][1][1]
            token_length = self.pre_processed.chunks[syls[0]][1][2]
            if ttype:
                token_type = ttype

            return self.create_token(token_type, token_start, token_length, token_syls, pos)
        elif len(syls) > 1:
            token_syls = [self.pre_processed.chunks[idx][0] for idx in syls]
            token_type = self.pre_processed.chunks[syls[-1]][1][0]
            token_start = self.pre_processed.chunks[syls[0]][1][1]
            token_length = 0
            for i in syls:
                token_length += self.pre_processed.chunks[i][1][2]
            if ttype:
                token_type = ttype

            return self.create_token(token_type, token_start, token_length, token_syls, pos)
        else:
            return None  # should raise an error instead?

    def create_token(self, ttype, start, length, syls, pos=None):
        """

        :param ttype: token type
        :param start: start index in input string
        :param length: length of the substring from the input string corresponding to this token
        :param syls: syl representation coming from PyBoTextChunks.
                        the indices are modified to be usable on the substring corresponding to this token
        :param pos: the POS retrieved from the chunk or from the trie
        :return: a Word object with all the above information
        """
        token = Word()
        token.content = self.string[start:start+length]
        token.chunk_type = ttype
        token.start_in_input = start
        token.length = length
        if syls != [None]:
            token.syls = []
            for syl in syls:
                token.syls.append([i-start for i in syl])
        if not pos:
            token.partOfSpeech = token.chunk_markers[ttype]
        else:
            if type(pos) == int:
                token.partOfSpeech = token.chunk_markers[pos]
            else:
                token.partOfSpeech = pos
        token.char_groups = self.pre_processed.export_groups(start, length, for_substring=True)
        return token

    @staticmethod
    def debug(debug, to_print):
        if debug:
            print(to_print)


if __name__ == '__main__':
    """example use"""
    input_string = ' ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ'
    test = 'ཀཀ་ཀཀ་ཞེས་བྱ་བ། ངེད་རྣམས་ནི་མཐོ་གོ་གནས་དང་། འབྱོར་ལྡན། མིང་གྲགས་ཡོད་མཁན་དེ་འདྲ་ནམ་ཡང་མིན་ལ། ' \
           'ཅི་ཞིག་ཤེས་ཁུལ་གྱིས་ཚོགས་པ་འདི་གཉེར་བ་ཞིག་ཀྱང་གཏན་ནས་མིན། ཚན་རྩལ་གྱི་རྦ་རླབས་དྲག་ཏུ་འཕྱོ་ལྡིང་བྱེད་' \
           'པའི་དུས་སྐབས་འདིར་ང་ཚོས་སྔ་ས་ནས་རང་གི་སྐད་ཡིག་དང་རིག་གཞུང་ལ་དུང་བ་ཞིག་ན་གཞོན་ཚོར་བསྐྲུན་མ་ཐུབ་པ་དང་། ' \
           'བདག་གཅེས་ལ་འབད་མ་ནུས་ཚེ་ཡོད་ཚད་མིང་ཙམ་ཞིག་ཏུ་གྱུར་ཚར་རྗེས་ངལ་བ་ཇི་ཙམ་བརྟེན་ཡང་སྙིང་པོ་ལོན་རྒྱུ་དཀའ་བས་ད་' \
           'ལྟ་མ་སྔ་མ་ཕྱིས་བའི་དུས་ཚིགས་གལ་ཆེན་ཞིག་ཏུ་བརྩིས་ནས་ང་ཚོས་འདི་ལྟར་རང་ནུས་ལ་དཔགས་པའི་སྐད་ཡིག་རིག་གཞུང་དང་' \
           'འབྲེལ་བའི་བྱེད་སྒོ་སྤེལ་མུས་ཡིན།'

    tok = Tokenizer(test)
    words = tok.tokenize()
    for w in words:
        print(w.to_string)
        print()

    tagged = ['{}/{}'.format(w.content, w.partOfSpeech) for w in words]
    print(' '.join(tagged))
