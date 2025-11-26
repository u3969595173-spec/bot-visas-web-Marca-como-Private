"""
Sistema de Seguimiento Post-Envío
Tracking de interacciones del estudiante después del envío
"""

from datetime import datetime
from typing import Dict, List
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database.models import get_db

Base = declarative_base()


class SeguimientoEnvio(Base):
    __tablename__ = 'seguimiento_envios'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    
    # Datos del envío
    fecha_envio = Column(DateTime, nullable=False)
    canales_enviados = Column(String(200))  # telegram,email
    
    # Tracking Email
    email_abierto = Column(Boolean, default=False)
    fecha_apertura_email = Column(DateTime)
    numero_aperturas = Column(Integer, default=0)
    
    # Tracking Telegram
    mensaje_visto = Column(Boolean, default=False)
    fecha_visto_telegram = Column(DateTime)
    
    # Respuestas
    respondio = Column(Boolean, default=False)
    fecha_respuesta = Column(DateTime)
    contenido_respuesta = Column(Text)
    
    # Métricas
    tiempo_hasta_apertura_horas = Column(Integer)  # Horas hasta abrir
    tiempo_hasta_respuesta_horas = Column(Integer)  # Horas hasta responder
    
    # Acciones tomadas
    acciones_tomadas = Column(Text)  # JSON con acciones del estudiante
    
    created_at = Column(DateTime, default=datetime.utcnow)


class SistemaSeguimiento:
    """Sistema de tracking post-envío"""
    
    @staticmethod
    def registrar_envio(estudiante_id: int, canales: List[str]) -> SeguimientoEnvio:
        """Registra un nuevo envío para tracking"""
        db = get_db()
        
        try:
            seguimiento = SeguimientoEnvio(
                estudiante_id=estudiante_id,
                fecha_envio=datetime.utcnow(),
                canales_enviados=','.join(canales)
            )
            
            db.add(seguimiento)
            db.commit()
            db.refresh(seguimiento)
            
            return seguimiento
        finally:
            db.close()
    
    @staticmethod
    def marcar_email_abierto(estudiante_id: int):
        """Marca que el estudiante abrió el email"""
        db = get_db()
        
        try:
            seguimiento = db.query(SeguimientoEnvio).filter(
                SeguimientoEnvio.estudiante_id == estudiante_id
            ).order_by(SeguimientoEnvio.fecha_envio.desc()).first()
            
            if seguimiento and not seguimiento.email_abierto:
                seguimiento.email_abierto = True
                seguimiento.fecha_apertura_email = datetime.utcnow()
                seguimiento.numero_aperturas = 1
                seguimiento.tiempo_hasta_apertura_horas = int(
                    (datetime.utcnow() - seguimiento.fecha_envio).total_seconds() / 3600
                )
                db.commit()
        finally:
            db.close()
    
    @staticmethod
    def marcar_respondido(estudiante_id: int, respuesta: str = None):
        """Marca que el estudiante respondió"""
        db = get_db()
        
        try:
            seguimiento = db.query(SeguimientoEnvio).filter(
                SeguimientoEnvio.estudiante_id == estudiante_id
            ).order_by(SeguimientoEnvio.fecha_envio.desc()).first()
            
            if seguimiento and not seguimiento.respondio:
                seguimiento.respondio = True
                seguimiento.fecha_respuesta = datetime.utcnow()
                seguimiento.contenido_respuesta = respuesta
                seguimiento.tiempo_hasta_respuesta_horas = int(
                    (datetime.utcnow() - seguimiento.fecha_envio).total_seconds() / 3600
                )
                db.commit()
        finally:
            db.close()
    
    @staticmethod
    def obtener_metricas_envio(estudiante_id: int) -> Dict:
        """Obtiene métricas de envío"""
        db = get_db()
        
        try:
            seguimiento = db.query(SeguimientoEnvio).filter(
                SeguimientoEnvio.estudiante_id == estudiante_id
            ).order_by(SeguimientoEnvio.fecha_envio.desc()).first()
            
            if not seguimiento:
                return {'sin_envios': True}
            
            return {
                'enviado': True,
                'fecha_envio': seguimiento.fecha_envio,
                'canales': seguimiento.canales_enviados.split(','),
                'email_abierto': seguimiento.email_abierto,
                'respondio': seguimiento.respondio,
                'tiempo_apertura_horas': seguimiento.tiempo_hasta_apertura_horas,
                'tiempo_respuesta_horas': seguimiento.tiempo_hasta_respuesta_horas,
                'estado': SistemaSeguimiento._calcular_estado(seguimiento)
            }
        finally:
            db.close()
    
    @staticmethod
    def _calcular_estado(seguimiento: SeguimientoEnvio) -> str:
        """Calcula estado del seguimiento"""
        if seguimiento.respondio:
            return 'respondido'
        elif seguimiento.email_abierto or seguimiento.mensaje_visto:
            return 'visto'
        else:
            horas_pasadas = (datetime.utcnow() - seguimiento.fecha_envio).total_seconds() / 3600
            if horas_pasadas > 48:
                return 'sin_abrir_48h'
            return 'enviado'
    
    @staticmethod
    def estadisticas_seguimiento() -> Dict:
        """Estadísticas generales de seguimiento"""
        db = get_db()
        
        try:
            total = db.query(SeguimientoEnvio).count()
            abiertos = db.query(SeguimientoEnvio).filter(SeguimientoEnvio.email_abierto == True).count()
            respondidos = db.query(SeguimientoEnvio).filter(SeguimientoEnvio.respondio == True).count()
            
            from sqlalchemy import func
            tiempo_promedio = db.query(func.avg(SeguimientoEnvio.tiempo_hasta_respuesta_horas)).filter(
                SeguimientoEnvio.respondio == True
            ).scalar()
            
            return {
                'total_envios': total,
                'tasa_apertura': (abiertos / total * 100) if total > 0 else 0,
                'tasa_respuesta': (respondidos / total * 100) if total > 0 else 0,
                'tiempo_promedio_respuesta_horas': tiempo_promedio or 0
            }
        finally:
            db.close()
