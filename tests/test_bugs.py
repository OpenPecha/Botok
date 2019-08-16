# coding: utf8
from pybo import *
import sys

sys.path.append('../')
from helpers import gmd_tok


def test_keyerror_part_lemma():
    tokens = gmd_tok.tokenize('ཕའིའོ།')
    assert len(tokens) == 3


def test_split_token():
    wt = WordTokenizer('empty')
    wt.tok.trie.rebuild_trie()
    wt.tok.trie.inflect_n_modify_trie('འ་')
    assert not wt.tok.trie.has_word('ར་')['exists']


def test_missing_entries_n_bad_unaffixed():
    input_str = "ཤུ་ཀ་ར་"
    tokens = gmd_tok.tokenize(input_str, split_affixes=False)
    assert [t.text for t in tokens] == ['ཤུ་ཀ་', 'ར་']
    assert tokens[0].entries
    assert tokens[1].text_unaffixed == 'ར་'


def test_multiple_spaces():
    bo_string = Chunks('ཤི ས་ཤི  ས་')
    chunks = bo_string.make_chunks()
    chunks = bo_string.get_readable(chunks)
    assert chunks[0] == ('TEXT', 'ཤི ས་')
    assert chunks[1] == ('TEXT', 'ཤི  ས་')
    assert len(chunks) == 2


def test_bug1():
    tok = WordTokenizer('POS')
    string = 'བ་ཀུ་'
    tokens = tok.tokenize(string, debug=True)
    assert tokens


def test_bug2():
    string = 'བྲ་གྲྀ་'
    tokens = gmd_tok.tokenize(string, debug=True)
    assert tokens


def test_many_tseks_in_syllable():
    input_str = ' ཤི་བཀྲ་ཤིས་  བདེ་་ལ             ེ       གས་ བཀྲ་ཤིས་བདེ་ལེགས'
    cb = ChunkFramework(input_str)
    chunks = cb.syllabify()
    readable = cb.get_readable(chunks)
    assert readable == [('TEXT', ' ཤི་'),
                        ('TEXT', 'བཀྲ་'),
                        ('TEXT', 'ཤིས་'),
                        ('TEXT', '  བདེ་་'),
                        ('TEXT', 'ལ             ེ       གས་'),
                        ('TEXT', ' བཀྲ་'),
                        ('TEXT', 'ཤིས་'),
                        ('TEXT', 'བདེ་'),
                        ('TEXT', 'ལེགས')]

    chunks = cb.chunk_punct()
    chunks = cb.merge_skippable_punct(chunks)
    readable = cb.get_readable(chunks)
    assert readable == [('NON_PUNCT', ' ཤི་བཀྲ་ཤིས་  བདེ་་ལ             ེ       གས་ བཀྲ་ཤིས་བདེ་ལེགས')]

    ck = Chunks(input_str)
    chunks = ck.make_chunks()
    readable = ck.get_readable(chunks)
    assert readable == [('TEXT', ' ཤི་'),
                        ('TEXT', 'བཀྲ་'),
                        ('TEXT', 'ཤིས་'),
                        ('TEXT', '  བདེ་་'),
                        ('TEXT', 'ལ             ེ       གས་'),
                        ('TEXT', ' བཀྲ་'),
                        ('TEXT', 'ཤིས་'),
                        ('TEXT', 'བདེ་'),
                        ('TEXT', 'ལེགས')]


def test_shad_in_syllable():
    input_str = ' tr བདེ་་ལེ གས། བཀྲ་'
    ck = Chunks(input_str)
    chunks = ck.make_chunks()
    readable = ck.get_readable(chunks)
    assert readable == [('LATIN', ' tr '),
                        ('TEXT', 'བདེ་་'),
                        ('TEXT', 'ལེ གས'),
                        ('PUNCT', '། '),
                        ('TEXT', 'བཀྲ་')]
