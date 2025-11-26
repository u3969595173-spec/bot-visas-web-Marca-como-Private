import os
from sqlalchemy import create_engine, text

DATABASE_URL = 'postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas'

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Agregar columnas faltantes
        columnas = [
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS telegram_id VARCHAR(255)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS nombre_completo VARCHAR(255)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS numero_pasaporte VARCHAR(50)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS fecha_nacimiento DATE",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS carrera_actual VARCHAR(255)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS nivel_educacion VARCHAR(100)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS especialidad_interes VARCHAR(255)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS telefono_emergencia VARCHAR(50)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS contacto_emergencia_nombre VARCHAR(255)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS estado_inscripcion VARCHAR(50) DEFAULT 'pendiente'",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS fecha_inscripcion TIMESTAMP",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS estado_visa VARCHAR(50)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS fecha_cita_consulado TIMESTAMP",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS numero_expediente VARCHAR(100)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS estado_procesamiento VARCHAR(50) DEFAULT 'pendiente'",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS fecha_procesamiento_automatico TIMESTAMP",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS fecha_revision_admin TIMESTAMP",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS admin_revisor_id INTEGER",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS notas_admin TEXT",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS modificaciones_admin TEXT",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS documentos_completados INTEGER DEFAULT 0",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS documentos_pendientes INTEGER DEFAULT 0",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS fecha_ultimo_documento TIMESTAMP",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS tiene_fondos_propios BOOLEAN DEFAULT FALSE",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS tiene_patrocinador BOOLEAN DEFAULT FALSE",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS patrocinador_id INTEGER",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS monto_fondos_disponibles NUMERIC(10,2)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS necesita_alojamiento BOOLEAN DEFAULT FALSE",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS alojamiento_asignado_id INTEGER",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS agente_asignado VARCHAR(255)",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS prioridad INTEGER DEFAULT 3",
            "ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        ]
        
        for sql in columnas:
            conn.execute(text(sql))
            print(f"[OK] Ejecutado: {sql[:60]}...")
        
        conn.commit()
        print("\n[OK] Todas las columnas agregadas exitosamente")
            
except Exception as e:
    print(f"[ERROR] {e}")
