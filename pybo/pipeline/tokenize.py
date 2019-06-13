# coding: utf-8
from typing import List, NewType

from ..chunks.chunks import Chunks
from ..tokenizer.token import Token
from ..tokenizer.tokenizer import Tokenizer

PyboToken = NewType('PyboToken', Token)


def space_tok(text: str) -> List[str]:
    """Tokenizes string on spaces

    """
    return text.split(' ')


def bo_tok(text: str, profile: str) -> List[PyboToken]:
    tok = Tokenizer(profile)
    return tok.tokenize(text)


def bo_syl_tok(text: str) -> List[str]:
    chunks = Chunks(text)
    output = chunks.chunk()
    with_substrings = chunks.get_chunked(output)
    return [b for a, b in with_substrings]
