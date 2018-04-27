# coding: utf-8
from .helpers import AFFIX_SEP


class Token:
    def __init__(self):
        self.content = ''
        self.aa_word = None
        self.lemma = ''
        self.chunk_type = None
        self.char_groups = None
        self.start = 0
        self.length = None
        self.syls = None
        self.tag = ''
        self.pos = ''
        self.affix = False
        self.affixed = False
        self.char_markers = {1: 'cons', 2: 'sub-cons', 3: 'vow', 4: 'tsek', 5: 'skrt-cons', 6: 'skrt-sub-cons',
                             7: 'skrt-vow', 8: 'punct', 9: 'num', 10: 'in-syl-mark', 11: 'special-punct', 12: 'symbol',
                             13: 'no-bo-no-skrt', 14: 'other', 15: 'space', 16: 'underscore'}
        self.chunk_markers = {100: 'bo', 101: 'non-bo', 102: 'punct', 103: 'non-punct', 104: 'space', 105: 'non-space',
                              106: 'syl', 1000: 'word', 1001: 'non-word'}
        self._ = {}  # dict for any user specific data

    def __getitem__(self, item):
        mapping = {'content': self.content,
                   'aa_word': self.aa_word,
                   'lemma': self.lemma,
                   'chunk_type': self.chunk_type,
                   'char_groups': self.char_groups,
                   'start': self.start,
                   'length': self.length,
                   'syls': self.syls,
                   'tag': self.tag,
                   'pos': self.pos,
                   'affix': self.affix,
                   'affixed': self.affixed,
                   'cleaned_content': self.cleaned_content,
                   'unaffixed_word': self.unaffixed_word}
        if item in mapping:
            return mapping[item]
        else:
            return None

    def get_pos_n_aa(self):
        if self.pos == '':
            if AFFIX_SEP in self.tag:
                parts = self.tag.split(AFFIX_SEP)
                self.pos = parts[0]
                if not self.aa_word and parts[-1] == 'aa':
                    self.aa_word = True
            else:
                self.pos = self.tag

    @property
    def cleaned_content(self):
        """
        Will append a tsek to every syllable except syllables that host
        an affix.

        """
        if self.syls:
            cleaned = '་'.join([''.join([self.content[idx] for idx in syl]) for syl in self.syls])
            if self.affixed and not self.affix:
                return cleaned
            else:
                return cleaned + '་'
        else:
            return ''

    @property
    def unaffixed_word(self):
        if self.aa_word and (not self.affix and self.affixed):
            if self.cleaned_content.endswith('་'):
                return self.cleaned_content[:-1] + 'འ་'
            else:
                return self.cleaned_content + 'འ'
        elif self.tag.count(AFFIX_SEP) == 3:
            _, _, affix_len, aa = self.tag.split(AFFIX_SEP)
            if affix_len:
                affix_len = int(affix_len)
                if self.cleaned_content.endswith('་'):
                    return self.cleaned_content[:-affix_len - 1] + 'འ་'
                else:
                    return self.cleaned_content[:-affix_len] + 'འ'
            else:
                return self.cleaned_content
        else:
            return self.cleaned_content

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
        out += '\ntag: '
        if self.tag:
            out += self.tag
        out += '\nPOS: '
        if self.pos:
            out += self.pos
        out += '\n'
        return out
