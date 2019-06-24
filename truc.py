from pybo import *
from textwrap import dedent

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
                start: 5
                len: 7
                
                """)
str(tokens[0])
assert str(tokens[1]) == expected
assert tokens[2].text == '། '
assert tokens[2].chunk_type == 'PUNCT'
