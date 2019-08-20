import click
from pathlib import Path

from pybo import Text, VERSION, parse_rdr_rules


@click.group()
@click.version_option(VERSION)
def cli():
    pass


@cli.command()
@click.argument('filename')
def tok_file(**kwargs):
    click.echo(f'parsing {kwargs["filename"]}...')
    t = Text(Path(kwargs['filename']))
    t.tokenize_words_raw_lines
    click.echo('done')


@cli.command()
@click.argument('string')
def tok_string(**kwargs):
    t = Text(kwargs['string'])
    click.echo(t.tokenize_words_raw_lines)


@cli.command()
@click.argument('infile')
def parse_rdr(**kwargs):
    infile = Path(kwargs['infile'])
    if not infile.is_file():
        raise FileExistsError(f'{infile} was not found.\nexiting...')
    dump = infile.read_text(encoding='utf-8-sig')
    rdr = parse_rdr_rules(dump)
    outfile = infile.parent / (infile.stem + '.yaml')
    outfile.write_text(rdr, encoding='utf-8-sig')


if __name__ == '__main__':
    cli()
