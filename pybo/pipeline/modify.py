# coding: utf-8
from typing import List, DefaultDict, NewType
from collections import defaultdict

from ..helpers import is_skrt_word
from ..tokenizer.token import Token

PyboToken = NewType('PyboToken', Token)


def is_mistake(token):
    exceptions = ['\n']
    if token.type == 'syl' or token.type == 'non-bo':
        if (not token.skrt
            and not is_skrt_word(token.cleaned_content)) \
           and \
            (token.pos == 'oov'
             or token.pos == 'non-word'
             or token.type == 'non-bo') \
           and token.content not in exceptions:
            return True
    return False


def pybo_error_concs(tokens: List[PyboToken], left=5, right=5) -> DefaultDict[str, List[str]]:
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

            l_context = [t.content for t in l]
            r_context = [t.content for t in r]
            mis = t.content.replace('\n', '\\n')
            mistakes[mis].append([''.join(l_context), ''.join(r_context)])
    return mistakes


def pybo_error_types(tokens: List[PyboToken]) -> DefaultDict[str, int]:
    mistakes = defaultdict(int)
    for num, t in enumerate(tokens):
        if is_mistake(t):
            mis = t.content.replace('\n', '\\n')
            mistakes[mis] += 1
    return mistakes


def pybo_raw_types(tokens: List[PyboToken]) -> DefaultDict[str, int]:
    types = defaultdict(int)
    for t in tokens:
        occ = t.content.replace('\n', '\\n')
        types[occ] += 1
    return types


def pybo_raw_content(tokens: List[PyboToken]) -> List[str]:
    return [t.content for t in tokens]
