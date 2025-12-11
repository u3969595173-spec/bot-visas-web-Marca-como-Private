import psycopg2
from config import DATABASE_URL

print("🚀 Ejecutando migraciones en producción...\n")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("1. Agregando credito_retirado a estudiantes...")
    cur.execute("""
        ALTER TABLE estudiantes 
        ADD COLUMN IF NOT EXISTS credito_retirado DECIMAL(10, 2) DEFAULT 0.00
    """)
    print("   ✅ OK\n")
    
    print("2. Agregando credito_retirado a agentes...")
    cur.execute("""
        ALTER TABLE agentes 
        ADD COLUMN IF NOT EXISTS credito_retirado DECIMAL(10, 2) DEFAULT 0.00
    """)
    print("   ✅ OK\n")
    
    conn.commit()
    
    print("3. Verificando...")
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'estudiantes' 
        AND column_name = 'credito_retirado'
    """)
    if cur.fetchone():
        print("   ✅ estudiantes.credito_retirado existe")
    
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'agentes' 
        AND column_name = 'credito_retirado'
    """)
    if cur.fetchone():
        print("   ✅ agentes.credito_retirado existe")
    
    cur.close()
    conn.close()
    
    print("\n✅ ¡MIGRACIÓN COMPLETADA!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
