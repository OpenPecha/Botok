# coding: utf-8
from .helpers import AFFIX_SEP, TSEK


class Token:
    a_n_tsek = 'འ་'
    char_markers = {1: 'cons', 2: 'sub-cons', 3: 'vow', 4: 'tsek', 5: 'skrt-cons', 6: 'skrt-sub-cons',
                    7: 'skrt-vow', 8: 'punct', 9: 'num', 10: 'in-syl-mark', 11: 'special-punct', 12: 'symbol',
                    13: 'no-bo-no-skrt', 14: 'other', 15: 'space', 16: 'underscore', 17: 'skrt-vow_long'}
    chunk_markers = {100: 'bo', 101: 'non-bo', 102: 'punct', 103: 'non-punct', 104: 'space', 105: 'non-space',
                     106: 'syl', 107: 'sym', 108: 'non-sym', 109: 'num', 110: 'non-num',
                     1000: 'word', 1001: 'oov'}

    def __init__(self):
        self.content = ''
        self.phono = ''
        self.char_types = None
        self.aa_word = None
        self.papo_word = None
        self.lemma = ''
        self.chunk_type = None
        self.type = None
        self.char_groups = None
        self.start = 0
        self.len = None
        self.syls = None
        self.tag = ''
        self.pos = ''
        self.affix = False
        self.affixed = False
        self.freq = None
        self.skrt = False
        self._ = {}  # dict for any user specific data

    def __getitem__(self, item):
        mapping = {'content': self.content,
                   'phono': self.phono,
                   'char_types': self.char_types,
                   'aa_word': self.aa_word,
                   'papo_word': self.papo_word,
                   'lemma': self.lemma,
                   'chunk_type': self.chunk_type,
                   'type': self.type,
                   'char_groups': self.char_groups,
                   'start': self.start,
                   'len': self.len,
                   'syls': self.syls,
                   'tag': self.tag,
                   'pos': self.pos,
                   'affix': self.affix,
                   'affixed': self.affixed,
                   'skrt': self.skrt,
                   'freq': self.freq,
                   'cleaned_content': self.cleaned_content,
                   'unaffixed_word': self.unaffixed_word}

        return mapping[item] if item in mapping else None

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
        Will append a TSEK to every syllable except syllables that host
        an affix.

        """
        if self.syls:
            cleaned = TSEK.join([''.join([self.content[idx] for idx in syl]) for syl in self.syls])
            if self.affixed and not self.affix:
                return cleaned
            else:
                return cleaned + TSEK
        else:
            return ''

    @property
    def unaffixed_word(self):
        if self.aa_word and (not self.affix and self.affixed):
            if self.cleaned_content.endswith(TSEK):
                return self.cleaned_content[:-1] + Token.a_n_tsek
            else:
                return self.cleaned_content + Token.a_n_tsek
        elif self.tag.count(AFFIX_SEP) == 3:
            _, _, affix_len, aa = self.tag.split(AFFIX_SEP)
            if affix_len:
                affix_len = int(affix_len)
                if self.cleaned_content.endswith(TSEK):
                    if aa:
                        return self.cleaned_content[:-affix_len - 1] + Token.a_n_tsek
                    else:
                        return self.cleaned_content[:-affix_len - 1] + TSEK
                else:
                    if aa:
                        return self.cleaned_content[:-affix_len] + Token.a_n_tsek
                    else:
                        return self.cleaned_content[:-affix_len] + TSEK

        if self.cleaned_content and not self.cleaned_content.endswith(TSEK):
            return self.cleaned_content + TSEK
        else:
            return self.cleaned_content

    def __repr__(self):
        out = 'content: "{}"'.format(self.content)
        if self.cleaned_content:
            out += '\ncleaned_content: "{}"'.format(self.cleaned_content)
        if self.unaffixed_word:
            out += '\nunaffixed_word: "{}"'.format(self.unaffixed_word)
        if self.lemma:
            out += '\nlemma: "{}"'.format(self.lemma)
        if self.phono:
            out += '\nphono: /{}/'.format(self.phono)
        out += '\nchar_types: |' + '|'.join([self.char_markers[self.char_groups[idx]]
                                             for idx in sorted(self.char_groups.keys())])+'|'
        out += '\ntype: ' + self.type
        out += '\nstart: ' + str(self.start)
        out += '\nlen: ' + str(self.len)
        if self.syls and self.syls != []:
            out += '\nsyls (' + ' '.join([''.join([self.content[char] for char in syl])
                                   for syl in self.syls]) + '): ' + str(self.syls)
        if self.tag:
            out += '\ntag: {}'.format(self.tag)
        if self.pos:
            out += '\npos: {}'.format(self.pos)
        if self.affix:
            out += '\naffix: {}'.format(self.affix)
        if self.affixed:
            out += '\naffixed: {}'.format(self.affixed)
        if self.aa_word:
            out += '\naa_word: {}'.format(self.aa_word)
        if self.skrt:
            out += "\nskrt: {}".format(self.skrt)
        if self.freq:
            out += '\nfreq: {}'.format(self.freq)
        if self._:
            out += '\n'
            for k, v in self._.items():
                out += "_{}: {}\n".format(k, v)
        out += '\n'
        return out
