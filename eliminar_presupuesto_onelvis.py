"""
Script para eliminar el presupuesto de Onelvis
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Buscar presupuestos de estudiantes con nombre similar a "onelvis"
        result = conn.execute(text("""
            SELECT p.id, e.nombre, p.estado, p.created_at
            FROM presupuestos p
            JOIN estudiantes e ON p.estudiante_id = e.id
            WHERE LOWER(e.nombre) LIKE '%onelvis%'
            ORDER BY p.created_at DESC
        """))
        
        presupuestos = result.fetchall()
        
        if not presupuestos:
            print("❌ No se encontró ningún presupuesto de Onelvis")
        else:
            print(f"\n📋 Presupuestos encontrados de Onelvis:\n")
            for p in presupuestos:
                print(f"ID: {p[0]} | Estudiante: {p[1]} | Estado: {p[2]} | Fecha: {p[3]}")
            
            print("\n🗑️ Eliminando presupuestos...")
            
            for p in presupuestos:
                conn.execute(text("DELETE FROM presupuestos WHERE id = :id"), {"id": p[0]})
                print(f"   ✅ Eliminado presupuesto ID: {p[0]}")
            
            conn.commit()
            print(f"\n✅ Se eliminaron {len(presupuestos)} presupuesto(s) de Onelvis")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
