# coding: utf8
from collections import defaultdict
from pathlib import Path

from botok import BoSyl, Config, TokChunks, Trie

config = Config()


def syls(string):
    return TokChunks(string).get_syls()


def test_createtrie():
    profile = "empty"
    config = Config.from_path("./tests/data/trie_dialect_pack")
    bt = Trie(BoSyl, profile, config.dictionary, config.adjustments)

    # the trie works as expected. but the add() method should never be used directly:
    # it does not inflect entries, so the tokenizer won't work as expected.
    # be careful only to use it with words that can't ever be inflected, like case particles.
    bt.add(syls("གྲུབ་མཐའ་"), {"pos": "NOUN"})
    assert bt.has_word(syls("གྲུབ་མཐའི་")) == {"exists": False, "data": {"_": {}}}

    # use inflect_n_modify_trie() instead, to add entries
    bt.inflect_n_modify_trie("གྲུབ་མཐའ་")
    assert bt.has_word(syls("གྲུབ་མཐའི་")) == {
        "exists": True,
        "data": {"_": {}, "affixation": {"len": 2, "type": "gi", "aa": True}},
    }

    bt.inflect_n_modify_trie("ཀ་ར་", skrt=True)
    assert bt.has_word(syls("ཀ་རར་")) == {
        "exists": True,
        "data": {
            "_": {},
            "affixation": {"len": 1, "type": "la", "aa": False},
            "skrt": True,
            "senses": [{"lemma": "", "affixed": True}],
        },
    }  # arrives here because skrt was True

    bt.inflect_n_add_data(
        "གྲུབ་མཐའ་\t\t\t\t532"
    )  # 'freq' is hard-coded in Trie, just as 'lemma' and 'pos' are
    assert bt.has_word(syls("གྲུབ་མཐའི་")) == {
        "exists": True,
        "data": {
            "_": {},
            "affixation": {"len": 2, "type": "gi", "aa": True},
            "senses": [{"freq": 532, "affixed": True}],
        },
    }  # freq is an int

    # just like add() was not meant to be used directly, deactivate() is not
    # instead, use bt.inflect_n_modify_trie("word", deactivate=True)
    bt.deactivate(syls("ཀ་ར་"))
    assert (
        bt.has_word(syls("ཀ་ར་"))["exists"] is False
    )  # since 'ཀ་ར་' has been deactivated


def test_multiple_words_per_entry():
    profile = "POS"
    config = Config.from_path("./tests/data/trie_dialect_pack")
    bt = Trie(BoSyl, profile, config.dictionary, config.adjustments)

    res = bt.has_word(syls("ལྟར་"))
    assert {"lemma": "ལྟ་", "pos": "VERB", "freq": 123, "affixed": True} in res["data"][
        "senses"
    ]
    assert {"lemma": "ལྟར་", "pos": "ADV", "freq": 456, "affixed": False} in res[
        "data"
    ]["senses"]
