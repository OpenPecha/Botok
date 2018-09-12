# workflow:
# 1. tokenize canon, all tokenized files are in output/tokenized
# 2. parse all types of non-words and OOV, from tokenized files : output/types
#    (gather stats about how many instances of each time in what file + total)
# 3. for each type, parse the whole output folder and generate a syllable-based concordance
#    + file name in the first column : output/concordances


from pybo import BoTokenizer
from pathlib import Path
import yaml
from collections import defaultdict


default_config = '''Exec:
    profile: ''
    tok_profile: GMD
    vocab_path: vocabs
    input_folder: input
    output_folder: output/tokenized/
    tokenized_suffix: _tokenized
    rebuild_trie: False

Profiles:
    Amdo1:
        - མཚོ་སྔོན་རྐང་ཚ།.txt'''


def get_vocab_files(config):
    vocab_folder = config['Exec']['vocab_path']
    profile = config['Exec']['profile']
    profiles = config['Profiles']

    if profile == '':
        return []

    assert Path(vocab_folder).is_dir()
    assert profile in profiles

    abs_paths = [Path().cwd() / vocab_folder / v for v in profiles[profile]]
    return abs_paths


def process_folders(config, format_func, user_vocabs=[]):
    in_folder = config['Exec']['input_folder']
    out_folder = config['Exec']['output_folder']
    tok_profile = config['Exec']['tok_profile']
    suffix = config['Exec']['tokenized_suffix']

    in_folder = Path(in_folder)
    out_folder = Path(out_folder)

    assert in_folder.is_dir()           # check the input folder exists
    out_folder.mkdir(exist_ok=True)     # ensure the output folder exists

    tok = BoTokenizer(tok_profile, user_word_list=user_vocabs)
    if bool(config['Exec']['rebuild_trie']):
        tok.tok.trie.rebuild_trie()

    in_files = in_folder.glob('*.txt')
    for f in in_files:
        content = f.read_text(encoding='utf-8-sig')
        tokens = tok.tokenize(content)
        out = format_func(tokens)
        out = ' '.join(out).replace('\n ', '\n')
        out_file = out_folder / str(f.name)
        out_file.write_text(out, encoding='utf-8-sig')


def tokenize_folder(format_func):
    """
    :param format_func: a function taking as input a list of tokens,
                        giving as output a list of strings
    """
    # ensure config.yaml exists with default values
    if not Path('tok_folder.yaml').exists():
        Path('tok_folder.yaml').write_text(default_config)
    raw_config = Path('tok_folder.yaml').read_text(encoding='utf-8-sig')

    config = yaml.load(raw_config)
    user_paths = get_vocab_files(config)
    process_folders(config, format_func, user_paths)


def mark_oov_nonword(tokens):
    out = []
    for t in tokens:
        token = t.content.replace(' ', '_')
        if t.pos == 'oov'or t.pos == 'non-word':
            out.append(f'#{token}')
        else:
            out.append(token)
    return out


def get_oov_nonword_types():
    folder = Path('output/tokenized')
    nonword = defaultdict(dict)
    for f in folder.glob('*.txt'):
        content = f.read_text(encoding='utf-8-sig').split('\n')
        words = [word for c in content for word in c.split(' ')]
        for w in words:
            w = w.rstrip('་')
            if '#' in w:
                w = w.lstrip('#')
                if w not in nonword[w]:
                    nonword[w][f.stem] = 0
                nonword[w][f.stem] += 1

    nonword_out = ''
    for k, v in nonword.items():
        nonword_out += f'\n{k}\n'
        total = 0
        for kk, vv in v.items():
            nonword_out += f'\t{kk}:\t\t{vv}\n'
            total += vv
        nonword_out += f'\ttotal:\t\t{total}\n'

    Path('output/types/nonwords.txt').write_text(nonword_out, encoding='utf-8-sig')
    return nonword


def create_concs(marked, left=5, right=5):
    for token in marked:
        concs = []
        total_occurences = sum(marked[token].values())

        # find concs
        tok_folder = Path('output/tokenized')
        for f in tok_folder.glob('*.txt'):
            content = f.read_text(encoding='utf-8-sig').split('\n')
            words = [word for c in content for word in c.split(' ')]
            for num, w in enumerate(words):
                w = w.rstrip('་').lstrip('#').lstrip('$')
                if w == token:
                    l_adjust = 0
                    while num - left + l_adjust < 0:
                        l_adjust += 1
                    r_adjust = 0
                    while num + 1 + right - r_adjust > len(words):
                        r_adjust += 1
                    l_conc = words[num - left + l_adjust:num]
                    while len(l_conc) < 5:
                        l_conc = [''] + l_conc
                    r_conc = words[num + 1: num + 1 + right - r_adjust]
                    while len(r_conc) < 5:
                        r_conc = r_conc + ['']
                    concs.append((l_conc, words[num], r_conc))

        # format concs
        out = 'L5\tL4\tL3\tL2\tL1\tA\tR1\tR2\tR3\tR4\tR5\n'
        for c in concs:
            out += '\t'.join(c[0] + [c[1]] + c[2]) + '\n'

        out_file = Path(f'output/concordances/') / f'{total_occurences}_{token}.tsv'
        out_file.write_text(out)


def main():
    tok_folder = Path('output/tokenized')
    if tok_folder.is_dir() and len(list(tok_folder.glob('*.txt'))) == 0:
        tokenize_folder(mark_oov_nonword)
    nonword = get_oov_nonword_types()
    create_concs(nonword)


if __name__ == '__main__':
    main()
