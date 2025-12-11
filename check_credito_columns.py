import psycopg2
from config import DATABASE_URL

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

print("=== COLUMNAS DE CRÉDITO EN ESTUDIANTES ===")
cur.execute("""
    SELECT column_name, data_type, column_default
    FROM information_schema.columns 
    WHERE table_name = 'estudiantes' 
    AND column_name LIKE '%credito%'
    ORDER BY ordinal_position
""")

rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"- {row[0]}: {row[1]} (default: {row[2]})")
else:
    print("No hay columnas de crédito en estudiantes")

print("\n=== COLUMNAS DE CRÉDITO EN AGENTES ===")
cur.execute("""
    SELECT column_name, data_type, column_default
    FROM information_schema.columns 
    WHERE table_name = 'agentes' 
    AND column_name LIKE '%credito%'
    ORDER BY ordinal_position
""")

rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"- {row[0]}: {row[1]} (default: {row[2]})")
else:
    print("No hay columnas de crédito en agentes")

cur.close()
conn.close()
