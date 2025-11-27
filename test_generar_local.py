import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Test generador de documentos
sys.path.append('.')

from api.generador_documentos_borrador import generar_todos_documentos
import psycopg2

# Obtener estudiante 1
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = conn.cursor()

cursor.execute("""
    SELECT 
        id, nombre, email, telefono, pasaporte, fecha_nacimiento, edad, 
        nacionalidad, pais_origen, ciudad_origen, carrera_deseada, especialidad, 
        nivel_espanol, tipo_visa, fondos_disponibles, fecha_inicio_estimada,
        archivo_titulo, archivo_pasaporte, archivo_extractos
    FROM estudiantes 
    WHERE id = 1
""")

result = cursor.fetchone()

if not result:
    print("❌ Estudiante no encontrado")
    sys.exit(1)

estudiante_data = {
    "id": result[0],
    "nombre": result[1],
    "email": result[2],
    "telefono": result[3],
    "pasaporte": result[4],
    "fecha_nacimiento": result[5].isoformat() if result[5] else None,
    "edad": result[6],
    "nacionalidad": result[7],
    "pais_origen": result[8],
    "ciudad_origen": result[9],
    "carrera_deseada": result[10],
    "especialidad": result[11],
    "nivel_espanol": result[12],
    "tipo_visa": result[13],
    "fondos_disponibles": float(result[14]) if result[14] else 0,
    "fecha_inicio_estimada": result[15].isoformat() if result[15] else "próximo semestre",
    "archivo_titulo": result[16],
    "archivo_pasaporte": result[17],
    "archivo_extractos": result[18]
}

print(f"✅ Estudiante cargado: {estudiante_data['nombre']}")
print(f"📧 Email: {estudiante_data['email']}")
print(f"🎓 Carrera: {estudiante_data['carrera_deseada']}")
print(f"💰 Fondos: €{estudiante_data['fondos_disponibles']:,.2f}")
print("\n🔄 Generando documentos...")

try:
    documentos = generar_todos_documentos(estudiante_data)
    print(f"\n✅ ÉXITO: {len(documentos)} documentos generados:")
    
    for i, doc in enumerate(documentos, 1):
        print(f"\n{i}. {doc['nombre']}")
        print(f"   Tipo: {doc['tipo']}")
        print(f"   Tamaño: {len(doc['contenido'])} caracteres")
        print(f"   Primeras 200 chars:")
        print(f"   {doc['contenido'][:200]}...")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

cursor.close()
conn.close()
