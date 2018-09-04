from pybo import BoTokenizer
from pathlib import Path
import yaml


def get_vocab_files(profile, profiles, vocab_folder):
    assert Path(vocab_folder).is_dir()
    assert profile in profiles

    abs_paths = [Path().cwd() / vocab_folder / v for v in profiles[profile]]
    return abs_paths


def get_tokenized_string(tokens):
    out = []
    for t in tokens:
        if t.type != 'syl':
            out.append(t.content)
        else:
            out.append(t.unaffixed_word)
    return out


def tokenize_folder(in_folder, out_folder='output', user_vocabs=[], suffix='_tokenized'):
    in_folder = Path(in_folder)
    out_folder = Path(out_folder)

    assert in_folder.is_dir()           # check the input folder exists
    out_folder.mkdir(exist_ok=True)     # ensure the output folder exists

    tok = BoTokenizer('POS', user_word_list=user_vocabs)

    in_files = in_folder.glob('*.txt')
    for f in in_files:
        content = f.read_text(encoding='utf-8-sig')
        tokens = tok.tokenize(content)
        out = get_tokenized_string(tokens)
        out = ' '.join(out)
        out_file = out_folder / str(f.stem + suffix + f.suffix)
        out_file.write_text(out, encoding='utf-8-sig')


def main():
    config = yaml.load(Path('conf.yaml').read_text(encoding='utf-8-sig'))

    profile = config['Exec']['profile']
    vocab_path = config['Exec']['vocab_path']
    vocab_profiles = config['Profiles']
    suffix = config['Exec']['tokenized_suffix']

    user_paths = get_vocab_files(profile, vocab_profiles, vocab_path)
    tokenize_folder('input', 'output', user_vocabs=user_paths, suffix=suffix)


if __name__ == '__main__':
    main()
