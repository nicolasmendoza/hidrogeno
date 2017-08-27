# -*- coding: utf-8 -*-
"""
Elementos usados para pronóstico de tiempo.
"""

class RainGauge(object):
    """Representa un pluviometro, es usado en coroutine.py como
    acumulador del stream de precipitation.
    """

    def __init__(self, level=0, day=0):
        self.level = level
        self.day = day
        self.more_days = []
        self.levels = []

    def gather(self, liquid, day):
        """Actualiza el nivel actual y día si el nivel de "líquido"
        es mayor al actual.
        """
        if liquid > self.level:
            self.level = liquid
            self.day = day

        elif liquid == self.level:
            self.levels.append(liquid)
            self.more_days.append(day)

    @property
    def summary(self):
        """Retorna resúmen del registro de precipitaciones almacenado"""
        summary = "\n El pico máximo de lluvía será el día: {} ." \
                  "\n Con una precipitación de: {:f} .\n".format(self.day, self.level)
        if len(self.more_days):
            summary += "\nTambién habrá lluvía intensa los días: {} \n ".format(self.more_days)
        return summary

    @property
    def peak_day(self):
        """Día con con el pico máximo de lluvía"""
        return self.day

    @property
    def precipitation(self):
        """Nivel de precipitación"""
        return self.level

    @property
    def all_peak_days(self):
        """Retorna todos los días con alta precipitación"""
        return self.more_days


class PeriodTime(object):
    """Representa un periodo de tiempo, es usado para
    acumular los periodos de tiempo y su duracion para cada
    periodo climtico.
    """

    def __init__(self, start_day, period_type):
        self.start_day = start_day
        self.end_day = start_day
        self.type = period_type

    def extend(self):
        """Incrementa período por unidad"""
        self.end_day += 1

    def length(self):
        """Devuelve el número de días que duró el periodo"""
        return self.end_day - self.start_day

    @classmethod
    def new_period(cls, start_day, period_type):
        """Shortcut, crea un nuevo objeto periodo"""
        return cls(start_day, period_type)

    @classmethod
    def empty_period(cls):
        """Crea un periodo vacío, ideal para empezar la subrutina"""
        return cls(0, 'empty')
