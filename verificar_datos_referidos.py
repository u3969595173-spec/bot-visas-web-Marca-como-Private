"""
Verificar datos del sistema de referidos en producción
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
    
    print(f"[INFO] Conectando a la base de datos de producción...")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        # Verificar datos de referidos
        print("\n[INFO] Datos del sistema de referidos:")
        result = conn.execute(text("""
            SELECT id, nombre, email, codigo_referido, credito_disponible, tipo_recompensa, referido_por_id
            FROM estudiantes
            ORDER BY id
        """))
        
        estudiantes = result.fetchall()
        
        print(f"\n📊 Total estudiantes: {len(estudiantes)}\n")
        
        sin_codigo = 0
        for row in estudiantes:
            tiene_codigo = "✅" if row[3] else "❌"
            print(f"{tiene_codigo} ID: {row[0]} | {row[1]} | Código: {row[3] or 'NULL'} | Crédito: {row[4] or 0}€ | Tipo: {row[5] or 'NULL'} | Referido por: {row[6] or '-'}")
            if not row[3]:
                sin_codigo += 1
        
        if sin_codigo > 0:
            print(f"\n⚠️ {sin_codigo} estudiantes SIN código de referido")
            print("🔧 Ejecuta: python create_referidos_system.py")
        else:
            print(f"\n✅ Todos los estudiantes tienen código de referido")

if __name__ == "__main__":
    main()
