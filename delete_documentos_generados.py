"""
Script para eliminar todos los documentos generados de la base de datos
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def main():
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("[ERROR] No se encontró DATABASE_URL en .env")
        return
    
    print(f"[INFO] Conectando a la base de datos...")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        # Contar documentos antes de eliminar
        result = conn.execute(text("SELECT COUNT(*) FROM documentos_generados"))
        count_antes = result.fetchone()[0]
        print(f"[INFO] Documentos generados encontrados: {count_antes}")
        
        if count_antes == 0:
            print("[INFO] No hay documentos para eliminar")
            return
        
        # Confirmar
        confirmar = input(f"\n¿Estás seguro de eliminar {count_antes} documentos? (escribe 'SI' para confirmar): ")
        
        if confirmar.upper() != 'SI':
            print("[CANCELADO] No se eliminó ningún documento")
            return
        
        # Eliminar todos los documentos generados
        conn.execute(text("DELETE FROM documentos_generados"))
        conn.commit()
        
        # Verificar eliminación
        result = conn.execute(text("SELECT COUNT(*) FROM documentos_generados"))
        count_despues = result.fetchone()[0]
        
        print(f"\n[OK] {count_antes} documentos eliminados exitosamente")
        print(f"[OK] Documentos restantes: {count_despues}")

if __name__ == "__main__":
    main()
