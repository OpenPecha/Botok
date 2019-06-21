# coding: utf-8

"""Configuration file to set up Pybo
"""

from pathlib import Path
from textwrap import dedent
import yaml
from collections import defaultdict

default_config = dedent('''\
    tokenizers:
      trie_files:
        - &ancient lexica_bo/ancient.txt
        - &except lexica_bo/exceptions.txt
        - &uncomp lexica_bo/uncompound_lexicon.txt
        - &tsikchen lexica_bo/tsikchen.txt
        - &oral0 lexica_bo/oral_corpus_0.txt
        - &oral1 lexica_bo/oral_corpus_1.txt
        - &oral2 lexica_bo/oral_corpus_2.txt
        - &oral3 lexica_bo/oral_corpus_3.txt
        - &oral4 lexica_bo/recordings_4.txt
        - &part lexica_bo/particles.txt
        - &mgd lexica_bo/mgd.txt
        - &verbs lexica_bo/verbs.txt
      skrt_files:
        - &skrt lexica_skrt/lexica_skrt.txt
      pos_files:
        - &soas pos/TiDC_corpus.txt
        - &partpos pos/particles.txt
      freq_files:
        - &freq_mgd frequencies/mgd.txt
        - &tc frequencies/tc.txt
      profiles:
        empty: []
        tsikchen: [*ancient, *except, *uncomp, *tsikchen, *soas, *part]
        POS: [*ancient, *except, *uncomp, *tsikchen, *soas, *part, *partpos]
        GMD: [*ancient, *except, *uncomp, *tsikchen, *mgd,*verbs, *soas, *skrt, *freq_mgd, *part, *partpos]''')


class Config:
    """pybo config

    1. by default, the profile is one of those in the config file.

    2. setting mode='custom', a path to a custom content folder can be given in the profile argument.

    The custom folder must contain any combination of the following subdirs:
                            lexica_bo, lexica_skrt, pos, lemmas, frequencies, deactivate

    - all folders are excepted to contain .txt files with a word a line, without ending tsek
    - pos should contain word-pos pairs in .txt files
    - lemmas should contain .yaml files with lines such as "lemma: [form1, form2, form3, ...]"

    3. the modifs argument contains a dir path to a similar structure as above.
       the files will be used to update the trie on the fly.
    """
    def __init__(self, filename='pybo.yaml'):
        """Initialize the class

        Converting the configuration file into a Python dictionnary object which
        contains all the necesary parameters to set up Pybo properly.

        The text file has to respect the YAML writing rules.
        For more information: 'https://pyyaml.org/wiki/PyYAML'

        :param filename: Filename of the file with its extension
        """
        self.filename = Path(filename).resolve()
        if self.filename.suffix != ".yaml":
            raise Exception("Unrecognised file extension. It only supports .yaml files")

        # if the file doesn't exist, write it with the default values
        if not self.filename.is_file():
            with self.filename.open('w', encoding='utf-8-sig') as f:
                f.write(default_config)

        with self.filename.open('r', encoding='utf-8-sig') as g:
            self.config = yaml.load(g.read(), Loader=yaml.FullLoader)

    def get_tok_data_paths(self, profile, modifs=None, mode='internal'):
        main_profile = defaultdict(list)
        if mode == 'internal':
            files = self.config['tokenizers']['profiles'][profile]
            for el in files:
                el = Path(__file__).parent / 'resources' / Path(el)
                main_profile[el.parts[-2]].append(el)

        elif mode == 'custom':
            self.__parse_dir(profile, main_profile)
        else:
            raise ValueError('mode needs to be either "internal" or "custom".')

        user_modifs = defaultdict(list)
        if modifs:
            self.__parse_dir(modifs, user_modifs)

        return main_profile, user_modifs

    def __parse_dir(self, dirpath, paths):
        dirpath = Path(dirpath).resolve()
        assert dirpath.is_dir()
        bo = dirpath / 'lexica_bo'
        skrt = dirpath / 'lexica_skrt'
        pos = dirpath / 'pos'
        lem = dirpath / 'lemmas'
        freq = dirpath / 'frequencies'
        deact = dirpath / 'deactivate'

        for p in [bo, skrt, pos, lem, freq, deact]:
            if p.is_dir():
                for el in list(p.glob('*.txt')) + list(p.glob('*.yaml')):
                    el = Path(__file__).parent / 'resources' / Path(el)
                    paths[el.parts[-2]].append(el)

    def reset_default(self):
        """Resets the configuration file to the default values"""
        with self.filename.open('w', encoding='utf-8-sig') as f:
            f.write(default_config)
