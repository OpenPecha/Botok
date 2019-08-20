# coding: utf8

# variables used in the tests
ending_particles = [
    "གོ་",
    "ངོ་",
    "དོ་",
    "ནོ་",
    "བོ་",
    "མོ་",
    "འོ་",
    "རོ་",
    "ལོ་",
    "སོ་",
    "ཏོ་",
]
ending_words = ["ཅིག་", "ཤོག་"]
ending_verbs = [
    "ཡིན་",
    "ཡོད་",
    "མིན་",
    "མེད་",
    "འགྱུར་",
    "ལྡན་",
    "བགྱི་",
    "བྱ་",
    "བཞུགས་",
]
te_particles = [
    "སྟེ་",
    "ཏེ་",
    "དེ་",
]  # separated because these seem to cut long sentences
clause_boundaries = te_particles + ["ནས་", "ན་"]
dagdra = ["པ་", "བ་", "པོ་", "བོ་"]


# Turn sentences as indices into sentences as follows:
# (<sent_length>, [token1, token2, ..., tokenn]) where tokens are Token objects
############################################################
def sentence_tokenizer(tokens):
    sent_indices = get_sentence_indices(tokens)
    # get tokens for each sentence
    sentences = []
    for sentence in sent_indices:
        start, end, l = sentence["start"], sentence["end"], sentence["len"]
        sentences.append((l, tokens[start : end + 1]))

    return sentences


# Get sentences in the form of indices
############################################################
def get_sentence_indices(tokens):
    """
    from 1 to 3, we want to use the shad since it reflects the writer's own idea of where parts of the
    sentence end and start.
    1. ending particle + shad to not take all the quotations that potentially contain ending particles

    2. clause boundary particles + shad: ན་ is often found within a sentence, but cuts it in a way that doesn't prevent
    the correct understanding, so for translation, we might want to remove it as translation units will want
    to keep those sentences together, but for segmentation jobs, it works as a fairly safe segmenter.
    we might want to use it.

    Output: list of sentences, each in the following format: (sentence-length, [word1, word2, ...])
    """
    # 1. find unambiguous sentence end markers: ending particles followed by punctuation
    previous_end = 0
    sentence_idx = extract_chunks(is_endpart_n_punct, tokens, 0, previous_end)

    # 2. find clause boundaries followed by punctuation
    sentence_idx = piped_sentencify(sentence_idx, tokens, is_clause_boundary_n_punct)

    # 3. find verbs followed by punctuation
    sentence_idx = piped_sentencify(sentence_idx, tokens, is_verb_n_punct)

    # 4. find verbs followed by clause boundaries
    sentence_idx = piped_sentencify(
        sentence_idx, tokens, is_verb_n_clause_boundary, threshold=30
    )  # max size to check

    # joining the sentences without verbs to either the one preceding them or following them
    sentence_idx = join_no_verb_sentences(sentence_idx, tokens)

    return sentence_idx


# Tests used in the sentence tokenizer
############################################################
def is_word(token):
    return token and token.chunk_type == "TEXT"


def has_last_syl(token, l):
    if token.syls:
        last_syl = "".join(token.syls[-1]) + "་"
        return last_syl in l
    else:
        return False


def is_ending_part(token):
    return token and token.pos == "PART" and has_last_syl(token, ending_particles)


def is_endpart_n_punct(token1, token2):
    return is_ending_part(token1) and token2.chunk_type == "PUNCT"


def is_clause_boundary_n_punct(token1, token2):
    return (
        has_last_syl(token1, clause_boundaries) or has_last_syl(token1, ending_words)
    ) and token2.chunk_type == "PUNCT"


def is_verb_n_punct(token1, token2):
    return (
        (token1.pos == "VERB" and not has_last_syl(token1, dagdra))
        or has_last_syl(token1, ending_verbs)
    ) and token2.chunk_type == "PUNCT"


def is_verb_n_clause_boundary(token1, token2):
    return (
        (token1.pos == "VERB" and not has_last_syl(token1, dagdra))
        or has_last_syl(token1, ending_verbs)
    ) and has_last_syl(token2, clause_boundaries)


# sentence tokenizer logic
############################################################
def join_no_verb_sentences(sentences, tokens, threshold=4):
    i = 0
    while i < len(sentences):
        start, end, length = (
            sentences[i]["start"],
            sentences[i]["end"],
            sentences[i]["len"],
        )
        if length > threshold:
            i += 1
            continue

        no_verb = True
        for token in tokens[start : end + 1]:
            if token.pos == "VERB" and not has_last_syl(token, dagdra):
                no_verb = False

        if no_verb:
            last_word = (
                tokens[end] if tokens[end].chunk_type == "TEXT" else tokens[end - 1]
            )
            if i + 1 < len(sentences) and has_last_syl(last_word, clause_boundaries):
                # join to the left
                sentences[i + 1]["start"] = sentences[i]["start"]
                sentences[i + 1]["len"] += sentences[i]["len"]
                del sentences[i]
                i -= 1
            elif i - 1 >= 0:
                # join to the right
                last_word_of_previous = (
                    tokens[sentences[i - 1]["end"]]
                    if tokens[sentences[i - 1]["end"]].chunk_type == "TEXT"
                    else tokens[sentences[i - 1]["end"] - 1]
                )
                if not has_last_syl(last_word_of_previous, ending_particles):
                    sentences[i - 1]["end"] = sentences[i]["end"]
                    sentences[i - 1]["len"] += sentences[i]["len"]
                    del sentences[i]
                    i -= 1

        i += 1

    return sentences


def extract_chunks(test, subtokens, start, previous_end):
    chunks = []
    n = 0
    for n, token in enumerate(subtokens):
        if test(subtokens[n - 1], token):
            chunks.append(
                {
                    "start": previous_end,
                    "end": start + n,
                    "len": start + n + 1 - previous_end,
                }
            )
            previous_end = start + n + 1
    if chunks and previous_end < start + n:
        chunks.append(
            {
                "start": previous_end,
                "end": start + n,
                "len": start + n + 1 - previous_end,
            }
        )

    # add all the subtokens if no chunk was produced
    if not chunks:
        chunks.append(
            {
                "start": previous_end,
                "end": start + n,
                "len": start + n + 1 - previous_end,
            }
        )

    return chunks


def piped_sentencify(sentences, tokens, test, threshold=None):
    a = 0
    while a < len(sentences):
        length, start, end = (
            sentences[a]["len"],
            sentences[a]["start"],
            sentences[a]["end"],
        )
        previous_end = start
        new_sentences = []
        if threshold:
            if end - start > threshold:
                new_sentences = extract_chunks(
                    test, tokens[start : end + 1], start, previous_end
                )
        else:
            new_sentences = extract_chunks(
                test, tokens[start : end + 1], start, previous_end
            )

        if new_sentences:
            sentences[a : a + 1] = new_sentences
            a += len(new_sentences)
        else:
            a += 1
    return sentences
