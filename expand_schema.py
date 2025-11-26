import psycopg2

DATABASE_URL = "postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("Expandiendo schema de estudiantes...")
    
    # Agregar campos faltantes a tabla estudiantes
    campos = [
        "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS nombre VARCHAR(255);",
        "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS email VARCHAR(255);",
        "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS telefono VARCHAR(50);",
        "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS pasaporte VARCHAR(100);",
        "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS edad INTEGER;",
        "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS nacionalidad VARCHAR(100);",
        "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS ciudad_origen VARCHAR(255);",
        "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS especialidad VARCHAR(100);",
        "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS nivel_espanol VARCHAR(50);",
    ]
    
    for campo in campos:
        cursor.execute(campo)
        print(f"✅ {campo}")
    
    conn.commit()
    print("\n✅ Schema expandido correctamente")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
