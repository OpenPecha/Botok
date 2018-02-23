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

        # these variables are here so they can be updated
        # by add_non_word(), ...
        self.tokens = []

        self.word = []
        # self.word_start = -1
        # self.word_len = -1

        self.non_word = []
        # self.non_word_start = -1
        # self.non_word_len = -1

    def tokenize(self):
        tokens = []
        current_node = None
        went_to_max = False

        c_idx = 0
        while c_idx < len(self.pre_processed.chunks):
            has_decremented = False
            is_non_word = False
            chunk = self.pre_processed.chunks[c_idx]
            if chunk[0]:  # chunk is a syllable

                syl = [self.pre_processed.string[idx] for idx in chunk[0]] + ['་']
                print(''.join(syl))

                s_idx = 0
                while s_idx <= len(syl)-1:
                    if s_idx == 0:
                        char = syl[s_idx]
                        if not current_node:
                            current_node = self.trie.walk(syl[s_idx], self.trie.head)
                        else:
                            current_node = self.trie.walk(syl[s_idx], current_node)
                        s_idx += 1

                    elif current_node and current_node.can_continue():
                        char = syl[s_idx]
                        current_node = self.trie.walk(syl[s_idx], current_node)

                        if not current_node and self.word:
                            if not has_decremented:
                                c_idx -= 1
                                has_decremented = True
                            went_to_max = True
                        s_idx += 1

                    else:
                        # we couldn't go until the end of the syl
                        if self.word:
                            if went_to_max:
                                s_idx += 1
                                continue

                            if not has_decremented:
                                c_idx -= 1
                                has_decremented = True
                            went_to_max = True
                        else:
                            # there is only a non-word
                            is_non_word = True
                        s_idx += 1

                if is_non_word:
                    non_word = syl
                    tokens.append(non_word)

                else:
                    if went_to_max:
                        if self.word and not has_decremented:
                            c_idx -= 1

                        else:
                            tokens.append(self.word)
                            self.word = []
                        went_to_max = False

                    else:
                        self.word.append(syl)

                    # we have reached the end of the syl
                    if current_node and current_node.is_match():
                        # self.non_max_match = self.word

                        # restart non_word at current position
                        self.non_word = []

            else:
                # if there is a word that was not added
                if self.word:
                    tokens.append(self.word)
                    self.word = []
                    # self.non_max_match = []
                    current_node = None

                # is non-bo, add it to tokens as a Word
                token = [[self.pre_processed.string[idx] for idx in range(chunk[1][1], chunk[1][1]+chunk[1][2])]]
                tokens.append(token)
                # tokens.append(self.create_token(chunk[1][0], chunk[1][1], chunk[1][2], [chunk[0]]))

            c_idx += 1

        if self.word:
            tokens.append(self.word)

        self.reinitialize_vars()
        return tokens

    def create_token(self, type, start, length, syls, POS=None):
        token = Word()
        token.content = self.string[start:start+length]
        token.chunk_type = type
        token.start_in_input = start
        token.length = length
        if syls != [None]:
            token.syls = []
            for syl in syls:
                token.syls.append([i-start for i in syl])
        if not POS:
            token.partOfSpeech = token.chunk_markers[type]
        else:
            token.partOfSpeech = POS
        token.char_groups = self.pre_processed.export_groups(start, length, for_substring=True)
        return token

    def reinitialize_vars(self):
        self.tokens = []
        self.word = []
        # self.word_start = -1
        # self.word_len = -1
        self.non_word = []
        # self.non_word_start = -1
        # self.non_word_len = -1


if __name__ == '__main__':
    """example use"""
    input_string = ' ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ'
    test = 'ཀཀ་ཀཀ་ཞེས་བྱ་བ། ངེད་རྣམས་ནི་མཐོ་གོ་གནས་དང་། འབྱོར་ལྡན། མིང་གྲགས་ཡོད་མཁན་དེ་འདྲ་ནམ་ཡང་མིན་ལ། ཅི་ཞིག་ཤེས་ཁུལ་གྱིས་ཚོགས་པ་འདི་གཉེར་བ་ཞིག་ཀྱང་གཏན་ནས་མིན། ཚན་རྩལ་གྱི་རྦ་རླབས་དྲག་ཏུ་འཕྱོ་ལྡིང་བྱེད་པའི་དུས་སྐབས་འདིར་ང་ཚོས་སྔ་ས་ནས་རང་གི་སྐད་ཡིག་དང་རིག་གཞུང་ལ་དུང་བ་ཞིག་ན་གཞོན་ཚོར་བསྐྲུན་མ་ཐུབ་པ་དང་། བདག་གཅེས་ལ་འབད་མ་ནུས་ཚེ་ཡོད་ཚད་མིང་ཙམ་ཞིག་ཏུ་གྱུར་ཚར་རྗེས་ངལ་བ་ཇི་ཙམ་བརྟེན་ཡང་སྙིང་པོ་ལོན་རྒྱུ་དཀའ་བས་ད་ལྟ་མ་སྔ་མ་ཕྱིས་བའི་དུས་ཚིགས་གལ་ཆེན་ཞིག་ཏུ་བརྩིས་ནས་ང་ཚོས་འདི་ལྟར་རང་ནུས་ལ་དཔགས་པའི་སྐད་ཡིག་རིག་གཞུང་དང་འབྲེལ་བའི་བྱེད་སྒོ་སྤེལ་མུས་ཡིན།'

    tok = Tokenizer(test)
    words = tok.tokenize()
    for word in words:
        print(''.join([''.join(a) for a in word]), end=' ')

