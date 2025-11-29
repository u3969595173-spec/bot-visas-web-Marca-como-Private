"""
Script para agregar columnas de control de pagos individuales por modalidad
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
        print("[INFO] Agregando columnas de pagos individuales...")
        
        # Agregar columnas para tracking de pagos por modalidad
        nuevas_columnas = [
            ("pagado_al_empezar", "BOOLEAN DEFAULT FALSE"),
            ("fecha_pago_al_empezar", "TIMESTAMP"),
            ("pagado_con_visa", "BOOLEAN DEFAULT FALSE"),
            ("fecha_pago_con_visa", "TIMESTAMP"),
            ("pagado_financiado", "BOOLEAN DEFAULT FALSE"),
            ("fecha_pago_financiado", "TIMESTAMP"),
        ]
        
        for nombre_columna, tipo in nuevas_columnas:
            try:
                conn.execute(text(f"""
                    ALTER TABLE presupuestos 
                    ADD COLUMN IF NOT EXISTS {nombre_columna} {tipo}
                """))
                print(f"  ✅ Agregada columna: {nombre_columna}")
            except Exception as e:
                if "already exists" in str(e).lower():
                    print(f"  ℹ️  Ya existe: {nombre_columna}")
                else:
                    print(f"  ❌ Error con {nombre_columna}: {e}")
        
        conn.commit()
        print("[OK] Columnas de pagos individuales agregadas exitosamente")
        
        print("\n[INFO] Nueva estructura de pagos:")
        print("💰 Control individual de pagos por modalidad:")
        print("  - pagado_al_empezar: Si se pagó la modalidad 'Pago Inicial'")
        print("  - pagado_con_visa: Si se pagó la modalidad 'Pago con Visa'")
        print("  - pagado_financiado: Si se pagó la modalidad 'Financiado'")
        print("\n📅 Fechas de pago por cada modalidad registradas")
        print("\n🔄 El campo 'pagado' general se actualiza automáticamente cuando TODAS las modalidades están pagadas")

if __name__ == "__main__":
    main()
