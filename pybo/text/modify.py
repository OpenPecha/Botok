# coding: utf-8
from typing import List, DefaultDict, NewType
from collections import defaultdict

from ..third_party.has_skrt_syl import has_skrt_syl
from ..tokenizers.token import Token

PyboToken = NewType('PyboToken', Token)


def is_mistake(token):
    exceptions = ['\n']
    if token.type == 'TEXT' or token.type == 'NON_BO':
        if (not token.skrt
            and not has_skrt_syl(token.text_cleaned)) \
           and \
            (token.pos == 'OOV'
             or token.pos == 'non-word'
             or token.type == 'non-bo') \
           and token.content not in exceptions:
            return True
    return False


def words_error_concs(tokens: List[PyboToken], left=5, right=5) -> DefaultDict[str, List[str]]:
    mistakes = defaultdict(list)
    for num, t in enumerate(tokens):
        if is_mistake(t):
            if num - left < 0:
                l = tokens[:num]
            else:
                l = tokens[num - left:num]
            if num + right > len(tokens)-1:
                r = tokens[num+1:]
            else:
                r = tokens[num+1:num+1+right]

            l_context = [t.text for t in l]
            r_context = [t.text for t in r]
            mis = t.text.replace('\n', '\\n')
            mistakes[mis].append([''.join(l_context), ''.join(r_context)])
    return mistakes


def words_error_types(tokens: List[PyboToken]) -> DefaultDict[str, int]:
    mistakes = defaultdict(int)
    for num, t in enumerate(tokens):
        if is_mistake(t):
            mis = t.text.replace('\n', '\\n')
            mistakes[mis] += 1
    return mistakes


def words_raw_types(tokens: List[PyboToken]) -> DefaultDict[str, int]:
    types = defaultdict(int)
    for t in tokens:
        occ = t.text.replace('\n', '\\n')
        types[occ] += 1
    return types


def words_raw_text(tokens: List[PyboToken]) -> List[str]:
    return [t.text for t in tokens]


def chunks_raw_text(tokens: List[(str, str)]) -> List[str]:
    return [t[1] for t in tokens]
