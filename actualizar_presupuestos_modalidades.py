#!/usr/bin/env python3
"""
Script para actualizar tabla presupuestos con nuevas modalidades de pago
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
        print("[INFO] Actualizando tabla presupuestos...")
        
        # Agregar nuevas columnas para modalidades de pago
        nuevas_columnas = [
            ("servicios_solicitados", "JSONB"),  # Lista de servicios que pidió el estudiante
            ("precio_al_empezar", "NUMERIC(10,2)"),  # Modalidad: pago al empezar
            ("precio_con_visa", "NUMERIC(10,2)"),    # Modalidad: pago al obtener visa
            ("precio_financiado", "NUMERIC(10,2)"),  # Modalidad: financiado 12 meses
            ("modalidad_seleccionada", "VARCHAR(50)"), # Qué modalidad eligió el estudiante
            ("comentarios_estudiante", "TEXT"),      # Comentarios del estudiante
            ("fecha_aceptacion", "TIMESTAMP"),       # Cuándo aceptó
            ("fecha_pago", "TIMESTAMP"),            # Cuándo pagó (para control del admin)
            ("pagado", "BOOLEAN DEFAULT FALSE")     # Si ya pagó (control del admin)
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
        print("[OK] Tabla presupuestos actualizada exitosamente")
        
        print("\n[INFO] Estructura actualizada:")
        print("💰 Modalidades de pago disponibles:")
        print("  - precio_al_empezar: Pago completo al iniciar")
        print("  - precio_con_visa: Pago al obtener visa")
        print("  - precio_financiado: Pago en 12 cuotas")
        print("\n🔄 Flujo del proceso:")
        print("  1. Estudiante solicita servicios → servicios_solicitados")
        print("  2. Admin define modalidades → precio_al_empezar, precio_con_visa, precio_financiado")
        print("  3. Estudiante acepta → modalidad_seleccionada")
        print("  4. Admin controla pago → pagado = true")

if __name__ == "__main__":
    main()