from pybo import *

# a. instanciate the tokenizer
bs = BoSyl()  # used to dynamically generate affixed versions
trie = PyBoTrie(bs, profile='POS')  # loads or builds a trie
tok = Tokenizer(trie)

# b. pre-process the input string
pre_processed = PyBoTextChunks(' ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ')

# c. tokenize
tokens = tok.tokenize(pre_processed)

tagged = ['"{}"/{}'.format(w.content, w.tag) for w in tokens]
print(', '.join(tagged))
# " ཤི་"/VERB---, "བཀྲ་ཤིས་  "/NOUN---, "tr"/non-bo, " བདེ་་ལེ གས"/NOUN---, "།"/punct,
# " བཀྲ་ཤིས་"/NOUN---, "བདེ་ལེགས་"/NOUN---, "ཀཀ"/non-word

print(tokens[0].to_string)
# content: " ཤི་"
# char types: |space|cons|vow|tsek|
# type: syl
# start in input: 0
# length: 4
# syl chars in content(ཤི): [[1, 2]]
# tag: VERB---
