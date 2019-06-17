# coding: utf-8
from .sylcomponents import SylComponents


class BoSyl(SylComponents):
    def __init__(self):
        SylComponents.__init__(self)
        self.affixes = {'ར': {'len': 1, 'affix': 'la'},
                        'ས': {'len': 1, 'affix': 'gis'},
                        'འི': {'len': 2, 'affix': 'gi'},
                        'འམ': {'len': 2, 'affix': 'am'},
                        'འང': {'len': 2, 'affix': 'ang'},
                        'འོ': {'len': 2, 'affix': 'o'},
                        'འིའོ': {'len': 4, 'affix': 'gi+o'},
                        'འིའམ': {'len': 4, 'affix': 'gi+am'},
                        'འིའང': {'len': 4, 'affix': 'gi+ang'},
                        'འོའམ': {'len': 4, 'affix': 'o+am'},
                        'འོའང': {'len': 4, 'affix': 'o+ang'}
                        }

    def is_affixable(self, syl):
        """expects a clean syllable without ending tsek"""
        affixable = False
        if self.is_thame(syl):
            affixable = True
            for ending in ['ར', 'ས', 'འི', 'འོ', 'མ', 'ང']:
                if len(syl) > len(ending) and syl.endswith(ending):
                    affixable = False
        return affixable

    def get_all_affixed(self, syl):
        """
        :param syl: syl to be affixed
        :return: if affixable: [(<syl+affixed>, {'len': int, 'affix': str, 'aa': bool}), (..., ...)]
                 otherwise   : <syl>
        """
        if self.is_affixable(syl):
            affixed = []
            aa = False
            if syl.endswith('འ'):
                aa = True
                syl = syl[:-1]

            for a in self.affixes.keys():
                metadata = self.affixes[a]

                metadata.update({'aa': aa})
                affixed.append((syl+a, metadata))
            return affixed
        else:
            return syl
