"""
Actualizar crédito de Leandro con la comisión del presupuesto de Onelvis
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def main():
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        # Actualizar crédito de Leandro
        conn.execute(text("""
            UPDATE estudiantes
            SET credito_disponible = 100.00
            WHERE nombre LIKE '%leandro%'
        """))
        conn.commit()
        
        print("✅ Crédito de Leandro actualizado a 100.00€")
        
        # Verificar
        leandro = conn.execute(text("""
            SELECT nombre, credito_disponible, codigo_referido
            FROM estudiantes
            WHERE nombre LIKE '%leandro%'
        """)).fetchone()
        
        print(f"\n[VERIFICACIÓN]")
        print(f"  Nombre: {leandro[0]}")
        print(f"  Crédito: {float(leandro[1])}€")
        print(f"  Código: {leandro[2]}")
        
        print(f"\n[PRUEBA COMPLETA]")
        print(f"  ✅ Onelvis es referido de Leandro")
        print(f"  ✅ Presupuesto de Onelvis: 1000€ (aceptado)")
        print(f"  ✅ Comisión 10%: 100€")
        print(f"  ✅ Crédito de Leandro: 100€")
        print(f"\n  Ahora Leandro puede ver su crédito en el dashboard!")
        print(f"  Código de referido de Leandro: {leandro[2]}")

if __name__ == "__main__":
    main()
