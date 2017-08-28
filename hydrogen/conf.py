# -*- coding: utf-8 -*-
"""
En este módulo se guardan common settings para la app.
"""

# http://docs.sqlalchemy.org/en/latest/core/engines.html
# Base de datos en donde se volcaran los registros del JOB
DATABASE_URL = 'sqlite:///ml.db'

# JOB. indica el número de registros por lote a enviar a la BD usando el "JOB"
JOB_BATCHER = 200
# indica el número de registros por default que debe volcar el JOB en su pr llamada.
JOB_WORK = 365 * 10 # por defecto 10 años calendario.

# Es usado para los cáculos matemáticos, mayor número == menor precisión
REL_TOL = 0.001
