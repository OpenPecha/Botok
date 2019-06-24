from pybo import *
from textwrap import dedent


def test_tokenize():
    profile = 'empty'
    main, custom = Config().get_tok_data_paths(profile)
    tok = Tokenize(Trie(BoSyl, profile, main, custom))
    tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་')
    tok.trie.inflect_n_add_data('བཀྲ་ཤིས་\tNOUN', 'pos')
    tok.trie.inflect_n_add_data('བཀྲ་ཤིས་\t17500', 'freq')
    tok.trie.inflect_n_modify_trie('མཐའ་')
    tok.trie.inflect_n_add_data('མཐའ་\tNOUN', 'pos')
    tokens = tok.tokenize(TokChunks('མཐའི་བཀྲ་ཤིས། ཀཀ abc མཐའི་རྒྱ་མཚོ་'))
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


def test_non_max2():
    profile = 'empty'
    main, custom = Config().get_tok_data_paths(profile)
    tok = Tokenize(Trie(BoSyl, profile, main, custom))
    tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་')
    tok.trie.inflect_n_add_data('བཀྲ་ཤིས་\tNOUN', 'pos')
    tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་བདེ་ལེགས།')  # to ensure we're not in a maximal match
    tokens = tok.tokenize(TokChunks('བཀྲ་ཤིས་བདེ་བཀྲ་'))
    assert tokens[0].text == 'བཀྲ་ཤིས་'
    assert tokens[0].pos == 'NOUN'
    assert tokens[1].text == 'བདེ་'
    assert tokens[1].pos == 'NON_WORD'
    assert tokens[2].text == 'བཀྲ་'
    assert tokens[2].pos == 'OOV'


def test_non_max_end_of_string():
    profile = 'empty'
    main, custom = Config().get_tok_data_paths(profile)
    tok = Tokenize(Trie(BoSyl, profile, main, custom))
    tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་')
    tok.trie.inflect_n_modify_trie('བཀྲ་ཤིས་བདེ་ལེགས།')  # to ensure we're not in a maximal match
    tokens = tok.tokenize(TokChunks('བཀྲ་ཤིས་བདེ་'))
    assert tokens[0].text == 'བཀྲ་ཤིས་'
    assert tokens[1].text == 'བདེ་'
