"""
Script para agregar campos de información económica y patrocinio a la tabla estudiantes
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
    
    print(f"[INFO] Conectando a la base de datos...")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        print("[INFO] Agregando campos de fondos y patrocinio...")
        
        try:
            # Agregar campos de fondos propios
            conn.execute(text("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS fondos_suficientes BOOLEAN DEFAULT FALSE
            """))
            print("[OK] Campo fondos_suficientes agregado")
            
            conn.execute(text("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS monto_fondos DECIMAL(10, 2)
            """))
            print("[OK] Campo monto_fondos agregado")
            
            # Agregar campos de patrocinio
            conn.execute(text("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS tiene_patrocinador BOOLEAN DEFAULT FALSE
            """))
            print("[OK] Campo tiene_patrocinador agregado")
            
            conn.execute(text("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS tipo_patrocinador VARCHAR(50)
            """))
            print("[OK] Campo tipo_patrocinador agregado")
            
            conn.execute(text("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS nombre_patrocinador VARCHAR(200)
            """))
            print("[OK] Campo nombre_patrocinador agregado")
            
            conn.execute(text("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS relacion_patrocinador VARCHAR(100)
            """))
            print("[OK] Campo relacion_patrocinador agregado")
            
            conn.commit()
            print("\n[OK] ✅ Todos los campos agregados exitosamente")
            
            # Verificar estructura
            print("\n[INFO] Verificando nuevos campos...")
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'estudiantes'
                AND column_name IN (
                    'fondos_suficientes', 'monto_fondos', 
                    'tiene_patrocinador', 'tipo_patrocinador',
                    'nombre_patrocinador', 'relacion_patrocinador'
                )
                ORDER BY column_name
            """))
            
            print("\n📋 Campos agregados:")
            for row in result.fetchall():
                print(f"  - {row[0]}: {row[1]} (nullable: {row[2]})")
                
        except Exception as e:
            print(f"[ERROR] {e}")
            conn.rollback()

if __name__ == "__main__":
    main()
