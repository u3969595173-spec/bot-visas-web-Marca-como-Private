"""
Verificar crédito actual de Leandro
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def main():
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        # Verificar crédito de Leandro
        leandro = conn.execute(text("""
            SELECT 
                id, 
                nombre, 
                codigo_referido,
                credito_disponible,
                tipo_recompensa
            FROM estudiantes 
            WHERE nombre LIKE '%leandro%'
        """)).fetchone()
        
        print(f"[LEANDRO - ESTADO ACTUAL]")
        print(f"  ID: {leandro[0]}")
        print(f"  Nombre: {leandro[1]}")
        print(f"  Código: {leandro[2]}")
        print(f"  Crédito Disponible: {float(leandro[3])}€")
        print(f"  Tipo Recompensa: {leandro[4]}")
        
        # Ver referidos de Leandro
        referidos = conn.execute(text("""
            SELECT nombre, email, created_at
            FROM estudiantes
            WHERE referido_por_id = :id
        """), {"id": leandro[0]}).fetchall()
        
        print(f"\n[REFERIDOS DE LEANDRO]")
        for ref in referidos:
            print(f"  - {ref[0]} ({ref[1]})")
        
        # Ver presupuestos aceptados de los referidos
        presupuestos = conn.execute(text("""
            SELECT 
                e.nombre,
                p.precio_ofertado,
                p.estado,
                (p.precio_ofertado * 0.10) as comision
            FROM presupuestos p
            JOIN estudiantes e ON p.estudiante_id = e.id
            WHERE e.referido_por_id = :id
        """), {"id": leandro[0]}).fetchall()
        
        print(f"\n[PRESUPUESTOS DE REFERIDOS]")
        if presupuestos:
            for p in presupuestos:
                print(f"  - {p[0]}: {float(p[1])}€ (Estado: {p[2]}) → Comisión: {float(p[3])}€")
        else:
            print(f"  No hay presupuestos aún")

if __name__ == "__main__":
    main()
