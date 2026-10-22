"""
Tests for botok.utils.lenient_normalization.normalize_punctuation.
"""
import pytest

from botok.utils.lenient_normalization import normalize_punctuation, remap_offsets


def norm(s, **kw):
    return normalize_punctuation(s, **kw)


# ===========================================================================
# Regressions: bugs of the previous implementation (old output in comments)
# ===========================================================================

class TestRegressions:
    def test_space_is_not_a_shad(self):
        # old: ཧྲཱིཿ། དངོས
        assert norm("ཧྲཱིཿ དངོས") == "ཧྲཱིཿ དངོས"

    def test_line_break_kept_by_default(self):
        # old: སངས། རྒྱས (\n became a space, then a shad)
        assert norm("སངས་\nརྒྱས") == "སངས་\nརྒྱས"

    def test_double_shad_kept(self):
        # old: ཡིན་ནོ། ཡང
        assert norm("ཡིན་ནོ། །ཡང") == "ཡིན་ནོ། །ཡང"

    def test_four_shads_become_two(self):
        # old: སོ། ཡང
        assert norm("སོ།། །།ཡང") == "སོ། །ཡང"

    def test_gter_tsheg_kept(self):
        # old: དངོས་གྲུབ། ཨེ
        assert norm("དངོས་གྲུབ༔ ཨེ") == "དངོས་གྲུབ༔ ཨེ"

    def test_yig_mgo_removal_keeps_shads_and_separation(self):
        # old: ལཾལམ་
        assert norm("ལཾ། །\n\n༄༅། །ལམ", original_eol=False) == "ལཾ། །ལམ"

    def test_opening_yig_mgo_kept(self):
        # old: ཆོས་
        assert norm("༄༅། །ཆོས", original_eol=False) == "༄༅། །ཆོས"

    def test_no_tsheg_added_at_end_of_text(self):
        # old: ཆོས་ (with original_eol=False)
        assert norm("ཆོས", original_eol=False) == "ཆོས"

    def test_implicit_double_shad_after_ga_kept(self):
        # old: ཅིག བློ (ག ། is ག + implicit shad + shad: a double shad)
        assert norm("ཅིག །བློ") == "ཅིག །བློ"
        assert norm("ཅིག། །བློ") == "ཅིག །བློ"

    def test_no_tsheg_between_visarga_and_shad(self):
        # old: ངཿ་། (and a trailing space)
        assert norm("ངཿ།") == "ངཿ།"

    def test_rin_chen_spungs_shad_not_doubled(self):
        # old: ཏུ༑། ཡང
        assert norm("ཏུ༑ ཡང") == "ཏུ། ཡང"

    def test_no_trailing_space_after_final_shad(self):
        # old: ཡིན་ནོ། (with a trailing space)
        assert norm("ཡིན་ནོ།") == "ཡིན་ནོ།"


# ===========================================================================
# Rules
# ===========================================================================

class TestCharacterVariants:
    def test_tsheg_variants(self):
        assert norm("ཀ\u0f0cཁ\u0fd2ག") == "ཀ་ཁ་ག"

    @pytest.mark.parametrize("shad", ["\u0f0f", "\u0f10", "\u0f11", "\u0f12"])
    def test_shad_variants(self, shad):
        assert norm(f"ཏེ{shad} ཡང") == "ཏེ། ཡང"

    def test_nyis_shad(self):
        assert norm("སོ\u0f0eཡང") == "སོ། །ཡང"


class TestSpaces:
    def test_space_runs_and_unicode_spaces(self):
        assert norm("ཧྲཱིཿ \u00a0\t\u3000དངོས") == "ཧྲཱིཿ དངོས"

    def test_space_around_newline(self):
        assert norm("སངས་ \n རྒྱས") == "སངས་\nརྒྱས"

    def test_windows_line_breaks(self):
        assert norm("སངས་\r\nརྒྱས") == "སངས་\nརྒྱས"

    def test_trailing_space(self):
        assert norm("ཧྲཱིཿ \nཨོཾ ") == "ཧྲཱིཿ\nཨོཾ"


class TestTsheg:
    def test_tsheg_runs(self):
        assert norm("ཞེས་་་་གསུངས") == "ཞེས་གསུངས"

    def test_space_after_tsheg(self):
        assert norm("ཁ་ ག") == "ཁ་ག"

    def test_space_before_tsheg(self):
        assert norm("ཁ ་ག") == "ཁ་ག"

    def test_tsheg_before_shad(self):
        assert norm("དོན་། ཡང") == "དོན། ཡང"

    def test_tsheg_before_gter_tsheg(self):
        assert norm("གྲུབ་༔ ཨེ") == "གྲུབ༔ ཨེ"

    def test_visarga_tsheg(self):
        assert norm("ཧཿ་ཡང") == "ཧཿཡང"


class TestYigMgo:
    def test_opening_normalized(self):
        assert norm(" ༄། །ཆོས") == "༄༅། །ཆོས"
        assert norm("༄༅༅།།ཆོས") == "༄༅། །ཆོས"

    def test_inner_yig_mgo_removed_closing_shads_kept(self):
        assert norm("བཞུགས། ༄༅༅། །དཀྱིལ") == "བཞུགས། དཀྱིལ"
        assert norm("ཅད། །\n\n༄༅། །སྒྲུབ") == "ཅད། །\n\nསྒྲུབ"

    def test_sbrul_shad_removed(self):
        assert norm("ཚོམས། ༈ བལ") == "ཚོམས། བལ"


class TestShad:
    def test_at_most_two_shads(self):
        assert norm("ལོ། ། ། །ཞེས") == "ལོ། །ཞེས"

    def test_single_shad_followed_by_space(self):
        assert norm("ཏེ།ཡང") == "ཏེ། ཡང"

    def test_no_space_before_shad(self):
        assert norm("ཏེ ། ཡང") == "ཏེ། ཡང"

    def test_double_shad_followed_by_text(self):
        assert norm("སོ། ། ཡང") == "སོ། །ཡང"

    def test_shad_at_line_end(self):
        assert norm("ཏེ། \nཡང") == "ཏེ།\nཡང"


class TestKaGaSha:
    def test_single_shad_carried(self):
        assert norm("ཐུག།ཕྱག") == "ཐུག ཕྱག"

    def test_tsheg_shad_after_ga_is_single(self):
        assert norm("ཐུག་།ཕྱག") == "ཐུག ཕྱག"

    def test_double_shad(self):
        assert norm("ཐུག། །ཕྱག") == "ཐུག །ཕྱག"
        assert norm("ཐུག ། །ཕྱག") == "ཐུག །ཕྱག"

    def test_with_vowel(self):
        assert norm("དགེ། བཀྲ") == "དགེ བཀྲ"
        assert norm("ཀུ། །ཡང") == "ཀུ །ཡང"

    def test_ka_and_sha(self):
        assert norm("ཀ། ཁ") == "ཀ ཁ"
        assert norm("ཤི་། ཡང") == "ཤི ཡང"

    def test_subscript_and_superscript_keep_shad(self):
        assert norm("གྲུ། །ཡང") == "གྲུ། །ཡང"
        assert norm("སྐུ། ཡང") == "སྐུ། ཡང"

    def test_visarga_keeps_shad(self):
        assert norm("ཀཿ། ཡང") == "ཀཿ། ཡང"

    def test_line_end(self):
        assert norm("ཐུག།\nཕྱག") == "ཐུག\nཕྱག"


class TestNga:
    def test_tsheg_added(self):
        assert norm("རྟེན་དང། ཡང") == "རྟེན་དང་། ཡང"

    def test_tsheg_kept(self):
        assert norm("རྟེན་དང་། ཡང") == "རྟེན་དང་། ཡང"

    def test_with_space_before_shad(self):
        assert norm("དང ། ཡང") == "དང་། ཡང"

    def test_with_vowel(self):
        assert norm("ཞེས་བྱ་ངོ།") == "ཞེས་བྱ་ངོ་།"


class TestGterTsheg:
    def test_runs(self):
        assert norm("ཧོ༔༔རང") == "ཧོ༔ རང"
        assert norm("གྲུབ༔༔ རང") == "གྲུབ༔ རང"

    def test_use_gter_shad(self):
        assert norm("ཡིན་ནོ། །ཡང་། ཐུག།ཕྱག", use_gter_shad=True) == "ཡིན་ནོ༔ ཡང༔ ཐུག༔ ཕྱག"
        assert norm("༄༅། །དང ། ཐུག ། །ཕྱག", use_gter_shad=True) == "༄༅། །དང༔ ཐུག༔ ཕྱག"


class TestJoinLines:
    def test_tsheg_added_between_syllables(self):
        assert norm("སངས\nརྒྱས", original_eol=False) == "སངས་རྒྱས"

    def test_existing_tsheg(self):
        assert norm("སངས་\nརྒྱས", original_eol=False) == "སངས་རྒྱས"

    def test_ka_ga_sha_line_end_is_a_shad(self):
        assert norm("ཐུག\nཕྱག", original_eol=False) == "ཐུག ཕྱག"

    def test_after_shad(self):
        assert norm("ཏེ།\nཡང", original_eol=False) == "ཏེ། ཡང"
        assert norm("སོ། །\n\nཡང", original_eol=False) == "སོ། །ཡང"


class TestProperties:
    SAMPLE = " ༄། །ཀ་ཁ།། །།༄༅། །ག་ང ། ཅ་ཆ༑ཐུག ། །ཧོ༔༔ རང་་ཞེས། \n\n༄༅། །ཡང"

    @pytest.mark.parametrize("kw", [{}, {"original_eol": False}, {"use_gter_shad": True}])
    def test_idempotent(self, kw):
        once = norm(self.SAMPLE, **kw)
        assert norm(once, **kw) == once

    def test_positions(self):
        text, pos, counts = normalize_punctuation(self.SAMPLE, return_positions=True)
        assert text == norm(self.SAMPLE)
        assert len(pos) == len(text) + 1 and pos[-1] == len(self.SAMPLE)
        assert all(a <= b for a, b in zip(pos, pos[1:]))
        assert counts["yig_mgo"] == 3 and "double_shad" in counts

    def test_remap_offsets(self):
        src = "ཀ་ཁ།། །།ག་ང ། ཅ་ཆ"
        text, pos, _ = normalize_punctuation(src, return_positions=True)
        a, b, c = remap_offsets([0, src.index("ག"), src.index("ཅ")], pos)
        assert a == 0 and text[b] == "ག" and text[c:] == "ཅ་ཆ"
