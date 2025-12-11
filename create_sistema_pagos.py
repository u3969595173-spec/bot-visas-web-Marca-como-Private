"""
Sistema de pagos y comisiones
Cada pago genera comisión para el referidor (agente 10% o estudiante 5%)
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def crear_sistema_pagos():
    """Crear tabla de pagos y sistema de comisiones"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    try:
        # Tabla de pagos de estudiantes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pagos_estudiantes (
                id SERIAL PRIMARY KEY,
                estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
                presupuesto_id INTEGER REFERENCES presupuestos(id) ON DELETE SET NULL,
                concepto VARCHAR(255) NOT NULL,
                monto DECIMAL(10, 2) NOT NULL,
                fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metodo_pago VARCHAR(100),
                referencia_pago VARCHAR(255),
                notas TEXT,
                comision_generada DECIMAL(10, 2) DEFAULT 0.00,
                comision_pagada BOOLEAN DEFAULT FALSE,
                beneficiario_tipo VARCHAR(50),
                beneficiario_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by VARCHAR(100)
            );
        """)
        
        # Índices
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_pagos_estudiante ON pagos_estudiantes(estudiante_id);
            CREATE INDEX IF NOT EXISTS idx_pagos_presupuesto ON pagos_estudiantes(presupuesto_id);
            CREATE INDEX IF NOT EXISTS idx_pagos_fecha ON pagos_estudiantes(fecha_pago);
            CREATE INDEX IF NOT EXISTS idx_pagos_beneficiario ON pagos_estudiantes(beneficiario_tipo, beneficiario_id);
        """)
        
        # Tabla de historial de comisiones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial_comisiones (
                id SERIAL PRIMARY KEY,
                pago_id INTEGER NOT NULL REFERENCES pagos_estudiantes(id) ON DELETE CASCADE,
                beneficiario_tipo VARCHAR(50) NOT NULL,
                beneficiario_id INTEGER NOT NULL,
                monto_comision DECIMAL(10, 2) NOT NULL,
                porcentaje DECIMAL(5, 2) NOT NULL,
                estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id),
                fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                pagada BOOLEAN DEFAULT FALSE,
                fecha_pago TIMESTAMP,
                notas TEXT
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_historial_beneficiario ON historial_comisiones(beneficiario_tipo, beneficiario_id);
            CREATE INDEX IF NOT EXISTS idx_historial_pago ON historial_comisiones(pago_id);
        """)
        
        conn.commit()
        print("✅ Tabla 'pagos_estudiantes' creada")
        print("✅ Tabla 'historial_comisiones' creada")
        print("✅ Índices creados correctamente")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    crear_sistema_pagos()
