"""
Scheduler para envío automático de alertas de fechas importantes
Ejecuta verificación diaria a las 9:00 AM
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from database.models import SessionLocal
from api.alertas_fechas import GestorAlertasFechas
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def job_verificar_alertas():
    """
    Job que verifica alertas pendientes y envía emails
    Se ejecuta diariamente a las 9:00 AM
    """
    logger.info(f"🔔 Iniciando verificación de alertas - {datetime.now()}")
    
    db = SessionLocal()
    try:
        alertas_enviadas = GestorAlertasFechas.verificar_alertas_pendientes(db)
        
        if alertas_enviadas:
            logger.info(f"✅ Se enviaron {len(alertas_enviadas)} alertas:")
            for alerta in alertas_enviadas:
                logger.info(f"   - Estudiante {alerta['estudiante_id']}: alerta de {alerta['tipo']}")
        else:
            logger.info("ℹ️ No hay alertas pendientes para enviar")
            
    except Exception as e:
        logger.error(f"❌ Error en verificación de alertas: {e}")
    finally:
        db.close()
    
    logger.info("🏁 Verificación de alertas completada\n")

# Crear scheduler
scheduler = BackgroundScheduler()

# Agregar job: ejecutar todos los días a las 9:00 AM (hora del servidor)
scheduler.add_job(
    job_verificar_alertas,
    trigger=CronTrigger(hour=9, minute=0),
    id='verificar_alertas_diarias',
    name='Verificación diaria de alertas de fechas',
    replace_existing=True
)

def iniciar_scheduler():
    """Inicia el scheduler de alertas"""
    if not scheduler.running:
        scheduler.start()
        logger.info("✅ Scheduler de alertas iniciado - Se ejecutará diariamente a las 9:00 AM")
        logger.info("📅 Próxima ejecución: " + str(scheduler.get_jobs()[0].next_run_time))
    else:
        logger.info("ℹ️ Scheduler ya está corriendo")

def detener_scheduler():
    """Detiene el scheduler de alertas"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("🛑 Scheduler de alertas detenido")

def ejecutar_verificacion_manual():
    """
    Ejecuta verificación manual de alertas (útil para testing)
    """
    logger.info("🔧 Ejecutando verificación manual de alertas...")
    job_verificar_alertas()
