#!/usr/bin/env python3
"""
Script para agregar columnas de patrocinio a la tabla estudiantes
"""
import psycopg2
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cursor = conn.cursor()
        
        print("🔄 Agregando columnas de patrocinio...")
        
        # Verificar si las columnas ya existen
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'estudiantes' 
            AND column_name IN ('moneda_fondos', 'patrocinador_nombre', 'patrocinador_relacion', 
                                'patrocinio_solicitado', 'estado_patrocinio', 'comentarios_patrocinio')
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        # Lista de columnas a agregar
        columns_to_add = [
            ("moneda_fondos", "VARCHAR(10) DEFAULT 'CUP'", "Moneda de los fondos disponibles"),
            ("patrocinador_nombre", "VARCHAR(255)", "Nombre del patrocinador"),
            ("patrocinador_relacion", "VARCHAR(100)", "Relación con el patrocinador"),
            ("patrocinio_solicitado", "BOOLEAN DEFAULT FALSE", "Si el estudiante solicita patrocinio"),
            ("estado_patrocinio", "VARCHAR(50) DEFAULT 'pendiente'", "Estado de la solicitud de patrocinio"),
            ("comentarios_patrocinio", "TEXT", "Comentarios del admin sobre el patrocinio")
        ]
        
        for column_name, column_def, description in columns_to_add:
            if column_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE estudiantes ADD COLUMN {column_name} {column_def}")
                    print(f"✅ Agregada columna: {column_name} - {description}")
                except Exception as e:
                    print(f"❌ Error agregando {column_name}: {e}")
            else:
                print(f"⚠️  Columna {column_name} ya existe")
        
        conn.commit()
        print("✅ ¡Migración de patrocinio completada!")
        
    except Exception as e:
        print(f"❌ Error en la migración: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()