import click
from pathlib import Path

from pybo import Text, VERSION


@click.group()
@click.version_option(VERSION)
def cli():
    pass


@cli.command()
@click.argument('filename')
def file(**kwargs):
    click.echo(f'parsing {kwargs["filename"]}...')
    t = Text(Path(kwargs['filename']))
    t.tokenize_words_raw_lines
    click.echo('done')


@cli.command()
@click.argument('string')
def string(**kwargs):
    t = Text(kwargs['string'])
    click.echo(t.tokenize_words_raw_lines)


if __name__ == '__main__':
    cli()
