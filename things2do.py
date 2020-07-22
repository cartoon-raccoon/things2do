import click
import sys

@click.group()
def cli():
    pass

@cli.command()
@click.option('--hi', default="dude", required=True)
def hello(hi):
    click.echo(f"Hello {hi}")