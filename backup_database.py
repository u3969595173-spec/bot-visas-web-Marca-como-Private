"""
Sistema de Backup Automático de Base de Datos
Crea copias de seguridad de la base de datos PostgreSQL
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# Configuración
DATABASE_URL = os.getenv('DATABASE_URL')
BACKUP_DIR = Path("backups")
BACKUP_RETENTION_DAYS = 30  # Mantener backups de los últimos 30 días
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@botvisasestudio.com')

# Parsear DATABASE_URL
# Formato: postgresql://user:password@host:port/database
if DATABASE_URL:
    # Eliminar prefijo postgresql://
    db_info = DATABASE_URL.replace('postgresql://', '')
    
    # Separar credenciales de host
    if '@' in db_info:
        credentials, host_info = db_info.split('@')
        username, password = credentials.split(':')
        
        # Separar host de database
        if '/' in host_info:
            host_port, database = host_info.split('/')
            host = host_port.split(':')[0]
            port = host_port.split(':')[1] if ':' in host_port else '5432'
        else:
            host = host_info
            port = '5432'
            database = 'postgres'
    else:
        print("❌ Formato de DATABASE_URL inválido")
        exit(1)
else:
    print("❌ DATABASE_URL no configurada en .env")
    exit(1)


def crear_directorio_backup():
    """Crea el directorio de backups si no existe"""
    BACKUP_DIR.mkdir(exist_ok=True)
    print(f"✅ Directorio de backups: {BACKUP_DIR.absolute()}")


def generar_nombre_backup():
    """Genera nombre de archivo con fecha y hora"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"backup_{database}_{timestamp}.sql"


def realizar_backup():
    """Ejecuta pg_dump para crear backup de la base de datos"""
    crear_directorio_backup()
    
    nombre_archivo = generar_nombre_backup()
    ruta_backup = BACKUP_DIR / nombre_archivo
    
    print(f"🔄 Iniciando backup de la base de datos: {database}")
    print(f"📁 Archivo: {nombre_archivo}")
    
    # Configurar variables de entorno para pg_dump
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    
    # Comando pg_dump
    comando = [
        'pg_dump',
        '-h', host,
        '-p', port,
        '-U', username,
        '-d', database,
        '-F', 'c',  # Formato custom (comprimido)
        '-f', str(ruta_backup)
    ]
    
    try:
        # Ejecutar pg_dump
        resultado = subprocess.run(
            comando,
            env=env,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos timeout
        )
        
        if resultado.returncode == 0:
            tamaño = ruta_backup.stat().st_size / (1024 * 1024)  # MB
            print(f"✅ Backup completado exitosamente")
            print(f"📊 Tamaño: {tamaño:.2f} MB")
            return ruta_backup, tamaño
        else:
            print(f"❌ Error en backup:")
            print(resultado.stderr)
            return None, 0
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout: El backup tardó más de 5 minutos")
        return None, 0
    except FileNotFoundError:
        print("❌ pg_dump no encontrado. Asegúrate de tener PostgreSQL instalado.")
        print("   En Windows: Descarga desde https://www.postgresql.org/download/windows/")
        print("   En Linux: sudo apt-get install postgresql-client")
        print("   En Mac: brew install postgresql")
        return None, 0
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return None, 0


def limpiar_backups_antiguos():
    """Elimina backups más antiguos que BACKUP_RETENTION_DAYS"""
    if not BACKUP_DIR.exists():
        return
    
    print(f"🧹 Limpiando backups antiguos (más de {BACKUP_RETENTION_DAYS} días)...")
    
    ahora = datetime.now()
    eliminados = 0
    
    for archivo in BACKUP_DIR.glob("backup_*.sql"):
        # Calcular antigüedad
        antiguedad_dias = (ahora - datetime.fromtimestamp(archivo.stat().st_mtime)).days
        
        if antiguedad_dias > BACKUP_RETENTION_DAYS:
            archivo.unlink()
            eliminados += 1
            print(f"   ❌ Eliminado: {archivo.name} ({antiguedad_dias} días)")
    
    if eliminados > 0:
        print(f"✅ {eliminados} backup(s) antiguo(s) eliminado(s)")
    else:
        print("✅ No hay backups antiguos para eliminar")


def listar_backups():
    """Lista todos los backups disponibles"""
    if not BACKUP_DIR.exists():
        print("ℹ️  No hay backups disponibles")
        return
    
    backups = sorted(BACKUP_DIR.glob("backup_*.sql"), key=lambda f: f.stat().st_mtime, reverse=True)
    
    if not backups:
        print("ℹ️  No hay backups disponibles")
        return
    
    print(f"\n📋 Backups disponibles ({len(backups)}):")
    print("-" * 80)
    
    for i, backup in enumerate(backups, 1):
        stats = backup.stat()
        tamaño = stats.st_size / (1024 * 1024)
        fecha = datetime.fromtimestamp(stats.st_mtime)
        antiguedad = (datetime.now() - fecha).days
        
        print(f"{i}. {backup.name}")
        print(f"   📅 Fecha: {fecha.strftime('%Y-%m-%d %H:%M:%S')} ({antiguedad} días)")
        print(f"   📊 Tamaño: {tamaño:.2f} MB")
        print()


def enviar_notificacion_email(exito, ruta_backup=None, tamaño=0, error=None):
    """Envía email de notificación sobre el backup"""
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_FROM = os.getenv('EMAIL_FROM', 'bot@botvisasestudio.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    
    if not EMAIL_PASSWORD or not ADMIN_EMAIL:
        print("⚠️  Configuración de email no disponible. No se envió notificación.")
        return
    
    fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if exito:
        asunto = f"✅ Backup Exitoso - {database} - {fecha_hora}"
        cuerpo = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #28a745;">✅ Backup Completado Exitosamente</h2>
            <p><strong>Base de datos:</strong> {database}</p>
            <p><strong>Fecha y hora:</strong> {fecha_hora}</p>
            <p><strong>Archivo:</strong> {ruta_backup.name if ruta_backup else 'N/A'}</p>
            <p><strong>Tamaño:</strong> {tamaño:.2f} MB</p>
            <p><strong>Ubicación:</strong> {ruta_backup.absolute() if ruta_backup else 'N/A'}</p>
            <hr>
            <p style="color: #6c757d; font-size: 0.9rem;">
                Este es un mensaje automático del sistema de backups de Bot Visas Estudio.
            </p>
        </body>
        </html>
        """
    else:
        asunto = f"❌ Backup Fallido - {database} - {fecha_hora}"
        cuerpo = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #dc3545;">❌ Error en Backup</h2>
            <p><strong>Base de datos:</strong> {database}</p>
            <p><strong>Fecha y hora:</strong> {fecha_hora}</p>
            <p><strong>Error:</strong></p>
            <pre style="background-color: #f8f9fa; padding: 10px; border-radius: 5px;">{error}</pre>
            <p style="color: #dc3545;"><strong>ACCIÓN REQUERIDA:</strong> Revisar logs y configuración del sistema de backups.</p>
            <hr>
            <p style="color: #6c757d; font-size: 0.9rem;">
                Este es un mensaje automático del sistema de backups de Bot Visas Estudio.
            </p>
        </body>
        </html>
        """
    
    try:
        mensaje = MIMEMultipart('alternative')
        mensaje['From'] = EMAIL_FROM
        mensaje['To'] = ADMIN_EMAIL
        mensaje['Subject'] = asunto
        
        parte_html = MIMEText(cuerpo, 'html')
        mensaje.attach(parte_html)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_FROM, EMAIL_PASSWORD)
            servidor.send_message(mensaje)
        
        print(f"📧 Notificación enviada a: {ADMIN_EMAIL}")
        
    except Exception as e:
        print(f"⚠️  Error al enviar notificación: {str(e)}")


def main():
    """Función principal"""
    print("=" * 80)
    print("🗄️  SISTEMA DE BACKUP AUTOMÁTICO - BOT VISAS ESTUDIO")
    print("=" * 80)
    print()
    
    # Realizar backup
    ruta_backup, tamaño = realizar_backup()
    
    if ruta_backup:
        # Limpiar backups antiguos
        limpiar_backups_antiguos()
        
        # Listar backups disponibles
        listar_backups()
        
        # Enviar notificación de éxito
        enviar_notificacion_email(True, ruta_backup, tamaño)
        
        print("\n" + "=" * 80)
        print("✅ Proceso de backup completado exitosamente")
        print("=" * 80)
    else:
        # Enviar notificación de error
        enviar_notificacion_email(False, error="Fallo al crear backup. Revisar logs.")
        
        print("\n" + "=" * 80)
        print("❌ Proceso de backup falló")
        print("=" * 80)
        exit(1)


if __name__ == "__main__":
    main()
