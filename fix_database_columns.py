"""
Script para agregar TODAS las columnas de aprobación que faltan en la base de datos
"""

import os
import psycopg2
from urllib.parse import urlparse

def agregar_columnas_aprobacion():
    """Agrega todas las columnas necesarias para el sistema de aprobaciones"""
    
    # URL de la base de datos de producción  
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ No se encontró DATABASE_URL")
        return
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(database_url, sslmode='require')
        cursor = conn.cursor()
        
        print("🔧 AGREGANDO COLUMNAS DE APROBACIÓN A LA BASE DE DATOS")
        print("=" * 60)
        
        # Lista de columnas a agregar
        columnas = [
            # Estados de aprobación
            ("estado_patrocinio", "VARCHAR(20) DEFAULT 'pendiente'"),
            ("comentarios_patrocinio", "TEXT"),
            ("estado_alojamiento", "VARCHAR(20) DEFAULT 'pendiente'"), 
            ("comentarios_alojamiento", "TEXT"),
            ("estado_seguro_medico", "VARCHAR(20) DEFAULT 'pendiente'"),
            ("comentarios_seguro_medico", "TEXT"),
            
            # Campos de solicitudes (algunos pueden ya existir)
            ("patrocinio_solicitado", "BOOLEAN DEFAULT FALSE"),
            ("gestion_alojamiento_solicitada", "BOOLEAN DEFAULT FALSE"), 
            ("gestion_seguro_solicitada", "BOOLEAN DEFAULT FALSE"),
            
            # Campos adicionales de alojamiento
            ("tiene_alojamiento", "BOOLEAN"),
            ("tipo_alojamiento", "VARCHAR(100)"),
            ("direccion_alojamiento", "TEXT"),
            ("contacto_alojamiento", "VARCHAR(200)"),
            ("telefono_alojamiento", "VARCHAR(50)"),
            ("precio_mensual", "DECIMAL(10,2)"),
            ("moneda_alojamiento", "VARCHAR(10) DEFAULT 'EUR'"),
            ("gestion_solicitada", "BOOLEAN DEFAULT FALSE"),
            
            # Campos adicionales financieros  
            ("fondos_patrocinador", "DECIMAL(15,2)"),
            ("moneda_patrocinador", "VARCHAR(10) DEFAULT 'EUR'"),
            ("patrocinador_nombre", "VARCHAR(200)"),
            ("patrocinador_relacion", "VARCHAR(100)"),
            ("moneda_fondos", "VARCHAR(10) DEFAULT 'EUR'")
        ]
        
        # Intentar agregar cada columna
        columnas_agregadas = 0
        columnas_existentes = 0
        errores = 0
        
        for nombre_columna, definicion in columnas:
            try:
                cursor.execute(f"""
                    ALTER TABLE estudiantes 
                    ADD COLUMN {nombre_columna} {definicion}
                """)
                conn.commit()
                print(f"✅ Agregada: {nombre_columna}")
                columnas_agregadas += 1
                
            except psycopg2.errors.DuplicateColumn:
                print(f"ℹ️  Ya existe: {nombre_columna}")
                columnas_existentes += 1
                conn.rollback()  # Rollback de esta transacción
                
            except Exception as e:
                print(f"❌ Error con {nombre_columna}: {e}")
                errores += 1
                conn.rollback()
        
        print(f"\n📊 RESUMEN:")
        print(f"   ✅ Columnas agregadas: {columnas_agregadas}")
        print(f"   ℹ️  Columnas ya existentes: {columnas_existentes}")
        print(f"   ❌ Errores: {errores}")
        
        if errores == 0:
            print(f"\n🎉 ¡COMPLETADO! Todas las columnas están listas")
            print(f"   🔄 El API debería funcionar ahora")
        else:
            print(f"\n⚠️  Hay algunos errores, pero las columnas principales deberían estar")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    agregar_columnas_aprobacion()