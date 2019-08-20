# coding: utf8
from pybo import *


def test_chunktokenizer():
    input_str = (
        " ཤི་བཀྲ་ཤིས་  བདེ་་ལ             ེ       གས་ "
        'བཀྲ་ཤིས་བདེ་ལེགས ༆ བཀྲ་ཤིས་བདེ་ལེགས།། །། 23PIEIUZLDVéjoldvép«»("«»%= ༪༫༝༜༛༚༇༆ ༡༢༣༠༩༨ '
        "This is a test. 这是  什么 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"
    )
    st = ChunkTokenizer(input_str)
    tokens = st.tokenize()
    assert tokens == [
        ("TEXT", " ཤི་"),
        ("TEXT", "བཀྲ་"),
        ("TEXT", "ཤིས་"),
        ("TEXT", "  བདེ་་"),
        ("TEXT", "ལ             ེ       གས་"),
        ("TEXT", " བཀྲ་"),
        ("TEXT", "ཤིས་"),
        ("TEXT", "བདེ་"),
        ("TEXT", "ལེགས"),
        ("PUNCT", " ༆ "),
        ("TEXT", "བཀྲ་"),
        ("TEXT", "ཤིས་"),
        ("TEXT", "བདེ་"),
        ("TEXT", "ལེགས"),
        ("PUNCT", "།། །། "),
        ("LATIN", '23PIEIUZLDVéjoldvép«»("«»%= '),
        ("SYM", "༪༫༝༜༛༚"),
        ("PUNCT", "༇༆ "),
        ("NUM", "༡༢༣༠༩༨ "),
        ("LATIN", "This is a test."),
        ("CJK", " 这是  什么 "),
        ("OTHER", "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธ"),
    ]
