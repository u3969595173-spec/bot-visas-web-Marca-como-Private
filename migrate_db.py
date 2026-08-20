import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas')

def migrar_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    print("Conectado a BD. Verificando/creando tablas...")

    # 1. Asegurarnos que la tabla aportaciones exista. (normalmente existe)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS aportaciones (
            id SERIAL PRIMARY KEY,
            inversor_id INT,
            nombre VARCHAR(200),
            email VARCHAR(200),
            importe DECIMAL(12,2),
            moneda VARCHAR(10),
            estado VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Añadir columnas a aportaciones
    alter_queries_aportaciones = [
        "ALTER TABLE aportaciones ADD COLUMN IF NOT EXISTS fecha_aprobacion TIMESTAMP;",
        "ALTER TABLE aportaciones ADD COLUMN IF NOT EXISTS tasa_diaria DECIMAL(5,2) DEFAULT 0;",
        "ALTER TABLE aportaciones ADD COLUMN IF NOT EXISTS ganancia_acelerada DECIMAL(12,2) DEFAULT 0;"
    ]
    for q in alter_queries_aportaciones:
        try:
            cur.execute(q)
            conn.commit()
            print("Ejecutado:", q)
        except Exception as e:
            print("Error en", q, e)
            conn.rollback()

    # Añadir columna a inversores
    try:
        cur.execute("ALTER TABLE inversores ADD COLUMN IF NOT EXISTS codigo_referido VARCHAR(50);")
        conn.commit()
        print("Ejecutado: ALTER TABLE inversores ADD COLUMN IF NOT EXISTS codigo_referido VARCHAR(50);")
    except Exception as e:
        print("Error en inversores", e)
        conn.rollback()
        
    cur.close()
    conn.close()
    print("Migración completada.")

if __name__ == '__main__':
    migrar_db()
