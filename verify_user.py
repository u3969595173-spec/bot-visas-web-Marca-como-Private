import psycopg2
from passlib.hash import bcrypt

DATABASE_URL = "postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Verificar usuario
cursor.execute("SELECT * FROM usuarios WHERE email = 'leandroeloytamayoreyes@gmail.com'")
user = cursor.fetchone()

if user:
    print(f"✅ Usuario encontrado: {user}")
    print(f"\nID: {user[0]}")
    print(f"Nombre: {user[1]}")
    print(f"Email: {user[2]}")
    print(f"Password hash: {user[3]}")
    print(f"Rol: {user[5]}")
    
    # Verificar password
    password = "Eloy1940"
    is_valid = bcrypt.verify(password, user[3])
    print(f"\n¿Password 'Eloy1940' es válido? {is_valid}")
    
    if not is_valid:
        print("\n⚠️ Password incorrecto. Generando nuevo hash...")
        new_hash = bcrypt.hash(password)
        print(f"Nuevo hash: {new_hash}")
        
        cursor.execute("UPDATE usuarios SET password = %s WHERE email = %s", (new_hash, 'leandroeloytamayoreyes@gmail.com'))
        conn.commit()
        print("✅ Password actualizado")
else:
    print("❌ Usuario NO encontrado")

cursor.close()
conn.close()
