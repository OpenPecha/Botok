from pybo import *


def get_token_list(in_str):
    bs = BoSyl()  # used to dynamically generate affixed versions
    trie = PyBoTrie(bs, profile='POS')  # loads or builds a trie
    tok = Tokenizer(trie)

    # b. pre-process the input string
    pre_processed = PyBoTextChunks(in_str)

    # c. tokenize
    return tok.tokenize(pre_processed)


def test_cql():
    input_str = ' ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ'
    tokens = get_token_list(input_str)
    query = '[pos="NOUN" & content!=""] []'
    split = TokenSplit(tokens[0], 1)
    first, second = split.split()
    matcher = BoMatcher(query)
    slices = matcher.match(tokens)
    slice_strings = [tuple([tokens[i].content for i in range(start, end + 1)]) for start, end in slices]
    assert slices == [(1, 2), (3, 4), (5, 6), (6, 7)]
    assert slice_strings == [('བཀྲ་ཤིས་  ', 'tr'), (' བདེ་་ལེ གས', '།'), (' བཀྲ་ཤིས་', 'བདེ་ལེགས་'), ('བདེ་ལེགས་', 'ཀཀ')]
