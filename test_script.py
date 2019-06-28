# coding: utf8
from pybo import *
from pathlib import Path
from pytest import raises
from textwrap import dedent

# all the tests showcasing functionality from the test suite are copied here

##########################################################################################################
# test_basictrie.py
##########################################################################################################

trie = BasicTrie()

# populate the basic lexica_bo
words = 'hello goo good goodbye help gerald gold tea ted team to too tom stan standard money'
for w in words.split():
    trie.add(w)

# test word existence. has_word() is not used in pybo. it is only there for testing purposes
assert trie.has_word('goodbye') == {'data': {'_': {}}, 'exists': True}

# add content to data
trie.add_data('goodbye', {'POS': 'NOUN'})
assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'NOUN'}, 'exists': True}

# only adds key/value pairs to the existing dict. does not replace the data variable
trie.add_data('goodbye', {}, overwrite=True)
assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'NOUN'}, 'exists': True}

# by default, overwrites existing dict values
trie.add_data('goodbye', {'POS': 'VERB', 'lang': 'en'})
assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'VERB', 'lang': 'en'}, 'exists': True}

# can be set to not overwrite
trie.add_data('goodbye', {'POS': 'NOUN'}, overwrite=False)
assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'VERB', 'lang': 'en'}, 'exists': True}

# deactivates an entry in the lexica_bo, only modifying the Node.leaf value (bool) to be efficient
trie.deactivate('goodbye')
assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'VERB', 'lang': 'en'}, 'exists': False}

# reactivates the entry
trie.deactivate('goodbye', rev=True)
assert trie.has_word('goodbye') == {'data': {'_': {}, 'POS': 'VERB', 'lang': 'en'}, 'exists': True}

# walk() is used to externalize the walking of the lexica_bo
node = trie.head  # getting to the root of the lexica_bo
for char in 'goodbye':
    if char in node.children:
        node = node[char]  # one step down the lexica_bo

assert node.label == 'e'  # last char of the word
assert node.leaf is True  # we reached the end of a word
assert node.data == {'_': {}, 'POS': 'VERB', 'lang': 'en'}

##########################################################################################################
# test_bostring.py
##########################################################################################################

bo_str = 'བཀྲ་ཤིས་ ༡༢༣ tr  就到 郊外玩བདེ་ལེགས།'
m = CharMarkers

"""Testing whether, at a given index, the char category corresponds to what is expected."""
bs = BoString(bo_str)

idx = 0
assert 'བ' == bo_str[idx]
assert m.CONS == bs.base_structure[idx]

idx = 2
assert 'ྲ' == bo_str[idx]
assert m.SUB_CONS == bs.base_structure[idx]

idx = 7
assert '་' == bo_str[idx]
assert m.TSEK == bs.base_structure[idx]

idx = 9
assert '༡' == bo_str[idx]
assert m.NUMERAL == bs.base_structure[idx]

idx = 13
assert 't' == bo_str[idx]
assert m.LATIN == bs.base_structure[idx]

idx = 17
assert '就' == bo_str[idx]
assert m.CJK == bs.base_structure[idx]

##########################################################################################################
# test_bosyl.py
##########################################################################################################

bs = BoSyl()

# is_affixable() Vs. SylComponents.is_thame()
assert bs.is_thame('ཀུན') is False and bs.is_affixable('ཀུན') is False
assert bs.is_thame('དེའིའམ') is True and bs.is_affixable('དེའིའམ') is False
assert bs.is_thame('དེའི') is True and bs.is_affixable('དེའི') is False
assert bs.is_thame('ང') is True and bs.is_affixable('ང') is True

# get_all_affixed()
affixed = bs.get_all_affixed('ང')
assert affixed == [('ངར', {'len': 1, 'type': 'la', 'aa': False}),
                   ('ངས', {'len': 1, 'type': 'gis', 'aa': False}),
                   ('ངའི', {'len': 2, 'type': 'gi', 'aa': False}),
                   ('ངའམ', {'len': 2, 'type': 'am', 'aa': False}),
                   ('ངའང', {'len': 2, 'type': 'ang', 'aa': False}),
                   ('ངའོ', {'len': 2, 'type': 'o', 'aa': False}),
                   ('ངའིའོ', {'len': 4, 'type': 'gi+o', 'aa': False}),
                   ('ངའིའམ', {'len': 4, 'type': 'gi+am', 'aa': False}),
                   ('ངའིའང', {'len': 4, 'type': 'gi+ang', 'aa': False}),
                   ('ངའོའམ', {'len': 4, 'type': 'o+am', 'aa': False}),
                   ('ངའོའང', {'len': 4, 'type': 'o+ang', 'aa': False})]

affixed = bs.get_all_affixed('མཐའ')
assert affixed == [('མཐར', {'len': 1, 'type': 'la', 'aa': True}),
                   ('མཐས', {'len': 1, 'type': 'gis', 'aa': True}),
                   ('མཐའི', {'len': 2, 'type': 'gi', 'aa': True}),
                   ('མཐའམ', {'len': 2, 'type': 'am', 'aa': True}),
                   ('མཐའང', {'len': 2, 'type': 'ang', 'aa': True}),
                   ('མཐའོ', {'len': 2, 'type': 'o', 'aa': True}),
                   ('མཐའིའོ', {'len': 4, 'type': 'gi+o', 'aa': True}),
                   ('མཐའིའམ', {'len': 4, 'type': 'gi+am', 'aa': True}),
                   ('མཐའིའང', {'len': 4, 'type': 'gi+ang', 'aa': True}),
                   ('མཐའོའམ', {'len': 4, 'type': 'o+am', 'aa': True}),
                   ('མཐའོའང', {'len': 4, 'type': 'o+ang', 'aa': True})]

affixed = bs.get_all_affixed('ཀུན')
assert affixed is None

##########################################################################################################
# test_chunkframework.py
##########################################################################################################
c = ChunkMarkers

# def test_bo_nonbo():
string = 'བཀྲ་་ཤིས་བདེ་ལེགས། 23PIEIUZLDVéjoldvép«»("«»%='
cb = ChunkFramework(string)
chunks = cb.chunk_bo_chars()

output = cb.get_readable(chunks)
assert output == [('BO', 'བཀྲ་་ཤིས་བདེ་ལེགས། '), ('OTHER', '23PIEIUZLDVéjoldvép«»("«»%=')]


# def test_punct_nonpunct():
string = '༆ བཀྲ་ཤིས་བདེ་ལེགས།། །།'
cb = ChunkFramework(string)
chunks = cb.chunk_punct()

output = cb.get_readable(chunks)
assert output == [('PUNCT', '༆ '), ('NON_PUNCT', 'བཀྲ་ཤིས་བདེ་ལེགས'), ('PUNCT', '།། །།')]


# def test_sym_nonsym():
string = 'བཀྲ་ཤིས་བདེ་ལེགས། ༪༫༝༜༛༚༇༆'
cb = ChunkFramework(string)
chunks = cb.chunk_symbol()

output = cb.get_readable(chunks)
assert output == [('NON_SYM', 'བཀྲ་ཤིས་བདེ་ལེགས།'), ('SYM', ' ༪༫༝༜༛༚'), ('NON_SYM', '༇༆')]


# def test_num_nonnum():
string = 'བཀྲ་ཤིས་བདེ་ལེགས།  ༡༢༣༠༩༨'
cb = ChunkFramework(string)
chunks = cb.chunk_number()

output = cb.get_readable(chunks)
assert output == [('NON_NUM', 'བཀྲ་ཤིས་བདེ་ལེགས།'), ('NUM', '  ༡༢༣༠༩༨')]


# def test_space_nonspace():
string = 'བཀྲ་ཤིས་བདེ་ལེགས།   །བཀྲ་ཤིས་བདེ་ལེགས།'
cb = ChunkFramework(string)
chunks = cb.chunk_spaces()

output = cb.get_readable(chunks)
assert output == [('NON_SPACE', 'བཀྲ་ཤིས་བདེ་ལེགས།'), ('SPACE', '   '), ('NON_SPACE', '།བཀྲ་ཤིས་བདེ་ལེགས།')]


# def test_text():
string = 'བཀྲ་ཤིས་བདེ་ལེགས'
cb = ChunkFramework(string)
chunks = cb.syllabify()

output = cb.get_readable(chunks)
assert output == [('TEXT', 'བཀྲ་'), ('TEXT', 'ཤིས་'), ('TEXT', 'བདེ་'), ('TEXT', 'ལེགས')]


# def test_latin():
string = 'བཀྲ་ཤིས་བདེ་ལེགས This is a test.'
cb = ChunkFramework(string)
chunks = cb.chunk_latin()

output = cb.get_readable(chunks)
assert output == [('OTHER', 'བཀྲ་ཤིས་བདེ་ལེགས'), ('LATIN', ' This is a test.')]


# def test_cjk():
string = 'བཀྲ་ཤིས་བདེ་ལེགས 这是  什么'
cb = ChunkFramework(string)
chunks = cb.chunk_cjk()

output = cb.get_readable(chunks)
assert output == [('OTHER', 'བཀྲ་ཤིས་བདེ་ལེགས'), ('CJK', ' 这是  什么')]


# def test_other():
string = 'བཀྲ་ཤིས་བདེ་ལེགས กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ'
cb = ChunkFramework(string)
chunks = cb.chunk_bo_chars()

output = cb.get_readable(chunks)
assert output == [('BO', 'བཀྲ་ཤིས་བདེ་ལེགས '), ('OTHER', 'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ')]


# def test_full_example():
# Follows the order implemented in Chunks
string = '༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། 23PIEIUZLDVéjoldvép«»("«»%= ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ ' \
         'This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ'
cb = ChunkFramework(string)

# BO / OTHER
chunks = cb.chunk_bo_chars()
chunks = cb.clean_chunks(chunks)
output = cb.get_readable(chunks)
assert output == [('BO', '༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། '),
                  ('OTHER', '23PIEIUZLDVéjoldvép«»("«»%='),
                  ('BO', ' ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ '),
                  ('OTHER', 'This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ')]

# BO / PUNCT
chunks = cb.pipe_chunk(chunks, cb.chunk_punct, c.BO.value, c.PUNCT.value)
chunks = cb.clean_chunks(chunks)
output = cb.get_readable(chunks)
assert output == [('PUNCT', '༆ '),
                  ('BO', 'བཀྲ་ཤིས་བདེ་ལེགས'),
                  ('PUNCT', '།། །། '),  # NEW
                  ('OTHER', '23PIEIUZLDVéjoldvép«»("«»%= '),
                  ('BO', '༪༫༝༜༛༚'),
                  ('PUNCT', '༇༆ '),  # NEW
                  ('BO', '༡༢༣༠༩༨ '),
                  ('OTHER', 'This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ')]

# BO / NUM
chunks = cb.pipe_chunk(chunks, cb.chunk_number, c.BO.value, c.NUM.value)
chunks = cb.clean_chunks(chunks)
output = cb.get_readable(chunks)
assert output == [('PUNCT', '༆ '),
                  ('BO', 'བཀྲ་ཤིས་བདེ་ལེགས'),
                  ('PUNCT', '།། །། '),
                  ('OTHER', '23PIEIUZLDVéjoldvép«»("«»%= '),
                  ('BO', '༪༫༝༜༛༚'),
                  ('PUNCT', '༇༆ '),
                  ('NUM', '༡༢༣༠༩༨ '),  # NEW
                  ('OTHER', 'This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ')]

# BO / SYM
chunks = cb.pipe_chunk(chunks, cb.chunk_symbol, c.BO.value, c.SYM.value)
chunks = cb.clean_chunks(chunks)
output = cb.get_readable(chunks)
assert output == [('PUNCT', '༆ '),
                  ('BO', 'བཀྲ་ཤིས་བདེ་ལེགས'),
                  ('PUNCT', '།། །། '),
                  ('OTHER', '23PIEIUZLDVéjoldvép«»("«»%= '),
                  ('SYM', '༪༫༝༜༛༚'),  # NEW
                  ('PUNCT', '༇༆ '),
                  ('NUM', '༡༢༣༠༩༨ '),
                  ('OTHER', 'This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ')]

# TEXT
chunks = cb.pipe_chunk(chunks, cb.syllabify, c.BO.value, c.TEXT.value)
chunks = cb.clean_chunks(chunks)
output = cb.get_readable(chunks)
assert output == [('PUNCT', '༆ '),
                  ('TEXT', 'བཀྲ་'),  # NEW
                  ('TEXT', 'ཤིས་'),  # NEW
                  ('TEXT', 'བདེ་'),  # NEW
                  ('TEXT', 'ལེགས'),  # NEW
                  ('PUNCT', '།། །། '),
                  ('OTHER', '23PIEIUZLDVéjoldvép«»("«»%= '),
                  ('SYM', '༪༫༝༜༛༚'),
                  ('PUNCT', '༇༆ '),
                  ('NUM', '༡༢༣༠༩༨ '),
                  ('OTHER', 'This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ')]

# OTHER / CJK
chunks = cb.pipe_chunk(chunks, cb.chunk_cjk, c.OTHER.value, c.CJK.value)
chunks = cb.clean_chunks(chunks)
output = cb.get_readable(chunks)
assert output == [('PUNCT', '༆ '),
                  ('TEXT', 'བཀྲ་'),
                  ('TEXT', 'ཤིས་'),
                  ('TEXT', 'བདེ་'),
                  ('TEXT', 'ལེགས'),
                  ('PUNCT', '།། །། '),
                  ('OTHER', '23PIEIUZLDVéjoldvép«»("«»%= '),
                  ('SYM', '༪༫༝༜༛༚'),
                  ('PUNCT', '༇༆ '),
                  ('NUM', '༡༢༣༠༩༨ '),
                  ('OTHER', 'This is a test.'),
                  ('CJK', ' 这是  什么 '),  # NEW
                  ('OTHER', 'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ')]

# OTHER / LATIN
chunks = cb.pipe_chunk(chunks, cb.chunk_latin, c.OTHER.value, c.LATIN.value)
chunks = cb.clean_chunks(chunks)
output = cb.get_readable(chunks)
assert output == [('PUNCT', '༆ '),
                  ('TEXT', 'བཀྲ་'),
                  ('TEXT', 'ཤིས་'),
                  ('TEXT', 'བདེ་'),
                  ('TEXT', 'ལེགས'),
                  ('PUNCT', '།། །། '),
                  ('LATIN', '23PIEIUZLDVéjoldvép«»("«»%= '),  # NEW
                  ('SYM', '༪༫༝༜༛༚'),
                  ('PUNCT', '༇༆ '),
                  ('NUM', '༡༢༣༠༩༨ '),
                  ('LATIN', 'This is a test.'),  # NEW
                  ('CJK', ' 这是  什么 '),
                  ('OTHER', 'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ')]

##########################################################################################################
# test_chunks.py
##########################################################################################################

string = '༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། 23PIEIUZLDVéjoldvép«»("«»%= ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ ' \
             'This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ'


# def test_chunks():
c = Chunks(string)
chunks = c.make_chunks()
output = c.get_readable(chunks)
assert output == [('PUNCT', '༆ '),
                  ('TEXT', 'བཀྲ་'),
                  ('TEXT', 'ཤིས་'),
                  ('TEXT', 'བདེ་'),
                  ('TEXT', 'ལེགས'),
                  ('PUNCT', '།། །། '),
                  ('LATIN', '23PIEIUZLDVéjoldvép«»("«»%= '),  # NEW
                  ('SYM', '༪༫༝༜༛༚'),
                  ('PUNCT', '༇༆ '),
                  ('NUM', '༡༢༣༠༩༨ '),
                  ('LATIN', 'This is a test.'),  # NEW
                  ('CJK', ' 这是  什么 '),
                  ('OTHER', 'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ')]


# def test_tokchunks():
c = TokChunks(string)
c.serve_syls_to_trie()
# generate what the tokenizer will ingest
chunks = c.chunks
assert chunks == [(None, (105, 0, 2)),
                  ([2, 3, 4], (104, 2, 4)),          # syllable 1
                  ([6, 7, 8], (104, 6, 4)),          # syllable 2
                  ([10, 11, 12], (104, 10, 4)),      # syllable 3
                  ([14, 15, 16, 17], (104, 14, 4)),  # syllable 4
                  (None, (105, 18, 6)),
                  (None, (101, 24, 28)),
                  (None, (109, 52, 6)),
                  (None, (105, 58, 3)),
                  (None, (111, 61, 7)),
                  (None, (101, 68, 15)),
                  (None, (102, 83, 8)),
                  (None, (103, 91, 24))]

# the second element of each tuple is the chunk from Chunks
readable = [(a[0], c.get_readable([a[1]])[0]) for a in chunks]
assert readable == [(None,              ('PUNCT', '༆ ')),
                    ([2, 3, 4],         ('TEXT', 'བཀྲ་')),
                    ([6, 7, 8],         ('TEXT', 'ཤིས་')),
                    ([10, 11, 12],      ('TEXT', 'བདེ་')),
                    ([14, 15, 16, 17],  ('TEXT', 'ལེགས')),
                    (None,              ('PUNCT', '།། །། ')),
                    (None,              ('LATIN', '23PIEIUZLDVéjoldvép«»("«»%= ')),
                    (None,              ('SYM', '༪༫༝༜༛༚')),
                    (None,              ('PUNCT', '༇༆ ')),
                    (None,              ('NUM', '༡༢༣༠༩༨ ')),
                    (None,              ('LATIN', 'This is a test.')),
                    (None,              ('CJK', ' 这是  什么 ')),
                    (None,              ('OTHER', 'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ'))]

# just for the fun of it: get the cleaned syllable as it is done in the Tokenizer
chunks = [''.join([string[c] for c in chars]) + TSEK for chars, chunk in chunks if chars]
assert chunks == ['བཀྲ་', 'ཤིས་', 'བདེ་', 'ལེགས་']

##########################################################################################################
# test_chunktokenizer.py
##########################################################################################################

# def test_chunktokenizer():
input_str = ' ཤི་བཀྲ་ཤིས་  བདེ་་ལ             ེ       གས་ ' \
            'བཀྲ་ཤིས་བདེ་ལེགས ༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། 23PIEIUZLDVéjoldvép«»("«»%= ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ ' \
            'This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ'
st = ChunkTokenizer(input_str)
tokens = st.tokenize()
assert tokens == [('TEXT', ' ཤི་'),
                  ('TEXT', 'བཀྲ་'),
                  ('TEXT', 'ཤིས་'),
                  ('TEXT', '  བདེ་་'),
                  ('TEXT', 'ལ             ེ       གས་'),
                  ('TEXT', ' བཀྲ་'),
                  ('TEXT', 'ཤིས་'),
                  ('TEXT', 'བདེ་'),
                  ('TEXT', 'ལེགས'),
                  ('PUNCT', ' ༆ '),
                  ('TEXT', 'བཀྲ་'),
                  ('TEXT', 'ཤིས་'),
                  ('TEXT', 'བདེ་'),
                  ('TEXT', 'ལེགས'),
                  ('PUNCT', '།། །། '),
                  ('LATIN', '23PIEIUZLDVéjoldvép«»("«»%= '),
                  ('SYM', '༪༫༝༜༛༚'),
                  ('PUNCT', '༇༆ '),
                  ('NUM', '༡༢༣༠༩༨ '),
                  ('LATIN', 'This is a test.'),
                  ('CJK', ' 这是  什么 '),
                  ('OTHER', 'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ')]

##########################################################################################################
# test_config
##########################################################################################################

# def test_config():
config = Config()

# default config filename
assert config.filename.name == 'pybo.yaml'  # config.filename is a Path object

# paths for trie content
main, custom = config.get_tok_data_paths('POS')
# each profile contains one or more sections
assert [m for m in main] == ['lexica_bo', 'pos']
# each element in a Path object leading to a resource file
assert isinstance(main['pos'][0], Path)

# custom files to overwrite the existing trie can be added as follows
assert len(custom) == 0
main, custom = config.get_tok_data_paths('POS', modifs=Path(__file__).parent / 'tests/trie_data/')
assert [c for c in custom] == ['lexica_bo', 'lemmas'] == [t.parts[-1] for t in Path(Path(__file__).parent / 'tests/trie_data/').glob('*')]

# overwriting the main profile
main, custom = config.get_tok_data_paths(Path(__file__).parent / 'tests/trie_data/', mode='custom')
assert [m for m in main] == ['lexica_bo', 'lemmas']

##########################################################################################################
# test_splitaffixed.py
##########################################################################################################

# def test_split_token():
wt = WordTokenizer('empty')
wt.tok.trie.rebuild_trie()
wt.tok.trie.inflect_n_modify_trie('བདེ་བ་')
wt.tok.trie.inflect_n_add_data('བདེ་བ་\tNOUN', 'pos')
wt.tok.trie.inflect_n_modify_trie('གཏན་')
wt.tok.trie.inflect_n_add_data('གཏན་\tNOUN', 'pos')
wt.tok.trie.inflect_n_modify_trie('གྱི་')
wt.tok.trie.inflect_n_add_data('གྱི་\tPART', 'pos')
tokens = wt.tokenize('གཏན་གྱི་བདེ་བའི་རྒྱུ།', split_affixes=False)
assert len(tokens) == 5
assert tokens[2].text == 'བདེ་བའི་'
tokens = wt.tokenize('གཏན་གྱི་བདེ་བའི་རྒྱུ།')
assert len(tokens) == 6
assert tokens[2].text == 'བདེ་བ'
assert tokens[3].text == 'འི་'

##########################################################################################################
# test_sylcomponents.py
##########################################################################################################

# def test_components():
sc = SylComponents()

# A) get_parts()
# 1. (prefix+main-stack, vowel+suffixes)
assert sc.get_parts('བཀྲིས') == ('བཀྲ', 'ིས')
# 2. (exceptions, 'x')
assert sc.get_parts('མདྲོན') == ('མདྲོན', 'x')
# 3. a list of solutions if there is more than one (not yet encountered)
# 4. None if the syllable is not wellformed
assert sc.get_parts('ཀཀ') is None

# B) get_mingzhi()
assert sc.get_mingzhi('བསྒྲུབས') == 'ྒ'
# the mingzhi that will serve for the particle agreement:
assert sc.get_mingzhi('ཁྱེའུར') == 'འ'
# None if more than one solution from get_parts() (not yet encountered)

# support for dadrag
assert sc.get_mingzhi('ཀུནད') == 'ཀ'

# dadrag normalize
assert sc.normalize_dadrag('ཀུནད') == 'ཀུན'

# C) get_info()
# 1. 'dadrag'
# A syllable that historically received a "da" second suffix.
# As for now, the list contains ["ཀུན", "ཤིན", "འོན"] (See pybo/resources/SylComponents.json)
assert sc.get_info('ཀུན') == 'dadrag'
# 2. 'thame'
# A syllable that has the potential of hosting an affixed particle.
# Will be returned for all such syls, whether or not a particle is affixed.
assert sc.get_info('དེའིའམ') == 'thame'
assert sc.get_info('དེའི') == 'thame'
# 3 the syllable itself in all other cases
assert sc.get_info('ང') == 'thame'
assert sc.get_info('རྒྱལ') == 'རྒྱལ'

# D) is_thame()
# True if the syllabe is affixable or is already affixed, False otherwise
assert sc.is_thame('ཀུན') is False
assert sc.is_thame('དེའིའམ') is True
assert sc.is_thame('དེའི') is True
assert sc.is_thame('ང') is True

##########################################################################################################
# test_token.py
##########################################################################################################

# def test_token():
t = Token()
t.text = 'test'
# Token supports access to attributes in two ways (required for CQL found in third_party/cql.py)
assert t.text == t['text']
assert t._ == t['_']

# setting existing attributes like dicts is supported
attrs = {'pos': 'NOUN', 'freq': '123', 'len': 4}
for k, v in attrs.items():
    t[k] = v
assert str(t) == dedent("""\
                        text: "test"
                        pos: NOUN
                        freq: 123
                        start: 0
                        len: 4

                        """)

# raises an error when trying to add a new attribute
with raises(AttributeError, match=r"Token objects don't have .* as attribute"):
    t['non_attr'] = 'test'

##########################################################################################################
# test_tokenize.py
##########################################################################################################

# def test_tokenize():
profile = 'empty'
main, custom = Config().get_tok_data_paths(profile)
tok = Tokenize(Trie(BoSyl, profile, main, custom))
tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་')
tok.trie.inflect_n_add_data('བཀྲ་ཤིས་\tNOUN', 'pos')
tok.trie.inflect_n_add_data('བཀྲ་ཤིས་\t17500', 'freq')
tok.trie.inflect_n_modify_trie('མཐའ་')
tok.trie.inflect_n_add_data('མཐའ་\tNOUN', 'pos')
preproc = TokChunks('མཐའི་བཀྲ་ཤིས། ཀཀ abc མཐའི་རྒྱ་མཚོ་')
preproc.serve_syls_to_trie()
tokens = tok.tokenize(preproc)
expected = dedent("""\
                    text: "བཀྲ་ཤིས"
                    text_cleaned: "བཀྲ་ཤིས་"
                    text_unaffixed: "བཀྲ་ཤིས་"
                    syls: ["བཀྲ", "ཤིས"]
                    char_types: |CONS|CONS|SUB_CONS|TSEK|CONS|VOW|CONS|
                    chunk_type: TEXT
                    pos: NOUN
                    freq: 17500
                    syls_idx: [[0, 1, 2], [4, 5, 6]]
                    start: 5
                    len: 7

                    """)
str(tokens[0])
assert str(tokens[1]) == expected
assert tokens[2].text == '། '
assert tokens[2].chunk_type == 'PUNCT'


# def test_non_max2():
profile = 'empty'
main, custom = Config().get_tok_data_paths(profile)
tok = Tokenize(Trie(BoSyl, profile, main, custom))
tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་')
tok.trie.inflect_n_add_data('བཀྲ་ཤིས་\tNOUN', 'pos')
tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་བདེ་ལེགས།')  # to ensure we're not in a maximal match
preproc = TokChunks('བཀྲ་ཤིས་བདེ་བཀྲ་')
preproc.serve_syls_to_trie()
tokens = tok.tokenize(preproc)
assert tokens[0].text == 'བཀྲ་ཤིས་'
assert tokens[0].pos == 'NOUN'
assert tokens[1].text == 'བདེ་'
assert tokens[1].pos == 'NON_WORD'
assert tokens[2].text == 'བཀྲ་'
assert tokens[2].pos == 'OOV'


# def test_non_max_end_of_string():
profile = 'empty'
main, custom = Config().get_tok_data_paths(profile)
tok = Tokenize(Trie(BoSyl, profile, main, custom))
tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་')
tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་བདེ་ལེགས།')  # to ensure we're not in a maximal match
preproc = TokChunks('བཀྲ་ཤིས་བདེ་')
preproc.serve_syls_to_trie()
tokens = tok.tokenize(preproc)
assert tokens[0].text == 'བཀྲ་ཤིས་'
assert tokens[1].text == 'བདེ་'


##########################################################################################################
# test_trie.py
##########################################################################################################

config = Config()


# def test_createtrie():
profile = 'empty'
main, custom = config.get_tok_data_paths(profile)
bt = Trie(BoSyl, profile, main, custom)

# the trie works as expected. but the add() method should never be used directly:
# it does not inflect entries, so the tokenizer won't work as expected.
bt.add('གྲུབ་མཐའ་', {'POS': 'NOUN'})
assert bt.has_word('གྲུབ་མཐའི་') == {'exists': False, 'data': {'_': {}}}

# use inflect_n_modify_trie() instead, to add entries
bt.inflect_n_modify_trie('གྲུབ་མཐའ་')

assert bt.has_word('གྲུབ་མཐའི་') == {'exists': True,
                                'data': {'_': {},
                                         'affixation': {'len': 2, 'type': 'gi', 'aa': True}}}

bt.inflect_n_modify_trie('ཀ་ར་', skrt=True)
assert bt.has_word('ཀ་རར་') == {'exists': True,
                              'data': {'_': {},
                                       'affixation': {'len': 1, 'type': 'la', 'aa': False},
                                       'skrt': True}}  # arrives here because skrt was True

bt.inflect_n_add_data('གྲུབ་མཐའ་\t532', 'freq')  # 'freq' is hard-coded in Trie, just as 'lemma' and 'pos' are
assert bt.has_word('གྲུབ་མཐའི་') == {'exists': True,
                                'data': {'_': {},
                                         'affixation': {'len': 2, 'type': 'gi', 'aa': True},
                                         'freq': 532}}  # freq is an int

# just like add() was not meant to be used directly, deactivate() is not
bt.deactivate('ཀ་ར་')
assert bt.has_word('ཀ་རར་')['exists'] is True

##########################################################################################################
# test_wordtokenizer.py
##########################################################################################################

# def test_get_default_lemma():
input_str = 'བཀྲ་ཤིས་བདེ་ལེགས། མཐའི་རྒྱ་མཚོར་གནས་སོ།། །།ཀཀ'
profile = 'POS'

# reconstitute all the pieces that WordTokenizer gathers
main, custom = Config().get_tok_data_paths(profile)
tok = Tokenize(Trie(BoSyl, profile, main, custom))
preproc = TokChunks(input_str)
preproc.serve_syls_to_trie()
tokens = tok.tokenize(preproc)
split_affixed(tokens)

# if __get_default_lemma() is not run, only the lemmas coming from the lemma folder will be included
# in the Token objects.
assert str(tokens[3]) == dedent("""\
                            text: "མཐ"
                            text_cleaned: "མཐ"
                            text_unaffixed: "མཐ"
                            syls: ["མཐ"]
                            char_types: |CONS|CONS|
                            chunk_type: TEXT
                            pos: OTHER
                            affix_host: True
                            syls_idx: [[0, 1]]
                            start: 18
                            len: 2

                            """)
assert tokens[3].lemma == ''

assert str(tokens[4]) == dedent("""\
                            text: "འི་"
                            text_cleaned: "འི་"
                            text_unaffixed: "འི་"
                            syls: ["འི"]
                            char_types: |CONS|VOW|TSEK|
                            chunk_type: TEXT
                            pos: PART
                            affix: True
                            syls_idx: [[0, 1]]
                            start: 20
                            len: 3

                            """)
assert tokens[4].lemma == ''

# regular words also have no lemmas
assert tokens[0].lemma == ''

# doing the same thing using WordTokenizer, which will apply its __get_default_lemma() method
# the profile is the same, so no lemma comes from the trie content files.
wt = WordTokenizer(profile)
tokens = wt.tokenize(input_str)

# the lemma is Token.text_unaffixed with an extra འ and/or a tsek where required
assert str(tokens[3]) == dedent('''\
                            text: "མཐ"
                            text_cleaned: "མཐ"
                            text_unaffixed: "མཐ"
                            lemma: "མཐའ་"
                            syls: ["མཐ"]
                            char_types: |CONS|CONS|
                            chunk_type: TEXT
                            pos: OTHER
                            affix_host: True
                            syls_idx: [[0, 1]]
                            start: 18
                            len: 2

                            ''')
assert tokens[3].lemma == 'མཐའ་'

# for particles, WordTokenizer reads the lemmas from a file and attributes them
assert str(tokens[4]) == dedent("""\
                            text: "འི་"
                            text_cleaned: "འི་"
                            text_unaffixed: "འི་"
                            lemma: "གི་"
                            syls: ["འི"]
                            char_types: |CONS|VOW|TSEK|
                            chunk_type: TEXT
                            pos: PART
                            affix: True
                            syls_idx: [[0, 1]]
                            start: 20
                            len: 3

                            """)
assert tokens[4].lemma == 'གི་'

# for regular words, Token.text_unaffixed is simply copied
assert tokens[0].lemma == 'བཀྲ་ཤིས་'

# non-words do not have lemmas
assert tokens[10].lemma == ''
assert tokens[10].text_cleaned == 'ཀཀ་'
assert tokens[10].text_unaffixed == 'ཀཀ་'

# Token objects whose chunk_type is not 'TEXT' will be attributed no lemma.
# text_unaffixed and text_cleaned are also empty. Token.text must be retrieved
assert tokens[2].text_unaffixed == '' == tokens[2].text_cleaned

