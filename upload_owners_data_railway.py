import pandas as pd
import logging
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import text

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("subida_propietarios_railway.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Leer DATABASE_URL desde el entorno
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("La variable de entorno DATABASE_URL no está definida en el archivo .env")

# Crear conexión con SQLAlchemy
try:
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    logger.info("Conexión exitosa a la base de datos de Railway")
except Exception as e:
    logger.error(f"No se pudo conectar a la base de datos: {e}")
    raise

# Configuración de archivo y columnas
FILE_NAME = 'doc.xlsx'
SHEET_NAME = 'Hoja1'
COLS = ['#ID', "NOMBRE PROPIETARIO", "TELEFONO"]

# Cargar DataFrame
try:
    logger.info(f'Inicializando DataFrame desde el archivo: {FILE_NAME}')
    df = pd.read_excel(FILE_NAME, sheet_name=SHEET_NAME, usecols=COLS)
    logger.info('DataFrame cargado correctamente')
except Exception as e:
    logger.error(f'Error al leer el archivo Excel: {str(e)}')
    raise

# Procesamiento e inserción
logger.info('Inicio del proceso de extracción e inserción de datos')
for index, series in df.iterrows():
    nombre = apellido_paterno = apellido_materno = telefono = o_id = ""
    logger.info(f'Procesando fila {index}')

    try:
        telefono = series["TELEFONO"]
        o_id = series['#ID']

        partes = series["NOMBRE PROPIETARIO"].split(" ")
        if len(partes) == 0:
            logger.error(f'No hay nombre en el índice {index}')
            continue
        if len(partes) == 3:
            nombre, apellido_paterno, apellido_materno = partes
        elif len(partes) == 2:
            nombre, apellido_paterno = partes
        elif len(partes) == 1:
            nombre = partes[0]
            logger.warning(f'El propietario solo tiene nombre en el índice {index}')
        else:
            nombre = partes[0]
            apellido_paterno = partes[1]
            apellido_materno = partes[2]

    except Exception as e:
        logger.error(f'Error procesando los datos en la fila {index}: {str(e)}')
        continue

    try:
        conn.execute(
            text("""
                INSERT INTO owner_baseowner (nombre, apellido_paterno, apellido_materno, telefono, o_id)
                VALUES (:nombre, :apellido_paterno, :apellido_materno, :telefono, :o_id)
            """),
            {
                "nombre": nombre,
                "apellido_paterno": apellido_paterno,
                "apellido_materno": apellido_materno,
                "telefono": telefono,
                "o_id": o_id
            }
        )
        conn.commit()
        logger.info(f'Fila {index} insertada correctamente')
    except Exception as e:
        logger.error(f'Error al insertar la fila {index}: {str(e)}')

conn.close()
logger.info('Proceso finalizado correctamente')
