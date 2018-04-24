# coding: utf-8
import re
from .sylcomponents import SylComponents


class BoSyl(SylComponents):
    def __init__(self):
        SylComponents.__init__(self)
        self.affixes = {'ར': {'len': 1, 'POS': 'la'},
                        'ས': {'len': 1, 'POS': 'gis'},
                        'འི': {'len': 2, 'POS': 'gi'},
                        'འམ': {'len': 2, 'POS': 'am'},
                        'འང': {'len': 2, 'POS': 'ang'},
                        'འོ': {'len': 2, 'POS': 'o'},
                        'འིའོ': {'len': 4, 'POS': 'gi+o'}
                        }

    def is_affixable(self, syl):
        """expects a clean syllable without ending tsek"""
        regex = r'(ར|ས|འི|འམ|འང|འོ)$'
        return self.is_thame(syl) and re.findall(regex, syl) == []

    def get_all_affixed(self, syl):
        """

        :param syl: syl to be affixed
        :return: if affixable: list of (<syl+affixed>, {'len': int, 'POS': str, 'aa': bool})
                 otherwise   : <syl>
        """
        if self.is_affixable(syl):
            affixed = []
            aa = ''
            if syl.endswith('འ'):
                aa = 'aa'
                syl = syl[:-1]

            for a in self.affixes.keys():
                metadata = self.affixes[a]

                metadata.update({'aa': aa})
                affixed.append((syl+a, metadata))
            return affixed
        else:
            return syl


if __name__ == '__main__':
    """ example of use """

    bs = BoSyl()
    print(bs.is_affixable('དྭོགས'))
    test = 'བཀྲིས'
    for syl in ['བཀྲིས', 'བཀའ', 'བཀྲི', 'དེའོ', 'དེའིའོ', 'དགས', 'ལེགས']:
        print(syl, 'can be affixed:', bs.is_affixable(syl))
        if bs.is_affixable(syl):
            print(bs.get_all_affixed(syl))
            # [('བཀར', 'ར', True), ('བཀས', 'ས', True), ('བཀའི', 'འི', True), ('བཀའམ', 'འམ', True), ('བཀའང', 'འང', True),
            # ('བཀའོ', 'འོ', True), ('བཀའིའོ', 'འིའོ', True)]
