import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cur = conn.cursor()

# Verificar si existe la tabla
cur.execute("""
    SELECT table_name FROM information_schema.tables 
    WHERE table_name = 'notificaciones'
""")
tabla = cur.fetchone()
print(f"Tabla notificaciones existe: {tabla is not None}")

# Verificar notificaciones del estudiante 1
cur.execute("""
    SELECT id, tipo, titulo, mensaje, leida, created_at 
    FROM notificaciones 
    WHERE estudiante_id = 1
    ORDER BY created_at DESC
""")
notifs = cur.fetchall()

print(f"\n📊 Total notificaciones para estudiante 1: {len(notifs)}")

if notifs:
    for n in notifs:
        print(f"\nID: {n[0]}")
        print(f"Tipo: {n[1]}")
        print(f"Título: {n[2]}")
        print(f"Mensaje: {n[3]}")
        print(f"Leída: {n[4]}")
        print(f"Fecha: {n[5]}")
else:
    print("\n❌ No hay notificaciones en la base de datos")
    print("Insertando una ahora...")
    
    cur.execute("""
        INSERT INTO notificaciones (estudiante_id, tipo, titulo, mensaje, icono, prioridad, leida)
        VALUES (1, 'sistema', '🎉 Notificación de Prueba', 'Esta es una prueba del sistema', '🎉', 'alta', false)
        RETURNING id
    """)
    new_id = cur.fetchone()[0]
    conn.commit()
    print(f"✅ Notificación creada con ID: {new_id}")

cur.close()
conn.close()
