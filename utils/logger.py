"""
Sistema de Logging Estructurado
Logs en formato JSON para mejor debugging y análisis
"""

import logging
import sys
from pythonjsonlogger import jsonlogger
from datetime import datetime

def setup_logger(name: str = "bot-visas"):
    """
    Configura logger con formato JSON para producción
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar duplicados
    if logger.handlers:
        return logger
    
    # Handler para stdout (Render lo captura automáticamente)
    logHandler = logging.StreamHandler(sys.stdout)
    
    # Formato JSON estructurado
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(levelname)s %(name)s %(message)s'
    )
    
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    
    return logger

# Logger global para usar en toda la app
logger = setup_logger()

def log_event(event_type: str, message: str, **kwargs):
    """
    Helper para logging consistente de eventos
    
    Args:
        event_type: Tipo de evento (registro, login, error, etc)
        message: Mensaje descriptivo
        **kwargs: Datos adicionales del evento
    """
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        **kwargs
    }
    
    logger.info(message, extra=log_data)

def log_error(error_type: str, message: str, error: Exception = None, **kwargs):
    """
    Helper para logging de errores
    
    Args:
        error_type: Tipo de error (db_error, validation_error, etc)
        message: Mensaje descriptivo
        error: Excepción original si existe
        **kwargs: Datos adicionales del error
    """
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "error_type": error_type,
        **kwargs
    }
    
    if error:
        log_data["error_message"] = str(error)
        log_data["error_class"] = type(error).__name__
    
    logger.error(message, extra=log_data, exc_info=error is not None)
