"""
Sistema de Recordatorios para Admin
Notifica si hay casos sin revisar por más de 24h
"""

from datetime import datetime, timedelta
from typing import List, Dict
from modules.estudiantes import Estudiante
from modules.notificaciones import SistemaNotificaciones
from database.models import get_db
import config


class SistemaRecordatorios:
    """Recordatorios automáticos para admins"""
    
    @staticmethod
    def verificar_casos_pendientes() -> Dict:
        """
        Verifica casos que llevan mucho tiempo sin revisar
        
        Returns:
            Dict con estadísticas de casos pendientes
        """
        db = get_db()
        
        try:
            ahora = datetime.now()
            hace_24h = ahora - timedelta(hours=24)
            hace_48h = ahora - timedelta(hours=48)
            hace_72h = ahora - timedelta(hours=72)
            
            # Casos pendientes por tiempo
            pendientes_24h = db.query(Estudiante).filter(
                Estudiante.estado_procesamiento == 'pendiente_revision_admin',
                Estudiante.fecha_procesamiento_automatico <= hace_24h,
                Estudiante.fecha_procesamiento_automatico > hace_48h
            ).all()
            
            pendientes_48h = db.query(Estudiante).filter(
                Estudiante.estado_procesamiento == 'pendiente_revision_admin',
                Estudiante.fecha_procesamiento_automatico <= hace_48h,
                Estudiante.fecha_procesamiento_automatico > hace_72h
            ).all()
            
            criticos_72h = db.query(Estudiante).filter(
                Estudiante.estado_procesamiento == 'pendiente_revision_admin',
                Estudiante.fecha_procesamiento_automatico <= hace_72h
            ).all()
            
            return {
                'pendientes_24h': len(pendientes_24h),
                'pendientes_48h': len(pendientes_48h),
                'criticos_72h': len(criticos_72h),
                'total_pendientes': len(pendientes_24h) + len(pendientes_48h) + len(criticos_72h),
                'estudiantes_24h': pendientes_24h,
                'estudiantes_48h': pendientes_48h,
                'estudiantes_criticos': criticos_72h
            }
            
        finally:
            db.close()
    
    @staticmethod
    def enviar_recordatorios():
        """Envía recordatorios a todos los admins"""
        
        casos = SistemaRecordatorios.verificar_casos_pendientes()
        
        if casos['total_pendientes'] == 0:
            print("✅ No hay casos pendientes que requieran recordatorio")
            return
        
        # Mensaje para admins
        mensaje = f"""
⏰ **RECORDATORIO: CASOS PENDIENTES DE REVISIÓN**

📊 Resumen:
   • ⚠️ Más de 24h: {casos['pendientes_24h']}
   • 🔴 Más de 48h: {casos['pendientes_48h']}
   • 🚨 MÁS DE 72H (CRÍTICO): {casos['criticos_72h']}

**TOTAL PENDIENTES: {casos['total_pendientes']}**

"""
        
        # Agregar casos críticos
        if casos['criticos_72h'] > 0:
            mensaje += "\n🚨 CASOS CRÍTICOS (>72h):\n"
            for est in casos['estudiantes_criticos'][:5]:  # Top 5
                horas = (datetime.now() - est.fecha_procesamiento_automatico).total_seconds() / 3600
                mensaje += f"   • {est.nombre_completo} ({horas:.0f}h esperando)\n"
        
        mensaje += "\n📋 Por favor, revisa el panel de control lo antes posible."
        
        # Enviar a todos los admins
        for admin_id in config.ADMIN_USER_IDS:
            try:
                SistemaNotificaciones._enviar_telegram(
                    admin_id,
                    "⏰ Recordatorio de Casos Pendientes",
                    mensaje
                )
                print(f"✅ Recordatorio enviado a admin {admin_id}")
            except Exception as e:
                print(f"❌ Error enviando a admin {admin_id}: {e}")
    
    @staticmethod
    def recordatorio_personalizado(admin_id: int):
        """Envía recordatorio personalizado a un admin específico"""
        db = get_db()
        
        try:
            # Casos asignados a este admin
            mis_casos = db.query(Estudiante).filter(
                Estudiante.admin_revisor_id == admin_id,
                Estudiante.estado_procesamiento == 'pendiente_revision_admin'
            ).all()
            
            if not mis_casos:
                return
            
            hace_24h = datetime.now() - timedelta(hours=24)
            pendientes = [est for est in mis_casos if est.fecha_procesamiento_automatico <= hace_24h]
            
            if not pendientes:
                return
            
            mensaje = f"""
⏰ **RECORDATORIO PERSONAL**

Tienes {len(pendientes)} casos asignados esperando revisión:

"""
            
            for est in pendientes[:5]:
                horas = (datetime.now() - est.fecha_procesamiento_automatico).total_seconds() / 3600
                mensaje += f"   • {est.nombre_completo} - {est.especialidad_interes} ({horas:.0f}h)\n"
            
            if len(pendientes) > 5:
                mensaje += f"\n   ... y {len(pendientes) - 5} más.\n"
            
            SistemaNotificaciones._enviar_telegram(
                admin_id,
                "⏰ Tus Casos Pendientes",
                mensaje
            )
            
        finally:
            db.close()


def tarea_diaria_recordatorios():
    """Tarea automática diaria para enviar recordatorios"""
    print("🔔 Ejecutando tarea de recordatorios...")
    SistemaRecordatorios.enviar_recordatorios()
    print("✅ Recordatorios enviados")
