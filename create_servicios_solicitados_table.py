#!/usr/bin/env python3
"""
Script para crear tabla de servicios solicitados por estudiantes
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def create_servicios_table():
    """Crea tabla servicios_solicitados"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    print("🔧 Creando tabla servicios_solicitados...")
    
    # Crear tabla
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios_solicitados (
            id SERIAL PRIMARY KEY,
            estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
            servicio_id VARCHAR(100) NOT NULL,
            servicio_nombre VARCHAR(255) NOT NULL,
            estado VARCHAR(50) DEFAULT 'pendiente',
            precio DECIMAL(10, 2),
            notas TEXT,
            fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_respuesta TIMESTAMP,
            respondido_por VARCHAR(255)
        );
    """)
    
    # Crear índices
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_servicios_estudiante 
        ON servicios_solicitados(estudiante_id);
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_servicios_estado 
        ON servicios_solicitados(estado);
    """)
    
    conn.commit()
    print("✅ Tabla servicios_solicitados creada exitosamente")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_servicios_table()
