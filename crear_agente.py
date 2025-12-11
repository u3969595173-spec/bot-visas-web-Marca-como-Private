"""
Script para crear agentes manualmente
Solo el admin puede crear agentes
"""

import os
import psycopg2
import bcrypt
import secrets
import string
from dotenv import load_dotenv

load_dotenv()

def generar_codigo_referido():
    """Genera código único de 8 caracteres"""
    caracteres = string.ascii_uppercase + string.digits
    caracteres = caracteres.replace('O', '').replace('I', '').replace('0', '').replace('1', '')
    return ''.join(secrets.choice(caracteres) for _ in range(8))

def crear_agente():
    """Crear nuevo agente interactivamente"""
    
    print("\n" + "="*50)
    print("🎯 CREAR NUEVO AGENTE")
    print("="*50 + "\n")
    
    # Solicitar datos
    nombre = input("Nombre completo: ").strip()
    email = input("Email: ").strip().lower()
    telefono = input("Teléfono (opcional): ").strip()
    password = input("Contraseña: ").strip()
    
    if not nombre or not email or not password:
        print("❌ Error: Nombre, email y contraseña son obligatorios")
        return
    
    # Conectar a BD
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    try:
        # Verificar si email ya existe
        cursor.execute("SELECT id FROM agentes WHERE email = %s", (email,))
        if cursor.fetchone():
            print(f"❌ Error: El email {email} ya está registrado")
            return
        
        # Generar código único
        while True:
            codigo = generar_codigo_referido()
            cursor.execute("SELECT id FROM agentes WHERE codigo_referido = %s", (codigo,))
            if not cursor.fetchone():
                break
        
        # Hash de contraseña
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Insertar agente
        cursor.execute("""
            INSERT INTO agentes (nombre, email, password, telefono, codigo_referido, activo)
            VALUES (%s, %s, %s, %s, %s, TRUE)
            RETURNING id, codigo_referido
        """, (nombre, email, password_hash, telefono or None, codigo))
        
        result = cursor.fetchone()
        conn.commit()
        
        print("\n" + "="*50)
        print("✅ AGENTE CREADO EXITOSAMENTE")
        print("="*50)
        print(f"📝 ID: {result[0]}")
        print(f"👤 Nombre: {nombre}")
        print(f"📧 Email: {email}")
        print(f"📱 Teléfono: {telefono or 'No especificado'}")
        print(f"🔗 Código Referido: {result[1]}")
        print(f"🔑 Contraseña: {password}")
        print(f"\n🌐 Login: https://www.fortunariocash.com/agente/login")
        print(f"🔗 Link Referido: https://www.fortunariocash.com/registro?ref={result[1]}")
        print("="*50 + "\n")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error creando agente: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_agentes():
    """Listar todos los agentes"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, nombre, email, telefono, codigo_referido, 
                   total_referidos, comision_total, activo, created_at
            FROM agentes
            ORDER BY created_at DESC
        """)
        
        agentes = cursor.fetchall()
        
        if not agentes:
            print("\n📭 No hay agentes registrados\n")
            return
        
        print("\n" + "="*80)
        print("👥 LISTA DE AGENTES")
        print("="*80)
        
        for a in agentes:
            estado = "✅ ACTIVO" if a[7] else "❌ INACTIVO"
            print(f"\nID: {a[0]} | {estado}")
            print(f"Nombre: {a[1]}")
            print(f"Email: {a[2]}")
            print(f"Teléfono: {a[3] or 'N/A'}")
            print(f"Código: {a[4]}")
            print(f"Referidos: {a[5]} | Comisión: {float(a[6]):.2f}€")
            print(f"Creado: {a[8].strftime('%d/%m/%Y')}")
            print("-" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

def menu():
    """Menú principal"""
    while True:
        print("\n" + "="*50)
        print("🎯 GESTIÓN DE AGENTES")
        print("="*50)
        print("1. Crear nuevo agente")
        print("2. Listar agentes")
        print("3. Salir")
        print("="*50)
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1":
            crear_agente()
        elif opcion == "2":
            listar_agentes()
        elif opcion == "3":
            print("\n👋 ¡Hasta luego!\n")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    menu()
