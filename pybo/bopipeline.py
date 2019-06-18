from pathlib import Path
from secrets import token_hex
from collections import namedtuple
from types import FunctionType

from .bopipes import pipes
from .config import Config


class Pipeline:
    def __init__(self, profile, new_pipes=None):
        self.pipes = pipes
        self.update_pipes(new_pipes)

        self.pre = None
        self.tok = None
        self.proc = None
        self.frm = None

        self.left = 5
        self.right = 5
        self.prof = None
        self.filename = None  # for an advanced mode, to show what conc comes from which file

        self.args_list = {
                          'pre', 'tok', 'proc', 'frm',  # components
                          'pybo_profile',               # pybo
                          'left', 'right',              # concs
                          'filename'                    # others
                          }

        self.config = Config('pybo.yaml')

        if isinstance(profile, dict):
            self.config.add_pipeline_profile(profile)
            profile = list(profile.keys())[0]  # prepare for next line

        self.parse_profile(self.config.get_pipeline_profile(profile))

    def update_pipes(self, new_pipes):
        """updates the default pipes with the ones provided

        :param new_pipes: should follow the following structure: {'pre': {'<name>: <func>, ...},
                                                                  'tok': {'<name>: <func>, ...},
                                                                  'proc': {'<name>: <func>, ...},
                                                                  'frm': {'<name>: <func>, ...}}
        """
        if new_pipes:
            for section, values in new_pipes.items():
                assert section in ['pre', 'tok', 'proc', 'frm'], 'Every pipe must fit in either sections: pre, tok, proc or frm'
                for name, func in values.items():
                    assert name not in self.pipes[section], 'The pipe ' + name + ' already exists in the pipes. Please rename it'
                    self.pipes[section][name] = func

    def pipe_str(self, text: str) -> str:
        # a. preprocessing
        if self.pre:
            text = pipes['pre'][self.pre](text)

        # b. tokenizing
        if self.tok == 'pybo':
            elts = pipes['tok'][self.tok](text, self.prof)
        else:
            elts = pipes['tok'][self.tok](text)

        # c. processing
        proc = pipes['proc'][self.proc]
        if self.proc.endswith('concs'):
            elts = proc(elts, left=self.left, right=self.right)
        else:
            elts = proc(elts)

        # d. formatting
        elts = pipes['frm'][self.frm](elts)

        return elts

    def pipe_file(self, filename: str, out_folder: str):
        in_file = Path(filename)
        out_dir = Path(out_folder)
        assert in_file.is_file()
        out_dir.mkdir(exist_ok=True)
        out_file = out_dir / in_file.name

        with in_file.open(encoding='utf-8-sig') as f:
            dump = f.read()

        output = self.pipe_str(dump)

        with out_file.open('w', encoding='utf-8-sig') as g:
            g.write(output)

    def parse_profile(self, pipeline):
        self.is_valid_params(pipeline)
        for arg, v in pipeline.items():
            if arg == 'pre':
                self.pre = v
            elif arg == 'tok':
                self.tok = v
            elif arg == 'proc':
                self.proc = v
            elif arg == 'frm':
                self.frm = v
            elif arg == 'pybo_profile':
                self.prof = v
            elif arg == 'left':
                self.left = v
            elif arg == 'right':
                self.right = v
            elif arg == 'filename':
                self.filename = v
        self.is_valid_pipeline()

    def is_valid_params(self, pipeline):
        for arg, val in pipeline.items():
            # ensure all arguments are valid attributes
            if arg not in self.args_list:
                raise SyntaxError(f'{arg} is not a valid argument\nvalid options are {" ".join(self.map)}')

            # ensure arguments have valid values
            if arg in pipes and val not in pipes[arg]:
                raise SyntaxError(f'{val} is not a valid value for {arg}\nvalid options are {" ".join(pipes[arg])}')

    def is_valid_pipeline(self):
        # missing pipes
        if not self.tok or not self.proc or not self.frm:
            raise BrokenPipeError('A valid pipeline must have a tokenizer, a processor and a formatter.')

        # detect pipeline inconsistencies through naming conventions
        if self.tok == 'pybo' and not self.prof:
            raise AttributeError('pybo tokenizer requires a profile as argument.')

        if (self.tok == 'pybo' and not self.proc.startswith('pybo')) \
           or (self.proc.startswith('pybo') and not self.tok == 'pybo'):
            raise BrokenPipeError('pybo tokenizer requires a pybo processor (both names start with "pybo").')

        if (self.proc.endswith('types') and not self.frm.endswith('types')) \
           or (self.frm.endswith('types') and not self.proc.endswith('types')):
            raise BrokenPipeError('types processor requires a types formatter (both names end with "types".')

        if (self.proc.endswith('concs') and not self.frm.endswith('concs')) \
           or (self.frm.endswith('concs') and not self.proc.endswith('concs')):
            raise BrokenPipeError('concs processor requires a concs formatter (both names end with "concs").')


class BoPipeline(Pipeline):
    def __init__(self, preprocessor, tokenizer, processor, formatter, pybo_profile=None):
        Ids = namedtuple('Ids', ['name', 'profile', 'pre', 'tok', 'proc', 'frm'])
        self.ids = Ids(token_hex(16), token_hex(16), token_hex(16),
                       token_hex(16), token_hex(16), token_hex(16))
        self.pipes = {'pre': {}, 'tok': {}, 'proc': {}, 'frm': {}}
        self.profile = {self.ids.name: {}}
        self.__create_pipeline(preprocessor, tokenizer, processor, formatter, pybo_profile)
        super().__init__(self.profile, self.pipes)

    def __create_pipeline(self, preprocessor, tokenizer, processor, formatter, pybo_profile):
        for a, b, c in [('pre', self.ids.pre, preprocessor),
                        ('tok', self.ids.tok, tokenizer),
                        ('proc', self.ids.proc, processor),
                        ('frm', self.ids.frm, formatter)]:
            if isinstance(c, FunctionType):
                self.pipes[a] = {b: c}
                self.profile[self.ids.name][a] = b
            elif isinstance(c, str):
                self.profile[self.ids.name][a] = c
            elif isinstance(c, tuple) and len(c) == 2:
                name, func = c
                assert isinstance(name, str)
                assert isinstance(func, FunctionType)
                self.pipes[a] = {name: func}
                self.profile[self.ids.name][a] = name
            else:
                raise SyntaxError('Should be either a function, a string or a tuple containing a string and a function')

        if pybo_profile and isinstance(pybo_profile, str):
            self.profile[self.ids.name]['pybo_profile'] = pybo_profile
