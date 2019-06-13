# coding: utf-8
from secrets import token_hex
from collections import namedtuple
from types import FunctionType

from .pipelinebase import PipelineBase

from .preprocess import *
from .tokenize import *
from .modify import *
from .format import *


def dummy(objects):
    return objects


pipes = {
    # a. Preprocessing
    'prep': {
        'dummy': dummy,
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
    'mod': {
        'dummy': dummy,
        'pybo_raw_content': pybo_raw_content,
        'pybo_raw_types': pybo_raw_types,
        'pybo_types': pybo_error_types,
        'pybo_concs': pybo_error_concs,
    },
    # d. Formatters
    'form': {
        'dummy': dummy,
        'plaintext': plaintext,
        'concs': basic_conc,
        'types': stats_types,
    }
}


class Pipeline(PipelineBase):
    def __init__(self, preprocessor, tokenizer, modifier, formatter, pybo_profile=None):
        ### replace with a Enum
        Ids = namedtuple('Ids', ['name', 'profile', 'prep', 'tok', 'mod', 'form'])
        self.ids = Ids(token_hex(16), token_hex(16), token_hex(16),
                       token_hex(16), token_hex(16), token_hex(16))
        self.pipes = {'prep': {}, 'tok': {}, 'mod': {}, 'form': {}}
        self.profile = {self.ids.name: {}}
        self.__create_pipeline(preprocessor, tokenizer, modifier, formatter, pybo_profile)
        super().__init__(self.profile, pipes)

    def __create_pipeline(self, preprocessor, tokenizer, modifier, formatter, pybo_profile):
        for a, b, c in [('prep', self.ids.prep, preprocessor),
                        ('tok', self.ids.tok, tokenizer),
                        ('mod', self.ids.mod, modifier),
                        ('form', self.ids.form, formatter)]:
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
