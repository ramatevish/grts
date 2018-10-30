import click

from grts.acquire import SENSORS


def _get_sensor(name):
    for sensor in SENSORS:
        if sensor.name == name:
            return sensor


@click.command()
@click.option('--sensor', '-s', multiple=True, default='', help='Which sensors should be checked.')
def cli(sensor):
    for name in sensor:
        s = _get_sensor(name)
        if s is None:
            click.echo(err=f"Couldn't find sensor 'name'")
        click.echo(f"'{name}': {s.read()}")
