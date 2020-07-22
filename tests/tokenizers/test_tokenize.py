# coding: utf8
from textwrap import dedent

import pytest

from botok import *


@pytest.fixture
def empty_config():
    return Config(Path("./tests/data/empty_dialect_pack"))


def test_tokenize(empty_config, wt):
    profile = "empty"
    config = empty_config
    tok = Tokenize(Trie(BoSyl, profile, config.dictionary, config.adjustments))
    tok.trie.inflect_n_modify_trie("བཀྲ་ཤིས་")
    tok.trie.inflect_n_add_data("བཀྲ་ཤིས་\tNOUN\t\tབཀྲ་ཤིས་\t17500")
    tok.trie.inflect_n_modify_trie("མཐའ་")
    tok.trie.inflect_n_add_data("མཐའ་\tNOUN")
    in_str = "མཐའི་བཀྲ་ཤིས། ཀཀ abc མཐའི་རྒྱ་མཚོ་"
    preproc = TokChunks(in_str)
    preproc.serve_syls_to_trie()
    tokens = tok.tokenize(preproc)
    expected = dedent(
        """\
                        text: "བཀྲ་ཤིས"
                        text_cleaned: "བཀྲ་ཤིས་"
                        text_unaffixed: "བཀྲ་ཤིས་"
                        syls: ["བཀྲ", "ཤིས"]
                        senses: | pos: NOUN, freq: 17500, sense: བཀྲ་ཤིས་, affixed: False |
                        char_types: |CONS|CONS|SUB_CONS|TSEK|CONS|VOW|CONS|
                        chunk_type: TEXT
                        syls_idx: [[0, 1, 2], [4, 5, 6]]
                        syls_start_end: [{'start': 0, 'end': 4}, {'start': 4, 'end': 7}]
                        start: 5
                        len: 7

                        """
    )
    str(tokens[0])
    assert str(tokens[1]) == expected
    assert tokens[2].text == "། "
    assert tokens[2].chunk_type == "PUNCT"
    # add sense to བཀྲ་ཤིས་
    wt.tok.trie.inflect_n_add_data("བཀྲ་ཤིས་\tNOUN\t\tབཀྲ་ཤིས་\t17500")
    tokens = wt.tokenize(in_str)
    expected = dedent(
        """\
                        text: "བཀྲ་ཤིས"
                        text_cleaned: "བཀྲ་ཤིས་"
                        text_unaffixed: "བཀྲ་ཤིས་"
                        syls: ["བཀྲ", "ཤིས"]
                        pos: NOUN
                        lemma: བཀྲ་ཤིས་
                        sense: བཀྲ་ཤིས་
                        senses: | pos: NOUN, freq: 17204, affixed: False, lemma: བཀྲ་ཤིས་ | pos: NOUN, freq: 17500, sense: བཀྲ་ཤིས་, affixed: False, lemma: བཀྲ་ཤིས་ |
                        char_types: |CONS|CONS|SUB_CONS|TSEK|CONS|VOW|CONS|
                        chunk_type: TEXT
                        freq: 17500
                        syls_idx: [[0, 1, 2], [4, 5, 6]]
                        syls_start_end: [{'start': 0, 'end': 4}, {'start': 4, 'end': 7}]
                        start: 5
                        len: 7

                        """
    )
    assert str(tokens[2]) == expected


def test_non_max2(empty_config):
    profile = "empty"
    config = empty_config
    tok = Tokenize(Trie(BoSyl, profile, config.dictionary, config.adjustments))
    tok.trie.inflect_n_modify_trie("བཀྲ་ཤིས་")
    tok.trie.inflect_n_add_data("བཀྲ་ཤིས་\tNOUN")
    tok.trie.inflect_n_modify_trie(
        "བཀྲ་ཤིས་བདེ་ལེགས།"
    )  # to ensure we're not in a maximal match
    preproc = TokChunks("བཀྲ་ཤིས་བདེ་བཀྲ་")
    preproc.serve_syls_to_trie()
    tokens = tok.tokenize(preproc)
    assert tokens[0].text == "བཀྲ་ཤིས་"
    assert tokens[0]["senses"][0]["pos"] == "NOUN"
    assert tokens[1].text == "བདེ་"
    assert tokens[1]["senses"][0]["pos"] == "NON_WORD"
    assert tokens[2].text == "བཀྲ་"
    assert tokens[2]["senses"][0]["pos"] == "NO_POS"


def test_non_max_end_of_string(empty_config):
    profile = "empty"
    config = empty_config
    tok = Tokenize(Trie(BoSyl, profile, config.dictionary, config.adjustments))
    tok.trie.inflect_n_modify_trie("བཀྲ་ཤིས་")
    tok.trie.inflect_n_modify_trie(
        "བཀྲ་ཤིས་བདེ་ལེགས།"
    )  # to ensure we're not in a maximal match
    preproc = TokChunks("བཀྲ་ཤིས་བདེ་")
    preproc.serve_syls_to_trie()
    tokens = tok.tokenize(preproc)
    assert tokens[0].text == "བཀྲ་ཤིས་"
    assert tokens[1].text == "བདེ་"


if __name__ == "__main__":
    test_non_max2()
