import pandas as pd
import logging
import sqlite3

from utils_upload_data_from_xlsx import extract_values

conn = sqlite3.connect('db.sqlite3')
COLS = [
    "DEPARTAMENTO",
    "UBICACIÓN",
    "PRECIO",
    "PROPIETARIO",
    "ID",
    "ESTATUS",
    "TELEFONO",
    "CALLE",
    "COLONIA",
    "NUMERO",
    "CIUDAD",
    "CP",
    "COCHERA",
    "BAÑOS",
    "PETFREDLY",
    "PATIO",
    "RECAMARAS",
    "CENTRO DE LAVADO",
    "MINISPLIT",
    "CARACTERISTICAS",
    "SERVICIOS INCLUIDOS",
    "PRECIO RENTA",
    "COMENTARIOS",
    "NO. SERVICIO CFE",
    "NO. SERVICIO SIMAS"
]
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("report_apartments_upload.log"),
        logging.StreamHandler()  # También los muestra en consola
    ]
)

logger = logging.getLogger(__name__)

FILE_NAME = 'doc.xlsx'
SHEET_NAME = 'DEPAS RENTA'


try:
    logger.info(f'Initializing data frame from file: {FILE_NAME}')
    df = pd.read_excel(FILE_NAME, sheet_name=SHEET_NAME, header=1)
    logger.info('Dataframe success')
except Exception as e:
    logger.error('There was an exception while reading the file', str(e))

logger.info('Extracting process initialized')

import math

def safe_val(v):
    return None if (v is None or (isinstance(v, float) and math.isnan(v))) else v



cursor = conn.cursor()
for data in extract_values(df, logger):
    data['tipo_propiedad'] = 'departamento'
    data['operacion'] = 'renta'
    o_id = data['id']
    try:
        logger.info('Getting the owner_baseowner.id')
        cursor.execute("SELECT id FROM owner_baseowner WHERE o_id = ?", (o_id,))
        propietario_id_row = cursor.fetchone()
        prop_id = propietario_id_row[0]
        logger.info('Successfully fetched data from owner_baseowner.id')
    except Exception:
        logger.error('there was an error while getting the prop id')
        prop_id = 9999999999
        logger.warning(f'setting the prop_id to {prop_id}')
    values_to_insert = [
            safe_val(data["id"]),                       # id
            'departamento',                             # tipo_propiedad
            safe_val(data["calle"]),                    # calle
            safe_val(data["colonia"]),                  # colonia
            safe_val(int(data["numero"])) if safe_val(data["numero"]) is not None else None,  # numero
            safe_val(int(data["cp"])) if safe_val(data["cp"]) is not None else None,          # codigo_postal
            safe_val(data["ciudad"]),                   # ciudad
            'renta',                                    # operacion
            safe_val(int(data["precio"])) if safe_val(data["precio"]) is not None else None,  # costo
            'disponible' if data["estatus"]=="DISPONIBLE" else 'rentada', # estatus
            safe_val(data["caracteristicas"]),          # caracteristicas_extras
            safe_val(data["comentarios"]),              # comentarios
            True if data['cochera']=="SI" else False,  # tiene_cochera
            safe_val(float(data["baños"])) if safe_val(data["baños"]) is not None else None, # banos
            True if data['petfredly']=="SI" else False,# acepta_mascotas
            True if data['patio']=="SI" else False,    # tiene_patio
            safe_val(int(data["recamaras"])) if safe_val(data["recamaras"]) is not None else None, # recamaras
            True if data['centro_de_lavado']=="SI" else False,  # centro_de_lavado
            safe_val(int(data["minisplit"])) if safe_val(data["minisplit"]) is not None else None, # minisplits
            safe_val(data["servicios_incluidos"]),      # servicios_incluidos
            safe_val(data["no_servicio_simas"]),        # numero_servicio_simas
            safe_val(data["no_servicio_cfe"]),          # numero_servicio_cfe
            None,                                       # superficie_terreno
            None,                                       # superficie_construccion
            None,                                       # metodo_pago
            None,                                       # observaciones
            None,                                       # negociable
            prop_id,                                    # propietario_id
            safe_val(data["departamento"])              # titulo
        ]

        # Query INSERT
    query = """
    INSERT INTO property_baseproperty
    (id, tipo_propiedad, calle, colonia, numero, codigo_postal, ciudad, operacion, costo, estatus, caracteristicas_extras, comentarios,
        tiene_cochera, banos, acepta_mascotas, tiene_patio, recamaras, centro_de_lavado, minisplits, servicios_incluidos, numero_servicio_simas,
        numero_servicio_cfe, superficie_terreno, superficie_construccion, metodo_pago, observaciones, negociable, propietario_id, titulo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        
        # q = query.replace("?", "{}").format(*[repr(v) for v in values_to_insert])
        print()
        cursor.execute(query, values_to_insert)
        conn.commit() 
        logger.info('Insert Successfull')
    except Exception as e:
        logger.error(f'Could not insert data into the table at index {str(e)}')