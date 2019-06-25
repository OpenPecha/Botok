# coding: utf8
from pybo import *


def test_multiple_spaces():
    bo_string = Chunks('ཤི ས་ཤི  ས་')
    chunks = bo_string.make_chunks()
    chunks = bo_string.get_readable(chunks)
    assert ('TEXT', 'ཤི ས་') == chunks[0]
    assert ('TEXT', 'ཤི  ས་') == chunks[1]
    assert 2 == len(chunks)


def test_bug1():
    tok = WordTokenizer('POS')
    string = 'བ་ཀུ་'
    tokens = tok.tokenize(string, debug=True)
    assert tokens


def test_bug2():
    tok = WordTokenizer('GMD')
    string = 'བྲ་གྲྀ་'
    tokens = tok.tokenize(string, debug=True)
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
