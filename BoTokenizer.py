from BoStringUtils import PyBoTextIterator
from BoTrie import BoTrie

trie = BoTrie()
trie.add("བཀྲ་", "word1")
trie.add("བཀྲ་ཤིས་", "word2")
trie.add("བདེ་", "word3")
trie.add("ལེགས་", "word4")
trie.add("བདེ་ལེགས་", "word5")
trie.add("བཀྲ་ཤིས་བདེ་ལེགས་", "word6")


input_string = ' ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། '
pybo_string = PyBoTextIterator(input_string)
chunks = pybo_string.serve_syls_to_trie()

words = []
current_node = None
syls = []
word_start = -1
word_len = -1
leaf = None
longest_match = None

for chunk in chunks:
    if chunk[0]:  # chunk is a syllable
        if word_start == -1:
            word_start = chunk[1][1]
        syl = [pybo_string.string[idx] for idx in chunk[0]] + ['་']
        for i, char in enumerate(syl):
            if current_node:
                current_node = trie.walk(char, current_node)
            else:
                current_node = trie.walk(char, trie.head)

        if current_node:
            leaf = current_node.leaf
            syls.append(chunk[0])
            word_len += chunk[1][2]

        if leaf:
            longest_match = {'type': 'word', 'start_idx': word_start, 'len': word_len, 'syls': syls}
        else:
            if not current_node:
                if longest_match:
                    words.append(longest_match)
                syls = []
                word_start = -1
                word_len = -1
                words.append({'type': 'non-word', 'start_idx': chunk[1][1], 'len': chunk[1][2], 'syls': [chunk[0]]})

    else:
        # add found word
        if longest_match:
            words.append(longest_match)

        # add non-word chunk
        words.append({'type': pybo_string.markers[chunk[1][0]], 'start_idx': chunk[1][1], 'len': chunk[1][2]})
        syls = []
        word_start = -1
        word_len = -1

for word in words:
    print('type:', word['type'])
    print('start:', word['start_idx'])
    print('len:', word['len'])
    if 'syls' in word.keys():
        print('char indices:', str(word['syls']))
        for syl in word['syls']:
            print(''.join([input_string[i] for i in syl]), end=' ')
        print()
    print()