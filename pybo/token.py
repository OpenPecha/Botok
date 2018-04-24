# coding: utf-8


class Token:
    def __init__(self):
        self.content = None
        self.chunk_type = None
        self.char_groups = None
        self.start = 0
        self.length = None
        self.syls = None
        self.tag = None
        self.pos = None
        self.char_markers = {1: 'cons', 2: 'sub-cons', 3: 'vow', 4: 'tsek', 5: 'skrt-cons', 6: 'skrt-sub-cons',
                             7: 'skrt-vow', 8: 'punct', 9: 'num', 10: 'in-syl-mark', 11: 'special-punct', 12: 'symbol',
                             13: 'no-bo-no-skrt', 14: 'other', 15: 'space', 16: 'underscore'}
        self.chunk_markers = {100: 'bo', 101: 'non-bo', 102: 'punct', 103: 'non-punct', 104: 'space', 105: 'non-space',
                              106: 'syl', 1000: 'word', 1001: 'non-word'}

    def __getitem__(self, item):
        mapping = {'content': self.content,
                   'chunk_type': self.chunk_type,
                   'start': self.start,
                   'length': self.length,
                   'syls': self.syls,
                   'tag': self.tag,
                   'pos': self.pos}
        if item in mapping:
            return mapping[item]
        else:
            return None

    def get_pos(self):
        affix_sep = 'ᛃ'
        if affix_sep in self.tag:
            self.pos = self.tag.split(affix_sep)[0]
        else:
            self.pos = self.tag

    @property
    def cleaned_content(self):
        """
        Will add a tsek at every syllable.
        Warning: Since it is unaware (at the moment) of syllables that have been
        separated from their affixed particles, it will add a tsek in the middle
        """
        if self.syls:
            return ''.join([''.join([self.content[idx] for idx in syl] + ['་']) for syl in self.syls])
        else:
            return None

    def __repr__(self):
        out = 'content: "'+self.content+'"'
        out += '\nchar types: '
        out += '|'+'|'.join([self.char_markers[self.char_groups[idx]]
                            for idx in sorted(self.char_groups.keys())])+'|'
        out += '\ntype: ' + self.chunk_markers[self.chunk_type]
        out += '\nstart in input: ' + str(self.start)
        out += '\nlength: ' + str(self.length)
        out += '\nsyl chars in content'
        if self.syls:
            out += '(' + ' '.join([''.join([self.content[char] for char in syl]) for syl in self.syls]) + '): '
        else:
            out += ': '
        out += str(self.syls)
        out += '\ntag: ' + self.tag
        out += '\nPOS: ' + self.pos
        return out
