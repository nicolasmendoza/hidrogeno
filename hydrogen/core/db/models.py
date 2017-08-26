# -*- coding: utf-8 -*-
""" Database Models.
"""
import sys
import enum


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from hydrogen import conf

Base = declarative_base()
engine = None

class WheaterType(enum.Enum):
    """Tipos de clima soportados.
    """
    RAINY = 'lluvia'  # lluvía, puede ser intensa dependiendo del nivel de precipitación.
    DROUGHT = 'sequía'
    OPTIMUN = 'óptimo'  # comfort térmico y pluviométrico.
    DEFAULT = 'estándar'  # clima standard, sin cambios.


class WheaterForeCastModel(Base):
    """ Database model para predicciones.
    day: día de predicción.
    wheater: tipo de clima.
    precipitation: nivel de precipitación
    """
    __tablename__ = 'wheaterforecast'

    day = Column(Integer, primary_key=True, index=True)
    wheater = Column(String(512))
    precipitation = Column(Integer, default=0)

    @classmethod
    def insert_bulk(cls, bulk_data_list):
        """Persiste lotes de objectos WheaterForeCastModel
        :param bulk_data_list: : requiere una lista de objetos de tipo WheaterForeCastModel
        :return:
        """
        if not isinstance(bulk_data_list, list):
            raise Exception(
                'Database error. WheaterForeCastModel.insert_bulk expect a list object. '
                'Received object {}'.format(
                    type(bulk_data_list)
                )
            )
        try:
            # inserción de lote & commit.
            session.add_all(bulk_data_list)
            session.commit()
        except:
            e = sys.exc_info()[0]
            raise Exception(''
                            'Database error. please see if you database conf s correct: '
                            'hydrogen/core/conf'
                            '', e)

def setup_database(dburl, echo, num):
    global engine
    engine = create_engine(dburl, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)