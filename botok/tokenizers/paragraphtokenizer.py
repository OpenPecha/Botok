# coding: utf8
from .sentencetokenizer import get_sentence_indices


def paragraph_tokenizer(tokens):
    # a paragraph is defined as a group of sentences that does not have more words than a given threshold
    threshold = 70
    paragraph_max = 150
    par_indices = get_sentence_indices(tokens)

    # join small sentences to form paragraphs
    i = 0
    while i < len(par_indices):
        start, end, l = (
            par_indices[i]["start"],
            par_indices[i]["end"],
            par_indices[i]["len"],
        )
        if i > 0 and l < threshold:
            previous_len = par_indices[i - 1]["len"]
            if l + previous_len < paragraph_max:
                par_indices[i - 1]["end"] = par_indices[i]["end"]
                par_indices[i - 1]["len"] += par_indices[i]["len"]
                del par_indices[i]
                i -= 1
        i += 1

    # get tokens for each paragraph
    pars = []
    for par in par_indices:
        start, end, l = par["start"], par["end"], par["len"]
        pars.append((l, tokens[start : end + 1]))

    return pars
