# -*- coding: utf-8 -*-
""" Database Models.
"""
import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from hydrogen import conf

Base = declarative_base()
metadata = Base.metadata
session = scoped_session(sessionmaker())
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

    day = Column(BigInteger, primary_key=True)
    wheater = Column(String(512))
    precipitation = Column(Integer, default=0)

    @classmethod
    def insert_bulk(cls, bulk_data):
        init_db()
        session.add_all(bulk_data)
        session.commit()


def init_db(db_name=conf.DATABASE_URL):
    global engine
    engine = create_engine(db_name, echo=False)
    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)
    metadata.drop_all(engine)
    metadata.create_all(engine)
