import psycopg2
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Crear tabla usuarios si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password TEXT NOT NULL,
        password_hash TEXT,
        nombre VARCHAR(255),
        rol VARCHAR(50) DEFAULT 'admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Usuario admin
email = "leandroeloytamayoreyes@gmail.com"
password = "Eloy1940"
nombre = "Leandro Eloy"

# Generar hash
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print(f"📧 Email: {email}")
print(f"🔑 Password: {password}")
print(f"🔐 Hash generado: {password_hash[:50]}...")

# Insertar o actualizar
cursor.execute("""
    INSERT INTO usuarios (email, password, nombre, rol)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (email) DO UPDATE 
    SET password = EXCLUDED.password,
        nombre = EXCLUDED.nombre
""", (email, password_hash, nombre, 'admin'))

conn.commit()

print("✅ Usuario admin creado/actualizado")
print(f"✅ Login: {email} / {password}")

cursor.close()
conn.close()
