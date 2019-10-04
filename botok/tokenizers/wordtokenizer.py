# coding: utf8
from pathlib import Path
import csv

from .tokenize import Tokenize
from ..modifytokens.splitaffixed import split_affixed
from ..modifytokens.mergedagdra import MergeDagdra
from ..modifytokens.adjusttokens import AdjustTokens
from ..tries.trie import Trie
from ..chunks.chunks import TokChunks
from ..textunits.bosyl import BoSyl
from ..config import Config
from ..vars import TSEK, AA

part_lemmas = {}
filename = Path(__file__).parent.parent / "resources" / "entry_data" / "particles.csv"
with filename.open("r", encoding="utf-8-sig") as f:
    reader = csv.reader(f, delimiter="\t")
    for row in list(reader)[1:]:
        form, lemma, _ = row
        part_lemmas[form] = lemma


class WordTokenizer:
    """
    Convenience class to tokenize a given string.

    """

    def __init__(
        self,
        tok_profile="POS",
        tok_modifs=None,
        tok_mode="internal",
        ignore_chars=None,
        adj_profile="basic",
        adj_modifs=None,
        adj_mode="internal",
        conf_path=None,
    ):
        """
        :param tok_profile: profile for building the trie. (see config.yaml)
        """
        config = Config(conf_path=conf_path)
        main, custom = config.get_tok_data_paths(
            tok_profile, modifs=tok_modifs, mode=tok_mode
        )
        self.ignore_chars = ignore_chars
        tok_profile = (
            tok_mode if tok_mode == "custom" else tok_profile
        )  # trie will be named custom if mode is custom
        self.tok = Tokenize(
            Trie(
                BoSyl,
                tok_profile,
                main_data=main,
                custom_data=custom,
                pickle_path=conf_path,
            )
        )

        adj_main, adj_custom = config.get_adj_data_paths(
            adj_profile, modifs=adj_modifs, mode=adj_mode
        )
        self.adj = AdjustTokens(main=adj_main, custom=adj_custom)

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
        self.adj.adjust(tokens)

        return tokens

    @staticmethod
    def _get_default_lemma(token_list):
        for t in token_list:
            # pass any token that is not a word
            if not t.text_unaffixed:
                continue

            # otherwise, check whether the aa needs to be added and if a tsek should be added
            if t.affix and not t.affix_host:
                part = "".join(["".join(syl) for syl in t.syls])
                lemma = part_lemmas[part] if part in part_lemmas else part
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

            for m in t.entries:
                if "lemma" not in m and ("pos" in m and m["pos"] != "NON_WORD"):
                    m["lemma"] = lemma
            if not t.entries:
                t.entries.append({"lemma": lemma})

    @staticmethod
    def _choose_default_entry(token_list):
        def choose_n_apply(entries, t):
            s = sorted(entries, key=len, reverse=True)
            for a in ["pos", "lemma", "freq"]:
                if a in s[0]:
                    t[a] = s[0][a]

        for t in token_list:
            if t.entries:
                # Categorize all meanings in three groups
                affixed, non_affixed, no = [], [], []
                for m in t.entries:
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
