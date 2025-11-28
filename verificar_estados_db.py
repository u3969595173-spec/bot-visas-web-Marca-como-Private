"""
Script para verificar el estado actual de las aprobaciones en la base de datos
"""

import os
import psycopg2
from urllib.parse import urlparse

def verificar_estados_aprobacion():
    """Verifica qué estados de aprobación tienen los estudiantes"""
    
    try:
        # Conectar a la base de datos
        db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/bot_visas')
        
        if 'postgres://' in db_url:
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(db_url, sslmode='require' if 'localhost' not in db_url else 'disable')
        cursor = conn.cursor()
        
        print("🔍 VERIFICANDO ESTADOS DE APROBACIÓN EN LA BASE DE DATOS")
        print("=" * 70)
        
        # Consultar estados de los estudiantes
        cursor.execute("""
            SELECT id, nombre, email,
                   estado_alojamiento, 
                   estado_patrocinio,
                   estado_seguro_medico,
                   gestion_alojamiento_solicitada,
                   patrocinio_solicitado,
                   gestion_seguro_solicitada
            FROM estudiantes 
            WHERE id <= 5
            ORDER BY id
        """)
        
        estudiantes = cursor.fetchall()
        
        print(f"{'ID':<4} {'Nombre':<20} {'Alojamiento':<12} {'Patrocinio':<12} {'Seguro':<12}")
        print("-" * 70)
        
        for est in estudiantes:
            print(f"{est[0]:<4} {est[1][:18]:<20} {est[3] or 'NULL':<12} {est[4] or 'NULL':<12} {est[5] or 'NULL':<12}")
        
        print("\n📊 SOLICITUDES ACTIVAS:")
        print("-" * 40)
        
        for est in estudiantes:
            print(f"\n👤 {est[1]} (ID: {est[0]}):")
            if est[6]:  # gestion_alojamiento_solicitada
                print(f"   🏠 Alojamiento: {est[3] or 'pendiente'}")
            if est[7]:  # patrocinio_solicitado  
                print(f"   💰 Patrocinio: {est[4] or 'pendiente'}")
            if est[8]:  # gestion_seguro_solicitada
                print(f"   🏥 Seguro: {est[5] or 'pendiente'}")
        
        # Verificar si hay estados diferentes a 'pendiente'
        cursor.execute("""
            SELECT COUNT(*) FROM estudiantes 
            WHERE estado_alojamiento IN ('aprobado', 'rechazado')
               OR estado_patrocinio IN ('aprobado', 'rechazado')  
               OR estado_seguro_medico IN ('aprobado', 'rechazado')
        """)
        
        procesados = cursor.fetchone()[0]
        print(f"\n🎯 Solicitudes procesadas por admin: {procesados}")
        
        if procesados == 0:
            print("\n⚠️  PROBLEMA ENCONTRADO:")
            print("   Ninguna solicitud ha sido aprobada/rechazada por el admin")
            print("   Por eso los estudiantes siguen viendo el formulario normal")
            print("\n💡 SOLUCIÓN:")
            print("   1. Ve al dashboard de admin")
            print("   2. Busca las solicitudes pendientes")
            print("   3. Aprueba o rechaza una para probar")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_estados_aprobacion()