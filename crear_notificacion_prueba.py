import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
cur = conn.cursor()

cur.execute("""
    INSERT INTO notificaciones (estudiante_id, tipo, titulo, mensaje, icono, prioridad)
    VALUES (1, 'sistema', '🎉 Notificación de Prueba', 'Esta es una prueba del sistema de notificaciones en tiempo real', '🎉', 'alta')
""")

conn.commit()
cur.close()
conn.close()

print('✅ Notificación creada exitosamente para estudiante ID 1')
print('🔔 Recarga tu página de estudiante para verla')
