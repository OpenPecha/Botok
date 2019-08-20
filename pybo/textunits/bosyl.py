# coding: utf-8
from .sylcomponents import SylComponents


class BoSyl(SylComponents):
    def __init__(self):
        SylComponents.__init__(self)
        self.affixes = {
            "ར": {"len": 1, "type": "la"},
            "ས": {"len": 1, "type": "gis"},
            "འི": {"len": 2, "type": "gi"},
            "འམ": {"len": 2, "type": "am"},
            "འང": {"len": 2, "type": "ang"},
            "འོ": {"len": 2, "type": "o"},
            "འིའོ": {"len": 4, "type": "gi+o"},
            "འིའམ": {"len": 4, "type": "gi+am"},
            "འིའང": {"len": 4, "type": "gi+ang"},
            "འོའམ": {"len": 4, "type": "o+am"},
            "འོའང": {"len": 4, "type": "o+ang"},
        }

    def is_affixable(self, syl):
        """expects a clean syllable without ending tsek"""
        affixable = False
        if self.is_thame(syl):
            affixable = True
            for ending in ["ར", "ས", "འི", "འོ", "མ", "ང"]:
                if len(syl) > len(ending) and syl.endswith(ending):
                    affixable = False
        return affixable

    def get_all_affixed(self, syl):
        """
        :param syl: syl to be affixed
        :return: if affixable: [(<syl+affixed>, {'len': int, 'type': str, 'aa': bool}), (..., ...)]
                 otherwise   : <syl>
        """
        if self.is_affixable(syl):
            aa = False
            if syl.endswith("འ") and len(syl) > 1:
                syl = syl[:-1]
                aa = True

            affixed = []
            for a in self.affixes.keys():
                metadata = {}
                metadata.update(self.affixes[a])
                metadata.update({"aa": aa})
                affixed.append((syl + a, metadata))
            return affixed

        else:
            return None
