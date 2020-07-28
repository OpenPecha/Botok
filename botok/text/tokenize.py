# coding: utf-8
from functools import lru_cache
from typing import List, NewType, Tuple

from ..tokenizers.chunktokenizer import ChunkTokenizer
from ..tokenizers.paragraphtokenizer import paragraph_tokenizer
from ..tokenizers.sentencetokenizer import sentence_tokenizer
from ..tokenizers.token import Token
from ..tokenizers.wordtokenizer import WordTokenizer

BoToken = NewType("BoToken", Token)


def space_tok(text: str) -> List[str]:
    """Tokenizes string on spaces

    """
    return text.split(" ")


def word_tok(text: str, config=None) -> List[BoToken]:
    tok = get_wordtokenizer(config=config)
    return tok.tokenize(text)


def sentence_tok(text: str, config=None) -> List[Tuple[int, List[BoToken]]]:
    tok = get_wordtokenizer(config=config)
    tokens = tok.tokenize(text)
    return sentence_tokenizer(tokens)


def paragraph_tok(text: str, config=None) -> List[Tuple[int, List[BoToken]]]:
    tok = get_wordtokenizer(config=config)
    tokens = tok.tokenize(text)
    return paragraph_tokenizer(tokens)


@lru_cache(
    maxsize=None
)  # <--- make sure that the trie is only built once then kept in memory
def get_wordtokenizer(config=None):
    return WordTokenizer(config=config)


def chunk_tok(text: str) -> List[str]:
    return ChunkTokenizer(text).tokenize()
