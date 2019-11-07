from pathlib import Path

from botok import *

expose_data("/tmp/truc", "POS")
###########################################
in_str = "ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ། མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།། །།མཁའ།"
WT = WordTokenizer("GMD")
tokens = WT.tokenize(in_str)
print()

in_str = "ལ་པོ་ལ་པོ་ལ་པོ་"
t = Text(in_str, tok_params={"profile": "POS"})
tokens = t.tokenize_words_raw_text
tt = Text(
    in_str,
    tok_params={
        "profile": "POS",
        "modifs": Path(__file__).parent / "tests" / "trie_data",
    },
)
ttokens = tt.tokenize_words_raw_text
print(tokens)
print(ttokens)
###########################################

#
# ### Extract token-string / POS pairs ########
#
# tagged = ['"{}"/{}'.format(w.text, w.pos) for w in tokens]
# print(', '.join(tagged))
#
#
# ### Extract the cleaned version of the tokens
#
# cleaned = [w.text_cleaned for w in tokens if w.text_cleaned]
# print(' '.join(cleaned))
