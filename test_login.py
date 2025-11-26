import psycopg2
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

email = 'leandroeloytamayoreyes@gmail.com'
password = 'Eloy1940'

# Buscar usuario
cur.execute('SELECT email, password, nombre, rol FROM usuarios WHERE email = %s', (email,))
result = cur.fetchone()

if result:
    print(f"✅ Usuario encontrado: {result[0]}")
    print(f"   Nombre: {result[2]}")
    print(f"   Rol: {result[3]}")
    
    # Verificar contraseña
    stored_hash = result[1]
    print(f"\n🔑 Hash almacenado: {stored_hash[:50]}...")
    
    try:
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            print("✅ Contraseña CORRECTA")
        else:
            print("❌ Contraseña INCORRECTA")
    except Exception as e:
        print(f"❌ Error verificando contraseña: {e}")
else:
    print("❌ Usuario NO encontrado")

cur.close()
conn.close()
