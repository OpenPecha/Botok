# coding: utf8
from botok import Config
from pathlib import Path


def test_config():
    config = Config()

    # default config filename
    assert config.filename.name == "botok.yaml"  # config.filename is a Path object

    # paths for trie content
    main, custom = config.get_tok_data_paths("POS")
    # each profile contains one or more sections
    assert [m for m in main] == ["words", "words_non_inflected"]
    # each element in a Path object leading to a resource file
    assert isinstance(main["words"][0], Path)

    # custom files to overwrite the existing trie can be added as follows
    modif_path = "trie_data/"
    assert not len(custom)
    main, custom = config.get_tok_data_paths("POS", modifs=modif_path)
    expected = sorted(["words", "words_skrt"])
    assert expected == sorted([c for c in custom])
    expected1 = sorted(["adjustment", "remove", "words", "words_skrt"])
    assert expected1 == sorted([t.parts[-1] for t in Path(modif_path).glob("*")])
    # overwriting the main profile
    main, custom = config.get_tok_data_paths(modif_path, mode="custom")
    expected = sorted(["words", "words_non_inflected", "words_skrt"])
    assert expected == sorted([m for m in main])


def test_adj_config():
    config = Config()
    modif_path = "trie_data"
    main, custom = config.get_adj_data_paths("basic", modifs=modif_path)
    assert "rdr_basis.tsv" == "".join([m.name for m in main])
    assert "test.tsv" == "".join([c.name for c in custom])
