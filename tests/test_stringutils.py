# encoding: utf-8
from pybo import *

# uses py.test


def test_pybo_chunk():
    pybo_string = PyBoChunk(' བཀྲ་ཤིས་  tr བདེ་་ལེ གས། ')
    found = pybo_string.chunk(indices=False)
    found = pybo_string.get_markers(found)
    assert found == [('syl', ' བཀྲ་'), ('syl', 'ཤིས་  '), ('non-bo', 'tr '), ('syl', 'བདེ་'), ('punct', '་'), ('syl', 'ལེ གས'),
                     ('punct', '། ')]

bo_string = BoChunk(' བཀྲ་ཤིས་  tr བདེ་ལེགས།')

def test_bo():
    chunks = bo_string.chunk_bo_chars()
    chunks = bo_string.get_markers(chunks)
    assert chunks == [('bo', 0, 11), ('non-bo', 11, 2), ('bo', 13, 10)]

    found = bo_string.get_chunked(chunks)
    assert found == [('bo', ' བཀྲ་ཤིས་  '), ('non-bo', 'tr'), ('bo', ' བདེ་ལེགས།')]


def test_bo_n_spaces():
    chunks = bo_string.chunk_bo_chars()
    bo_string.pipe_chunk(chunks, bo_string.chunk_spaces, to_chunk=bo_string.BO_MARKER, yes=bo_string.SPACE_MARKER)
    chunks = bo_string.get_markers(chunks)
    assert chunks == [('space', 0, 1), ('bo', 1, 8), ('space', 9, 2), ('non-bo', 11, 2), ('space', 13, 1),
                      ('bo', 14, 9)]

    found = bo_string.get_chunked(chunks)
    assert found == [('space', ' '), ('bo', 'བཀྲ་ཤིས་'), ('space', '  '), ('non-bo', 'tr'), ('space', ' '),
                     ('bo', 'བདེ་ལེགས།')]


def test_bo_n_spaces_n_syls():
    chunks = bo_string.chunk_bo_chars()
    bo_string.pipe_chunk(chunks, bo_string.chunk_spaces, to_chunk=bo_string.BO_MARKER, yes=bo_string.SPACE_MARKER)
    bo_string.pipe_chunk(chunks, bo_string.syllabify, to_chunk=bo_string.BO_MARKER, yes=bo_string.SYL_MARKER)
    chunks = bo_string.get_markers(chunks)
    assert chunks == [('space', 0, 1), ('syl', 1, 4), ('syl', 5, 4), ('space', 9, 2), ('non-bo', 11, 2),
                      ('space', 13, 1), ('syl', 14, 4), ('syl', 18, 5)]

    found = bo_string.get_chunked(chunks)
    assert found == [('space', ' '), ('syl', 'བཀྲ་'), ('syl', 'ཤིས་'), ('space', '  '), ('non-bo', 'tr'),
                     ('space', ' '), ('syl', 'བདེ་'), ('syl', 'ལེགས།')]


def test_spaces():
    chunks = bo_string.chunk_spaces()
    chunks = bo_string.get_markers(chunks)
    assert chunks == [('space', 0, 1), ('non-space', 1, 8), ('space', 9, 2), ('non-space', 11, 2), ('space', 13, 1),
                      ('non-space', 14, 9)]

    found = bo_string.get_chunked(chunks)
    assert found == [('space', ' '), ('non-space', 'བཀྲ་ཤིས་'), ('space', '  '), ('non-space', 'tr'), ('space', ' '),
                     ('non-space', 'བདེ་ལེགས།')]


def test_multiple_spaces():
    bo_string = PyBoChunk('ཤི ས་ཤི  ས་')
    chunks = bo_string.chunk()
    chunks = bo_string.get_markers(chunks)
    chunks = bo_string.get_chunked(chunks)
    assert ('syl', 'ཤི ས་') == chunks[0]
    assert ('syl', 'ཤི  ས་') == chunks[1]
    assert 2 == len(chunks)
