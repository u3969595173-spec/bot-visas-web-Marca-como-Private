import psycopg2

DATABASE_URL = "postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create usuarios table
cursor.execute("""
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    telefono VARCHAR(50),
    rol VARCHAR(50) DEFAULT 'estudiante',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);
""")

# Create estudiantes table
cursor.execute("""
CREATE TABLE estudiantes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    fecha_cita TIMESTAMP,
    tipo_visa VARCHAR(100),
    estado VARCHAR(50) DEFAULT 'pendiente',
    documentos_estado VARCHAR(50) DEFAULT 'pendiente',
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Insert admin user
cursor.execute("""
INSERT INTO usuarios (nombre, email, password, telefono, rol)
VALUES ('LEANDRO ELOY TAMAYO REYES', 'leandroeloytamayoreyes@gmail.com', '$2b$12$/G2D1U6JKxWD3tY8.xZiwukJfb/FdFYN8gyLQpqW0VfdK12EFMePS', NULL, 'admin');
""")

conn.commit()
cursor.close()
conn.close()

print("✅ Tablas creadas y usuario admin insertado correctamente")
