#!/usr/bin/env python3
"""
Script para crear tabla de mensajes entre admin y agentes
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_mensajes_agentes_table():
    """Crear tabla para chat admin-agente"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        print("💬 Creando tabla mensajes_agentes...")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes_agentes (
                id SERIAL PRIMARY KEY,
                agente_id INTEGER REFERENCES agentes(id) ON DELETE CASCADE,
                remitente VARCHAR(20) NOT NULL,
                mensaje TEXT NOT NULL,
                leido BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear índices
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_mensajes_agentes_agente 
            ON mensajes_agentes(agente_id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_mensajes_agentes_leido 
            ON mensajes_agentes(leido);
        """)
        
        conn.commit()
        
        print("✅ Tabla mensajes_agentes creada exitosamente")
        print("\n📊 Estructura de la tabla:")
        print("  - id: Identificador único")
        print("  - agente_id: Referencia al agente")
        print("  - remitente: 'admin' o 'agente'")
        print("  - mensaje: Contenido del mensaje")
        print("  - leido: Si fue leído por el destinatario")
        print("  - created_at: Fecha del mensaje")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    create_mensajes_agentes_table()
