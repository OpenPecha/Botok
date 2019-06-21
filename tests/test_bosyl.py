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
    assert affixed == [('ངར', {'len': 1, 'type': 'la', 'aa': False}),
                       ('ངས', {'len': 1, 'type': 'gis', 'aa': False}),
                       ('ངའི', {'len': 2, 'type': 'gi', 'aa': False}),
                       ('ངའམ', {'len': 2, 'type': 'am', 'aa': False}),
                       ('ངའང', {'len': 2, 'type': 'ang', 'aa': False}),
                       ('ངའོ', {'len': 2, 'type': 'o', 'aa': False}),
                       ('ངའིའོ', {'len': 4, 'type': 'gi+o', 'aa': False}),
                       ('ངའིའམ', {'len': 4, 'type': 'gi+am', 'aa': False}),
                       ('ངའིའང', {'len': 4, 'type': 'gi+ang', 'aa': False}),
                       ('ངའོའམ', {'len': 4, 'type': 'o+am', 'aa': False}),
                       ('ངའོའང', {'len': 4, 'type': 'o+ang', 'aa': False})]

    affixed = bs.get_all_affixed('མཐའ')
    assert affixed == [('མཐར', {'len': 1, 'type': 'la', 'aa': True}),
                       ('མཐས', {'len': 1, 'type': 'gis', 'aa': True}),
                       ('མཐའི', {'len': 2, 'type': 'gi', 'aa': True}),
                       ('མཐའམ', {'len': 2, 'type': 'am', 'aa': True}),
                       ('མཐའང', {'len': 2, 'type': 'ang', 'aa': True}),
                       ('མཐའོ', {'len': 2, 'type': 'o', 'aa': True}),
                       ('མཐའིའོ', {'len': 4, 'type': 'gi+o', 'aa': True}),
                       ('མཐའིའམ', {'len': 4, 'type': 'gi+am', 'aa': True}),
                       ('མཐའིའང', {'len': 4, 'type': 'gi+ang', 'aa': True}),
                       ('མཐའོའམ', {'len': 4, 'type': 'o+am', 'aa': True}),
                       ('མཐའོའང', {'len': 4, 'type': 'o+ang', 'aa': True})]

    affixed = bs.get_all_affixed('ཀུན')
    assert affixed is None
