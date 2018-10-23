# coding: utf-8

"""Configuration file to set up Pybo
"""

from pathlib import Path
import yaml

default_config = '''pybo:
  trie_files:
    - &part 'particles.txt'
    - &ancient ancient.txt
    - &except exceptions.txt
    - &uncomp uncompound_lexicon.txt
    - &tsikchen tsikchen.txt
    - &oral0 oral_corpus_0.txt
    - &oral1 oral_corpus_1.txt
    - &oral2 oral_corpus_2.txt
    - &oral3 oral_corpus_3.txt
    - &record recordings_4.txt
    - &mgd mgd.txt
    - &verb verbs.txt
  skrt_files:
    - &skrt ~ssanskrit.txt
  pos_files:
    - &tibdict ~pTibetan.DICT
  freq_files:
    - &freq_mgd ~fmgd.txt
  Profile:
    empty: []
    pytib: [*ancient, *except, *uncomp, *tsikchen, *tibdict, *part]
    POS: [*ancient, *except, *uncomp, *tsikchen, *tibdict, *part]
    PP: [*part]
    GMD: [*ancient, *except, *uncomp, *tsikchen, *mgd, *verb, *tibdict, *skrt, *freq_mgd, *part]'''


class Config:
    """Configuration class

    Attributes :
        filename: Complete filename of the configuration file
        config : Dictionary object containing all the configuration elements
    """
    def __init__(self, filename):
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
            self.config = yaml.load(g.read())

    def get_profile(self, profile):
        """Get the profile configuration list

        Each profile has a list of files which can be collected by this function.

        :param profile: the profile name
        :return: the list of files of the selected profile
        """
        return self.config["pybo"]["Profile"][profile]

    def reset_default(self):
        """Resets the configuration file to the default values"""
        with self.filename.open('w', encoding='utf-8-sig') as f:
            f.write(default_config)


if __name__ == '__main__':
    config = Config("config.yaml")
    config.reset_default()
    print(config.get_profile('POS'))
