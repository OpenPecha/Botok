# coding: utf-8

"""Configuration file to set up botok
"""

from pathlib import Path
from textwrap import dedent
import yaml
from collections import defaultdict

default_config = dedent(
    """\
    tokenizers:
      trie_files:
        - &ancient words_bo/ancient.txt
        - &except words_bo/exceptions.txt
        - &uncomp words_bo/uncompound_lexicon.txt
        - &tsikchen words_bo/tsikchen.txt
        - &dagdra words_bo/dagdra.txt
        - &oral0 words_bo/oral_corpus_0.txt
        - &oral1 words_bo/oral_corpus_1.txt
        - &oral2 words_bo/oral_corpus_2.txt
        - &oral3 words_bo/oral_corpus_3.txt
        - &oral4 words_bo/recordings_4.txt
        - &mgd words_bo/mgd.txt
        - &verbs words_bo/verbs.txt
      skrt_files:
        - &skrt words_skrt/sanskrit.txt
      non_inflected:
        - &part words_non_inflected/particles.txt
      lem-pos-freq_files:
        - &lpf_soas entry_data/TiDC_corpus.csv
        - &lpf_part entry_data/particles.csv
      freq_files:
        - &freq_mgd frequency/mgd.txt
        - &tc frequency/tc.txt
      profiles:
        empty: []
        tsikchen: [*ancient, *except, *uncomp, *tsikchen, *part, *dagdra]
        POS: [*ancient, *except, *uncomp, *tsikchen, *part, *lpf_soas, *lpf_part, *dagdra]
        GMD: [*ancient, *except, *uncomp, *tsikchen, *mgd, *verbs, *skrt, *freq_mgd, *part, *lpf_soas, *lpf_part, *dagdra]

    adjustments:
      files:
        - &rdr adjustment/rdr_basis.yaml
      profiles:
        empty: []
        basic: [*rdr]"""
)


class Config:
    """botok config

    1. by default, the profile is one of those in the config file.

    2. setting mode='custom', a path to a custom content folder can be given in the profile argument.

    The custom folder must contain any combination of the following subdirs:
                            words_bo, words_skrt, entry_data, frequency, deactivate, adjustment

    - all folders are excepted to contain .txt files with a word a line, without ending tsek
    - pos should contain word-pos pairs in .txt files
    - lemmas should contain .yaml files with lines such as "lemma: [form1, form2, form3, ...]"

    3. the modifs argument contains a dir path to a similar structure as above.
       the files will be used to update the trie on the fly.
    """

    def __init__(self, filename="botok.yaml", conf_path=None):
        """Initialize the class

        Converting the configuration file into a Python dictionary object which
        contains all the necessary parameters to set up botok properly.

        The text file has to respect the YAML writing rules.
        For more information: 'https://pyyaml.org/wiki/PyYAML'

        :param filename: Filename of the file with its extension
        """
        self.filename = Path(filename).resolve()
        if conf_path:
            self.filename = Path(conf_path) / self.filename
        if self.filename.suffix != ".yaml":
            raise Exception("Unrecognised file extension. It only supports .yaml files")

        # if the file doesn't exist, write it with the default values
        if not self.filename.is_file():
            with self.filename.open("w", encoding="utf-8-sig") as f:
                f.write(default_config)

        with self.filename.open("r", encoding="utf-8-sig") as g:
            self.config = yaml.safe_load(g.read())

    def get_tok_data_paths(self, profile, modifs=None, mode="internal"):
        main_profile = defaultdict(list)
        if mode == "internal":
            files = self.config["tokenizers"]["profiles"][profile]
            for el in files:
                el = Path(__file__).parent / "resources" / Path(el)
                main_profile[el.parts[-2]].append(el)

        elif mode == "custom":
            self.__parse_tok_dir(profile, main_profile)
        else:
            raise ValueError('mode needs to be either "internal" or "custom".')

        user_modifs = defaultdict(list)
        if modifs:
            self.__parse_tok_dir(modifs, user_modifs)

        return main_profile, user_modifs

    def get_adj_data_paths(self, profile, modifs=None, mode="internal"):
        main = []
        if mode == "internal":
            files = self.config["adjustments"]["profiles"][profile]
            for el in files:
                el = Path(__file__).parent / "resources" / Path(el)
                main.append(el)

        elif mode == "custom":
            self.__parse_adj_dir(profile, main)
        else:
            raise ValueError('mode needs to be either "internal" or "custom".')

        custom = []
        if modifs:
            self.__parse_adj_dir(modifs, custom)

        return main, custom

    def __parse_tok_dir(self, dirpath, paths):
        dirpath = Path(dirpath).resolve()
        assert dirpath.is_dir()
        bo = dirpath / "words_bo"
        skrt = dirpath / "words_skrt"
        non_infl = dirpath / "words_non_inflected"
        lem_pos_freq = dirpath / "entry_data"
        freq = dirpath / "frequency"
        deact = dirpath / "deactivate"

        for p in [bo, skrt, non_infl, lem_pos_freq, freq, deact]:
            if p.is_dir():
                for el in list(p.glob("*.txt")) + list(p.glob("*.csv")):
                    el = Path(__file__).parent / "resources" / Path(el)
                    paths[el.parts[-2]].append(el)

    def __parse_adj_dir(self, dirpath, paths):
        dirpath = Path(dirpath).resolve()
        assert dirpath.is_dir()
        adjs = dirpath / "adjustment"
        if adjs.is_dir():
            for el in adjs.glob("*.yaml"):
                el = Path(__file__).parent / "resources" / Path(el)
                paths.append(el)

    def reset_default(self):
        """Resets the configuration file to the default values"""
        with self.filename.open("w", encoding="utf-8-sig") as f:
            f.write(default_config)
