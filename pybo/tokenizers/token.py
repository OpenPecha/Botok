# coding: utf-8
from ..vars import TSEK, AA


class Token:
    def __init__(self):
        self.text = ""
        self.char_types = []
        self.has_merged_dagdra = None
        self.lemma = ""
        self.chunk_type = None
        self.start = 0
        self.len = None
        self.syls_idx = None
        self.pos = ""
        self.affixation = {}
        self.entries = None
        self.affix = False
        self.affix_host = False
        self.form_freq = None
        self.freq = None
        self.skrt = False
        self._ = {}  # dict for any user specific data

    def __getitem__(self, attr):
        # allows to access attributes with the Token['attr'] syntax, besides the Token.attr default
        try:
            return self.__getattribute__(attr)
        except AttributeError:
            raise AttributeError("does not have attribute: " + attr)

    def __setitem__(self, key, value):
        # enforces not to add any extra attribute. Token._ should be used for any custom data
        if hasattr(self, key):
            if key != "_":
                self.__dict__[key] = value
            else:
                if not isinstance(value, dict):
                    raise TypeError("only dicts are accepted for Token._")
                self.__dict__[key].update(value)
        else:
            raise AttributeError("Token objects don't have " + key + " as attribute")

    @property
    def syls(self):
        return (
            [[self.text[s] for s in syl] for syl in self.syls_idx]
            if self.syls_idx
            else ""
        )

    @property
    def text_cleaned(self):
        """
        Will append a TSEK to every syllable except syllables that host
        an affix.

        """
        if self.syls:
            cleaned = TSEK.join(["".join(syl) for syl in self.syls])
            if self.affix_host and not self.affix:
                return cleaned
            else:
                return cleaned + TSEK
        else:
            return ""

    @property
    def text_unaffixed(self):
        unaffixed = TSEK.join(["".join(syl) for syl in self.syls]) if self.syls else ""
        if (
            self.affixation
            and not self.affix
            and "len" in self.affixation
            and len([True for m in self.entries if "affixed" in m and m["affixed"]]) > 0
        ):
            unaffixed = unaffixed[: -self.affixation["len"]]

            if unaffixed and "aa" in self.affixation and self.affixation["aa"]:
                unaffixed += AA

        if self.affixation and self.affix_host and not self.affix:
            return unaffixed
        elif unaffixed:
            return unaffixed + TSEK
        else:
            return ""

    def __repr__(self):
        out = 'text: "{}"\n'.format(self.text)
        if self.text_cleaned:
            out += 'text_cleaned: "{}"\n'.format(self.text_cleaned)
        if self.text_unaffixed:
            out += 'text_unaffixed: "{}"\n'.format(self.text_unaffixed)
        if self.syls and self.syls != []:
            out += (
                'syls: ["' + '", "'.join(["".join(syl) for syl in self.syls]) + '"]\n'
            )
        if self.pos:
            out += "pos: {}\n".format(self.pos)
        if self.lemma:
            out += "lemma: {}\n".format(self.lemma)
        if self.entries:
            out += (
                "entries: | "
                + " | ".join(
                    [
                        ", ".join([f"{k}: {v}" for k, v in m.items()])
                        for m in self.entries
                    ]
                )
                + " |\n"
            )
        if self.char_types:
            out += "char_types: |" + "|".join(self.char_types) + "|\n"
        if self.chunk_type:
            out += "chunk_type: {}\n".format(self.chunk_type)
        if self.form_freq:
            out += "form_freq: {}\n".format(self.form_freq)
        if self.freq:
            out += "freq: {}\n".format(self.freq)
        if self.skrt:
            out += "skrt: {}\n".format(self.skrt)
        if self.affix:
            out += "affix: {}\n".format(self.affix)
        if self.affix_host:
            out += "affix_host: {}\n".format(self.affix_host)
        if self.has_merged_dagdra:
            out += "has_merged_dagdra: {}\n".format(self.has_merged_dagdra)
        if self.syls_idx:
            out += "syls_idx: {}\n".format(self.syls_idx)
        out += "start: {}\n".format(self.start)
        out += "len: {}\n".format(self.len)
        if self._:
            out += "\n"
            for k, v in self._.items():
                out += "_{}: {}\n".format(k, v)
        out += "\n"
        return out
