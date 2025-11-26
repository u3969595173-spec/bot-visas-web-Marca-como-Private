"""
Sistema de Historial de Cambios y Auditoría
Registra todas las modificaciones realizadas por admins
"""

from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database.models import get_db

Base = declarative_base()


class HistorialModificacion(Base):
    __tablename__ = 'historial_modificaciones'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'), nullable=False)
    admin_id = Column(Integer, nullable=False)
    admin_nombre = Column(String(255))
    
    # Tipo de acción
    tipo_accion = Column(String(50))  # 'edicion', 'aprobacion', 'rechazo', 'envio', 'reasignacion'
    
    # Detalles del cambio
    campo_modificado = Column(String(255))  # Qué campo se modificó
    valor_anterior = Column(Text)  # Valor antes del cambio
    valor_nuevo = Column(Text)  # Valor después del cambio
    
    # Contexto
    motivo = Column(Text)  # Por qué se hizo el cambio
    descripcion = Column(Text)  # Descripción detallada
    metadatos = Column(JSON)  # Información adicional
    
    # Timestamp
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # IP y ubicación (opcional)
    ip_address = Column(String(50))
    user_agent = Column(Text)


class AuditoriaEstudiante:
    """Sistema de auditoría para cambios en estudiantes"""
    
    @staticmethod
    def registrar_cambio(
        estudiante_id: int,
        admin_id: int,
        tipo_accion: str,
        motivo: str = None,
        campo_modificado: str = None,
        valor_anterior: str = None,
        valor_nuevo: str = None,
        descripcion: str = None,
        admin_nombre: str = None,
        metadatos: Dict = None
    ) -> HistorialModificacion:
        """
        Registra un cambio en el historial de auditoría
        
        Args:
            estudiante_id: ID del estudiante modificado
            admin_id: ID del admin que realizó el cambio
            tipo_accion: Tipo de acción (edicion, aprobacion, rechazo, envio)
            motivo: Motivo del cambio
            campo_modificado: Qué campo se modificó
            valor_anterior: Valor antes del cambio
            valor_nuevo: Valor después del cambio
            descripcion: Descripción detallada
            admin_nombre: Nombre del admin
            metadatos: Información adicional en JSON
            
        Returns:
            HistorialModificacion creado
        """
        db = get_db()
        
        try:
            historial = HistorialModificacion(
                estudiante_id=estudiante_id,
                admin_id=admin_id,
                admin_nombre=admin_nombre or f"Admin {admin_id}",
                tipo_accion=tipo_accion,
                campo_modificado=campo_modificado,
                valor_anterior=str(valor_anterior) if valor_anterior is not None else None,
                valor_nuevo=str(valor_nuevo) if valor_nuevo is not None else None,
                motivo=motivo,
                descripcion=descripcion,
                metadatos=metadatos or {},
                fecha=datetime.utcnow()
            )
            
            db.add(historial)
            db.commit()
            db.refresh(historial)
            
            return historial
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def registrar_aprobacion(
        estudiante_id: int,
        admin_id: int,
        admin_nombre: str,
        curso_seleccionado: str = None,
        alojamiento_seleccionado: str = None,
        notas: str = None
    ):
        """Registra la aprobación de un estudiante"""
        
        descripcion = f"Admin {admin_nombre} aprobó la información del estudiante"
        
        metadatos = {
            'curso_seleccionado': curso_seleccionado,
            'alojamiento_seleccionado': alojamiento_seleccionado
        }
        
        return AuditoriaEstudiante.registrar_cambio(
            estudiante_id=estudiante_id,
            admin_id=admin_id,
            admin_nombre=admin_nombre,
            tipo_accion='aprobacion',
            motivo=notas or "Aprobación estándar",
            descripcion=descripcion,
            metadatos=metadatos
        )
    
    @staticmethod
    def registrar_rechazo(
        estudiante_id: int,
        admin_id: int,
        admin_nombre: str,
        motivo_rechazo: str,
        acciones_requeridas: List[str]
    ):
        """Registra el rechazo de un estudiante"""
        
        descripcion = f"Admin {admin_nombre} rechazó la información del estudiante"
        
        metadatos = {
            'acciones_requeridas': acciones_requeridas
        }
        
        return AuditoriaEstudiante.registrar_cambio(
            estudiante_id=estudiante_id,
            admin_id=admin_id,
            admin_nombre=admin_nombre,
            tipo_accion='rechazo',
            motivo=motivo_rechazo,
            descripcion=descripcion,
            metadatos=metadatos
        )
    
    @staticmethod
    def registrar_envio(
        estudiante_id: int,
        admin_id: int,
        admin_nombre: str,
        canales: List[str],
        plantilla_usada: str = None
    ):
        """Registra el envío de información al estudiante"""
        
        descripcion = f"Admin {admin_nombre} envió información al estudiante por: {', '.join(canales)}"
        
        metadatos = {
            'canales': canales,
            'plantilla_usada': plantilla_usada
        }
        
        return AuditoriaEstudiante.registrar_cambio(
            estudiante_id=estudiante_id,
            admin_id=admin_id,
            admin_nombre=admin_nombre,
            tipo_accion='envio',
            descripcion=descripcion,
            metadatos=metadatos
        )
    
    @staticmethod
    def registrar_edicion_campo(
        estudiante_id: int,
        admin_id: int,
        admin_nombre: str,
        campo: str,
        valor_anterior: any,
        valor_nuevo: any,
        motivo: str
    ):
        """Registra la edición de un campo específico"""
        
        descripcion = f"Admin {admin_nombre} modificó {campo}"
        
        return AuditoriaEstudiante.registrar_cambio(
            estudiante_id=estudiante_id,
            admin_id=admin_id,
            admin_nombre=admin_nombre,
            tipo_accion='edicion',
            campo_modificado=campo,
            valor_anterior=valor_anterior,
            valor_nuevo=valor_nuevo,
            motivo=motivo,
            descripcion=descripcion
        )
    
    @staticmethod
    def obtener_historial_estudiante(
        estudiante_id: int,
        limite: int = 50
    ) -> List[HistorialModificacion]:
        """
        Obtiene el historial completo de un estudiante
        
        Args:
            estudiante_id: ID del estudiante
            limite: Número máximo de registros a retornar
            
        Returns:
            Lista de cambios ordenados por fecha descendente
        """
        db = get_db()
        
        try:
            historial = db.query(HistorialModificacion).filter(
                HistorialModificacion.estudiante_id == estudiante_id
            ).order_by(HistorialModificacion.fecha.desc()).limit(limite).all()
            
            return historial
            
        finally:
            db.close()
    
    @staticmethod
    def obtener_actividad_admin(
        admin_id: int,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None
    ) -> List[HistorialModificacion]:
        """
        Obtiene toda la actividad de un admin en un período
        
        Args:
            admin_id: ID del admin
            fecha_desde: Fecha inicio del período
            fecha_hasta: Fecha fin del período
            
        Returns:
            Lista de acciones del admin
        """
        db = get_db()
        
        try:
            query = db.query(HistorialModificacion).filter(
                HistorialModificacion.admin_id == admin_id
            )
            
            if fecha_desde:
                query = query.filter(HistorialModificacion.fecha >= fecha_desde)
            
            if fecha_hasta:
                query = query.filter(HistorialModificacion.fecha <= fecha_hasta)
            
            actividad = query.order_by(HistorialModificacion.fecha.desc()).all()
            
            return actividad
            
        finally:
            db.close()
    
    @staticmethod
    def estadisticas_auditoria(
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None
    ) -> Dict:
        """
        Genera estadísticas de auditoría
        
        Args:
            fecha_desde: Fecha inicio
            fecha_hasta: Fecha fin
            
        Returns:
            Diccionario con estadísticas
        """
        db = get_db()
        
        try:
            query = db.query(HistorialModificacion)
            
            if fecha_desde:
                query = query.filter(HistorialModificacion.fecha >= fecha_desde)
            
            if fecha_hasta:
                query = query.filter(HistorialModificacion.fecha <= fecha_hasta)
            
            total_cambios = query.count()
            
            # Por tipo de acción
            aprobaciones = query.filter(HistorialModificacion.tipo_accion == 'aprobacion').count()
            rechazos = query.filter(HistorialModificacion.tipo_accion == 'rechazo').count()
            envios = query.filter(HistorialModificacion.tipo_accion == 'envio').count()
            ediciones = query.filter(HistorialModificacion.tipo_accion == 'edicion').count()
            
            # Admins más activos
            from sqlalchemy import func
            admins_activos = db.query(
                HistorialModificacion.admin_id,
                HistorialModificacion.admin_nombre,
                func.count(HistorialModificacion.id).label('total_acciones')
            ).group_by(
                HistorialModificacion.admin_id,
                HistorialModificacion.admin_nombre
            ).order_by(func.count(HistorialModificacion.id).desc()).limit(10).all()
            
            return {
                'total_cambios': total_cambios,
                'aprobaciones': aprobaciones,
                'rechazos': rechazos,
                'envios': envios,
                'ediciones': ediciones,
                'admins_mas_activos': [
                    {
                        'admin_id': a[0],
                        'admin_nombre': a[1],
                        'total_acciones': a[2]
                    } for a in admins_activos
                ]
            }
            
        finally:
            db.close()
    
    @staticmethod
    def generar_reporte_auditoria(
        estudiante_id: int
    ) -> str:
        """
        Genera un reporte legible del historial de un estudiante
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            String con el reporte formateado
        """
        historial = AuditoriaEstudiante.obtener_historial_estudiante(estudiante_id)
        
        if not historial:
            return "No hay historial de cambios para este estudiante."
        
        reporte = f"""
╔══════════════════════════════════════════════════════════════╗
║           HISTORIAL DE AUDITORÍA - ESTUDIANTE #{estudiante_id:04d}         ║
╚══════════════════════════════════════════════════════════════╝

Total de cambios: {len(historial)}

"""
        
        for i, cambio in enumerate(historial, 1):
            icono = {
                'aprobacion': '✅',
                'rechazo': '❌',
                'envio': '📧',
                'edicion': '✏️',
                'reasignacion': '🔄'
            }.get(cambio.tipo_accion, '📝')
            
            reporte += f"""
{i}. {icono} {cambio.tipo_accion.upper()}
   • Admin: {cambio.admin_nombre} (ID: {cambio.admin_id})
   • Fecha: {cambio.fecha.strftime('%d/%m/%Y %H:%M:%S')}
"""
            
            if cambio.campo_modificado:
                reporte += f"   • Campo: {cambio.campo_modificado}\n"
                if cambio.valor_anterior:
                    reporte += f"   • Antes: {cambio.valor_anterior}\n"
                if cambio.valor_nuevo:
                    reporte += f"   • Ahora: {cambio.valor_nuevo}\n"
            
            if cambio.motivo:
                reporte += f"   • Motivo: {cambio.motivo}\n"
            
            if cambio.descripcion:
                reporte += f"   • Descripción: {cambio.descripcion}\n"
            
            reporte += "\n" + "-" * 60 + "\n"
        
        return reporte
