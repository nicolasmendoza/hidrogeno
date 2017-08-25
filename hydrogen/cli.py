import click
from hydrogen.core.job import WeatherWatcher
from hydrogen.core.galaxy.simulator import SpaceTime


@click.command()
@click.option('--option', default=1, prompt='Seleccione una opción:')
def show_options(option):
    """
    Pipeline...para las opciones disponibles.
    :param opcion:
    :return:
    """

    value = click.echo(option)

    if option == 1:
        init_db()


def init_db():
    click.echo('Inicializando database...')
    try:
        watcher = WeatherWatcher()
        for stream_data in SpaceTime.galaxy(from_day=0, to_day=360):
            watcher.analyze(stream_data)

    except Exception as e:
        click.echo(e)


def main():
    """
 | |  | (_)   | |
 | |__| |_  __| |_ __ ___   __ _  ___ _ __   ___
 |  __  | |/ _` | '__/ _ \ / _` |/ _ \ '_ \ / _ \
 | |  | | | (_| | | | (_) | (_| |  __/ | | | (_) |
 |_|  |_|_|\__,_|_|  \___/ \__, |\___|_| |_|\___(_)
                            __/ |
                           |___/
    """
    # Opciones app.
    opts = {
        2: 'Calcular cuántos períodos de sequía habrá.',
        3: 'Calcular cuántos períodos de lluvía habrá y qué día será el pico máximo de lluvia',
        4: 'Calcular cuántos períodos de condiciones óptimas de presión y temperatura habrá',
        5: 'Generar datos con las condiciones climáticas de todos los días (utilizando JOB para calcularlas)'
    }

    click.echo('Seleccione una opción:')

    for opcion, descripcion in opts.items():
        click.echo('[{:d}] {:s}.'.format(opcion, descripcion))

    # Seleccionar opción
    show_options()

if __name__ == "__main__":
    main()
