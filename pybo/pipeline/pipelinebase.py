# coding: utf-8
from pathlib import Path

from ..config import Config


class PipelineBase:
    def __init__(self, profile, pipes=None):
        self.pipes = pipes

        self.prep = None
        self.tok = None
        self.mod = None
        self.form = None

        self.left = 5
        self.right = 5
        self.prof = None
        self.filename = None  # for an advanced mode, to show what conc comes from which file

        self.args_list = {'prep', 'tok', 'mod', 'form',  # components
                          'pybo_profile',                # pybo
                          'left', 'right',               # concs
                          'filename'}                    # others

        self.config = Config('pybo.yaml')

        if isinstance(profile, dict):
            self.config.add_pipeline_profile(profile)
            profile = list(profile.keys())[0]  # prepare for next line

        self.parse_profile(self.config.get_pipeline_profile(profile))

    def pipe_str(self, text: str) -> str:
        # a. preprocessing
        if self.prep:
            text = self.pipes['prep'][self.prep](text)

        # b. tokenizing
        if self.tok == 'pybo':
            elts = self.pipes['tok'][self.tok](text, self.prof)
        else:
            elts = self.pipes['tok'][self.tok](text)

        # c. processing
        proc = self.pipes['mod'][self.mod]
        if self.mod.endswith('concs'):
            elts = proc(elts, left=self.left, right=self.right)
        else:
            elts = proc(elts)

        # d. formatting
        elts = self.pipes['form'][self.form](elts)

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
            if arg == 'prep':
                self.prep = v
            elif arg == 'tok':
                self.tok = v
            elif arg == 'mod':
                self.mod = v
            elif arg == 'form':
                self.form = v
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
            if arg in self.pipes and val not in self.pipes[arg]:
                raise SyntaxError(f'{val} is not a valid value for {arg}\nvalid options are {" ".join(self.pipes[arg])}')

    def is_valid_pipeline(self):
        # missing pipes
        if not self.tok or not self.mod or not self.form:
            raise BrokenPipeError('A valid pipeline must have a tokenizers, a processor and a formatter.')

        # detect pipeline inconsistencies through naming conventions
        if self.tok == 'pybo' and not self.prof:
            raise AttributeError('pybo tokenizers requires a profile as argument.')

        if (self.tok == 'pybo' and not self.mod.startswith('pybo')) \
           or (self.mod.startswith('pybo') and not self.tok == 'pybo'):
            raise BrokenPipeError('pybo tokenizers requires a pybo processor (both names start with "pybo").')

        if (self.mod.endswith('types') and not self.form.endswith('types')) \
           or (self.form.endswith('types') and not self.mod.endswith('types')):
            raise BrokenPipeError('types processor requires a types formatter (both names end with "types".')

        if (self.mod.endswith('concs') and not self.form.endswith('concs')) \
           or (self.form.endswith('concs') and not self.mod.endswith('concs')):
            raise BrokenPipeError('concs processor requires a concs formatter (both names end with "concs").')
