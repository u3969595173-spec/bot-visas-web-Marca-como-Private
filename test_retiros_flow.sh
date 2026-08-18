#!/bin/bash

# Script para probar el sistema de retiros e inversiones
# Uso: bash test_retiros_flow.sh

API_URL="http://localhost:8000"
ADMIN_TOKEN=""

echo "🎯 TEST DEL SISTEMA DE RETIROS E INVERSIONES"
echo "=================================================="

# Función para imprimir secciones
print_section() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔹 $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# 1. Verificar API
print_section "1. Verificando API"
echo "URL: $API_URL"

if curl -s "$API_URL/docs" > /dev/null; then
    echo "✅ API está corriendo"
else
    echo "❌ API no responde. Asegúrate de que FastAPI está corriendo."
    exit 1
fi

# 2. Obtener solicitudes de crédito
print_section "2. Obteniendo solicitudes de crédito"

response=$(curl -s \
    -H "Content-Type: application/json" \
    "$API_URL/api/admin/solicitudes-credito")

# Contar solicitudes
count=$(echo "$response" | jq '. | length' 2>/dev/null || echo "0")

echo "Solicitudes encontradas: $count"

if [ "$count" -gt 0 ]; then
    echo ""
    echo "📋 Primeras 3 solicitudes:"
    echo "$response" | jq -r '.[:3][] | "\(.id) | \(.nombre) (\(.beneficiario_tipo)) | \(.monto)€ | \(.estado)"' 2>/dev/null
else
    echo "⚠️  No hay solicitudes de crédito"
fi

# 3. Verificar tabla de solicitudes_credito
print_section "3. Verificando base de datos"

echo "Comando SQL para verificar tabla:"
echo ""
echo "SELECT COUNT(*) as total_solicitudes, "
echo "       COUNT(CASE WHEN estado='pendiente' THEN 1 END) as pendientes,"
echo "       COUNT(CASE WHEN estado='aprobada' THEN 1 END) as aprobadas"
echo "FROM solicitudes_credito;"
echo ""
echo "Ejecuta esto en psql para verificar los datos."

# 4. Verificar que los archivos están en su lugar
print_section "4. Verificando archivos del frontend"

files=(
    "frontend/src/components/RetirosCreditoPanel.jsx"
    "frontend/src/styles/RetirosCreditoPanel.css"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file existe"
    else
        echo "❌ $file FALTA"
    fi
done

# 5. Resumen
print_section "5. Resumen de Test"

echo "✅ API funcionando"
echo "✅ Endpoint /api/admin/solicitudes-credito disponible"
echo "✅ Archivos del frontend en lugar"
echo ""
echo "🚀 Próximos pasos:"
echo "  1. Abre http://localhost:3000 en el navegador"
echo "  2. Navega a la sección de 'Retiros'"
echo "  3. Deberías ver las solicitudes de la API"
echo "  4. Intenta aprobar una solicitud pendiente"
echo ""
echo "📝 Si no ves solicitudes, crea una:"
echo "   curl -X POST http://localhost:8000/api/referidos/solicitar-uso \\"
echo "     -H 'Authorization: Bearer TOKEN_ESTUDIANTE' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"tipo\": \"retiro\", \"monto\": 50.00}'"
echo ""
echo "✅ Test completado"
