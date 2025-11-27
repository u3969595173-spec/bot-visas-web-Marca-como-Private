"""
Migración: Crear tablas faltantes que estaban en código muerto
Ejecutar SOLO UNA VEZ después del fix del except block

Tablas a crear:
- cursos
- alojamientos
- roles
- usuarios_admin
- logs_auditoria
- notas_internas
- historial_cambios
- email_templates
- universidades_partner
- comisiones
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def migrate():
    print("🔧 Iniciando migración de tablas faltantes...")
    
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    
    try:
        # 1. Tabla cursos
        print("Creando tabla cursos...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cursos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                descripcion TEXT,
                duracion_meses INTEGER,
                precio_eur DECIMAL(10,2),
                ciudad VARCHAR(100),
                nivel_espanol_requerido VARCHAR(50),
                cupos_disponibles INTEGER DEFAULT 0,
                activo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 2. Tabla alojamientos
        print("Creando tabla alojamientos...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alojamientos (
                id SERIAL PRIMARY KEY,
                tipo VARCHAR(100) NOT NULL,
                direccion TEXT,
                ciudad VARCHAR(100),
                precio_mensual_eur DECIMAL(10,2),
                capacidad INTEGER DEFAULT 1,
                disponible BOOLEAN DEFAULT TRUE,
                descripcion TEXT,
                servicios TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_alojamientos_ciudad 
            ON alojamientos(ciudad);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_alojamientos_disponible 
            ON alojamientos(disponible);
        """)
        
        # 3. Tabla roles
        print("Creando tabla roles...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(50) UNIQUE NOT NULL,
                descripcion TEXT,
                permisos JSONB NOT NULL,
                activo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 4. Tabla usuarios_admin
        print("Creando tabla usuarios_admin...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_admin (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                nombre VARCHAR(255),
                password_hash VARCHAR(255) NOT NULL,
                rol_id INTEGER REFERENCES roles(id),
                activo BOOLEAN DEFAULT TRUE,
                ultimo_acceso TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_usuarios_admin_email 
            ON usuarios_admin(email);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_usuarios_admin_rol 
            ON usuarios_admin(rol_id);
        """)
        
        # 5. Tabla logs_auditoria
        print("Creando tabla logs_auditoria...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs_auditoria (
                id SERIAL PRIMARY KEY,
                usuario_email VARCHAR(255),
                accion VARCHAR(100) NOT NULL,
                entidad VARCHAR(100),
                entidad_id INTEGER,
                detalles JSONB,
                ip_address VARCHAR(50),
                user_agent TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_logs_auditoria_usuario 
            ON logs_auditoria(usuario_email);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_logs_auditoria_timestamp 
            ON logs_auditoria(timestamp);
        """)
        
        # 6. Tabla notas_internas
        print("Creando tabla notas_internas...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas_internas (
                id SERIAL PRIMARY KEY,
                estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
                autor_email VARCHAR(255) NOT NULL,
                autor_nombre VARCHAR(255),
                contenido TEXT NOT NULL,
                privada BOOLEAN DEFAULT FALSE,
                importante BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_notas_internas_estudiante 
            ON notas_internas(estudiante_id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_notas_internas_autor 
            ON notas_internas(autor_email);
        """)
        
        # 7. Tabla historial_cambios
        print("Creando tabla historial_cambios...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial_cambios (
                id SERIAL PRIMARY KEY,
                estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
                campo_modificado VARCHAR(100) NOT NULL,
                valor_anterior TEXT,
                valor_nuevo TEXT,
                usuario_email VARCHAR(255),
                usuario_nombre VARCHAR(255),
                razon TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_historial_cambios_estudiante 
            ON historial_cambios(estudiante_id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_historial_cambios_timestamp 
            ON historial_cambios(timestamp);
        """)
        
        # 8. Tabla email_templates
        print("Creando tabla email_templates...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_templates (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) UNIQUE NOT NULL,
                asunto VARCHAR(255) NOT NULL,
                contenido_html TEXT NOT NULL,
                contenido_texto TEXT,
                variables_disponibles TEXT[],
                activo BOOLEAN DEFAULT TRUE,
                ultima_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modificado_por VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 9. Tabla universidades_partner
        print("Creando tabla universidades_partner...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS universidades_partner (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                pais VARCHAR(100) DEFAULT 'España',
                codigo_referido VARCHAR(50) UNIQUE NOT NULL,
                email_contacto VARCHAR(255),
                persona_contacto VARCHAR(255),
                telefono VARCHAR(50),
                tipo_comision VARCHAR(50) DEFAULT 'porcentaje',
                valor_comision DECIMAL(10,2) DEFAULT 15.00,
                estado VARCHAR(50) DEFAULT 'activo',
                logo_url TEXT,
                sitio_web VARCHAR(255),
                notas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_universidades_codigo 
            ON universidades_partner(codigo_referido);
        """)
        
        # 10. Tabla comisiones
        print("Creando tabla comisiones...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comisiones (
                id SERIAL PRIMARY KEY,
                universidad_id INTEGER REFERENCES universidades_partner(id),
                estudiante_id INTEGER REFERENCES estudiantes(id),
                monto_curso DECIMAL(10,2),
                monto_comision DECIMAL(10,2),
                estado VARCHAR(50) DEFAULT 'pendiente',
                fecha_matricula TIMESTAMP,
                fecha_pago TIMESTAMP,
                notas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_comisiones_universidad 
            ON comisiones(universidad_id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_comisiones_estado 
            ON comisiones(estado);
        """)
        
        # 11. Agregar columnas a estudiantes (si no existen)
        print("Agregando columnas a estudiantes...")
        cursor.execute("""
            ALTER TABLE estudiantes 
            ADD COLUMN IF NOT EXISTS curso_asignado_id INTEGER REFERENCES cursos(id),
            ADD COLUMN IF NOT EXISTS alojamiento_asignado_id INTEGER REFERENCES alojamientos(id),
            ADD COLUMN IF NOT EXISTS universidad_referidora_id INTEGER,
            ADD COLUMN IF NOT EXISTS codigo_referido VARCHAR(50);
        """)
        
        # 12. Agregar foreign key a estudiantes
        print("Agregando foreign key a estudiantes...")
        cursor.execute("""
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.table_constraints 
                    WHERE constraint_name = 'fk_estudiantes_universidad'
                ) THEN
                    ALTER TABLE estudiantes 
                    ADD CONSTRAINT fk_estudiantes_universidad 
                    FOREIGN KEY (universidad_referidora_id) 
                    REFERENCES universidades_partner(id);
                END IF;
            END $$;
        """)
        
        # 13. Insertar roles por defecto
        print("Insertando roles por defecto...")
        cursor.execute("""
            INSERT INTO roles (nombre, descripcion, permisos)
            VALUES 
                ('super_admin', 
                 'Administrador con acceso total',
                 '{"estudiantes": ["crear", "leer", "actualizar", "eliminar", "aprobar", "rechazar"], 
                   "documentos": ["leer", "generar", "aprobar", "eliminar"],
                   "usuarios": ["crear", "leer", "actualizar", "eliminar"],
                   "configuracion": ["leer", "actualizar"],
                   "reportes": ["leer", "exportar"],
                   "templates": ["leer", "actualizar"]}'),
                   
                ('admin', 
                 'Administrador estándar',
                 '{"estudiantes": ["crear", "leer", "actualizar", "aprobar", "rechazar"], 
                   "documentos": ["leer", "generar", "aprobar"],
                   "reportes": ["leer", "exportar"]}'),
                   
                ('revisor',
                 'Revisor de solicitudes',
                 '{"estudiantes": ["leer"], 
                   "documentos": ["leer"],
                   "reportes": ["leer"]}'),
                   
                ('asistente',
                 'Asistente administrativo',
                 '{"estudiantes": ["leer", "actualizar"], 
                   "documentos": ["leer", "generar"]}')
            ON CONFLICT (nombre) DO NOTHING
        """)
        
        # 14. Insertar templates de email por defecto
        print("Insertando templates de email...")
        cursor.execute("""
            INSERT INTO email_templates (nombre, asunto, contenido_html, contenido_texto, variables_disponibles)
            VALUES 
                ('bienvenida', 
                 'Bienvenido a Bot Visas Estudio - {{nombre}}',
                 '<h2>¡Bienvenido {{nombre}}!</h2><p>Gracias por registrarte. Tu código de acceso es: <strong>{{codigo_acceso}}</strong></p>',
                 'Bienvenido {{nombre}}! Tu código: {{codigo_acceso}}',
                 ARRAY['nombre', 'email', 'codigo_acceso']),
                 
                ('aprobacion',
                 'Solicitud Aprobada - {{nombre}}',
                 '<h2>¡Felicitaciones {{nombre}}!</h2><p>Tu solicitud ha sido aprobada. Próximos pasos: {{instrucciones}}</p>',
                 'Felicitaciones {{nombre}}! Solicitud aprobada.',
                 ARRAY['nombre', 'email', 'instrucciones']),
                 
                ('rechazo',
                 'Solicitud Requiere Correcciones - {{nombre}}',
                 '<h2>Hola {{nombre}}</h2><p>Tu solicitud requiere correcciones: {{motivo}}</p><p>Sugerencias: {{sugerencias}}</p>',
                 'Hola {{nombre}}, correcciones necesarias: {{motivo}}',
                 ARRAY['nombre', 'email', 'motivo', 'sugerencias'])
            ON CONFLICT (nombre) DO NOTHING
        """)
        
        # 15. Actualizar tabla documentos con campos OCR (si no existen)
        print("Agregando campos OCR a documentos...")
        cursor.execute("""
            ALTER TABLE documentos 
            ADD COLUMN IF NOT EXISTS ocr_procesado BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS ocr_datos_extraidos JSONB,
            ADD COLUMN IF NOT EXISTS ocr_validacion JSONB,
            ADD COLUMN IF NOT EXISTS ocr_nivel_confianza INTEGER DEFAULT 0,
            ADD COLUMN IF NOT EXISTS ocr_alertas JSONB,
            ADD COLUMN IF NOT EXISTS ocr_fecha_procesamiento TIMESTAMP;
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_documentos_ocr_procesado 
            ON documentos(ocr_procesado);
        """)
        
        conn.commit()
        print("✅ Migración completada exitosamente")
        print("""
        Tablas creadas:
        - cursos
        - alojamientos
        - roles (con 4 roles por defecto)
        - usuarios_admin
        - logs_auditoria
        - notas_internas
        - historial_cambios
        - email_templates (con 3 templates)
        - universidades_partner
        - comisiones
        
        Columnas agregadas a estudiantes:
        - curso_asignado_id
        - alojamiento_asignado_id
        - universidad_referidora_id
        - codigo_referido
        
        Columnas agregadas a documentos:
        - ocr_procesado
        - ocr_datos_extraidos
        - ocr_validacion
        - ocr_nivel_confianza
        - ocr_alertas
        - ocr_fecha_procesamiento
        """)
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error durante migración: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate()
