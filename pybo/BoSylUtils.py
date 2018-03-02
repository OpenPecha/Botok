# coding: utf-8
import re
import os
import json


class SylComponents:
    """
    Provides information about a syllable
    """

    def __init__(self):
        # check for possible dadrag https://github.com/eroux/tibetan-spellchecker/blob/master/doc/second-suffix-da.md
        # roots is an import from root + rareC and wazurC and suffixes is the 'AB' entry from  suffixes.json
        self.data_path = os.path.join(os.path.split(__file__)[0], "resources", "SylComponents.json")

        with open(self.data_path, 'r', -1, 'utf-8-sig') as f:
            data = json.loads(f.read())
        self.dadrag = data['dadrag']
        self.roots = data['roots']
        self.suffixes = data['suffixes']
        self.Csuffixes = data['Csuffixes']

        # all dicts from https://github.com/eroux/tibetan-spellchecker/tree/master/syllables
        self.special = data['special']
        self.wazurs = data['wazurs']
        self.exceptions = self.special + self.wazurs
        self.ambiguous = data['ambiguous']

        self.m_roots = data['m_roots']
        self.m_exceptions = data['m_exceptions']
        self.m_wazurs = data['m_wazurs']
        self.mingzhis = self.m_roots.copy()
        self.mingzhis.update(self.m_exceptions)
        self.mingzhis.update(self.m_wazurs)

    def get_parts(self, syl):
        """
        :param syl: takes a syllable as input
        :return: a tuple:
                        - (prefix+main-stack, vowel+suffixes)
                        - (exceptions, x)
                        - a list of solutions if there is more than one
                        - None if the syllable is not wellformed
        """
        if syl not in self.exceptions and syl not in self.ambiguous:
            l_s = len(syl)
            # find all possible roots
            root = []
            if len(syl) > 5 and syl[:6] in self.roots:
                root.append(syl[:6])
            if len(syl) > 4 and syl[:5] in self.roots:
                root.append(syl[:5])
            if len(syl) > 3 and syl[:4] in self.roots:
                root.append(syl[:4])
            if len(syl) > 2 and syl[:3] in self.roots:
                root.append(syl[:3])
            if len(syl) > 1 and syl[:2] in self.roots:
                root.append(syl[:2])
            if len(syl) > 0 and syl[:1] in self.roots:
                root.append(syl[:1])
            # find all possible suffixes
            suffix = []
            if l_s > 1:
                if syl[l_s - 1:] in self.suffixes:
                    suffix.append(syl[l_s - 1:])
                if syl[l_s - 2:] in self.suffixes:
                    suffix.append(syl[l_s - 2:])
                if syl[l_s - 3:] in self.suffixes:
                    suffix.append(syl[l_s - 3:])
                if syl[l_s - 4:] in self.suffixes:
                    suffix.append(syl[l_s - 4:])
                if syl[l_s - 5:] in self.suffixes:
                    suffix.append(syl[l_s - 5:])

            # deal with all the C roots
            # print(self.syl, root)
            if root != [] and self.roots[root[0]] == 'C':
                if root[0] == syl:
                    return root[0], ''
                else:
                    for s in suffix:
                        if s in self.Csuffixes and root[0] + s == syl:
                            return root[0], s

            # find all possible matches
            solutions = []
            if suffix != [] and root != []:
                # dealing with all other cases
                for r in root:
                    for s in suffix:
                        # unexpected འ་
                        if self.roots[r] == 'A' and s == 'འ' and r + s == syl:
                            # print(r, roots[r])
                            return None
                        else:
                            # if root+suffix make the syllable + avoids duplicates
                            if r + s == syl and (r, s) not in solutions:
                                solutions.append((r, s))
                if solutions != []:
                    if len(solutions) > 1:
                        return solutions
                    else:
                        return solutions[0]
                # root + suffix don’t make syl
                else:
                    # print(solutions)
                    return None
            elif root != []:
                # print('k')
                for r in root:
                    if r in self.roots and r == syl:
                        # if syllable is valid without suffix + without aa
                        if self.roots[r] != 'NB' and (r, '') not in solutions:
                            solutions.append((r, ''))
                if solutions != []:
                    if len(solutions) > 1:
                        return solutions
                    else:
                        return solutions[0]
                # non-valid syl
                else:
                    return None
            # non-valid syl
            else:
                return None
        elif syl in self.ambiguous:
            return self.ambiguous[syl]
        else:
            return syl, 'x'

    def get_mingzhi(self, syl):
        """
        :param syl: syllable
        :return:    the mingzhi that will serve for the particle agreement. for example, ཁྱེའུར will return འ
                    None if more than one solution from get_parts()
        """
        components = self.get_parts(syl)
        if type(components) == 'list' or not components:
            return None
        else:
            return self.mingzhis[components[0]]

    def get_info(self, syl):
        """
        :param syl: syllable
        :return: required info to part_agreement:
                - dadrag
                - thame
                - the syllable
        """
        mingzhi = self.get_mingzhi(syl)
        if not mingzhi:
            return None
        else:
            if syl in self.dadrag:
                return 'dadrag'
            elif re.findall(mingzhi + '([ྱྲླྭྷ]?[ིེོུ]?(འ?[ིོུ]?ར?ས?|(འ[མང])?|(འིའོ)?))$', syl) != []:
                return 'thame'
            else:
                return syl

    def is_thame(self, syl):
        """
        :param syl: a string without tsek or other punct
        :return: True if the syllabe is affixable or is already affixed, False otherwise
        """
        return self.get_info(syl) == 'thame'


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
    sc = SylComponents()
    assert sc.get_parts('བཀྲིས') == ('བཀྲ', 'ིས')

    bs = BoSyl()
    print(bs.is_affixable('དྭོགས'))
    test = 'བཀྲིས'
    for syl in ['བཀྲིས', 'བཀའ', 'བཀྲི', 'དེའོ', 'དེའིའོ', 'དགས', 'ལེགས']:
        print(syl, 'can be affixed:', bs.is_affixable(syl))
        if bs.is_affixable(syl):
            print(bs.get_all_affixed(syl))
            # [('བཀར', 'ར', True), ('བཀས', 'ས', True), ('བཀའི', 'འི', True), ('བཀའམ', 'འམ', True), ('བཀའང', 'འང', True),
            # ('བཀའོ', 'འོ', True), ('བཀའིའོ', 'འིའོ', True)]
