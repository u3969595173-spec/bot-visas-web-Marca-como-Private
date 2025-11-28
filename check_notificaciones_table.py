#!/usr/bin/env python3

import psycopg2
import os
from config import DATABASE_URL

def main():
    try:
        # Usar la conexión de base de datos de config.py
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Verificar estructura de la tabla notificaciones
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'notificaciones' 
            ORDER BY ordinal_position;
        """)
        
        print("=== ESTRUCTURA TABLA NOTIFICACIONES ===")
        columns = cur.fetchall()
        for column_name, data_type in columns:
            print(f"- {column_name}: {data_type}")
        
        if not columns:
            print("❌ La tabla notificaciones no existe")
        
        cur.close()
        conn.close()
        print("\n✅ Verificación completada")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()