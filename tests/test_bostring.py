# coding: utf8
import warnings

from botok import BoString
from botok import CharMarkers as m

bo_str = "བཀྲ་ཤིས་ ༡༢༣ tr  就到 郊外玩བདེ་ལེགས།"


def test_string():
    """Testing whether, at a given index, the char category corresponds to what is expected."""
    bs = BoString(bo_str)

    idx = 0
    assert "བ" == bo_str[idx]
    assert m.CONS == bs.base_structure[idx]

    idx = 2
    assert "ྲ" == bo_str[idx]
    assert m.SUB_CONS == bs.base_structure[idx]

    idx = 7
    assert "་" == bo_str[idx]
    assert m.TSEK == bs.base_structure[idx]

    idx = 9
    assert "༡" == bo_str[idx]
    assert m.NUMERAL == bs.base_structure[idx]

    idx = 13
    assert "t" == bo_str[idx]
    assert m.LATIN == bs.base_structure[idx]

    idx = 17
    assert "就" == bo_str[idx]
    assert m.CJK == bs.base_structure[idx]


def test_warning():
    with warnings.catch_warnings(record=True) as w:
        BoString("ༀ་པ་ཊུ་")
        assert len(w) == 1
        assert (
            str(w[0].message)
            == 'Beware of unexpected results: input string contains the non-expanded char "ༀ", found in "ༀ་པ་ཊུ".'
        )
