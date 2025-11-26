"""
Ejemplos de uso de todos los módulos de la Agencia Educativa
"""

from datetime import datetime, timedelta


def ejemplo_completo():
    """Ejemplo del flujo completo de un estudiante"""
    
    print("=" * 60)
    print("EJEMPLO: FLUJO COMPLETO DE ESTUDIANTE")
    print("=" * 60)
    
    # ===== PASO 1: REGISTRO =====
    print("\n1️⃣ REGISTRANDO NUEVO ESTUDIANTE...")
    
    from modules.flujo_principal import FlujoPrincipal
    
    datos_estudiante = {
        'telegram_id': 987654321,
        'nombre_completo': 'Ana María López',
        'numero_pasaporte': 'CB123456',
        'fecha_nacimiento': datetime(1998, 5, 15),
        'edad': 27,
        'nacionalidad': 'Cuba',
        'ciudad_origen': 'La Habana',
        'carrera_actual': 'Licenciatura en Biología',
        'nivel_educacion': 'universitario',
        'especialidad_interes': 'Biotecnología',
        'nivel_espanol': 'B2',
        'email': 'ana.lopez@example.com',
        'telefono': '+53 5 123 4567',
        'telefono_emergencia': '+53 7 234 5678',
        'contacto_emergencia_nombre': 'María López (Madre)'
    }
    
    resultado = FlujoPrincipal.registrar_nuevo_estudiante(datos_estudiante)
    
    if resultado['exito']:
        estudiante_id = resultado['estudiante_id']
        print(f"✅ Estudiante registrado con ID: {estudiante_id}")
        print(f"📋 Checklist generado con {resultado['checklist']['total_obligatorios']} documentos obligatorios")
    else:
        print(f"❌ Error: {resultado.get('error')}")
        return
    
    # ===== PASO 2: BUSCAR Y ASIGNAR CURSO =====
    print("\n2️⃣ BUSCANDO CURSOS RELEVANTES...")
    
    from modules.cursos import GestorCursos
    
    cursos_sugeridos = GestorCursos.filtrar_cursos(
        especialidad='biotecnologia',
        nivel_idioma='b2',
        precio_max=10000
    )
    
    print(f"✅ Se encontraron {len(cursos_sugeridos)} cursos relevantes")
    
    if cursos_sugeridos:
        curso_seleccionado = cursos_sugeridos[0]
        print(f"\nCurso seleccionado: {curso_seleccionado.nombre}")
        print(f"🏫 Escuela: {curso_seleccionado.escuela}")
        print(f"💰 Precio: {curso_seleccionado.precio}€")
        print(f"⏱️ Duración: {curso_seleccionado.duracion_meses} meses")
        
        # Asignar curso
        asignacion = FlujoPrincipal.sugerir_y_asignar_curso(
            estudiante_id, 
            curso_seleccionado.id
        )
        
        if asignacion.get('exito'):
            print("✅ Curso asignado exitosamente")
    
    # ===== PASO 3: REGISTRAR PATROCINADOR =====
    print("\n3️⃣ REGISTRANDO PATROCINADOR...")
    
    from modules.fondos import GestorFondos
    
    datos_patrocinador = {
        'nombre_completo': 'Roberto López García',
        'numero_identificacion': '12345678X',
        'nacionalidad': 'España',
        'fecha_nacimiento': datetime(1965, 3, 20),
        'relacion_estudiante': 'Tío',
        'pais_residencia': 'España',
        'ciudad_residencia': 'Madrid',
        'email': 'roberto.lopez@example.com',
        'telefono': '+34 600 123 456',
        'direccion_completa': 'Calle Gran Vía 123, 28013 Madrid, España',
        'ocupacion': 'Ingeniero Civil',
        'empresa': 'Construcciones López S.L.',
        'ingresos_mensuales': 3500,
        'capacidad_patrocinio': 18000
    }
    
    patrocinador = GestorFondos.registrar_patrocinador(
        datos_patrocinador, 
        estudiante_id=estudiante_id
    )
    
    print(f"✅ Patrocinador registrado: {patrocinador.nombre_completo}")
    print(f"💰 Capacidad de patrocinio: {patrocinador.capacidad_patrocinio:,.2f}€")
    
    # Generar carta de patrocinio
    print("\n📄 Generando carta de patrocinio en PDF...")
    
    try:
        pdf_bytes = GestorFondos.generar_carta_patrocinio(
            patrocinador.id,
            estudiante_id
        )
        
        filename = f'carta_patrocinio_ana_lopez.pdf'
        with open(filename, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ Carta de patrocinio guardada: {filename}")
    except Exception as e:
        print(f"⚠️ Error generando carta: {e}")
    
    # ===== PASO 4: VERIFICAR FONDOS =====
    print("\n4️⃣ VERIFICANDO FONDOS ECONÓMICOS...")
    
    verificacion = FlujoPrincipal.verificar_y_gestionar_fondos(estudiante_id)
    
    print(f"Estado: {verificacion['estado']}")
    print(f"Fondos disponibles: {verificacion['fondos_disponibles']:,.2f}€")
    print(f"Fondos requeridos: {verificacion['fondos_minimos_requeridos']:,.2f}€")
    print(f"Cobertura: {verificacion['porcentaje_cobertura']:.1f}%")
    
    if verificacion['porcentaje_cobertura'] >= 100:
        print("✅ Fondos suficientes para proceder con visa")
    else:
        print(f"⚠️ Déficit: {verificacion['deficit']:,.2f}€")
    
    # ===== PASO 5: BUSCAR ALOJAMIENTO =====
    print("\n5️⃣ BUSCANDO ALOJAMIENTO...")
    
    from modules.alojamiento import GestorAlojamiento
    
    alojamientos = GestorAlojamiento.buscar_alojamientos(
        ciudad='Madrid',
        precio_max=600,
        tipo='habitacion_individual'
    )
    
    print(f"✅ Se encontraron {len(alojamientos)} alojamientos disponibles")
    
    if alojamientos:
        alojamiento_seleccionado = alojamientos[0]
        print(f"\nAlojamiento seleccionado:")
        print(f"📍 {alojamiento_seleccionado.direccion}")
        print(f"💰 {alojamiento_seleccionado.precio_mensual}€/mes")
        print(f"🛏️ {alojamiento_seleccionado.num_habitaciones} habitaciones")
        
        # Asignar alojamiento
        asignacion_aloj = GestorAlojamiento.asignar_alojamiento(
            estudiante_id=estudiante_id,
            alojamiento_id=alojamiento_seleccionado.id,
            fecha_inicio=datetime(2026, 2, 1),
            duracion_meses=12
        )
        
        print(f"✅ Alojamiento asignado desde {asignacion_aloj.fecha_inicio.strftime('%d/%m/%Y')}")
    
    # ===== PASO 6: MARCAR DOCUMENTOS =====
    print("\n6️⃣ COMPLETANDO DOCUMENTOS...")
    
    from modules.estudiantes import GestorEstudiantes
    
    documentos_completar = ['pasaporte', 'carta_aceptacion', 'seguro_medico']
    
    for doc in documentos_completar:
        resultado_doc = GestorEstudiantes.marcar_documento_completado(
            estudiante_id,
            doc,
            ruta_archivo=f'/uploads/{estudiante_id}/{doc}.pdf'
        )
        print(f"✅ {doc}: {resultado_doc['porcentaje']:.0f}% completado")
    
    # ===== PASO 7: PROGRAMAR CITA CONSULADO =====
    print("\n7️⃣ PROGRAMANDO CITA EN CONSULADO...")
    
    fecha_cita = datetime.now() + timedelta(days=30)
    
    GestorEstudiantes.actualizar_estado_visa(
        estudiante_id,
        'cita_agendada',
        fecha_cita=fecha_cita
    )
    
    print(f"✅ Cita programada para: {fecha_cita.strftime('%d/%m/%Y %H:%M')}")
    
    # ===== PASO 8: GENERAR REPORTE FINAL =====
    print("\n8️⃣ GENERANDO REPORTE FINAL...")
    
    reporte = FlujoPrincipal.generar_y_enviar_reportes(estudiante_id)
    
    print(f"📊 Probabilidad de aprobación: {reporte['prediccion']['probability']:.0f}%")
    print(f"📄 Documentos completados: {reporte['documentos_completados']}")
    print(f"📋 Documentos pendientes: {reporte['documentos_pendientes']}")
    
    print("\n" + "=" * 60)
    print("✅ FLUJO COMPLETO EJECUTADO EXITOSAMENTE")
    print("=" * 60)


def ejemplo_panel_administrativo():
    """Ejemplo de uso del panel administrativo"""
    
    print("\n" + "=" * 60)
    print("EJEMPLO: PANEL ADMINISTRATIVO")
    print("=" * 60)
    
    from modules.admin_panel import PanelAdministrativo
    
    # Dashboard completo
    print("\n📊 GENERANDO DASHBOARD...")
    dashboard = PanelAdministrativo.dashboard()
    
    print("\n📈 RESUMEN EJECUTIVO:")
    print(f"• Total estudiantes: {dashboard['resumen']['total_estudiantes']}")
    print(f"• Nuevos este mes: {dashboard['resumen']['estudiantes_nuevos_mes']}")
    print(f"• Visas aprobadas: {dashboard['resumen']['visas_aprobadas']}")
    print(f"• Tasa de aprobación: {dashboard['resumen']['tasa_aprobacion']}%")
    print(f"• Alertas urgentes: {dashboard['resumen']['alertas_urgentes']}")
    
    print("\n🎓 CURSOS:")
    print(f"• Total cursos activos: {dashboard['cursos']['total_activos']}")
    print(f"• Estudiantes inscritos: {dashboard['cursos']['estudiantes_inscritos']}")
    
    print("\n🏠 ALOJAMIENTO:")
    print(f"• Total alojamientos: {dashboard['alojamiento']['total']}")
    print(f"• Disponibles: {dashboard['alojamiento']['disponibles']}")
    print(f"• Ocupados: {dashboard['alojamiento']['ocupados']}")
    
    print("\n💰 PAGOS:")
    print(f"• Pendientes: {dashboard['pagos']['pendientes']}")
    print(f"• Atrasados: {dashboard['pagos']['atrasados']}")
    print(f"• Monto pendiente: {dashboard['pagos']['monto_total_pendiente']:,.2f}€")
    
    # Estudiantes que requieren atención
    print("\n⚠️ ESTUDIANTES QUE REQUIEREN ATENCIÓN:")
    atencion = PanelAdministrativo.estudiantes_requieren_atencion()
    
    for est in atencion[:5]:  # Primeros 5
        print(f"\n• {est['nombre']}")
        print(f"  Razón: {est['razon']}")
        print(f"  Prioridad: {est['prioridad']}")
        print(f"  Acción: {est['accion_sugerida']}")
    
    # Estadísticas por especialidad
    print("\n📚 ESTADÍSTICAS POR ESPECIALIDAD:")
    especialidades = PanelAdministrativo.estadisticas_por_especialidad()
    
    for esp in especialidades[:3]:  # Top 3
        print(f"\n• {esp['especialidad']}")
        print(f"  Total: {esp['total_estudiantes']}")
        print(f"  Aprobados: {esp['visas_aprobadas']}")
        print(f"  Tasa éxito: {esp['tasa_exito']}%")


def ejemplo_tareas_automaticas():
    """Ejemplo de tareas automáticas programadas"""
    
    print("\n" + "=" * 60)
    print("EJEMPLO: TAREAS AUTOMÁTICAS")
    print("=" * 60)
    
    from modules.flujo_principal import (
        tarea_diaria_sincronizar_cursos,
        tarea_diaria_alertas,
        tarea_diaria_alquileres,
        generar_reporte_semanal
    )
    
    print("\n🔄 EJECUTANDO TAREAS DIARIAS...")
    
    # 1. Sincronizar cursos
    print("\n1. Sincronizando cursos...")
    try:
        resultado_cursos = tarea_diaria_sincronizar_cursos()
        print(f"✅ Escuelas sincronizadas: {resultado_cursos['exitosas']}")
        print(f"✅ Cursos nuevos: {resultado_cursos['cursos_nuevos']}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    
    # 2. Generar alertas
    print("\n2. Generando alertas...")
    try:
        resultado_alertas = tarea_diaria_alertas()
        print(f"✅ Alertas generadas: {resultado_alertas['alertas']['total_alertas']}")
        print(f"✅ Recordatorios enviados: {resultado_alertas['recordatorios']['recordatorios_enviados']}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    
    # 3. Alertas de alquileres
    print("\n3. Procesando alertas de alquiler...")
    try:
        resultado_alquileres = tarea_diaria_alquileres()
        print(f"✅ Alertas enviadas: {resultado_alquileres['alertas_enviadas']}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    
    print("\n📊 GENERANDO REPORTE SEMANAL...")
    try:
        reporte_semanal = generar_reporte_semanal()
        print("✅ Reporte semanal generado y enviado a administradores")
    except Exception as e:
        print(f"⚠️ Error: {e}")


def ejemplo_notificaciones():
    """Ejemplo del sistema de notificaciones"""
    
    print("\n" + "=" * 60)
    print("EJEMPLO: SISTEMA DE NOTIFICACIONES")
    print("=" * 60)
    
    from modules.notificaciones import SistemaNotificaciones
    
    estudiante_id = 1  # Usar ID real
    
    # Notificación simple
    print("\n📧 Enviando notificación simple...")
    resultado = SistemaNotificaciones.notificar_estudiante(
        estudiante_id=estudiante_id,
        mensaje="""
Tu solicitud de visa está avanzando correctamente.

📋 Próximos pasos:
1. Completa los documentos pendientes
2. Prepárate para la entrevista
3. Revisa la fecha de tu cita

¡Estamos aquí para ayudarte!
""",
        titulo="📬 Actualización de tu proceso",
        canales=['telegram', 'email'],
        prioridad='normal'
    )
    
    print(f"✅ Enviado por: {', '.join(resultado['exitosos'])}")
    if resultado['fallidos']:
        print(f"❌ Falló: {', '.join(resultado['fallidos'])}")
    
    # Generar alertas internas
    print("\n⚠️ Generando alertas para administradores...")
    alertas = SistemaNotificaciones.alertas_internas()
    print(f"✅ {alertas['total_alertas']} alertas generadas")


if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════╗
║   🎓 BOT AGENCIA EDUCATIVA - EJEMPLOS DE USO             ║
╚═══════════════════════════════════════════════════════════╝
    
Selecciona un ejemplo:

1. Flujo completo de estudiante
2. Panel administrativo
3. Tareas automáticas
4. Sistema de notificaciones
5. Ejecutar todos

""")
    
    opcion = input("Opción (1-5): ").strip()
    
    if opcion == '1':
        ejemplo_completo()
    elif opcion == '2':
        ejemplo_panel_administrativo()
    elif opcion == '3':
        ejemplo_tareas_automaticas()
    elif opcion == '4':
        ejemplo_notificaciones()
    elif opcion == '5':
        ejemplo_completo()
        ejemplo_panel_administrativo()
        ejemplo_tareas_automaticas()
        ejemplo_notificaciones()
    else:
        print("Opción no válida")
    
    print("\n✅ EJEMPLOS COMPLETADOS\n")
