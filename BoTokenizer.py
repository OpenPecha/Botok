from BoStringUtils import PyBoTextIterator
from BoTrie import BoTrie
import csv
import os


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
        self.pre_process = PyBoTextIterator(string)
        trie_content = '{}/{}'.format('resources', 'trie')
        self.trie = self.__load_trie_from_csv(trie_content)
        self.WORD = 1000
        self.NON_WORD = 1001

    @staticmethod
    def __load_trie_from_csv(folder):
        trie = BoTrie()
        for f in os.listdir(folder):
            full_path = '{}/{}'.format(folder, f)
            with open(full_path, newline='') as csvfile:
                freader = csv.reader(csvfile)
                for row in freader:
                    trie.add(row[0], row[1])
        return trie

    def tokenize(self):
        tokens = []
        syls = []
        word_start = -1
        word_len = -1
        current_node = None
        longest_match = None

        for chunk in self.pre_process.chunks:
            if chunk[0]:  # chunk is a syllable
                if word_start == -1:
                    word_start = chunk[1][1]
                syl = [self.pre_process.string[idx] for idx in chunk[0]] + ['་']
                for i, char in enumerate(syl):
                    if current_node:
                        current_node = self.trie.walk(char, current_node)
                    else:
                        current_node = self.trie.walk(char, self.trie.head)

                if current_node:
                    leaf = current_node.leaf
                    syls.append(chunk[0])
                    word_len += chunk[1][2]

                    if leaf:
                        longest_match = self.create_token(self.WORD, word_start,
                                                          word_len + 1, syls, current_node.data)

                else:
                    if not current_node:
                        if longest_match:
                            tokens.append(longest_match)
                            longest_match = None
                        else:
                            tokens.append(self.create_token(self.NON_WORD, chunk[1][1],
                                                            chunk[1][2], [chunk[0]]))
                        syls = []
                        word_start = -1
                        word_len = -1

            else:
                # add found word
                if longest_match:
                    tokens.append(longest_match)
                    longest_match = None

                tokens.append(self.create_token(chunk[1][0], chunk[1][1], chunk[1][2], [chunk[0]]))
                syls = []
                word_start = -1
                word_len = -1
                current_node = None

        if longest_match:
            tokens.append(longest_match)

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
        token.char_groups = self.pre_process.export_groups(start, length, for_substring=True)
        return token


if __name__ == '__main__':
    """example use"""
    input_string = ' ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས'

    tok = Tokenizer(input_string)
    tokens = tok.tokenize()

    pos_tagged = ['{}/{}'.format(t.content.replace(' ', '_'), t.partOfSpeech) for t in tokens]
    print(' '.join(pos_tagged))
    # _ཤི་/non-word བཀྲ་ཤིས་__/NOUN tr/non-bo _བདེ་་ལེ_གས/NOUN །/punct _བཀྲ་ཤིས་བདེ་ལེགས/EXCLS

    for t in tokens:
        print(t.to_string)
    # content: " ཤི་"
    # char types: |space|cons|vow|tsek|
    # type: non-word
    # start in input: 0
    # length: 4
    # syl chars in content(ཤི): [[1, 2]]
    # POS: non - word
    #
    # content: "བཀྲ་ཤིས་  "
    # char types: |cons|cons|sub-cons|tsek|cons|vow|cons|tsek|space|space|
    # type: word
    # start in input: 4
    # length: 10
    # syl chars in content(བཀྲ ཤིས): [[0, 1, 2], [4, 5, 6]]
    # POS: NOUN
    #
    # (...)
