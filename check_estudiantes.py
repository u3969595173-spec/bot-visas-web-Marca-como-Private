import os
from sqlalchemy import create_engine, text

DATABASE_URL = 'postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas'

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, nombre, email, tipo_visa, estado, created_at FROM estudiantes LIMIT 5"))
        rows = result.fetchall()
        
        if rows:
            print(f"[INFO] Encontrados {len(rows)} estudiantes:")
            for row in rows:
                print(f"  ID: {row[0]}, Nombre: {row[1]}, Email: {row[2]}")
        else:
            print("[WARN] No hay estudiantes en la base de datos")
            
except Exception as e:
    print(f"[ERROR] {e}")
