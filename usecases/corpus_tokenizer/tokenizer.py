from pybo import BoTokenizer
import PySimpleGUI as sg
from pathlib import Path
import yaml


class MarkupObj:
    def __init__(self):
        self._ = {'markup': True}  # dict for any user specific data
        self.content = ''

    def __repr__(self):
        out = 'content: {}\n'.format(self.content)
        for k, v in self._.items():
            out += "_{}: {}\n".format(k, v)
        return out


class CorpusTokenizer:
    def __init__(self, tokenizer):
        self.VER_START = '༺'
        self.vern_normal_start = False
        self.VER_SEP = '།'
        self.vern_has_trans = False
        self.VER_STOP = '༻'
        self.vern_normal_stop = False

        self.VER_NOORTH = '༙'
        self.vern_noorth = False

        self.UNCLEAR = '༼༽'

        self.ONOMA_START = '༼༼'
        self.onoma_start = False
        self.ONOMA_STOP = '༽༽'
        self.onoma_stop = False

        self.GUESS_START = '༼'
        self.guess_start = False
        self.GUESS_STOP = '༽'
        self.guess_stop = False

        self.BORROW_START = '（'
        self.borrowing_start = False
        self.BORROW_STOP = '）'
        self.borrowing_stop = False

        self.NOEND = '་་་'
        self.meta = ['ཕོ་མིང་', 'མོ་མིང་', 'དོགས་གཞིའི་ཚིག']
        self.tok = tokenizer

    @staticmethod
    def add_current_elt(chunks, tmp, elt, marker):
        if tmp:
            chunks.append(tmp)
        chunks.append((marker, elt))
        return ''

    @staticmethod
    def print_context(in_str, i):
        left = i - 20
        right = i + 20
        if left < 0:
            left = 0
        if right > len(in_str) - 1:
            right = len(in_str) - 1
        return in_str[left:right]

    def all_markers_ok(self):
        return not self.vern_normal_start \
               and not self.vern_normal_stop \
               and not self.vern_has_trans \
               and not self.vern_noorth \
               and not self.onoma_start \
               and not self.onoma_stop \
               and not self.guess_start \
               and not self.guess_stop \
               and not self.borrowing_start \
               and not self.borrowing_stop

    def chunk_corpus(self, in_str):
        chunks = []
        tmp = ''
        i = 0
        while i < len(in_str):

            # vernacular with or without translation
            if in_str[i] == self.VER_START:
                tmp = self.add_current_elt(chunks, tmp, self.VER_START, 'vern_start')
                if not self.all_markers_ok(): self.print_context(in_str, i)
                self.vern_normal_start = True

            elif self.vern_normal_start and in_str[i] == self.VER_SEP:
                tmp = self.add_current_elt(chunks, tmp, self.VER_SEP, 'vern_sep')
                self.vern_has_trans = True

            elif in_str[i] == self.VER_STOP:
                tmp = self.add_current_elt(chunks, tmp, self.VER_STOP, 'vern_end')

                if not self.vern_normal_start:
                    print('closing vernacular marker without the opening one:', self.print_context(in_str, i))
                if self.vern_has_trans and type(chunks[-2]) != str:
                    print('the vernacular translation marker is not followed by any translation:', self.print_context(in_str, i))

                    self.vern_has_trans = False
                if not self.vern_normal_start:
                    self.vern_normal_stop = True
                self.vern_normal_start = False

            # vernacular without conventional orthography
            elif in_str[i] == self.VER_NOORTH:
                if not self.vern_noorth:
                    tmp = self.add_current_elt(chunks, tmp, self.VER_NOORTH, 'vern_no_start')
                    if not self.all_markers_ok(): self.print_context(in_str, i)
                    self.vern_noorth = True
                else:
                    tmp = self.add_current_elt(chunks, tmp, self.VER_NOORTH, 'vern_no_end')
                    self.vern_noorth = False

            # unclear speech
            elif in_str[i:i+2] == self.UNCLEAR:
                tmp = self.add_current_elt(chunks, tmp, self.UNCLEAR, 'unclear')
                i += 1

            # onomatopeias
            elif in_str[i:i+2] == self.ONOMA_START:
                tmp = self.add_current_elt(chunks, tmp, self.ONOMA_START, 'onoma_start')
                if not self.all_markers_ok(): self.print_context(in_str, i)
                self.onoma_start = True
                i += 1
            elif in_str[i:i+2] == self.ONOMA_STOP:
                tmp = self.add_current_elt(chunks, tmp, self.ONOMA_STOP, 'onoma_end')
                self.onoma_stop = False
                i += 1

            # guesses / doubts
            elif in_str[i] == self.GUESS_START:
                tmp = self.add_current_elt(chunks, tmp, self.GUESS_START, 'guess_start')
                self.guess = True
            elif in_str[i] == self.GUESS_STOP:
                tmp = self.add_current_elt(chunks, tmp, self.GUESS_STOP, 'guess_end')
                self.guess = False

            # borrowings
            elif in_str[i] == self.BORROW_START:
                tmp = self.add_current_elt(chunks, tmp, self.BORROW_START, 'borrowing_start')
                if not self.all_markers_ok(): self.print_context(in_str, i)
                self.borrowing = True
            elif in_str[i] == self.BORROW_STOP:
                tmp = self.add_current_elt(chunks, tmp, self.BORROW_STOP, 'borrowing_end')
                self.borrowing = False

            elif in_str[i:i+3] == self.NOEND:
                tmp = self.add_current_elt(chunks, tmp, self.NOEND, 'unfinished')
                i += 2

            else:
                tmp += in_str[i]

            i += 1

        if tmp:
            chunks.append(tmp)

        return chunks

    def corpus_tokens(self, in_str):
        def mark_tokens(tokens, mark):
            for t in tokens:
                t._['type'] = mark

        chunks = self.chunk_corpus(in_str)
        tokens = []
        current_mark = ''
        one_shot_mark = ''
        for chunk in chunks:
            if type(chunk) == tuple:
                marker, string = chunk
                tmp = MarkupObj()
                tmp.content = string
                if marker.endswith('start'):
                    current_mark = marker.replace('_start', '')
                    tmp._['type'] = current_mark + '_mark'
                if marker.endswith('end'):
                    tmp._['type'] = current_mark + '_mark'
                    current_mark = ''
                    one_shot_mark = ''
                if marker == 'unclear' \
                        or marker == 'unfinished':
                    one_shot_mark = marker
                    tmp._['type'] = one_shot_mark
                    one_shot_mark = ''
                elif marker == 'vern_sep':
                    one_shot_mark = marker
                    tmp._['type'] = one_shot_mark
                tokens.append(tmp)

            else:
                if chunk in self.meta:
                    tmp = MarkupObj()
                    tmp.content = chunk
                    tmp._['type'] = 'meta'
                    tokens.append(tmp)

                else:
                    tmp = self.tok.tokenize(chunk)
                    if one_shot_mark == 'vern_sep':
                        mark_tokens(tmp, 'translation')
                        one_shot_mark = ''
                    elif current_mark:
                        mark_tokens(tmp, current_mark)
                    tokens.extend(tmp)
        return tokens


def get_vocab_files(vocab_folder):
    """helper function to get the absolute paths of all .txt files in a give dir"""
    files = Path(vocab_folder).glob('*.txt')
    abs_file_paths = [Path().cwd() / f for f in files]
    return abs_file_paths


if __name__ == '__main__':
    in_str = '''ལག་ཁུག་མདར་བོ་་་༺ཟིག་།ཞིག་༻གི་ནང་༺ང་།ལ་༻གོན་༺གྱི་།རྒྱུ་༻བཞག་༺ཡོ་ཁུ་།ཡོད་ཀི༻ 
༺དོ་ཚིགས་།ད་ལོ་༻ ༺ཟེ་།ཟེར་༻ནི་༺རེ་།རེད་༻༙པཱ་༙ 
ཁྱག་ནི་རེ། ༼དོགས་གཞིའི་ཚིག༽  （健康证）
༼དོགས་གཞིའི་ཚིག༽ ཀན་༺ན་།ལ་༻ངས་གཅིག་འདྲི་ཨ༻  ༼༽
སློབ་གྲྭ་ར་༺བ་།བར་༻བལྟས་ན་༺ཨུ་།ཨེ་༻ཡིན། ལྟ་༺གྱི་ཟིག་ཡོ་ཁུ་༻ཡ། ༺འདི་ཆེ་ཁ་ཟིག་རེ་དྲ་།འདི་ཡིས་ཆེ་ནི་འདྲ་ཞིག་རེད་དེ།༻  
གང་གི་ལམ། ༺མོས་རས་།མ་གིའི་༻ལམ་༺ཟེ་༻ནི་༺ཨུ་༻ཡིན། ༺དུ་རེ་།དེ་རེད།༻ 
༺རང་ང་།རང་བཞིན་༻ ༺ངེ་ཀི་།ངེད་ཀི་༻རྒན་མོ་བརྟག་དཔྱད་༺ཟིག་༻ ༺ཡེད་ཀི་།བྱེད་ཀི་༻འགྲོ་ནི་ཡིན། 
༺སྒ་བ་།སྒལ་བ་༻ ༺ཟིག་༻ ༺ཁོས་འུ་།ན་གི་༺ཟེ་གི་༻ རྒྱ་གྲམ་དམར་༺རོ་།པོ་༻ ཨེ། ཇོ་བོ་རིན་པོ་༼མོ་མིང་༽༺ཨུ་༻ཡིན། 
ཨ་ལ། ༼༼ཧ་ཧ་ཧ་ཧ་༽༽ སྐྱེ་དངོས་སྲུང་སྐྱོབས་༺ཡེ་གྱི་བོ་༻ལོ་༺དུ་འུ་༻རིང་༺ང་༻སྲུང་སྐྱོབས་་་ ༺ཁ་ཕྱེ་སོ་།ཁ་ཕྱེ་ལུགས་༻མ་ཤེས་༙ཁྱིར་༙ སོང་༺ངིས་༻'''

    tok = BoTokenizer('GMD', toadd_filenames=get_vocab_files('vocabs'))
    corpus = CorpusTokenizer(tok)

    tokens = corpus.corpus_tokens(in_str)

    print('ok')
