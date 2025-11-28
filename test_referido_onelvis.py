"""
Script de prueba: Hacer que Onelvis sea referido de Leandro
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def main():
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("[ERROR] No se encontró DATABASE_URL en .env")
        return
    
    print(f"[INFO] Conectando a la base de datos...")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        # 1. Obtener datos de Leandro
        leandro = conn.execute(text("""
            SELECT id, nombre, codigo_referido FROM estudiantes 
            WHERE nombre LIKE '%leandro%'
        """)).fetchone()
        
        if not leandro:
            print("[ERROR] No se encontró a Leandro")
            return
        
        print(f"\n[INFO] Leandro encontrado:")
        print(f"  ID: {leandro[0]}")
        print(f"  Nombre: {leandro[1]}")
        print(f"  Código de Referido: {leandro[2]}")
        
        # 2. Obtener datos de Onelvis
        onelvis = conn.execute(text("""
            SELECT id, nombre, referido_por_id FROM estudiantes 
            WHERE nombre LIKE '%onelvis%'
        """)).fetchone()
        
        if not onelvis:
            print("[ERROR] No se encontró a Onelvis")
            return
        
        print(f"\n[INFO] Onelvis encontrado:")
        print(f"  ID: {onelvis[0]}")
        print(f"  Nombre: {onelvis[1]}")
        print(f"  Referido por: {onelvis[2]}")
        
        # 3. Actualizar Onelvis para que sea referido de Leandro
        conn.execute(text("""
            UPDATE estudiantes 
            SET referido_por_id = :leandro_id
            WHERE id = :onelvis_id
        """), {"leandro_id": leandro[0], "onelvis_id": onelvis[0]})
        conn.commit()
        
        print(f"\n✅ Onelvis ahora es referido de Leandro")
        
        # 4. Verificar el cambio
        verificacion = conn.execute(text("""
            SELECT e.nombre, e.id, r.nombre as referidor
            FROM estudiantes e
            LEFT JOIN estudiantes r ON e.referido_por_id = r.id
            WHERE e.id = :onelvis_id
        """), {"onelvis_id": onelvis[0]}).fetchone()
        
        print(f"\n[VERIFICACIÓN]")
        print(f"  {verificacion[0]} (ID: {verificacion[1]}) fue referido por: {verificacion[2]}")
        
        # 5. Mostrar estadísticas de Leandro
        stats = conn.execute(text("""
            SELECT 
                COUNT(*) as total_referidos,
                COALESCE(SUM(p.precio_ofertado * 0.10), 0) as comision_total
            FROM estudiantes e
            LEFT JOIN presupuestos p ON p.estudiante_id = e.id AND p.estado = 'aceptado'
            WHERE e.referido_por_id = :leandro_id
        """), {"leandro_id": leandro[0]}).fetchone()
        
        print(f"\n[ESTADÍSTICAS DE LEANDRO]")
        print(f"  Total de Referidos: {stats[0]}")
        print(f"  Comisión Total Ganada: {float(stats[1])}€")
        
        print(f"\n[INFO] Para probar la comisión:")
        print(f"  1. Onelvis debe solicitar un presupuesto")
        print(f"  2. Admin hace contraoferta")
        print(f"  3. Onelvis acepta el presupuesto")
        print(f"  4. Leandro recibirá automáticamente 10% del precio en su crédito")

if __name__ == "__main__":
    main()
