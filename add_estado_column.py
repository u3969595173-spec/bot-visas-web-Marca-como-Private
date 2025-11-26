import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("[ERROR] DATABASE_URL no configurada")
    exit(1)

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Agregar columna estado si no existe
        conn.execute(text("""
            ALTER TABLE estudiantes 
            ADD COLUMN IF NOT EXISTS estado VARCHAR(50) DEFAULT 'pendiente'
        """))
        conn.commit()
        print("[OK] Columna 'estado' agregada a tabla 'estudiantes'")
        
        # Verificar
        result = conn.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'estudiantes' AND column_name = 'estado'
        """))
        row = result.fetchone()
        if row:
            print(f"[OK] Columna verificada: {row[0]} ({row[1]})")
        else:
            print("[WARN] No se pudo verificar la columna")
            
except Exception as e:
    print(f"[ERROR] {e}")
