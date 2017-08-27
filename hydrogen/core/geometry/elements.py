# -*- coding: utf-8 -*-
"""
Este módulo contiene los elementos geométricos esenciales para clculos de la aplicación.
por diseño temporalmente se han desacoplado y movido todas las operaciones math a calculator.py

"""
import collections
from . import calculator as calc

_Point = collections.namedtuple('Point', 'x y')

_Triangle = collections.namedtuple('Triangle', ['vertice_a', 'vertice_b', 'vertice_c'])


class Point(_Point):
    """Punto es un object inmutable que representa un Punto en el espacio.
    Point(x, y)
    """
    @classmethod
    def new_from_deg(cls, deg, radius):
        """Crea un object Point a partir del radio y angulo"""
        radians = calc.deg2radians(deg)
        kwargs = {
            'x': radius * calc.sin(radians),
            'y': radius * calc.cos(radians)
        }
        return Point(**kwargs)


class Triangle(_Triangle):
    """Triangulo es es un objecto inmutable.
    Triangle(Point0, Point1, Point2)
    """
    def get_area(self):
        return calc.get_triangle_area(self.vertice_a, self.vertice_b, self.vertice_c)

    @classmethod
    def new_from_(cls, point0, point1, point2):
        """Crea un object Triangle a partir de tres objectos Point"""
        return Triangle(point0, point1, point2)
