import psycopg2
from config import DATABASE_URL

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

print("=== VERIFICACIÓN DE CONTABILIDAD ===\n")

# 1. Verificar presupuestos aceptados
print("1. PRESUPUESTOS ACEPTADOS:")
cur.execute("""
    SELECT COUNT(*), COALESCE(SUM(precio_ofertado), 0) as total
    FROM presupuestos
    WHERE LOWER(estado) = 'aceptado'
""")
result = cur.fetchone()
print(f"   Total presupuestos aceptados: {result[0]}")
print(f"   Valor total: {result[1]}€\n")

# Ver todos los estados
print("   Estados en tabla presupuestos:")
cur.execute("SELECT DISTINCT estado, COUNT(*) FROM presupuestos GROUP BY estado")
for row in cur.fetchall():
    print(f"   - {row[0]}: {row[1]} presupuestos")

print("\n2. VERIFICAR COLUMNA credito_retirado:")
# Verificar si existe credito_retirado en estudiantes
cur.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'estudiantes' 
    AND column_name = 'credito_retirado'
""")
if cur.fetchone():
    print("   ✅ Columna credito_retirado existe en estudiantes")
else:
    print("   ❌ Columna credito_retirado NO existe en estudiantes")

# Verificar si existe credito_retirado en agentes
cur.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'agentes' 
    AND column_name = 'credito_retirado'
""")
if cur.fetchone():
    print("   ✅ Columna credito_retirado existe en agentes")
else:
    print("   ❌ Columna credito_retirado NO existe en agentes")

print("\n3. ESTUDIANTES CON REFERIDOS:")
cur.execute("""
    SELECT e.id, e.nombre, COUNT(r.id) as total_referidos
    FROM estudiantes e
    INNER JOIN estudiantes r ON r.referido_por_id = e.id
    GROUP BY e.id, e.nombre
    HAVING COUNT(r.id) > 0
""")
referidores = cur.fetchall()
if referidores:
    print(f"   Total estudiantes con referidos: {len(referidores)}")
    for ref in referidores:
        print(f"   - {ref[1]} (ID: {ref[0]}): {ref[2]} referidos")
else:
    print("   ❌ No hay estudiantes con referidos")

print("\n4. AGENTES CON REFERIDOS:")
cur.execute("""
    SELECT a.id, a.nombre, COUNT(e.id) as total_referidos
    FROM agentes a
    INNER JOIN estudiantes e ON e.referido_por_agente_id = a.id
    GROUP BY a.id, a.nombre
    HAVING COUNT(e.id) > 0
""")
agentes = cur.fetchall()
if agentes:
    print(f"   Total agentes con referidos: {len(agentes)}")
    for ag in agentes:
        print(f"   - {ag[1]} (ID: {ag[0]}): {ag[2]} referidos")
else:
    print("   ❌ No hay agentes con referidos")

cur.close()
conn.close()
