from BoSylUtils import BoSyl
import time

# inspired from https://gist.github.com/nickstanisha/733c134a0171a00f66d4
# and https://github.com/eroux/tibetan-phonetics-py


class Node:
    def __init__(self, label=None, leaf=False, data=None):
        self.label = label
        self.leaf = leaf
        self.data = data
        self.children = dict()

    def add_child(self, key, leaf=False):
        if not isinstance(key, Node):
            self.children[key] = Node(key, leaf)
        else:
            self.children[key.leaf] = key

    def __getitem__(self, key):
        return self.children[key]


class Trie:
    def __init__(self):
        self.head = Node()

    def __getitem__(self, key):
        return self.head.children[key]

    def add(self, word, data=None):
        current_node = self.head
        word_finished = True

        i = 0
        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_finished = False
                break

        if not word_finished:
            while i < len(word):
                current_node.add_child(word[i])
                current_node = current_node.children[word[i]]
                i += 1

        current_node.leaf = True
        if data:
            current_node.data = data

    def walk(self, char, current_node=None):
        if not current_node:
            current_node = self.head

        if char in current_node.children:
            next_node = current_node[char]
        else:
            next_node = None

        return next_node

    def has_word(self, word):
        if word == '':
            return False
        elif not word:
            raise ValueError('Trie.has_word requires a not-Null string')

        # Start at the top
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break

        # Still need to check if we just reached a word like 't'
        # that isn't actually a full word in our dictionary
        if exists:
            if not current_node.leaf:
                exists = False
        if exists:
            return {'exists': exists, 'data': current_node.data}
        else:
            return {'exists': exists}


class PyBoTrie(Trie):
    def __init__(self, profile='pytib'):
        Trie.__init__(self)
        self.bt = BoSyl()
        self.build_trie(profile)

    def build_trie(self, profile):
        """
        TODO: choose which file to add,
        :param profile:
        :return:
        """
        files = {1: 'ancient.txt',
                 2: 'exceptions.txt',
                 3: 'uncompound_lexicon.txt',
                 4: 'Tibetan.DICT',
                 5: 'tsikchen.txt',
                 6: 'oral_corpus_0.txt',
                 7: 'oral_corpus_1.txt',
                 8: 'oral_corpus_2.txt',
                 9: 'oral_corpus_3.txt',
                 10: 'recordings_4.txt'}
        profiles = {
                    'pytib': [files[1], files[2], files[3], files[5], 'particles.txt'],
                    'POS': [files[1], files[2], files[3], files[5], 'particles.txt', files[4]]
                    }

        print('Building the Trie...')
        start = time.time()
        for f in profiles[profile]:
            full_path = '{}/{}/{}'.format('resources', 'trie', f)
            self.__add_one_file(full_path)
        end = time.time()
        print('Time:', end-start)

    def __add_one_file(self, folder):
        def find_sep(l):
            s = None
            if ',' in l:
                s = ','
            if '\t' in l:
                s = '\t'
            return s

        def clean(l):
            if '#' in l:
                start = l.index('#')
                if start:
                    return l[:start].strip()
            else:
                return l.strip()

        with open(folder, 'r') as g:
            content = g.read().split('\n')
            content = [c for c in content if not c.startswith('#')]

            sep = find_sep(content[0])
            for line in content:
                line = clean(line)
                if line:
                    if sep:
                        word, pos = line.split(sep)
                    else:
                        word, pos = line, 'XXX'

                    if not word.endswith('་'):
                        word += '་'
                    self.add(word, pos)
                    self.add_affixed(word[:-1], pos)

    def add_affixed(self, word, pos):
        """
        Add to the trie all the affixed versions of the word
        :param word: a word without ending tsek
        :param pos: initial POS
        """
        beginning, last_syl = self.split_at_last_syl(word)

        if self.bt.is_affixable(last_syl):
            affixed = self.bt.get_all_affixed(last_syl)
            for a in affixed:
                data = '{}_{}_{}_{}'.format(pos, a[1]['POS'], a[1]['len'], a[1]['aa'])
                self.add(beginning+a[0]+'་', data)

    @staticmethod
    def split_at_last_syl(word):
        if word.count('་') >= 1:
            tsek_idx = word.rindex('་')
            return word[:tsek_idx+1], word[tsek_idx+1:]
        else:
            return '', word


if __name__ == '__main__':
    """ Example use """
    bt = PyBoTrie('POS')
    print('གྲུབ་མཐའ་', bt.has_word('གྲུབ་མཐའ་'))
    print('གྲུབ་མཐའི་', bt.has_word('གྲུབ་མཐའི་'))
    print('ཟས་', bt.has_word('ཟས་'))

    trie = Trie()
    words = 'hello goo good goodbye help gerald gold tea ted team to too tom stan standard money'
    for w in words.split():
        trie.add(w)
    print("'goodbye':", trie.has_word('goodbye'))
