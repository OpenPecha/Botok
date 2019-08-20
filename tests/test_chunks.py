# coding: utf8
from pybo import Chunks, TokChunks, TSEK

string = (
    '༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། 23PIEIUZLDVéjoldvép«»("«»%= ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ '
    "This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"
)


def test_chunks():
    c = Chunks(string)
    chunks = c.make_chunks()
    output = c.get_readable(chunks)
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


def test_tokchunks():
    c = TokChunks(string)
    c.serve_syls_to_trie()
    # generate what the tokenizer will ingest
    chunks = c.chunks
    assert chunks == [
        (None, (105, 0, 2)),
        ([2, 3, 4], (104, 2, 4)),  # syllable 1
        ([6, 7, 8], (104, 6, 4)),  # syllable 2
        ([10, 11, 12], (104, 10, 4)),  # syllable 3
        ([14, 15, 16, 17], (104, 14, 4)),  # syllable 4
        (None, (105, 18, 6)),
        (None, (101, 24, 28)),
        (None, (109, 52, 6)),
        (None, (105, 58, 3)),
        (None, (111, 61, 7)),
        (None, (101, 68, 15)),
        (None, (102, 83, 8)),
        (None, (103, 91, 24)),
    ]

    # the second element of each tuple is the chunk from Chunks
    readable = [(a[0], c.get_readable([a[1]])[0]) for a in chunks]
    assert readable == [
        (None, ("PUNCT", "༆ ")),
        ([2, 3, 4], ("TEXT", "བཀྲ་")),
        ([6, 7, 8], ("TEXT", "ཤིས་")),
        ([10, 11, 12], ("TEXT", "བདེ་")),
        ([14, 15, 16, 17], ("TEXT", "ལེགས")),
        (None, ("PUNCT", "།། །། ")),
        (None, ("LATIN", '23PIEIUZLDVéjoldvép«»("«»%= ')),
        (None, ("SYM", "༪༫༝༜༛༚")),
        (None, ("PUNCT", "༇༆ ")),
        (None, ("NUM", "༡༢༣༠༩༨ ")),
        (None, ("LATIN", "This is a test.")),
        (None, ("CJK", " 这是  什么 ")),
        (None, ("OTHER", "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ")),
    ]

    # just for the fun of it: get the cleaned syllable as it is done in the Tokenizer
    chunks = [
        "".join([string[c] for c in chars]) + TSEK for chars, chunk in chunks if chars
    ]
    assert chunks == ["བཀྲ་", "ཤིས་", "བདེ་", "ལེགས་"]
