import psycopg2
from config import DATABASE_URL
import random
import string

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

print("=== VERIFICANDO REGISTRO DE LEANDRO ===\n")

# Buscar a Leandro
cur.execute("""
    SELECT id, nombre, email, codigo_referido, credito_disponible, tipo_recompensa
    FROM estudiantes
    WHERE nombre ILIKE '%leandro%' OR email ILIKE '%leandro%'
    ORDER BY id
""")

estudiantes = cur.fetchall()

if not estudiantes:
    print("❌ No se encontró a Leandro")
else:
    for est in estudiantes:
        print(f"ID: {est[0]}")
        print(f"Nombre: {est[1]}")
        print(f"Email: {est[2]}")
        print(f"Código Referido: {est[3] or '❌ NO TIENE'}")
        print(f"Crédito Disponible: {est[4]}€")
        print(f"Tipo Recompensa: {est[5]}")
        
        if not est[3]:
            # Generar código único
            codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            print(f"\n🔧 Generando código para Leandro: {codigo}")
            
            cur.execute("""
                UPDATE estudiantes
                SET codigo_referido = :codigo,
                    tipo_recompensa = 'dinero'
                WHERE id = :id
            """, {"codigo": codigo, "id": est[0]})
            
            conn.commit()
            print("✅ Código asignado correctamente")
        else:
            print("✅ Ya tiene código referido")
        
        print("-" * 50)

cur.close()
conn.close()
