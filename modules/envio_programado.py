"""
Sistema de Envío Programado
Permite programar el envío de información para fecha/hora específica
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database.models import get_db
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

Base = declarative_base()


class EnvioProgramado(Base):
    __tablename__ = 'envios_programados'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'), nullable=False)
    admin_id = Column(Integer, nullable=False)
    
    # Programación
    fecha_programada = Column(DateTime, nullable=False)
    
    # Contenido del envío
    canales = Column(JSON)  # ['telegram', 'email']
    mensaje_personalizado = Column(Text)
    plantilla_id = Column(Integer)
    
    # Estado
    estado = Column(String(50), default='programado')  # programado, enviado, cancelado, error
    fecha_envio_real = Column(DateTime)
    error_mensaje = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GestorEnviosProgramados:
    """Gestor de envíos programados"""
    
    scheduler = None
    
    @staticmethod
    def inicializar_scheduler():
        """Inicializa el scheduler de tareas programadas"""
        if GestorEnviosProgramados.scheduler is None:
            GestorEnviosProgramados.scheduler = BackgroundScheduler()
            GestorEnviosProgramados.scheduler.start()
            print("✅ Scheduler de envíos programados iniciado")
    
    @staticmethod
    def programar_envio(
        estudiante_id: int,
        admin_id: int,
        fecha_programada: datetime,
        canales: List[str],
        mensaje_personalizado: str = None,
        plantilla_id: int = None
    ) -> EnvioProgramado:
        """
        Programa un envío para el futuro
        
        Args:
            estudiante_id: ID del estudiante
            admin_id: ID del admin que programa
            fecha_programada: Fecha y hora del envío
            canales: Lista de canales ['telegram', 'email']
            mensaje_personalizado: Mensaje adicional (opcional)
            plantilla_id: ID de plantilla a usar (opcional)
            
        Returns:
            EnvioProgramado creado
        """
        db = get_db()
        
        try:
            # Validar que la fecha sea futura
            if fecha_programada <= datetime.now():
                raise ValueError("La fecha programada debe ser futura")
            
            # Crear registro
            envio = EnvioProgramado(
                estudiante_id=estudiante_id,
                admin_id=admin_id,
                fecha_programada=fecha_programada,
                canales=canales,
                mensaje_personalizado=mensaje_personalizado,
                plantilla_id=plantilla_id,
                estado='programado'
            )
            
            db.add(envio)
            db.commit()
            db.refresh(envio)
            
            # Programar en el scheduler
            GestorEnviosProgramados.inicializar_scheduler()
            
            GestorEnviosProgramados.scheduler.add_job(
                func=GestorEnviosProgramados._ejecutar_envio,
                trigger=DateTrigger(run_date=fecha_programada),
                args=[envio.id],
                id=f"envio_{envio.id}",
                replace_existing=True
            )
            
            print(f"✅ Envío programado para {fecha_programada.strftime('%d/%m/%Y %H:%M')}")
            return envio
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def _ejecutar_envio(envio_id: int):
        """
        Ejecuta el envío programado
        
        Args:
            envio_id: ID del envío programado
        """
        from modules.panel_revision_admin import PanelRevisionAdmin
        
        db = get_db()
        
        try:
            envio = db.query(EnvioProgramado).filter(
                EnvioProgramado.id == envio_id
            ).first()
            
            if not envio or envio.estado != 'programado':
                return
            
            print(f"📤 Ejecutando envío programado #{envio_id}...")
            
            # Realizar el envío
            resultado = PanelRevisionAdmin.enviar_informacion_manual(
                estudiante_id=envio.estudiante_id,
                admin_id=envio.admin_id,
                canales=envio.canales,
                mensaje_personalizado=envio.mensaje_personalizado
            )
            
            # Actualizar estado
            if resultado.get('exito'):
                envio.estado = 'enviado'
                envio.fecha_envio_real = datetime.utcnow()
                print(f"✅ Envío programado #{envio_id} completado")
            else:
                envio.estado = 'error'
                envio.error_mensaje = resultado.get('error', 'Error desconocido')
                print(f"❌ Error en envío programado #{envio_id}: {envio.error_mensaje}")
            
            db.commit()
            
        except Exception as e:
            envio.estado = 'error'
            envio.error_mensaje = str(e)
            db.commit()
            print(f"❌ Error ejecutando envío #{envio_id}: {e}")
        finally:
            db.close()
    
    @staticmethod
    def cancelar_envio(envio_id: int, admin_id: int) -> bool:
        """
        Cancela un envío programado
        
        Args:
            envio_id: ID del envío
            admin_id: ID del admin que cancela
            
        Returns:
            True si se canceló exitosamente
        """
        db = get_db()
        
        try:
            envio = db.query(EnvioProgramado).filter(
                EnvioProgramado.id == envio_id
            ).first()
            
            if not envio or envio.estado != 'programado':
                return False
            
            # Cancelar en el scheduler
            try:
                GestorEnviosProgramados.scheduler.remove_job(f"envio_{envio_id}")
            except:
                pass
            
            # Actualizar estado
            envio.estado = 'cancelado'
            db.commit()
            
            print(f"✅ Envío programado #{envio_id} cancelado")
            return True
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def reprogramar_envio(
        envio_id: int,
        nueva_fecha: datetime,
        admin_id: int
    ) -> EnvioProgramado:
        """
        Reprograma un envío para otra fecha
        
        Args:
            envio_id: ID del envío
            nueva_fecha: Nueva fecha programada
            admin_id: ID del admin
            
        Returns:
            EnvioProgramado actualizado
        """
        db = get_db()
        
        try:
            envio = db.query(EnvioProgramado).filter(
                EnvioProgramado.id == envio_id
            ).first()
            
            if not envio or envio.estado != 'programado':
                raise ValueError("Envío no encontrado o ya fue ejecutado")
            
            if nueva_fecha <= datetime.now():
                raise ValueError("La nueva fecha debe ser futura")
            
            # Actualizar fecha
            envio.fecha_programada = nueva_fecha
            envio.updated_at = datetime.utcnow()
            
            # Reprogramar en el scheduler
            GestorEnviosProgramados.scheduler.reschedule_job(
                job_id=f"envio_{envio_id}",
                trigger=DateTrigger(run_date=nueva_fecha)
            )
            
            db.commit()
            db.refresh(envio)
            
            print(f"✅ Envío #{envio_id} reprogramado para {nueva_fecha.strftime('%d/%m/%Y %H:%M')}")
            return envio
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def listar_envios_programados(
        solo_pendientes: bool = True,
        admin_id: int = None
    ) -> List[EnvioProgramado]:
        """
        Lista todos los envíos programados
        
        Args:
            solo_pendientes: Solo mostrar envíos pendientes
            admin_id: Filtrar por admin (opcional)
            
        Returns:
            Lista de envíos
        """
        db = get_db()
        
        try:
            query = db.query(EnvioProgramado)
            
            if solo_pendientes:
                query = query.filter(EnvioProgramado.estado == 'programado')
            
            if admin_id:
                query = query.filter(EnvioProgramado.admin_id == admin_id)
            
            envios = query.order_by(EnvioProgramado.fecha_programada).all()
            
            return envios
            
        finally:
            db.close()
    
    @staticmethod
    def obtener_proximos_envios(horas: int = 24) -> List[EnvioProgramado]:
        """
        Obtiene los envíos programados para las próximas X horas
        
        Args:
            horas: Número de horas hacia adelante
            
        Returns:
            Lista de envíos próximos
        """
        db = get_db()
        
        try:
            fecha_limite = datetime.now() + timedelta(hours=horas)
            
            envios = db.query(EnvioProgramado).filter(
                EnvioProgramado.estado == 'programado',
                EnvioProgramado.fecha_programada <= fecha_limite,
                EnvioProgramado.fecha_programada >= datetime.now()
            ).order_by(EnvioProgramado.fecha_programada).all()
            
            return envios
            
        finally:
            db.close()
    
    @staticmethod
    def estadisticas_envios() -> Dict:
        """
        Genera estadísticas de envíos programados
        
        Returns:
            Dict con estadísticas
        """
        db = get_db()
        
        try:
            total = db.query(EnvioProgramado).count()
            programados = db.query(EnvioProgramado).filter(EnvioProgramado.estado == 'programado').count()
            enviados = db.query(EnvioProgramado).filter(EnvioProgramado.estado == 'enviado').count()
            cancelados = db.query(EnvioProgramado).filter(EnvioProgramado.estado == 'cancelado').count()
            errores = db.query(EnvioProgramado).filter(EnvioProgramado.estado == 'error').count()
            
            proximos_24h = len(GestorEnviosProgramados.obtener_proximos_envios(24))
            
            return {
                'total': total,
                'programados': programados,
                'enviados': enviados,
                'cancelados': cancelados,
                'errores': errores,
                'proximos_24_horas': proximos_24h
            }
            
        finally:
            db.close()
