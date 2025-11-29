"""
Script para eliminar presupuesto de Onelvis
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Buscar presupuestos de Onelvis
        result = conn.execute(text("""
            SELECT p.id, e.nombre, p.estado
            FROM presupuestos p
            JOIN estudiantes e ON p.estudiante_id = e.id
            WHERE LOWER(e.nombre) LIKE '%onelvis%'
        """))
        
        presupuestos = result.fetchall()
        
        if not presupuestos:
            print("❌ No se encontró presupuesto de Onelvis")
        else:
            print(f"📋 Presupuestos encontrados:\n")
            for p in presupuestos:
                print(f"ID: {p[0]} | {p[1]} | Estado: {p[2]}")
            
            print("\n🗑️ Eliminando...")
            for p in presupuestos:
                conn.execute(text("DELETE FROM presupuestos WHERE id = :id"), {"id": p[0]})
                print(f"✅ Eliminado ID: {p[0]}")
            
            conn.commit()
            print(f"\n✅ Total eliminados: {len(presupuestos)}")
        
except Exception as e:
    print(f"❌ Error: {e}")
