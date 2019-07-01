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


def word_tok(text: str, profile, modifs=None, mode='internal') -> List[PyboToken]:
    tok = get_wordtokenizer(profile, modifs, mode)
    return tok.tokenize(text)


@lru_cache(maxsize=None)  # <--- make sure that the trie is only built once then kept in memory
def get_wordtokenizer(profile, modifs, mode):
    return WordTokenizer(profile, modifs=modifs, mode=mode)


def chunk_tok(text: str) -> List[str]:
    return ChunkTokenizer(text).tokenize()
