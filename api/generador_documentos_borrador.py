"""
Generador automático de documentos borrador para estudiantes
"""

from datetime import datetime

def generar_carta_aceptacion(estudiante_data: dict) -> str:
    """
    Genera carta de aceptación borrador
    """
    nombre = estudiante_data.get('nombre', '')
    pasaporte = estudiante_data.get('pasaporte', '')
    nacionalidad = estudiante_data.get('nacionalidad', '')
    carrera = estudiante_data.get('carrera_deseada', 'programa académico')
    fecha_inicio = estudiante_data.get('fecha_inicio_estimada', 'próximo semestre')
    
    carta = f"""
CARTA DE ACEPTACIÓN UNIVERSITARIA
[BORRADOR - VERIFICAR CON INSTITUCIÓN]

Fecha: {datetime.now().strftime('%d de %B de %Y')}

A QUIEN CORRESPONDA:

Por medio de la presente, hacemos constar que el/la estudiante:

Nombre completo: {nombre}
Número de pasaporte: {pasaporte}
Nacionalidad: {nacionalidad}

Ha sido ACEPTADO(A) en nuestro programa de {carrera} con inicio previsto para {fecha_inicio}.

Duración del programa: [COMPLETAR]
Costo total del programa: [COMPLETAR]
Nivel de español requerido: {estudiante_data.get('nivel_espanol', 'intermedio')}

REQUISITOS DE MATRÍCULA:
- Pago de matrícula inicial: €[MONTO]
- Seguro médico estudiantil
- Prueba de fondos económicos
- Título académico apostillado

La institución se compromete a brindar apoyo académico completo durante el período de estudios.

Atentamente,

[FIRMA Y SELLO DE LA INSTITUCIÓN]
[Nombre del representante]
[Cargo]

---
NOTA: Este es un BORRADOR. Debe ser completado y firmado por la institución educativa oficial.
"""
    return carta


def generar_carta_patrocinio(estudiante_data: dict) -> str:
    """
    Genera carta de patrocinio/solvencia económica
    """
    nombre = estudiante_data.get('nombre', '')
    pasaporte = estudiante_data.get('pasaporte', '')
    fondos = estudiante_data.get('fondos_disponibles', 0)
    
    carta = f"""
CARTA DE PATROCINIO ECONÓMICO
[BORRADOR - COMPLETAR CON DATOS REALES]

Fecha: {datetime.now().strftime('%d de %B de %Y')}

A QUIEN CORRESPONDA:
Consulado de España en [PAÍS]

Yo, [NOMBRE DEL PATROCINADOR], con documento de identidad [NÚMERO], declaro bajo juramento que:

1. RELACIÓN CON EL ESTUDIANTE:
   Soy [padre/madre/familiar/patrocinador] de {nombre}, titular del pasaporte {pasaporte}.

2. COMPROMISO ECONÓMICO:
   Me comprometo a cubrir todos los gastos de manutención, alojamiento, estudios y gastos personales 
   del estudiante durante su estancia en España.

3. CAPACIDAD ECONÓMICA:
   Dispongo de fondos suficientes por un monto aproximado de €{fondos:,.2f} para garantizar 
   el sustento del estudiante durante todo el período académico.

4. DOCUMENTACIÓN ADJUNTA:
   - Extractos bancarios de los últimos 3 meses
   - Certificado de ingresos
   - Declaración de impuestos
   - [Otros documentos de respaldo]

5. COMPROMISO:
   Me comprometo a garantizar el retorno del estudiante a su país de origen al finalizar 
   sus estudios, asumiendo todos los costos asociados.

Firma: _____________________
Nombre: [NOMBRE COMPLETO]
Documento: [NÚMERO]
Teléfono: [NÚMERO]
Email: [EMAIL]

---
NOTA: Este es un BORRADOR. Debe ser completado con datos reales, firmado ante notario y apostillado.
"""
    return carta


def generar_checklist_personalizado(estudiante_data: dict) -> str:
    """
    Genera checklist personalizado según tipo de visa y nacionalidad
    """
    tipo_visa = estudiante_data.get('tipo_visa', 'estudiante')
    nacionalidad = estudiante_data.get('nacionalidad', '')
    nombre = estudiante_data.get('nombre', '')
    
    checklist = f"""
CHECKLIST PERSONALIZADO: VISA DE ESTUDIANTE PARA ESPAÑA
Estudiante: {nombre}
Tipo de visa: {tipo_visa.upper()}
Nacionalidad: {nacionalidad}

═══════════════════════════════════════════════════════════════

✅ DOCUMENTOS OBLIGATORIOS (TODOS):

□ Formulario de solicitud de visado nacional (completado y firmado)
□ Fotografía reciente tamaño pasaporte (fondo blanco)
□ Pasaporte original vigente (mínimo 1 año de validez)
□ Fotocopia de todas las páginas del pasaporte
□ Certificado médico (formato oficial del consulado)
□ Certificado de antecedentes penales apostillado
□ Seguro médico con cobertura mínima €30,000

═══════════════════════════════════════════════════════════════

📚 DOCUMENTOS ACADÉMICOS:

□ Carta de aceptación de la universidad española (original)
□ Título académico previo apostillado
□ Expediente académico completo apostillado
□ Certificado de nivel de español (DELE, SIELE, o equivalente)
"""
    
    if tipo_visa == 'idiomas':
        checklist += """
□ Matrícula pagada del curso de español (mínimo 20 horas/semana)
□ Comprobante de pago de matrícula
"""
    else:
        checklist += """
□ Plan de estudios del programa
□ Comprobante de pago de matrícula universitaria
"""
    
    checklist += """
═══════════════════════════════════════════════════════════════

💰 DOCUMENTOS FINANCIEROS:

□ Extractos bancarios últimos 3-6 meses
□ Carta de patrocinio económico (si aplica)
□ Certificado de ingresos del patrocinador
□ Declaración de impuestos del patrocinador
□ Prueba de fondos: Mínimo €6,000-€10,000 (según duración)

═══════════════════════════════════════════════════════════════

🏠 DOCUMENTOS DE ALOJAMIENTO:

□ Reserva o contrato de alojamiento en España
   Opciones:
   • Residencia estudiantil (carta de asignación)
   • Alquiler privado (contrato firmado)
   • Carta de invitación de familiar en España

═══════════════════════════════════════════════════════════════
"""
    
    # Requisitos específicos por nacionalidad
    if nacionalidad.lower() in ['colombia', 'perú', 'ecuador', 'venezuela', 'méxico']:
        checklist += """
⚠️ REQUISITOS ADICIONALES PARA LATINOAMÉRICA:

□ Todos los documentos deben estar apostillados
□ Prueba de vínculos familiares en país de origen
□ Carta de intención de retorno
□ Documentos traducidos al español por traductor oficial (si están en otro idioma)

"""
    
    checklist += f"""
═══════════════════════════════════════════════════════════════

📋 PROCESO PASO A PASO:

1. ✅ Completar todos los documentos de este checklist
2. ⏰ Solicitar cita en consulado español (con 2-3 meses de anticipación)
3. 💶 Pagar tasa consular (aproximadamente €160)
4. 📤 Presentar solicitud en persona en el consulado
5. 🔍 Entrevista consular (preparar respuestas sobre estudios y planes)
6. ⏳ Esperar resolución (4-8 semanas normalmente)
7. ✈️ Recoger visa y comprar vuelo a España

═══════════════════════════════════════════════════════════════

⚡ CONSEJOS IMPORTANTES:

• Inicia el proceso con 3-4 meses de anticipación
• Todos los documentos extranjeros deben estar apostillados
• Las traducciones deben ser oficiales
• Mantén copias de TODOS los documentos
• Lleva originales + 2 copias de cada documento
• Practica tu entrevista consular en español
• Demuestra intención de retornar a tu país

═══════════════════════════════════════════════════════════════

📞 CONTACTOS ÚTILES:

Consulado de España en {nacionalidad}: [BUSCAR DATOS]
Embajada: [BUSCAR DATOS]
Universidad de destino: [COMPLETAR]

---
GENERADO AUTOMÁTICAMENTE - {datetime.now().strftime('%d/%m/%Y')}
Verificar requisitos actualizados en la web oficial del consulado.
"""
    
    return checklist


def generar_todos_documentos(estudiante_data: dict) -> dict:
    """
    Genera todos los documentos y retorna un diccionario
    """
    return {
        'carta_aceptacion': generar_carta_aceptacion(estudiante_data),
        'carta_patrocinio': generar_carta_patrocinio(estudiante_data),
        'checklist_personalizado': generar_checklist_personalizado(estudiante_data)
    }
