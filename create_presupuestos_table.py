"""
Script para crear tabla de presupuestos/cotizaciones
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
        print("[INFO] Creando tabla presupuestos...")
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS presupuestos (
                id SERIAL PRIMARY KEY,
                estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
                servicios JSONB NOT NULL,
                precio_solicitado NUMERIC(10,2) NOT NULL,
                precio_ofertado NUMERIC(10,2),
                forma_pago TEXT,
                mensaje_admin TEXT,
                estado VARCHAR(20) DEFAULT 'pendiente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.commit()
        print("[OK] Tabla presupuestos creada exitosamente")
        
        # Crear índice para búsquedas rápidas
        print("[INFO] Creando índices...")
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_presupuestos_estudiante 
            ON presupuestos(estudiante_id)
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_presupuestos_estado 
            ON presupuestos(estado)
        """))
        conn.commit()
        print("[OK] Índices creados")
        
        print("\n[OK] ✅ Tabla presupuestos lista para usar")
        print("\nEstados disponibles:")
        print("  - pendiente: Estudiante envió solicitud, esperando admin")
        print("  - ofertado: Admin hizo contraoferta, esperando estudiante")
        print("  - aceptado: Estudiante aceptó la oferta")
        print("  - rechazado: Estudiante rechazó la oferta")

if __name__ == "__main__":
    main()
