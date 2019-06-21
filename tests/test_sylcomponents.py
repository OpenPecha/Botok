# coding: utf8
from pybo import SylComponents


def test_components():
    sc = SylComponents()

    # A) get_parts()
    # 1. (prefix+main-stack, vowel+suffixes)
    assert sc.get_parts('བཀྲིས') == ('བཀྲ', 'ིས')
    # 2. (exceptions, 'x')
    assert sc.get_parts('མདྲོན') == ('མདྲོན', 'x')
    # 3. a list of solutions if there is more than one (not yet encountered)
    # 4. None if the syllable is not wellformed
    assert sc.get_parts('ཀཀ') is None

    # B) get_mingzhi()
    assert sc.get_mingzhi('བསྒྲུབས') == 'ྒ'
    # the mingzhi that will serve for the particle agreement:
    assert sc.get_mingzhi('ཁྱེའུར') == 'འ'
    # None if more than one solution from get_parts() (not yet encountered)

    # support for dadrag
    assert sc.get_mingzhi('ཀུནད') == 'ཀ'

    # dadrag normalize
    assert sc.normalize_dadrag('ཀུནད') == 'ཀུན'

    # C) get_info()
    # 1. 'dadrag'
    # A syllable that historically received a "da" second suffix.
    # As for now, the list contains ["ཀུན", "ཤིན", "འོན"] (See pybo/resources/SylComponents.json)
    assert sc.get_info('ཀུན') == 'dadrag'
    # 2. 'thame'
    # A syllable that has the potential of hosting an affixed particle.
    # Will be returned for all such syls, whether or not a particle is affixed.
    assert sc.get_info('དེའིའམ') == 'thame'
    assert sc.get_info('དེའི') == 'thame'
    # 3 the syllable itself in all other cases
    assert sc.get_info('ང') == 'thame'
    assert sc.get_info('རྒྱལ') == 'རྒྱལ'

    # D) is_thame()
    # True if the syllabe is affixable or is already affixed, False otherwise
    assert sc.is_thame('ཀུན') is False
    assert sc.is_thame('དེའིའམ') is True
    assert sc.is_thame('དེའི') is True
    assert sc.is_thame('ང') is True
