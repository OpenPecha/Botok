import re
from typing import NewType, List, DefaultDict, Tuple
from collections import defaultdict

from .token import Token
from .botokenizer import BoTokenizer
from .pybochunk import PyBoChunk

PyboToken = NewType('PyboToken', Token)


# ############################################ Helpers ############################################################### #

def is_skrt(syl):
    """Source for regexes : Paul Hackett Visual Basic script

    regex1: Now do Sanskrit: Skt.vowels, [g|d|b|dz]+_h, hr, shr, Skt
    regex2: more Sanskrit: invalid superscript-subscript pairs
    regex3: tsa-phru mark used in Chinese transliteration
    :param syl: syllable to assert
    :return: True if matches either of the regexes, False otherwise
    """
    regex1 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཱཱཱིུ-ཹཻཽ-ྃ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}" \
             r"[གཌདབཛྒྜྡྦྫ][ྷ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཤཧ][ྲ][ཀ-ཬཱ-྅ྐ-ྼ]{0,}|[ཀ-ཬཱ-྅ྐ-ྼ]{0,}" \
             r"[གྷཊ-ཎདྷབྷཛྷཥཀྵ-ཬཱཱཱིུ-ཹཻཽ-ྃྒྷྚ-ྞྡྷྦྷྫྷྵྐྵ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    regex2 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[ཀཁགང-ཉཏ-དན-བམ-ཛཝ-ཡཤཧཨ][ྐ-ྫྷྮ-ྰྴ-ྼ][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    regex3 = r"([ཀ-ཬཱ-྅ྐ-ྼ]{0,}[༹][ཀ-ཬཱ-྅ྐ-ྼ]{0,})"
    return re.search(regex1, syl) or re.search(regex2, syl) or re.search(regex3, syl)


def is_skrt_word(word):
    """Uses is_skrt() to check for sanskrit syllables

    """
    skrt = False
    syls = word.strip('་').split('་')
    for s in syls:
        if is_skrt(s):
            skrt = True

    return skrt


# ############################################ A. Preprocessing ###################################################### #

def dummy_preprocess(text: str) -> str:
    return text


def basic_cleanup(text: str) -> str:
    text = text.strip()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def basic_keeps_lines(text: str) -> str:
    text = text.strip()
    # text = re.sub(r'\s+', ' ', text)
    return text


# ############################################ B. Tokenizers ######################################################### #

def space_tok(text: str) -> List[str]:
    """Tokenizes string on spaces

    """
    return text.split(' ')


def bo_tok(text: str, profile: str) -> List[PyboToken]:
    tok = BoTokenizer(profile)
    return tok.tokenize(text)


def bo_syl_tok(text: str) -> List[str]:
    chunks = PyBoChunk(text)
    output = chunks.chunk()
    with_substrings = chunks.get_chunked(output)
    return [b for a, b in with_substrings]


# ############################################ C. Processors ######################################################### #

def dummy_process(tokens: List[str]) -> List[str]:
    # do nothing
    return tokens


def is_mistake(token):
    exceptions = ['\n']
    if token.type == 'syl' or token.type == 'non-bo':
        if (not token.skrt
            and not is_skrt_word(token.cleaned_content)) \
           and \
            (token.pos == 'oov'
             or token.pos == 'non-word'
             or token.type == 'non-bo') \
           and token.content not in exceptions:
            return True
    return False


def pybo_error_concs(tokens: List[PyboToken], left=5, right=5) -> DefaultDict[str, List[str]]:
    mistakes = defaultdict(list)
    for num, t in enumerate(tokens):
        if is_mistake(t):
            if num - left < 0:
                l = tokens[:num]
            else:
                l = tokens[num - left:num]
            if num + right > len(tokens)-1:
                r = tokens[num+1:]
            else:
                r = tokens[num+1:num+1+right]

            l_context = [t.content for t in l]
            r_context = [t.content for t in r]
            mis = t.content.replace('\n', '\\n')
            mistakes[mis].append([''.join(l_context), ''.join(r_context)])
    return mistakes


def pybo_error_types(tokens: List[PyboToken]) -> DefaultDict[str, int]:
    mistakes = defaultdict(int)
    for num, t in enumerate(tokens):
        if is_mistake(t):
            mis = t.content.replace('\n', '\\n')
            mistakes[mis] += 1
    return mistakes


def pybo_raw_types(tokens: List[PyboToken]) -> DefaultDict[str, int]:
    types = defaultdict(int)
    for t in tokens:
        occ = t.content.replace('\n', '\\n')
        types[occ] += 1
    return types


def pybo_raw_content(tokens: List[PyboToken]) -> List[str]:
    return [t.content for t in tokens]


# ############################################ D. Formatters ######################################################### #


def dummy_format(tokens: List[str]) -> List[str]:
    return tokens


def plaintext(tokens: List[str], sep: chr = ' ') -> str:
    # do nothing
    return sep.join(tokens)


def basic_conc(concs: List[Tuple[List[str], str, List[str]]], sep: chr = '\t', context_sep: chr = ' ', esc_context: bool = True) -> str:
    out = []
    for L, occ, R in concs:
        left = context_sep.join(L)
        right = context_sep.join(R)

        if esc_context:
            left, right = f'"{left}"', f'"{right}"'

        line = f'{left}{sep}{occ}{sep}{right}'
        out.append(line)

    return '\n'.join(out)


def stats_types(total_mistakes: DefaultDict[str, int], sep: chr = '\t') -> str:
    total = [(mis, freq) for mis, freq in total_mistakes.items()]
    total = sorted(total, reverse=True, key=lambda x: x[1])
    total = [f'{mis}{sep}{freq}' for mis, freq in total]
    return '\n'.join(total)


pipes = {
    # a. Preprocessing
    'pre': {
        'dummy': dummy_preprocess,
        'pre_basic': basic_cleanup,
        'pre_basic_lines': basic_keeps_lines,
    },
    # b. Tokenizers
    'tok': {
        'spaces': space_tok,
        'pybo': bo_tok,
        'syls': bo_syl_tok,
    },
    # c. Processors
    'proc': {
        'dummy': dummy_process,
        'pybo_raw_content': pybo_raw_content,
        'pybo_raw_types': pybo_raw_types,
        'pybo_types': pybo_error_types,
        'pybo_concs': pybo_error_concs,
    },
    # d. Formatters
    'frm': {
        'dummy': dummy_format,
        'plaintext': plaintext,
        'concs': basic_conc,
        'types': stats_types,
    }
}
