"""
Script para corregir el estado del presupuesto de aceptado a pendiente
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# Conectar a la base de datos
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("❌ No se encontró DATABASE_URL en .env")
    exit(1)

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Verificar presupuestos actuales
        result = conn.execute(text("""
            SELECT id, estudiante_id, estado, precio_al_empezar, precio_con_visa, precio_financiado
            FROM presupuestos
            WHERE estado = 'aceptado'
        """))
        
        presupuestos = result.fetchall()
        print(f"\n📊 Presupuestos encontrados con estado 'aceptado': {len(presupuestos)}\n")
        
        for p in presupuestos:
            print(f"ID: {p[0]}, Estudiante: {p[1]}, Estado: {p[2]}")
            print(f"  - Precio inicial: €{p[3] or 0}")
            print(f"  - Precio con visa: €{p[4] or 0}")
            print(f"  - Precio financiado: €{p[5] or 0}")
            print()
        
        # Actualizar a pendiente los que NO tienen precios definidos
        result = conn.execute(text("""
            UPDATE presupuestos
            SET estado = 'pendiente',
                precio_al_empezar = NULL,
                precio_con_visa = NULL,
                precio_financiado = NULL,
                mensaje_admin = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE estado = 'aceptado'
            AND (precio_al_empezar IS NULL OR precio_con_visa IS NULL OR precio_financiado IS NULL)
            RETURNING id
        """))
        
        actualizados = result.fetchall()
        conn.commit()
        
        if actualizados:
            print(f"✅ Se actualizaron {len(actualizados)} presupuestos a estado 'pendiente'")
            for row in actualizados:
                print(f"   - Presupuesto ID: {row[0]}")
        else:
            print("ℹ️ No se encontraron presupuestos para actualizar (todos tienen precios definidos)")
            print("\n💡 Si hay presupuestos con estado 'aceptado' y precios definidos,")
            print("   significa que el estudiante YA aceptó la oferta y están correctos.")
        
        print("\n✅ Proceso completado")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
