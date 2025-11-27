"""
Script para verificar que el endpoint de universidades funciona en Render
"""
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

print("=" * 70)
print("DIAGNÓSTICO: Verificando universidades en Render")
print("=" * 70)

try:
    # Conectar a Render
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    # Verificar que existe la tabla
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'contactos_universidades'
        );
    """)
    existe = cursor.fetchone()[0]
    
    if not existe:
        print("❌ LA TABLA NO EXISTE en Render")
        print("Solución: Ejecuta nuevamente: python cargar_universidades_render.py")
    else:
        print("✅ La tabla existe")
        
        # Contar universidades
        cursor.execute("SELECT COUNT(*) FROM contactos_universidades")
        total = cursor.fetchone()[0]
        
        print(f"✅ Universidades en base de datos: {total}")
        
        if total == 0:
            print("⚠️ La tabla existe pero está VACÍA")
            print("Solución: Ejecuta: python cargar_universidades_render.py")
        else:
            # Mostrar las primeras 5
            cursor.execute("""
                SELECT id, universidad, email, estado 
                FROM contactos_universidades 
                ORDER BY id 
                LIMIT 5
            """)
            
            print("\n📋 Primeras 5 universidades:")
            for row in cursor.fetchall():
                print(f"   {row[0]}. {row[1]} - {row[2]} ({row[3]})")
            
            print(f"\n✅ TODO ESTÁ CORRECTO")
            print(f"   El problema debe ser en el frontend o token de autenticación")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("=" * 70)
