# coding: utf8
from pybo import Config
from pathlib import Path


def test_config():
    config = Config()

    # default config filename
    assert config.filename.name == 'pybo.yaml'  # config.filename is a Path object

    # paths for trie content
    main, custom = config.get_tok_data_paths('POS')
    # each profile contains one or more sections
    assert [m for m in main] == ['lexica_bo', 'lexica_non_inflected', 'lem_pos_freq']
    # each element in a Path object leading to a resource file
    assert isinstance(main['lem_pos_freq'][0], Path)

    # custom files to overwrite the existing trie can be added as follows
    modif_path = 'trie_data/'
    assert len(custom) == 0
    main, custom = config.get_tok_data_paths('POS', modifs=modif_path)
    expected = sorted(['lexica_bo', 'deactivate', 'lem_pos_freq', 'frequencies', 'lexica_skrt'])
    assert expected == sorted([c for c in custom]) == sorted([t.parts[-1] for t in Path(modif_path).glob('*')])

    # overwriting the main profile
    main, custom = config.get_tok_data_paths(modif_path, mode='custom')
    assert expected == sorted([m for m in main])
