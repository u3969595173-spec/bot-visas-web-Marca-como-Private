import psycopg2

DATABASE_URL = "postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("Creando tabla documentos...")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id SERIAL PRIMARY KEY,
            estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
            tipo_documento VARCHAR(100) NOT NULL,
            nombre_archivo VARCHAR(255) NOT NULL,
            url_archivo TEXT NOT NULL,
            tamano_bytes INTEGER,
            estado VARCHAR(50) DEFAULT 'pendiente',
            notas TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    print("✅ Tabla documentos creada correctamente")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
