"""
Script para eliminar estudiantes de prueba
"""
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("[ERROR] DATABASE_URL no encontrada en .env")
    exit(1)

print("[INFO] Conectando a la base de datos...")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Mostrar estudiantes actuales
    cursor.execute("SELECT id, nombre, email FROM estudiantes ORDER BY id;")
    estudiantes = cursor.fetchall()
    
    print(f"\n[INFO] Estudiantes actuales en la base de datos:")
    for e in estudiantes:
        print(f"  ID: {e[0]} - Nombre: {e[1]} - Email: {e[2]}")
    
    if not estudiantes:
        print("\n[INFO] No hay estudiantes para eliminar")
        cursor.close()
        conn.close()
        exit(0)
    
    # Confirmar eliminación
    print(f"\n[WARN] Se eliminarán {len(estudiantes)} estudiante(s)")
    
    # Eliminar todos los estudiantes
    cursor.execute("DELETE FROM estudiantes;")
    deleted = cursor.rowcount
    
    # Reiniciar secuencia del ID
    cursor.execute("ALTER SEQUENCE estudiantes_id_seq RESTART WITH 1;")
    
    conn.commit()
    
    print(f"[OK] {deleted} estudiante(s) eliminado(s) exitosamente")
    print("[OK] Secuencia de IDs reiniciada")
    
    cursor.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"[ERROR] Error de base de datos: {e}")
    exit(1)
except Exception as e:
    print(f"[ERROR] Error inesperado: {e}")
    exit(1)
