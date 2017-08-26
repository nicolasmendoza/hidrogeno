
from collections import deque

from hydrogen.core.galaxy.simulator import SpaceTime, PlanetPosition
from hydrogen.core.job import pipeline
from hydrogen.core.db.models import WheaterForeCastModel


class WeatherWatcher(object):
    """Weather Watcher es un  "dispatch object" que mapea los tipos de movimiento planetario
    a los respectivos filtros/comandos de la tuberia. pipeline.py
    """
    __slots__ = ('lot_size', 'lot')

    def __init__(self, lot_size):
        """WheaterWatcher es un objeto observador que permite el mapeo desde el generador SpaceTime object a
        filtros especificos.
        Pensado para aplicar cualquier filtro o regla a la data obtenida en la "simulación" planetaria.
        :param lot_size: :int: número de registros a batear, es un batcher.
        """

        self.lot_size = lot_size  # tamaño de lotes que se envían a db.
        self.lot = deque()

    DISPATCH = {
        PlanetPosition.are_aligned.value: pipeline.wheater_optimun,
        PlanetPosition.are_aligned_with_sun.value: pipeline.wheater_drought,
        PlanetPosition.planets_sun_triangle.value: pipeline.wheater_rainy,
        PlanetPosition.no_identify.value: pipeline.default_wheater
    }

    def save(self, wheater_forecast):
        """Data processed"""
        if not isinstance(wheater_forecast, WheaterForeCastModel):
            raise Exception('Error processing data, watcher expect a wheaterForeCastModel, received:', wheater_forecast)

        # agrega registro a lote
        self.lot.append(wheater_forecast)

        if len(self.lot) == self.lot_size:
            self.flush()

    def flush(self):
        """Inserta lote de datos en la db y reinicia el conteo del batcher."""

        #todo, cambiar por logging.info()
        print(' Hit database, lot size={}. Sending bulk data and flushing the batcher.'.format(self.lot_size))

        # convertimos datatype deque a list antes de enviar el lote.
        WheaterForeCastModel.insert_bulk(list(self.lot))
        self.lot.clear()

    def analyze(self, galaxy_report):
        """Recibe stream de SpaceTime Object y redirecciona al filtro correspondiente en pipeline.py.

        *Esto es simplemente un ejercicio, la pipeline se puede omitir si se quiere, la conservé porque
        en la versión inicial estaba "matando moscas a cañonazos" con una versión totalmente async.
        """
        command = galaxy_report.position
        self.save(self.DISPATCH[command](galaxy_report))
