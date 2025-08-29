import os
import django

# Configuración de Django (antes de importar modelos)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

import sqlite3
import pandas as pd
from property.models import HouseForSale
from owner.models import Owner


conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

FILE_NAME = 'casas.xlsx'


FIELDS_XLSX_HOUSE_FOR_SALE = {
    "title": 0,
    "street": 7,
    "number": 8,
    "nghood": 9,
    "postal_code": 11,
    "city": 10,
    "selling_cost": 2,
    "comments": 23,
    "owner": 1_000,
    "estatus": 5,
    "cochera": 12,
    "baths": 13,
    "beds": 15,
    "minisplits": 16,
    "construccion": 18,
    "superficie": 17,
    "servicios": 20,
    "metodo_de_pago": 22,
    "negociable": 24
}
def load_houses(filename: str):
    df = pd.read_excel(filename, sheet_name='CASAS VENTA', header=1)
    df.columns = df.columns.str.strip().str.upper()

    for _, row in df.iterrows():
        # precio limpio
        precio = str(row["PRECIO"]).replace("$", "").replace(",", "").strip()
        try:
            precio = int(float(precio))
        except:
            precio = None

        # booleans
        patio = True if str(row["PATIO"]).strip().upper().startswith("SI") else False
        negociable = True if str(row["NEGOCIABLE?"]).strip().upper().startswith("SI") else False

        cochera_val = row.get("COCHERA")

        if pd.isna(cochera_val) or str(cochera_val).strip() in ("", "NAN", "NONE"):
            cochera = None
        else:
            val = str(cochera_val).strip().upper()
            if val.isdigit():
                cochera = int(val)
            elif val == "SI":
                cochera = 1
            elif val == "NO":
                cochera = 0
            else:
                cochera = None
        postal_code_val = row.get("CP")

        if pd.isna(postal_code_val) or str(postal_code_val).strip() in ("", "NAN", "NONE"):
            postal_code = None
        else:
            try:
                postal_code = int(str(postal_code_val).strip())
            except ValueError:
                postal_code = None
        # owner
        try:
            owner = Owner.objects.get(owner_id_house=row["#ID"])
        except Owner.DoesNotExist:
            print(f"⚠️ Owner {row['PROPIETARIO']} no existe, saltando fila")
            continue

        house = HouseForSale.objects.create(
            title=row["CASA"],
            street=row["CALLE"],
            number=str(row["NUMERO"]).replace("#", "").strip() if pd.notna(row["NUMERO"]) else None,
            nghood=row["COLONIA"],
            postal_code=postal_code,
            city=row["CIUDAD"],
            selling_cost=precio,
            comments=row["OBSERVACIONES"],
            owner=owner,
            estatus=row["ESTATUS"],
            cochera=cochera,  # 👈 ya normalizado
            baths=row["BAÑOS"] if pd.notna(row["BAÑOS"]) else None,
            patio=patio,
            beds=row["RECAMARAS"] if pd.notna(row["RECAMARAS"]) else None,
            minisplits=row["MINISPLIT"] if pd.notna(row["MINISPLIT"]) else None,
            construccion=str(row["CONSTRUCCION"]).replace("M2", "").strip() if pd.notna(row["CONSTRUCCION"]) else None,
            superficie=str(row["TERRENO"]).replace("M2", "").strip() if pd.notna(row["TERRENO"]) else None,
            servicios=row["SERVICIOS INCLUIDOS"],
            metodo_de_pago=row["METODO DE PAGO"],
            negociable=negociable,
        )
        print(f"✅ Casa insertada: {house.title}")


def load_owners():
    file_path = 'casas.xlsx'
    sheet_name = 'Hoja1'
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    # print(df.head)
    all_rows = df.values.tolist()
    # print(all_rows)
    ID_IDX = 0
    NAME_IDX = 1
    PHONE_IDX = 2
    obs = []
    for row in all_rows:
        name = row[NAME_IDX]
        phone = row[PHONE_IDX]
        prop_id = row[ID_IDX]
        ob = (prop_id, name, phone)
        obs.append(ob)
    # print(obs)
    cur.executemany(
        "INSERT INTO owner_owner (owner_id_house, name, phone) VALUES (?, ?, ?)",
        obs
    )
    conn.commit()


def main():

    # handle_file(FILE_NAME)
    # load_owners()
    load_houses(FILE_NAME)

main()

