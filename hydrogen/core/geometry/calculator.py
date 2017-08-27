# -*- coding: utf-8 -*-
"""
Este módulo actua de wrapper para las operaciones matemáticas requeridas en la app.
Por diseño ha sido intencional desacoplarlas de las clases, de esta manera podemos
aplicarles memoization y/o reemplazar los algoritmos base en esta etapa de prototipado y
después encapsularlas cmo corresponde.

Lista Operaciones:

-> deg2radians(degrees): Convierte grados a radianes.
-> are_points_collinear(Point0, Point1, Point2): Retorna True si los puntos dados son colineales.
-> is_point_inside_triangle(point0, point1, point2, pointx): Retorna True si pointx se encuentra dentro de
    un poligono conformado por por los tres puntos anteriores.
-> get_perimeter(p0, p1, p2): retorna perímetro.
-> sin(radians)
-> cos(radians)
-> deg2radians(degrees)
"""
import math
import functools

from ... import conf


@functools.lru_cache(maxsize=None)
def get_distance_between_points(point0, point1):
    """Retorna la distancia entre dos Puntos"""
    x = math.pow(point1.x - point0.x, 2)
    y = math.pow(point1.y - point0.y, 2)

    return math.sqrt(x+y)


@functools.lru_cache(maxsize=None)
def are_points_collinear(point0, point1, point2):
    """Retorna True si los puntos son colineares."""
    ab = get_distance_between_points(point0, point2)
    ac = get_distance_between_points(point0, point1)
    bc = get_distance_between_points(point2, point1)

    # todo #debt #improvement utilizar ccw aprovechando la clase ClockWise

    if math.isclose(ac + bc, ab, rel_tol=conf.REL_TOL):
        return True
    elif math.isclose(ac + ab, bc, rel_tol=conf.REL_TOL):
        return True
    elif math.isclose(bc + ab, ac, rel_tol=conf.REL_TOL):
        return True
    else:
        return False


@functools.lru_cache(maxsize=None)
def get_area(p0, p1, p2):
    return (p0.x - p2.x) * (p1.y-p2.y) - (p1.x - p2.x) * (p0.y -p2.y)


@functools.lru_cache(maxsize=None)
def is_point_inside_triangle(p0, p1, p2, px):
    """Retorna true si el Punto Px está dentro de un triángulo formado
    por los puntos p0, p1, y p2.
    """
    a, b, c, x = p0, p1, p2 , px

    ab = get_area(x, a, b) < 0.0
    ac = get_area(x, b, c) < 0.0
    ca = get_area(x, c, a) < 0.0

    return ab == ac and ac == ca


@functools.lru_cache(maxsize=None)
def get_perimeter(p0, p1, p2):
    """Retorna el perímetro de un poligono."""
    ab_distance = get_distance_between_points(p0, p1)
    bc_distance = get_distance_between_points(p1, p2)
    ac_distance = get_distance_between_points(p0, p2)
    return ab_distance + bc_distance + ac_distance


@functools.lru_cache(maxsize=None)
def sin(radians):
    return math.sin(radians)


@functools.lru_cache(maxsize=None)
def cos(radians):
    return math.cos(radians)


@functools.lru_cache(maxsize=None)
def deg2radians(degrees):
    return math.radians(degrees)
