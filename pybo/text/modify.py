# coding: utf-8
from typing import List, DefaultDict, NewType, Tuple
from collections import defaultdict

from .tokenize import PyboToken
from ..third_party.has_skrt_syl import has_skrt_syl


def is_mistake(token):
    exceptions = ["\n"]
    if token.chunk_type == "TEXT" or (
        token.chunk_type == "LATIN"
        or token.chunk_type == "CJK"
        or token.chunk_type == "OTHER"
    ):
        if (
            (not token.skrt and not has_skrt_syl(token.text_cleaned))
            and (
                token.entries
                and len(
                    [
                        True
                        for m in token.entries
                        if "pos" in m and (m["pos"] == "OOV" or m["pos"] == "NON_WORD")
                    ]
                )
                > 0
                or (
                    token.chunk_type == "LATIN"
                    or token.chunk_type == "CJK"
                    or token.chunk_type == "OTHER"
                )
            )
            and token.text not in exceptions
        ):
            return True
    return False


def words_error_concs(
    tokens: List[PyboToken], left=5, right=5
) -> DefaultDict[str, List[str]]:
    mistakes = defaultdict(list)
    for num, t in enumerate(tokens):
        if is_mistake(t):
            if num - left < 0:
                l = tokens[:num]
            else:
                l = tokens[num - left : num]
            if num + right > len(tokens) - 1:
                r = tokens[num + 1 :]
            else:
                r = tokens[num + 1 : num + 1 + right]

            l_context = [t.text for t in l]
            r_context = [t.text for t in r]
            mis = t.text.replace("\n", "\\n")
            mistakes[mis].append(["".join(l_context), "".join(r_context)])
    return mistakes


def words_error_types(tokens: List[PyboToken]) -> DefaultDict[str, int]:
    mistakes = defaultdict(int)
    for num, t in enumerate(tokens):
        if is_mistake(t):
            mis = t.text.replace("\n", "\\n")
            mistakes[mis] += 1
    return mistakes


def words_raw_types(tokens: List[PyboToken]) -> DefaultDict[str, int]:
    types = defaultdict(int)
    for t in tokens:
        occ = t.text.replace("\n", "\\n")
        types[occ] += 1
    return types


def words_raw_text(tokens: List[PyboToken]) -> List[str]:
    return [t.text for t in tokens]


def chunks_raw_text(tokens: List[Tuple[str, str]]) -> List[str]:
    return [chunk for _, chunk in tokens]
