"""
Script para crear tabla de contactos con universidades
"""
import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_contactos_universidades_table():
    """Crear tabla para tracking de contactos con universidades"""
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        # Crear tabla de contactos universidades
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contactos_universidades (
                id SERIAL PRIMARY KEY,
                universidad VARCHAR(200) NOT NULL,
                email VARCHAR(200) NOT NULL,
                telefono VARCHAR(50),
                contacto_nombre VARCHAR(200),
                pais VARCHAR(100) DEFAULT 'España',
                ciudad VARCHAR(100),
                tipo_universidad VARCHAR(100), -- Privada/Pública
                programas_interes TEXT,
                estado VARCHAR(50) DEFAULT 'pendiente', -- pendiente, contactado, respondido, reunion_agendada, acuerdo_firmado
                fecha_contacto TIMESTAMP,
                fecha_respuesta TIMESTAMP,
                fecha_reunion TIMESTAMP,
                notas TEXT,
                condiciones_propuestas TEXT, -- Condiciones que ofrecen
                comision_acordada DECIMAL(10, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear índices para mejorar rendimiento
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_contactos_universidad 
            ON contactos_universidades(universidad);
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_contactos_estado 
            ON contactos_universidades(estado);
        """)
        
        # Insertar universidades predefinidas
        universidades = [
            ('UCAM - Universidad Católica de Murcia', 'internacional@ucam.edu', '+34 968 278 160', 'Departamento Internacional', 'España', 'Murcia', 'Privada', 'Grados, Másteres, Formación Profesional'),
            ('UNIR - Universidad Internacional de La Rioja', 'admisiones@unir.net', '+34 941 209 743', 'Admisiones Internacionales', 'España', 'Logroño', 'Privada', 'Grados Online, Másteres Online'),
            ('VIU - Universidad Internacional de Valencia', 'informacion@universidadviu.com', '+34 961 924 950', 'Información y Admisiones', 'España', 'Valencia', 'Privada', 'Grados, Másteres, Doctorados'),
            ('INSA - Business, Marketing & Communication School', 'admissions@grupoinsabarcelona.com', '+34 933 803 161', 'Admissions Department', 'España', 'Barcelona', 'Privada', 'Business, Marketing, Comunicación'),
            ('EU Business School', 'info@euruni.edu', '+34 932 016 550', 'Admissions Office', 'España', 'Barcelona', 'Privada', 'Business, MBA, Entrepreneurship')
        ]
        
        for uni in universidades:
            cur.execute("""
                INSERT INTO contactos_universidades 
                (universidad, email, telefono, contacto_nombre, pais, ciudad, tipo_universidad, programas_interes, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pendiente')
                ON CONFLICT DO NOTHING
            """, uni)
        
        conn.commit()
        print("✅ Tabla contactos_universidades creada exitosamente")
        print("✅ 5 universidades objetivo agregadas")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al crear tabla: {e}")

if __name__ == "__main__":
    create_contactos_universidades_table()
