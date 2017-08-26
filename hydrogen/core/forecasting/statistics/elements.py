"""
August 2017
hidrogeno app. elements.py
Author: Nicolás Mendoza.
"""


class RainGauge(object):
    """Representa un pluviometro, es usado en coroutine.py como
    acumulador del stream de precipitation.
    """
    def __init__(self, level=0, day=0):
        self.level = level
        self.day = day

    def gather(self, liquid, day):
        """Actualiza el nivel actual y día si el nivel de "liquido"
        es mayor al actual.
        """
        if liquid > self.level:
            self.level = liquid
            self.day = day


class PeriodTime(object):
    """Representa un periodo de tiempo, es usado para
    acumular los periodos de tiempo de los diferentes climas,
    ver coroutine.py
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
        """Crea un periodo vacío, ideal para empezar la coroutine.py"""
        return cls(0, 'empty')