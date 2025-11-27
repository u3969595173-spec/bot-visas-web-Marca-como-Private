import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def add_perfil_completo_column():
    """Agregar columna perfil_completo a la tabla estudiantes"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    try:
        # Verificar si la columna ya existe
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='estudiantes' AND column_name='perfil_completo'
        """)
        
        if cursor.fetchone():
            print("✅ La columna 'perfil_completo' ya existe")
            return
        
        # Agregar columna
        cursor.execute("""
            ALTER TABLE estudiantes 
            ADD COLUMN perfil_completo BOOLEAN DEFAULT FALSE
        """)
        
        # Marcar como completo los perfiles que ya tienen datos
        cursor.execute("""
            UPDATE estudiantes 
            SET perfil_completo = TRUE 
            WHERE pasaporte IS NOT NULL 
            AND fecha_nacimiento IS NOT NULL 
            AND carrera_deseada IS NOT NULL
        """)
        
        conn.commit()
        print("✅ Columna 'perfil_completo' agregada exitosamente")
        print("✅ Perfiles existentes actualizados según sus datos")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    add_perfil_completo_column()
