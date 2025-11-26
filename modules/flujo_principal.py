"""
Flujo Principal de Negocio - Agencia Educativa
SEMI-AUTOMATIZADO: Bot procesa → Admin revisa → Envío manual
"""

from datetime import datetime, timedelta
from typing import Dict
from modules.estudiantes import GestorEstudiantes, Estudiante
from modules.cursos import GestorCursos
from modules.fondos import GestorFondos
from modules.alojamiento import GestorAlojamiento
from modules.notificaciones import SistemaNotificaciones
from modules.admin_panel import PanelAdministrativo
from database.models import get_db


class FlujoPrincipal:
    """
    Flujo SEMI-AUTOMATIZADO de la agencia:
    1. Estudiante registra todos sus datos
    2. Bot procesa TODO automáticamente (cursos, fondos, alojamiento, checklist)
    3. Admin revisa en panel de control
    4. Admin aprueba/modifica
    5. Admin envía manualmente al estudiante
    """
    
    @staticmethod
    def registrar_estudiante(datos_completos: Dict) -> Dict:
        """
        PASO 1: Recopilación completa de datos del estudiante
        El estudiante proporciona TODA la información necesaria de una vez:
        - Datos personales
        - Carrera/profesión
        - Nivel de idioma
        - Fondos disponibles o patrocinador
        - Preferencias de curso (especialidad, duración, ciudad)
        
        Args:
            datos_completos: Diccionario con TODA la información del estudiante
            
        Returns:
            Diccionario con resultado del registro
        """
        try:
            # 1. Registrar estudiante con todos los datos
            estudiante = GestorEstudiantes.registrar_estudiante(datos_completos)
            
            # 2. Marcar como registrado
            db = get_db()
            est = db.query(Estudiante).filter(Estudiante.id == estudiante.id).first()
            est.estado_procesamiento = 'registrado'
            db.commit()
            db.close()
            
            # 3. Notificar al estudiante (confirmación simple)
            SistemaNotificaciones.notificar_estudiante(
                estudiante.id,
                mensaje=f"""
¡Hola {estudiante.nombre_completo}! 👋

Hemos recibido tu registro exitosamente.

🤖 Nuestro sistema está procesando tu información automáticamente:
   • Buscando cursos relevantes para ti
   • Verificando tu situación económica
   • Generando tu checklist de documentos
   • Buscando opciones de alojamiento

⏱️ Este proceso toma solo unos minutos.

Un miembro de nuestro equipo revisará toda la información y te contactará pronto con tu plan personalizado.

¡Gracias por confiar en nosotros! 🇪🇸
""",
                titulo="✅ Registro recibido",
                canales=['telegram', 'email']
            )
            
            # 4. Alerta a administradores
            SistemaNotificaciones._crear_alerta_admin(
                tipo='nuevo_estudiante',
                titulo=f'Nuevo estudiante registrado: {estudiante.nombre_completo}',
                descripcion=f'Especialidad: {estudiante.especialidad_interes or "No especificada"}\nIniciando procesamiento automático...',
                estudiante_id=estudiante.id,
                prioridad='normal'
            )
            
            return {
                'exito': True,
                'estudiante_id': estudiante.id,
                'mensaje': 'Estudiante registrado. Iniciando procesamiento automático.',
                'estado': 'registrado'
            }
            
        except Exception as e:
            return {
                'exito': False,
                'error': str(e)
            }
    
    @staticmethod
    def procesar_automaticamente(estudiante_id: int) -> Dict:
        """
        PASO 2: PROCESAMIENTO AUTOMÁTICO COMPLETO
        El bot procesa automáticamente TODA la información sin intervención:
        a) Buscar cursos relevantes según perfil
        b) Generar checklist de documentos necesarios
        c) Verificar fondos y generar carta de patrocinio si aplica
        d) Sugerir opciones de alojamiento
        
        TODO se procesa automáticamente y queda listo para revisión del admin.
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Diccionario con todo el procesamiento completado
        """
        db = get_db()
        
        try:
            estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
            
            if not estudiante:
                return {'exito': False, 'error': 'Estudiante no encontrado'}
            
            print(f"🤖 Iniciando procesamiento automático para {estudiante.nombre_completo}...")
            
            # A) BUSCAR CURSOS RELEVANTES
            print("  📚 Buscando cursos relevantes...")
            cursos_sugeridos = []
            if estudiante.especialidad_interes:
                cursos = GestorCursos.filtrar_cursos(
                    especialidad=estudiante.especialidad_interes.lower(),
                    nivel_idioma=estudiante.nivel_espanol.lower() if estudiante.nivel_espanol else None,
                    precio_max=estudiante.presupuesto_curso if hasattr(estudiante, 'presupuesto_curso') else None
                )
                cursos_sugeridos = cursos[:5]  # Top 5 cursos
                
                # Auto-asignar el mejor curso (el primero)
                if cursos_sugeridos:
                    mejor_curso = cursos_sugeridos[0]
                    GestorEstudiantes.asignar_curso(estudiante_id, mejor_curso.id)
                    print(f"  ✅ Curso sugerido: {mejor_curso.nombre} ({mejor_curso.escuela})")
            
            # B) GENERAR CHECKLIST DE DOCUMENTOS
            print("  📋 Generando checklist de documentos...")
            checklist = GestorEstudiantes.checklist_documentos(estudiante_id)
            print(f"  ✅ {checklist['total_obligatorios']} documentos obligatorios identificados")
            
            # C) VERIFICAR FONDOS Y PATROCINIO
            print("  💰 Verificando fondos económicos...")
            verificacion_fondos = GestorFondos.verificar_fondos(estudiante_id)
            
            # Si tiene patrocinador, generar carta automáticamente
            carta_patrocinio_generada = False
            if estudiante.tiene_patrocinador and estudiante.patrocinador_id:
                try:
                    pdf_bytes = GestorFondos.generar_carta_patrocinio(
                        estudiante.patrocinador_id,
                        estudiante_id
                    )
                    carta_patrocinio_generada = True
                    print("  ✅ Carta de patrocinio generada automáticamente")
                except Exception as e:
                    print(f"  ⚠️ Error generando carta: {e}")
            
            print(f"  ✅ Fondos: {verificacion_fondos['fondos_disponibles']:,.2f}€ / {verificacion_fondos['fondos_minimos_requeridos']:,.2f}€")
            
            # D) SUGERIR ALOJAMIENTO
            print("  🏠 Buscando opciones de alojamiento...")
            alojamientos_sugeridos = []
            if estudiante.necesita_alojamiento and estudiante.curso_asignado_id:
                curso = GestorCursos.obtener_curso_por_id(estudiante.curso_asignado_id)
                if curso:
                    alojamientos = GestorAlojamiento.buscar_alojamientos(
                        ciudad=curso.ciudad,
                        disponible=True,
                        precio_max=estudiante.presupuesto_alojamiento if hasattr(estudiante, 'presupuesto_alojamiento') else None
                    )
                    alojamientos_sugeridos = alojamientos[:5]  # Top 5
                    print(f"  ✅ {len(alojamientos_sugeridos)} opciones de alojamiento encontradas")
            
            # Actualizar estado a procesado_automaticamente
            estudiante.estado_procesamiento = 'procesado_automaticamente'
            estudiante.fecha_procesamiento_automatico = datetime.now()
            db.commit()
            
            print(f"✅ Procesamiento automático completado para {estudiante.nombre_completo}")
            
            # Notificar a admins que hay un nuevo caso pendiente de revisión
            SistemaNotificaciones._crear_alerta_admin(
                tipo='procesamiento_completado',
                titulo=f'Procesamiento completado: {estudiante.nombre_completo}',
                descripcion=f'• {len(cursos_sugeridos)} cursos encontrados\n• Fondos: {verificacion_fondos["porcentaje_cobertura"]:.0f}% cubiertos\n• {len(alojamientos_sugeridos)} alojamientos disponibles\n\n⏳ Pendiente de revisión admin',
                estudiante_id=estudiante_id,
                prioridad='alta'
            )
            
            return {
                'exito': True,
                'estudiante_id': estudiante_id,
                'estado': 'procesado_automaticamente',
                'resumen': {
                    'cursos_encontrados': len(cursos_sugeridos),
                    'documentos_obligatorios': checklist['total_obligatorios'],
                    'fondos_suficientes': verificacion_fondos['fondos_suficientes'],
                    'porcentaje_fondos': verificacion_fondos['porcentaje_cobertura'],
                    'carta_patrocinio': carta_patrocinio_generada,
                    'alojamientos_disponibles': len(alojamientos_sugeridos)
                },
                'mensaje': 'Procesamiento automático completado. Pendiente de revisión admin.'
            }
            
        except Exception as e:
            db.rollback()
            return {'exito': False, 'error': str(e)}
        finally:
            db.close()
        """
        PASO 2: Bot sugiere cursos y estudiante confirma
        
        Args:
            estudiante_id: ID del estudiante
            curso_id: ID del curso seleccionado (opcional, si None sugiere)
            
        Returns:
            Diccionario con cursos sugeridos o confirmación de asignación
        """
        estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=estudiante_id)
        
        if not estudiante:
            return {'error': 'Estudiante no encontrado'}
        
        if curso_id:
            # Asignar curso específico
            resultado = GestorEstudiantes.asignar_curso(estudiante_id, curso_id)
            
            if resultado.get('exito'):
                # Notificar estudiante
                curso = resultado['curso']
                SistemaNotificaciones.notificar_estudiante(
                    estudiante_id,
                    mensaje=f"""
🎓 **Curso asignado exitosamente**

{curso.nombre}
🏫 {curso.escuela}
🌍 {curso.ciudad}
⏱️ Duración: {curso.duracion_meses} meses
💰 Precio: {curso.precio}€

📅 Inicio: {curso.fecha_inicio.strftime('%d/%m/%Y') if curso.fecha_inicio else 'Por confirmar'}

**Próximos pasos:**
1. Verificaremos tus fondos económicos
2. Generaremos documentación específica
3. Te prepararemos para la solicitud de visa
""",
                    titulo="✅ Curso asignado",
                    canales=['telegram', 'email']
                )
                
                # Actualizar checklist con requisitos del curso
                GestorEstudiantes.checklist_documentos(estudiante_id)
            
            return resultado
        else:
            # Sugerir cursos
            return GestorEstudiantes.asignar_curso(estudiante_id, auto_sugerir=True)
    
    @staticmethod
    def verificar_y_gestionar_fondos(estudiante_id: int) -> Dict:
        """
        PASO 3: Verifica fondos económicos y alerta si falta algo
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Diccionario con evaluación de fondos
        """
        verificacion = GestorFondos.verificar_fondos(estudiante_id)
        estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=estudiante_id)
        
        if not estudiante:
            return {'error': 'Estudiante no encontrado'}
        
        # Determinar mensaje según estado de fondos
        if verificacion['porcentaje_cobertura'] >= 100:
            mensaje_estado = f"""
✅ **FONDOS SUFICIENTES**

{verificacion['mensaje']}

Tienes {verificacion['fondos_disponibles']:,.2f}€ disponibles.
Mínimo requerido: {verificacion['fondos_minimos_requeridos']:,.2f}€

✅ Puedes proceder con la solicitud de visa.
"""
        else:
            mensaje_estado = f"""
⚠️ **FONDOS INSUFICIENTES**

{verificacion['mensaje']}

Tienes: {verificacion['fondos_disponibles']:,.2f}€
Necesitas: {verificacion['fondos_minimos_requeridos']:,.2f}€
Déficit: {verificacion['deficit']:,.2f}€

**Opciones:**
1. Buscar un patrocinador (familiar en España/Cuba)
2. Solicitar préstamo estudiantil
3. Buscar beca parcial
4. Ahorrar el monto faltante

Nuestro equipo puede ayudarte a gestionar un patrocinador.
"""
        
        # Enviar notificación
        SistemaNotificaciones.notificar_estudiante(
            estudiante_id,
            mensaje=mensaje_estado + "\n\n**Desglose de fondos:**\n" + 
                   f"• Matrícula: {verificacion['desglose']['matricula']:,.2f}€\n" +
                   f"• Manutención: {verificacion['desglose']['manutencion']:,.2f}€\n" +
                   f"• Alojamiento: {verificacion['desglose']['alojamiento']:,.2f}€\n" +
                   f"• Seguro: {verificacion['desglose']['seguro']:,.2f}€",
            titulo="💰 Verificación de fondos",
            canales=['telegram']
        )
        
        # Si fondos insuficientes, crear alerta para admin
        if verificacion['porcentaje_cobertura'] < 100:
            SistemaNotificaciones._crear_alerta_admin(
                tipo='fondos_insuficientes',
                titulo=f'Fondos insuficientes: {estudiante.nombre_completo}',
                descripcion=f'Déficit: {verificacion["deficit"]:,.2f}€',
                estudiante_id=estudiante_id,
                prioridad='alta'
            )
        
        return verificacion
    
    @staticmethod
    def gestionar_documentos_y_recordatorios(estudiante_id: int) -> Dict:
        """
        PASO 4: Genera checklist y configura recordatorios automáticos
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Diccionario con checklist y recordatorios configurados
        """
        estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=estudiante_id)
        
        if not estudiante:
            return {'error': 'Estudiante no encontrado'}
        
        # Obtener checklist actualizado
        checklist = GestorEstudiantes.checklist_documentos(estudiante_id)
        
        # Crear recordatorios para documentos críticos
        hoy = datetime.utcnow()
        
        # Recordatorio para iniciar documentos (3 días)
        GestorEstudiantes.crear_evento(
            estudiante_id=estudiante_id,
            tipo_evento='recordatorio',
            titulo='Inicio de recolección de documentos',
            fecha_evento=hoy + timedelta(days=3),
            descripcion='Es momento de comenzar a reunir todos los documentos necesarios',
            dias_recordatorio=1
        )
        
        # Recordatorio para completar documentos (7 días)
        GestorEstudiantes.crear_evento(
            estudiante_id=estudiante_id,
            tipo_evento='recordatorio',
            titulo='Plazo para completar documentos',
            fecha_evento=hoy + timedelta(days=7),
            descripcion='Fecha límite recomendada para tener todos los documentos listos',
            dias_recordatorio=2
        )
        
        # Notificar sobre checklist
        mensaje_docs = f"""
📋 **CHECKLIST DE DOCUMENTOS GENERADO**

**Documentos obligatorios:** {checklist['total_obligatorios']}
**Documentos recomendados:** {checklist['total_recomendados']}

Los documentos obligatorios son esenciales para tu visa.
Los recomendados aumentan tu probabilidad de aprobación.

⏰ **Recordatorios configurados:**
• Inicio de recolección: en 3 días
• Plazo recomendado: en 7 días

Te iremos recordando sobre cada documento y su fecha de vencimiento.
"""
        
        SistemaNotificaciones.notificar_estudiante(
            estudiante_id,
            mensaje=mensaje_docs,
            titulo="📋 Checklist de documentos",
            canales=['telegram', 'email']
        )
        
        return {
            'checklist': checklist,
            'recordatorios_configurados': 2
        }
    
    @staticmethod
    def coordinar_alojamiento(estudiante_id: int, preferencias: Dict = None) -> Dict:
        """
        PASO 5: Busca y asigna alojamiento si es necesario
        
        Args:
            estudiante_id: ID del estudiante
            preferencias: Diccionario con preferencias de alojamiento
            
        Returns:
            Diccionario con opciones de alojamiento
        """
        estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=estudiante_id)
        
        if not estudiante:
            return {'error': 'Estudiante no encontrado'}
        
        if not estudiante.necesita_alojamiento:
            return {'mensaje': 'Estudiante ya tiene alojamiento o no lo necesita'}
        
        # Obtener curso para saber la ciudad
        ciudad = None
        if estudiante.curso_asignado_id:
            curso = GestorCursos.obtener_curso_por_id(estudiante.curso_asignado_id)
            if curso:
                ciudad = curso.ciudad
        
        # Buscar alojamientos disponibles
        precio_max = preferencias.get('precio_max') if preferencias else None
        tipo = preferencias.get('tipo') if preferencias else None
        
        alojamientos = GestorAlojamiento.buscar_alojamientos(
            ciudad=ciudad,
            precio_max=precio_max,
            tipo=tipo,
            disponible=True
        )
        
        if alojamientos:
            mensaje = f"""
🏠 **ALOJAMIENTOS DISPONIBLES**

Encontramos {len(alojamientos)} opciones en {ciudad or 'España'}:

"""
            for i, aloj in enumerate(alojamientos[:5], 1):
                mensaje += f"""
{i}. {aloj.tipo.replace('_', ' ').title()}
   📍 {aloj.direccion}, {aloj.ciudad}
   💰 {aloj.precio_mensual}€/mes {'(gastos incluidos)' if aloj.gastos_incluidos else ''}
   🛏️ {aloj.num_habitaciones} hab | 🚿 {aloj.num_banos} baños
   📏 {aloj.metros_cuadrados}m²
   
"""
            
            mensaje += "\nUn agente te contactará para coordinar visitas y asignación."
            
            SistemaNotificaciones.notificar_estudiante(
                estudiante_id,
                mensaje=mensaje,
                titulo="🏠 Alojamientos disponibles",
                canales=['telegram']
            )
        else:
            SistemaNotificaciones.notificar_estudiante(
                estudiante_id,
                mensaje="No encontramos alojamientos disponibles con tus criterios. Nuestro equipo buscará más opciones y te contactará pronto.",
                titulo="🏠 Búsqueda de alojamiento",
                canales=['telegram']
            )
        
        return {
            'alojamientos_encontrados': len(alojamientos),
            'opciones': alojamientos[:5]
        }
    
    @staticmethod
    def generar_y_enviar_reportes(estudiante_id: int) -> Dict:
        """
        PASO 6: Genera todos los reportes y documentos necesarios
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Diccionario con reportes generados
        """
        from utils.predictor import SuccessPredictor
        from utils.calculator import FundsCalculator
        
        estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=estudiante_id)
        
        if not estudiante:
            return {'error': 'Estudiante no encontrado'}
        
        # 1. Reporte de probabilidad de éxito
        application_data = {
            'country_origin': estudiante.nacionalidad.lower(),
            'study_type': estudiante.especialidad_interes or 'master',
            'university_type': 'publica',  # Ajustar según datos reales
            'funds_evaluation': GestorFondos.verificar_fondos(estudiante_id),
            'spanish_level': estudiante.nivel_espanol or 'b1',
            'has_recommendations': False,
            'num_recommendations': 0,
            'clean_background': True,
            'has_insurance': True,
            'insurance_quality': 'recognized',
            'documents_complete_percentage': (len(estudiante.documentos_completados) / 
                (len(estudiante.documentos_completados) + len(estudiante.documentos_pendientes)) * 100)
                if (len(estudiante.documentos_completados) + len(estudiante.documentos_pendientes)) > 0 else 0
        }
        
        prediccion = SuccessPredictor.calculate_score(application_data)
        
        # 2. Generar carta de patrocinio si tiene patrocinador
        carta_patrocinio_generada = False
        if estudiante.tiene_patrocinador and estudiante.patrocinador_id:
            try:
                pdf_bytes = GestorFondos.generar_carta_patrocinio(
                    estudiante.patrocinador_id,
                    estudiante_id
                )
                # Guardar el PDF (aquí se guardaría en el sistema de archivos)
                carta_patrocinio_generada = True
            except:
                pass
        
        # 3. Enviar reporte al estudiante
        mensaje_reporte = f"""
📊 **REPORTE COMPLETO GENERADO**

**Probabilidad de aprobación de visa:** {prediccion['probability']:.0f}%

{prediccion['status']}

**Recomendación:** {prediccion['recommendation']}

**Documentos:**
• Completados: {len(estudiante.documentos_completados)}
• Pendientes: {len(estudiante.documentos_pendientes)}

"""
        
        if carta_patrocinio_generada:
            mensaje_reporte += "✅ Carta de patrocinio generada\n"
        
        if prediccion['improvements']:
            mensaje_reporte += "\n**Mejoras sugeridas:**\n"
            for mejora in prediccion['improvements']:
                mensaje_reporte += f"{mejora}\n"
        
        SistemaNotificaciones.notificar_estudiante(
            estudiante_id,
            mensaje=mensaje_reporte,
            titulo="📊 Reporte completo",
            canales=['telegram', 'email']
        )
        
        return {
            'prediccion': prediccion,
            'carta_patrocinio': carta_patrocinio_generada,
            'documentos_completados': len(estudiante.documentos_completados),
            'documentos_pendientes': len(estudiante.documentos_pendientes)
        }
    
    @staticmethod
    def flujo_semi_automatizado(datos_completos: Dict) -> Dict:
        """
        FLUJO COMPLETO SEMI-AUTOMATIZADO
        
        1. Estudiante se registra con TODOS los datos
        2. Bot procesa automáticamente:
           - Cursos relevantes
           - Checklist de documentos
           - Verificación de fondos / carta de patrocinio
           - Opciones de alojamiento
        3. Admin revisa todo en el panel de control
        4. Admin envía manualmente la información al estudiante
        
        Args:
            datos_completos: Diccionario completo con información del estudiante
            
        Returns:
            Diccionario con resultado del flujo hasta el punto de revisión admin
        """
        # PASO 1: REGISTRO COMPLETO
        print("=" * 60)
        print("INICIANDO FLUJO SEMI-AUTOMATIZADO")
        print("=" * 60)
        
        registro = FlujoPrincipal.registrar_estudiante(datos_completos)
        
        if not registro['exito']:
            return registro
        
        estudiante_id = registro['estudiante_id']
        print(f"\n✅ PASO 1/2: Estudiante registrado (ID: {estudiante_id})")
        
        # PASO 2: PROCESAMIENTO AUTOMÁTICO COMPLETO
        print("\n🤖 PASO 2/2: Iniciando procesamiento automático...")
        procesamiento = FlujoPrincipal.procesar_automaticamente(estudiante_id)
        
        if not procesamiento['exito']:
            return procesamiento
        
        print("\n" + "=" * 60)
        print("✅ PROCESAMIENTO AUTOMÁTICO COMPLETADO")
        print("=" * 60)
        print(f"\n📊 RESUMEN:")
        print(f"  • Cursos encontrados: {procesamiento['resumen']['cursos_encontrados']}")
        print(f"  • Documentos obligatorios: {procesamiento['resumen']['documentos_obligatorios']}")
        print(f"  • Fondos: {procesamiento['resumen']['porcentaje_fondos']:.0f}% cubiertos")
        print(f"  • Carta patrocinio: {'✅ Sí' if procesamiento['resumen']['carta_patrocinio'] else '❌ No'}")
        print(f"  • Alojamientos disponibles: {procesamiento['resumen']['alojamientos_disponibles']}")
        
        print(f"\n⏳ ESTADO: Pendiente de revisión admin")
        print(f"📋 El admin puede ver toda la información en el Panel de Revisión")
        print("=" * 60)
        
        return {
            'exito': True,
            'estudiante_id': estudiante_id,
            'estado': 'procesado_automaticamente',
            'registro': registro,
            'procesamiento': procesamiento['resumen'],
            'mensaje': 'Flujo completado hasta revisión admin. Use panel_revision_admin.py para revisar y aprobar.',
            'siguiente_paso': 'Admin debe revisar en panel_revision_admin.obtener_estudiantes_pendientes_revision()'
        }


# Funciones auxiliares para tareas automáticas
def tarea_diaria_sincronizar_cursos():
    """Sincroniza cursos de todas las escuelas (ejecutar diariamente)"""
    from modules.cursos import GestorCursos
    resultados = GestorCursos.sincronizar_cursos_todas_escuelas()
    print(f"✅ Sincronización de cursos: {resultados}")
    return resultados


def tarea_diaria_alertas():
    """Genera alertas y envía notificaciones (ejecutar diariamente)"""
    from modules.notificaciones import tarea_diaria_alertas
    resultados = tarea_diaria_alertas()
    print(f"✅ Alertas y notificaciones: {resultados}")
    return resultados


def tarea_diaria_alquileres():
    """Procesa alertas de pagos de alquiler (ejecutar diariamente)"""
    from modules.alojamiento import GestorAlojamiento
    alertas = GestorAlojamiento.alertas_alquiler()
    
    # Enviar notificaciones por cada alerta
    for alerta in alertas:
        SistemaNotificaciones.notificar_estudiante(
            alerta['estudiante_id'],
            alerta['mensaje'],
            alerta['titulo'],
            canales=['telegram', 'email'],
            prioridad=alerta['prioridad']
        )
    
    print(f"✅ Alertas de alquiler: {len(alertas)} enviadas")
    return {'alertas_enviadas': len(alertas)}


def generar_reporte_semanal():
    """Genera reporte semanal para administradores (ejecutar semanalmente)"""
    reporte = PanelAdministrativo.generar_reporte_mensual()
    
    # Enviar a administradores
    resumen = reporte['resumen_ejecutivo']
    mensaje = f"""
📊 **REPORTE SEMANAL**

**Estudiantes:**
• Total: {resumen['total_estudiantes']}
• Nuevos: {resumen['nuevos_este_mes']}
• Visas aprobadas: {resumen['visas_aprobadas']} ({resumen['tasa_aprobacion']}%)

**Financiero:**
• Ingresos mes: {resumen['ingresos_mes']}€

**Alertas:**
• Urgentes: {resumen['alertas_urgentes']}
• Requieren atención: {resumen['estudiantes_requieren_atencion']}

Dashboard completo disponible en el panel administrativo.
"""
    
    import config
    for admin_id in config.ADMIN_USER_IDS:
        SistemaNotificaciones._enviar_telegram(admin_id, "📊 Reporte Semanal", mensaje)
    
    return reporte
