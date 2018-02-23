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
        out = '\ncontent: "'+self.content+'"'
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

        current_node = None
        went_to_max = False
        match_idx = -1

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
                            if current_node and current_node.is_match:
                                match_idx = c_idx

                        # walking resumed after previous syllable
                        else:
                            current_node = self.trie.walk(syl[s_idx], current_node)
                            if current_node and current_node.is_match:
                                match_idx = c_idx
                        s_idx += 1

                    # continuing to walk
                    elif current_node and current_node.can_walk:
                        self.debug(debug, syl[s_idx])
                        current_node = self.trie.walk(syl[s_idx], current_node)
                        if current_node and current_node.is_match:
                            match_idx = c_idx
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

                # Finished looping over current syl.
                if is_non_word:
                    # non-word syls are turned into independant tokens
                    non_word = syl
                    tokens.append(non_word)

                else:

                    if went_to_max:
                        if not has_decremented:
                            c_idx -= 1

                        else:
                            c_idx = self.there_are_syls_process(c_idx, match_idx, syls, tokens)
                            syls = []
                        went_to_max = False

                    else:
                        syls.append(syl)

            # 2. CHUNK IS NON-SYLLABLE
            else:
                # if there is a word that was not added
                if syls:
                    c_idx = self.there_are_syls_process(c_idx, match_idx, syls, tokens)
                    syls = []
                    current_node = None

                token = [[self.pre_processed.string[idx] for idx in range(chunk[1][1], chunk[1][1]+chunk[1][2])]]
                tokens.append(token)

            c_idx += 1

        # a potential token was left
        if syls:
            self.there_are_syls_process(c_idx, match_idx, syls, tokens)

        return tokens

    @staticmethod
    def there_are_syls_process(c_idx, match_idx, syls, tokens):
        # there is a match
        if match_idx == c_idx:
            word = syls
            tokens.append(word)
        else:
            # add first syl in syls as non-word
            tokens.append(syls[0])
            del syls[0]

            # decrement chunk-idx for a new attempt to find a match
            if syls:
                c_idx -= len(syls) - 1
        return c_idx

    def create_token(self, ttype, start, length, syls, pos=None):
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
        print(''.join([''.join(a) for a in w]), end=' ')
