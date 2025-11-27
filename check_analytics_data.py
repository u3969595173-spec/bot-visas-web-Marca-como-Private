import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cursor = conn.cursor()

print("=" * 60)
print("VERIFICACIÓN DE DATOS PARA ANALYTICS")
print("=" * 60)

# Total estudiantes
cursor.execute("SELECT COUNT(*) FROM estudiantes")
total = cursor.fetchone()[0]
print(f"\n📊 Total estudiantes: {total}")

# Por estado
cursor.execute("""
    SELECT estado, COUNT(*) 
    FROM estudiantes 
    WHERE estado IS NOT NULL
    GROUP BY estado
    ORDER BY COUNT(*) DESC
""")
print("\n📋 Estudiantes por estado:")
estados = cursor.fetchall()
if estados:
    for row in estados:
        print(f"  - {row[0]}: {row[1]}")
else:
    print("  ⚠️  Ningún estudiante tiene estado definido")

# Sin estado
cursor.execute("SELECT COUNT(*) FROM estudiantes WHERE estado IS NULL")
sin_estado = cursor.fetchone()[0]
if sin_estado > 0:
    print(f"  ⚠️  {sin_estado} estudiantes SIN estado")

# Por nacionalidad
cursor.execute("""
    SELECT nacionalidad, COUNT(*) 
    FROM estudiantes 
    WHERE nacionalidad IS NOT NULL
    GROUP BY nacionalidad
    ORDER BY COUNT(*) DESC
    LIMIT 5
""")
print("\n🌍 Top 5 nacionalidades:")
naciones = cursor.fetchall()
if naciones:
    for row in naciones:
        print(f"  - {row[0]}: {row[1]}")
else:
    print("  ⚠️  Ningún estudiante tiene nacionalidad")

# Registros último mes
cursor.execute("""
    SELECT COUNT(*) 
    FROM estudiantes 
    WHERE created_at >= NOW() - INTERVAL '30 days'
""")
ultimo_mes = cursor.fetchone()[0]
print(f"\n📅 Registros últimos 30 días: {ultimo_mes}")

# Mensajes chat
cursor.execute("SELECT COUNT(*) FROM mensajes_chat")
mensajes = cursor.fetchone()[0]
print(f"\n💬 Total mensajes chat: {mensajes}")

# Documentos
cursor.execute("SELECT COUNT(*) FROM documentos")
documentos = cursor.fetchone()[0]
print(f"\n📄 Total documentos: {documentos}")

# Universidades visitas
cursor.execute("""
    SELECT nombre, visitas 
    FROM universidades_espana 
    WHERE visitas > 0
    ORDER BY visitas DESC
    LIMIT 5
""")
unis = cursor.fetchall()
print(f"\n🏫 Top universidades visitadas:")
if unis:
    for row in unis:
        print(f"  - {row[0]}: {row[1]} visitas")
else:
    print("  ⚠️  Ninguna universidad tiene visitas registradas")

# Verificar columna visitas existe
cursor.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'universidades_espana' AND column_name = 'visitas'
""")
if not cursor.fetchone():
    print("  ❌ La columna 'visitas' NO EXISTE en universidades_espana")

cursor.close()
conn.close()

print("\n" + "=" * 60)
