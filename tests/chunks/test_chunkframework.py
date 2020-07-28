# coding: utf8
from botok import ChunkFramework
from botok import ChunkMarkers as c


def test_bo_nonbo():
    string = 'བཀྲ་་ཤིས་བདེ་ལེགས། 23PIEIUZLDVéjoldvép«»("«»%='
    cb = ChunkFramework(string)
    chunks = cb.chunk_bo_chars()

    output = cb.get_readable(chunks)
    assert output == [
        ("BO", "བཀྲ་་ཤིས་བདེ་ལེགས། "),
        ("OTHER", '23PIEIUZLDVéjoldvép«»("«»%='),
    ]


def test_punct_nonpunct():
    string = "༆ བཀྲ་ཤིས་བདེ་ལེགས།། །།"
    cb = ChunkFramework(string)
    chunks = cb.chunk_punct()

    output = cb.get_readable(chunks)
    assert output == [
        ("PUNCT", "༆ "),
        ("NON_PUNCT", "བཀྲ་ཤིས་བདེ་ལེགས"),
        ("PUNCT", "།། །།"),
    ]


def test_sym_nonsym():
    string = "བཀྲ་ཤིས་བདེ་ལེགས། ༪༫༝༜༛༚༇༆"
    cb = ChunkFramework(string)
    chunks = cb.chunk_symbol()

    output = cb.get_readable(chunks)
    assert output == [
        ("NON_SYM", "བཀྲ་ཤིས་བདེ་ལེགས།"),
        ("SYM", " ༪༫༝༜༛༚"),
        ("NON_SYM", "༇༆"),
    ]


def test_num_nonnum():
    string = "བཀྲ་ཤིས་བདེ་ལེགས།  ༡༢༣༠༩༨"
    cb = ChunkFramework(string)
    chunks = cb.chunk_number()

    output = cb.get_readable(chunks)
    assert output == [("NON_NUM", "བཀྲ་ཤིས་བདེ་ལེགས།"), ("NUM", "  ༡༢༣༠༩༨")]


def test_space_nonspace():
    string = "བཀྲ་ཤིས་བདེ་ལེགས།   །བཀྲ་ཤིས་བདེ་ལེགས།"
    cb = ChunkFramework(string)
    chunks = cb.chunk_spaces()

    output = cb.get_readable(chunks)
    assert output == [
        ("NON_SPACE", "བཀྲ་ཤིས་བདེ་ལེགས།"),
        ("SPACE", "   "),
        ("NON_SPACE", "།བཀྲ་ཤིས་བདེ་ལེགས།"),
    ]


def test_text():
    string = "བཀྲ་ཤིས་བདེ་ལེགས"
    cb = ChunkFramework(string)
    chunks = cb.syllabify()

    output = cb.get_readable(chunks)
    assert output == [
        ("TEXT", "བཀྲ་"),
        ("TEXT", "ཤིས་"),
        ("TEXT", "བདེ་"),
        ("TEXT", "ལེགས"),
    ]


def test_latin():
    string = "བཀྲ་ཤིས་བདེ་ལེགས This is a test."
    cb = ChunkFramework(string)
    chunks = cb.chunk_latin()

    output = cb.get_readable(chunks)
    assert output == [("OTHER", "བཀྲ་ཤིས་བདེ་ལེགས"), ("LATIN", " This is a test.")]


def test_cjk():
    string = "བཀྲ་ཤིས་བདེ་ལེགས 这是  什么"
    cb = ChunkFramework(string)
    chunks = cb.chunk_cjk()

    output = cb.get_readable(chunks)
    assert output == [("OTHER", "བཀྲ་ཤིས་བདེ་ལེགས"), ("CJK", " 这是  什么")]


def test_other():
    string = "བཀྲ་ཤིས་བདེ་ལེགས กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"
    cb = ChunkFramework(string)
    chunks = cb.chunk_bo_chars()

    output = cb.get_readable(chunks)
    assert output == [
        ("BO", "བཀྲ་ཤིས་བདེ་ལེགས "),
        ("OTHER", "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"),
    ]


def test_full_example():
    # Follows the order implemented in Chunks
    string = (
        '༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། 23PIEIUZLDVéjoldvép«»("«»%= ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ '
        "This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"
    )
    cb = ChunkFramework(string)

    # BO / OTHER
    chunks = cb.chunk_bo_chars()
    chunks = cb.clean_chunks(chunks)
    output = cb.get_readable(chunks)
    assert output == [
        ("BO", "༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། "),
        ("OTHER", '23PIEIUZLDVéjoldvép«»("«»%='),
        ("BO", " ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ "),
        ("OTHER", "This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"),
    ]

    # BO / PUNCT
    chunks = cb.pipe_chunk(chunks, cb.chunk_punct, c.BO.value, c.PUNCT.value)
    chunks = cb.clean_chunks(chunks)
    output = cb.get_readable(chunks)
    assert output == [
        ("PUNCT", "༆ "),
        ("BO", "བཀྲ་ཤིས་བདེ་ལེགས"),
        ("PUNCT", "།། །། "),  # NEW
        ("OTHER", '23PIEIUZLDVéjoldvép«»("«»%= '),
        ("BO", "༪༫༝༜༛༚"),
        ("PUNCT", "༇༆ "),  # NEW
        ("BO", "༡༢༣༠༩༨ "),
        ("OTHER", "This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"),
    ]

    # BO / NUM
    chunks = cb.pipe_chunk(chunks, cb.chunk_number, c.BO.value, c.NUM.value)
    chunks = cb.clean_chunks(chunks)
    output = cb.get_readable(chunks)
    assert output == [
        ("PUNCT", "༆ "),
        ("BO", "བཀྲ་ཤིས་བདེ་ལེགས"),
        ("PUNCT", "།། །། "),
        ("OTHER", '23PIEIUZLDVéjoldvép«»("«»%= '),
        ("BO", "༪༫༝༜༛༚"),
        ("PUNCT", "༇༆ "),
        ("NUM", "༡༢༣༠༩༨ "),  # NEW
        ("OTHER", "This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"),
    ]

    # BO / SYM
    chunks = cb.pipe_chunk(chunks, cb.chunk_symbol, c.BO.value, c.SYM.value)
    chunks = cb.clean_chunks(chunks)
    output = cb.get_readable(chunks)
    assert output == [
        ("PUNCT", "༆ "),
        ("BO", "བཀྲ་ཤིས་བདེ་ལེགས"),
        ("PUNCT", "།། །། "),
        ("OTHER", '23PIEIUZLDVéjoldvép«»("«»%= '),
        ("SYM", "༪༫༝༜༛༚"),  # NEW
        ("PUNCT", "༇༆ "),
        ("NUM", "༡༢༣༠༩༨ "),
        ("OTHER", "This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"),
    ]

    # TEXT
    chunks = cb.pipe_chunk(chunks, cb.syllabify, c.BO.value, c.TEXT.value)
    chunks = cb.clean_chunks(chunks)
    output = cb.get_readable(chunks)
    assert output == [
        ("PUNCT", "༆ "),
        ("TEXT", "བཀྲ་"),  # NEW
        ("TEXT", "ཤིས་"),  # NEW
        ("TEXT", "བདེ་"),  # NEW
        ("TEXT", "ལེགས"),  # NEW
        ("PUNCT", "།། །། "),
        ("OTHER", '23PIEIUZLDVéjoldvép«»("«»%= '),
        ("SYM", "༪༫༝༜༛༚"),
        ("PUNCT", "༇༆ "),
        ("NUM", "༡༢༣༠༩༨ "),
        ("OTHER", "This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"),
    ]

    # OTHER / CJK
    chunks = cb.pipe_chunk(chunks, cb.chunk_cjk, c.OTHER.value, c.CJK.value)
    chunks = cb.clean_chunks(chunks)
    output = cb.get_readable(chunks)
    assert output == [
        ("PUNCT", "༆ "),
        ("TEXT", "བཀྲ་"),
        ("TEXT", "ཤིས་"),
        ("TEXT", "བདེ་"),
        ("TEXT", "ལེགས"),
        ("PUNCT", "།། །། "),
        ("OTHER", '23PIEIUZLDVéjoldvép«»("«»%= '),
        ("SYM", "༪༫༝༜༛༚"),
        ("PUNCT", "༇༆ "),
        ("NUM", "༡༢༣༠༩༨ "),
        ("OTHER", "This is a test."),
        ("CJK", " 这是  什么 "),  # NEW
        ("OTHER", "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"),
    ]

    # OTHER / LATIN
    chunks = cb.pipe_chunk(chunks, cb.chunk_latin, c.OTHER.value, c.LATIN.value)
    chunks = cb.clean_chunks(chunks)
    output = cb.get_readable(chunks)
    assert output == [
        ("PUNCT", "༆ "),
        ("TEXT", "བཀྲ་"),
        ("TEXT", "ཤིས་"),
        ("TEXT", "བདེ་"),
        ("TEXT", "ལེགས"),
        ("PUNCT", "།། །། "),
        ("LATIN", '23PIEIUZLDVéjoldvép«»("«»%= '),  # NEW
        ("SYM", "༪༫༝༜༛༚"),
        ("PUNCT", "༇༆ "),
        ("NUM", "༡༢༣༠༩༨ "),
        ("LATIN", "This is a test."),  # NEW
        ("CJK", " 这是  什么 "),
        ("OTHER", "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"),
    ]
