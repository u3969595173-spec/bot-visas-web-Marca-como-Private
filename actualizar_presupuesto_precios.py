"""
Script para actualizar precios de un presupuesto existente
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def actualizar_precios_presupuesto():
    """Actualiza los precios del presupuesto ID 1 del estudiante 4"""
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ Error: No se encontró DATABASE_URL en .env")
        return
    
    # Fix para Render (postgresql:// -> postgresql+psycopg2://)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    elif database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
    
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            # Primero ver el estado actual
            result = conn.execute(text("""
                SELECT id, estudiante_id, estado, 
                       precio_al_empezar, precio_con_visa, precio_financiado,
                       modalidad_seleccionada
                FROM presupuestos 
                WHERE estudiante_id = 4 AND id = 1
            """))
            
            presupuesto = result.fetchone()
            if presupuesto:
                print(f"\n📋 Presupuesto actual:")
                print(f"   ID: {presupuesto[0]}")
                print(f"   Estudiante: {presupuesto[1]}")
                print(f"   Estado: {presupuesto[2]}")
                print(f"   Precio al empezar: {presupuesto[3]}")
                print(f"   Precio con visa: {presupuesto[4]}")
                print(f"   Precio financiado: {presupuesto[5]}")
                print(f"   Modalidad seleccionada: {presupuesto[6]}")
                
                # Actualizar con precios de ejemplo
                print("\n🔄 Actualizando precios...")
                conn.execute(text("""
                    UPDATE presupuestos
                    SET precio_al_empezar = 1200.00,
                        precio_con_visa = 1500.00,
                        precio_financiado = 1800.00,
                        estado = 'ofertado',
                        mensaje_admin = 'Oferta personalizada con 3 modalidades de pago. Elige la que mejor se ajuste a tu situación.',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = 1 AND estudiante_id = 4
                """))
                conn.commit()
                
                print("✅ Precios actualizados correctamente!")
                print("\n💰 Nuevos precios:")
                print("   🚀 Pago al empezar: €1,200.00")
                print("   🎯 Pago con visa: €1,500.00")
                print("   📅 Pago financiado: €1,800.00 (€150/mes)")
                print("\n📝 Estado cambiado a 'ofertado' para que el estudiante pueda aceptar")
                
            else:
                print("❌ No se encontró el presupuesto con ID 1 para el estudiante 4")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("🔧 Actualizando precios del presupuesto...\n")
    actualizar_precios_presupuesto()
