# encoding: utf-8
from StringUtils import TibStringChunk, PyBoChunk

# uses py.test


def test_pybo_chunk():
    pybo_string = PyBoChunk(' བཀྲ་ཤིས་  tr བདེ་ལེགས།')
    found = pybo_string.chunk(indices=False)
    assert found == [('space', ' '), ('syl', 'བཀྲ་'), ('syl', 'ཤིས་'), ('space', '  '), ('non-bo', 'tr'),
                     ('space', ' '), ('syl', 'བདེ་'), ('syl', 'ལེགས'), ('punct', '།')]


tib_string = TibStringChunk(' བཀྲ་ཤིས་  tr བདེ་ལེགས།')


def test_bo():
    chunks = tib_string.chunk_tib_chars(yes='bo')
    assert chunks == [('bo', 0, 11), ('non-bo', 11, 2), ('bo', 13, 10)]

    found = tib_string.get_chunked(chunks)
    assert found == [('bo', ' བཀྲ་ཤིས་  '), ('non-bo', 'tr'), ('bo', ' བདེ་ལེགས།')]


def test_bo_n_spaces():
    chunks = tib_string.chunk_tib_chars(yes='bo')
    tib_string.pipe_chunk(chunks, tib_string.chunk_spaces, to_chunk='bo', yes='space')
    assert chunks == [('space', 0, 1), ('bo', 1, 8), ('space', 9, 2), ('non-bo', 11, 2), ('space', 13, 1),
                      ('bo', 14, 9)]

    found = tib_string.get_chunked(chunks)
    assert found == [('space', ' '), ('bo', 'བཀྲ་ཤིས་'), ('space', '  '), ('non-bo', 'tr'), ('space', ' '),
                     ('bo', 'བདེ་ལེགས།')]


def test_bo_n_spaces_n_syls():
    chunks = tib_string.chunk_tib_chars(yes='bo')
    tib_string.pipe_chunk(chunks, tib_string.chunk_spaces, to_chunk='bo', yes='space')
    tib_string.pipe_chunk(chunks, tib_string.syllabify, to_chunk='bo', yes='syl')
    assert chunks == [('space', 0, 1), ('syl', 1, 4), ('syl', 5, 4), ('space', 9, 2), ('non-bo', 11, 2),
                      ('space', 13, 1), ('syl', 14, 4), ('syl', 18, 5)]

    found = tib_string.get_chunked(chunks)
    assert found == [('space', ' '), ('syl', 'བཀྲ་'), ('syl', 'ཤིས་'), ('space', '  '), ('non-bo', 'tr'),
                     ('space', ' '), ('syl', 'བདེ་'), ('syl', 'ལེགས།')]


def test_spaces():
    chunks = tib_string.chunk_spaces()
    assert chunks == [('space', 0, 1), ('chars', 1, 8), ('space', 9, 2), ('chars', 11, 2), ('space', 13, 1),
                      ('chars', 14, 9)]

    found = tib_string.get_chunked(chunks)
    assert found == [('space', ' '), ('chars', 'བཀྲ་ཤིས་'), ('space', '  '), ('chars', 'tr'), ('space', ' '),
                     ('chars', 'བདེ་ལེགས།')]
