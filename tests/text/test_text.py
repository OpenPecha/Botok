# coding: utf8
from pathlib import Path
from textwrap import dedent

import pytest

from botok import *

in_str = """ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་  tr
བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ།
མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།། །།མཁའ།"""


def test_simple_usage():
    # instanciating the Text object
    t = Text(in_str)

    # get builtin properties
    chunks = t.tokenize_chunks_plaintext
    assert (
        chunks
        == "ལེ_གས །_ བཀྲ་ ཤིས་ མཐའི་ _༆_ ཤི་ བཀྲ་ ཤིས་__ tr\n བདེ་་ ལེ_གས །_ བཀྲ་ ཤིས་ བདེ་ ལེགས་ ༡༢༣ ཀཀ །\n མཐའི་ རྒྱ་ མཚོར་ གནས་ པའི་ ཉས་ ཆུ་ འཐུང་ །།_།། མཁའ །"
    )

    spaces = t.tokenize_on_spaces
    assert (
        spaces
        == "ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་ tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ། མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།། །།མཁའ།"
    )
    # re-joins with a space, so it seems to only have replaces multiple spaces by single space (done in preprocessing)

    words = t.tokenize_words_raw_text
    assert (
        words
        == "ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་_ tr_ བདེ་་ལེ_གས །_ བཀྲ་ཤིས་ བདེ་ལེགས་ ༡༢༣ ཀཀ །_ མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །"
    )
    # replaces all spaces in the input with "_" so the output is splittable with a space

    t_lines = Text(in_str + "\n" + in_str)
    with_lines = t_lines.tokenize_words_raw_lines
    assert (
        with_lines == "ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་__ tr\n "
        "བདེ་་ལེ_གས །_ བཀྲ་ཤིས་ བདེ་ལེགས་ ༡༢༣ ཀཀ །\n "
        "མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །\n "
        "ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་__ tr\n "
        "བདེ་་ལེ_གས །_ བཀྲ་ཤིས་ བདེ་ལེགས་ ༡༢༣ ཀཀ །\n "
        "མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །"
    )
    # keeps returns from the input (only do this if you know words are not split over two lines)

    # note: see in the console that the trie was only loaded once: lru_cache ensures we only load it once,
    # even over different instances of Text class

    types = t.list_word_types
    assert (
        types == "འི་	3\n"
        "། 	2\n"
        "བཀྲ་ཤིས་	2\n"
        "མཐ	2\n"
        "ལེ གས	1\n"
        " ༆ 	1\n"
        "ཤི་	1\n"
        "བཀྲ་ཤིས་  	1\n"
        "tr\\n	1\n"
        "བདེ་་ལེ གས	1\n"
        "བདེ་ལེགས་	1\n"
        "༡༢༣	1\n"
        "ཀཀ	1\n"
        "།\\n	1\n"
        "རྒྱ་མཚོ	1\n"
        "ར་	1\n"
        "གནས་པ	1\n"
        "ཉ	1\n"
        "ས་	1\n"
        "ཆུ་	1\n"
        "འཐུང་	1\n"
        "།། །།	1\n"
        "མཁའ	1\n"
        "།	1"
    )
    # calculates the frequency of words in the text

    # now, run Text on a file. (using tokenize_chunks_plaintext property to test the feature because it is fast)
    in_file = Path("./tests") / "resources" / "test_file_to_tokenize.txt"
    t = Text(in_file)
    t.tokenize_chunks_plaintext
    out_file = in_file.parent / (
        in_file.stem + "_pybo" + in_file.suffix
    )  # see inside code for naming convention
    assert out_file.is_file()
    # the file has been written
    assert (
        out_file.read_text()
        == "﻿ལེ_གས །_ བཀྲ་ ཤིས་ མཐའི་ _༆_ ཤི་ བཀྲ་ ཤིས་__ tr_ བདེ་་ ལེ_གས །_ བཀྲ་ ཤིས་ བདེ་ ལེགས་ ༡༢༣ ཀཀ །_ མཐའི་ རྒྱ་ མཚོར་ གནས་ པའི་ ཉས་ ཆུ་ འཐུང་ །།_།། མཁའ །"
    )


@pytest.mark.skip(reason="not a config bug")
def test_tokenize_sentences_and_paragraph():
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
    out = t.tokenize_sentences_plaintext

    expected = dedent(
        """\
                            བཀུར་བར་མི་འགྱུར་ཞིང༌། །བརྙས་བཅོས་མི་སྙན་རྗོད་པར་བྱེད། །
                            དབང་དང་འབྱོར་པ་ལྡན་པ་ཡི། །རྒྱལ་རིགས་ཕལ་ཆེར་བག་མེད་པས། །མྱོས་པའི་གླང་ཆེན་བཞིན་དུ་འཁྱམས། །དེ་ཡི་འཁོར་ཀྱང་དེ་འདྲར་འགྱུར། །
                            གཞན་ཡང་རྒྱལ་པོ་རྒྱལ་རིགས་ཀྱི། །སྤྱོད་པ་བཟང་ངན་ཅི་འདྲ་བ། །དེ་འདྲའི་ཚུལ་ལ་བལྟས་ནས་སུ། །འབངས་རྣམས་དེ་དང་དེ་འདྲ་སྟེ། །
                            རྒྱལ་པོ་ནོར་ལ་བརྐམས་གྱུར་ན། །
                            ནོར་གྱིས་རྒྱལ་ཁྲིམས་བསླུ་བར་རྩོམ། །
                            མི་བདག་གཡེམ་ལ་དགའ་གྱུར་ན། །
                            འཕྱོན་མའི་ཚོགས་རྣམས་མགོ་འཕང་མཐོ། །
                            ཕྲ་མར་ཉན་ན་དབྱེན་གྱིས་གཏོར། །
                            བརྟག་དཔྱད་མི་ཤེས་རྫུན་གྱིས་སླུ། །ང་ལོ་ཡང་ན་ཀུན་གྱིས་བསྐྱོད། །
                            ངོ་དགར་བརྩི་ན་ཟོལ་ཚིག་སྨྲ། །
                            དེ་དང་དེ་ལ་སོགས་པ་ཡི། །མི་བདག་དེ་ལ་གང་གང་གིས། །བསླུ་བར་རུང་བའི་སྐབས་མཐོང་ན། །
                            གཡོན་ཅན་ཚོགས་ཀྱིས་ཐབས་དེ་སེམས། །མི་རྣམས་རང་འདོད་སྣ་ཚོགས་ལ། །རྒྱལ་པོ་ཀུན་གྱི་ཐུན་མོང་ཕྱིར། །རྒྱལ་པོས་བསམ་གཞིགས་མ་བྱས་ན། །
                            ཐ་མར་རྒྱལ་སྲིད་འཇིག་པར་འགྱུར། །
                            ཆེན་པོའི་གོ་སར་གནས་པ་ལ། །སྐྱོན་ཀྱང་ཡོན་ཏན་ཡིན་ཚུལ་དུ། །འཁོར་ངན་རྣམས་ཀྱིས་ངོ་བསྟོད་སྨྲ། །
                            དེ་ཕྱིར་སྐྱོན་ཡོན་ཤེས་པ་དཀའ། །
                            ལྷག་པར་རྩོད་ལྡན་སྙིགས་མའི་ཚེ། །འཁོར་གྱི་ནང་ན་མ་རབས་མང༌། །
                            སྐྱོན་ཡང་ཡོན་ཏན་ལྟར་མཐོང་ལ། །རང་འདོད་ཆེ་ཞིང་རྒྱལ་པོ་བསླུ། །ཆུས་དང་འཁོར་གྱི་བདེ་ཐབས་ལ། །བསམ་གཞིགས་བྱེད་པ་དཀོན་པའི་ཕྱིར། །རྒྱལ་པོས་ལེགས་པར་དཔྱད་ནས་
                            སུ། །བདེན་པའི་ངག་ལས་"""
    )
    # each line is a sentence
    assert out == expected

    out = t.tokenize_paragraph_plaintext

    expected = dedent(
        """\
            བཀུར་བར་མི་འགྱུར་ཞིང༌། །བརྙས་བཅོས་མི་སྙན་རྗོད་པར་བྱེད། །དབང་དང་འབྱོར་པ་ལྡན་པ་ཡི། །རྒྱལ་རིགས་ཕལ་ཆེར་བག་མེད་པས། །མྱོས་པའི་གླང་ཆེན་བཞིན་དུ་འཁྱམས། །དེ་ཡི་འཁོར་ཀྱང་དེ་འདྲར་འགྱུར། །གཞན་ཡང་རྒྱལ་པོ་རྒྱལ་རིགས་ཀྱི། །སྤྱོད་པ་བཟང་ངན་ཅི་འདྲ་བ། །དེ་འདྲའི་ཚུལ་ལ་བལྟས་ནས་སུ། །འབངས་རྣམས་དེ་དང་དེ་འདྲ་སྟེ། །རྒྱལ་པོ་ནོར་ལ་བརྐམས་གྱུར་ན། །ནོར་གྱིས་རྒྱལ་ཁྲིམས་བསླུ་བར་རྩོམ། །མི་བདག་གཡེམ་ལ་དགའ་གྱུར་ན། །འཕྱོན་མའི་ཚོགས་རྣམས་མགོ་འཕང་མཐོ། །ཕྲ་མར་ཉན་ན་དབྱེན་གྱིས་གཏོར། །བརྟག་དཔྱད་མི་ཤེས་རྫུན་གྱིས་སླུ། །ང་ལོ་ཡང་ན་ཀུན་གྱིས་བསྐྱོད། །ངོ་དགར་བརྩི་ན་ཟོལ་ཚིག་སྨྲ། །དེ་དང་དེ་ལ་སོགས་པ་ཡི། །མི་བདག་དེ་ལ་གང་གང་གིས། །བསླུ་བར་རུང་བའི་སྐབས་མཐོང་ན། །
            གཡོན་ཅན་ཚོགས་ཀྱིས་ཐབས་དེ་སེམས། །མི་རྣམས་རང་འདོད་སྣ་ཚོགས་ལ། །རྒྱལ་པོ་ཀུན་གྱི་ཐུན་མོང་ཕྱིར། །རྒྱལ་པོས་བསམ་གཞིགས་མ་བྱས་ན། །ཐ་མར་རྒྱལ་སྲིད་འཇིག་པར་འགྱུར། །ཆེན་པོའི་གོ་སར་གནས་པ་ལ། །སྐྱོན་ཀྱང་ཡོན་ཏན་ཡིན་ཚུལ་དུ། །འཁོར་ངན་རྣམས་ཀྱིས་ངོ་བསྟོད་སྨྲ། །དེ་ཕྱིར་སྐྱོན་ཡོན་ཤེས་པ་དཀའ། །ལྷག་པར་རྩོད་ལྡན་སྙིགས་མའི་ཚེ། །འཁོར་གྱི་ནང་ན་མ་རབས་མང༌། །སྐྱོན་ཡང་ཡོན་ཏན་ལྟར་མཐོང་ལ། །རང་འདོད་ཆེ་ཞིང་རྒྱལ་པོ་བསླུ། །ཆུས་དང་འཁོར་གྱི་བདེ་ཐབས་ལ། །བསམ་གཞིགས་བྱེད་པ་དཀོན་པའི་ཕྱིར། །རྒྱལ་པོས་ལེགས་པར་དཔྱད་ནས་སུ། །བདེན་པའི་ངག་ལས་"""
    )
    # each line is a paragraph
    assert out == expected


def test_advanced_features():
    ########################################
    # 1. instanciating with a custom profile
    t = Text(in_str, tok_params={"config": Config()})
    tokens = t.tokenize_words_raw_text
    assert (
        tokens
        == "ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་_ tr_ བདེ་་ལེ_གས །_ བཀྲ་ཤིས་ བདེ་ལེགས་ ༡༢༣ ཀཀ །_ མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །"
    )

    # instanciating with a custom profile. tok_params can receive all the supported arguments of WordTokenizer
    config = Config()
    # config.add_dialect_pack(Path("./tests/data/trie_dialect_pack"))
    tt = Text(in_str, tok_params={"config": config})
    ttokens = tt.tokenize_words_raw_text
    assert (
        ttokens
        == "ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་_ tr_ བདེ་་ལེ_གས །_ བཀྲ་ཤིས་ བདེ་ལེགས་ ༡༢༣ ཀཀ །_ མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །"
    )

    #############################
    # 2. adding a custom pipeline
    def custom_tokenizer(string):
        return string.split(" ")  # simply reimplementing the space-tokenizer

    def custom_modifier(tokens):
        return ["__" + t + "__" for t in tokens]

    def custom_formatter(tokens):
        return "\n".join(tokens)

    t = Text(in_str)
    tokens = t.custom_pipeline(
        "dummy", custom_tokenizer, custom_modifier, custom_formatter
    )
    # note how you pass the names of the functions you declare, without parens

    assert (
        tokens == "__ལེ__\n"
        "__གས།__\n"
        "__བཀྲ་ཤིས་མཐའི་__\n"
        "__༆__\n"
        "__ཤི་བཀྲ་ཤིས་__\n"
        "____\n"
        "__tr\n"
        "བདེ་་ལེ__\n"
        "__གས།__\n"
        "__བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ།\n"
        "མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།།__\n"
        "__།།མཁའ།__"
    )

    # or use other pipes
    tokens = t.custom_pipeline("dummy", "word_tok", "words_error_concs", "basic_concs")
    print(tokens)
    assert (
        tokens
        == '"མཐའི་ ༆ ཤི་བཀྲ་ཤིས་  "	tr\\n	"བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣"\n"བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣"	ཀཀ	"།\nམཐའི་རྒྱ་མཚོར་"\n"གནས་པའི་ཉས་ཆུ་"	འཐུང་	"།། །།མཁའ།"'
    )
    # two non-words found

    tokens = t.custom_pipeline("dummy", "word_tok", "words_error_types", "stats_types")
    assert tokens == "tr\\n	1\nཀཀ	1\nའཐུང་\t1"
    # the same non-words as before
