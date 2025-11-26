"""
Ejemplo completo del FLUJO SEMI-AUTOMATIZADO
Bot Agencia Educativa

FLUJO:
1. Estudiante registra todos sus datos
2. Bot procesa automáticamente (cursos, fondos, documentos, alojamiento)
3. Admin revisa en panel de control
4. Admin aprueba/modifica
5. Admin envía manualmente al estudiante
"""

from datetime import datetime
from modules.flujo_principal import FlujoPrincipal
from modules.panel_revision_admin import PanelRevisionAdmin


def ejemplo_completo_flujo_semi_automatizado():
    """
    Ejemplo paso a paso del flujo semi-automatizado completo
    """
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║     🎓 FLUJO SEMI-AUTOMATIZADO - AGENCIA EDUCATIVA          ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # ===================================================================
    # PARTE 1: ESTUDIANTE REGISTRA TODOS SUS DATOS
    # ===================================================================
    print("\n" + "="*60)
    print("PARTE 1: REGISTRO DEL ESTUDIANTE")
    print("="*60)
    print("\n📝 El estudiante proporciona TODA su información...")
    
    datos_estudiante = {
        # Datos personales
        'telegram_id': 123456789,
        'nombre_completo': 'Carlos Rodríguez Pérez',
        'numero_pasaporte': 'CB987654',
        'fecha_nacimiento': datetime(1995, 8, 20),
        'edad': 28,
        'nacionalidad': 'Cuba',
        'ciudad_origen': 'Santiago de Cuba',
        
        # Datos académicos
        'carrera_actual': 'Ingeniero en Sistemas',
        'nivel_educacion': 'universitario',
        'especialidad_interes': 'Inteligencia Artificial',
        'nivel_espanol': 'C1',
        
        # Contacto
        'email': 'carlos.rodriguez@example.com',
        'telefono': '+53 5 234 5678',
        'telefono_emergencia': '+53 7 345 6789',
        'contacto_emergencia_nombre': 'Ana Pérez (Madre)',
        
        # Preferencias de curso
        'ciudad_preferida': 'Madrid',
        'duracion_preferida_meses': 12,
        'presupuesto_curso': 8000,
        
        # Situación económica
        'fondos_propios': 5000,
        'tiene_patrocinador': True,
        
        # Alojamiento
        'necesita_alojamiento': True,
        'presupuesto_alojamiento': 500
    }
    
    # ===================================================================
    # PARTE 2: BOT PROCESA TODO AUTOMÁTICAMENTE
    # ===================================================================
    print("\n🤖 Iniciando procesamiento automático del bot...\n")
    
    resultado = FlujoPrincipal.flujo_semi_automatizado(datos_estudiante)
    
    if not resultado['exito']:
        print(f"❌ Error: {resultado.get('error')}")
        return
    
    estudiante_id = resultado['estudiante_id']
    
    print(f"\n✅ Procesamiento completado!")
    print(f"   Estudiante ID: {estudiante_id}")
    print(f"   Estado: {resultado['estado']}")
    
    # ===================================================================
    # PARTE 3: ADMIN REVISA EN PANEL DE CONTROL
    # ===================================================================
    print("\n" + "="*60)
    print("PARTE 3: REVISIÓN POR ADMINISTRADOR")
    print("="*60)
    
    input("\n⏸️  Presiona ENTER para que el admin vea el panel de revisión...")
    
    print("\n👤 Admin abre el panel de revisión...\n")
    
    # Ver todos los estudiantes pendientes
    pendientes = PanelRevisionAdmin.obtener_estudiantes_pendientes_revision()
    
    print(f"📋 Estudiantes pendientes de revisión: {len(pendientes)}")
    
    # Ver panel completo del estudiante
    panel = PanelRevisionAdmin.ver_panel_estudiante(estudiante_id)
    
    print(f"\n📊 PANEL DE REVISIÓN - {panel['estudiante']['nombre_completo']}")
    print("="*60)
    
    print(f"\n📈 RESUMEN:")
    print(f"  • Cursos encontrados: {panel['resumen']['cursos_encontrados']}")
    print(f"  • Documentos completos: {panel['resumen']['documentos_completos']:.0f}%")
    print(f"  • Fondos suficientes: {'✅ Sí' if panel['resumen']['fondos_suficientes'] else '❌ No'}")
    print(f"  • Alojamientos disponibles: {panel['resumen']['alojamientos_disponibles']}")
    
    print(f"\n📚 CURSOS SUGERIDOS:")
    for i, curso in enumerate(panel['detalles']['cursos'][:3], 1):
        print(f"\n  {i}. {curso['nombre']}")
        print(f"     🏫 {curso['escuela']}")
        print(f"     📍 {curso['ciudad']}")
        print(f"     💰 {curso['precio']:,.2f}€")
        print(f"     ⏱️  {curso['duracion_meses']} meses")
        if curso['curso_asignado']:
            print(f"     ⭐ CURSO PRE-SELECCIONADO")
    
    print(f"\n💰 VERIFICACIÓN DE FONDOS:")
    fondos = panel['detalles']['fondos']
    print(f"  • Fondos disponibles: {fondos['fondos_disponibles']:,.2f}€")
    print(f"  • Fondos requeridos: {fondos['fondos_minimos_requeridos']:,.2f}€")
    print(f"  • Cobertura: {fondos['porcentaje_cobertura']:.1f}%")
    print(f"  • Estado: {fondos['estado']}")
    
    if panel['resumen']['alojamientos_disponibles'] > 0:
        print(f"\n🏠 ALOJAMIENTOS SUGERIDOS:")
        for i, aloj in enumerate(panel['detalles']['alojamientos'][:3], 1):
            print(f"\n  {i}. {aloj['tipo'].replace('_', ' ').title()}")
            print(f"     📍 {aloj['direccion']}, {aloj['ciudad']}")
            print(f"     💰 {aloj['precio_mensual']}€/mes")
            print(f"     🛏️  {aloj['num_habitaciones']} habitaciones")
    
    # ===================================================================
    # PARTE 4: ADMIN APRUEBA/MODIFICA
    # ===================================================================
    print("\n" + "="*60)
    print("PARTE 4: DECISIÓN DEL ADMINISTRADOR")
    print("="*60)
    
    input("\n⏸️  Presiona ENTER para que el admin apruebe la información...")
    
    print("\n👤 Admin revisa y aprueba la información...\n")
    
    # Admin puede seleccionar curso específico (opcional)
    curso_seleccionado = panel['detalles']['cursos'][0]['id'] if panel['detalles']['cursos'] else None
    alojamiento_seleccionado = panel['detalles']['alojamientos'][0]['id'] if panel['detalles']['alojamientos'] else None
    
    aprobacion = PanelRevisionAdmin.aprobar_y_preparar_envio(
        estudiante_id=estudiante_id,
        admin_id=1,  # ID del admin
        curso_seleccionado_id=curso_seleccionado,
        alojamiento_seleccionado_id=alojamiento_seleccionado,
        notas_admin="""
        Revisado y aprobado.
        - Curso seleccionado: Opción 1 (mejor relación calidad-precio)
        - Fondos: Verificados con patrocinador
        - Alojamiento: Reserva confirmada
        """
    )
    
    if aprobacion['exito']:
        print(f"✅ APROBACIÓN EXITOSA")
        print(f"   Estado: {aprobacion['estado']}")
        print(f"   Paquete de envío preparado")
    else:
        print(f"❌ Error en aprobación: {aprobacion.get('error')}")
        return
    
    # ===================================================================
    # PARTE 5: ADMIN ENVÍA MANUALMENTE AL ESTUDIANTE
    # ===================================================================
    print("\n" + "="*60)
    print("PARTE 5: ENVÍO MANUAL AL ESTUDIANTE")
    print("="*60)
    
    input("\n⏸️  Presiona ENTER para que el admin envíe la información...")
    
    print("\n👤 Admin envía la información al estudiante...\n")
    
    envio = PanelRevisionAdmin.enviar_informacion_manual(
        estudiante_id=estudiante_id,
        admin_id=1,
        canales=['telegram', 'email'],
        mensaje_personalizado="""
Estimado Carlos,

Hemos procesado tu solicitud y tenemos excelentes noticias.
A continuación encontrarás tu plan personalizado para estudiar en España.

Nuestro equipo está disponible para resolver cualquier duda.

¡Bienvenido a tu nueva aventura educativa! 🇪🇸

Saludos,
Equipo Agencia Educativa
        """
    )
    
    if envio['exito']:
        print(f"✅ INFORMACIÓN ENVIADA EXITOSAMENTE")
        print(f"   Canales: {', '.join(envio['canales_enviados'])}")
        print(f"   Estado final: {envio['estado_final']}")
        print(f"   Fecha envío: {envio['fecha_envio'].strftime('%d/%m/%Y %H:%M')}")
        
        if envio['canales_fallidos']:
            print(f"   ⚠️  Canales fallidos: {', '.join(envio['canales_fallidos'])}")
    else:
        print(f"❌ Error en envío: {envio.get('error')}")
    
    # ===================================================================
    # RESUMEN FINAL
    # ===================================================================
    print("\n" + "="*60)
    print("✅ FLUJO SEMI-AUTOMATIZADO COMPLETADO")
    print("="*60)
    
    print(f"""
📊 RESUMEN DEL PROCESO:

1️⃣  Estudiante registrado: Carlos Rodríguez Pérez
2️⃣  Procesamiento automático completado
3️⃣  Revisión admin realizada
4️⃣  Información aprobada y modificada por admin
5️⃣  Información enviada manualmente al estudiante

🎯 VENTAJAS DEL FLUJO SEMI-AUTOMATIZADO:
   ✅ Bot procesa rápidamente toda la información
   ✅ Admin revisa y valida antes de enviar
   ✅ Admin puede modificar o ajustar lo necesario
   ✅ Control total sobre la comunicación con el estudiante
   ✅ Estudiante recibe información verificada y personalizada

Estado final: ENVIADO AL ESTUDIANTE
""")


def ejemplo_panel_estadisticas():
    """Ver estadísticas del panel de revisión"""
    
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS DEL PANEL DE REVISIÓN")
    print("="*60)
    
    stats = PanelRevisionAdmin.estadisticas_revision()
    
    print(f"""
📈 ESTADO ACTUAL:

• Pendientes de revisión: {stats.get('pendientes_revision', 0)}
• Aprobados (pendiente envío): {stats.get('aprobados_pendiente_envio', 0)}
• Enviados a estudiantes: {stats.get('enviados_estudiante', 0)}
• Rechazados: {stats.get('rechazados', 0)}

Total procesados: {stats.get('total_procesados', 0)}
""")


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║   🤖 BOT AGENCIA EDUCATIVA - FLUJO SEMI-AUTOMATIZADO        ║
║                                                              ║
║   El bot procesa → Admin revisa → Envío manual              ║
╚══════════════════════════════════════════════════════════════╝

Selecciona una opción:

1. Ejecutar flujo completo paso a paso
2. Ver estadísticas del panel
3. Salir

""")
    
    opcion = input("Opción (1-3): ").strip()
    
    if opcion == '1':
        ejemplo_completo_flujo_semi_automatizado()
    elif opcion == '2':
        ejemplo_panel_estadisticas()
    elif opcion == '3':
        print("Saliendo...")
    else:
        print("Opción no válida")
    
    print("\n✅ PROGRAMA FINALIZADO\n")
