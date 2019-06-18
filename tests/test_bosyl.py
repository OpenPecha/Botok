# coding: utf8
from pybo import BoSyl

bs = BoSyl()


def test_bosyl():
    # is_affixable() Vs. SylComponents.is_thame()
    assert bs.is_thame('ཀུན') is False and bs.is_affixable('ཀུན') is False
    assert bs.is_thame('དེའིའམ') is True and bs.is_affixable('དེའིའམ') is False
    assert bs.is_thame('དེའི') is True and bs.is_affixable('དེའི') is False
    assert bs.is_thame('ང') is True and bs.is_affixable('ང') is True

    # get_all_affixed()
    affixed = bs.get_all_affixed('ང')
    assert affixed == [('ངར', {'len': 1, 'affix': 'la', 'aa': False}),
                       ('ངས', {'len': 1, 'affix': 'gis', 'aa': False}),
                       ('ངའི', {'len': 2, 'affix': 'gi', 'aa': False}),
                       ('ངའམ', {'len': 2, 'affix': 'am', 'aa': False}),
                       ('ངའང', {'len': 2, 'affix': 'ang', 'aa': False}),
                       ('ངའོ', {'len': 2, 'affix': 'o', 'aa': False}),
                       ('ངའིའོ', {'len': 4, 'affix': 'gi+o', 'aa': False}),
                       ('ངའིའམ', {'len': 4, 'affix': 'gi+am', 'aa': False}),
                       ('ངའིའང', {'len': 4, 'affix': 'gi+ang', 'aa': False}),
                       ('ངའོའམ', {'len': 4, 'affix': 'o+am', 'aa': False}),
                       ('ངའོའང', {'len': 4, 'affix': 'o+ang', 'aa': False})]

    affixed = bs.get_all_affixed('མཐའ')
    assert affixed == [('མཐར', {'len': 1, 'affix': 'la', 'aa': True}),
                       ('མཐས', {'len': 1, 'affix': 'gis', 'aa': True}),
                       ('མཐའི', {'len': 2, 'affix': 'gi', 'aa': True}),
                       ('མཐའམ', {'len': 2, 'affix': 'am', 'aa': True}),
                       ('མཐའང', {'len': 2, 'affix': 'ang', 'aa': True}),
                       ('མཐའོ', {'len': 2, 'affix': 'o', 'aa': True}),
                       ('མཐའིའོ', {'len': 4, 'affix': 'gi+o', 'aa': True}),
                       ('མཐའིའམ', {'len': 4, 'affix': 'gi+am', 'aa': True}),
                       ('མཐའིའང', {'len': 4, 'affix': 'gi+ang', 'aa': True}),
                       ('མཐའོའམ', {'len': 4, 'affix': 'o+am', 'aa': True}),
                       ('མཐའོའང', {'len': 4, 'affix': 'o+ang', 'aa': True})]

    affixed = bs.get_all_affixed('ཀུན')
    assert affixed == 'ཀུན'
