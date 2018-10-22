class ValidityError(Exception):
    '''Raised when a validity check is not passed'''

from collections import Counter
import pybo as bo

# 1. PREPARATION

# 1.1. Initializing the tokenizer
tok = bo.BoTokenizer('POS')

# 1.2. Loading in text
input_str = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'

# -------------------------

# 2. CREATING THE OBJECTS

# 2.1. creating pre_processed object
pre_processed = bo.PyBoTextChunks(input_str)

# 2.2. creating tokens object
tokens = tok.tokenize(input_str)

# -------------------------

# 3. TESTING ALL CLASS OBJECT ATTRIBUTES
# (this needs to be checking accuracy and not just function)

# 3.1. testing pre processed attributes
for a in dir(pre_processed):
    if not a.startswith('__'):
        print(getattr(pre_processed, a))

# 3.2. testing tokens attributes
for a in dir(tokens):
    if not a.startswith('__'):
        getattr(tokens, a)

# -------------------------

# 4. FUNCTIONALITY TESTING

# 4.1. accessing single token
tokens[0]

# 4.2. accessing content in all tokens
[t.content for t in tokens]

# 4.3. accessing tags in all tokens
[t.tag for t in tokens]

# 4.4. accessing tags that are nouns in all tokens
[t.content for t in tokens if t.tag == 'NOUNᛃᛃᛃ']

# 4.5. separating content based on tags and compiling into one list

tags = set([t.tag for t in tokens])
l = []
for tag in tags:
    l.append([t.content for t in tokens if t.tag == tag])

# -------------------------

# 5. VALIDITY TESTING

# 5.1. length of output
expected = 13
if len(l) != expected:
    raise ValidityError('Test 5.1. failed with list length ' + str(len(l)) + ' instead of the expected ' + str(expected))
