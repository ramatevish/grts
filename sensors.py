import click

from grts.acquire import SENSORS


def _get_sensor(name):
    for sensor in SENSORS:
        if sensor.name == name:
            return sensor


@click.command()
@click.option('--list-all', '-a', is_flag=True, default=False,
              help='Check all sensors.')
@click.option('--sensor', '-s', 'sensors', multiple=True, default='',
              help='Specify which sensors should be checked.')
def cli(sensors, list_all):
    if list_all:
        for sensor in SENSORS:
            click.echo("%s: %s" % (sensor.name, sensor.read()))
    else:
        for sensor in sensors:
            sensor = _get_sensor(sensor)
            if sensor is None:
                click.echo(err="Couldn't find sensor '%s'" % sensor)
            click.echo("%s: %s" % (sensor.name, sensor.read()))
