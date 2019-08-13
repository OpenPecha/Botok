# coding: utf8
from pybo import *
from textwrap import dedent


def test_tokenize():
    profile = 'empty'
    main, custom = Config().get_tok_data_paths(profile)
    tok = Tokenize(Trie(BoSyl, profile, main, custom))
    tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་')
    tok.trie.inflect_n_add_data('བཀྲ་ཤིས་\t\tNOUN\t17500')
    tok.trie.inflect_n_modify_trie('མཐའ་')
    tok.trie.inflect_n_add_data('མཐའ་\t\tNOUN')
    preproc = TokChunks('མཐའི་བཀྲ་ཤིས། ཀཀ abc མཐའི་རྒྱ་མཚོ་')
    preproc.serve_syls_to_trie()
    tokens = tok.tokenize(preproc)
    expected = dedent("""\
                        text: "བཀྲ་ཤིས"
                        text_cleaned: "བཀྲ་ཤིས་"
                        text_unaffixed: "བཀྲ་ཤིས་"
                        syls: ["བཀྲ", "ཤིས"]
                        meanings: | pos: NOUN, freq: 17500, affixed: False |
                        char_types: |CONS|CONS|SUB_CONS|TSEK|CONS|VOW|CONS|
                        chunk_type: TEXT
                        syls_idx: [[0, 1, 2], [4, 5, 6]]
                        start: 5
                        len: 7
                        
                        """)
    str(tokens[0])
    assert str(tokens[1]) == expected
    assert tokens[2].text == '། '
    assert tokens[2].chunk_type == 'PUNCT'


def test_non_max2():
    profile = 'empty'
    main, custom = Config().get_tok_data_paths(profile)
    tok = Tokenize(Trie(BoSyl, profile, main, custom))
    tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་')
    tok.trie.inflect_n_add_data('བཀྲ་ཤིས་\t\tNOUN')
    tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་བདེ་ལེགས།')  # to ensure we're not in a maximal match
    preproc = TokChunks('བཀྲ་ཤིས་བདེ་བཀྲ་')
    preproc.serve_syls_to_trie()
    tokens = tok.tokenize(preproc)
    assert tokens[0].text == 'བཀྲ་ཤིས་'
    assert tokens[0]['meanings'][0]['pos'] == 'NOUN'
    assert tokens[1].text == 'བདེ་'
    assert tokens[1]['meanings'][0]['pos'] == 'NON_WORD'
    assert tokens[2].text == 'བཀྲ་'
    assert tokens[2]['meanings'][0]['pos'] == 'OOV'


def test_non_max_end_of_string():
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
