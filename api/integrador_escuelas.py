"""
Sistema de integración con APIs y scraping de escuelas españolas
Obtiene cursos actualizados, precios y disponibilidad en tiempo real
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import json


class IntegradorEscuelas:
    """Integrador con APIs y web scraping de escuelas"""
    
    @staticmethod
    def obtener_cursos_universidad_barcelona() -> List[Dict]:
        """
        Scraping simulado de Universidad de Barcelona
        En producción, usar API real o scraping actualizado
        """
        # Simulación de datos - En producción conectar a API real
        cursos = [
            {
                "universidad": "Universidad de Barcelona",
                "nombre": "Máster en Ingeniería Informática",
                "descripcion": "Programa avanzado en desarrollo de software y sistemas",
                "duracion_meses": 12,
                "precio_eur": 6500,
                "ciudad": "Barcelona",
                "nivel_espanol_requerido": "B2",
                "cupos_disponibles": 25,
                "fecha_inicio": "2025-09-01",
                "url": "https://www.ub.edu",
                "requisitos": ["Título universitario", "Nivel B2 español", "Certificado académico"],
                "modalidad": "Presencial"
            },
            {
                "universidad": "Universidad de Barcelona",
                "nombre": "MBA - Administración de Empresas",
                "descripcion": "Master en administración y gestión empresarial",
                "duracion_meses": 18,
                "precio_eur": 8500,
                "ciudad": "Barcelona",
                "nivel_espanol_requerido": "C1",
                "cupos_disponibles": 15,
                "fecha_inicio": "2025-09-15",
                "url": "https://www.ub.edu",
                "requisitos": ["Título universitario", "3 años experiencia", "Nivel C1 español"],
                "modalidad": "Presencial"
            }
        ]
        return cursos
    
    @staticmethod
    def obtener_cursos_universidad_madrid() -> List[Dict]:
        """Scraping simulado de Universidad Complutense de Madrid"""
        cursos = [
            {
                "universidad": "Universidad Complutense de Madrid",
                "nombre": "Máster en Derecho Internacional",
                "descripcion": "Especialización en derecho internacional y europeo",
                "duracion_meses": 12,
                "precio_eur": 5800,
                "ciudad": "Madrid",
                "nivel_espanol_requerido": "C1",
                "cupos_disponibles": 20,
                "fecha_inicio": "2025-10-01",
                "url": "https://www.ucm.es",
                "requisitos": ["Licenciatura en Derecho", "Nivel C1 español"],
                "modalidad": "Presencial"
            },
            {
                "universidad": "Universidad Complutense de Madrid",
                "nombre": "Doctorado en Medicina",
                "descripcion": "Programa doctoral en ciencias médicas",
                "duracion_meses": 36,
                "precio_eur": 12000,
                "ciudad": "Madrid",
                "nivel_espanol_requerido": "C1",
                "cupos_disponibles": 10,
                "fecha_inicio": "2025-09-01",
                "url": "https://www.ucm.es",
                "requisitos": ["Máster en Medicina", "Publicaciones científicas", "Nivel C1 español"],
                "modalidad": "Presencial"
            }
        ]
        return cursos
    
    @staticmethod
    def obtener_cursos_universidad_valencia() -> List[Dict]:
        """Scraping simulado de Universidad de Valencia"""
        cursos = [
            {
                "universidad": "Universidad de Valencia",
                "nombre": "Máster en Biotecnología",
                "descripcion": "Programa avanzado en biotecnología y genética",
                "duracion_meses": 12,
                "precio_eur": 5500,
                "ciudad": "Valencia",
                "nivel_espanol_requerido": "B2",
                "cupos_disponibles": 18,
                "fecha_inicio": "2025-09-15",
                "url": "https://www.uv.es",
                "requisitos": ["Grado en Biología o afines", "Nivel B2 español"],
                "modalidad": "Presencial"
            },
            {
                "universidad": "Universidad de Valencia",
                "nombre": "Curso Intensivo de Español",
                "descripcion": "Curso de español para extranjeros - Nivel A1 a C2",
                "duracion_meses": 6,
                "precio_eur": 2800,
                "ciudad": "Valencia",
                "nivel_espanol_requerido": "A1",
                "cupos_disponibles": 50,
                "fecha_inicio": "2025-07-01",
                "url": "https://www.uv.es",
                "requisitos": ["Pasaporte vigente"],
                "modalidad": "Presencial"
            }
        ]
        return cursos
    
    @staticmethod
    def obtener_cursos_escuelas_idiomas() -> List[Dict]:
        """Cursos de escuelas de idiomas especializadas"""
        cursos = [
            {
                "universidad": "Escuela Cervantes - Madrid",
                "nombre": "Español Intensivo B1-B2",
                "descripcion": "Curso intensivo de español con preparación DELE",
                "duracion_meses": 3,
                "precio_eur": 1800,
                "ciudad": "Madrid",
                "nivel_espanol_requerido": "A2",
                "cupos_disponibles": 30,
                "fecha_inicio": "2025-08-01",
                "url": "https://www.cervantes.es",
                "requisitos": ["Nivel A2 previo"],
                "modalidad": "Presencial"
            },
            {
                "universidad": "Don Quijote - Barcelona",
                "nombre": "Español + Cultura Española",
                "descripcion": "Curso de español con actividades culturales",
                "duracion_meses": 6,
                "precio_eur": 3200,
                "ciudad": "Barcelona",
                "nivel_espanol_requerido": "A1",
                "cupos_disponibles": 40,
                "fecha_inicio": "2025-07-15",
                "url": "https://www.donquijote.org",
                "requisitos": ["Sin requisitos previos"],
                "modalidad": "Presencial"
            }
        ]
        return cursos
    
    @classmethod
    def sincronizar_todos_cursos(cls) -> List[Dict]:
        """
        Obtiene cursos de todas las fuentes y los devuelve consolidados
        """
        todos_cursos = []
        
        try:
            todos_cursos.extend(cls.obtener_cursos_universidad_barcelona())
        except Exception as e:
            print(f"Error UB: {e}")
        
        try:
            todos_cursos.extend(cls.obtener_cursos_universidad_madrid())
        except Exception as e:
            print(f"Error UCM: {e}")
        
        try:
            todos_cursos.extend(cls.obtener_cursos_universidad_valencia())
        except Exception as e:
            print(f"Error UV: {e}")
        
        try:
            todos_cursos.extend(cls.obtener_cursos_escuelas_idiomas())
        except Exception as e:
            print(f"Error Escuelas: {e}")
        
        return todos_cursos
    
    @staticmethod
    def buscar_cursos_por_especialidad(especialidad: str, cursos: List[Dict]) -> List[Dict]:
        """Filtra cursos por especialidad"""
        especialidad_lower = especialidad.lower()
        resultados = []
        
        for curso in cursos:
            if (especialidad_lower in curso['nombre'].lower() or 
                especialidad_lower in curso['descripcion'].lower()):
                resultados.append(curso)
        
        return resultados
    
    @staticmethod
    def filtrar_por_presupuesto(cursos: List[Dict], presupuesto_max: float) -> List[Dict]:
        """Filtra cursos que estén dentro del presupuesto"""
        return [c for c in cursos if c['precio_eur'] <= presupuesto_max]
    
    @staticmethod
    def filtrar_por_ciudad(cursos: List[Dict], ciudad: str) -> List[Dict]:
        """Filtra cursos por ciudad"""
        ciudad_lower = ciudad.lower()
        return [c for c in cursos if ciudad_lower in c['ciudad'].lower()]
    
    @staticmethod
    def actualizar_disponibilidad_real(curso_id: int) -> Optional[int]:
        """
        Consulta disponibilidad real de un curso específico
        En producción, hacer llamada a API de la universidad
        """
        # Simulación - en producción hacer request real
        import random
        return random.randint(0, 50)


class APIEscuelasEjemplo:
    """
    Ejemplo de integración con API REST real
    Template para conectar con APIs de universidades
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api.universidad-ejemplo.es/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Content-Type": "application/json"
        }
    
    def obtener_cursos(self, categoria: str = None) -> List[Dict]:
        """
        Template para obtener cursos de API real
        """
        try:
            # En producción, hacer request real:
            # response = requests.get(
            #     f"{self.base_url}/cursos",
            #     headers=self.headers,
            #     params={"categoria": categoria} if categoria else {}
            # )
            # return response.json()
            
            # Por ahora retornar datos simulados
            return []
        except Exception as e:
            print(f"Error API: {e}")
            return []
    
    def verificar_disponibilidad(self, curso_id: str) -> Dict:
        """Verifica disponibilidad en tiempo real"""
        try:
            # response = requests.get(
            #     f"{self.base_url}/cursos/{curso_id}/disponibilidad",
            #     headers=self.headers
            # )
            # return response.json()
            
            return {"disponible": True, "cupos": 15}
        except Exception as e:
            print(f"Error verificando disponibilidad: {e}")
            return {"disponible": False, "cupos": 0}


class ScraperWeb:
    """
    Scraper genérico para extraer información de sitios web de universidades
    """
    
    @staticmethod
    def extraer_cursos_desde_html(url: str) -> List[Dict]:
        """
        Extrae cursos desde HTML de página web
        Template para scraping real
        """
        try:
            # En producción:
            # response = requests.get(url)
            # soup = BeautifulSoup(response.content, 'html.parser')
            # cursos = []
            # for elemento in soup.find_all('div', class_='curso'):
            #     curso = {
            #         'nombre': elemento.find('h3').text,
            #         'precio': elemento.find('span', class_='precio').text,
            #         ...
            #     }
            #     cursos.append(curso)
            # return cursos
            
            return []
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []
