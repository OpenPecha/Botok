# coding: utf8
import csv
from pathlib import Path

from ..chunks.chunks import TokChunks
from ..config import Config
from ..modifytokens.adjusttokens import AdjustTokens
from ..modifytokens.mergedagdra import MergeDagdra
from ..modifytokens.splitaffixed import split_affixed
from ..textunits.bosyl import BoSyl
from ..tries.trie import Trie
from ..vars import AA, TSEK
from .tokenize import Tokenize


def get_part_lemmas(path):
    part_lemmas = {}
    if not path.is_file():
        return part_lemmas
    with path.open("r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in list(reader)[1:]:
            form, _, lemma, _, _ = row
            part_lemmas[form] = lemma
    return part_lemmas


class WordTokenizer:
    """
    Convenience class to tokenize a given string.

    """

    def __init__(
        self, config=None, ignore_chars=None, build_trie=False,
    ):
        """
        :param tok_profile: profile for building the trie. (see config.yaml)
        """
        if not config:
            # if config is not given then use default config
            config = Config()

        self.config = config
        self.ignore_chars = ignore_chars
        self.tok = Tokenize(
            Trie(
                BoSyl,
                config.profile,
                main_data=config.dictionary,
                custom_data=config.adjustments,
                pickle_path=config.dialect_pack_path.parent,
                build=build_trie,
            )
        )

        self.adj = AdjustTokens(
            main=config.dictionary["rules"], custom=config.adjustments["rules"]
        )

        self.part_lemmas = get_part_lemmas(
            config.dialect_pack_path
            / "dictionary"
            / "words_non_inflected"
            / "particles.tsv"
        )

    def tokenize(self, string, split_affixes=True, spaces_as_punct=False, debug=False):
        """
        :param string: to be tokenized
        :param split_affixes: separates the affixed particles into seperate tokens if True
        :param debug: print debug info while parsing
        :return: list of pybo.tokenizers.Token objects
        """
        preprocessed = TokChunks(
            string, ignore_chars=self.ignore_chars, space_as_punct=spaces_as_punct
        )
        preprocessed.serve_syls_to_trie()
        tokens = self.tok.tokenize(preprocessed, debug=debug)

        if split_affixes:
            split_affixed(tokens)

        self._get_default_lemma(tokens)
        self._choose_default_entry(tokens)

        # merge pa/po/ba/bo tokens with previous ones
        MergeDagdra().merge(tokens)

        # do adjustments
        tokens = self.adj.adjust(tokens)

        return tokens

    def _get_default_lemma(self, token_list):
        for t in token_list:
            # pass any token that is not a word
            if not t.text_unaffixed:
                continue

            # otherwise, check whether the aa needs to be added and if a tsek should be added
            if t.affix and not t.affix_host:
                part = "".join(["".join(syl) for syl in t.syls])
                lemma = self.part_lemmas[part] if part in self.part_lemmas else part
                lemma += TSEK
            elif not t.affix and t.affix_host:
                lemma = (
                    t.text_unaffixed + AA + TSEK
                    if t.affixation["aa"]
                    else t.text_unaffixed + TSEK
                )
            else:
                lemma = (
                    t.text_unaffixed
                    if t.text_unaffixed.endswith(TSEK)
                    else t.text_unaffixed + TSEK
                )

            for m in t.senses:
                if "lemma" not in m and ("pos" in m and m["pos"] != "NON_WORD"):
                    m["lemma"] = lemma
            if not t.senses:
                t.senses.append({"lemma": lemma})

    @staticmethod
    def _choose_default_entry(token_list):
        def choose_n_apply(senses, t):
            s = sorted(senses, key=len, reverse=True)
            for a in ["pos", "lemma", "freq", "sense"]:
                if a in s[0]:
                    t[a] = s[0][a]

        for t in token_list:
            if t.senses:
                # Categorize all meanings in three groups
                affixed, non_affixed, no = [], [], []
                for m in t.senses:
                    if "affixed" in m:
                        if m["affixed"]:
                            affixed.append(m)
                        else:
                            non_affixed.append(m)
                    else:
                        no.append(m)

                # Decide what meaning to use as default
                # get a meaning from either group in the following order: non_affixed, no, affixed
                # take the one with the highest amount of attrs
                if non_affixed:
                    choose_n_apply(non_affixed, t)
                elif no:
                    choose_n_apply(no, t)
                elif affixed:
                    choose_n_apply(affixed, t)
                else:
                    raise ValueError("This should never happen.")
