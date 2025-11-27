import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = conn.cursor()

# Verificar tabla existe
cursor.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'documentos_generados'
    ORDER BY ordinal_position
""")

print("📋 ESTRUCTURA DE documentos_generados:")
print("=" * 60)
for col in cursor.fetchall():
    print(f"  {col[0]:<30} {col[1]}")

# Contar registros
cursor.execute("SELECT COUNT(*) FROM documentos_generados")
count = cursor.fetchone()[0]
print(f"\n📊 Total de registros: {count}")

if count > 0:
    cursor.execute("SELECT id, estudiante_id, tipo_documento, estado FROM documentos_generados LIMIT 5")
    print("\n🔍 Primeros 5 registros:")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Estudiante: {row[1]}, Tipo: {row[2]}, Estado: {row[3]}")

cursor.close()
conn.close()
