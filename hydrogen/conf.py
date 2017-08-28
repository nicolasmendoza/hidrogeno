# -*- coding: utf-8 -*-
"""
En este módulo se guardan common settings para la app.
"""
import os

# Ejemplos url y db soportadas: http://docs.sqlalchemy.org/en/latest/core/engines.html
# Base de datos en donde volcaremos los registros del JOB

DEFAULT_DB = 'sqlite:///default.db'  #todo

# postgresql+psycopg2://USER:PASSWORD@localhost/DATABASE
DATABASE_URL = os.environ.get('HIDROGENO_DB', DEFAULT_DB)

# JOB. indica el número de registros por lote a enviar a la BD usando el "JOB"
JOB_BATCHER = 200
# indica el número de registros por default que debe volcar el JOB en su pr llamada.
JOB_WORK = 365 * 10 # por defecto 10 años calendario.

# Es usado para los cáculos matemáticos, mayor número == menor precisión
REL_TOL = 0.001


# export HIDROGENO=postgresql+psycopg2://nicolas:nicolas@localhost/hidrogeno
