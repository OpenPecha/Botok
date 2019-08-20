# coding: utf-8
from pathlib import Path


class PipelineBase:
    def __init__(self, profile, pipes=None):
        self.pipes = pipes

        self.prep = None
        self.tok = None
        self.mod = None
        self.form = None

        self.left = 5
        self.right = 5
        self.tok_params = None
        self.filename = (
            None
        )  # for an advanced mode, to show what conc comes from which file

        self.args_list = {
            "prep",
            "tok",
            "mod",
            "form",  # components
            "tok_params",  # pybo
            "left",
            "right",  # concs
            "filename",
        }  # others

        self.parse_profile(profile)

    def pipe_str(self, text: str) -> str:
        # a. preprocessing
        if self.prep:
            text = self.pipes["prep"][self.prep](text)

        # b. tokenizing
        if (
            isinstance(self.tok, str)
            and (
                "word" in self.tok or "sentence" in self.tok or "paragraph" in self.tok
            )
            and self.tok_params
        ):
            modifs = self.tok_params["modifs"] if "modifs" in self.tok_params else None
            mode = self.tok_params["mode"] if "mode" in self.tok_params else "internal"
            elts = self.pipes["tok"][self.tok](
                text, self.tok_params["profile"], modifs=modifs, mode=mode
            )
        else:
            elts = self.pipes["tok"][self.tok](text)

        # c. modifying
        mod = self.pipes["mod"][self.mod]
        if isinstance(self.mod, str) and self.mod.endswith("concs"):
            elts = mod(elts, left=self.left, right=self.right)
        else:
            elts = mod(elts)

        # d. formatting
        elts = self.pipes["form"][self.form](elts)

        return elts

    def pipe_file(self, filename: str, out_file: str):
        in_file = Path(filename)
        out_file = Path(out_file)
        assert in_file.is_file()

        with in_file.open(encoding="utf-8-sig") as f:
            dump = f.read()

        output = self.pipe_str(dump)

        with out_file.open("w", encoding="utf-8-sig") as g:
            g.write(output)

    def parse_profile(self, pipeline):
        self.is_valid_params(pipeline)
        for arg, v in pipeline.items():
            if arg == "prep":
                self.prep = v
            elif arg == "tok":
                self.tok = v
            elif arg == "mod":
                self.mod = v
            elif arg == "form":
                self.form = v
            elif arg == "tok_params":
                self.tok_params = v
            elif arg == "left":
                self.left = v
            elif arg == "right":
                self.right = v
            elif arg == "filename":
                self.filename = v
        self.is_valid_pipeline()

    def is_valid_params(self, pipeline):
        for arg, val in pipeline.items():
            # ensure all arguments are valid attributes
            if arg not in self.args_list:
                raise SyntaxError(
                    f'{arg} is not a valid argument\nvalid options are {" ".join(self.map)}'
                )

            # ensure arguments have valid values
            if arg in self.pipes and val not in self.pipes[arg]:
                raise SyntaxError(
                    f'{val} is not a valid value for {arg}\nvalid options are {" ".join(self.pipes[arg])}'
                )

    def is_valid_pipeline(self):
        # missing pipes
        if not self.tok or not self.mod or not self.form:
            raise BrokenPipeError(
                "A valid pipeline must have a tokenizer, a processor and a formatter."
            )
