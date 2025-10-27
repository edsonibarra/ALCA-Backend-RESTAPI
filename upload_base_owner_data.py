import pandas as pd
import logging
import sqlite3

conn = sqlite3.connect('db.sqlite3')

logging.basicConfig(
    level=logging.DEBUG,  # Nivel de log: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("subida_propietarios.log"),  # Guarda los logs en un archivo
        logging.StreamHandler()  # También los muestra en consola
    ]
)

logger = logging.getLogger(__name__)

FILE_NAME = 'doc.xlsx'
SHEET_NAME = 'Hoja1'
COLS = ['#ID', "NOMBRE PROPIETARIO", "TELEFONO"]

try:
    logger.info(f'Initializing data frame from file: {FILE_NAME}')
    df = pd.read_excel(FILE_NAME, sheet_name=SHEET_NAME, usecols=COLS)
    logger.info('Dataframe success')
except Exception as e:
    logger.error('There was an exception while reading the file', str(e))

logger.info('Extracting process initialized')
for index, series in df.iterrows():
    nombre = ""
    apellido_paterno = ""
    apellido_materno = ""
    telefono = ""
    o_id = ""
    logger.info(f'Reading row {index}')
    try:
        telefono = series["TELEFONO"]
        o_id = series['#ID']
        try:
            partes = series["NOMBRE PROPIETARIO"].split(" ")
            if len(partes) == 0:
                logger.error(f'There is no name for this owner at index {index}')
                continue
            if len(partes) == 3:
                nombre = partes[0]
                apellido_paterno = partes[1]
                apellido_materno = partes[2]
            elif len(partes) == 2:
                nombre = partes[0]
                apellido_paterno = partes[1]
            elif len(partes) == 1:
                nombre = partes[0]
                logger.warning(f'The owner only has name at index {index}')
            else:
                nombre = partes[0]
                apellido_paterno = partes[1]
                apellido_materno = partes[2]
        except Exception as e:
            logger.error(f'There was a problem processing the name at index {index}')
            raise
    except Exception as e:
        logger.error(f'There was a problem extracting the fields at index {index}')
    logger.info(f'Extracted fields: nombre {nombre}, apellido_paterno {apellido_paterno}, apellido materno {apellido_materno}, telefono {telefono}, o_id {o_id}')
    logger.info('Inserting the values into the database')
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO owner_baseowner (nombre, apellido_paterno, apellido_materno, telefono, o_id)
        VALUES (?, ?, ?, ?, ?)
        """, [nombre, apellido_paterno, apellido_materno, telefono, o_id])
        conn.commit() 
        logger.info('Insert Successfull')
    except Exception as e:
        logger.error(f'Could not insert data into the table at index {index} {str(e)}')
logger.info('Finish')
    

