"""
Sistema de Mensajería Interna
Chat entre estudiantes y admins dentro de la plataforma web
"""

from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.models import Base, get_db


class Mensaje(Base):
    """Modelo de mensaje en el sistema"""
    __tablename__ = 'mensajes'
    
    id = Column(Integer, primary_key=True, index=True)
    conversacion_id = Column(Integer, ForeignKey('conversaciones.id'))
    remitente_tipo = Column(String(20))  # 'estudiante' o 'admin'
    remitente_id = Column(Integer)
    contenido = Column(Text)
    leido = Column(Boolean, default=False)
    fecha_envio = Column(DateTime, default=datetime.now)
    fecha_lectura = Column(DateTime, nullable=True)
    
    conversacion = relationship("Conversacion", back_populates="mensajes")


class Conversacion(Base):
    """Modelo de conversación entre estudiante y admin"""
    __tablename__ = 'conversaciones'
    
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    admin_id = Column(Integer, nullable=True)
    estado = Column(String(20), default='activa')  # activa, cerrada, archivada
    ultima_actividad = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    
    mensajes = relationship("Mensaje", back_populates="conversacion", cascade="all, delete-orphan")


class SistemaMensajeria:
    """Gestiona la mensajería interna de la plataforma"""
    
    @staticmethod
    def crear_conversacion(estudiante_id: int, admin_id: int = None) -> Conversacion:
        """
        Crea una nueva conversación
        
        Args:
            estudiante_id: ID del estudiante
            admin_id: ID del admin (opcional)
            
        Returns:
            Conversacion creada
        """
        db = get_db()
        
        try:
            # Verificar si ya existe conversación activa
            conversacion_existente = db.query(Conversacion).filter(
                Conversacion.estudiante_id == estudiante_id,
                Conversacion.estado == 'activa'
            ).first()
            
            if conversacion_existente:
                return conversacion_existente
            
            # Crear nueva conversación
            nueva = Conversacion(
                estudiante_id=estudiante_id,
                admin_id=admin_id,
                estado='activa'
            )
            
            db.add(nueva)
            db.commit()
            db.refresh(nueva)
            
            return nueva
            
        finally:
            db.close()
    
    @staticmethod
    def enviar_mensaje(
        conversacion_id: int,
        remitente_tipo: str,
        remitente_id: int,
        contenido: str
    ) -> Dict:
        """
        Envía un mensaje en una conversación
        
        Args:
            conversacion_id: ID de la conversación
            remitente_tipo: 'estudiante' o 'admin'
            remitente_id: ID del remitente
            contenido: Contenido del mensaje
            
        Returns:
            Dict con el mensaje enviado
        """
        db = get_db()
        
        try:
            # Crear mensaje
            mensaje = Mensaje(
                conversacion_id=conversacion_id,
                remitente_tipo=remitente_tipo,
                remitente_id=remitente_id,
                contenido=contenido
            )
            
            db.add(mensaje)
            
            # Actualizar última actividad de conversación
            conversacion = db.query(Conversacion).filter(
                Conversacion.id == conversacion_id
            ).first()
            
            if conversacion:
                conversacion.ultima_actividad = datetime.now()
            
            db.commit()
            db.refresh(mensaje)
            
            return {
                'exito': True,
                'mensaje_id': mensaje.id,
                'fecha_envio': mensaje.fecha_envio.isoformat(),
                'contenido': mensaje.contenido
            }
            
        except Exception as e:
            db.rollback()
            return {
                'exito': False,
                'error': str(e)
            }
        finally:
            db.close()
    
    @staticmethod
    def obtener_mensajes(
        conversacion_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict]:
        """
        Obtiene mensajes de una conversación
        
        Args:
            conversacion_id: ID de la conversación
            limit: Cantidad máxima de mensajes
            offset: Offset para paginación
            
        Returns:
            Lista de mensajes
        """
        db = get_db()
        
        try:
            mensajes = db.query(Mensaje).filter(
                Mensaje.conversacion_id == conversacion_id
            ).order_by(
                Mensaje.fecha_envio.asc()
            ).offset(offset).limit(limit).all()
            
            return [
                {
                    'id': m.id,
                    'remitente_tipo': m.remitente_tipo,
                    'remitente_id': m.remitente_id,
                    'contenido': m.contenido,
                    'leido': m.leido,
                    'fecha_envio': m.fecha_envio.isoformat(),
                    'fecha_lectura': m.fecha_lectura.isoformat() if m.fecha_lectura else None
                }
                for m in mensajes
            ]
            
        finally:
            db.close()
    
    @staticmethod
    def marcar_como_leido(mensaje_id: int):
        """Marca un mensaje como leído"""
        db = get_db()
        
        try:
            mensaje = db.query(Mensaje).filter(Mensaje.id == mensaje_id).first()
            
            if mensaje and not mensaje.leido:
                mensaje.leido = True
                mensaje.fecha_lectura = datetime.now()
                db.commit()
            
        finally:
            db.close()
    
    @staticmethod
    def obtener_conversaciones_estudiante(estudiante_id: int) -> List[Dict]:
        """Obtiene todas las conversaciones de un estudiante"""
        db = get_db()
        
        try:
            conversaciones = db.query(Conversacion).filter(
                Conversacion.estudiante_id == estudiante_id
            ).order_by(
                Conversacion.ultima_actividad.desc()
            ).all()
            
            return [
                {
                    'id': c.id,
                    'estudiante_id': c.estudiante_id,
                    'admin_id': c.admin_id,
                    'estado': c.estado,
                    'ultima_actividad': c.ultima_actividad.isoformat(),
                    'mensajes_no_leidos': db.query(Mensaje).filter(
                        Mensaje.conversacion_id == c.id,
                        Mensaje.leido == False,
                        Mensaje.remitente_tipo == 'admin'
                    ).count()
                }
                for c in conversaciones
            ]
            
        finally:
            db.close()
    
    @staticmethod
    def obtener_conversaciones_admin(admin_id: int = None) -> List[Dict]:
        """Obtiene conversaciones asignadas a un admin o todas"""
        db = get_db()
        
        try:
            query = db.query(Conversacion).filter(
                Conversacion.estado == 'activa'
            )
            
            if admin_id:
                query = query.filter(Conversacion.admin_id == admin_id)
            
            conversaciones = query.order_by(
                Conversacion.ultima_actividad.desc()
            ).all()
            
            resultado = []
            for c in conversaciones:
                # Obtener info del estudiante
                from modules.estudiantes import Estudiante
                estudiante = db.query(Estudiante).filter(
                    Estudiante.id == c.estudiante_id
                ).first()
                
                # Contar mensajes no leídos
                no_leidos = db.query(Mensaje).filter(
                    Mensaje.conversacion_id == c.id,
                    Mensaje.leido == False,
                    Mensaje.remitente_tipo == 'estudiante'
                ).count()
                
                # Obtener último mensaje
                ultimo_mensaje = db.query(Mensaje).filter(
                    Mensaje.conversacion_id == c.id
                ).order_by(
                    Mensaje.fecha_envio.desc()
                ).first()
                
                resultado.append({
                    'id': c.id,
                    'estudiante_id': c.estudiante_id,
                    'estudiante_nombre': estudiante.nombre_completo if estudiante else 'Desconocido',
                    'admin_id': c.admin_id,
                    'estado': c.estado,
                    'ultima_actividad': c.ultima_actividad.isoformat(),
                    'mensajes_no_leidos': no_leidos,
                    'ultimo_mensaje': {
                        'contenido': ultimo_mensaje.contenido[:100] if ultimo_mensaje else '',
                        'fecha': ultimo_mensaje.fecha_envio.isoformat() if ultimo_mensaje else None
                    }
                })
            
            return resultado
            
        finally:
            db.close()
    
    @staticmethod
    def cerrar_conversacion(conversacion_id: int):
        """Cierra una conversación"""
        db = get_db()
        
        try:
            conversacion = db.query(Conversacion).filter(
                Conversacion.id == conversacion_id
            ).first()
            
            if conversacion:
                conversacion.estado = 'cerrada'
                db.commit()
            
        finally:
            db.close()
