"""
Script para eliminar solo los presupuestos de Onelvis para probar flujo desde cero
"""
import psycopg2
from config import DATABASE_URL

def delete_onelvis_presupuestos():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("🔍 Buscando estudiante Onelvis...")
        
        # Buscar ID de Onelvis
        cursor.execute("""
            SELECT id, nombre, email FROM estudiantes 
            WHERE LOWER(nombre) LIKE '%onelvis%'
        """)
        
        estudiante = cursor.fetchone()
        
        if not estudiante:
            print("❌ No se encontró estudiante con nombre Onelvis")
            cursor.close()
            conn.close()
            return
        
        estudiante_id = estudiante[0]
        print(f"✅ Encontrado: ID={estudiante_id}, Nombre={estudiante[1]}, Email={estudiante[2]}")
        
        # Ver cuántos presupuestos tiene
        cursor.execute("SELECT COUNT(*) FROM presupuestos WHERE estudiante_id = %s", (estudiante_id,))
        count = cursor.fetchone()[0]
        print(f"📊 Presupuestos encontrados: {count}")
        
        # Eliminar SOLO los presupuestos
        print(f"🗑️ Eliminando presupuestos del estudiante {estudiante_id}...")
        cursor.execute("DELETE FROM presupuestos WHERE estudiante_id = %s", (estudiante_id,))
        print(f"✅ {count} presupuesto(s) eliminado(s)")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ ¡PRESUPUESTOS DE ONELVIS ELIMINADOS!")
        print("👉 El estudiante sigue existiendo, solo se borraron sus presupuestos")
        print("👉 Ahora puedes crear un nuevo presupuesto y probar el flujo completo")
        
    except Exception as e:
        print(f"❌ Error eliminando presupuestos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("⚠️  Este script eliminará SOLO los presupuestos de Onelvis (no el estudiante)")
    print("Presiona ENTER para continuar o Ctrl+C para cancelar...")
    input()
    delete_onelvis_presupuestos()
