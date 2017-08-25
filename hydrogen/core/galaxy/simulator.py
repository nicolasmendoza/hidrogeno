# -*- coding: utf-8 -*-
import enum

from collections import namedtuple

from ..geometry.elements import Point
from ..geometry import calculator as calc

from .planet import Planet
from ..db.models import WheaterType


class PlanetPosition(enum.Enum):
    """Singleton con las posiciones planetarias soportadas en SpaceTime object.
    """
    are_aligned = 'planets_are_aligned' # cuando los planetas están alineados
    are_aligned_with_sun = 'planet_and_sun_are_aligned' # cuando los planetas están alineados con el sol.
    planets_sun_triangle = 'sun_inside_planet_triangle' # cuando los planetas forman un triángulo y el sol está
    no_identify = 'position_no_identify' # formación no registrada


_GalacticReport = namedtuple('GalaxyStreamReport', 'day position extra_data')


class GalacticReport(_GalacticReport):
    """Galactic Report es un objeto inmutable  que contiene
    información de "streaming" generada por la clase generator SpaceTime
    """

    def whats_wheater(self):
        """Retorna un tipo de clima de acuerdo a la posición planetaria recibida generada por
        el  objeto SpaceTime"""
        if self.position == PlanetPosition.are_aligned:
            return WheaterType.OPTIMUN
        elif self.position == PlanetPosition.are_aligned_with_sun:
            return WheaterType.DROUGHT
        elif self.position == PlanetPosition.planets_sun_triangle:
            return WheaterType.RAINY
        else:
            return WheaterType.DEFAULT


    @property
    def get_precipitation(self):
        """Retorna la precipitación, en caso de no existir
        data de precipitación entonces retornará cero"""
        return 8989


class SpaceTime(object):
    """Space Time, es un generator que representa el tiempo espacial,
    es un iterator que permite simular el movimiento espacial que retorna un objecto GalaxyReport
    conteniendo la información espacial.
    """

    Sun = Point(0, 0)

    def __init__(self, start_day, end_day, planets):
        """Space time es un "simulador"

        :param start_day: :int: día de inicio
        :param end_day:  :int: día final -fin del ciclo-
        :param planets: lista de planetas.
        """
        self._planets = planets
        self._start_day = start_day
        self._end_day = end_day

    def __iter__(self):
        return self

    def __next__(self):
        """Se crea un generator para para presetar la data como stream sin carga todo a memoria"""
        if self._start_day <= self._end_day:
            # obtenemos información de la galaxia en un día especifico.
            _galaxy_info = self._get_galaxy_info_day(self._start_day)
            self._start_day += 1

            return _galaxy_info
        else:
            raise StopIteration()

    def _get_planets_position_day(self, day):
        """Retorna la posición de los planetas en un día especifico"""
        return [planet.get_position_day(day) for planet in self._planets]

    def _get_galaxy_info_day(self, day):
        """Retorna un objeto GalaxyReport que contiene información posicional de los astros
        en la linea de tiempo.
        """

        data_stream = GalacticReport(day, PlanetPosition.no_identify.value, {})
        planet_positions = self._get_planets_position_day(day)

        # si los planetas están alineados:
        if calc.are_points_collinear(*planet_positions):
            data_stream = GalacticReport(day, PlanetPosition.are_aligned.value, {})

            # si los planetas están alineados con el Sol.
            if calc.are_points_collinear(self.Sun, planet_positions[0], planet_positions[2]):
                return GalacticReport(day, PlanetPosition.are_aligned_with_sun.value, {})

            return data_stream

        # si los planetas forman un triángulo y el sol está dentro del triángulo
        elif calc.is_point_inside_triangle(*planet_positions, self.Sun):
            return GalacticReport(day, PlanetPosition.planets_sun_triangle.value, {
                'perimeter': calc.get_perimeter(*planet_positions),
                'shape': 'triangle'
            })

        else:
            return data_stream

    @classmethod
    def galaxy(cls, from_day, to_day):
        """Creates default galaxy configuration.
        Default galaxy contains three planets: Betasoide, Ferengi, and Vulcano. and starts day zero.
        """
        default_planets = [Planet.new_betasoide(), Planet.new_ferengi(), Planet.new_vulcano()]
        return cls(from_day, to_day, planets=default_planets)