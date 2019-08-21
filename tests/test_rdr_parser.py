# coding: utf8
from pathlib import Path
from textwrap import dedent

from pybo import rdr_2_replace_matcher


def test_parse_rdr():
    f_path = Path(Path(__file__).parent / "resources/rdr_rules.txt")
    dump = f_path.read_text()
    res = rdr_2_replace_matcher(dump)
    expected = """\
 - repla: ['[pos="DET"] [pos="SCONJ"]', 2, '[pos="ADP"]']
 - repla: ['[pos="DET"] [pos="SCONJ" & text="སྟེ་"]', 2, '[pos="SCONJ"]']
 - repla: ['[pos="DET"] [pos="SCONJ" & text="ཅིང་"]', 2, '[pos="SCONJ"]']
 - repla: ['[pos="DET"] [pos="SCONJ" & text="ཞིང་"]', 2, '[pos="NOUN"]']
 - repla: ['[pos="DET"] [pos="SCONJ" & text="ཤིང་"]', 2, '[pos="NOUN"]']
 - repla: ['[pos="NOUN"] [pos="SCONJ"]', 2, '[pos="ADP"]']
 - repla: ['[pos="NOUN"] [pos="SCONJ" & text="སྟེ་"]', 2, '[pos="SCONJ"]']
 - repla: ['[pos="NOUN"] [pos="SCONJ" & text="ཏེ་"]', 2, '[pos="SCONJ"]']
 - repla: ['[pos="NOUN"] [pos="SCONJ" & text="ཞིང་"]', 2, '[pos="SCONJ"]']
 - repla: ['[pos="NOUN"] [pos="SCONJ" & text="ཤིང་"]', 2, '[pos="SCONJ"]']
 - repla: ['[pos="NOUN"] [pos="SCONJ" & text="ཤིང་"] [] [pos="ADP"]', 2, '[pos="NOUN"]']
 - repla: ['[pos="PRON"] [pos="SCONJ" & text="ནས་"]', 2, '[pos="ADP"]']
 - repla: ['[text="སུ་"] [pos="PRON"] [pos="SCONJ" & text="ནས་"]', 3, '[pos="SCONJ"]']
 - repla: ['[pos="NUM"] [pos="SCONJ"]', 2, '[pos="ADP"]']
 - repla: ['[pos="NUM"] [pos="SCONJ" & text="སྟེ་"]', 2, '[pos="SCONJ"]']
 - repla: ['[pos="ADP"] [pos="SCONJ"]', 2, '[pos="NOUN"]']
 - repla: ['[pos="NOUN"] [pos="ADP"] [pos="SCONJ" & text="ནས་"]', 3, '[pos="ADP"]']
 - repla: ['[pos="ADP"] [pos="SCONJ" & text="ཏེ་"]', 2, '[pos="SCONJ"]']"""
    assert res == expected
