# coding: utf-8
from typing import List, NewType, Tuple
from functools import lru_cache

from ..tokenizers.token import Token
from ..tokenizers.wordtokenizer import WordTokenizer
from ..tokenizers.chunktokenizer import ChunkTokenizer
from ..tokenizers.sentencetokenizer import sentence_tokenizer
from ..tokenizers.paragraphtokenizer import paragraph_tokenizer

PyboToken = NewType("PyboToken", Token)


def space_tok(text: str) -> List[str]:
    """Tokenizes string on spaces

    """
    return text.split(" ")


def word_tok(text: str, profile, modifs=None, mode="internal") -> List[PyboToken]:
    tok = get_wordtokenizer(profile, modifs, mode)
    return tok.tokenize(text)


def sentence_tok(
    text: str, profile, modifs=None, mode="internal"
) -> List[Tuple[int, List[PyboToken]]]:
    tok = get_wordtokenizer(profile, modifs, mode)
    tokens = tok.tokenize(text)
    return sentence_tokenizer(tokens)


def paragraph_tok(
    text: str, profile, modifs=None, mode="internal"
) -> List[Tuple[int, List[PyboToken]]]:
    tok = get_wordtokenizer(profile, modifs, mode)
    tokens = tok.tokenize(text)
    return paragraph_tokenizer(tokens)


@lru_cache(
    maxsize=None
)  # <--- make sure that the trie is only built once then kept in memory
def get_wordtokenizer(profile, modifs, mode):
    return WordTokenizer(profile, tok_modifs=modifs, tok_mode=mode)


def chunk_tok(text: str) -> List[str]:
    return ChunkTokenizer(text).tokenize()
