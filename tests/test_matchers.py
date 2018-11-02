from pybo import *
from pathlib import Path

rules_path = Path(__file__).parent / "resources" / "rules"


input_str = ' མཐའི་རྒྱ་མཚོའི་གླིང་། ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ'
tok = BoTokenizer('POS')
tok.tok.trie.rebuild_trie()
tokens = tok.tokenize(input_str)


def test_cql_query():
    query = '[content="ན"] []'
    q = Query(query)
    assert q


def test_cql():
    query = '[pos="NOUN" & content!=""] []'
    matcher = CQLMatcher(query)
    slices = matcher.match(tokens)
    slice_strings = [tuple([tokens[i].content for i in range(start, end + 1)]) for start, end in slices]
    assert slices == [(0, 1), (2, 3), (4, 5), (7, 8), (13, 14), (14, 15)]
    assert slice_strings == [(' མཐ', 'འི་'), ('རྒྱ་མཚོ', 'འི་'), ('གླིང་', '། '), ('བཀྲ་ཤིས་  ', 'tr '),
                             ('བཀྲ་ཤིས་', 'བདེ་ལེགས་'), ('བདེ་ལེགས་', 'ཀཀ')]


def test_token_split():
    ts = TokenSplit(tokens[2], 1, token_changes='[tag="SPACE" & pos="PUNCT" & aa_word="False" & affixed="False"] []')
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
    assert len(tokens) == 16  # TODO: should be 14. same remark as below
    assert len(split_tokens) == 20  # TODO: should be 19, but there is a token with a single tsek.


def test_match_merge():
    match_query = '[pos="NOUN" & content!=""] []'
    replace_idx = 1  # slot number in match query
    replace = '[tag="XXX" & pos="xxx"]'

    mm = MergingMatcher(match_query, replace_idx, tokens, replace)
    merged_tokens = mm.merge_on_matches()
    assert len(tokens) == 16  # TODO: should be 14. same remark as above
    assert len(merged_tokens) == 11  # TODO: should be 8. same remark as above


def test_match_replace():
    match_query = '[pos="NOUN" & content!=""] []'
    replace_idx = 1
    replace = '[tag="XXX" & pos="xxx"]'

    ReplacingMatcher(match_query, replace_idx, tokens, replace).replace_on_matches()
    assert len(tokens) == 16
    assert tokens[0].pos == 'xxx'
    assert tokens[1].pos == 'PART'


def test_adjust_tokens():
    # string = 'ན་ན་ན་སྟེ་ན་བས་དགའ།། རྐྱེན་ངན་གྱིས་བར་དུ་མ་ཆོད་ཅིང་། །'
    # token_list = tok.tokenize(string, split_affixes=False)
    # at = AdjustTokens(rules_folder=rules_path)
    # adjusted = at.adjust(token_list)
    # assert token_list[9].content == 'བར་'
    # assert token_list[10].content == 'དུ་མ་'
    # assert token_list[11].content == 'ཆོད་'

    # assert adjusted[9].content == 'བར་དུ་'
    # assert adjusted[9].pos == 'PART'
    # assert adjusted[10].content == 'མ་'
    # assert adjusted[10].pos == 'PART'
    # assert adjusted[11].content == 'ཆོད་'

    string= 'ལ་ལ་ལ་ལ་ལ་བ་ཡོད།'
    token_list = tok.tokenize(string, split_affixes=False)
    at = AdjustTokens(rules_folder=rules_path)
    adjusted = at.adjust(token_list)
    assert token_list[0].content == 'ལ་ལ་'
    assert token_list[1].content == 'ལ་ལ་'

    assert adjusted[0].content == 'ལ་'
    assert adjusted[0].pos == 'PART'
    assert adjusted[1].content == 'ལ་ལ་'
    assert adjusted[1].pos == 'PART'
    assert adjusted[2].content == 'ལ་'
    assert adjusted[2].pos == 'PART'
