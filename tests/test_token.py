# coding: utf8
from textwrap import dedent
from pytest import raises

from pybo import *


def test_token():
    t = Token()
    t.text = 'test'
    # Token supports access to attributes in two ways (required for CQL found in third_party/cql.py)
    assert t.text == t['text']
    assert t._ == t['_']

    # setting existing attributes like dicts is supported
    attrs = {'pos': 'NOUN', 'freq': '123', 'len': 4}
    for k, v in attrs.items():
        t[k] = v
    assert str(t) == dedent("""\
                            text: "test"
                            pos: NOUN
                            freq: 123
                            start: 0
                            len: 4
                            
                            """)

    # raises an error when trying to add a new attribute
    with raises(AttributeError, match=r"Token objects don't have .* as attribute"):
        t['non_attr'] = 'test'
