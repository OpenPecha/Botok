# coding: utf-8
from typing import List, NewType
from functools import lru_cache

from ..tokenizers.token import Token
from ..tokenizers.wordtokenizer import WordTokenizer
from ..tokenizers.chunktokenizer import ChunkTokenizer

PyboToken = NewType('PyboToken', Token)


def space_tok(text: str) -> List[str]:
    """Tokenizes string on spaces

    """
    return text.split(' ')


def word_tok(text: str, profile: str) -> List[PyboToken]:
    tok = get_wordtokenizer(profile)
    return tok.tokenize(text)


@lru_cache  # <--- make sure that the trie is only built once then kept in memory
def get_wordtokenizer(profile):
    return WordTokenizer(profile)


def chunk_tok(text: str) -> List[str]:
    return ChunkTokenizer(text).tokenize()
