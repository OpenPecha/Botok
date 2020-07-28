# coding: utf8
from textwrap import dedent

from botok import *


def test_get_default_lemma(wt):
    input_str = "བཀྲ་ཤིས་བདེ་ལེགས། མཐའི་རྒྱ་མཚོར་གནས་སོ།། །།ཀཀ"
    config = Config()
    profile = config.dialect_pack_path.name

    # reconstitute all the pieces that WordTokenizer gathers
    tok = Tokenize(Trie(BoSyl, profile, config.dictionary, config.adjustments))
    preproc = TokChunks(input_str)
    preproc.serve_syls_to_trie()
    tokens = tok.tokenize(preproc)
    split_affixed(tokens)

    # if __get_default_lemma() is not run, only the lemmas coming from the lemma folder will be included
    # in the Token objects.
    assert str(tokens[3]) == dedent(
        """\
                                text: "མཐ"
                                text_cleaned: "མཐ"
                                text_unaffixed: "མཐ"
                                syls: ["མཐ"]
                                senses: | pos: NOUN, freq: 45097, affixed: True |
                                char_types: |CONS|CONS|
                                chunk_type: TEXT
                                affix_host: True
                                syls_idx: [[0, 1]]
                                syls_start_end: [{'start': 0, 'end': 2}]
                                start: 18
                                len: 2

                                """
    )
    assert "lemma" not in tokens[3]["senses"][0]

    assert str(tokens[4]) == dedent(
        """\
                                text: "འི་"
                                text_cleaned: "འི་"
                                text_unaffixed: "འི་"
                                syls: ["འི"]
                                pos: PART
                                char_types: |CONS|VOW|TSEK|
                                chunk_type: TEXT
                                affix: True
                                syls_idx: [[0, 1]]
                                syls_start_end: [{'start': 2, 'end': 5}]
                                start: 20
                                len: 3

                                """
    )

    # regular words also have no lemmas
    assert "lemma" not in tokens[0]["senses"][0]

    # doing the same thing using WordTokenizer, which will apply its __get_default_lemma() method
    # the profile is the same, so no lemma comes from the trie content files.
    tokens = wt.tokenize(input_str)

    # the lemma is Token.text_unaffixed with an extra འ and/or a tsek where required
    assert str(tokens[3]) == dedent(
        """\
                                text: "མཐ"
                                text_cleaned: "མཐ"
                                text_unaffixed: "མཐ"
                                syls: ["མཐ"]
                                pos: NOUN
                                lemma: མཐའ་
                                senses: | pos: NOUN, freq: 45097, affixed: True, lemma: མཐའ་ |
                                char_types: |CONS|CONS|
                                chunk_type: TEXT
                                freq: 45097
                                affix_host: True
                                syls_idx: [[0, 1]]
                                syls_start_end: [{'start': 0, 'end': 2}]
                                start: 18
                                len: 2

                                """
    )
    assert tokens[3]["senses"][0]["lemma"] == "མཐའ་"

    # for particles, WordTokenizer reads the lemmas from a file and attributes them
    assert str(tokens[4]) == dedent(
        """\
                                text: "འི་"
                                text_cleaned: "འི་"
                                text_unaffixed: "འི་"
                                syls: ["འི"]
                                pos: PART
                                lemma: གི་
                                senses: | lemma: གི་ |
                                char_types: |CONS|VOW|TSEK|
                                chunk_type: TEXT
                                affix: True
                                syls_idx: [[0, 1]]
                                syls_start_end: [{'start': 2, 'end': 5}]
                                start: 20
                                len: 3

                                """
    )

    # for regular words, Token.text_unaffixed is simply copied
    assert tokens[0]["senses"][0]["lemma"] == "བཀྲ་ཤིས་"

    # non-words do not have lemmas
    assert "lemma" not in tokens[10]["senses"][0]
    assert tokens[10].text_cleaned == "ཀཀ་"
    assert tokens[10].text_unaffixed == "ཀཀ་"

    # Token objects whose chunk_type is not 'TEXT' will be attributed no lemma.
    # text_unaffixed and text_cleaned are also empty. Token.text must be retrieved
    assert tokens[2].text_unaffixed == "" == tokens[2].text_cleaned


def test_spaces_as_punct(wt):
    input_str = "བ ཀྲ་ཤིས་ བདེ་ལེགས། \nམཐའི་རྒྱ་མཚོར་ག ནས་སོ།། །།ཀཀ"
    tokens = wt.tokenize(input_str, spaces_as_punct=True)
    assert tokens[0].text == "བ"
    assert tokens[1].text == " "
    assert tokens[2].text == "ཀྲ་"
    assert tokens[8].text == " \n"
