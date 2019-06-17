# coding: utf8
from pybo import ChunkBase


def test_bo_nonbo():
    string = 'བཀྲ་་ཤིས་བདེ་ལེགས། 23PIEIUZLDVéjoldvép«»("«»%='
    cb = ChunkBase(string)
    chunks = cb.chunk_bo_chars()

    output = cb.get_readable(chunks)
    assert [('BO', 'བཀྲ་་ཤིས་བདེ་ལེགས། '), ('OTHER', '23PIEIUZLDVéjoldvép«»("«»%=')] == output


def test_punct_nonpunct():
    string = '༆ བཀྲ་ཤིས་བདེ་ལེགས།། །།'
    cb = ChunkBase(string)
    chunks = cb.chunk_punct()

    output = cb.get_readable(chunks)
    assert [('PUNCT', '༆ '), ('NON_PUNCT', 'བཀྲ་ཤིས་བདེ་ལེགས'), ('PUNCT', '།། །།')] == output


def test_sym_nonsym():
    string = 'བཀྲ་ཤིས་བདེ་ལེགས། ༪༫༝༜༛༚༇༆'
    cb = ChunkBase(string)
    chunks = cb.chunk_symbol()

    output = cb.get_readable(chunks)
    assert [('NON_SYM', 'བཀྲ་ཤིས་བདེ་ལེགས། '), ('SYM', '༪༫༝༜༛༚'), ('NON_SYM', '༇༆')] == output


def test_num_nonnum():
    string = 'བཀྲ་ཤིས་བདེ་ལེགས།  ༡༢༣༠༩༨'
    cb = ChunkBase(string)
    chunks = cb.chunk_number()

    output = cb.get_readable(chunks)
    assert [('NON_NUM', 'བཀྲ་ཤིས་བདེ་ལེགས།  '), ('NUM', '༡༢༣༠༩༨')] == output


def test_space_nonspace():
    string = 'བཀྲ་ཤིས་བདེ་ལེགས།   །བཀྲ་ཤིས་བདེ་ལེགས།'
    cb = ChunkBase(string)
    chunks = cb.chunk_spaces()

    output = cb.get_readable(chunks)
    assert [('NON_SPACE', 'བཀྲ་ཤིས་བདེ་ལེགས།'), ('SPACE', '   '), ('NON_SPACE', '།བཀྲ་ཤིས་བདེ་ལེགས།')] == output


def test_text():
    string = 'བཀྲ་ཤིས་བདེ་ལེགས'
    cb = ChunkBase(string)
    chunks = cb.syllabify()

    output = cb.get_readable(chunks)
    assert [('TEXT', 'བཀྲ་'), ('TEXT', 'ཤིས་'), ('TEXT', 'བདེ་'), ('TEXT', 'ལེགས')] == output


def test_latin():
    string = 'བཀྲ་ཤིས་བདེ་ལེགས This is a test.'
    cb = ChunkBase(string)
    chunks = cb.chunk_latin()

    output = cb.get_readable(chunks)
    assert [('OTHER', 'བཀྲ་ཤིས་བདེ་ལེགས'), ('LATIN', ' This is a test.')] == output


def test_cjk():
    string = 'བཀྲ་ཤིས་བདེ་ལེགས 这是  什么'
    cb = ChunkBase(string)
    chunks = cb.chunk_cjk()

    output = cb.get_readable(chunks)
    assert [('OTHER', 'བཀྲ་ཤིས་བདེ་ལེགས'), ('CJK', ' 这是  什么')] == output


def test_other():
    string = 'བཀྲ་ཤིས་བདེ་ལེགས กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ'
    cb = ChunkBase(string)
    chunks = cb.chunk_bo_chars()

    output = cb.get_readable(chunks)
    assert [('BO', 'བཀྲ་ཤིས་བདེ་ལེགས '), ('OTHER', 'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ')] == output


def test_full_example():
    string = '༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། 23PIEIUZLDVéjoldvép«»("«»%= ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ ' \
             'This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ'
    cb = ChunkBase(string)
    chunks = cb.chunk_bo_chars()
    output = cb.get_readable(chunks)
    print()

    output = cb.get_readable(chunks)
    assert [('NON_SYM', 'བཀྲ་ཤིས་བདེ་ལེགས། '), ('SYM', '༪༫༝༜༛༚'), ('NON_SYM', '༇༆')] == output



# # 1. Initial chunking
# chunks = bc.chunk_bo_chars()  # uses default chunk-marks here, but override them in the pipeline
#
# chunks  # actual chunks. each chunk is tuple containing: (chunk-marker, starting_index, chunk_length)
# [(100, 0, 11), (101, 11, 2), (100, 13, 10)]
# cchunks = bc.get_markers(chunks)  # shows the human-readable description of the constant
# [('bo', 0, 11), ('non-bo', 11, 2), ('bo', 13, 10)]
# cchunks = bc.get_chunked(chunks)  # shows the substring for each chunk
# [(100, ' བཀྲ་ཤིས་  '), (101, 'tr'), (100, ' བདེ་ལེགས།')]
#
# # 2. First piped chunking: re-chunks tibetan chunks into tibetan text and tibetan punctuation.
# bc.pipe_chunk(chunks, bc.chunk_punct, to_chunk=u.BO, yes=u.PUNCT.value)
#
# chunks
# [(100, 0, 11), (101, 11, 2), (100, 13, 9), (102, 22, 1)]
# cchunks = bc.get_markers(chunks)
# [('bo', 0, 11), ('non-bo', 11, 2), ('bo', 13, 9), ('punct', 22, 1)]
# cchunks = bc.get_chunked(chunks)
# [(100, ' བཀྲ་ཤིས་  '), (101, 'tr'), (100, ' བདེ་ལེགས'), (102, '།')]
#
# # 3. Second piped chunking: re-chunks tibetan text into syllables, keeping the same chunk-marker.
# bc.pipe_chunk(chunks, bc.syllabify, to_chunk=u.BO, yes=u.TEXT.value)
#
# chunks
# [(100, 0, 5), (100, 5, 4), (100, 9, 2), (101, 11, 2), (100, 13, 5), (100, 18, 4), (102, 22, 1)]
# cchunks = bc.get_markers(chunks)
# [('bo', 0, 5), ('bo', 5, 4), ('bo', 9, 2), ('non-bo', 11, 2), ('bo', 13, 5), ('bo', 18, 4), ('punct', 22, 1)]
# cchunks = bc.get_chunked(chunks)
# [(100, ' བཀྲ་'), (100, 'ཤིས་'), (100, '  '), (101, 'tr'), (100, ' བདེ་'), (100, 'ལེགས'), (102, '།')]
#
# # 4. Formatting the resultant chunks into an easily usable structure
# chunks = bc.get_markers(chunks)         # exchange the constants for the human-readable description
# final_result = bc.get_chunked(chunks)   # exchange the indices for the substrings of each chunk
# final_result
# [('bo', ' བཀྲ་'), ('bo', 'ཤིས་'), ('bo', '  '), ('non-bo', 'tr'), ('bo', ' བདེ་'), ('bo', 'ལེགས'), ('punct', '།')]
#
