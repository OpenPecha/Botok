# coding: utf-8

"""Configuration file to set up Pybo
"""

from pathlib import Path
from textwrap import dedent
import yaml

default_config = dedent('''\
                        tokenizers:
                          trie_files:
                            - &ancient trie/ancient.txt
                            - &except trie/exceptions.txt
                            - &uncomp trie/uncompound_lexicon.txt
                            - &tsikchen trie/tsikchen.txt
                            - &oral0 trie/oral_corpus_0.txt
                            - &oral1 trie/oral_corpus_1.txt
                            - &oral2 trie/oral_corpus_2.txt
                            - &oral3 trie/oral_corpus_3.txt
                            - &record trie/recordings_4.txt
                            - &part trie/particles.txt
                            - &mgd trie/mgd.txt
                            - &verbs trie/verbs.txt
                          skrt_files:
                            - &skrt sanskrit/sanskrit.txt
                          pos_files:
                            - &soas pos/Tibetan.DICT
                          freq_files:
                            - &freq_mgd frequency/mgd.txt
                            - &tc frequency/tc.txt
                          profiles:
                            empty: []
                            pytib: [*ancient, *except, *uncomp, *tsikchen, *soas, *part]
                            POS: [*ancient, *except, *uncomp, *tsikchen, *soas, *part]
                            PP: [*part]
                            GMD: [*ancient, *except, *uncomp, *tsikchen, *mgd, *verbs, *soas, *skrt, *freq_mgd, *part]
                        
                        pipeline:
                          basic:
                              pre: pre_basic
                              tok: spaces
                              proc: spaces_fulltext
                              frm: plaintext
                          pybo_raw_content:
                              pre: pre_basic
                              tok: pybo
                              pybo_profile: GMD
                              proc: pybo_raw_content
                              frm: plaintext
                          pybo_raw_lines:
                              pre: pre_basic_lines
                              tok: pybo
                              pybo_profile: GMD
                              proc: pybo_raw_content
                              frm: plaintext
                          syls:
                              pre: pre_basic
                              tok: syls
                              proc: spaces_fulltext
                              frm: plaintext
                          pybo_raw_types:
                              pre: pre_basic
                              tok: pybo
                              pybo_profile: GMD
                              proc: pybo_raw_types
                              frm: types''')


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
            self.config = yaml.load(g.read(), Loader=yaml.FullLoader)

    def get_tokenizer_profile(self, profile):
        """Get the profile configuration list

        Each profile has a list of files which can be collected by this function.

        :param profile: the profile name
        :return: the list of files of the selected profile
        """
        return self.config["tokenizers"]["profiles"][profile]

    def get_pipeline_profile(self, profile):

        return self.config["pipeline"][profile]

    def reset_default(self):
        """Resets the configuration file to the default values"""
        with self.filename.open('w', encoding='utf-8-sig') as f:
            f.write(default_config)


if __name__ == '__main__':
    config = Config("pybo.yaml")
    config.reset_default()
    print(config.get_tokenizer_profile('POS'))
