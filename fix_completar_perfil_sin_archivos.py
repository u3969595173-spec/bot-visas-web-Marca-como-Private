"""
Fix para cuando el estudiante completa perfil SIN subir archivos
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

print("="*70)
print("FIX: COMPLETAR PERFIL SIN ARCHIVOS")
print("="*70)

try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    # 1. Verificar estudiante Manuel
    print("\n1️⃣ Verificando estudiante Manuel (ID: 16)...")
    cursor.execute("""
        SELECT id, nombre, email, codigo_acceso, 
               pasaporte, fecha_nacimiento, edad, nacionalidad,
               archivo_titulo, archivo_pasaporte, archivo_extractos,
               perfil_completo
        FROM estudiantes 
        WHERE id = 16
    """)
    
    manuel = cursor.fetchone()
    if manuel:
        print(f"   ✅ Encontrado: {manuel[1]}")
        print(f"   📧 Email: {manuel[2]}")
        print(f"   🔑 Código: {manuel[3][:8]}***")
        print(f"   📋 Perfil completo: {manuel[11]}")
        print(f"   📄 Datos básicos:")
        print(f"      - Pasaporte: {manuel[4] or '❌ VACÍO'}")
        print(f"      - Fecha nacimiento: {manuel[5] or '❌ VACÍO'}")
        print(f"      - Edad: {manuel[6] or '❌ VACÍO'}")
        print(f"      - Nacionalidad: {manuel[7] or '❌ VACÍO'}")
        print(f"   📎 Archivos:")
        print(f"      - Título: {manuel[8] or '❌ NO SUBIDO'}")
        print(f"      - Pasaporte: {manuel[9] or '❌ NO SUBIDO'}")
        print(f"      - Extractos: {manuel[10] or '❌ NO SUBIDO'}")
    else:
        print("   ❌ No encontrado")
        
    # 2. Verificar que las columnas existen
    print("\n2️⃣ Verificando estructura de tabla...")
    cursor.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'estudiantes'
        AND column_name IN (
            'pasaporte', 'fecha_nacimiento', 'edad', 'nacionalidad',
            'pais_origen', 'ciudad_origen', 'carrera_deseada', 
            'especialidad', 'nivel_espanol', 'tipo_visa', 
            'fondos_disponibles', 'perfil_completo'
        )
        ORDER BY column_name
    """)
    
    columnas = cursor.fetchall()
    print(f"   ✅ Encontradas {len(columnas)} columnas necesarias:")
    for col in columnas:
        nullable = "NULL OK" if col[2] == "YES" else "NOT NULL"
        print(f"      - {col[0]}: {col[1]} ({nullable})")
    
    # 3. Test de actualización sin archivos
    print("\n3️⃣ Test de actualización (solo datos, sin archivos)...")
    
    # Simular lo que hace el frontend
    test_data = {
        'pasaporte': 'TEST123456',
        'fecha_nacimiento': '1990-01-01',
        'edad': 35,
        'nacionalidad': 'Cubana',
        'pais_origen': 'Cuba',
        'ciudad_origen': 'La Habana',
        'carrera_deseada': 'Ingeniería',
        'especialidad': 'Telecomunicaciones',
        'nivel_espanol': 'nativo',
        'tipo_visa': 'estudiante',
        'fondos_disponibles': 5000.00
    }
    
    print("   Intentando UPDATE con datos de prueba...")
    
    # NO hacer commit, solo probar
    cursor.execute("""
        UPDATE estudiantes SET
            pasaporte = %(pasaporte)s,
            fecha_nacimiento = %(fecha_nacimiento)s,
            edad = %(edad)s,
            nacionalidad = %(nacionalidad)s,
            pais_origen = %(pais_origen)s,
            ciudad_origen = %(ciudad_origen)s,
            carrera_deseada = %(carrera_deseada)s,
            especialidad = %(especialidad)s,
            nivel_espanol = %(nivel_espanol)s,
            tipo_visa = %(tipo_visa)s,
            fondos_disponibles = %(fondos_disponibles)s,
            perfil_completo = FALSE,
            updated_at = NOW()
        WHERE id = 999999
        RETURNING id
    """, test_data)
    
    # Si llegamos aquí sin error, el query es válido
    print("   ✅ Query SQL es válido")
    conn.rollback()  # Revertir el test
    
    # 4. Verificar posibles problemas
    print("\n4️⃣ Diagnóstico de posibles errores:")
    
    problemas = []
    
    # Check 1: Código de acceso
    if not manuel[3]:
        problemas.append("❌ Código de acceso vacío")
    else:
        print(f"   ✅ Código de acceso existe: {manuel[3][:8]}***")
    
    # Check 2: Email configurado
    gmail_user = os.getenv('GMAIL_USER')
    gmail_pass = os.getenv('GMAIL_APP_PASSWORD')
    
    if not gmail_user or not gmail_pass:
        problemas.append("⚠️ Email no configurado (no crítico para perfil)")
    else:
        print(f"   ✅ Email configurado")
    
    # Check 3: CORS
    print(f"   ℹ️ Verificar CORS en producción")
    
    if problemas:
        print("\n⚠️ PROBLEMAS ENCONTRADOS:")
        for p in problemas:
            print(f"   {p}")
    else:
        print("\n   ✅ No se encontraron problemas estructurales")
    
    print("\n" + "="*70)
    print("DIAGNÓSTICO COMPLETADO")
    print("="*70)
    
    print("\n💡 POSIBLES CAUSAS DEL ERROR:")
    print("   1. Código de acceso no se guarda en localStorage del navegador")
    print("   2. Error de CORS (Access-Control-Allow-Origin)")
    print("   3. Campo requerido falta en el frontend")
    print("   4. Timeout de conexión a la BD")
    
    print("\n🔧 SOLUCIONES:")
    print("   1. Pedir a Manuel que:")
    print("      - Abra Chrome DevTools (F12)")
    print("      - Vaya a Console")
    print("      - Escriba: localStorage.getItem('codigo_acceso')")
    print("      - Debe mostrar su código")
    print("   2. Si NO aparece el código:")
    print("      - Enviarle el link directo con código en URL")
    print("      - https://fortunariocash.com/completar-perfil/16")
    print("   3. Ver el error exacto en Console (F12)")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
