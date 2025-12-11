"""
Agregar soporte para solicitudes de agentes
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
        print("[INFO] Agregando columnas para agentes...")
        
        # Agregar columnas
        try:
            conn.execute(text("""
                ALTER TABLE solicitudes_credito 
                ADD COLUMN IF NOT EXISTS beneficiario_tipo VARCHAR(50)
            """))
            print("  ✅ Agregada columna: beneficiario_tipo")
        except Exception as e:
            print(f"  ℹ️  {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE solicitudes_credito 
                ADD COLUMN IF NOT EXISTS beneficiario_id INTEGER
            """))
            print("  ✅ Agregada columna: beneficiario_id")
        except Exception as e:
            print(f"  ℹ️  {e}")
        
        # Hacer estudiante_id nullable para agentes
        try:
            conn.execute(text("""
                ALTER TABLE solicitudes_credito 
                ALTER COLUMN estudiante_id DROP NOT NULL
            """))
            print("  ✅ estudiante_id ahora permite NULL")
        except Exception as e:
            print(f"  ℹ️  {e}")
        
        conn.commit()
        print("\n✅ Tabla actualizada para soportar agentes")
        print("   - beneficiario_tipo: 'estudiante' o 'agente'")
        print("   - beneficiario_id: ID del estudiante o agente")

if __name__ == "__main__":
    main()
