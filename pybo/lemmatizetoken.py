# coding: utf-8
import yaml
from pathlib import Path


class LemmatizeTokens:
    """
    Fills the lemma attribute of a Token if the token has an unaffixed_word content
    in other words, if it is valid tibetan syllables.
    """
    def __init__(self, lemma_folder=None):
        self.particles_path = Path(__file__).parent / 'resources' / 'lemmas' / 'particles.yaml'
        self.paths = []
        self.paths.append(self.particles_path.parent)
        if lemma_folder:
            self.paths.append(Path(lemma_folder).resolve())
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
        filename = Path(filename)
        with filename.open('r', encoding='utf-8-sig') as f:
            parsed_yaml = yaml.load(f.read())

        lemmas = {}
        for lemma, forms in parsed_yaml.items():
            for form in forms:
                lemmas[form] = lemma

        return lemmas

    def parse_lemmas(self):
        paths = [p for path in self.paths for p in path.glob('*.yaml')]

        for lemmafile in paths:
            self.lemmas.update(self.parse_lemma_file(lemmafile))
