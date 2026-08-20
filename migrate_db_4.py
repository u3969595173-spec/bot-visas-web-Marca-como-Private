import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas')

def migrar_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    print("Inyectando columnas de Justificantes...")

    try:
        cur.execute("ALTER TABLE aportaciones ADD COLUMN IF NOT EXISTS comprobante_base64 TEXT;")
        cur.execute("ALTER TABLE aportaciones ADD COLUMN IF NOT EXISTS comprobante_tipo VARCHAR(100);")
        conn.commit()
        print("Migración completada exitosamente.")
    except Exception as e:
        print("Error en migración", e)
        conn.rollback()
        
    cur.close()
    conn.close()

if __name__ == '__main__':
    migrar_db()
