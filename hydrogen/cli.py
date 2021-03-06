# -*- coding: utf-8 -*-
"""
Este módulo es el punto de entrada __main__ para la útilidad de comando.
"""
import datetime
import enum
import click

from . import conf
from .core.wheater.job.watcher import WeatherWatcher
from .core.wheater.statistics import coroutine as coro
from .core.wheater.statistics.coroutine import WheaterStatsSumary
from .core.galaxy.simulator import SpaceTime

NOW = datetime.datetime.now()

ONE_HUMAN_YEAR = 365
ONE_VULCAN_YEAR = 72
ONE_BETASOIDE_YEAR = 120
ONE_FERENGI_YEAR = 360


def generate_entropy():
    click.clear()
    click.echo('| |  | (_)   | |')
    click.echo('| |__| |_  __| |')
    click.echo("|  __  | |/ _` | '__/ _ \ / _` |/ _ \ '_ \ / _ ")
    click.echo("| |  | | | (_| | | | (_) | (_| |  __/ | | | (_) |")
    click.echo("|_|  |_|_|\__,_|_|  \___/ \__, |\___|_| |_|\___(_)")
    click.echo("                          __/ |")
    click.echo("                         |___/")


class CommandLineOption(enum.IntEnum):
    """Lista de opciones de la app, línea de comandos.
    """
    FORECASTING = 1
    INIT_WHEATER_JOB = 2


@click.option('--generardatos', default=365*10)
def init_db():

    if conf.DATABASE_URL != conf.DEFAULT_DB:   #wk. contratiempo.
        click.echo('Procesando datos...')

        # Creamos un object WheaterWatcher y le indicamos el número de lotes a envíar a db.
        watcher = WeatherWatcher(lot_size=conf.JOB_BATCHER)
        space_time = SpaceTime.galaxy(from_day=0, to_day=conf.JOB_WORK)

        with click.progressbar(space_time, length=conf.JOB_WORK) as stream:
            for stream_data in stream:
                watcher.analyze(stream_data)

        click.echo('done!')
    else:
        click.echo('!'*80)
        click.echo('\n\n Antes de continuar necesitas setear la variable de entorno HIDROGENO_DB con la '
                   'URL de la base de datos a usar')
        click.echo('\n Para más información ver la documentación.\n')
        click.echo('!' * 80)

def main():
    generate_entropy()

    opts = {
        CommandLineOption.FORECASTING: 'Pronóstico de Clima por Años. (simulación)',
        CommandLineOption.INIT_WHEATER_JOB: 'Volcar datos a bd con las condiciones climáticas de todos los días '
                                            '(utilizando "JOB" para calcularlas)'
    }
    click.echo('\nSeleccione una opción:\n')
    for opcion, descripcion in opts.items():
        click.echo('[{:d}] {:s}.'.format(opcion, descripcion))
    # mostrar opciones
    show_options()


@click.command()
@click.option('--option', default=1, prompt='Seleccione una opción:')
def show_options(option):
    """Listado de opciones diponibles.
    """
    if option == CommandLineOption.INIT_WHEATER_JOB.value:
        init_db()
    elif option == CommandLineOption.FORECASTING:
        forecast_wheater()
    else:
        click.echo('Debes seleccionar una opción')


@click.command()
@click.option('--years', default=10, prompt='Indique el número de años a predecir. Default (10):')
def forecast_wheater(years):

    days_to_calculate = 360 * years

    # llamammos subrutina, indicandole cuántos registros procesar antes de su cierre "automático".
    coro_stats = coro.listen_stream(days_to_calculate)

    try:

        click.echo('preparando simulación de {} años. {} días...'.format(years, days_to_calculate))

        # iniciamos "simulación" planetaria...partiendo del día Cero.
        data_space_stream = SpaceTime.galaxy(from_day=0, to_day=days_to_calculate)

        with click.progressbar(data_space_stream, length=days_to_calculate) as stream:

            for data in stream:
                # envíamos el (día, el clima, y el nivel de precipitación) para estadísticas.
                coro_stats.send(
                    (data.day, data.wheater, data.precipitation)
                )

    except StopIteration as result:

        if isinstance(result.value, WheaterStatsSumary):

            # predicciones y datos estadísticos después de la "simulación"
            forecasting = result.value
            click.echo('*' * 100)

            # mostramos pronóstico del tiempo...
            click.echo(forecasting.periods_summary)
            click.echo(forecasting.pluviometer.summary)
            click.echo(forecasting.general_stats)
        else:
            raise

if __name__ == "__main__":
    main()
