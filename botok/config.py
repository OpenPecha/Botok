# coding: utf-8

"""Configuration file to set up botok
"""

from pathlib import Path
from textwrap import dedent
import yaml
from collections import defaultdict

from .vars import __version__


default_config = dedent(
    """\
    tokenizers:
      trie_files:
        - &ancient words/ancient.tsv
        - &except words/exceptions.tsv
        - &uncomp words/uncompound_lexicon.tsv
        - &tsikchen words/tsikchen.tsv
        - &dagdra words/dagdra.tsv
      profiles:
        empty: []
        POS: [*ancient, *except, *uncomp, *tsikchen, *dagdra]

    adjustments:
      files:
        - &rdr adjustment/rdr_basis.tsv
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
            self.filename = Path(conf_path) / filename
        if self.filename.suffix != ".yaml":
            raise Exception("Unrecognised file extension. It only supports .yaml files")

        # if the file doesn't exist, write it with the default values
        if not self.filename.is_file():
            with self.filename.open("w", encoding="utf-8-sig") as f:
                f.write(f"{__version__}\n{default_config}")

        with self.filename.open("r", encoding="utf-8-sig") as g:
            dump = g.read()
            version, dump = dump.split("\n", 1)
            # version = dump[:dump.find("\n")]
            if __version__ > version:
                print(f"Updating config file to version {__version__}")
                with self.filename.open("w", encoding="utf-8-sig") as f:
                    dump = default_config
                    f.write(f"{__version__}\n{default_config}")
            self.config = yaml.safe_load(dump)

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

        # add non-inflected to the main profile
        if profile != "empty":
            main_profile["words_non_inflected"] = [Path(__file__).parent / "resources/particles.tsv"]

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
        bo = dirpath / "words"
        skrt = dirpath / "words_skrt"
        deact = dirpath / "deactivate"

        for p in [bo, skrt, deact]:
            if p.is_dir():
                for el in list(p.glob("*.txt")) + list(p.glob("*.tsv")):
                    el = Path(__file__).parent / "resources" / Path(el)
                    paths[el.parts[-2]].append(el)

    def __parse_adj_dir(self, dirpath, paths):
        dirpath = Path(dirpath).resolve()
        assert dirpath.is_dir()
        adjs = dirpath / "adjustment"
        if adjs.is_dir():
            for el in adjs.glob("*.tsv"):
                el = Path(__file__).parent / "resources" / Path(el)
                paths.append(el)

    def reset_default(self):
        """Resets the configuration file to the default values"""
        with self.filename.open("w", encoding="utf-8-sig") as f:
            f.write(default_config)
