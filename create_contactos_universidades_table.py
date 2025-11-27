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
        
        # BORRAR tabla existente para recrearla con todas las universidades
        print("🔄 Recreando tabla con lista completa de universidades...")
        cur.execute("DROP TABLE IF EXISTS contactos_universidades CASCADE")
        
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
        
        # Insertar universidades predefinidas - LISTA COMPLETA
        universidades = [
            # === UNIVERSIDADES PRIVADAS ONLINE (MÁS FLEXIBLES) ===
            ('UCAM - Universidad Católica de Murcia', 'internacional@ucam.edu', '+34 968 278 160', 'Departamento Internacional', 'España', 'Murcia', 'Privada', 'Grados, Másteres, FP, Medicina, Ingeniería'),
            ('UNIR - Universidad Internacional de La Rioja', 'admisiones@unir.net', '+34 941 209 743', 'Admisiones Internacionales', 'España', 'Logroño', 'Privada', 'Grados Online, Másteres Online, Doctorados'),
            ('VIU - Universidad Internacional de Valencia', 'informacion@universidadviu.com', '+34 961 924 950', 'Información y Admisiones', 'España', 'Valencia', 'Privada', 'Grados Online/Presencial, Másteres, Doctorados'),
            ('UDIMA - Universidad a Distancia de Madrid', 'info@udima.es', '+34 918 561 699', 'Información', 'España', 'Madrid', 'Privada', 'Grados Online, Másteres, Doctorados'),
            ('UOC - Universitat Oberta de Catalunya', 'internacional@uoc.edu', '+34 932 532 300', 'Admisiones Internacionales', 'España', 'Barcelona', 'Privada', 'Grados Online, Másteres, Idiomas'),
            
            # === UNIVERSIDADES PRIVADAS MADRID ===
            ('Universidad Europea de Madrid', 'admision@universidadeuropea.es', '+34 912 115 200', 'Admisiones', 'España', 'Madrid', 'Privada', 'Grados, Másteres, Medicina, Ingeniería, Deportes'),
            ('Universidad Nebrija', 'admision@nebrija.es', '+34 914 521 100', 'Admisiones', 'España', 'Madrid', 'Privada', 'Grados, Másteres, Idiomas, Comunicación'),
            ('Universidad CEU San Pablo', 'informacion@ceu.es', '+34 914 566 300', 'Información', 'España', 'Madrid', 'Privada', 'Grados, Másteres, Medicina, Derecho, Arquitectura'),
            ('Universidad Francisco de Vitoria', 'admision@ufv.es', '+34 913 510 303', 'Admisiones', 'España', 'Madrid', 'Privada', 'Grados, Másteres, Medicina, Biotecnología'),
            ('Universidad Camilo José Cela', 'admisiones@ucjc.edu', '+34 918 153 131', 'Admisiones', 'España', 'Madrid', 'Privada', 'Grados, Másteres, Deportes, Comunicación'),
            ('Universidad Alfonso X el Sabio', 'admision@uax.es', '+34 918 109 200', 'Admisiones', 'España', 'Madrid', 'Privada', 'Grados, Másteres, Medicina, Arquitectura'),
            
            # === UNIVERSIDADES PRIVADAS BARCELONA ===
            ('Universitat Abat Oliba CEU', 'admissions@uao.es', '+34 932 540 900', 'Admissions', 'España', 'Barcelona', 'Privada', 'Grados, Másteres, Derecho, ADE, Comunicación'),
            ('Universidad Internacional de Catalunya', 'admissions@uic.es', '+34 932 541 800', 'Admissions Office', 'España', 'Barcelona', 'Privada', 'Grados, Másteres, Medicina, Odontología, Arquitectura'),
            ('Universitat Ramon Llull', 'info@url.edu', '+34 932 533 000', 'Información', 'España', 'Barcelona', 'Privada', 'Grados, Másteres, Ingeniería, Arquitectura, Diseño'),
            ('ESADE Business School', 'admissions@esade.edu', '+34 932 806 162', 'Admissions', 'España', 'Barcelona', 'Privada', 'Business, MBA, Law, Executive Education'),
            ('EU Business School Barcelona', 'info.bcn@euruni.edu', '+34 932 016 550', 'Admissions Office', 'España', 'Barcelona', 'Privada', 'Business, MBA, Entrepreneurship'),
            ('INSA Business School', 'admissions@grupoinsabarcelona.com', '+34 933 803 161', 'Admissions', 'España', 'Barcelona', 'Privada', 'Business, Marketing, Comunicación, Diseño'),
            
            # === UNIVERSIDADES PRIVADAS VALENCIA ===
            ('Universidad Católica de Valencia', 'informacion@ucv.es', '+34 963 637 412', 'Información', 'España', 'Valencia', 'Privada', 'Grados, Másteres, Medicina, Odontología, Psicología'),
            ('Universidad Europea de Valencia', 'informacion.valencia@universidadeuropea.es', '+34 961 366 850', 'Información', 'España', 'Valencia', 'Privada', 'Grados, Másteres, Fisioterapia, Deportes'),
            ('Florida Universitària', 'info@florida-uni.es', '+34 961 590 555', 'Información', 'España', 'Valencia', 'Privada', 'Grados, FP Superior, Diseño, Multimedia'),
            
            # === UNIVERSIDADES PRIVADAS ANDALUCÍA ===
            ('Universidad Loyola Andalucía', 'admisiones@uloyola.es', '+34 955 641 600', 'Admisiones', 'España', 'Sevilla', 'Privada', 'Grados, Másteres, ADE, Derecho, Ingeniería'),
            ('Universidad Internacional de Andalucía', 'informacion@unia.es', '+34 954 462 299', 'Información', 'España', 'Sevilla', 'Pública', 'Másteres, Doctorados, Especialización'),
            
            # === ESCUELAS DE NEGOCIOS ===
            ('EAE Business School Madrid', 'admisiones@eae.es', '+34 914 160 511', 'Admisiones', 'España', 'Madrid', 'Privada', 'MBA, Másteres Business, Marketing, Finanzas'),
            ('EAE Business School Barcelona', 'info.barcelona@eae.es', '+34 933 592 088', 'Información', 'España', 'Barcelona', 'Privada', 'MBA, Másteres Business, International Business'),
            ('ESERP Business School', 'info@eserp.com', '+34 934 583 688', 'Información', 'España', 'Barcelona', 'Privada', 'Business, Marketing, Turismo, Comunicación'),
            ('ESIC Business & Marketing School', 'informacion@esic.edu', '+34 914 524 100', 'Información', 'España', 'Madrid', 'Privada', 'Business, Marketing, Digital Business'),
            ('IMF Business School', 'info@imf-formacion.com', '+34 917 191 519', 'Información', 'España', 'Madrid', 'Privada', 'MBA, Másteres Online, Recursos Humanos, Marketing'),
            
            # === ESCUELAS TÉCNICAS Y DISEÑO ===
            ('IED Madrid - Instituto Europeo di Design', 'info@madrid.ied.es', '+34 914 480 444', 'Información', 'España', 'Madrid', 'Privada', 'Diseño, Moda, Artes Visuales, Gestión'),
            ('IED Barcelona', 'info@bcn.ied.es', '+34 932 385 889', 'Información', 'España', 'Barcelona', 'Privada', 'Diseño, Moda, Management, Visual Arts'),
            ('Escuela Superior de Diseño de Barcelona', 'info@esdesignbarcelona.com', '+34 932 380 808', 'Información', 'España', 'Barcelona', 'Privada', 'Diseño Gráfico, Interiores, Producto, Digital'),
            ('Escuela TAI', 'informacion@escuela-tai.com', '+34 915 337 300', 'Información', 'España', 'Madrid', 'Privada', 'Artes Escénicas, Cine, Música, Fotografía'),
            
            # === FORMACIÓN PROFESIONAL SUPERIOR ===
            ('CENP - Centro de Estudios Profesionales', 'info@cenp.es', '+34 915 216 060', 'Información', 'España', 'Madrid', 'Privada', 'FP Superior: Informática, Diseño, Administración'),
            ('MEDAC - Centro de Formación Profesional', 'informacion@medac.es', '+34 955 206 000', 'Información', 'España', 'Sevilla', 'Privada', 'FP Superior: Sanidad, Deportes, Informática, Imagen'),
            ('Ilerna Online', 'info@ilerna.es', '+34 902 002 152', 'Información', 'España', 'Barcelona', 'Privada', 'FP Online: Sanidad, Informática, Administración'),
            
            # === UNIVERSIDADES PÚBLICAS (MÁS SELECTIVAS PERO ECONÓMICAS) ===
            ('Universidad Complutense de Madrid', 'internacional@ucm.es', '+34 914 520 400', 'Relaciones Internacionales', 'España', 'Madrid', 'Pública', 'Todas las áreas - Universidad más grande España'),
            ('Universidad Autónoma de Madrid', 'relaciones.internacionales@uam.es', '+34 914 974 000', 'RRII', 'España', 'Madrid', 'Pública', 'Ciencias, Medicina, Derecho, Económicas'),
            ('Universidad de Barcelona', 'internacional@ub.edu', '+34 934 021 100', 'Oficina Internacional', 'España', 'Barcelona', 'Pública', 'Todas las áreas - Top 1 España en rankings'),
            ('Universidad Autónoma de Barcelona', 'international.welcome@uab.cat', '+34 935 811 111', 'International Welcome', 'España', 'Barcelona', 'Pública', 'Medicina, Veterinaria, Traducción, Ingeniería'),
            ('Universidad Politécnica de Madrid', 'ori@upm.es', '+34 910 674 000', 'Oficina RRII', 'España', 'Madrid', 'Pública', 'Ingenierías, Arquitectura, Deportes'),
            ('Universidad Politécnica de Valencia', 'ori@upv.es', '+34 963 877 000', 'Oficina RRII', 'España', 'Valencia', 'Pública', 'Ingenierías, Arquitectura, Bellas Artes'),
            ('Universidad de Valencia', 'international@uv.es', '+34 963 864 100', 'Relaciones Internacionales', 'España', 'Valencia', 'Pública', 'Medicina, Farmacia, Biología, Física'),
            ('Universidad de Sevilla', 'ori@us.es', '+34 954 551 000', 'Oficina RRII', 'España', 'Sevilla', 'Pública', 'Medicina, Arquitectura, Ingenierías, Filología'),
            ('Universidad de Granada', 'internacional@ugr.es', '+34 958 243 000', 'Relaciones Internacionales', 'España', 'Granada', 'Pública', 'Traducción, Medicina, Bellas Artes'),
            ('Universidad de Málaga', 'internacional@uma.es', '+34 952 131 000', 'RRII', 'España', 'Málaga', 'Pública', 'Turismo, Medicina, Ingeniería Telecomunicaciones')
        ]
        
        for uni in universidades:
            cur.execute("""
                INSERT INTO contactos_universidades 
                (universidad, email, telefono, contacto_nombre, pais, ciudad, tipo_universidad, programas_interes, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pendiente')
            """, uni)
        
        conn.commit()
        print("✅ Tabla contactos_universidades creada exitosamente")
        print(f"✅ {len(universidades)} universidades agregadas")
        print("\n📊 DISTRIBUCIÓN:")
        print("   🔵 Privadas Online: 5")
        print("   🏢 Privadas Madrid: 6") 
        print("   🏢 Privadas Barcelona: 6")
        print("   🏢 Privadas Valencia: 3")
        print("   🏢 Privadas Andalucía: 2")
        print("   💼 Escuelas de Negocios: 5")
        print("   🎨 Escuelas Técnicas/Diseño: 4")
        print("   📚 Formación Profesional: 3")
        print("   🏛️ Universidades Públicas: 10")
        print(f"\n   📧 TOTAL: {len(universidades)} UNIVERSIDADES LISTAS PARA CONTACTAR")
        print("\n💡 Estrategia: Contacta primero las privadas (más flexibles)")
        print("   Las públicas son más selectivas pero más baratas")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al crear tabla: {e}")

if __name__ == "__main__":
    create_contactos_universidades_table()
