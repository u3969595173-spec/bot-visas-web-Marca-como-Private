"""
Verificar qué devuelve el endpoint de referidos para Leandro
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def verificar_endpoint_referidos():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("SIMULANDO ENDPOINT /api/estudiantes/1/referidos")
    print("="*60)
    
    # Simular la query del endpoint corregido
    cursor.execute("""
        SELECT codigo_referido, credito_disponible, tipo_recompensa, 
               COALESCE(credito_retirado, 0) as credito_retirado
        FROM estudiantes WHERE id = 1
    """)
    estudiante = cursor.fetchone()
    
    if estudiante:
        print("\n📊 Datos del endpoint:")
        print(f"   codigo_referido: {estudiante[0]}")
        print(f"   credito_disponible: {float(estudiante[1] or 0):.2f}€")
        print(f"   credito_retirado: {float(estudiante[3] or 0):.2f}€")
        print(f"   tipo_recompensa: {estudiante[2]}")
        
        # Calcular como lo hace el código corregido
        credito_disponible = float(estudiante[1] or 0)
        credito_retirado = float(estudiante[3] or 0)
        total_ganado = credito_disponible + credito_retirado
        
        print(f"\n💰 CÁLCULO:")
        print(f"   total_ganado = {credito_disponible} + {credito_retirado}")
        print(f"   total_ganado = {total_ganado:.2f}€")
        
        # Contar referidos
        cursor.execute("""
            SELECT COUNT(*) FROM estudiantes WHERE referido_por_id = 1
        """)
        total_referidos = cursor.fetchone()[0]
        
        print(f"\n   total_referidos: {total_referidos}")
        
        print("\n" + "="*60)
        print("RESPUESTA DEL ENDPOINT:")
        print("="*60)
        print(f"""
{{
    "codigo_referido": "{estudiante[0]}",
    "credito_disponible": {credito_disponible},
    "credito_retirado": {credito_retirado},
    "tipo_recompensa": "{estudiante[2]}",
    "total_referidos": {total_referidos},
    "total_ganado": {total_ganado}
}}
        """)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    verificar_endpoint_referidos()
