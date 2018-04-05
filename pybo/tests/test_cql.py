from pybo import *


def get_token_list(in_str):
    bs = BoSyl()  # used to dynamically generate affixed versions
    trie = PyBoTrie(bs, profile='POS')  # loads or builds a trie
    tok = Tokenizer(trie)

    # b. pre-process the input string
    pre_processed = PyBoTextChunks(in_str)

    # c. tokenize
    return tok.tokenize(pre_processed)


def match(query, tokens_list):
    """
    Runs cql.Query on a slice of the list of tokens for every index in the list.

    :param query: CQL compliant query string
    :param tokens_list: output of BoTokenizer
    :type query: string
    :type tokens_list: list of Token objects
    :return: a list of matching slices of tokens_list
    :rtype: list of tuples with each two values: beginning and end indices
    """
    q = Query(query)
    slice_len = len(q.tokenexprs) - 1
    matches = []
    for i in range(len(tokens_list) - 1):
        if i + slice_len <= len(tokens_list) and q(tokens_list[i:i + slice_len + 1]):
            matches.append((i, i + slice_len))
    return matches


def test_cql():
    input_str = ' ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ'
    tokens = get_token_list(input_str)
    query = '[pos="NOUN"] [content!=""]'
    results = match(query, tokens)
    assert results
