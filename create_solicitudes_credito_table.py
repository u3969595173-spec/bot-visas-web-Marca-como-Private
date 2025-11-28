"""
Crear tabla para solicitudes de uso de crédito de referidos
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
        print("[INFO] Creando tabla solicitudes_credito...")
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS solicitudes_credito (
                id SERIAL PRIMARY KEY,
                estudiante_id INTEGER REFERENCES estudiantes(id),
                tipo VARCHAR(20) NOT NULL, -- 'retiro' o 'descuento'
                monto NUMERIC(10,2) NOT NULL,
                estado VARCHAR(20) DEFAULT 'pendiente', -- 'pendiente', 'aprobada', 'rechazada'
                fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_respuesta TIMESTAMP,
                respondido_por VARCHAR(100),
                notas TEXT
            )
        """))
        conn.commit()
        
        print("✅ Tabla solicitudes_credito creada exitosamente")

if __name__ == "__main__":
    main()
