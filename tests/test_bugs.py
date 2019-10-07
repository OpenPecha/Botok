# coding: utf8
from botok import *
import sys

sys.path.append("../")
from helpers import gmd_tok


def test_no_shad_syllable():
    in_str = "ཀ འདི་ ཤི དེ་ག རེད་དོ།"
    bo_string = Chunks(in_str)
    chunks = bo_string.make_chunks()
    chunks = bo_string.get_readable(chunks)
    assert chunks == [
        ("TEXT", "ཀ "),
        ("TEXT", "འདི་ "),
        ("TEXT", "ཤི "),
        ("TEXT", "དེ་"),
        ("TEXT", "ག "),
        ("TEXT", "རེད་"),
        ("TEXT", "དོ"),
        ("PUNCT", "།"),
    ]


def test_segmentation_bug():
    tokens = gmd_tok.tokenize("ལ་པོ་ལ་པོ་ལ་པོ་")
    assert len(tokens) == 3

    tokens = gmd_tok.tokenize("ལ་མོ་ལ་མོ་ལ་མོ་")
    assert len(tokens) == 3

    tokens = gmd_tok.tokenize("གྲོགས་པོ་གྲོགས་པོ་གྲོགས་པོ་")
    assert len(tokens) == 3

    tokens = gmd_tok.tokenize("བདག་པོ་བདག་པོ་བདག་པོ་དང་")
    assert len(tokens) == 4

    tokens = gmd_tok.tokenize("བདག་པོ་བདག་པོ་བདག་པོ་")
    assert len(tokens) == 3

    tokens = gmd_tok.tokenize("བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་")
    assert len(tokens) == 9


def test_keyerror_part_lemma():
    tokens = gmd_tok.tokenize("ཕའིའོ།")
    assert len(tokens) == 3


def test_split_token():
    wt = WordTokenizer("empty")
    wt.tok.trie.rebuild_trie()
    wt.tok.trie.inflect_n_modify_trie("འ་")
    assert not wt.tok.trie.has_word("ར་")["exists"]


def test_missing_entries_n_bad_unaffixed():
    input_str = "ཤུ་ཀ་ར་"
    tokens = gmd_tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ཤུ་ཀ་", "ར་"]
    assert tokens[0].entries
    assert tokens[1].text_unaffixed == "ར་"


def test_multiple_spaces():
    bo_string = Chunks("ཁྱོ ད་ད  ང་")
    chunks = bo_string.make_chunks()
    chunks = bo_string.get_readable(chunks)
    assert chunks[0] == ("TEXT", "ཁྱོ ད་")
    assert chunks[1] == ("TEXT", "ད  ང་")
    assert len(chunks) == 2


def test_bug1():
    tok = WordTokenizer("POS")
    string = "བ་ཀུ་"
    tokens = tok.tokenize(string, debug=True)
    assert tokens


def test_bug2():
    string = "བྲ་གྲྀ་"
    tokens = gmd_tok.tokenize(string, debug=True)
    assert tokens


def test_many_tseks_in_syllable():
    input_str = " ཤི་བཀྲ་ཤིས་  བདེ་་ལ             ེ       གས་ བཀྲ་ཤིས་བདེ་ལེགས"
    cb = ChunkFramework(input_str)
    chunks = cb.syllabify()
    readable = cb.get_readable(chunks)
    assert readable == [
        ("TEXT", " ཤི་"),
        ("TEXT", "བཀྲ་"),
        ("TEXT", "ཤིས་"),
        ("TEXT", "  བདེ་་"),
        ("TEXT", "ལ             ེ       གས་"),
        ("TEXT", " བཀྲ་"),
        ("TEXT", "ཤིས་"),
        ("TEXT", "བདེ་"),
        ("TEXT", "ལེགས"),
    ]

    chunks = cb.chunk_punct()
    chunks = cb.merge_skippable_punct(chunks)
    readable = cb.get_readable(chunks)
    assert readable == [
        ("NON_PUNCT", " ཤི་བཀྲ་ཤིས་  བདེ་་ལ             ེ       གས་ བཀྲ་ཤིས་བདེ་ལེགས")
    ]

    ck = Chunks(input_str)
    chunks = ck.make_chunks()
    readable = ck.get_readable(chunks)
    assert readable == [
        ("TEXT", " ཤི་"),
        ("TEXT", "བཀྲ་"),
        ("TEXT", "ཤིས་  "),
        ("TEXT", "བདེ་་"),
        ("TEXT", "ལ             ེ       གས་ "),
        ("TEXT", "བཀྲ་"),
        ("TEXT", "ཤིས་"),
        ("TEXT", "བདེ་"),
        ("TEXT", "ལེགས"),
    ]


def test_shad_in_syllable():
    input_str = " tr བདེ་་ལེ གས། བཀྲ་"
    ck = Chunks(input_str)
    chunks = ck.make_chunks()
    readable = ck.get_readable(chunks)
    assert readable == [
        ("LATIN", " tr "),
        ("TEXT", "བདེ་་"),
        ("TEXT", "ལེ གས"),
        ("PUNCT", "། "),
        ("TEXT", "བཀྲ་"),
    ]
