# coding: utf-8
from typing import List, DefaultDict, Tuple

from .tokenize import PyboToken


def plaintext(tokens: List[str], sep=" ") -> str:
    tokens = [t.replace(" ", "_") for t in tokens]
    return sep.join(tokens)


def plaintext_sent_par(units: List[Tuple[int, List[PyboToken]]], sep="\n") -> str:
    out = []
    for u in units:
        unit = "".join([word.text for word in u[1]])
        out.append(unit)
    return sep.join(out)


def basic_conc(concs: DefaultDict[str, List[str]], sep="\t", esc_context=True) -> str:
    out = []
    for occ, LR in concs.items():
        for left, right in LR:

            if esc_context:
                left, right = f'"{left}"', f'"{right}"'

            line = f"{left}{sep}{occ}{sep}{right}"
            out.append(line)

    return "\n".join(out)


def stats_types(total_mistakes: DefaultDict[str, int], sep="\t") -> str:
    total = [(mis, freq) for mis, freq in total_mistakes.items()]
    total = sorted(total, reverse=True, key=lambda x: x[1])
    total = [f"{mis}{sep}{freq}" for mis, freq in total]
    return "\n".join(total)
