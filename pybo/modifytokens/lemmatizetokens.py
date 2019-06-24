# coding: utf-8
import yaml
from pathlib import Path

from ..vars import TSEK


class LemmatizeTokens:
    """
    Fills the lemma attribute of a Token if the token has an unaffixed_word content
    in other words, if it is valid tibetan syllables.
    """
    def __init__(self, lemma_folder=None):
        self.paths = [Path(__file__).parent.parent / 'resources' / 'lemmas']
        if isinstance(lemma_folder, str) or isinstance(lemma_folder, Path):
            self.paths.append(Path(lemma_folder).resolve())
        self.lemmas = {}
        self.particles = {}
        self.parse_lemmas()

    def lemmatize(self, token_list):
        for token in token_list:
            if token.text_unaffixed:
                no_tsek = token.text_unaffixed.rstrip(TSEK)
                if no_tsek in self.particles and token.pos == 'PART':
                    token.lemma = self.particles[no_tsek] + TSEK

                elif no_tsek in self.lemmas:
                    token.lemma = self.lemmas[no_tsek] + TSEK

                else:
                    token.lemma = token.text_unaffixed

    @staticmethod
    def parse_lemma_file(filename):
        """
        :param filename: input file
        :return: dict where key is a form and value is its lemma
        """
        filename = Path(filename)
        with filename.open('r', encoding='utf-8-sig') as f:
            parsed_yaml = yaml.load(f.read(), Loader=yaml.FullLoader)

        lemmas = {}
        for lemma, forms in parsed_yaml.items():
            for form in forms:
                lemmas[form] = lemma

        return lemmas

    def parse_lemmas(self):
        paths = [p for path in self.paths for p in path.glob('*.yaml')]

        for lemmafile in paths:
            self.lemmas.update(self.parse_lemma_file(lemmafile))
