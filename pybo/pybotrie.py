# coding: utf-8
import time
import pickle
from pathlib import Path
from .basictrie import BasicTrie, Node
from .helpers import AFFIX_SEP, OOV


class PyBoTrie(BasicTrie):
    def __init__(self, bosyl, profile='pytib', build=False, toadd_filenames=[], todel_filenames=[], config=None):
        BasicTrie.__init__(self)
        self.bosyl = bosyl
        self.TSEK = '་'
        self.COMMENT = '#'
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

        # load the custom entries on the fly (at each instanciation)
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

        for f in self.config_trie.get_profile(self.profile):
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
            full_path = Path(__file__).parent / 'resources' / resource_directory / f
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

                sep = "" if word[-1] == "ཿ" else "་"
                self.add(word + sep, skrt=True)
        else:
            with in_file.open('r', encoding='utf-8-sig') as f:
                lines = [line.rstrip('\n') for line in f.readlines()]

            for line in lines:
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

                    word = word.rstrip('།')  # strip any ending shad

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
            self.deactivate_inflected(word)
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

    def deactivate_inflected(self, word):
        self.deactivate_word(word)

        if word.endswith(self.TSEK):
            word = word[:-1]

        beginning, last_syl = self.split_at_last_syl(word)

        if self.bosyl.is_affixable(last_syl):
            affixed = self.bosyl.get_all_affixed(last_syl)
            for a in affixed:
                affixed_word = beginning + a[0] + self.TSEK
                self.deactivate_word(affixed_word)

    def deactivate_wordlist(self, f):
        """

        :param f: filename of wordlist
        """
        with Path(f).open('r', encoding='utf-8-sig') as f:
            words = [line.rstrip('\n') for line in f.readlines()]

        # cleanup the entries
        # TODO: also remove non-breaking tseks. maybe centralize in a method such cleanup
        words = [word.rstrip('།') for word in words]
        words = [word + self.TSEK if not word.endswith(self.TSEK) else word for word in words]

        for word in words:
            self.deactivate_inflected(word)
