"""
Módulo de gestión de estudiantes
Registro, asignación de cursos, checklist de documentos, seguimiento de fechas
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database.models import get_db

Base = declarative_base()


class Estudiante(Base):
    __tablename__ = 'estudiantes'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    
    # Datos personales
    nombre_completo = Column(String(300), nullable=False)
    numero_pasaporte = Column(String(50), unique=True, nullable=False)
    fecha_nacimiento = Column(DateTime)
    edad = Column(Integer)
    nacionalidad = Column(String(100), default='Cuba')
    ciudad_origen = Column(String(100))
    
    # Datos académicos
    carrera_actual = Column(String(255))
    nivel_educacion = Column(String(100))  # secundaria, universitario, graduado, etc.
    especialidad_interes = Column(String(255))
    nivel_espanol = Column(String(10))  # A1, A2, B1, B2, C1, C2
    
    # Datos de contacto
    email = Column(String(255))
    telefono = Column(String(50))
    telefono_emergencia = Column(String(50))
    contacto_emergencia_nombre = Column(String(255))
    
    # Asignación de curso
    curso_asignado_id = Column(Integer, ForeignKey('cursos.id'))
    estado_inscripcion = Column(String(50), default='pendiente')  # pendiente, inscrito, rechazado, completado
    fecha_inscripcion = Column(DateTime)
    
    # Estado de visa
    estado_visa = Column(String(50), default='no_iniciado')  # no_iniciado, documentos, cita_agendada, aprobado, rechazado
    fecha_cita_consulado = Column(DateTime)
    numero_expediente = Column(String(100))
    
    # Estados de revisión admin (flujo semi-automatizado)
    estado_procesamiento = Column(String(50), default='registrado')  # registrado, procesado_automaticamente, pendiente_revision_admin, aprobado_admin, rechazado_admin, enviado_estudiante
    fecha_procesamiento_automatico = Column(DateTime)  # Cuando el bot terminó de procesar
    fecha_revision_admin = Column(DateTime)  # Cuando admin revisó
    admin_revisor_id = Column(Integer)  # ID del admin que revisó
    notas_admin = Column(Text)  # Notas u observaciones del admin
    modificaciones_admin = Column(JSON)  # Cambios realizados por admin antes de enviar
    
    # Documentos
    documentos_completados = Column(JSON, default=[])
    documentos_pendientes = Column(JSON, default=[])
    fecha_ultimo_documento = Column(DateTime)
    
    # Situación económica
    tiene_fondos_propios = Column(Boolean, default=False)
    tiene_patrocinador = Column(Boolean, default=False)
    patrocinador_id = Column(Integer, ForeignKey('patrocinadores.id'))
    monto_fondos_disponibles = Column(Float)
    
    # Alojamiento
    necesita_alojamiento = Column(Boolean, default=True)
    alojamiento_asignado_id = Column(Integer, ForeignKey('alojamientos.id'))
    
    # Seguimiento
    notas = Column(Text)
    agente_asignado = Column(String(255))  # Nombre del agente de la agencia
    prioridad = Column(String(20), default='normal')  # baja, normal, alta, urgente
    
    # Fechas importantes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DocumentoEstudiante(Base):
    __tablename__ = 'documentos_estudiante'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    tipo_documento = Column(String(100))  # pasaporte, carta_aceptacion, fondos, seguro, etc.
    nombre_archivo = Column(String(500))
    ruta_archivo = Column(Text)
    estado = Column(String(50), default='pendiente')  # pendiente, revision, aprobado, rechazado
    fecha_subida = Column(DateTime, default=datetime.utcnow)
    fecha_expiracion = Column(DateTime)
    notas = Column(Text)
    validado_por = Column(String(255))


class EventoEstudiante(Base):
    __tablename__ = 'eventos_estudiante'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    tipo_evento = Column(String(100))  # cita_consulado, entrega_documentos, pago, reunion, etc.
    titulo = Column(String(255))
    descripcion = Column(Text)
    fecha_evento = Column(DateTime)
    recordatorio_dias_antes = Column(Integer, default=3)
    completado = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class GestorEstudiantes:
    """Gestor principal de estudiantes"""
    
    @staticmethod
    def registrar_estudiante(datos_personales: Dict) -> Estudiante:
        """
        Registra un nuevo estudiante con sus datos personales
        
        Args:
            datos_personales: Diccionario con información del estudiante
            
        Returns:
            Objeto Estudiante creado
        """
        db = get_db()
        
        # Verificar si ya existe
        existe = db.query(Estudiante).filter(
            Estudiante.numero_pasaporte == datos_personales['numero_pasaporte']
        ).first()
        
        if existe:
            raise ValueError(f"Estudiante con pasaporte {datos_personales['numero_pasaporte']} ya existe")
        
        # Crear estudiante
        estudiante = Estudiante(**datos_personales)
        db.add(estudiante)
        db.commit()
        db.refresh(estudiante)
        
        # Crear checklist inicial de documentos
        GestorEstudiantes.checklist_documentos(estudiante.id)
        
        return estudiante
    
    @staticmethod
    def obtener_estudiante(estudiante_id: int = None, telegram_id: int = None, pasaporte: str = None) -> Optional[Estudiante]:
        """Obtiene un estudiante por ID, telegram_id o pasaporte"""
        db = get_db()
        
        if estudiante_id:
            return db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
        elif telegram_id:
            return db.query(Estudiante).filter(Estudiante.telegram_id == telegram_id).first()
        elif pasaporte:
            return db.query(Estudiante).filter(Estudiante.numero_pasaporte == pasaporte).first()
        
        return None
    
    @staticmethod
    def asignar_curso(estudiante_id: int, curso_id: int = None, auto_sugerir: bool = True) -> Dict:
        """
        Asigna un curso a un estudiante o sugiere cursos relevantes
        
        Args:
            estudiante_id: ID del estudiante
            curso_id: ID del curso específico a asignar
            auto_sugerir: Si es True, sugiere cursos relevantes basados en perfil
            
        Returns:
            Diccionario con resultado de la asignación o lista de sugerencias
        """
        from modules.cursos import GestorCursos
        
        db = get_db()
        estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
        
        if not estudiante:
            return {'error': 'Estudiante no encontrado'}
        
        if curso_id:
            # Asignar curso específico
            curso = GestorCursos.obtener_curso_por_id(curso_id)
            if not curso:
                return {'error': 'Curso no encontrado'}
            
            estudiante.curso_asignado_id = curso_id
            estudiante.fecha_inscripcion = datetime.utcnow()
            estudiante.estado_inscripcion = 'inscrito'
            db.commit()
            
            # Crear evento de inicio de curso
            evento = EventoEstudiante(
                estudiante_id=estudiante_id,
                tipo_evento='inicio_curso',
                titulo=f'Inicio del curso: {curso.nombre}',
                descripcion=f'Fecha de inicio del curso en {curso.escuela}',
                fecha_evento=curso.fecha_inicio if curso.fecha_inicio else datetime.utcnow() + timedelta(days=30),
                recordatorio_dias_antes=7
            )
            db.add(evento)
            db.commit()
            
            return {
                'exito': True,
                'mensaje': f'Curso {curso.nombre} asignado exitosamente',
                'curso': curso
            }
        
        elif auto_sugerir:
            # Sugerir cursos basados en perfil del estudiante
            cursos_sugeridos = GestorCursos.filtrar_cursos(
                especialidad=estudiante.especialidad_interes,
                nivel_idioma=estudiante.nivel_espanol
            )
            
            # Ordenar por relevancia (se puede mejorar con ML)
            return {
                'sugerencias': cursos_sugeridos[:5],
                'mensaje': f'Se encontraron {len(cursos_sugeridos)} cursos relevantes'
            }
        
        return {'error': 'Debe proporcionar curso_id o activar auto_sugerir'}
    
    @staticmethod
    def checklist_documentos(estudiante_id: int) -> Dict:
        """
        Genera checklist automático de documentos para visa según perfil del estudiante
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Diccionario con checklist personalizado
        """
        db = get_db()
        estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
        
        if not estudiante:
            return {'error': 'Estudiante no encontrado'}
        
        # Documentos base obligatorios para todos
        documentos_obligatorios = [
            {
                'tipo': 'pasaporte',
                'nombre': 'Pasaporte válido',
                'descripcion': 'Pasaporte vigente con mínimo 6 meses de validez',
                'requisitos': ['Original', 'Copia de todas las páginas', 'Vigente +6 meses'],
                'urgente': True
            },
            {
                'tipo': 'carta_aceptacion',
                'nombre': 'Carta de aceptación de la universidad/escuela',
                'descripcion': 'Original firmada y sellada por la institución',
                'requisitos': ['Original', 'Firmada', 'Sellada', 'Incluye duración y costo'],
                'urgente': True
            },
            {
                'tipo': 'certificado_antecedentes',
                'nombre': 'Certificado de antecedentes penales',
                'descripcion': 'Emitido por autoridades cubanas',
                'requisitos': ['Apostillado', 'Máximo 3 meses de antigüedad', 'Traducido al español (si aplica)'],
                'urgente': True
            },
            {
                'tipo': 'certificado_medico',
                'nombre': 'Certificado médico',
                'descripcion': 'Certifica que no padeces enfermedades cuarentenables',
                'requisitos': ['Firmado por médico', 'Máximo 3 meses antigüedad'],
                'urgente': True
            },
            {
                'tipo': 'seguro_medico',
                'nombre': 'Seguro médico internacional',
                'descripcion': 'Cobertura mínima 30,000€',
                'requisitos': ['Cobertura: 30,000€', 'Válido en España', 'Incluye repatriación'],
                'urgente': True
            },
            {
                'tipo': 'fotos',
                'nombre': 'Fotografías tamaño carnet',
                'descripcion': '2 fotos recientes fondo blanco',
                'requisitos': ['2 fotos', '35x45mm', 'Fondo blanco', 'Recientes (últimos 6 meses)'],
                'urgente': False
            },
            {
                'tipo': 'formulario_visa',
                'nombre': 'Formulario de solicitud de visa',
                'descripcion': 'Formulario oficial del consulado español',
                'requisitos': ['Completado a máquina o letra imprenta', 'Firmado'],
                'urgente': False
            }
        ]
        
        # Documentos financieros (depende si tiene patrocinador o fondos propios)
        if estudiante.tiene_patrocinador:
            documentos_obligatorios.append({
                'tipo': 'carta_patrocinio',
                'nombre': 'Carta de patrocinio',
                'descripcion': 'Carta del patrocinador comprometiéndose a cubrir gastos',
                'requisitos': [
                    'Firmada y notariada',
                    'Incluye datos del patrocinador',
                    'Compromiso de manutención completa',
                    'Extractos bancarios del patrocinador (últimos 6 meses)'
                ],
                'urgente': True
            })
            documentos_obligatorios.append({
                'tipo': 'relacion_patrocinador',
                'nombre': 'Prueba de relación con patrocinador',
                'descripcion': 'Certificado que demuestre parentesco o relación',
                'requisitos': ['Acta de nacimiento', 'Documentos que prueben relación'],
                'urgente': True
            })
        else:
            documentos_obligatorios.append({
                'tipo': 'extractos_bancarios',
                'nombre': 'Extractos bancarios propios',
                'descripcion': 'Últimos 6 meses de movimientos',
                'requisitos': [
                    '6 meses completos',
                    'Saldo suficiente (600€/mes)',
                    'Sellados por el banco'
                ],
                'urgente': True
            })
        
        # Documentos recomendados
        documentos_recomendados = [
            {
                'tipo': 'carta_motivacion',
                'nombre': 'Carta de motivación',
                'descripcion': 'Explica por qué quieres estudiar en España',
                'beneficio': '+10% probabilidad aprobación'
            },
            {
                'tipo': 'titulos_academicos',
                'nombre': 'Títulos académicos previos',
                'descripcion': 'Certificados de estudios anteriores',
                'beneficio': '+8% probabilidad'
            },
            {
                'tipo': 'certificado_idioma',
                'nombre': 'Certificado de nivel de español',
                'descripcion': 'DELE, SIELE o similar',
                'beneficio': '+15% probabilidad'
            }
        ]
        
        # Guardar documentos pendientes
        estudiante.documentos_pendientes = [doc['tipo'] for doc in documentos_obligatorios]
        estudiante.documentos_completados = []
        db.commit()
        
        return {
            'obligatorios': documentos_obligatorios,
            'recomendados': documentos_recomendados,
            'total_obligatorios': len(documentos_obligatorios),
            'total_recomendados': len(documentos_recomendados),
            'completados': 0,
            'pendientes': len(documentos_obligatorios),
            'porcentaje_completado': 0
        }
    
    @staticmethod
    def marcar_documento_completado(estudiante_id: int, tipo_documento: str, ruta_archivo: str = None) -> Dict:
        """
        Marca un documento como completado
        
        Args:
            estudiante_id: ID del estudiante
            tipo_documento: Tipo de documento completado
            ruta_archivo: Ruta del archivo subido (opcional)
            
        Returns:
            Diccionario con estado actualizado
        """
        db = get_db()
        estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
        
        if not estudiante:
            return {'error': 'Estudiante no encontrado'}
        
        # Actualizar listas
        if tipo_documento in estudiante.documentos_pendientes:
            estudiante.documentos_pendientes.remove(tipo_documento)
        
        if tipo_documento not in estudiante.documentos_completados:
            estudiante.documentos_completados.append(tipo_documento)
        
        estudiante.fecha_ultimo_documento = datetime.utcnow()
        
        # Registrar documento en tabla separada
        if ruta_archivo:
            doc = DocumentoEstudiante(
                estudiante_id=estudiante_id,
                tipo_documento=tipo_documento,
                ruta_archivo=ruta_archivo,
                estado='revision'
            )
            db.add(doc)
        
        db.commit()
        
        # Calcular progreso
        total = len(estudiante.documentos_completados) + len(estudiante.documentos_pendientes)
        porcentaje = (len(estudiante.documentos_completados) / total * 100) if total > 0 else 0
        
        return {
            'exito': True,
            'completados': len(estudiante.documentos_completados),
            'pendientes': len(estudiante.documentos_pendientes),
            'porcentaje': porcentaje,
            'mensaje': f'Documento {tipo_documento} marcado como completado'
        }
    
    @staticmethod
    def seguimiento_fechas(estudiante_id: int) -> List[Dict]:
        """
        Obtiene todas las fechas importantes y recordatorios del estudiante
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Lista de eventos ordenados por fecha
        """
        db = get_db()
        
        eventos = db.query(EventoEstudiante).filter(
            EventoEstudiante.estudiante_id == estudiante_id,
            EventoEstudiante.completado == False
        ).order_by(EventoEstudiante.fecha_evento).all()
        
        eventos_formateados = []
        for evento in eventos:
            dias_restantes = (evento.fecha_evento - datetime.utcnow()).days
            
            eventos_formateados.append({
                'id': evento.id,
                'tipo': evento.tipo_evento,
                'titulo': evento.titulo,
                'descripcion': evento.descripcion,
                'fecha': evento.fecha_evento,
                'dias_restantes': dias_restantes,
                'urgente': dias_restantes <= evento.recordatorio_dias_antes,
                'completado': evento.completado
            })
        
        return eventos_formateados
    
    @staticmethod
    def crear_evento(estudiante_id: int, tipo_evento: str, titulo: str, fecha_evento: datetime, descripcion: str = '', dias_recordatorio: int = 3) -> EventoEstudiante:
        """Crea un nuevo evento para el estudiante"""
        db = get_db()
        
        evento = EventoEstudiante(
            estudiante_id=estudiante_id,
            tipo_evento=tipo_evento,
            titulo=titulo,
            descripcion=descripcion,
            fecha_evento=fecha_evento,
            recordatorio_dias_antes=dias_recordatorio
        )
        
        db.add(evento)
        db.commit()
        db.refresh(evento)
        
        return evento
    
    @staticmethod
    def marcar_evento_completado(evento_id: int) -> bool:
        """Marca un evento como completado"""
        db = get_db()
        evento = db.query(EventoEstudiante).filter(EventoEstudiante.id == evento_id).first()
        
        if evento:
            evento.completado = True
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def obtener_eventos_proximos(dias: int = 7) -> List[EventoEstudiante]:
        """Obtiene todos los eventos próximos en los próximos X días"""
        db = get_db()
        fecha_limite = datetime.utcnow() + timedelta(days=dias)
        
        eventos = db.query(EventoEstudiante).filter(
            EventoEstudiante.fecha_evento <= fecha_limite,
            EventoEstudiante.fecha_evento >= datetime.utcnow(),
            EventoEstudiante.completado == False
        ).order_by(EventoEstudiante.fecha_evento).all()
        
        return eventos
    
    @staticmethod
    def actualizar_estado_visa(estudiante_id: int, nuevo_estado: str, fecha_cita: datetime = None) -> Dict:
        """
        Actualiza el estado de la visa del estudiante
        
        Args:
            estudiante_id: ID del estudiante
            nuevo_estado: Nuevo estado (no_iniciado, documentos, cita_agendada, aprobado, rechazado)
            fecha_cita: Fecha de cita en consulado si aplica
            
        Returns:
            Diccionario con confirmación
        """
        db = get_db()
        estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
        
        if not estudiante:
            return {'error': 'Estudiante no encontrado'}
        
        estudiante.estado_visa = nuevo_estado
        
        if fecha_cita:
            estudiante.fecha_cita_consulado = fecha_cita
            
            # Crear evento de cita
            GestorEstudiantes.crear_evento(
                estudiante_id=estudiante_id,
                tipo_evento='cita_consulado',
                titulo='Cita en Consulado de España',
                fecha_evento=fecha_cita,
                descripcion='Cita para entrevista de visa de estudiante',
                dias_recordatorio=3
            )
        
        db.commit()
        
        return {
            'exito': True,
            'estado_actual': nuevo_estado,
            'mensaje': f'Estado actualizado a: {nuevo_estado}'
        }
    
    @staticmethod
    def listar_estudiantes(filtros: Dict = None) -> List[Estudiante]:
        """
        Lista estudiantes con filtros opcionales
        
        Args:
            filtros: Diccionario con filtros (estado_visa, estado_inscripcion, prioridad, etc.)
            
        Returns:
            Lista de estudiantes que cumplen los filtros
        """
        db = get_db()
        query = db.query(Estudiante)
        
        if filtros:
            if 'estado_visa' in filtros:
                query = query.filter(Estudiante.estado_visa == filtros['estado_visa'])
            if 'estado_inscripcion' in filtros:
                query = query.filter(Estudiante.estado_inscripcion == filtros['estado_inscripcion'])
            if 'prioridad' in filtros:
                query = query.filter(Estudiante.prioridad == filtros['prioridad'])
            if 'necesita_alojamiento' in filtros:
                query = query.filter(Estudiante.necesita_alojamiento == filtros['necesita_alojamiento'])
        
        return query.all()
