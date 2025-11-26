"""
Script para agregar columna codigo_acceso a la tabla estudiantes
y generar códigos únicos para estudiantes existentes
"""
import os
import string
import secrets
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def generar_codigo_acceso(longitud=8):
    """Genera un código alfanumérico aleatorio"""
    caracteres = string.ascii_uppercase + string.digits
    # Evitar caracteres confusos como O/0, I/1
    caracteres = caracteres.replace('O', '').replace('I', '').replace('0', '').replace('1', '')
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def main():
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("[ERROR] No se encontró DATABASE_URL en .env")
        return
    
    print(f"[INFO] Conectando a la base de datos...")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        # 1. Agregar columna codigo_acceso si no existe
        print("[INFO] Agregando columna codigo_acceso...")
        try:
            conn.execute(text("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS codigo_acceso VARCHAR(20) UNIQUE
            """))
            conn.commit()
            print("[OK] Columna codigo_acceso agregada")
        except Exception as e:
            print(f"[WARN] {e}")
        
        # 2. Generar códigos para estudiantes existentes que no tienen
        print("[INFO] Generando códigos para estudiantes existentes...")
        result = conn.execute(text("""
            SELECT id FROM estudiantes WHERE codigo_acceso IS NULL
        """))
        estudiantes_sin_codigo = result.fetchall()
        
        for row in estudiantes_sin_codigo:
            estudiante_id = row[0]
            codigo = generar_codigo_acceso()
            
            # Verificar que el código sea único
            while True:
                check = conn.execute(text("""
                    SELECT id FROM estudiantes WHERE codigo_acceso = :codigo
                """), {"codigo": codigo}).fetchone()
                
                if not check:
                    break
                codigo = generar_codigo_acceso()
            
            conn.execute(text("""
                UPDATE estudiantes SET codigo_acceso = :codigo WHERE id = :id
            """), {"codigo": codigo, "id": estudiante_id})
            print(f"[OK] Estudiante ID {estudiante_id} → Código: {codigo}")
        
        conn.commit()
        print(f"\n[OK] {len(estudiantes_sin_codigo)} códigos generados exitosamente")
        
        # 3. Mostrar todos los códigos
        print("\n[INFO] Códigos de acceso actuales:")
        result = conn.execute(text("""
            SELECT id, nombre, email, codigo_acceso 
            FROM estudiantes 
            ORDER BY id
        """))
        
        for row in result.fetchall():
            print(f"  ID: {row[0]} | Nombre: {row[1]} | Email: {row[2]} | Código: {row[3]}")

if __name__ == "__main__":
    main()
