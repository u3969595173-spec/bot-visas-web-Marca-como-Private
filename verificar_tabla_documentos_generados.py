"""
Script para verificar y crear la tabla documentos_generados si no existe
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Verificar si la tabla existe
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'documentos_generados'
            )
        """))
        
        existe = result.fetchone()[0]
        
        if existe:
            print("✅ La tabla 'documentos_generados' YA existe")
            
            # Contar registros
            result = conn.execute(text("SELECT COUNT(*) FROM documentos_generados"))
            count = result.fetchone()[0]
            print(f"   📊 Registros en la tabla: {count}")
        else:
            print("⚠️ La tabla 'documentos_generados' NO existe")
            print("   Creando tabla...")
            
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS documentos_generados (
                    id SERIAL PRIMARY KEY,
                    estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
                    tipo_documento VARCHAR(100) NOT NULL,
                    nombre_archivo VARCHAR(255) NOT NULL,
                    contenido_pdf TEXT,
                    estado VARCHAR(50) DEFAULT 'pendiente',
                    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_aprobacion TIMESTAMP,
                    enviado_estudiante BOOLEAN DEFAULT FALSE,
                    notas TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("✅ Tabla 'documentos_generados' creada exitosamente")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
