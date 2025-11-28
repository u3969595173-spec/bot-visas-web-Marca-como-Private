"""
Verificar si existen las columnas del sistema de referidos en producción
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def main():
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("[ERROR] No se encontró DATABASE_URL en .env")
        return
    
    print(f"[INFO] Conectando a la base de datos de producción...")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        # Verificar columnas de la tabla estudiantes
        print("\n[INFO] Verificando columnas de 'estudiantes'...")
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'estudiantes'
            AND column_name IN ('codigo_referido', 'referido_por_id', 'credito_disponible', 'tipo_recompensa')
            ORDER BY column_name
        """))
        
        columnas = result.fetchall()
        
        if not columnas:
            print("❌ NO SE ENCONTRARON las columnas del sistema de referidos")
            print("\n[INFO] Columnas actuales de 'estudiantes':")
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'estudiantes'
                ORDER BY ordinal_position
            """))
            for row in result.fetchall():
                print(f"  - {row[0]}")
        else:
            print("✅ Columnas encontradas:")
            for row in columnas:
                print(f"  - {row[0]}: {row[1]} (nullable: {row[2]})")
        
        # Verificar datos de ejemplo
        print("\n[INFO] Datos de estudiantes:")
        result = conn.execute(text("""
            SELECT id, nombre, email, 
                   CASE WHEN EXISTS (
                       SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'estudiantes' AND column_name = 'codigo_referido'
                   ) THEN 'SI' ELSE 'NO' END as tiene_columna
            FROM estudiantes
            LIMIT 3
        """))
        
        for row in result.fetchall():
            print(f"  ID: {row[0]} | Nombre: {row[1]} | Email: {row[2]}")

if __name__ == "__main__":
    main()
