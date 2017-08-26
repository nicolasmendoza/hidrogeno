"""
August 2017
hidrogeno app. coroutine.py
Author: Nicolás Mendoza.
"""
import collections
from hydrogen.core.db.models import  WheaterType
from .elements import RainGauge, PeriodTime

_WheaterStatsSummary = collections.namedtuple('WheaterStatsSummary', 'type lenght')


class WheaterStatisticAcummulator:
    """Acumulador estadistico para los diferentes tipos de clima.
    """

    def __init__(self):
        self.counter = collections.Counter()

    def save(self, key):
        """Aumenta contador para el tipo de key/clima especificado
        """
        self.counter[key] += 1


class WheaterStatsSumary(_WheaterStatsSummary):
    """WheaterStatsSummary es un objeto inmutable que contiene
    resumenes de estadísticas metereológicas disparadas desde una courotine"""
    pass


def weather_coroutine_statistics(max_days_to_process):
    """WheaterStatistic es una corutina que se encarga de acumular estadisticas enviadas
    desde un stream SpaceTime. Tiene toda la información organizada y al final de su cierre
    arroja un object StatsSummary con toda la información estadistica.

    :param endDay: Indica el número de registros que espera procesar, cuando se cumple, la rutina
    se cierra automaticamente y genera un StopIteration con toda la información estadistica acumulada,
    en un aplicación real la señal de cierre debería venir del stream... no de un StopIteration programado
    pero esto es slo un ejercicio.
    """
    _stats_started = False
    list_of_periods = collections.deque()  #high performance container, ideal para .appends()

    general_stats = WheaterStatisticAcummulator()
    current_period_opened = PeriodTime.empty_period()
    pluviometer = RainGauge()

    while True:
        current_day, current_wheater, precipitation_level = yield

        if current_day == max_days_to_process:
            break

        if _stats_started and current_period_opened.type != current_wheater:
            list_of_periods.append(current_period_opened)
        else:
            current_period_opened.extend()

        if not _stats_started:
            _stats_started = True
            current_period_opened = PeriodTime.new_period(current_day, current_wheater)

        # General Stats
        if current_wheater == WheaterType.DROUGHT:
            general_stats.save(WheaterType.DROUGHT)

        elif current_wheater == WheaterType.OPTIMUN:
            general_stats.save(WheaterType.OPTIMUN)

        elif current_wheater == WheaterType.RAINY:
            general_stats.save(WheaterType.RAINY)

            # recolectamos nivel de precipitación
            pluviometer.gather(current_day, precipitation_level)

        elif current_wheater == WheaterType.DEFAULT:
            general_stats.save(WheaterType.DEFAULT)

    return WheaterStatsSumary(pluviometer, general_stats)