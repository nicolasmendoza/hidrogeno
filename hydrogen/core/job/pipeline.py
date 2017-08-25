"""
La pipeline es usada por el "Job", se desacopla para aplicar cualquier filtro o estrategia a la data
recibida vía SpaceTime generator. Se retorna siempre un WheaterForeCastModel para persistencia en db.
Es slo para mostrar otra estrategía con el manejo de datos en el caso del "job", esto fue causal porque
inicialmente empecé a hacerlo todo de manera Async pero era como "matar una mosca de un cañonazo", entonces decidí
dejar por lo menos la parte de "tuberias".
"""
from ..db.models import WheaterForeCastModel, WheaterType


def wheater_drought(galaxy_report):
    """Cuando los tres planetas están alineados entre si y a su vez alineados
    con respecto al sol, el sistema solar experimenta un periodo de sequía.

    WheaterType.DROUGHT
    """
    return WheaterForeCastModel(
        day=galaxy_report.day,
        wheater=WheaterType.DROUGHT.value,
        precipitation=galaxy_report.get_precipitation
    )


def wheater_rainy(galaxy_report):
    """ Cuando los tres planetas no están alineados, forman entre si un
    triángulo. Es sabido que en el momento en que el se encuentra dentro del triángulo,
    el sistema solar experimenta un periodo de lluvia, teniendo éste, un pico de intensidad
    cuando el perímetro del triángulo está en su máximo.

    WheaterType.RAINY

    """
    return WheaterForeCastModel(
        day=galaxy_report.day,
        wheater=WheaterType.RAINY.value,
        precipitation=galaxy_report.get_precipitation
    )


def wheater_optimun(galaxy_report):
    """Cuando los tres planetas están alineados entre sí pero no están alineados con
    el sol, el sistema solar experimenta un clima "optimo" con condiciones óptimas
    de presión y temperatura.

    WheaterType.OPTIMUN
    """
    return WheaterForeCastModel(
        day=galaxy_report.day,
        wheater=WheaterType.OPTIMUN.value,
        precipitation=galaxy_report.get_precipitation
    )


def default_wheater(galaxy_report):
    """
    Cuando los planetas y el sol se encuentran en una posición no señalada,
        entonces se considera en un status "default", lo llamaremos de momento:
        clima "stándar".

        WheaterType.STANDARD
    :param data:
    :return:
    """
    return WheaterForeCastModel(
        day=galaxy_report.day,
        wheater=WheaterType.DEFAULT.value,
        precipitation=galaxy_report.get_precipitation
    )
