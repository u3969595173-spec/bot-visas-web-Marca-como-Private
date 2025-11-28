"""
Script para resetear presupuesto 1 a estado pendiente
para que el admin pueda enviar una nueva oferta
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Resetear presupuesto ID 1 a pendiente
        conn.execute(text("""
            UPDATE presupuestos
            SET estado = 'pendiente',
                precio_al_empezar = NULL,
                precio_con_visa = NULL,
                precio_financiado = NULL,
                mensaje_admin = NULL,
                modalidad_seleccionada = NULL,
                fecha_aceptacion = NULL,
                fecha_pago = NULL,
                pagado = FALSE,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        """))
        conn.commit()
        
        print("✅ Presupuesto ID 1 reseteado a estado 'pendiente'")
        print("   - Todos los precios eliminados")
        print("   - Mensaje admin eliminado")
        print("   - Fechas reseteadas")
        print("\n💡 Ahora puedes enviar una nueva oferta desde el panel de admin")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
