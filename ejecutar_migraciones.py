"""
Script de migración automática para producción
Ejecuta todas las migraciones pendientes de forma segura
"""
import psycopg2
import os
import sys

# Intentar conectar con DATABASE_URL de entorno
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    try:
        from config import DATABASE_URL
    except:
        print("❌ ERROR: No se encontró DATABASE_URL")
        sys.exit(1)

print("=" * 60)
print("🚀 INICIANDO MIGRACIONES AUTOMÁTICAS")
print("=" * 60)

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # MIGRACIÓN 1: Agregar credito_retirado
    print("\n📦 Migración 1: Agregar columna credito_retirado...")
    try:
        cur.execute("""
            ALTER TABLE estudiantes 
            ADD COLUMN IF NOT EXISTS credito_retirado DECIMAL(10, 2) DEFAULT 0.00
        """)
        print("   ✅ credito_retirado agregado a estudiantes")
    except Exception as e:
        print(f"   ⚠️  estudiantes: {e}")
    
    try:
        cur.execute("""
            ALTER TABLE agentes 
            ADD COLUMN IF NOT EXISTS credito_retirado DECIMAL(10, 2) DEFAULT 0.00
        """)
        print("   ✅ credito_retirado agregado a agentes")
    except Exception as e:
        print(f"   ⚠️  agentes: {e}")
    
    conn.commit()
    
    # VERIFICACIÓN
    print("\n🔍 VERIFICANDO ESTADO ACTUAL...")
    
    # Verificar columnas
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'estudiantes' 
        AND column_name = 'credito_retirado'
    """)
    if cur.fetchone():
        print("   ✅ estudiantes.credito_retirado existe")
    else:
        print("   ❌ estudiantes.credito_retirado NO existe")
    
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'agentes' 
        AND column_name = 'credito_retirado'
    """)
    if cur.fetchone():
        print("   ✅ agentes.credito_retirado existe")
    else:
        print("   ❌ agentes.credito_retirado NO existe")
    
    # Verificar presupuestos
    cur.execute("""
        SELECT COUNT(*), COALESCE(SUM(precio_ofertado), 0)
        FROM presupuestos
        WHERE LOWER(estado) = 'aceptado'
    """)
    result = cur.fetchone()
    print(f"\n📊 CONTABILIDAD:")
    print(f"   Presupuestos aceptados: {result[0]}")
    print(f"   Valor total: {result[1]}€")
    
    # Verificar referidos
    cur.execute("""
        SELECT COUNT(DISTINCT e.id)
        FROM estudiantes e
        INNER JOIN estudiantes r ON r.referido_por_id = e.id
    """)
    est_referidos = cur.fetchone()[0]
    
    cur.execute("""
        SELECT COUNT(DISTINCT a.id)
        FROM agentes a
        INNER JOIN estudiantes e ON e.referido_por_agente_id = a.id
    """)
    ag_referidos = cur.fetchone()[0]
    
    print(f"\n👥 REFERIDOS:")
    print(f"   Estudiantes con referidos: {est_referidos}")
    print(f"   Agentes con referidos: {ag_referidos}")
    
    cur.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ MIGRACIONES COMPLETADAS EXITOSAMENTE")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    sys.exit(1)
