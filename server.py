import click

from grts.server import start_server


@click.command()
def cli():
    start_server()
