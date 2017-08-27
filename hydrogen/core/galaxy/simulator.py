# -*- coding: utf-8 -*-
"""
Este módulo contiene clases relacionadas a la simulación planetaria.
"""
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


_GalacticReport = namedtuple('GalaxyStreamReport', 'cycle day position extra_data')


class GalacticReport(_GalacticReport):
    """Galactic Report es un objeto inmutable  que contiene
    información de "streaming" generada por la clase SpaceTime en cada iteration.

    GalaxyReport.cycle : contiene el número de ciclo en que fue generado, los ciclos duran 360 días.
    GalaxyReport.day: contiene el día en que se generó el reporte.
    GalaxyReport.position: contiene el tipo de formación -PlanetPosition.- de los astros al momento de generar reporte.
    GalaxyReport.extra_data: contiene información extra y no común para todos los objetos GalacticReport.
    """

    def __repr__(self):
        return '<simulator.GalaxyReport {} {}>'.format(self.day, self.position)

    @property
    def wheater(self):
        """Helper, retorna el tipo de clima de acuerdo a la posición planetaria recibida desde
        un objeto SpaceTime"""
        if self.position == PlanetPosition.are_aligned.value:
            return WheaterType.OPTIMUN
        elif self.position == PlanetPosition.are_aligned_with_sun.value:
            return WheaterType.DROUGHT
        elif self.position == PlanetPosition.planets_sun_triangle.value:
            return WheaterType.RAINY
        else:
            return WheaterType.DEFAULT

    @property
    def precipitation(self):
        """Helper, retorna nivel de precipitación basado en el perimetro según datos de SpaceTime"""
        if self.extra_data:
            return self.extra_data.get('perimeter', 0)
        return 0


class SpaceTime(object):
    """Space Time, es un generator que representa el tiempo espacial, es un iterator que
     permite simular el movimiento espacial, retorna objetos GalaxyReport con la información espacial.
    """

    Sun = Point(0, 0)
    CYCLE_TIME = 360  # los ciclos duran 360 días.

    def __init__(self, start_day, end_day, planets):
        """
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
        """Registramos el iterator"""
        if self._start_day <= self._end_day:

            # obtenemos información de la galaxia en un día especifico.
            _galaxy_info = self._get_galaxy_info_day(self._start_day)

            if not _galaxy_info:
                raise RuntimeError('RuntimeError.Trying to obtain ._get_galaxy_info_day, '
                                   'please check config:'
                                   'start_day:{}, end_day:{}, with planetas {}'.format(
                                        self._start_day, self._end_day, self._planets))
            self._start_day += 1

            return _galaxy_info
        else:
            raise StopIteration()

    @property
    def current_year(self):
        """Retorna el año actual de la galaxia"""
        return self._start_day

    def _get_planets_position_day(self, day):
        """Retorna la posición de los planetas en un día especifico"""
        return [planet.get_position_day(day) for planet in self._planets]

    def _get_galaxy_info_day(self, day):
        """Retorna un objeto GalaxyReport que contiene información posicional de los astros
        en la linea de tiempo.
        """
        current_cycle = int(self.current_year/self.CYCLE_TIME)
        data_stream = GalacticReport(current_cycle, day, PlanetPosition.no_identify.value, {})
        planet_positions = self._get_planets_position_day(day)

        # si los planetas están alineados:
        if calc.are_points_collinear(*planet_positions):
            data_stream = GalacticReport(current_cycle, day, PlanetPosition.are_aligned.value, {})

            # si los planetas están alineados con el Sol.
            if calc.are_points_collinear(self.Sun, planet_positions[0], planet_positions[2]):
                return GalacticReport(current_cycle, day, PlanetPosition.are_aligned_with_sun.value, {})

            return data_stream

        # si los planetas forman un triángulo y el sol está dentro del triángulo
        elif calc.is_point_inside_triangle(*planet_positions, self.Sun):
            return GalacticReport(current_cycle, day, PlanetPosition.planets_sun_triangle.value, {
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