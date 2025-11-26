"""
Sistema de caché para cursos scraped
Evita scraping excesivo y mejora rendimiento
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import hashlib


class CacheManager:
    """Gestor de caché para cursos externos"""
    
    CACHE_DIR = "cache"
    CACHE_DURATION_HOURS = 24
    
    def __init__(self):
        # Crear directorio cache si no existe
        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)
    
    def _get_cache_key(self, source: str, filters: Dict = None) -> str:
        """Genera clave única para cache basada en fuente y filtros"""
        filter_str = json.dumps(filters or {}, sort_keys=True)
        key = f"{source}_{filter_str}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Ruta del archivo de cache"""
        return os.path.join(self.CACHE_DIR, f"{cache_key}.json")
    
    def get(self, source: str, filters: Dict = None) -> Optional[List[Dict]]:
        """
        Obtiene cursos del cache si existen y no han expirado
        
        Args:
            source: Fuente de datos (ej: 'educations', 'emagister')
            filters: Filtros aplicados (ej: {'especialidad': 'ingenieria'})
        
        Returns:
            Lista de cursos o None si no hay cache válido
        """
        cache_key = self._get_cache_key(source, filters)
        cache_path = self._get_cache_path(cache_key)
        
        # Verificar si existe el archivo
        if not os.path.exists(cache_path):
            print(f"⚠️ No existe cache para {source}")
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verificar expiración
            cached_at = datetime.fromisoformat(data['timestamp'])
            expires_at = cached_at + timedelta(hours=self.CACHE_DURATION_HOURS)
            
            if datetime.now() > expires_at:
                print(f"⏰ Cache expirado para {source} (más de {self.CACHE_DURATION_HOURS}h)")
                os.remove(cache_path)  # Eliminar cache expirado
                return None
            
            # Cache válido
            hours_ago = (datetime.now() - cached_at).total_seconds() / 3600
            print(f"✅ Cache válido para {source} ({hours_ago:.1f}h antiguos, {len(data['cursos'])} cursos)")
            return data['cursos']
            
        except Exception as e:
            print(f"❌ Error leyendo cache: {e}")
            return None
    
    def set(self, source: str, cursos: List[Dict], filters: Dict = None):
        """
        Guarda cursos en cache
        
        Args:
            source: Fuente de datos
            cursos: Lista de cursos a cachear
            filters: Filtros aplicados
        """
        cache_key = self._get_cache_key(source, filters)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'source': source,
                'filters': filters or {},
                'cursos': cursos,
                'count': len(cursos)
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Cache guardado: {source} ({len(cursos)} cursos)")
            
        except Exception as e:
            print(f"❌ Error guardando cache: {e}")
    
    def clear(self, source: str = None):
        """
        Limpia cache
        
        Args:
            source: Si se especifica, solo borra cache de esa fuente.
                   Si es None, borra todo el cache.
        """
        try:
            if source:
                # Borrar cache específico
                for filename in os.listdir(self.CACHE_DIR):
                    if filename.startswith(source):
                        os.remove(os.path.join(self.CACHE_DIR, filename))
                print(f"🗑️ Cache borrado: {source}")
            else:
                # Borrar todo el cache
                for filename in os.listdir(self.CACHE_DIR):
                    os.remove(os.path.join(self.CACHE_DIR, filename))
                print("🗑️ Todo el cache ha sido borrado")
        except Exception as e:
            print(f"❌ Error limpiando cache: {e}")
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del cache"""
        stats = {
            'total_files': 0,
            'total_cursos': 0,
            'sources': {},
            'oldest': None,
            'newest': None
        }
        
        try:
            for filename in os.listdir(self.CACHE_DIR):
                if filename.endswith('.json'):
                    stats['total_files'] += 1
                    
                    with open(os.path.join(self.CACHE_DIR, filename), 'r') as f:
                        data = json.load(f)
                        
                        source = data.get('source', 'unknown')
                        count = data.get('count', 0)
                        timestamp = data.get('timestamp')
                        
                        if source not in stats['sources']:
                            stats['sources'][source] = {'files': 0, 'cursos': 0}
                        
                        stats['sources'][source]['files'] += 1
                        stats['sources'][source]['cursos'] += count
                        stats['total_cursos'] += count
                        
                        # Track oldest/newest
                        if timestamp:
                            if not stats['oldest'] or timestamp < stats['oldest']:
                                stats['oldest'] = timestamp
                            if not stats['newest'] or timestamp > stats['newest']:
                                stats['newest'] = timestamp
        
        except Exception as e:
            print(f"Error getting cache stats: {e}")
        
        return stats
