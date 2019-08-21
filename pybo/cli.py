import click
from pathlib import Path

from pybo import Text, VERSION, rdr_2_replace_matcher, get_regex_pairs, batch_apply_regex


@click.group()
@click.version_option(VERSION)
def cli():
    pass


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def tok_file(**kwargs):
    click.echo(f'parsing {kwargs["filename"]}...')
    t = Text(Path(kwargs["filename"]))
    t.tokenize_words_raw_lines
    click.echo("done")


@cli.command()
@click.argument("string")
def tok_string(**kwargs):
    t = Text(kwargs["string"])
    click.echo(t.tokenize_words_raw_lines)


@cli.command()
@click.argument("infile", type=click.Path(exists=True))
def rdr2repl(**kwargs):
    infile = kwargs["infile"]
    outfile = infile.parent / (infile.stem + ".yaml")
    dump = infile.read_text(encoding="utf-8-sig")
    processed = rdr_2_replace_matcher(dump)
    outfile.write_text(processed, encoding="utf-8-sig")


@cli.command()
@click.argument('in-dir', type=click.Path(exists=True))
@click.argument('regex-file', type=click.Path(exists=True))
@click.option('-o', '--out-dir', type=click.Path(exists=True))
def fnr(**kwargs):
    # get the args
    indir = Path(kwargs["in_dir"])
    regex_file = Path(kwargs['regex_file'])
    out_dir = Path(kwargs['out_dir']) if kwargs['out_dir'] else None
    if not indir.is_dir():
        print('in-dir should be a folder, not a file.\nexiting...')
        exit(1)

    # generate rules
    rules = get_regex_pairs(regex_file.open(encoding='utf-8-sig').readlines())

    # apply on each file, prefixing each one with the regex filename
    for f in indir.rglob('*.txt'):
        if not f.stem.startswith('_'):
            string = f.read_text(encoding='utf-8-sig')
            out = batch_apply_regex(string, rules)
            name = f'_{regex_file.stem}__' + f.name
            if out_dir:
                outfile = out_dir / name
            else:
                outfile = f.parent / name
            outfile.write_text(out, encoding='utf-8-sig')


if __name__ == "__main__":
    cli()
