from pybo import BoTokenizer
import PySimpleGUI as sg
from pathlib import Path
import yaml


default_config = '''Exec:
    profile: Amdo1
    tok_profile: POS
    vocab_path: vocabs
    input_folder: input
    output_folder: output
    tokenized_suffix: _tokenized
    rebuild_trie: False

Profiles:
    Amdo1:
        - མཚོ་སྔོན་རྐང་ཚ།.txt'''


def get_vocab_files(config):
    vocab_folder = config['Exec']['vocab_path']
    profile = config['Exec']['profile']
    profiles = config['Profiles']

    assert Path(vocab_folder).is_dir()
    assert profile in profiles

    abs_paths = [Path().cwd() / vocab_folder / v for v in profiles[profile]]
    return abs_paths


def get_tokenized_string(tokens):
    out = []
    for t in tokens:
        if '༺' in t.content or '༻' in t.content:
            out.append(t.content.replace('༺', '[').replace('༻', ']'))
        elif t.type != 'syl':
            out.append(t.content)
        else:
            out.append(t.unaffixed_word)
    return out


def tokenize_folder(config, user_vocabs=[]):
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
        out = get_tokenized_string(tokens)
        out = ' '.join(out).replace('\n ', '\n')
        out_file = out_folder / str(f.stem + suffix + f.suffix)
        out_file.write_text(out, encoding='utf-8-sig')


def main(config):
    config = yaml.load(config)

    user_paths = get_vocab_files(config)
    tokenize_folder(config, user_paths)


def GUI(config):
    while True:
        with sg.FlexForm('Folder Tokenizer') as form:

            layout = [[sg.Multiline(default_text=config, scale=(2, 10))],
                      [sg.Submit(button_text='Tokenize'), sg.Quit()]]

            button, (new_config,) = form.LayoutAndRead(layout)
            if button == 'Tokenize':
                if config != new_config:
                    main(new_config)
                else:
                    main(config)
            else:
                if config != new_config:
                    Path('conf.yaml').write_text(new_config)
                break


if __name__ == '__main__':
    # ensure config.yaml exists with default values
    if not Path('conf.yaml').exists():
        Path('conf.yaml').write_text(default_config)
    raw_config = Path('conf.yaml').read_text(encoding='utf-8-sig')
    GUI(raw_config)
