# -*- coding: utf-8 -*-
import heapq
import datetime
import enum
import logging
import click

from hydrogen.core.job import WeatherWatcher
from hydrogen.core.galaxy.simulator import SpaceTime

NOW = datetime.datetime.now()


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
    """Lista de opciones la de línea de comandos."""

    CALCULATE_WHEATER_RAINY = 1
    CALCULATE_WHEATER_DROUGHT =2
    CALCULATE_WHEATER_OPTIMUN = 3
    INIT_WHEATER_JOB = 4


@click.option('--generardatos', default=365*10)
def init_db():

    click.echo('Procesando datos...')

    # creamos wheater watcher y le indicamos
    watcher = WeatherWatcher(lot_size=3000)

    with click.progressbar(SpaceTime.galaxy(from_day=0, to_day=10000), length=11360) as stream:
        for stream_data in stream:
            watcher.analyze(stream_data)

click.echo('Finish!')


def main():
    generate_entropy()

    opts = {
        CommandLineOption.CALCULATE_WHEATER_DROUGHT: 'Calcular cuántos períodos de sequía habrá.',

        CommandLineOption.CALCULATE_WHEATER_RAINY: 'Calcular cuántos períodos de lluvía habrá y qué día será '
                                                   'el pico máximo de lluvia',

        CommandLineOption.CALCULATE_WHEATER_OPTIMUN: 'Calcular cuántos períodos de condiciones óptimas de presión '
                                                     'y temperatura habrá',

        CommandLineOption.INIT_WHEATER_JOB: 'Volcar datos a bd con las condiciones climáticas de todos los días '
                                            '(utilizando "JOB" para calcularlas)'
    }

    click.echo('\nSeleccione una opción:\n')

    for opcion, descripcion in opts.items():
        click.echo('[{:d}] {:s}.'.format(opcion, descripcion))

    # Seleccionar opción
    show_options()


@click.command()
@click.option('--option', default=1, prompt='Seleccione una opción:')
def show_options(option):
    """Listado de opciones diponibles.
    *esta parte la hice sin mucha dedicación y contratiempo.
    """
    option_selected = click.echo(option)

    #todo #debt sacar festín de elifs, un command pattern u t iría mejor.

    if option == CommandLineOption.INIT_WHEATER_JOB.value:
        init_db()
    elif option == CommandLineOption.CALCULATE_WHEATER_DROUGHT:
        forecasting_drought()
    elif option == CommandLineOption.CALCULATE_WHEATER_OPTIMUN:
        pass
    elif option == CommandLineOption.CALCULATE_WHEATER_RAINY:
        pass
    else:
        click.echo('Debes seleccionar una opción')


from collections import Counter, namedtuple

WheaterReport = namedtuple('Result', 'count pluviometer peak_rain_day')









@click.command()
@click.option('--year', default=10, prompt='Escriba número de años a calcular. Default:')
def forecasting_drought(year):
    to_day = 365 * 10
    click.echo(to_day)
    END_DAY = 360

    # ponemos a escuchar una corutina indicandole cuantos registros espera antes de su cierre automático.
    wheater_stats_coro = weather_coroutine_statistics(END_DAY)
    next(wheater_stats_coro)

    with click.progressbar(SpaceTime.galaxy(from_day=0, to_day=END_DAY), length=to_day) as stream:
        for data in stream:
            # envíamos el día, el clima, y el nivel de precipitación a una corutina acumuladora.
            wheater_stats_coro.send((data.day, data.wheater, data.precipitation))

if __name__ == "__main__":
    main()