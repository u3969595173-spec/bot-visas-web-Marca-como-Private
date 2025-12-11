import psycopg2
from config import DATABASE_URL

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

print("=== AGREGANDO COLUMNAS PARA TRACKING DE RETIROS ===\n")

try:
    # Agregar credito_retirado a estudiantes
    print("1. Agregando credito_retirado a estudiantes...")
    cur.execute("""
        ALTER TABLE estudiantes 
        ADD COLUMN IF NOT EXISTS credito_retirado DECIMAL(10, 2) DEFAULT 0.00
    """)
    print("   ✅ Columna credito_retirado agregada a estudiantes")
    
    # Agregar credito_retirado a agentes
    print("2. Agregando credito_retirado a agentes...")
    cur.execute("""
        ALTER TABLE agentes 
        ADD COLUMN IF NOT EXISTS credito_retirado DECIMAL(10, 2) DEFAULT 0.00
    """)
    print("   ✅ Columna credito_retirado agregada a agentes")
    
    conn.commit()
    print("\n✅ MIGRACIÓN COMPLETADA")
    print("\nAhora cuando se apruebe un retiro:")
    print("- Se descuenta de credito_disponible")
    print("- Se suma a credito_retirado (historial)")
    
except Exception as e:
    conn.rollback()
    print(f"\n❌ Error: {e}")
finally:
    cur.close()
    conn.close()
