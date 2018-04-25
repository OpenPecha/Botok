from pybo import *


input_str = ' ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ'
tok = BoTokenizer('POS')
tokens = tok.tokenize(input_str)


def test_cql():
    query = '[pos="NOUN" & content!=""] []'
    matcher = CQLMatcher(query)
    slices = matcher.match(tokens)
    slice_strings = [tuple([tokens[i].content for i in range(start, end + 1)]) for start, end in slices]
    assert slices == [(1, 2), (3, 4), (5, 6), (6, 7)]
    assert slice_strings == [('བཀྲ་ཤིས་  ', 'tr'), (' བདེ་་ལེ གས', '།'), (' བཀྲ་ཤིས་', 'བདེ་ལེགས་'), ('བདེ་ལེགས་', 'ཀཀ')]


def test_token_split():
    ts = TokenSplit(tokens[0], 1, token_changes='[tag="XXX" & pos="xxx"] []')
    first, second = ts.split()
    assert first
    assert second


def test_token_merge():
    tm = TokenMerge(tokens[0], tokens[1])
    merged = tm.merge()
    assert merged


def test_match_split():
    match_query = '[pos="NOUN" & content!=""] []'
    replace_idx = 1  # slot number in match query
    split_idx = 1  # char index in token.content where split should occur
    replace = '[tag="XXX" & pos="xxx"] []'

    ms = SplittingMatcher(match_query, replace_idx, split_idx, tokens, replace)
    split_tokens = ms.split_on_matches()
    print('ok')
