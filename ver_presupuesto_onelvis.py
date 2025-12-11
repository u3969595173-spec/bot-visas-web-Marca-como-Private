"""
Ver estructura de tabla presupuestos y datos de Onelvis
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def ver_estructura_presupuestos():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("ESTRUCTURA DE TABLA PRESUPUESTOS")
    print("="*80)
    
    # Ver todas las columnas
    cursor.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'presupuestos'
        ORDER BY ordinal_position
    """)
    
    columnas = cursor.fetchall()
    print("\n📋 COLUMNAS:\n")
    for col in columnas:
        print(f"   {col[0]:30} {col[1]:20} {col[2]}")
    
    # Ver presupuesto de Onelvis con TODAS las columnas
    print("\n" + "="*80)
    print("PRESUPUESTO DE ONELVIS")
    print("="*80 + "\n")
    
    cursor.execute("""
        SELECT p.*, e.nombre, e.referido_por_id
        FROM presupuestos p
        JOIN estudiantes e ON p.estudiante_id = e.id
        WHERE e.nombre LIKE '%onelvis%'
        ORDER BY p.id DESC
        LIMIT 1
    """)
    
    pres = cursor.fetchone()
    if pres:
        col_names = [desc[0] for desc in cursor.description]
        print("DATOS DEL PRESUPUESTO:\n")
        for i, col_name in enumerate(col_names):
            valor = pres[i]
            if valor is not None:
                print(f"   {col_name:30} {valor}")
        
        # Calcular comisión si hay precio
        for i, col_name in enumerate(col_names):
            if 'precio' in col_name.lower() and pres[i] and pres[i] > 0:
                comision = pres[i] * 0.05
                print(f"\n   💰 Comisión (5% de {col_name}): {comision:.2f}€")
    else:
        print("⚠️  No se encontró presupuesto de Onelvis")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    ver_estructura_presupuestos()
