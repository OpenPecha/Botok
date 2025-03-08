# coding: utf-8
import csv
import pickle
import time
from pathlib import Path
import logging

from ..chunks.chunks import TokChunks
from ..vars import HASH, NAMCHE, NO_POS, TSEK, __version__
from .basictrie import BasicTrie, Node


class Trie(BasicTrie):
    def __init__(
        self, bosyl, profile, main_data, custom_data, build=False, pickle_path=None
    ):
        BasicTrie.__init__(self)
        self.bosyl = bosyl()
        self.main_data = main_data
        self.custom_data = custom_data
        self.pickled_file = Path(profile + "_trie.pickled")
        if pickle_path:
            self.pickled_file = Path(pickle_path) / self.pickled_file
        self.tmp_inflected = (
            dict()
        )  # tmp to inflect only once, even if a word appears in many files.
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
        with self.pickled_file.open("rb") as f:
            self.head = pickle.load(f)
            version = self.head.data["_"]["version"]
            if version != __version__:
                print(
                    f"\nThe trie was build for botok {version}. Current version: {__version__}"
                )
                self._build_trie()

    def _build_trie(self):
        """
        """
        logging.debug("Building Trie:")
        start = time.time()
        self.head.data["_"]["version"] = __version__  # add version in trie
        self._populate_trie(self.main_data)

        with self.pickled_file.open("wb") as f:
            pickle.dump(self.head, f, pickle.HIGHEST_PROTOCOL)
        end = time.time()
        logging.debug("({:.0f} s.)".format(end - start))

    def _populate_trie(self, files):
        # first populate the trie with words
        lexica = (d for d in files if d.startswith("lexica"))
        for l in lexica:
            for f in files[l]:
                self._add_one_file(f, l)

        # then add data to the added words
        rest = (
            d for d in files if not d.startswith("lexica") and not d.startswith("rules")
        )
        for r in rest:
            for f in files[r]:
                self._add_one_file(f, r)

    def _add_one_file(self, in_file, category):
        """
        files can have comments starting with #
        spaces and empty lines are trimmed
        a single space(breaks if more than one), a comma or a tab can be used as separators
        """
        logging.debug("\t" + str(in_file))
        with in_file.open("r", encoding="utf-8-sig") as f:
            lines = self.__clean_lines(f)
            for l in lines:
                word = l.split("\t", 1)[0]
                if category == "words":
                    self.inflect_n_modify_trie(word)
                    self.inflect_n_add_data(l)

                elif category == "words_non_inflected":
                    self.add_non_inflectible(word)
                    self.inflect_n_add_data(l)

                elif category == "words_skrt":
                    self.inflect_n_modify_trie(word, skrt=True)
                    self.inflect_n_add_data(l)

                elif category == "remove":
                    self.inflect_n_modify_trie(l, deactivate=True)

                else:
                    raise SyntaxError(
                        "'category' is: '"
                        + category
                        + "'. Valid answers: words_bo, words_skrt,"
                        "words_non_inflected, entry_data, remove"
                    )

    def add_non_inflectible(self, word):
        syls = TokChunks(word).get_syls()
        if not syls:
            return None

        # infl = self.__join_syls(syls)
        self.add(syls)

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
                        data = {"skrt": True}
                    else:
                        data.update({"skrt": True})
                    self.add(infl, data=data)
                else:
                    self.add(infl, data=data)

    def inflect_n_add_data(self, line):
        form, pos, lemma, sense, freq = self.__parse_line(line)
        freq = int(freq) if freq else None
        lemma = self.__join_syls(TokChunks(lemma).get_syls()) if lemma else None

        inflected = self._get_inflected(form)
        if not inflected:
            return  # The entry is not Tibetan, so return doing nothing

        for infl, _ in inflected:
            affixed = True if _ else False
            data = {
                k: v
                for k, v in [
                    ("lemma", lemma),
                    ("pos", pos),
                    ("freq", freq),
                    ("sense", sense),
                    ("affixed", affixed),
                ]
                if v is not None
            }
            self.add_data(infl, data)

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

        inflected = [(syls, None)]
        affixed = self.bosyl.get_all_affixed(syls[-1])
        if affixed:
            for infl, data in affixed:
                infl_word = syls[:-1] + [infl]
                inflected.append((infl_word, {"affixation": data}))

        self.tmp_inflected[word] = inflected
        return inflected

    @staticmethod
    def __join_syls(syls):
        return "".join([syl if syl.endswith(NAMCHE) else syl + TSEK for syl in syls])

    @staticmethod
    def __clean_lines(f):
        # cuts off comments, then strips empty lines
        lines = (
            line[: line.index(HASH)] if HASH in line else line for line in f.readlines()
        )
        return (l for l in lines if l)

    @staticmethod
    def __parse_line(line):
        """
        enables support of '\t' and ',' as separator.
        """
        fields = [None, None, None, None, None]
        if "\t" in line:
            sep = "\t"
        elif "," in line:
            sep = ","
        else:
            fields[0] = line
            fields[2] = NO_POS
            return fields

        for num, cell in enumerate(list(csv.reader([line], delimiter=sep))[0]):
            fields[num] = cell if cell else None
        return fields
