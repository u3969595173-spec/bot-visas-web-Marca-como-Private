"""
Sistema de scraping para universidades españolas sin API pública
Extrae información de programas, precios, requisitos y fechas
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScraperUniversidadEspana:
    """Scraper genérico para universidades españolas"""
    
    def __init__(self, universidad_nombre, url_base):
        self.universidad_nombre = universidad_nombre
        self.url_base = url_base
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_programas(self):
        """Extrae lista de programas de la universidad"""
        try:
            logger.info(f"Scraping programas de {self.universidad_nombre}")
            # Implementación específica por universidad
            return []
        except Exception as e:
            logger.error(f"Error scraping {self.universidad_nombre}: {e}")
            return []

class ScraperComplutense(ScraperUniversidadEspana):
    """Scraper específico para Universidad Complutense de Madrid"""
    
    def __init__(self):
        super().__init__("Universidad Complutense de Madrid", "https://www.ucm.es")
    
    def scrape_programas(self):
        programas = []
        try:
            # URL de oferta académica
            url_grados = f"{self.url_base}/estudios/grado"
            response = self.session.get(url_grados, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar enlaces de grados
                grados = soup.find_all('a', href=re.compile(r'/grado|/estudios'))
                
                for grado in grados[:20]:  # Limitar a primeros 20
                    nombre = grado.get_text(strip=True)
                    if nombre and len(nombre) > 10:
                        programas.append({
                            'nombre': nombre,
                            'tipo_programa': 'grado',
                            'universidad': self.universidad_nombre,
                            'url_info': self.url_base + grado.get('href', ''),
                            'duracion_anos': 4,
                            'creditos_ects': 240,
                            'idioma': 'español',
                            'modalidad': 'presencial'
                        })
            
            logger.info(f"✅ UCM: {len(programas)} programas encontrados")
        except Exception as e:
            logger.error(f"❌ Error scraping UCM: {e}")
        
        return programas

class ScraperBarcelona(ScraperUniversidadEspana):
    """Scraper específico para Universidad de Barcelona"""
    
    def __init__(self):
        super().__init__("Universidad de Barcelona", "https://www.ub.edu")
    
    def scrape_programas(self):
        programas = []
        try:
            url_estudios = f"{self.url_base}/web/estudis"
            response = self.session.get(url_estudios, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                enlaces_programas = soup.find_all('a', href=re.compile(r'/grau|/master'))
                
                for enlace in enlaces_programas[:20]:
                    nombre = enlace.get_text(strip=True)
                    tipo = 'master' if 'master' in enlace.get('href', '').lower() else 'grado'
                    
                    if nombre and len(nombre) > 10:
                        programas.append({
                            'nombre': nombre,
                            'tipo_programa': tipo,
                            'universidad': self.universidad_nombre,
                            'url_info': enlace.get('href', ''),
                            'duracion_anos': 1 if tipo == 'master' else 4,
                            'idioma': 'español',
                            'modalidad': 'presencial'
                        })
            
            logger.info(f"✅ UB: {len(programas)} programas encontrados")
        except Exception as e:
            logger.error(f"❌ Error scraping UB: {e}")
        
        return programas

class ScraperValencia(ScraperUniversidadEspana):
    """Scraper específico para Universidad de Valencia"""
    
    def __init__(self):
        super().__init__("Universidad de Valencia", "https://www.uv.es")
    
    def scrape_programas(self):
        programas = []
        try:
            url_grados = f"{self.url_base}/estudios/grados"
            response = self.session.get(url_grados, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                enlaces = soup.find_all('a', href=re.compile(r'/grado'))
                
                for enlace in enlaces[:20]:
                    nombre = enlace.get_text(strip=True)
                    if nombre and len(nombre) > 10:
                        programas.append({
                            'nombre': nombre,
                            'tipo_programa': 'grado',
                            'universidad': self.universidad_nombre,
                            'url_info': enlace.get('href', ''),
                            'duracion_anos': 4,
                            'idioma': 'español'
                        })
            
            logger.info(f"✅ UV: {len(programas)} programas encontrados")
        except Exception as e:
            logger.error(f"❌ Error scraping UV: {e}")
        
        return programas

class ScraperGranada(ScraperUniversidadEspana):
    """Scraper específico para Universidad de Granada"""
    
    def __init__(self):
        super().__init__("Universidad de Granada", "https://www.ugr.es")
    
    def scrape_programas(self):
        programas = []
        try:
            # Granada tiene estructura similar a otras
            url_oferta = f"{self.url_base}/estudiantes/grados"
            response = self.session.get(url_oferta, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                enlaces = soup.find_all('a', href=re.compile(r'/grado'))
                
                for enlace in enlaces[:20]:
                    nombre = enlace.get_text(strip=True)
                    if nombre and len(nombre) > 10:
                        programas.append({
                            'nombre': nombre,
                            'tipo_programa': 'grado',
                            'universidad': self.universidad_nombre,
                            'duracion_anos': 4,
                            'idioma': 'español'
                        })
            
            logger.info(f"✅ UGR: {len(programas)} programas encontrados")
        except Exception as e:
            logger.error(f"❌ Error scraping UGR: {e}")
        
        return programas

class ScraperSevilla(ScraperUniversidadEspana):
    """Scraper específico para Universidad de Sevilla"""
    
    def __init__(self):
        super().__init__("Universidad de Sevilla", "https://www.us.es")
    
    def scrape_programas(self):
        programas = []
        try:
            url_estudios = f"{self.url_base}/estudiar/que-estudiar/oferta-de-grados"
            response = self.session.get(url_estudios, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                enlaces = soup.find_all('a', text=re.compile(r'Grado|grado'))
                
                for enlace in enlaces[:20]:
                    nombre = enlace.get_text(strip=True)
                    if 'Grado en' in nombre:
                        programas.append({
                            'nombre': nombre,
                            'tipo_programa': 'grado',
                            'universidad': self.universidad_nombre,
                            'duracion_anos': 4,
                            'idioma': 'español'
                        })
            
            logger.info(f"✅ US: {len(programas)} programas encontrados")
        except Exception as e:
            logger.error(f"❌ Error scraping US: {e}")
        
        return programas

# Mapeo de universidades a sus scrapers
SCRAPERS_DISPONIBLES = {
    'Universidad Complutense de Madrid': ScraperComplutense,
    'Universidad de Barcelona': ScraperBarcelona,
    'Universidad de Valencia': ScraperValencia,
    'Universidad de Granada': ScraperGranada,
    'Universidad de Sevilla': ScraperSevilla
}

def obtener_scraper(universidad_nombre):
    """Devuelve el scraper apropiado para una universidad"""
    scraper_class = SCRAPERS_DISPONIBLES.get(universidad_nombre)
    if scraper_class:
        return scraper_class()
    else:
        # Scraper genérico para universidades sin implementación específica
        return None

def scrape_programas_universidad(universidad_nombre, url_base):
    """
    Extrae programas de una universidad
    Usa scraper específico si existe, o genérico si no
    """
    scraper = obtener_scraper(universidad_nombre)
    
    if scraper:
        return scraper.scrape_programas()
    else:
        logger.info(f"⚠️ No hay scraper específico para {universidad_nombre}")
        return []

def actualizar_todas_universidades(db_session):
    """
    Actualiza datos de todas las universidades configuradas
    Debe ejecutarse periódicamente (diariamente)
    """
    from database.models import UniversidadEspana, ProgramaUniversitario
    
    universidades = db_session.query(UniversidadEspana).filter(
        UniversidadEspana.activa == True,
        UniversidadEspana.metodo_scraping == 'beautifulsoup'
    ).all()
    
    total_programas_nuevos = 0
    
    for universidad in universidades:
        logger.info(f"🔄 Actualizando {universidad.nombre}...")
        
        try:
            programas = scrape_programas_universidad(
                universidad.nombre,
                universidad.url_oficial
            )
            
            for programa_data in programas:
                # Verificar si ya existe
                existe = db_session.query(ProgramaUniversitario).filter(
                    ProgramaUniversitario.universidad_id == universidad.id,
                    ProgramaUniversitario.nombre == programa_data['nombre']
                ).first()
                
                if not existe:
                    nuevo_programa = ProgramaUniversitario(
                        universidad_id=universidad.id,
                        nombre=programa_data['nombre'],
                        tipo_programa=programa_data.get('tipo_programa', 'grado'),
                        duracion_anos=programa_data.get('duracion_anos', 4),
                        creditos_ects=programa_data.get('creditos_ects', 240),
                        idioma=programa_data.get('idioma', 'español'),
                        modalidad=programa_data.get('modalidad', 'presencial'),
                        url_info=programa_data.get('url_info', ''),
                        activo=True
                    )
                    db_session.add(nuevo_programa)
                    total_programas_nuevos += 1
            
            # Actualizar timestamp
            universidad.ultima_actualizacion = datetime.utcnow()
            db_session.commit()
            
            logger.info(f"✅ {universidad.nombre}: OK")
            
        except Exception as e:
            logger.error(f"❌ Error actualizando {universidad.nombre}: {e}")
            db_session.rollback()
    
    logger.info(f"🎉 Actualización completa: {total_programas_nuevos} programas nuevos")
    return total_programas_nuevos
