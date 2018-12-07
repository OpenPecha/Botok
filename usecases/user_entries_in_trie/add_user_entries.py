from pybo import BoTokenizer
from pathlib import Path


def get_vocab_files(vocab_folder):
    """helper function to get the absolute paths of all .txt files in a give dir"""
    files = Path(vocab_folder).glob('*.txt')
    abs_file_paths = [Path().cwd() / f for f in files]
    return abs_file_paths


if __name__ == '__main__':
    custom_vocab_filenames = get_vocab_files('vocabs')

    tok = BoTokenizer('POS', toadd_filenames=custom_vocab_filenames)

    in_str = 'བཀྲ་ཤིས་བདེ་ལེགས། ཀཀཀ། པཔཔ།'
    tokens = tok.tokenize(in_str)
    for t in tokens:
        print(f'{t.content}: {t.pos}')

            # བཀྲ་ཤིས་: NOUN
            # བདེ་ལེགས: NOUN
            # །: punct
            # ཀཀཀ: TEST
            # །: punct
            # པཔཔ: TEST
            # །: punct
