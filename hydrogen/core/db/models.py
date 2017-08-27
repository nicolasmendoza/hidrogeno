# -*- coding: utf-8 -*-
"""
Database Models. Este módulo contiene los modelos para persistencia en db relacianods
a la funcionalidad de "prónostico" / clima.
"""
import sys
import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, MetaData
from sqlalchemy.orm import sessionmaker


from hydrogen import conf

Base = declarative_base()
metadata = MetaData()


class WheaterType(enum.Enum):
    """Tipos de clima soportados.
    """
    RAINY = 'lluvia'  # lluvía, puede ser intensa dependiendo del nivel de precipitación.
    DROUGHT = 'sequía'
    OPTIMUN = 'óptimo'  # comfort térmico y pluviométrico.
    DEFAULT = 'estándar'  # clima standard, sin cambios.


class WheaterForeCastModel(Base):
    """ Database model para predicciones.
    day: día al que pertenece la predicción.
    wheater: tipo de clima.
    precipitation: nivel de precipitación
    """
    __tablename__ = 'wheaterforecast'

    day = Column(Integer(), primary_key=True)
    wheater = Column(String(50))
    precipitation = Column(Integer(), default=0)

    def createSession(self):
        Session = sessionmaker()
        self.session = Session.configure(bind=self.engine)

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
            Session = sessionmaker(bind=engine)
            session = Session()
            session.add_all(bulk_data_list)
            session.commit()
        except:
            e = sys.exc_info()[0]
            raise Exception(''
                            'Database error. please see if you database conf s correct: '
                            'hydrogen/core/conf'
                            '', e)


global engine

engine = create_engine(conf.DATABASE_URL)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

