"""
Script para eliminar documentos generados en la base de datos de producción
USAR SOLO EN EMERGENCIAS - Esto borrará documentos de la BD de producción
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def main():
    # Usar la URL de producción directamente
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("[ERROR] No se encontró DATABASE_URL en .env")
        return
    
    print("⚠️  ADVERTENCIA: Este script eliminará documentos de la BASE DE DATOS DE PRODUCCIÓN")
    print(f"[INFO] Conectando a: {database_url[:50]}...")
    
    confirmar_primero = input("\n¿Estás ABSOLUTAMENTE SEGURO? Escribe 'PRODUCCION' para continuar: ")
    if confirmar_primero != 'PRODUCCION':
        print("[CANCELADO] Operación cancelada por seguridad")
        return
    
    try:
        conn = psycopg2.connect(database_url, sslmode='require')
        cursor = conn.cursor()
        
        # Contar documentos
        cursor.execute("SELECT COUNT(*) FROM documentos_generados")
        count_antes = cursor.fetchone()[0]
        print(f"\n[INFO] Documentos generados encontrados en producción: {count_antes}")
        
        if count_antes == 0:
            print("[INFO] No hay documentos para eliminar")
            cursor.close()
            conn.close()
            return
        
        # Mostrar algunos IDs para referencia
        cursor.execute("SELECT id, tipo_documento, estudiante_id FROM documentos_generados ORDER BY id DESC LIMIT 10")
        print("\n[INFO] Últimos 10 documentos:")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]} | Tipo: {row[1]} | Estudiante: {row[2]}")
        
        # Segunda confirmación
        confirmar_segundo = input(f"\n¿Eliminar {count_antes} documentos? Escribe 'SI ELIMINAR': ")
        if confirmar_segundo != 'SI ELIMINAR':
            print("[CANCELADO] No se eliminó ningún documento")
            cursor.close()
            conn.close()
            return
        
        # Eliminar
        cursor.execute("DELETE FROM documentos_generados")
        conn.commit()
        
        # Verificar
        cursor.execute("SELECT COUNT(*) FROM documentos_generados")
        count_despues = cursor.fetchone()[0]
        
        print(f"\n[OK] ✅ {count_antes} documentos eliminados de producción")
        print(f"[OK] Documentos restantes: {count_despues}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n[ERROR] ❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
