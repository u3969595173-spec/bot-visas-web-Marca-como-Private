import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas')

def migrar_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    print("Conectado a BD para inyectar tabla restante de logica Referidos...")

    try:
        cur.execute("ALTER TABLE inversores ADD COLUMN IF NOT EXISTS referido_por VARCHAR(50);")
        conn.commit()
        print("Ejecutado: ALTER TABLE inversores ADD COLUMN IF NOT EXISTS referido_por VARCHAR(50);")
    except Exception as e:
        print("Error en inversores", e)
        conn.rollback()
        
    cur.close()
    conn.close()
    print("Migración completada.")

if __name__ == '__main__':
    migrar_db()
