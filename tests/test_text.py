# coding: utf8
from textwrap import dedent
from pathlib import Path

from pybo import *

in_str = "ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ། མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།། །།མཁའ།"


def test_simple_usage():
    # instanciating the Text object
    t = Text(in_str)

    # get builtin properties
    chunks = t.tokenize_chunks_plaintext
    assert chunks == 'ལེ_གས །_ བཀྲ་ ཤིས་ མཐའི་ _༆_ ཤི་ བཀྲ་ ཤིས་__ tr_ བདེ་་ ལེ_གས །_ བཀྲ་ ཤིས་ བདེ་ ལེགས་ ༡༢༣ ཀཀ །_ མཐའི་ རྒྱ་ མཚོར་ གནས་ པའི་ ཉས་ ཆུ་ འཐུང་ །།_།། མཁའ །'

    spaces = t.tokenize_on_spaces
    assert spaces == 'ལེ གས། བཀྲ་ཤིས་མཐའི་ ༆ ཤི་བཀྲ་ཤིས་ tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ། མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།། །།མཁའ།'
    # re-joins with a space, so it seems to only have replaces multiple spaces by single space (done in preprocessing)

    words = t.tokenize_words_raw_text
    assert words == 'ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་_ tr_ བདེ་་ལེ_གས །_ བཀྲ་ཤིས་ བདེ་ལེགས་ ༡༢༣ ཀཀ །_ མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །'
    # replaces all spaces in the input with "_" so the output is splittable with a space

    t_lines = Text(in_str + '\n' + in_str)
    with_lines = t_lines.tokenize_words_raw_lines
    assert with_lines == dedent("""\
        ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་__ tr_ བདེ་་ལེ_གས །_ བཀྲ་ཤིས་ བདེ་ལེགས་ ༡༢༣ ཀཀ །_ མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །
         ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་__ tr_ བདེ་་ལེ_གས །_ བཀྲ་ཤིས་ བདེ་ལེགས་ ༡༢༣ ཀཀ །_ མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །""")
    # keeps returns from the input (only do this if you know words are not split over two lines)

    # note: see in the console that the trie was only loaded once: lru_cache ensures we only load it once,
    # even over different instances of Text class

    types = t.list_word_types
    assert types == dedent("""\
                            ། 	3
                            འི་	3
                            བཀྲ་ཤིས་	2
                            མཐ	2
                            ལེ གས	1
                             ༆ 	1
                            ཤི་	1
                            བཀྲ་ཤིས་  	1
                            tr 	1
                            བདེ་་ལེ གས	1
                            བདེ་ལེགས་	1
                            ༡༢༣	1
                            ཀཀ	1
                            རྒྱ་མཚོ	1
                            ར་	1
                            གནས་པ	1
                            ཉ	1
                            ས་	1
                            ཆུ་	1
                            འཐུང་	1
                            །། །།	1
                            མཁའ	1
                            །	1""")
    # calculates the frequency of words in the text

    # now, run Text on a file. (using tokenize_chunks_plaintext property to test the feature because it is fast)
    in_file = Path(__file__).parent / 'resources' / 'test_file_to_tokenize.txt'
    t = Text(in_file)
    t.tokenize_chunks_plaintext
    out_file = in_file.parent / (in_file.stem + '_pybo' + in_file.suffix)  # see inside code for naming convention
    assert out_file.is_file()
    # the file has been written
    assert out_file.read_text() == '﻿ལེ_གས །_ བཀྲ་ ཤིས་ མཐའི་ _༆_ ཤི་ བཀྲ་ ཤིས་__ tr_ བདེ་་ ལེ_གས །_ བཀྲ་ ཤིས་ བདེ་ ལེགས་ ༡༢༣ ཀཀ །_ མཐའི་ རྒྱ་ མཚོར་ གནས་ པའི་ ཉས་ ཆུ་ འཐུང་ །།_།། མཁའ །'


def test_advanced_features():
    ########################################
    # 1. instanciating with a custom profile
    t = Text(in_str, tok_params={'profile': 'GMD'})
    tokens = t.tokenize_words_raw_text
    assert tokens == 'ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་_ tr_ བདེ་་ལེ_གས །_ བཀྲ་ཤིས་བདེ་ལེགས་ ༡༢༣ ཀཀ །_ མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །'

    # instanciating with a custom profile. tok_params can receive all the supported arguments of WordTokenizer
    tt = Text(in_str, tok_params={'profile': 'GMD', 'modifs': Path(__file__).parent / 'trie_data'})
    ttokens = tt.tokenize_words_raw_text
    assert ttokens == 'ལེ_གས །_ བཀྲ་ཤིས་ མཐ འི་ _༆_ ཤི་ བཀྲ་ཤིས་_ tr_ བདེ་་ལེ_གས །_ བཀྲ་ཤིས་ བདེ་ལེགས་ ༡༢༣ ཀཀ །_ མཐ འི་ རྒྱ་མཚོ ར་ གནས་པ འི་ ཉ ས་ ཆུ་ འཐུང་ །།_།། མཁའ །'
    # note that བཀྲ་ཤིས་ བདེ་ལེགས་ is now two tokens instead of 1 as in tokens

    #############################
    # 2. adding a custom pipeline
    def custom_tokenizer(string):
        return string.split(' ')  # simply reimplementing the space-tokenizer

    def custom_modifier(tokens):
        return ['__' + t + '__' for t in tokens]

    def custom_formatter(tokens):
        return '\n'.join(tokens)

    t = Text(in_str)
    tokens = t.custom_pipeline('dummy', custom_tokenizer, custom_modifier, custom_formatter)
    # note how you pass the names of the functions you declare, without parens

    assert tokens == dedent("""\
                            __ལེ__
                            __གས།__
                            __བཀྲ་ཤིས་མཐའི་__
                            __༆__
                            __ཤི་བཀྲ་ཤིས་__
                            ____
                            __tr__
                            __བདེ་་ལེ__
                            __གས།__
                            __བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣ཀཀ།__
                            __མཐའི་རྒྱ་མཚོར་གནས་པའི་ཉས་ཆུ་འཐུང་།།__
                            __།།མཁའ།__""")

    # or use other pipes
    tokens = t.custom_pipeline('dummy', 'word_tok', 'words_error_concs', 'basic_concs')
    assert tokens == '"བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་༡༢༣"\tཀཀ\t"། མཐའི་རྒྱ་མཚོར་"\n"གནས་པའི་ཉས་ཆུ་"\tའཐུང་\t"།། །།མཁའ།"'
    # two non-words found

    tokens = t.custom_pipeline('dummy', 'word_tok', 'words_error_types', 'stats_types')
    assert tokens == dedent("""\
                            ཀཀ	1
                            འཐུང་	1""")
    # the same non-words as before
