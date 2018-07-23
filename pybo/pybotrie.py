# coding: utf-8
import time
import os
import pickle
from .basictrie import BasicTrie, Node
from .helpers import open_file, AFFIX_SEP, OOV


class PyBoTrie(BasicTrie):
    def __init__(self, bosyl, profile='pytib', build=False, user_word_list=[]):
        BasicTrie.__init__(self)
        self.bosyl = bosyl
        self.TSEK = '་'
        self.COMMENT = '#'
        self.profile = profile
        self.pickled_file = profile + '_trie.pickled'
        self.user_word_list = user_word_list
        self.load_or_build_trie(build)

    def load_or_build_trie(self, build):
        if build or not os.path.exists(self.pickled_file):
            self.build_trie()
        else:
            self.load_trie()

    def load_trie(self):
        print('Loading Trie...')
        start = time.time()
        with open(self.pickled_file, 'rb') as f:
            self.head = pickle.load(f)
        end = time.time()
        print('Time:', end - start)

    def rebuild_trie(self):
        self.head = Node()
        self.build_trie()

    def build_trie(self):
        """
        """
        print('building Trie...', end=' ')
        start = time.time()
        files = {1: 'ancient.txt',
                 2: 'exceptions.txt',
                 3: 'uncompound_lexicon.txt',
                 5: 'tsikchen.txt',
                 6: 'oral_corpus_0.txt',
                 7: 'oral_corpus_1.txt',
                 8: 'oral_corpus_2.txt',
                 9: 'oral_corpus_3.txt',
                 10: 'recordings_4.txt',
                 11: 'mgd.txt',
                 12: 'verbs.txt'}
        tests = {1: 'test.txt'}
        freq = {1: 'mgd_freq.txt'}
        profiles = {
                    'pytib': [files[1], files[2], files[3], files[5], 'particles.txt'],
                    'POS': [files[1], files[2], files[3], files[5], 'particles.txt'],
                    'MGD': [files[1], files[2], files[3], files[5], files[11], files[12], 'particles.txt'],
                    'empty': [],
                    'test': [tests[1]]
                    }

        if self.profile == 'test':
            for f in profiles[self.profile]:
                full_path = os.path.join(os.path.split(__file__)[0], '..', 'tests', 'resources', f)
                self.__add_one_file(full_path)
            return

        for f in profiles[self.profile]:
            full_path = os.path.join(os.path.split(__file__)[0], 'resources', 'trie', f)
            self.__add_one_file(full_path)

        for f in self.user_word_list:
            self.__add_one_file(f)

        if self.profile == 'POS':
            full_path_pos = os.path.join(os.path.split(__file__)[0], 'resources', 'trie', "Tibetan.DICT")
            full_path_freq = os.path.join(os.path.split(__file__)[0], 'resources', 'frequency', "mgd.txt")
            full_path_skrt = os.path.join(os.path.split(__file__)[0], 'resources', 'sanskrit', "sanskrit.txt")
            self.__add_one_file(full_path_pos, data_only=True)
            self.__add_one_file(full_path_freq, ins="freq", data_only=True)
            self.__add_sanskrit_to_trie(full_path_skrt)

        if self.profile == 'MGD':
            full_path_dict = os.path.join(os.path.split(__file__)[0], 'resources', 'trie', "Tibetan.DICT")
            full_path_freq = os.path.join(os.path.split(__file__)[0], 'resources', 'frequency', "mgd.txt")
            full_path_skrt = os.path.join(os.path.split(__file__)[0], 'resources', 'sanskrit', "sanskrit.txt")
            self.__add_one_file(full_path_dict, data_only=True)
            self.__add_one_file(full_path_freq, ins="freq", data_only=True)
            self.__add_sanskrit_to_trie(full_path_skrt)

        with open(self.pickled_file, 'wb') as f:
            pickle.dump(self.head, f, pickle.HIGHEST_PROTOCOL)
        end = time.time()
        print('Time:', end - start)

    def __add_sanskrit_to_trie(self, in_file):
        for line in open_file(in_file).split('\n'):
            if line:
                word = line

            sep = "" if word[-1] == "ཿ" else "་"
            self.add(word+sep, skrt=True)

    def __add_one_file(self, in_file, ins="data", data_only=False):
        """
        files can have comments starting with #
        spaces and empty lines are trimmed
        a single space(breaks if more than one), a comma or a tab can be used as separators

        :param in_file: file to be processed
        :param data_only:
        """
        for line in open_file(in_file).split('\n'):
            if self.COMMENT in line:
                comment_idx = line.index(self.COMMENT)
                line = line[:comment_idx]

            line = line.strip()

            if line:
                if '\t' in line:
                    word, pos = line.split('\t')
                elif ',' in line:
                    word, pos = line.split(',')
                elif ' ' in line:
                    if line.count(' ') > 1:
                        break
                    word, pos = line.split(' ')
                else:
                    word, pos = line, OOV

                remove_word = False
                if word[0] == '-':
                    word = word[1:]
                    remove_word = True

                self.inflect_n_add(word, pos, ins, data_only, remove_word)

    def inflect_n_add(self, word, pos, ins, data_only=False, remove_word=False):
        """
        Add to the trie all the affixed versions of the word
        :param word: a word without ending tsek
        :param pos: initial POS
        """
        if word.endswith(self.TSEK):
            word = word[:-1]

        beginning, last_syl = self.split_at_last_syl(word)

        if self.bosyl.is_affixable(last_syl):
            affixed = self.bosyl.get_all_affixed(last_syl)
            for a in affixed:
                if ins == "data":
                    data = '{}{}{}{}{}{}{}'.format(pos, AFFIX_SEP,
                                                    a[1]['POS'], AFFIX_SEP,
                                                    a[1]['len'], AFFIX_SEP,
                                                    a[1]['aa'])
                else:
                    data = pos
                self.modify_tree(beginning+a[0]+self.TSEK, data, ins, data_only, remove_word)

        data = '{}{}{}{}'.format(pos, AFFIX_SEP, AFFIX_SEP, AFFIX_SEP) if ins == "data" else pos
        self.modify_tree(word + self.TSEK, data, ins, data_only, remove_word)

    def modify_tree(self, word, data, ins="data", data_only=False, remove_word=False):
        if remove_word and data_only:
            self.add_data_to_word(word, None, ins)
        elif remove_word:
            self.remove_word(word)
        elif not data_only:
            self.add(word, data)
        else:
            self.add_data_to_word(word, data, ins, data_only)

    def split_at_last_syl(self, word):
        if word.count(self.TSEK) >= 1:
            tsek_idx = word.rindex(self.TSEK)
            return word[:tsek_idx+1], word[tsek_idx+1:]
        else:
            return '', word
