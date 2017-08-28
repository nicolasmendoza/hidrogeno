# -*- coding: utf-8 -*-
"""
Es módulo contiene las class iniciales para la simulación
"""
import enum
from ...core.geometry.elements import Point


class ClockWise(enum.Enum):
    """Sentido horario, indica el sentido horario en que se mueve un objeto.
    """
    COUNTERCLOCK = 1
    ANTICLOCK = -1


class Planet(object):
    """Representa un planeta."""

    def __init__(self, name, velocity, sun_distance, clockwise):
        """
        :param name: :str: nombre del planeta - pensado para graficar-
        :param velocity: :int: velocidad de desplazamiento del planeta.
        :param sun_distance: :int: distancia del planeta con respecto al Sol.
        :param clockwise: :ClockWise: Sentido horario alrededor del sol.
        """

        self.name = name
        self._velocity = velocity * clockwise
        self._sun_distance = sun_distance

    def get_position_day(self, day):
        """Retorna la posición espacial del planeta según un día específico."""
        return self._get_cartesian_point(self._get_deg(day))

    def _get_cartesian_point(self, deg):
        """Retorna un object Point desde un valor correspendiente al ángulo."""
        return Point.new_from_deg(deg, self._sun_distance)

    def _get_deg(self, day):
        """Retorna posicion angular del planeta en un día especifico."""
        return self._velocity * day

    @classmethod
    def new_ferengi(cls):
        """Fabrica un planeta de tipo Ferengi con sus default atributos."""
        kwargs = {
            'name': 'Ferengi',
            'velocity': 1,
            'clockwise': ClockWise.COUNTERCLOCK.value,
            'sun_distance': 500,
        }
        return cls(**kwargs)

    @classmethod
    def new_vulcano(cls):
        """Fabrica un planeta de tipo Ferengi con sus default atributos."""
        kwargs = {
            'name': 'Vulcano',
            'velocity': 5,
            'clockwise': ClockWise.ANTICLOCK.value,
            'sun_distance': 1000
        }
        return cls(**kwargs)

    @classmethod
    def new_betasoide(cls):
        """Fabrica un planeta de tipo Ferengi con sus default atributos."""
        kwargs = {
            'name': 'Betasoide',
            'velocity': 3,
            'clockwise': ClockWise.COUNTERCLOCK.value,
            'sun_distance': 2000
        }
        return cls(**kwargs)
