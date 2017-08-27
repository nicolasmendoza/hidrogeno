# -*- coding: utf-8 -*-
"""
Este módulo contiene elementos estadisticos y la subrutina encargada
de clasificar y ordenar los pronósticos del tiempo.
"""
import collections

from ...db.models import WheaterType
from ...wheater.statistics.elements import RainGauge, PeriodTime


class WheaterStatisticAcummulator(collections.Counter):
    """Acumulador estadístico para los diferentes tipos de clima.
    """
    pass


_WheaterStatsSummary = collections.namedtuple('WheaterStatsSummary', 'pluviometer periods general')


class WheaterStatsSumary(_WheaterStatsSummary):
    """WheaterStatsSummary es un objeto inmutable que contiene
    resumenes de estadísticas metereológicas disparadas desde coroutine.py

    pluviometer: contiene los datos estadisticos del nivel de precipitación
    periods : contiene listado ordenado de los periodos, su duración y otros datos estadisticos.
    general: contiene las estadísticas generales. Ejemplo: cuántos días de lluvía por año, etc.
    """

    @property
    def general_stats(self):
        """Retorna el número total de días para cada clima en un ciclo de 360 días"""


    @property
    def periods_summary(self):
        """Retorna un resumen de los periodos"""
        if self.periods:
            summary = 'En un ciclo de 360 días el pronóstico es el siguiente: '
            for k, v in self.periods.items():
                summary += "\n tendremos {} periodos, Clima: {}.".format(v, k.value)

            return summary

        return "No data"


def weather_coroutine_statistics(max_days_to_process):
    """WheaterStatistic es una subrutina que se encarga de acumular estadisticas enviadas
    desde un stream SpaceTime. Tiene toda la información organizada y al final de su cierre
    arroja un object StatsSummary con toda la información estadistica.

    :param endDay: Indica el número de registros que espera procesar, cuando se cumple, la rutina
    se cierra automaticamente y genera un StopIteration con toda la información estadistica acumulada,
    en un aplicación real la señal de cierre debería venir del stream... no de un StopIteration programado
    pero esto es slo un ejercicio.
    """
    _stats_started = False

    current_period_opened = None
    general_stats = WheaterStatisticAcummulator()
    pluviometer = RainGauge()
    periods = collections.Counter()

    while True:
        current_day, current_wheater, precipitation_level = yield

        if current_day == max_days_to_process:
            break

        if current_period_opened and current_period_opened.type is WheaterType.RAINY:
            # Recolectamos nivel de precipitación del período actual
            pluviometer.gather(precipitation_level, current_day)

        if _stats_started and current_period_opened.type != current_wheater:
            periods[current_period_opened.type] += 1
            current_period_opened = PeriodTime.new_period(current_day, current_wheater)

        elif _stats_started and current_period_opened:
            current_period_opened.extend()

        if not _stats_started:
            _stats_started = True
            current_period_opened = PeriodTime.new_period(current_day, current_wheater)

        # General Stats,número total de días
        if current_wheater == WheaterType.DROUGHT:
            general_stats[WheaterType.DROUGHT] += 1

        elif current_wheater == WheaterType.OPTIMUN:
            general_stats[WheaterType.OPTIMUN] += 1

        elif current_wheater == WheaterType.RAINY:
            general_stats[WheaterType.RAINY] += 1

        elif current_wheater == WheaterType.DEFAULT:
            general_stats[WheaterType.DEFAULT] += 1

    return WheaterStatsSumary(pluviometer, periods, general_stats)


def listen_stream(lenght):
    """Levantar coroutine. en un escenario real..esto debería
    ir con un decorator y no usar una cr primitiva con cierre abrupto.
    :param lenght: cantidad de datos a procesar, después de eso se cierra
    con un StopIteration.
    :return: retorna un WheaterStatsSummary
    """
    wheater_stats_coro = weather_coroutine_statistics(lenght)
    next(wheater_stats_coro)
    return wheater_stats_coro

