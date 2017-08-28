=========
hidrógeno
=========

.. image:: https://travis-ci.org/nicolasmendoza/hidrogeno.svg?branch=master
    :target: https://travis-ci.org/nicolasmendoza/hidrogeno
    
.. image:: https://codecov.io/gh/nicolasmendoza/hidrogeno/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/nicolasmendoza/hidrogeno
  
Hydrogen is a library and command line utility.

* Ejercicio de programación.

Hidrogeno es una "librería" y línea de comandos escrita en python 3.5 sin uso de ningún framework, si bien la app tiene demasiados "super poderes" para resolver un ejercicio sencillo quise darle un poco más de ficción pensando en una app que necesitaba un nivel de procesamiento/simulación alto. 

Conociendo cuántos períodos climáticos habrá en un ciclo de 360 días nos bastará con multiplicar para saber cuántos habrá en determinado año.

.. image:: https://raw.githubusercontent.com/nicolasmendoza/hidrogeno/develop/docs/img/hydrogen0.jpg
   :height: 100px
   :width: 200 px
   :scale: 50 %
   :alt: alternate text
   :align: right
   
Features
--------

* Job Batcher. 
* Data Pipelines.
* Space Time /Data Stream generator.
* WheaterForecast - Coroutine stats.
* Memoization.

Requerimientos:
--------------
Python 3.5

Installation
-----------
pip install git+https://github.com/nicolasmendoza/hidrogeno.git

screencast: https://vimeo.com/231359435


API Rest.
---------
https://github.com/nicolasmendoza/microservice


Uso de la librería
--------------------
.. code:: python

    from hidrogeno.galaxy.core.simulator import SpaceTime
   
    """SpaceTime es un generator, galaxy() es un método/shortcut que fabrica 
    un SpaceTime con los planetas y la configuración por defecto. 
    Cuando SpaceTime es recorrido este genera objectos de tipo GalacticReport,
    los objetos GalacticReport contiene: Día, Ciclo, Posición Planetaria, etc.
    """
    days = 3000
    space_time = SpaceTime.galaxy(from_day=0, to_day=days) 
    
    
    # Subrutina para capturar que recibe stream.
    from .core.wheater.statistics import coroutine as coro
    
    coro_stats = coro.listen_stream(days)

    
    for data in stream:  
           # envíamos el (día, el clima, y el nivel de precipitación) para estadísticas.
            coro_stats.send(
            (data.day, data.wheater, data.precipitation)
            )

     
        ... ...
        
.. code:: python

     # Contiene modelo de dato usado para persist.
    hidrogeno/hydrogen/core/db/models.py
     # Contiene la clases singletone ClockWise y la clase Planet.
    hidrogeno/hydrogen/core/galaxy/planet.py
    # Contiene: PlanetPosition, GalacticReport, y SpaceTime
    hidrogeno/hydrogen/core/galaxy/simulator.py

Cobertura de tests.
-------------------
UP. in progress...





