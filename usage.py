from pybo import *


###########################################
tok = WordTokenizer('POS')  # instanciated
tokens = tok.tokenize("ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ། མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།། །།མཁའ།")
###########################################


### Extract token-string / POS pairs ########

tagged = ['"{}"/{}'.format(w.text, w.pos) for w in tokens]
print(', '.join(tagged))


### Extract the cleaned version of the tokens

cleaned = [w.text_cleaned for w in tokens if w.text_cleaned]
print(' '.join(cleaned))
