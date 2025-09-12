import psycopg2

# URL de Railway
DATABASE_URL = "postgresql://postgres:nOEcTmCjBALApbzBeXmcGDtMkqeXWeYM@centerbeam.proxy.rlwy.net:11872/railway"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT NOW();")
    print("Conexión exitosa. Fecha y hora:", cursor.fetchone())

    cursor.close()
    conn.close()
except Exception as e:
    print("Error al conectar:", e)