# coding: utf-8
from typing import List, DefaultDict, Tuple


def plaintext(tokens: List[str], sep=' ') -> str:
    tokens = [t.replace(' ', '_') for t in tokens]
    return sep.join(tokens)


def basic_conc(concs: DefaultDict[str, List[str]], sep='\t', esc_context=True) -> str:
    out = []
    for occ, LR in concs.items():
        for left, right in LR:

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
