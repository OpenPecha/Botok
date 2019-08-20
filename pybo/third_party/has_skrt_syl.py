# coding: utf-8
import re

from ..vars import TSEK


def is_skrt(syl):
    """Source for regexes : Paul Hackett Visual Basic script

    regex1: Now do Sanskrit: Skt.vowels, [g|d|b|dz]+_h, hr, shr, Skt
    regex2: more Sanskrit: invalid superscript-subscript pairs
    regex3: tsa-phru mark used in Chinese transliteration
    :param syl: syllable to assert
    :return: True if matches either of the regexes, False otherwise
    """
    regex1 = (
        r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཱཱཱིུ-ཹཻཽ-ྃ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}"
        r"[གཌདབཛྒྜྡྦྫ][ྷ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཤཧ][ྲ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}"
        r"[གྷཊ-ཎདྷབྷཛྷཥཀྵ-ཬཱཱཱིུ-ཹཻཽ-ྃྒྷྚ-ྞྡྷྦྷྫྷྵྐྵ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    )
    regex2 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཀཁགང-ཉཏ-དན-བམ-ཛཝ-ཡཤཧཨ][ྐ-ྫྷྮ-ྰྴ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    regex3 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[༹][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    return re.search(regex1, syl) or re.search(regex2, syl) or re.search(regex3, syl)


def has_skrt_syl(word):
    """Uses is_skrt() to check for sanskrit syllables

    """
    skrt = False
    syls = word.strip(TSEK).split(TSEK)
    for s in syls:
        if is_skrt(s):
            skrt = True

    return skrt
