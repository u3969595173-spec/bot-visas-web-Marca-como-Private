"""
Script para crear tabla de agentes/afiliados
Sistema de comisión: 10% para agentes, 5% para estudiantes
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def crear_tabla_agentes():
    """Crear tabla agentes con todos los campos necesarios"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    try:
        # Crear tabla agentes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agentes (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                telefono VARCHAR(50),
                codigo_referido VARCHAR(20) UNIQUE NOT NULL,
                comision_total DECIMAL(10, 2) DEFAULT 0.00,
                credito_disponible DECIMAL(10, 2) DEFAULT 0.00,
                total_referidos INTEGER DEFAULT 0,
                activo BOOLEAN DEFAULT TRUE,
                notas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Índices para mejorar rendimiento
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_agentes_email ON agentes(email);
            CREATE INDEX IF NOT EXISTS idx_agentes_codigo ON agentes(codigo_referido);
            CREATE INDEX IF NOT EXISTS idx_agentes_activo ON agentes(activo);
        """)
        
        # Agregar campo referido_por_agente_id en tabla estudiantes
        cursor.execute("""
            ALTER TABLE estudiantes 
            ADD COLUMN IF NOT EXISTS referido_por_agente_id INTEGER REFERENCES agentes(id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_estudiantes_agente ON estudiantes(referido_por_agente_id);
        """)
        
        conn.commit()
        print("✅ Tabla 'agentes' creada exitosamente")
        print("✅ Campo 'referido_por_agente_id' agregado a estudiantes")
        print("✅ Índices creados correctamente")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error creando tabla: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    crear_tabla_agentes()
