import os
from .sdtrie import *

def _get_trie_path(name):
    return os.path.join(os.path.split(__file__)[0], 'data', 'chinese', name)

zhuyin_csv = get_trie_from_file(_get_trie_path("zhuyin.csv"), "zhuyin_csv")
chinese_trad_csv = get_trie_from_file(_get_trie_path("chinese_trad.csv"), "chinese_trad_csv")
exception_csv = get_trie_from_file(_get_trie_path("exception.csv"), "exception_csv")

space = " "*2

def _simplify_api(s):
    # simplify onset
    if '\u0325' in s:
        s = s.replace('\u0325', '')
    elif '\u030A' in s:
        s = s.replace('\u030A', '')
    # simplify coda
    s = s.rstrip("ː\u031A\u032Fgkprlɣɪˊˋ")
    # m
    if s.endswith("m"):
        s = s[0]+(s[1:].replace("m", "̃ŋ"))
        if "ø" in s:
            s = s.replace("ø", "o")
    elif "n" in s[1:] and not "̃" in s :
        s = s[0]+(s[1:].replace("n", "̃n"))
    elif "ŋ" in s[1:] and not "̃" in s :
        s = s[0]+(s[1:].replace("ŋ", "̃ŋ"))
    # vowel
    if "ə" in s :
        s = s.replace("ə", "a")
    elif "ɛ" in s :
        s = s.replace("ɛ", "e")
    elif "ỹŋ" in s :
        s = s.replace("y", "i")
    return s

def api2chinese(api, phon={"zhuyin":[], "chinese_trad":[]}) :
    ws = [api.split(".")]
    for index, w in enumerate(ws):
        #Exception
        wj = ".".join(w)
        exc = exception_csv.get_data(wj)
        if exc:
            r = exc.split("|")
            phon["zhuyin"].append(r[0] + space)
            if len(w) > 1 or len(r) > 1:
                phon["chinese_trad"].append(r[1] + space)
            else :
                phon["chinese_trad"].append(chinese_trad_csv.get_data(r[0]) + space)
            continue

        for i, s in enumerate(w):
            if not s or s[-1:] == "ɪ" :
                continue
            so = s  #Keep the original one
            s = _simplify_api(s)
            #Tone
            s += "+" if not i and "ˊ" in so else "-"

            #Exception for simplified transcription
            exc = exception_csv.get_data("@"+s)
            if exc:
                r = exc.split("|")
                phon["zhuyin"].append(r[0] + space)
                if len(r) > 1:
                    phon["chinese_trad"].append(r[1] + space)
                else:
                    phon["chinese_trad"].append(chinese_trad_csv.get_data(r[0]) + space)
                continue
            elif zhuyin_csv.get_data(s):
                zhuyin = zhuyin_csv.get_data(s)
                chinese_trad = chinese_trad_csv.get_data(zhuyin)
            else:
                print("Can't find the syllable: " + so)
                zhuyin = chinese_trad = "?"

            phon["zhuyin"].append(zhuyin + space)
            phon["chinese_trad"].append(chinese_trad + space)

    zhuyin = "".join(phon["zhuyin"]).strip(' ')
    chinese_trad = "".join(phon["chinese_trad"]).strip(' ')

    phon["zhuyin"].clear()
    phon["chinese_trad"].clear()

    return {"zhuyin":zhuyin, "chinese_trad":chinese_trad}
