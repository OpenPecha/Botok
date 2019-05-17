from pybo import *


###########################################
tok = BoTokenizer('POS')  # instanciated
tok.tok.trie.rebuild_trie()

input_str = ' དེ་ལ་ནི་རང་ལྷ་དེ་འོ་སྙམ་པའི་རིགས་འདྲ་བར་བར་མ་ཆད་དུ་མི་དགོས'
tokens = tok.tokenize(input_str)
###########################################


### Extract token-string / POS pairs ########

tagged = ['"{}"/{}'.format(w.content, w.pos) for w in tokens]
print(', '.join(tagged))
# " ཤི་"/VERB, "བཀྲ་ཤིས་  "/NOUN, "tr"/non-bo, " བདེ་་ལེ གས"/NOUN, "།"/punct,
# " བཀྲ་ཤིས་"/NOUN, "བདེ་ལེགས་"/NOUN, "ཀཀ"/non-word


### Extract the cleaned version of the tokens

cleaned = [w.cleaned_content for w in tokens if w.cleaned_content]
print(' '.join(cleaned))
# ཤི་ བཀྲ་ཤིས་ བདེ་ལེགས་ བཀྲ་ཤིས་ བདེ་ལེགས་ ཀཀ་


### The fields found in each token ###########

print(tokens[0])
# content: " ཤི་"
# char types: |space|cons|vow|tsek|
# type: syl
# start in input: 0
# length: 4
# syl chars in content(ཤི): [[1, 2]]
# tag: VERBᛃᛃᛃ
# POS: VERB

count_tokens = 'pybo_raw_types'
pipeline = BoPipeline(pybo_profile=count_tokens)
pipeline.prof = 'POS'
result = pipeline.pipe_str(' ཤི་བཀྲ་ཤིས་  tr བདེ་ལེགས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ  བཀྲ་ཤིས་')
print(result)
# ཤི་	1
# བཀྲ་ཤིས་ 	1
# tr 	1
# བདེ་ལེགས	1
# ། 	1
# བཀྲ་ཤིས་	1
# བདེ་ལེགས་	1
# ཀཀ	1
