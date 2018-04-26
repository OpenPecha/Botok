from pybo import *


input_str = ' མཐའི་རྒྱ་མཚོའི་གླིང་། ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ'
tok = BoTokenizer('POS')
tokens = tok.tokenize(input_str)


def test_cql():
    query = '[pos="NOUN" & content!=""] []'
    matcher = CQLMatcher(query)
    slices = matcher.match(tokens)
    slice_strings = [tuple([tokens[i].content for i in range(start, end + 1)]) for start, end in slices]
    assert slices == [(0, 1), (2, 3), (4, 5), (7, 8), (9, 10), (11, 12), (12, 13)]
    assert slice_strings == [('མཐ', 'འི་'), ('རྒྱ་མཚོ', 'འི་'), ('གླིང་', '།'), ('བཀྲ་ཤིས་  ', 'tr'),
                             (' བདེ་་ལེ གས', '།'), (' བཀྲ་ཤིས་', 'བདེ་ལེགས་'), ('བདེ་ལེགས་', 'ཀཀ')]


def test_token_split():
    ts = TokenSplit(tokens[0], 1, token_changes='[tag="SPACE" & pos="PUNCT" & aa_word="False" & affixed="False"] []')
    first, second = ts.split()
    assert first.tag == 'SPACE'
    assert first.pos == 'PUNCT'


def test_token_merge():
    tm = TokenMerge(tokens[0], tokens[1])
    merged = tm.merge()
    assert merged


def test_match_split():
    match_query = '[pos="NOUN" & content!=""] []'
    replace_idx = 1  # slot number in match query
    split_idx = 1  # char index in token.content where split should occur
    replace = '[tag="XXX" & pos="xxx"] []'

    sm = SplittingMatcher(match_query, replace_idx, split_idx, tokens, replace)
    split_tokens = sm.split_on_matches()
    assert len(tokens) == 14
    assert len(split_tokens) == 20


def test_match_merge():
    match_query = '[pos="NOUN" & content!=""] []'
    replace_idx = 1  # slot number in match query
    split_idx = 1  # char index in token.content where split should occur
    replace = '[tag="XXX" & pos="xxx"]'

    mm = MergingMatcher(match_query, replace_idx, tokens, replace)
    merged_tokens = mm.merge_on_matches()
    assert len(tokens) == 14
    assert len(merged_tokens) == 8
