# coding: utf-8
from ..vars import AFFIX_SEP, TSEK, AA_TSEK


class Token:

    def __init__(self):
        self.text = ''
        self.char_types = None
        self.aa_word = None
        self.papo_word = None
        self.lemma = ''
        self.chunk_type = None
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

    def __getitem__(self, attr):
        # allows to access attributes with the Token['attr'] syntax, besides the Token.attr default
        try:
            return self.__getattribute__(attr)
        except AttributeError:
            raise AttributeError('does not have attribute: ' + attr)

    def __setitem__(self, key, value):
        # enforces not to add any extra attribute. Token._ should be used for any custom data
        if hasattr(self, key):
            if key != '_':
                self.__dict__[key] = value
            else:
                if not isinstance(value, dict):
                    raise TypeError('only dicts are accepted for Token._')
                self.__dict__[key].update(value)
        else:
            raise AttributeError("Token objects don't have " + key + ' as attribute')

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
    def text_cleaned(self):
        """
        Will append a TSEK to every syllable except syllables that host
        an affix.

        """
        if self.syls:
            cleaned = TSEK.join([''.join([self.text[idx] for idx in syl]) for syl in self.syls])
            if self.affixed and not self.affix:
                return cleaned
            else:
                return cleaned + TSEK
        else:
            return ''

    @property
    def text_unaffixed(self):
        if self.aa_word and (not self.affix and self.affixed):
            if self.text_cleaned.endswith(TSEK):
                return self.text_cleaned[:-1] + AA_TSEK
            else:
                return self.text_cleaned + AA_TSEK
        elif self.tag.count(AFFIX_SEP) == 3:
            _, _, affix_len, aa = self.tag.split(AFFIX_SEP)
            if affix_len:
                affix_len = int(affix_len)
                if self.text_cleaned.endswith(TSEK):
                    if aa:
                        return self.text_cleaned[:-affix_len - 1] + AA_TSEK
                    else:
                        return self.text_cleaned[:-affix_len - 1] + TSEK
                else:
                    if aa:
                        return self.text_cleaned[:-affix_len] + AA_TSEK
                    else:
                        return self.text_cleaned[:-affix_len] + TSEK

        if self.text_cleaned and not self.text_cleaned.endswith(TSEK):
            return self.text_cleaned + TSEK
        else:
            return self.text_cleaned

    def __repr__(self):
        out = 'content: "{}"'.format(self.text)
        if self.text_cleaned:
            out += '\ncleaned_content: "{}"'.format(self.text_cleaned)
        if self.text_unaffixed:
            out += '\nunaffixed_word: "{}"'.format(self.text_unaffixed)
        if self.lemma:
            out += '\nlemma: "{}"'.format(self.lemma)
        out += '\nstart: ' + str(self.start)
        out += '\nlen: ' + str(self.len)
        if self.syls and self.syls != []:
            out += '\nsyls (' + ' '.join([''.join([self.text[char] for char in syl])
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
        out += '\n\n'
        return out
