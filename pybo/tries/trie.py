# coding: utf-8
import time
import pickle
from pathlib import Path

from .basictrie import BasicTrie, Node
from ..vars import AFFIX_SEP, OOV, TSEK, NAMCHE, SHAD, HASH


class Trie(BasicTrie):
    def __init__(self, bosyl, profile='pytib', build=False, toadd_filenames=None, todel_filenames=None, config=None):
        BasicTrie.__init__(self)
        if toadd_filenames is None:
            toadd_filenames = []
        if todel_filenames is None:
            todel_filenames = []
        self.bosyl = bosyl()
        self.profile = profile
        self.pickled_file = Path(profile + '_trie.pickled')
        self.toadd_filenames = toadd_filenames
        self.todel_filenames = todel_filenames
        self.config_trie = config
        self.load_or_build_trie(build)

    def load_or_build_trie(self, build):
        if build or not Path(self.pickled_file).exists():
            self.build_trie()
        else:
            self.load_trie()

        # add and deactivate the custom entries on the fly, at each instanciation
        for f in self.toadd_filenames:
            self.__add_one_file(Path(f))
        for f in self.todel_filenames:
            self.deactivate_wordlist(f)

    def load_trie(self):
        print('Loading Trie...', end=' ')
        start = time.time()
        with self.pickled_file.open('rb') as f:
            self.head = pickle.load(f)
        end = time.time()
        print('({:.0f}s.)'.format(end - start))

    def rebuild_trie(self):
        self.head = Node()
        self.build_trie()

    def build_trie(self):
        """
        """
        print('Building Trie...', end=' ')
        start = time.time()

        for f in self.config_trie.get_tokenizer_profile(self.profile):
            print()

            ins_s = "data"
            data_s = False
            resource_directory = 'trie'
            if f.startswith("~"):
                if f[1] == "p":
                    data_s = True
                if f[1] == "f":
                    resource_directory = 'frequency'
                    ins_s = "freq"
                    data_s = True
                elif f[1] == "s":
                    resource_directory = 'sanskrit'
                    ins_s = "skrt"
                f = f[2:]
            full_path = Path(__file__).parent.parent / 'resources' / resource_directory / f
            self.__add_one_file(full_path, ins=ins_s, data_only=data_s)

        with self.pickled_file.open('wb') as f:
            pickle.dump(self.head, f, pickle.HIGHEST_PROTOCOL)
        end = time.time()
        print('({:.0f} s.)'.format(end - start))

    def __add_one_file(self, in_file, ins="data", data_only=False):
        """
        files can have comments starting with #
        spaces and empty lines are trimmed
        a single space(breaks if more than one), a comma or a tab can be used as separators

        :param in_file: file to be processed
        :type in_file: Path object
        :param data_only:
        """
        if ins == "skrt":
            with in_file.open('r', encoding='utf-8-sig') as f:
                lines = [line.rstrip('\n') for line in f.readlines()]

            for line in lines:
                if line:
                    word = line

                sep = "" if word[-1] == NAMCHE else TSEK
                self.add(word + sep)
        else:
            with in_file.open('r', encoding='utf-8-sig') as f:
                lines = [line.rstrip('\n') for line in f.readlines()]

            for line in lines:
                if HASH in line:
                    comment_idx = line.index(HASH)
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

                    deactivate = False
                    if word[0] == '-':
                        word = word[1:]
                        deactivate = True

                    word = word.rstrip(SHAD)  # strip any ending shad

                    self.inflect_n_add(word, pos, ins, data_only, deactivate)

    def inflect_n_add(self, word, data, deactivate=False, overwrite=True):
        """
        Add to the trie all the affixed versions of the word
        :param word: a word without ending tsek
        :param pos: initial POS
        """
        # add/deactivate word as is
        self.modify_tree(word, data, deactivate=deactivate, overwrite=overwrite)

        # add/deactivate inflected forms
        if word.endswith(TSEK):
            word = word[:-1]
        beginning, last_syl = self.split_at_last_syl(word)

        if self.bosyl.is_affixable(last_syl):
            affixed = self.bosyl.get_all_affixed(last_syl)
            for a in affixed:
                a[1].update(data)  # adds affix, len and aa
                inflected_word = beginning + a[0] + TSEK
                self.modify_tree(inflected_word, a[1], deactivate=deactivate, overwrite=overwrite)

    def modify_tree(self, word, data, deactivate=False, overwrite=True):
        if not deactivate:
            self.add_data_to_word(word, data, overwrite=overwrite)
        else:
            self.deactivate_word(word)

    def split_at_last_syl(self, word):
        if word.count(TSEK) >= 1:
            tsek_idx = word.rindex(TSEK)
            return word[:tsek_idx+1], word[tsek_idx+1:]
        else:
            return '', word

    def deactivate_inflected(self, word):
        self.deactivate_word(word)

        if word.endswith(TSEK):
            word = word[:-1]

        beginning, last_syl = self.split_at_last_syl(word)

        if self.bosyl.is_affixable(last_syl):
            affixed = self.bosyl.get_all_affixed(last_syl)
            for a in affixed:
                affixed_word = beginning + a[0] + TSEK
                self.deactivate_word(affixed_word)

    def deactivate_wordlist(self, f):
        """

        :param f: filename of wordlist
        """
        with Path(f).open('r', encoding='utf-8-sig') as f:
            words = [line.rstrip('\n') for line in f.readlines()]

        # cleanup the entries
        # TODO: also remove non-breaking tseks. maybe centralize in a method such cleanup
        words = [word.rstrip(SHAD) for word in words]
        words = [word + TSEK if not word.endswith(TSEK) else word for word in words]

        for word in words:
            self.deactivate_inflected(word)
