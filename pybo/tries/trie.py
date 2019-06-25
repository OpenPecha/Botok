# coding: utf-8
import time
import pickle
from pathlib import Path

from .basictrie import BasicTrie, Node
from ..chunks.chunks import TokChunks
from ..vars import OOV, TSEK, NAMCHE, HASH


class Trie(BasicTrie):
    def __init__(self, bosyl, profile, main_data, custom_data, build=False):
        BasicTrie.__init__(self)
        self.bosyl = bosyl()
        self.main_data = main_data
        self.custom_data = custom_data
        self.pickled_file = Path(profile + '_trie.pickled')
        self.tmp_inflected = dict()  # tmp to inflect only once, even if a word appears in many files.
        self.load_or_build_trie(build)

    def rebuild_trie(self):
        self.head = Node()
        self.load_or_build_trie(build=True)

    def load_or_build_trie(self, build=False):
        if build or not self.pickled_file.exists():
            self._build_trie()
        else:
            self._load_trie()

        # add and deactivate the custom entries in memory (will not be written)
        self._populate_trie(self.custom_data)
        self.tmp_inflected = dict()

    def _load_trie(self):
        print('Loading Trie...', end=' ')
        start = time.time()
        with self.pickled_file.open('rb') as f:
            self.head = pickle.load(f)
        end = time.time()
        print('({:.0f}s.)'.format(end - start))

    def _build_trie(self):
        """
        """
        print('Building Trie...', end=' ')
        start = time.time()
        self._populate_trie(self.main_data)

        with self.pickled_file.open('wb') as f:
            pickle.dump(self.head, f, pickle.HIGHEST_PROTOCOL)
        end = time.time()
        print('({:.0f} s.)'.format(end - start))

    def _populate_trie(self, files):
        # first populate the trie with words
        lexica = (d for d in files if d.startswith('lexica'))
        for l in lexica:
            for f in files[l]:
                self._add_one_file(f, l)

        # then add data to the added words
        rest = (d for d in files if not d.startswith('lexica'))
        for r in rest:
            for f in files[r]:
                self._add_one_file(f, r)

    def _add_one_file(self, in_file, category):
        """
        files can have comments starting with #
        spaces and empty lines are trimmed
        a single space(breaks if more than one), a comma or a tab can be used as separators
        """
        with in_file.open('r', encoding='utf-8-sig') as f:
            lines = self.__clean_lines(f)
            for l in lines:
                if category == 'lexica_bo':
                    self.inflect_n_modify_trie(l)

                elif category == 'lexica_skrt':
                    self.inflect_n_modify_trie(l, skrt=True)

                elif category == 'deactivate':
                    self.inflect_n_modify_trie(l, deactivate=True)

                elif category == 'lemmas':
                    self.inflect_n_add_data(l, 'lemma')

                elif category == 'pos':
                    self.inflect_n_add_data(l, 'pos')

                elif category == 'frequencies':
                    self.inflect_n_add_data(l, 'freq')

                else:
                    raise SyntaxError('category is one of: lexica_bo, lexica_skrt, '
                                      'pos, lemmas, frequencies, deactivate')

    def inflect_n_modify_trie(self, word, deactivate=False, skrt=False):
        """
        Add or deactivate to the trie all the affixed versions of the word
        :param word: a word without ending tsek
        :param deactivate: switch to add or deactivate a word
        """
        inflected = self._get_inflected(word)
        if not inflected:
            return

        for infl, data in inflected:
            if deactivate:
                self.deactivate(infl)
            else:
                if skrt:
                    if data is None:
                        data = {'skrt': True}
                    else:
                        data.update({'skrt': True})
                    self.add(infl, data=data)
                else:
                    self.add(infl, data=data)

    def inflect_n_add_data(self, line, info):
        word, data = self.__parse_line(line)
        data = data.strip()
        if info == 'freq':
            data = int(data)
        inflected = self._get_inflected(word)
        if not inflected:
            return

        for infl, _ in inflected:
            self.add_data(infl, {info: data})

    def _get_inflected(self, word):
        """
        gets the clean syls using TokChunks(), then inflects the last syl using BoSyl.get_all_affixed()

        :return: list of (<inflected word>, <affixation data>)
        """
        if word in self.tmp_inflected:
            return self.tmp_inflected[word]

        syls = TokChunks(word).get_syls()
        if not syls:
            return None

        inflected = [(self.__join_syls(syls), None)]
        affixed = self.bosyl.get_all_affixed(syls[-1])
        if affixed:
            for infl, data in affixed:
                infl_word = self.__join_syls(syls[:-1] + [infl])
                inflected.append((infl_word, {'affixation': data}))

        self.tmp_inflected[word] = inflected
        return inflected

    @staticmethod
    def __join_syls(syls):
        return ''.join([syl if syl.endswith(NAMCHE) else syl + TSEK for syl in syls])

    @staticmethod
    def __clean_lines(f):
        # cuts off comments, then strips empty lines
        lines = (
            line[:line.index(HASH)] if HASH in line else line
            for line in f.readlines()
        )
        return (l for l in lines if l)

    @staticmethod
    def __parse_line(line):
        """
        enables support of '\t', ',', '-' and ' ' as separator.
        """
        if '\t' in line:
            assert line.count('\t') == 1
            word, pos = line.split('\t')
        elif ',' in line:
            assert line.count(',') == 1
            word, pos = line.split(',')
        elif '-' in line:
            assert line.count('-') == 1
            word, pos = line.split('-')
        elif ' ' in line:
            assert line.count(' ') == 1
            word, pos = line.split(' ')
        else:
            word, pos = line, OOV
        return word, pos
