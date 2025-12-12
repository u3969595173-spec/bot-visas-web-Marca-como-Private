#!/usr/bin/env python3
"""
Script para crear tabla de solicitudes de retiro de agentes
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_retiros_agentes_table():
    """Crear tabla para solicitudes de retiro de agentes"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        print("💰 Creando tabla solicitudes_retiro_agentes...")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solicitudes_retiro_agentes (
                id SERIAL PRIMARY KEY,
                agente_id INTEGER REFERENCES agentes(id) ON DELETE CASCADE,
                monto DECIMAL(10,2) NOT NULL,
                estado VARCHAR(20) DEFAULT 'pendiente',
                notas_agente TEXT,
                comentarios_admin TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear índices
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_retiros_agentes_agente 
            ON solicitudes_retiro_agentes(agente_id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_retiros_agentes_estado 
            ON solicitudes_retiro_agentes(estado);
        """)
        
        conn.commit()
        
        print("✅ Tabla solicitudes_retiro_agentes creada exitosamente")
        print("\n📊 Estructura de la tabla:")
        print("  - id: Identificador único")
        print("  - agente_id: Referencia al agente")
        print("  - monto: Cantidad a retirar")
        print("  - estado: pendiente/aprobado/rechazado")
        print("  - notas_agente: Mensaje del agente al solicitar")
        print("  - comentarios_admin: Respuesta del administrador")
        print("  - created_at: Fecha de solicitud")
        print("  - updated_at: Fecha de última actualización")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    create_retiros_agentes_table()
