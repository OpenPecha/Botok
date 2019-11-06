# coding: utf8
from botok import *
from pathlib import Path
from pytest import raises
from textwrap import dedent

# all the tests showcasing functionality from the test suite are copied here

##########################################################################################################
# test_basictrie.py
##########################################################################################################

trie = BasicTrie()

# populate the basic trie
words = "hello goo good goodbye help gerald gold tea ted team to too tom stan standard money"
for w in words.split():
    trie.add(w)

# test word existence. has_word() is not used in pybo. it is only there for testing purposes
trie.has_word("goodbye")

# add content to data
trie.add_data("goodbye", {"pos": "NOUN"})
trie.has_word("goodbye")

# adding an empty dict to show it does not replace existing content but updates it
trie.add_data("goodbye", {})
trie.has_word("goodbye")

# by default, overwrites existing dict values
trie.add_data("goodbye", {"pos": "VERB", "lemma": "goodbye"})
trie.has_word("goodbye")

# deactivates an entry, only modifying the Node.leaf value (bool) instead of removing it from the trie.
trie.deactivate("goodbye")
trie.has_word("goodbye")

# reactivates the entry
trie.deactivate("goodbye", rev=True)
trie.has_word("goodbye")

# walk() is used to externalize the walking of the trie
current_node = None  # setting an empty variable for the current node
for char in "goodbye":
    current_node = trie.walk(char, current_node)

print(current_node.label)
print(current_node.leaf)
print(current_node.data)

##########################################################################################################
# test_bostring.py
##########################################################################################################

bo_str = "བཀྲ་ཤིས་ ༡༢༣ tr  就到 郊外玩བདེ་ལེགས།"
m = CharMarkers

"""Testing whether, at a given index, the char category corresponds to what is expected."""
bs = BoString(bo_str)

idx = 0
print(bo_str[idx])
print(bs.base_structure[idx])

idx = 2
print(bo_str[idx])
print(bs.base_structure[idx])

idx = 7
print(bo_str[idx])
print(bs.base_structure[idx])

idx = 9
print(bo_str[idx])
print(bs.base_structure[idx])

idx = 13
print(bo_str[idx])
print(bs.base_structure[idx])

idx = 17
print(bo_str[idx])
print(bs.base_structure[idx])

##########################################################################################################
# test_bosyl.py
##########################################################################################################

bs = BoSyl()

# is_affixable() Vs. SylComponents.is_thame()
bs.is_thame("ཀུན")
bs.is_affixable("ཀུན")
bs.is_thame("དེའིའམ")
bs.is_affixable("དེའིའམ")
bs.is_thame("དེའི")
bs.is_affixable("དེའི")
bs.is_thame("ང")
bs.is_affixable("ང")

# get_all_affixed()
bs.get_all_affixed("ང")

bs.get_all_affixed("མཐའ")

bs.get_all_affixed("ཀུན")

##########################################################################################################
# test_chunkframework.py
##########################################################################################################
c = ChunkMarkers

# def test_bo_nonbo():
string = 'བཀྲ་་ཤིས་བདེ་ལེགས། 23PIEIUZLDVéjoldvép«»("«»%='
cb = ChunkFramework(string)
chunks = cb.chunk_bo_chars()

cb.get_readable(chunks)


# def test_punct_nonpunct():
string = "༆ བཀྲ་ཤིས་བདེ་ལེགས།། །།"
cb = ChunkFramework(string)
chunks = cb.chunk_punct()

cb.get_readable(chunks)

# def test_sym_nonsym():
string = "བཀྲ་ཤིས་བདེ་ལེགས། ༪༫༝༜༛༚༇༆"
cb = ChunkFramework(string)
chunks = cb.chunk_symbol()

cb.get_readable(chunks)


# def test_num_nonnum():
string = "བཀྲ་ཤིས་བདེ་ལེགས།  ༡༢༣༠༩༨"
cb = ChunkFramework(string)
chunks = cb.chunk_number()

cb.get_readable(chunks)


# def test_space_nonspace():
string = "བཀྲ་ཤིས་བདེ་ལེགས།   །བཀྲ་ཤིས་བདེ་ལེགས།"
cb = ChunkFramework(string)
chunks = cb.chunk_spaces()

cb.get_readable(chunks)


# def test_text():
string = "བཀྲ་ཤིས་བདེ་ལེགས"
cb = ChunkFramework(string)
chunks = cb.syllabify()

cb.get_readable(chunks)


# def test_latin():
string = "བཀྲ་ཤིས་བདེ་ལེགས This is a test."
cb = ChunkFramework(string)
chunks = cb.chunk_latin()

cb.get_readable(chunks)


# def test_cjk():
string = "བཀྲ་ཤིས་བདེ་ལེགས 这是  什么"
cb = ChunkFramework(string)
chunks = cb.chunk_cjk()

cb.get_readable(chunks)


# def test_other():
string = "བཀྲ་ཤིས་བདེ་ལེགས กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"
cb = ChunkFramework(string)
chunks = cb.chunk_bo_chars()

cb.get_readable(chunks)


# def test_full_example():
# Follows the order implemented in Chunks
string = (
    '༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། 23PIEIUZLDVéjoldvép«»("«»%= ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ '
    "This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"
)
cb = ChunkFramework(string)

# BO / OTHER
chunks = cb.chunk_bo_chars()
chunks = cb.clean_chunks(chunks)
cb.get_readable(chunks)

# BO / PUNCT
chunks = cb.pipe_chunk(chunks, cb.chunk_punct, c.BO.value, c.PUNCT.value)
chunks = cb.clean_chunks(chunks)
cb.get_readable(chunks)

# BO / NUM
chunks = cb.pipe_chunk(chunks, cb.chunk_number, c.BO.value, c.NUM.value)
chunks = cb.clean_chunks(chunks)
cb.get_readable(chunks)

# BO / SYM
chunks = cb.pipe_chunk(chunks, cb.chunk_symbol, c.BO.value, c.SYM.value)
chunks = cb.clean_chunks(chunks)
cb.get_readable(chunks)

# TEXT
chunks = cb.pipe_chunk(chunks, cb.syllabify, c.BO.value, c.TEXT.value)
chunks = cb.clean_chunks(chunks)
cb.get_readable(chunks)

# OTHER / CJK
chunks = cb.pipe_chunk(chunks, cb.chunk_cjk, c.OTHER.value, c.CJK.value)
chunks = cb.clean_chunks(chunks)
cb.get_readable(chunks)

# OTHER / LATIN
chunks = cb.pipe_chunk(chunks, cb.chunk_latin, c.OTHER.value, c.LATIN.value)
chunks = cb.clean_chunks(chunks)
cb.get_readable(chunks)

##########################################################################################################
# test_chunks.py
##########################################################################################################

string = (
    '༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། 23PIEIUZLDVéjoldvép«»("«»%= ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ '
    "This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"
)


# def test_chunks():
c = Chunks(string)
chunks = c.make_chunks()
c.get_readable(chunks)


# def test_tokchunks():
c = TokChunks(string)
c.serve_syls_to_trie()
# generate what the tokenizer will ingest
chunks = c.chunks

# the second element of each tuple is the chunk from Chunks
readable = [(a[0], c.get_readable([a[1]])[0]) for a in chunks]

# just for the fun of it: get the cleaned syllable as it is done in the Tokenizer
chunks = [
    "".join([string[c] for c in chars]) + TSEK for chars, chunk in chunks if chars
]

##########################################################################################################
# test_chunktokenizer.py
##########################################################################################################

# def test_chunktokenizer():
input_str = (
    " ཤི་བཀྲ་ཤིས་  བདེ་་ལ             ེ       གས་ "
    'བཀྲ་ཤིས་བདེ་ལེགས ༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། 23PIEIUZLDVéjoldvép«»("«»%= ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ '
    "This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"
)
st = ChunkTokenizer(input_str)
tokens = st.tokenize()

##########################################################################################################
# test_config
##########################################################################################################

# def test_config():
config = Config()

# default config filename
print(config.filename.name)

# paths for trie content
main, custom = config.get_tok_data_paths("POS")
# each profile contains one or more sections
print([m for m in main])
# each element in a Path object leading to a resource file
isinstance(main["entry_data"][0], Path)

# custom files to overwrite the existing trie can be added as follows
len(custom)
main, custom = config.get_tok_data_paths(
    "POS", modifs=Path(__file__).parent / "tests/trie_data/"
)
print([c for c in custom])
print([t.parts[-1] for t in Path(Path(__file__).parent / "tests/trie_data/").glob("*")])

# overwriting the main profile
main, custom = config.get_tok_data_paths(
    Path(__file__).parent / "tests/trie_data/", mode="custom"
)
print([m for m in main])

config.get_adj_data_paths("basic", modifs=Path(__file__).parent / "tests/trie_data/")

##########################################################################################################
# test_splitaffixed.py
##########################################################################################################

# def test_split_token():
wt = WordTokenizer("empty")
wt.tok.trie.rebuild_trie()
wt.tok.trie.inflect_n_modify_trie("བདེ་བ་")
wt.tok.trie.inflect_n_add_data("བདེ་བ་\tNOUN")
wt.tok.trie.inflect_n_modify_trie("གཏན་")
wt.tok.trie.inflect_n_add_data("གཏན་\tNOUN")
wt.tok.trie.inflect_n_modify_trie("གྱི་")
wt.tok.trie.inflect_n_add_data("གྱི་\tPART\tགི")
tokens = wt.tokenize("གཏན་གྱི་བདེ་བའི་རྒྱུ།", split_affixes=False)
len(tokens)
print(tokens[2].text)
tokens = wt.tokenize("གཏན་གྱི་བདེ་བའི་རྒྱུ།")
len(tokens)
print(tokens[2].text)
print(tokens[3].text)

##########################################################################################################
# test_sylcomponents.py
##########################################################################################################

# def test_components():
sc = SylComponents()

# A) get_parts()
# 1. (prefix+main-stack, vowel+suffixes)
sc.get_parts("བཀྲིས")
# 2. (exceptions, 'x')
sc.get_parts("མདྲོན")
# 3. a list of solutions if there is more than one (not yet encountered)
# 4. None if the syllable is not wellformed
sc.get_parts("ཀཀ")

# B) get_mingzhi()
sc.get_mingzhi("བསྒྲུབས")
# the mingzhi that will serve for the particle agreement:
sc.get_mingzhi("ཁྱེའུར")
# None if more than one solution from get_parts() (not yet encountered)

# support for dadrag
sc.get_mingzhi("ཀུནད")

# dadrag normalize
sc.normalize_dadrag("ཀུནད")

# C) get_info()
# 1. 'dadrag'
# A syllable that historically received a "da" second suffix.
# As for now, the list contains ["ཀུན", "ཤིན", "འོན"] (See pybo/resources/SylComponents.json)
sc.get_info("ཀུན")
# 2. 'thame'
# A syllable that has the potential of hosting an affixed particle.
# Will be returned for all such syls, whether or not a particle is affixed.
sc.get_info("དེའིའམ")
sc.get_info("དེའི")
# 3 the syllable itself in all other cases
sc.get_info("ང")
sc.get_info("རྒྱལ")

# D) is_thame()
# True if the syllabe is affixable or is already affixed, False otherwise
sc.is_thame("ཀུན")
sc.is_thame("དེའིའམ")
sc.is_thame("དེའི")
sc.is_thame("ང")

##########################################################################################################
# test_token.py
##########################################################################################################

# def test_token():
t = Token()
t.text = "test"
# Token supports access to attributes in two ways (required for CQL found in third_party/cql.py)
print(t.text)
print(t._)

# setting existing attributes like dicts is supported
attrs = {"pos": "NOUN", "freq": "123", "len": 4}
for k, v in attrs.items():
    t[k] = v
str(t)

# raises an error when trying to add a new attribute
with raises(AttributeError, match=r"Token objects don't have .* as attribute"):
    t["non_attr"] = "test"

##########################################################################################################
# test_tokenize.py
##########################################################################################################

# def test_tokenize():
profile = "empty"
main, custom = Config().get_tok_data_paths(profile)
tok = Tokenize(Trie(BoSyl, profile, main, custom))
tok.trie.inflect_n_modify_trie("བཀྲ་ཤིས་")
tok.trie.inflect_n_add_data("བཀྲ་ཤིས་\tNOUN\t\t\t17500")
tok.trie.inflect_n_modify_trie("མཐའ་")
tok.trie.inflect_n_add_data("མཐའ་\tNOUN")
preproc = TokChunks("མཐའི་བཀྲ་ཤིས། ཀཀ abc མཐའི་རྒྱ་མཚོ་")
preproc.serve_syls_to_trie()
tokens = tok.tokenize(preproc)
expected = dedent(
    """\
                    text: "བཀྲ་ཤིས"
                    text_cleaned: "བཀྲ་ཤིས་"
                    text_unaffixed: "བཀྲ་ཤིས་"
                    syls: ["བཀྲ", "ཤིས"]
                    entries: | pos: NOUN, freq: 17500, affixed: False |
                    char_types: |CONS|CONS|SUB_CONS|TSEK|CONS|VOW|CONS|
                    chunk_type: TEXT
                    syls_idx: [[0, 1, 2], [4, 5, 6]]
                    start: 5
                    len: 7

                    """
)
str(tokens[0])
str(tokens[1])
print(tokens[2].text)
print(tokens[2].chunk_type)


# def test_non_max2():
profile = "empty"
main, custom = Config().get_tok_data_paths(profile)
tok = Tokenize(Trie(BoSyl, profile, main, custom))
tok.trie.inflect_n_modify_trie("བཀྲ་ཤིས་")
tok.trie.inflect_n_add_data("བཀྲ་ཤིས་\tNOUN")
tok.trie.inflect_n_modify_trie(
    "བཀྲ་ཤིས་བདེ་ལེགས།"
)  # to ensure we're not in a maximal match
preproc = TokChunks("བཀྲ་ཤིས་བདེ་བཀྲ་")
preproc.serve_syls_to_trie()
tokens = tok.tokenize(preproc)
print(tokens[0].text)
print(tokens[0]["entries"][0]["pos"])
print(tokens[1].text)
print(tokens[1]["entries"][0]["pos"])
print(tokens[2].text)
print(tokens[2]["entries"][0]["pos"])


# def test_non_max_end_of_string():
profile = "empty"
main, custom = Config().get_tok_data_paths(profile)
tok = Tokenize(Trie(BoSyl, profile, main, custom))
tok.trie.inflect_n_modify_trie("བཀྲ་ཤིས་")
tok.trie.inflect_n_modify_trie(
    "བཀྲ་ཤིས་བདེ་ལེགས།"
)  # to ensure we're not in a maximal match
preproc = TokChunks("བཀྲ་ཤིས་བདེ་")
preproc.serve_syls_to_trie()
tokens = tok.tokenize(preproc)
print(tokens[0].text)
print(tokens[1].text)


##########################################################################################################
# test_trie.py
##########################################################################################################

config = Config()


# def test_createtrie():
profile = "empty"
modifs = Path(__file__).parent / "tests" / "trie_data"
main, custom = config.get_tok_data_paths(profile, modifs=modifs)
bt = Trie(BoSyl, profile, main, custom)

# the trie works as expected. but the add() method should never be used directly:
# it does not inflect entries, so the tokenizer won't work as expected.
# be careful only to use it with words that can't ever be inflected, like case particles.
bt.add("གྲུབ་མཐའ་", {"pos": "NOUN"})
bt.has_word("གྲུབ་མཐའི་")

# use inflect_n_modify_trie() instead, to add entries
bt.inflect_n_modify_trie("གྲུབ་མཐའ་")

bt.has_word("གྲུབ་མཐའི་")

bt.inflect_n_modify_trie("ཀ་ར་", skrt=True)
bt.has_word("ཀ་རར་")

bt.inflect_n_add_data(
    "གྲུབ་མཐའ་\t\t\t\t532"
)  # 'freq' is hard-coded in Trie, just as 'lemma' and 'pos' are
bt.has_word("གྲུབ་མཐའི་")

# just like add() was not meant to be used directly, deactivate() is not
# instead, use bt.inflect_n_modify_trie("word", deactivate=True)
bt.deactivate("ཀ་ར་")
print(bt.has_word("ཀ་རར་")["exists"])

profile = "POS"
main, custom = config.get_tok_data_paths(profile, modifs=modifs)
bt = Trie(BoSyl, profile, main, custom)

res = bt.has_word("ལྟར་")
print(res["data"]["entries"])
print(res["data"]["entries"])

##########################################################################################################
# test_wordtokenizer.py
##########################################################################################################

# def test_get_default_lemma():
input_str = "བཀྲ་ཤིས་བདེ་ལེགས། མཐའི་རྒྱ་མཚོར་གནས་སོ།། །།ཀཀ"
profile = "POS"

# reconstitute all the pieces that WordTokenizer gathers
main, custom = Config().get_tok_data_paths(profile)
tok = Tokenize(Trie(BoSyl, profile, main, custom))
preproc = TokChunks(input_str)
preproc.serve_syls_to_trie()
tokens = tok.tokenize(preproc)
split_affixed(tokens)

# if __get_default_lemma() is not run, only the lemmas coming from the lemma folder will be included
# in the Token objects.
str(tokens[3])
print(tokens[3]["entries"][0])

str(tokens[4])

# regular words also have no lemmas
print(tokens[0]["entries"][0])

# doing the same thing using WordTokenizer, which will apply its __get_default_lemma() method
# the profile is the same, so no lemma comes from the trie content files.
pos_tok = WordTokenizer(profile)
tokens = pos_tok.tokenize(input_str)

# the lemma is Token.text_unaffixed with an extra འ and/or a tsek where required
str(tokens[3])
print(tokens[3]["entries"][0]["lemma"])

# for particles, WordTokenizer reads the lemmas from a file and attributes them
str(tokens[4])
print(tokens[4]["entries"][0]["lemma"])

# for regular words, Token.text_unaffixed is simply copied
print(tokens[0]["entries"][0])

# non-words do not have lemmas
print(tokens[10]["entries"][0])
print(tokens[10].text_cleaned)
print(tokens[10].text_unaffixed)

# Token objects whose chunk_type is not 'TEXT' will be attributed no lemma.
# text_unaffixed and text_cleaned are also empty. Token.text must be retrieved
print(tokens[2].text_unaffixed)
print(tokens[2].text_cleaned)

##########################################################################################################
# test_matchers.py
##########################################################################################################

# coding: utf8
from botok import *
from pathlib import Path

rules_path = Path(__file__).parent / "tests" / "resources"
main, custom = Config().get_adj_data_paths("basic", rules_path)


input_str = " མཐའི་རྒྱ་མཚོའི་གླིང་། ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ"
tokens = pos_tok.tokenize(input_str, split_affixes=False)

# IMPORTANT: all the tests have merely been adapted after refactorisation.
# They should be split in tests per file that also show the expected behaviour of every matcher.


# def test_cql_query():
query = '[text="ན"] []'
q = Query(query)
print(q)

test = [
    {"word": "This", "lemma": "this", "tag": "Det"},
    {"word": "is", "lemma": "be", "tag": "Verb"},
    {"word": "it", "lemma": "it", "tag": "Pron"},
    {"word": ".", "lemma": ".", "tag": "Punct"},
]
q = '[lemma="this" & tag="Det"] [tag!="ADJ"]'

matcher = CQLMatcher(q)
matched = matcher.match(test)
print(matched)

# def test_cql():
query = '[pos="NOUN" & text!=""] []'
matcher = CQLMatcher(query)
slices = matcher.match(tokens)
slice_strings = [
    tuple([tokens[i].text for i in range(start, end + 1)]) for start, end in slices
]


# def test_token_split():
ts = TokenSplit(
    tokens[3],
    1,
    token_changes='[chunk_type="SPACE" & pos="PUNCT" & affix_host="False"] []',
)
first, second = ts.split()
print(first.chunk_type)
print(first.pos)


# def test_token_merge():
tm = TokenMerge(tokens[0], tokens[1])
merged = tm.merge()
print(merged)


# def test_match_split():
match_query = '[pos="NOUN" & text!=""] []'
replace_idx = 1  # slot number in match query
split_idx = 1  # char index in token.content where split should occur
replace = '[chunk_type="XXX" & pos="xxx"] []'

sm = SplittingMatcher(match_query, replace_idx, split_idx, tokens, replace)
split_tokens = sm.split_on_matches()
len(tokens)
len(split_tokens)


# def test_match_merge():
match_query = '[pos="NOUN" & text!=""] []'
replace_idx = 1  # slot number in match query
replace = '[chunk_type="XXX" & pos="xxx"]'

mm = MergingMatcher(match_query, replace_idx, tokens, replace)
merged_tokens = mm.merge_on_matches()
len(tokens)
len(merged_tokens)


# def test_match_replace():
match_query = '[pos="NOUN" & text!=""] []'
replace_idx = 1
replace = '[chunk_type="XXX" & pos="xxx"]'

ReplacingMatcher(match_query, replace_idx, tokens, replace).replace_on_matches()
len(tokens)
print(tokens[1].pos)
print(tokens[2].pos)


# def test_adjust_tokens():
string = "ལ་ལ་ལ་ལ་ལ་བ་ཡོད།"
token_list = pos_tok.tokenize(string, split_affixes=False)
at = AdjustTokens(main=main, custom=custom)
adjusted = at.adjust(token_list)
print(token_list[0].text)
print(token_list[1].text)

print(adjusted[0].text)
print(adjusted[0].pos)
print(adjusted[1].text)
print(adjusted[1].pos)
print(adjusted[2].text)
print(adjusted[2].pos)


# def test_last_token():
token1 = Token()
token1.pos = "NOUN"

token2 = Token()
token2.pos = "VERB"

matcher = CQLMatcher('[pos="NOUN"]')
slices = matcher.match([token1, token2])

matcher = CQLMatcher('[pos="VERB"]')
print(matcher.match([token1, token2]))


# def test_mergedagdra():
token_list = pos_tok.tokenize("བཀྲ་ཤིས་-པ་")
token_list = [
    t for t in token_list if t.text != "-"
]  # remove the "-" inserted to ensure we have two tokens
mp = MergeDagdra()
mp.merge(token_list)
len(token_list)
print(token_list[0].text)

token_list = pos_tok.tokenize("བཀྲ་ཤིས་-པའོ།")
token_list = [
    t for t in token_list if t.text != "-"
]  # remove the "-" inserted to ensure we have two tokens
mp.merge(token_list)
len(token_list)
print(token_list[0].text)


##########################################################################################################
# test_text.py
##########################################################################################################


in_str = "ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ། མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།། །།མཁའ།"


# def test_simple_usage():
# instanciating the Text object
t = Text(in_str)

# get builtin properties
print(t.tokenize_chunks_plaintext)

print(t.tokenize_on_spaces)

print(t.tokenize_words_raw_text)

t_lines = Text(in_str + "\n" + in_str)
print(t_lines.tokenize_words_raw_lines)

# note: see in the console that the trie was only loaded once: lru_cache ensures we only load it once,
# even over different instances of Text class

print(t.list_word_types)
# calculates the frequency of words in the text

# now, run Text on a file. (using tokenize_chunks_plaintext property to test the feature because it is fast)
in_file = Path(__file__).parent / "tests" / "resources" / "test_file_to_tokenize.txt"
t = Text(in_file)
print(t.tokenize_chunks_plaintext)
out_file = in_file.parent / (
    in_file.stem + "_pybo" + in_file.suffix
)  # see inside code for naming convention
out_file.is_file()
out_file.read_text()
# the file has been written

# Test sentence and paragraph tokenizer
text = (
    "བཀུར་བར་མི་འགྱུར་ཞིང༌། །བརྙས་བཅོས་མི་སྙན་རྗོད་པར་བྱེད། །དབང་དང་འབྱོར་པ་ལྡན་པ་ཡི། །རྒྱལ་རིགས་ཕལ་ཆེར་བག་མེད་པས། །"
    "མྱོས་པའི་གླང་ཆེན་བཞིན་དུ་འཁྱམས། །དེ་ཡི་འཁོར་ཀྱང་དེ་འདྲར་འགྱུར། །གཞན་ཡང་རྒྱལ་པོ་རྒྱལ་རིགས་ཀྱི། །སྤྱོད་པ་བཟང་ངན་ཅི་འདྲ་བ། །"
    "དེ་འདྲའི་ཚུལ་ལ་བལྟས་ནས་སུ། །འབངས་རྣམས་དེ་དང་དེ་འདྲ་སྟེ། །རྒྱལ་པོ་ནོར་ལ་བརྐམས་གྱུར་ན། །ནོར་གྱིས་རྒྱལ་ཁྲིམས་བསླུ་བར་རྩོམ། །"
    "མི་བདག་གཡེམ་ལ་དགའ་གྱུར་ན། །འཕྱོན་མའི་ཚོགས་རྣམས་མགོ་འཕང་མཐོ། །ཕྲ་མར་ཉན་ན་དབྱེན་གྱིས་གཏོར། །བརྟག་དཔྱད་མི་ཤེས་རྫུན་གྱིས་སླུ། །"
    "ང་ལོ་ཡང་ན་ཀུན་གྱིས་བསྐྱོད། །ངོ་དགར་བརྩི་ན་ཟོལ་ཚིག་སྨྲ། །དེ་དང་དེ་ལ་སོགས་པ་ཡི། །མི་བདག་དེ་ལ་གང་གང་གིས། །"
    "བསླུ་བར་རུང་བའི་སྐབས་མཐོང་ན། །གཡོན་ཅན་ཚོགས་ཀྱིས་ཐབས་དེ་སེམས། །མི་རྣམས་རང་འདོད་སྣ་ཚོགས་ལ། །རྒྱལ་པོ་ཀུན་གྱི་ཐུན་མོང་ཕྱིར། །"
    "རྒྱལ་པོས་བསམ་གཞིགས་མ་བྱས་ན། །ཐ་མར་རྒྱལ་སྲིད་འཇིག་པར་འགྱུར། །ཆེན་པོའི་གོ་སར་གནས་པ་ལ། །སྐྱོན་ཀྱང་ཡོན་ཏན་ཡིན་ཚུལ་དུ། །"
    "འཁོར་ངན་རྣམས་ཀྱིས་ངོ་བསྟོད་སྨྲ། །དེ་ཕྱིར་སྐྱོན་ཡོན་ཤེས་པ་དཀའ། །ལྷག་པར་རྩོད་ལྡན་སྙིགས་མའི་ཚེ། །འཁོར་གྱི་ནང་ན་མ་རབས་མང༌། །"
    "སྐྱོན་ཡང་ཡོན་ཏན་ལྟར་མཐོང་ལ། །རང་འདོད་ཆེ་ཞིང་རྒྱལ་པོ་བསླུ། །ཆུས་དང་འཁོར་གྱི་བདེ་ཐབས་ལ། །བསམ་གཞིགས་བྱེད་པ་དཀོན་པའི་ཕྱིར། །"
    "རྒྱལ་པོས་ལེགས་པར་དཔྱད་ནས་སུ། །བདེན་པའི་ངག་ལས་"
)
t = Text(text)
print(t.tokenize_sentences_plaintext)

print(t.tokenize_paragraph_plaintext)

# def test_advanced_features():
########################################
# 1. instanciating with a custom profile
t = Text(in_str, tok_params={"profile": "GMD"})
print(t.tokenize_words_raw_text)

# instanciating with a custom profile. tok_params can receive all the supported arguments of WordTokenizer
tt = Text(
    in_str,
    tok_params={
        "profile": "GMD",
        "modifs": Path(__file__).parent / "tests" / "trie_data",
    },
)
print(tt.tokenize_words_raw_text)

#############################
# 2. adding a custom pipeline
def custom_tokenizer(string):
    return string.split(" ")  # simply reimplementing the space-tokenizer


def custom_modifier(tokens):
    return ["__" + t + "__" for t in tokens]


def custom_formatter(tokens):
    return "\n".join(tokens)


t = Text(in_str)
t.custom_pipeline("dummy", custom_tokenizer, custom_modifier, custom_formatter)
# note how you pass the names of the functions you declare, without parens

t.custom_pipeline("dummy", "word_tok", "words_error_concs", "basic_concs")

t.custom_pipeline("dummy", "word_tok", "words_error_types", "stats_types")
