# coding: utf-8
from typing import List, NewType

from ..chunks.chunks import Chunks
from ..tokenizers.token import Token
from ..tokenizers.wordtokenizer import WordTokenizer

PyboToken = NewType('PyboToken', Token)


def space_tok(text: str) -> List[str]:
    """Tokenizes string on spaces

    """
    return text.split(' ')


def bo_tok(text: str, profile: str) -> List[PyboToken]:
    tok = WordTokenizer(profile)
    return tok.tokenize(text)


def bo_syl_tok(text: str) -> List[str]:
    chunks = Chunks(text)
    output = chunks.chunk()
    with_substrings = chunks.get_chunked(output)
    return [b for a, b in with_substrings]
