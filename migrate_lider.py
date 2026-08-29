import psycopg2
import os

DATABASE_URL = 'postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas'

try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    cur.execute("ALTER TABLE inversores ADD COLUMN IF NOT EXISTS es_lider BOOLEAN DEFAULT FALSE;")
    conn.commit()
    print("Columna 'es_lider' añadida con éxito.")

    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
