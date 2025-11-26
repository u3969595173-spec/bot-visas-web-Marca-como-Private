import psycopg2
import bcrypt

DATABASE_URL = "postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Generar nuevo hash con bcrypt directo
password = "Eloy1940"
new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print(f"Nuevo hash generado: {new_hash}")

# Actualizar usuario
cursor.execute("UPDATE usuarios SET password = %s WHERE email = %s", (new_hash, 'leandroeloytamayoreyes@gmail.com'))
conn.commit()

print("✅ Password actualizado correctamente")

cursor.close()
conn.close()
