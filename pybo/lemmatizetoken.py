# coding: utf-8
from .helpers import open_file
import yaml
import os


class LemmatizeTokens:
    """
    Fills the lemma attribute of a Token if the token has an unaffixed_word content
    in other words, if it is valid tibetan syllables.
    """
    def __init__(self, lemma_folder=None):
        self.particles_path = os.path.join(os.path.split(__file__)[0], 'resources', 'lemmas', 'particles.yaml')
        self.paths = [os.path.join(os.path.split(__file__)[0], 'resources', 'lemmas')]
        if lemma_folder:
            self.paths.append(lemma_folder)
        self.lemmas = {}
        self.particles = {}
        self.parse_lemmas()

    def lemmatize(self, token_list):
        for token in token_list:
            if token.unaffixed_word:
                no_tsek = token.unaffixed_word.rstrip('་')
                if no_tsek in self.particles and token.pos == 'PART':
                    token.lemma = self.particles[no_tsek] + '་'

                elif no_tsek in self.lemmas:
                    token.lemma = self.lemmas[no_tsek] + '་'

                else:
                    token.lemma = token.unaffixed_word

    @staticmethod
    def parse_lemma_file(filename):
        """
        :param filename: input file
        :return: dict where key is a form and value is its lemma
        """
        parsed_yaml = yaml.load(open_file(filename))

        lemmas = {}
        for lemma, forms in parsed_yaml.items():
            for form in forms:
                lemmas[form] = lemma

        return lemmas

    def parse_lemmas(self):
        def gen_file_paths(folders):
            paths = [os.path.join(os.path.split(__file__)[0], folder, f) for folder in folders for f in os.listdir(folder)]
            paths.remove(self.particles_path)
            return paths

        for lemmafile in gen_file_paths(self.paths):
            self.lemmas.update(self.parse_lemma_file(lemmafile))

        self.particles.update(self.parse_lemma_file(self.particles_path))
