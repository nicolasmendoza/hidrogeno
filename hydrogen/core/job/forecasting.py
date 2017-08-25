
from hydrogen import conf

from hydrogen.core.galaxy.simulator import SpaceTime, PlanetPosition
from hydrogen.core.job import pipeline
from hydrogen.core.db.models import WheaterForeCastModel


class WeatherWatcher(object):
    """Weather Watcher es un  "dispatch object" que mapea los tipos de movimiento planetario
    a los respectivos filtros de la tuberia pipeline.py
    """
    __slots__ = ('lot_size', 'lot')

    def __init__(self, lot_size=None):
        """WheaterWatcher es objeto observador que permite el mapeo desde el stream de
        SpaceTime a filtros especificos, pensado para aplicar cualquier filtro o regla a la data
        obtenida de la "simulación" planetaria.

        :param lot_size: :int: número de registros a batear, es un batcher.
        """
        self.lot_size = lot_size  # tamaño de lotes que se envían a db.
        self.lot = []

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

        # lote completo...envíar a la db.
        if len(self.lot) == self.lot_size or self.lot_size is None:
            self.flush()

    def flush(self):
        """Inserta lote de datos en la db y reinicia el conteo del batcher."""
        WheaterForeCastModel.insert_bulk(self.lot)
        self.lot = []

    def analyze(self, galaxy_report):
        """recibe stream de SpaceTime Object y redirecciona al filtro correspondiente en pipeline.py,
        esto es simplemente un ejercicio, la pipeline se puede omitir si se quiere, además desde el objeto
        GalaxyReport podemos "extraer" el tipo de clima.
        """
        command = galaxy_report.position
        self.save(self.DISPATCH[command](galaxy_report))
