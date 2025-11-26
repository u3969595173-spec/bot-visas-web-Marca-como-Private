"""
Sistema de monitoreo y alertas para scrapers
Detecta fallos y envía notificaciones
"""
import json
import os
from datetime import datetime
from typing import Dict, List
from api.email_utils import enviar_email


class MonitorScrapers:
    """Monitor de salud de scrapers"""
    
    LOG_FILE = "scraper_monitor.json"
    ALERT_THRESHOLD = 3  # Fallos consecutivos antes de alertar
    
    def __init__(self, admin_email: str = "estudiovisaespana@gmail.com"):
        self.admin_email = admin_email
        self.load_history()
    
    def load_history(self):
        """Carga historial de ejecuciones"""
        if os.path.exists(self.LOG_FILE):
            with open(self.LOG_FILE, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = {}
    
    def save_history(self):
        """Guarda historial"""
        with open(self.LOG_FILE, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def log_execution(self, source: str, success: bool, cursos_count: int = 0, error: str = None):
        """
        Registra ejecución de scraper
        
        Args:
            source: Nombre de la fuente (educations, emagister, etc)
            success: Si la ejecución fue exitosa
            cursos_count: Cantidad de cursos obtenidos
            error: Mensaje de error si falló
        """
        if source not in self.history:
            self.history[source] = {
                'total_executions': 0,
                'successful': 0,
                'failed': 0,
                'last_success': None,
                'last_failure': None,
                'consecutive_failures': 0,
                'alert_sent': False,
                'executions': []
            }
        
        # Registrar ejecución
        execution = {
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'cursos_count': cursos_count,
            'error': error
        }
        
        self.history[source]['executions'].append(execution)
        self.history[source]['total_executions'] += 1
        
        if success:
            self.history[source]['successful'] += 1
            self.history[source]['last_success'] = datetime.now().isoformat()
            self.history[source]['consecutive_failures'] = 0
            self.history[source]['alert_sent'] = False
        else:
            self.history[source]['failed'] += 1
            self.history[source]['last_failure'] = datetime.now().isoformat()
            self.history[source]['consecutive_failures'] += 1
        
        # Mantener solo últimas 100 ejecuciones
        if len(self.history[source]['executions']) > 100:
            self.history[source]['executions'] = self.history[source]['executions'][-100:]
        
        self.save_history()
        
        # Verificar si se debe enviar alerta
        self._check_and_alert(source)
    
    def _check_and_alert(self, source: str):
        """Verifica si se debe enviar alerta"""
        data = self.history[source]
        
        # Si ya se envió alerta, no enviar otra
        if data['alert_sent']:
            return
        
        # Si hay muchos fallos consecutivos
        if data['consecutive_failures'] >= self.ALERT_THRESHOLD:
            self._send_alert(source, data)
            self.history[source]['alert_sent'] = True
            self.save_history()
    
    def _send_alert(self, source: str, data: Dict):
        """Envía alerta por email al admin"""
        asunto = f"🚨 ALERTA: Scraper {source} fallando"
        
        last_errors = [e for e in data['executions'][-5:] if not e['success']]
        error_messages = "\n".join([f"- {e.get('error', 'Error desconocido')}" for e in last_errors])
        
        cuerpo = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #e53e3e;">⚠️ Alerta de Scraper</h2>
            
            <p><strong>Fuente:</strong> {source}</p>
            <p><strong>Fallos consecutivos:</strong> {data['consecutive_failures']}</p>
            <p><strong>Último éxito:</strong> {data['last_success'] or 'Nunca'}</p>
            <p><strong>Tasa de éxito:</strong> {(data['successful'] / data['total_executions'] * 100):.1f}%</p>
            
            <h3>Últimos errores:</h3>
            <pre style="background: #f7fafc; padding: 15px; border-radius: 8px;">
{error_messages}
            </pre>
            
            <h3>Acciones recomendadas:</h3>
            <ul>
                <li>Verificar si el sitio web cambió su estructura HTML</li>
                <li>Revisar logs en Render para más detalles</li>
                <li>Actualizar selectores CSS en integrador_escuelas.py</li>
                <li>El sistema está usando cursos de respaldo automáticamente</li>
            </ul>
            
            <p style="color: #718096; margin-top: 30px;">
                Bot Visas Estudio - Sistema de Monitoreo Automático
            </p>
        </body>
        </html>
        """
        
        try:
            enviar_email(self.admin_email, asunto, cuerpo)
            print(f"📧 Alerta enviada para {source}")
        except Exception as e:
            print(f"❌ Error enviando alerta: {e}")
    
    def get_health_report(self) -> Dict:
        """Genera reporte de salud de todos los scrapers"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'scrapers': {}
        }
        
        for source, data in self.history.items():
            if data['total_executions'] > 0:
                success_rate = (data['successful'] / data['total_executions']) * 100
            else:
                success_rate = 0
            
            report['scrapers'][source] = {
                'status': 'healthy' if data['consecutive_failures'] == 0 else 'failing',
                'success_rate': f"{success_rate:.1f}%",
                'total_executions': data['total_executions'],
                'consecutive_failures': data['consecutive_failures'],
                'last_success': data['last_success'],
                'last_failure': data['last_failure']
            }
        
        return report
    
    def clear_alerts(self, source: str = None):
        """Limpia alertas (después de arreglar el problema)"""
        if source:
            if source in self.history:
                self.history[source]['alert_sent'] = False
                self.history[source]['consecutive_failures'] = 0
        else:
            for src in self.history:
                self.history[src]['alert_sent'] = False
                self.history[src]['consecutive_failures'] = 0
        
        self.save_history()
        print(f"✅ Alertas limpiadas: {source or 'todas'}")
