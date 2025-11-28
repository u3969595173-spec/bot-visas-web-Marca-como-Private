#!/usr/bin/env python3
"""
Script para agregar columnas de información de alojamiento a la tabla estudiantes
Ejecutar: python add_alojamiento_columns.py
"""

import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def add_alojamiento_columns():
    """Agregar columnas relacionadas con alojamiento a la tabla estudiantes"""
    
    # Columnas a agregar
    alojamiento_columns = {
        'tiene_alojamiento': 'BOOLEAN DEFAULT NULL',
        'tipo_alojamiento': 'VARCHAR(100)',
        'direccion_alojamiento': 'TEXT',
        'contacto_alojamiento': 'VARCHAR(255)',
        'telefono_alojamiento': 'VARCHAR(50)',
        'precio_mensual': 'DECIMAL(10,2)',
        'moneda_alojamiento': 'VARCHAR(10) DEFAULT \'EUR\'',
        'gestion_solicitada': 'BOOLEAN DEFAULT FALSE',
        'estado_alojamiento': 'VARCHAR(50) DEFAULT \'pendiente\'',
        'comentarios_alojamiento': 'TEXT'
    }
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        print("🏠 Agregando columnas de alojamiento a la tabla estudiantes...")
        
        # Verificar si las columnas ya existen antes de agregarlas
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'estudiantes'
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        columns_added = []
        for column_name, column_def in alojamiento_columns.items():
            if column_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE estudiantes ADD COLUMN {column_name} {column_def}")
                    columns_added.append(column_name)
                    print(f"✅ Columna '{column_name}' agregada exitosamente")
                except psycopg2.Error as e:
                    print(f"❌ Error agregando columna '{column_name}': {e}")
            else:
                print(f"⚠️ Columna '{column_name}' ya existe, omitiendo...")
        
        # Confirmar cambios
        conn.commit()
        
        if columns_added:
            print(f"\n🎉 Se agregaron {len(columns_added)} columnas nuevas:")
            for col in columns_added:
                print(f"   - {col}")
        else:
            print("\n📝 No se agregaron columnas nuevas (todas ya existían)")
        
        print("\n✅ Migración de alojamiento completada exitosamente")
        
    except psycopg2.Error as e:
        print(f"❌ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    
    return True

if __name__ == "__main__":
    print("🚀 Iniciando migración de columnas de alojamiento...")
    success = add_alojamiento_columns()
    
    if success:
        print("\n🎯 ¡Migración completada! Las columnas de alojamiento están listas.")
        print("\nColumnas agregadas:")
        print("- tiene_alojamiento: ¿El estudiante ya tiene alojamiento?")
        print("- tipo_alojamiento: Tipo de alojamiento (piso, habitación, etc.)")
        print("- direccion_alojamiento: Dirección completa del alojamiento")
        print("- contacto_alojamiento: Nombre del contacto/propietario")
        print("- telefono_alojamiento: Teléfono de contacto")
        print("- precio_mensual: Precio mensual del alojamiento")
        print("- moneda_alojamiento: Moneda del precio (EUR por defecto)")
        print("- gestion_solicitada: ¿Solicita que la empresa gestione?")
        print("- estado_alojamiento: Estado de la gestión (pendiente/aprobado/rechazado)")
        print("- comentarios_alojamiento: Comentarios y preferencias")
    else:
        print("\n💥 La migración falló. Revisar errores arriba.")