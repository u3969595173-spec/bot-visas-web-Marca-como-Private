import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas')

def migrar_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    print("Conectado a BD para Inyectar Reparto Dinámico diario...")

    try:
        cur.execute("ALTER TABLE aportaciones ADD COLUMN IF NOT EXISTS ganancia_rentabilidad DECIMAL(12,2) DEFAULT 0;")
        cur.execute("ALTER TABLE aportaciones ADD COLUMN IF NOT EXISTS ultima_fecha_pago DATE;")
        conn.commit()
        print("Ejecutado correctamente.")
    except Exception as e:
        print("Error en migración", e)
        conn.rollback()
        
    cur.close()
    conn.close()
    print("Migración completada.")

if __name__ == '__main__':
    migrar_db()
