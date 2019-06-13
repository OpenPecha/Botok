# coding: utf-8
from typing import List, DefaultDict, Tuple


def plaintext(tokens: List[str], sep=' ') -> str:
    return sep.join(tokens)


def basic_conc(concs: List[Tuple[List[str], str, List[str]]], sep='\t', context_sep=' ', esc_context=True) -> str:
    out = []
    for L, occ, R in concs:
        left = context_sep.join(L)
        right = context_sep.join(R)

        if esc_context:
            left, right = f'"{left}"', f'"{right}"'

        line = f'{left}{sep}{occ}{sep}{right}'
        out.append(line)

    return '\n'.join(out)


def stats_types(total_mistakes: DefaultDict[str, int], sep='\t') -> str:
    total = [(mis, freq) for mis, freq in total_mistakes.items()]
    total = sorted(total, reverse=True, key=lambda x: x[1])
    total = [f'{mis}{sep}{freq}' for mis, freq in total]
    return '\n'.join(total)
