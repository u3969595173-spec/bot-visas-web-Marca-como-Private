# 🔍 Cómo Usar el Sistema OCR de Validación de Documentos

## 📋 Flujo de Uso

### **1. El estudiante sube un documento**
```
Dashboard → Documentos → Seleccionar tipo → Subir archivo
```

### **2. Aparece botón "🔍 Validar con OCR"**
El sistema muestra automáticamente este botón en cada documento subido.

### **3. Click en "Validar con OCR"**
Al hacer click:
- Se envía el documento a OCR.space API
- Extrae texto automáticamente
- Valida según tipo de documento
- Muestra resultados instantáneamente

### **4. Ver resultados**
El sistema muestra:
- ✅ **Nivel de confianza**: 0-100%
  - 🟢 Alta (80-100%): Todo correcto
  - 🟡 Media (60-79%): Revisar detalles
  - 🔴 Baja (<60%): Documento problemático

- ⚠️ **Alertas automáticas**:
  - "Pasaporte vence en X días"
  - "Saldo insuficiente: 12,000€ (mínimo: 15,000€)"
  - "No se detectó número de pasaporte"
  - "Universidad no reconocida"

---

## 🎯 Tipos de Documentos Validados

### **Pasaporte** 🛂
**Extrae:**
- Número de pasaporte (ej: AB1234567)
- Fecha de emisión
- Fecha de expiración
- Zona MRZ (Machine Readable Zone)

**Valida:**
- ✅ Vigencia mínima de 6 meses
- ✅ Formato de número válido
- ✅ Presencia de MRZ

**Ejemplo de alerta:**
```
⚠️ Pasaporte vence en 45 días (mínimo 6 meses)
```

---

### **DNI/NIE** 🆔
**Extrae:**
- Número de DNI (ej: 12345678Z)
- Fecha de nacimiento
- Nombre completo

**Valida:**
- ✅ Letra de control correcta
- ✅ Formato válido
- ✅ Documento español reconocido

**Ejemplo de alerta:**
```
⚠️ Letra DNI incorrecta (esperada: Z)
```

---

### **Extracto Bancario** 💰
**Extrae:**
- Saldo disponible
- IBAN
- Fecha del extracto
- Movimientos

**Valida:**
- ✅ Saldo mínimo 15,000€
- ✅ Extracto reciente (<3 meses)
- ✅ IBAN español válido

**Ejemplo de alerta:**
```
⚠️ Saldo insuficiente: 12,500€ (mínimo: 15,000€)
⚠️ Extracto muy antiguo (95 días)
```

---

### **Carta de Admisión** 📧
**Extrae:**
- Nombre de universidad
- Programa/curso
- Fecha de inicio
- Email de contacto

**Valida:**
- ✅ Universidad española registrada
- ✅ Fecha de inicio futura
- ✅ Información de contacto

**Ejemplo de alerta:**
```
⚠️ No se reconoció una universidad española registrada
⚠️ La fecha de inicio ya pasó
```

---

### **Certificado de Idioma** 🗣️
**Extrae:**
- Nivel (A1, A2, B1, B2, C1, C2)
- Fecha de emisión
- Institución emisora

**Valida:**
- ✅ Nivel MCER detectado
- ✅ Certificado reciente
- ✅ Formato válido

---

## 💡 Ejemplos de Uso

### **Ejemplo 1: Pasaporte Válido**
```json
{
  "nivel_confianza": 95,
  "nivel_riesgo": "MUY BAJO",
  "datos_extraidos": {
    "numero_pasaporte": "AB1234567",
    "fecha_expiracion": "15/08/2027",
    "dias_vigencia": 630
  },
  "alertas": []
}
```
**Resultado:** ✅ Documento válido - puede continuar

---

### **Ejemplo 2: Extracto Bancario con Problemas**
```json
{
  "nivel_confianza": 55,
  "nivel_riesgo": "MEDIO",
  "datos_extraidos": {
    "saldo_disponible": "12,500.00 €",
    "iban": "ES91 2100 0418 4502 0005 1332",
    "fecha_extracto": "15/08/2024"
  },
  "alertas": [
    "⚠️ Saldo insuficiente: 12,500€ (mínimo: 15,000€)",
    "⚠️ Extracto muy antiguo (103 días)"
  ]
}
```
**Resultado:** ⚠️ Necesita actualizar extracto y aumentar fondos

---

## 🔧 Para Administradores

### **Ver todos los documentos procesados**
```
Dashboard Admin → Estudiantes → Ver Detalles → Documentos
```

Verás:
- Lista de documentos con estado OCR
- Nivel de confianza de cada uno
- Alertas detectadas
- Botón para reprocelar si es necesario

### **Filtrar estudiantes con problemas**
El sistema marca automáticamente estudiantes con:
- 🔴 Documentos con confianza <60%
- ⚠️ Documentos con alertas críticas
- ❌ Documentos rechazados

---

## 📊 API Endpoints

### **POST /api/documentos/{id}/validar-ocr**
Procesa un documento con OCR

**Parámetros:**
- `documento_id`: ID del documento
- `tipo_documento`: pasaporte | dni | extracto_bancario | carta_admision | certificado_idioma

**Response:**
```json
{
  "exito": true,
  "tipo_documento": "pasaporte",
  "nivel_confianza": 95,
  "datos_extraidos": {...},
  "validacion": {...},
  "alertas": []
}
```

### **GET /api/estudiantes/{id}/documentos/ocr-status**
Obtiene estado de validación OCR de todos los documentos

**Response:**
```json
{
  "estudiante_id": 123,
  "total_documentos": 5,
  "procesados_ocr": 3,
  "confianza_promedio": 82.5,
  "documentos": [...]
}
```

---

## ⚡ Límites y Rendimiento

### **OCR.space API (Plan Gratuito)**
- ✅ 25,000 requests/mes
- ✅ Máx 1MB por imagen
- ✅ Formatos: PDF, JPG, PNG
- ✅ ~3-5 segundos por documento

### **Recomendaciones**
- Procesar documentos bajo demanda (no automático)
- Validar solo documentos críticos (pasaporte, extracto)
- Cachear resultados OCR en base de datos
- Informar al usuario que tome ~5 segundos

---

## 🎓 Tips para Mejores Resultados

### **Para Estudiantes:**
1. **Escanea documentos con buena luz**
2. **Usa máximo contraste** (fondo blanco, texto negro)
3. **Evita fotos inclinadas** (usa apps de escaneo)
4. **Formato PDF preferible** sobre fotos
5. **Documentos originales** mejor que copias

### **Calidad de imagen:**
- ✅ 300 DPI mínimo
- ✅ Sin sombras ni reflejos
- ✅ Texto legible a simple vista
- ✅ Colores claros (no amarillentos)

---

## 🔐 Seguridad y Privacidad

- 🔒 Documentos procesados temporalmente
- 🗑️ OCR.space no almacena imágenes
- 📦 Datos extraídos guardados en tu BD
- 🔐 Solo admins ven resultados OCR
- ✅ Cumple GDPR

---

## 🆘 Solución de Problemas

### **"Error al extraer texto"**
- Documento muy borroso
- Formato no soportado
- Tamaño mayor a 1MB
→ Solicitar nuevo escaneo al estudiante

### **"Nivel de confianza bajo (<60%)"**
- Imagen de mala calidad
- Documento en otro idioma
- Formato no estándar
→ Revisión manual recomendada

### **"Timeout al procesar OCR"**
- API temporalmente lenta
- Conexión inestable
→ Reintentar en 1 minuto

---

## 📞 Soporte

Si necesitas ajustar las validaciones o agregar nuevos tipos de documentos, contacta al desarrollador.

**API Key actual:** K87899142388957 (Free tier - 25k/mes)
**Registrarse para más:** https://ocr.space/ocrapi
