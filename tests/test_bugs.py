# coding: utf8
import sys

import pytest

from botok import TokChunks, Config, Trie, BoSyl, Tokenize, Chunks, ChunkFramework


sys.path.append("../")


def test_syl_tokenize():
    instr = " མཐའི་རྒྱ་མཚོའི་གླིང་། ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ"
    preprocessed = TokChunks(instr)
    preprocessed.serve_syls_to_trie()
    config = Config()
    trie = Trie(BoSyl, config.profile, config.dictionary, config.adjustments)
    tok = Tokenize(trie)
    tokens = tok.tokenize(preprocessed)
    texts = [t.text for t in tokens]
    expected = [
        " མཐའི་",
        "རྒྱ་མཚོའི་",
        "གླིང་",
        "། ",
        "ཤི་",
        "བཀྲ་ཤིས་  ",
        "tr ",
        "བདེ་་ལེ གས",
        "། ",
        "བཀྲ་ཤིས་",
        "བདེ་ལེགས་",
        "ཀཀ",
    ]
    # current: [' མཐའི་', 'རྒྱ་མཚོའི་', '། ', 'གླིང་', 'བཀྲ་', 'ཤི་', 'tr ', 'ཤིས་  ', 'བདེ་་ལེ གས', '། ', 'བདེ་',
    #          'བཀྲ་ཤིས་', 'ཀཀ', 'ལེགས་']
    assert texts == expected


def test_num_lemmas_missing(wt):
    in_str = "སྟོང་ཕྲག་བརྒྱ་པ་སུམ་བརྒྱ་པ་བཅུ་པ་ལྔ་པ་"
    tokens = wt.tokenize(in_str)
    assert [t.lemma for t in tokens] == [
        "སྟོང་ཕྲག་",
        "བརྒྱ་པ་",
        "སུམ་བརྒྱ་པ་",
        "བཅུ་པ་",
        "ལྔ་པ་",
    ]


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


def test_segmentation_bug(wt):
    tokens = wt.tokenize("ལ་པོ་ལ་པོ་ལ་པོ་")
    assert len(tokens) == 3

    tokens = wt.tokenize("ལ་མོ་ལ་མོ་ལ་མོ་")
    assert len(tokens) == 3

    tokens = wt.tokenize("གྲོགས་པོ་གྲོགས་པོ་གྲོགས་པོ་")
    assert len(tokens) == 3

    tokens = wt.tokenize("བདག་པོ་བདག་པོ་བདག་པོ་དང་")
    assert len(tokens) == 4

    tokens = wt.tokenize("བདག་པོ་བདག་པོ་བདག་པོ་")
    assert len(tokens) == 3

    tokens = wt.tokenize(
        "བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་བདག་པོ་"
    )
    assert len(tokens) == 9


def test_keyerror_part_lemma(wt):
    tokens = wt.tokenize("ཕའིའོ།")
    assert len(tokens) == 3


def test_split_token(empty_wt):
    wt = empty_wt
    wt.tok.trie.rebuild_trie()
    wt.tok.trie.inflect_n_modify_trie("འ་")
    assert not wt.tok.trie.has_word("ར་")["exists"]


def test_missing_entries_n_bad_unaffixed(wt):
    input_str = "ཤུ་ཀ་ར་"
    tokens = wt.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ["ཤུ་", "ཀ་ར་"]
    assert tokens[0].senses
    assert tokens[1].text_unaffixed == "ཀ་ར་"


def test_multiple_spaces():
    bo_string = Chunks("ཁྱོ ད་ད  ང་")
    chunks = bo_string.make_chunks()
    chunks = bo_string.get_readable(chunks)
    assert chunks[0] == ("TEXT", "ཁྱོ ད་")
    assert chunks[1] == ("TEXT", "ད  ང་")
    assert len(chunks) == 2


def test_bug1(wt):
    string = "བ་ཀུ་"
    tokens = wt.tokenize(string, debug=True)
    assert tokens


def test_bug2(wt):
    string = "བྲ་གྲྀ་"
    tokens = wt.tokenize(string, debug=True)
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

def test_unexpected_skip_syl(wt):
    input_strs = ["དེའི་སྒོ་ནས་བསྟན་པ་དང་སེམས་ཅན་ལ་ཕན་ཐོགས་མཛད་ཚུལ།", "དེ་ཁོ་རང་ཡིན་མོད།"]
    wt.tok.trie.inflect_n_modify_trie("དང་སེམས་", deactivate=True) # To remove དང་སེམས་ from trie
    wt.tok.trie.inflect_n_modify_trie("ཡིན་མོད", deactivate=True)
    wt.tok.trie.inflect_n_modify_trie("ཕན་ཐོགས་")
    expected_strs = ["དེའི་ སྒོ་ ནས་ བསྟན་པ་ དང་ སེམས་ཅན་ ལ་ ཕན་ཐོགས་ མཛད་ ཚུལ ། ", "དེ་ ཁོ་རང་ ཡིན་ མོད ། "]
    result_strs = []
    for input_str in input_strs:
        tokens = wt.tokenize(input_str, split_affixes = False)
        result_str = ''
        for token in tokens:
            result_str += f'{token.text} '
        result_strs.append(result_str)
    assert expected_strs == result_strs


if __name__ == "__main__":
    test_split_token()
