"""
Script para crear sistema de referidos
- Agrega columnas a estudiantes: codigo_referido, referido_por_id, credito_disponible, tipo_recompensa
- Cada estudiante obtiene 10% del presupuesto aceptado de sus referidos
"""
import os
import string
import secrets
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def generar_codigo_referido(longitud=8):
    """Genera un código alfanumérico único para referidos"""
    caracteres = string.ascii_uppercase + string.digits
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
        # 1. Agregar columnas a estudiantes
        print("[INFO] Agregando columnas de referidos a estudiantes...")
        try:
            conn.execute(text("""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS codigo_referido VARCHAR(20) UNIQUE,
                ADD COLUMN IF NOT EXISTS referido_por_id INTEGER REFERENCES estudiantes(id),
                ADD COLUMN IF NOT EXISTS credito_disponible NUMERIC(10,2) DEFAULT 0.00,
                ADD COLUMN IF NOT EXISTS tipo_recompensa VARCHAR(20) DEFAULT 'dinero'
            """))
            conn.commit()
            print("[OK] Columnas agregadas a estudiantes")
        except Exception as e:
            print(f"[INFO] {e}")
        
        # 2. Generar códigos únicos para estudiantes existentes
        print("\n[INFO] Generando códigos de referido para estudiantes...")
        result = conn.execute(text("""
            SELECT id, nombre FROM estudiantes WHERE codigo_referido IS NULL
        """))
        estudiantes_sin_codigo = result.fetchall()
        
        for row in estudiantes_sin_codigo:
            estudiante_id = row[0]
            nombre = row[1]
            codigo = generar_codigo_referido()
            
            # Verificar que sea único
            while True:
                check = conn.execute(text("""
                    SELECT id FROM estudiantes WHERE codigo_referido = :codigo
                """), {"codigo": codigo}).fetchone()
                
                if not check:
                    break
                codigo = generar_codigo_referido()
            
            conn.execute(text("""
                UPDATE estudiantes 
                SET codigo_referido = :codigo, credito_disponible = 0.00, tipo_recompensa = 'dinero'
                WHERE id = :id
            """), {"codigo": codigo, "id": estudiante_id})
            print(f"[OK] {nombre} → Código: {codigo}")
        
        conn.commit()
        print(f"\n✅ Sistema de referidos creado - {len(estudiantes_sin_codigo)} códigos generados")
        
        # 3. Mostrar resumen
        print("\n[INFO] Resumen de códigos de referido:")
        result = conn.execute(text("""
            SELECT id, nombre, codigo_referido, credito_disponible 
            FROM estudiantes 
            ORDER BY id
        """))
        
        for row in result.fetchall():
            print(f"  {row[1]} | Código: {row[2]} | Crédito: €{row[3]}")

if __name__ == "__main__":
    main()
