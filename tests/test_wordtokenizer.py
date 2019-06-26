from textwrap import dedent

from pybo import *


def test_get_default_lemma():
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
