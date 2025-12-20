"""
Script para diagnosticar errores al completar perfil
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

print("="*70)
print("DIAGNÓSTICO: ERROR AL COMPLETAR PERFIL")
print("="*70)

try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    # 1. Verificar que la columna perfil_completo existe
    print("\n1️⃣ Verificando columna 'perfil_completo'...")
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'estudiantes' 
        AND column_name = 'perfil_completo'
    """)
    column = cursor.fetchone()
    
    if column:
        print(f"   ✅ Columna perfil_completo existe: {column[1]}")
    else:
        print(f"   ❌ Columna perfil_completo NO EXISTE")
        print("   🔧 Agregando columna...")
        cursor.execute("""
            ALTER TABLE estudiantes 
            ADD COLUMN IF NOT EXISTS perfil_completo BOOLEAN DEFAULT FALSE
        """)
        conn.commit()
        print("   ✅ Columna agregada")
    
    # 2. Verificar columnas de archivos
    print("\n2️⃣ Verificando columnas de archivos...")
    columnas_necesarias = ['archivo_titulo', 'archivo_pasaporte', 'archivo_extractos']
    for col in columnas_necesarias:
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'estudiantes' 
            AND column_name = %s
        """, (col,))
        
        if cursor.fetchone():
            print(f"   ✅ {col} existe")
        else:
            print(f"   ❌ {col} NO EXISTE")
            print(f"   🔧 Agregando {col}...")
            cursor.execute(f"""
                ALTER TABLE estudiantes 
                ADD COLUMN IF NOT EXISTS {col} TEXT
            """)
            conn.commit()
            print(f"   ✅ {col} agregada")
    
    # 3. Verificar estudiantes recientes sin perfil completo
    print("\n3️⃣ Estudiantes recientes sin perfil completo:")
    cursor.execute("""
        SELECT id, nombre, email, codigo_acceso, perfil_completo, created_at
        FROM estudiantes 
        WHERE created_at > NOW() - INTERVAL '7 days'
        ORDER BY created_at DESC
        LIMIT 5
    """)
    
    estudiantes = cursor.fetchall()
    if estudiantes:
        for est in estudiantes:
            perfil = "✅" if est[4] else "❌"
            print(f"   {perfil} ID: {est[0]} | {est[1]} | {est[2]}")
            print(f"      Código: {est[3][:8]}*** | Fecha: {est[5]}")
    else:
        print("   No hay estudiantes recientes")
    
    # 4. Verificar directorio uploads
    print("\n4️⃣ Verificando directorio uploads...")
    import pathlib
    uploads_dir = pathlib.Path("uploads")
    if uploads_dir.exists():
        print(f"   ✅ Directorio uploads existe")
        archivos = list(uploads_dir.glob("*"))
        print(f"   📁 {len(archivos)} archivos subidos")
    else:
        print(f"   ❌ Directorio uploads NO existe")
        print("   🔧 Creando directorio...")
        uploads_dir.mkdir(exist_ok=True)
        print("   ✅ Directorio creado")
    
    # 5. Test de conexión
    print("\n5️⃣ Test de conexión a BD...")
    cursor.execute("SELECT NOW()")
    now = cursor.fetchone()[0]
    print(f"   ✅ Conexión OK: {now}")
    
    print("\n" + "="*70)
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("="*70)
    print("\n💡 INSTRUCCIONES PARA EL ESTUDIANTE:")
    print("   1. Verifica que tienes el código de acceso (revisar email)")
    print("   2. Abre el navegador en modo incógnito")
    print("   3. Ingresa con tu código de acceso")
    print("   4. Completa el perfil paso a paso")
    print("   5. Si sigue fallando, envíame el error exacto que aparece")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
