"""
Sistema de Restauración de Backups
Restaura una base de datos desde un archivo de backup
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuración
DATABASE_URL = os.getenv('DATABASE_URL')
BACKUP_DIR = Path("backups")

# Parsear DATABASE_URL
if DATABASE_URL:
    db_info = DATABASE_URL.replace('postgresql://', '')
    
    if '@' in db_info:
        credentials, host_info = db_info.split('@')
        username, password = credentials.split(':')
        
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


def listar_backups():
    """Lista todos los backups disponibles y retorna la lista"""
    if not BACKUP_DIR.exists():
        print("❌ No hay backups disponibles")
        return []
    
    backups = sorted(BACKUP_DIR.glob("backup_*.sql"), key=lambda f: f.stat().st_mtime, reverse=True)
    
    if not backups:
        print("❌ No hay backups disponibles")
        return []
    
    print(f"\n📋 Backups disponibles ({len(backups)}):")
    print("=" * 80)
    
    for i, backup in enumerate(backups, 1):
        stats = backup.stat()
        tamaño = stats.st_size / (1024 * 1024)
        fecha = datetime.fromtimestamp(stats.st_mtime)
        antiguedad = (datetime.now() - fecha).days
        
        print(f"{i}. {backup.name}")
        print(f"   📅 Fecha: {fecha.strftime('%Y-%m-%d %H:%M:%S')} ({antiguedad} días)")
        print(f"   📊 Tamaño: {tamaño:.2f} MB")
        print()
    
    return backups


def restaurar_backup(ruta_backup):
    """Restaura la base de datos desde un backup"""
    print(f"\n🔄 Iniciando restauración de backup...")
    print(f"📁 Archivo: {ruta_backup.name}")
    
    # ADVERTENCIA
    print("\n" + "=" * 80)
    print("⚠️  ADVERTENCIA: Esta operación SOBRESCRIBIRÁ la base de datos actual")
    print("=" * 80)
    
    confirmacion = input("\n¿Estás seguro de continuar? (escribe 'SI' para confirmar): ")
    
    if confirmacion.upper() != 'SI':
        print("❌ Restauración cancelada por el usuario")
        return False
    
    # Configurar variables de entorno
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    
    # Comando pg_restore
    comando = [
        'pg_restore',
        '-h', host,
        '-p', port,
        '-U', username,
        '-d', database,
        '--clean',  # Limpia objetos antes de restaurar
        '--if-exists',  # Evita errores si no existen
        '--no-owner',  # No restaura ownership
        '--no-privileges',  # No restaura privilegios
        str(ruta_backup)
    ]
    
    try:
        print("\n🔄 Restaurando base de datos...")
        
        resultado = subprocess.run(
            comando,
            env=env,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutos timeout
        )
        
        # pg_restore puede devolver warnings que no son críticos
        if resultado.returncode == 0 or (resultado.returncode == 1 and 'error' not in resultado.stderr.lower()):
            print("✅ Restauración completada exitosamente")
            if resultado.stderr:
                print("\nAdvertencias (no críticas):")
                print(resultado.stderr[:500])  # Primeros 500 caracteres
            return True
        else:
            print(f"❌ Error en restauración:")
            print(resultado.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout: La restauración tardó más de 10 minutos")
        return False
    except FileNotFoundError:
        print("❌ pg_restore no encontrado. Asegúrate de tener PostgreSQL instalado.")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False


def main():
    """Función principal"""
    print("=" * 80)
    print("🔧 SISTEMA DE RESTAURACIÓN DE BACKUPS - BOT VISAS ESTUDIO")
    print("=" * 80)
    
    # Listar backups disponibles
    backups = listar_backups()
    
    if not backups:
        exit(1)
    
    # Seleccionar backup
    print("=" * 80)
    try:
        seleccion = int(input("\nSelecciona el número del backup a restaurar (0 para cancelar): "))
        
        if seleccion == 0:
            print("❌ Restauración cancelada")
            exit(0)
        
        if seleccion < 1 or seleccion > len(backups):
            print("❌ Selección inválida")
            exit(1)
        
        backup_seleccionado = backups[seleccion - 1]
        
        # Restaurar
        if restaurar_backup(backup_seleccionado):
            print("\n" + "=" * 80)
            print("✅ Proceso de restauración completado exitosamente")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("❌ Proceso de restauración falló")
            print("=" * 80)
            exit(1)
            
    except ValueError:
        print("❌ Entrada inválida. Debes ingresar un número.")
        exit(1)
    except KeyboardInterrupt:
        print("\n❌ Restauración cancelada por el usuario")
        exit(1)


if __name__ == "__main__":
    main()
