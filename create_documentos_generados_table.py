"""
Script para crear tabla de documentos generados por el admin
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def crear_tabla_documentos_generados():
    try:
        # URL de Render directamente (reemplazar con la real si es diferente)
        database_url = os.getenv('DATABASE_URL') or 'postgresql://botvisas_user:pqfvUVYtKxLlYb3dUkNO9LMmz8c9bxvn@dpg-ct3tcf52ng1s73a33050-a.oregon-postgres.render.com/botvisas'
        conn = psycopg2.connect(database_url, sslmode='require')
        cursor = conn.cursor()
        
        # Crear tabla documentos_generados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documentos_generados (
                id SERIAL PRIMARY KEY,
                estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
                tipo_documento VARCHAR(100) NOT NULL,
                nombre_archivo VARCHAR(255) NOT NULL,
                contenido_pdf TEXT NOT NULL,
                estado VARCHAR(50) DEFAULT 'generado',
                notas TEXT,
                generado_por VARCHAR(100),
                aprobado_por VARCHAR(100),
                fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_aprobacion TIMESTAMP,
                enviado_estudiante BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Índices para optimizar consultas
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_documentos_generados_estudiante 
            ON documentos_generados(estudiante_id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_documentos_generados_estado 
            ON documentos_generados(estado);
        """)
        
        conn.commit()
        print("✅ Tabla documentos_generados creada correctamente")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al crear tabla: {e}")

if __name__ == "__main__":
    crear_tabla_documentos_generados()
