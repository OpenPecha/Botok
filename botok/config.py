# coding: utf-8

"""Configuration file to set up botok
"""

from collections import defaultdict
from pathlib import Path
from textwrap import dedent

import yaml

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

    def __init__(
        self, d_pack_path=Path().home() / "Documents" / "pybo" / "bo_general_pack"
    ):
        """Create config from dialect_pack path."""
        self.d_pack_path = d_pack_path
        self.main = self._get_tok_data_paths("dictionary")
        self.adjustment = self._get_tok_data_paths("adjustment")

    def _get_tok_data_paths(self, d_type):
        data_paths = defaultdict(list)
        for path in (self.d_pack_path / d_type).iterdir():
            data_paths[path.name] = list(path.iterdir())
        return data_paths

    def reset_default(self):
        """Resets the configuration file to the default values"""
        with self.filename.open("w", encoding="utf-8-sig") as f:
            f.write(default_config)
