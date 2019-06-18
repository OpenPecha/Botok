# coding: utf8
from pybo import Chunks


def test_multiple_spaces():
    bo_string = Chunks('ཤི ས་ཤི  ས་')
    chunks = bo_string.make_chunks()
    chunks = bo_string.get_readable(chunks)
    assert ('TEXT', 'ཤི ས་') == chunks[0]
    assert ('TEXT', 'ཤི  ས་') == chunks[1]
    assert 2 == len(chunks)
