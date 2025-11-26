"""
Módulo de gestión de cursos y escuelas
Conecta con APIs o scraping para obtener cursos actualizados
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import json
from database.models import get_db
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Curso(Base):
    __tablename__ = 'cursos'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(500), nullable=False)
    especialidad = Column(String(255))
    duracion_meses = Column(Integer)
    ciudad = Column(String(100))
    escuela = Column(String(300))
    nivel_idioma_requerido = Column(String(50))
    precio = Column(Float)
    link_inscripcion = Column(Text)
    fecha_inicio = Column(DateTime)
    fecha_limite_inscripcion = Column(DateTime)
    descripcion = Column(Text)
    requisitos = Column(JSON)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Escuela(Base):
    __tablename__ = 'escuelas'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(300), nullable=False)
    ciudad = Column(String(100))
    tipo = Column(String(100))  # universidad, escuela_idiomas, instituto, etc.
    direccion = Column(Text)
    telefono = Column(String(50))
    email = Column(String(255))
    website = Column(Text)
    descripcion = Column(Text)
    api_url = Column(Text)  # URL de API si está disponible
    api_key = Column(String(255))
    activa = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class GestorCursos:
    """Gestor principal de cursos y escuelas"""
    
    @staticmethod
    def obtener_cursos(api_url: str = None, escuela_id: int = None) -> List[Dict]:
        """
        Conecta con APIs de universidades/escuelas para traer cursos actualizados.
        Si no hay API, usar web scraping legal de páginas públicas.
        
        Args:
            api_url: URL de la API de la escuela
            escuela_id: ID de la escuela en la base de datos
            
        Returns:
            Lista de diccionarios con información de cursos
        """
        cursos = []
        
        try:
            if api_url:
                # Intentar obtener vía API
                cursos = GestorCursos._obtener_via_api(api_url)
            elif escuela_id:
                # Obtener de la base de datos
                db = get_db()
                escuela = db.query(Escuela).filter(Escuela.id == escuela_id).first()
                if escuela and escuela.api_url:
                    cursos = GestorCursos._obtener_via_api(escuela.api_url, escuela.api_key)
                elif escuela and escuela.website:
                    # Fallback a scraping si no hay API
                    cursos = GestorCursos._obtener_via_scraping(escuela.website)
            
            # Guardar/actualizar en base de datos
            if cursos:
                GestorCursos._guardar_cursos(cursos)
            
            return cursos
            
        except Exception as e:
            print(f"Error obteniendo cursos: {e}")
            return []
    
    @staticmethod
    def _obtener_via_api(api_url: str, api_key: str = None) -> List[Dict]:
        """Obtiene cursos vía API"""
        headers = {}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Normalizar formato (depende de cada API)
            cursos = []
            if isinstance(data, list):
                for item in data:
                    curso = GestorCursos._normalizar_curso_api(item)
                    cursos.append(curso)
            
            return cursos
        except Exception as e:
            print(f"Error en API: {e}")
            return []
    
    @staticmethod
    def _obtener_via_scraping(website_url: str) -> List[Dict]:
        """
        Obtiene cursos mediante web scraping (solo páginas públicas)
        IMPORTANTE: Solo usar en sitios con términos que lo permitan
        """
        cursos = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(website_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # EJEMPLO: Adaptar según estructura real del sitio
            # Esto es solo un template genérico
            cursos_html = soup.find_all('div', class_='curso-item')
            
            for curso_html in cursos_html:
                try:
                    nombre = curso_html.find('h3').text.strip()
                    duracion = curso_html.find('span', class_='duracion')
                    precio = curso_html.find('span', class_='precio')
                    link = curso_html.find('a')['href']
                    
                    curso = {
                        'nombre': nombre,
                        'duracion_meses': int(duracion.text) if duracion else None,
                        'precio': float(precio.text.replace('€', '').replace(',', '')) if precio else None,
                        'link_inscripcion': link,
                        'website_origen': website_url
                    }
                    cursos.append(curso)
                except:
                    continue
            
            return cursos
            
        except Exception as e:
            print(f"Error en scraping: {e}")
            return []
    
    @staticmethod
    def _normalizar_curso_api(data: Dict) -> Dict:
        """Normaliza datos de curso de diferentes APIs a formato estándar"""
        return {
            'nombre': data.get('name') or data.get('title') or data.get('nombre'),
            'especialidad': data.get('specialty') or data.get('area') or data.get('especialidad'),
            'duracion_meses': data.get('duration_months') or data.get('duracion'),
            'ciudad': data.get('city') or data.get('location') or data.get('ciudad'),
            'escuela': data.get('school') or data.get('institution') or data.get('escuela'),
            'nivel_idioma_requerido': data.get('language_level') or data.get('nivel_idioma'),
            'precio': data.get('price') or data.get('cost') or data.get('precio'),
            'link_inscripcion': data.get('enrollment_link') or data.get('url') or data.get('link'),
            'fecha_inicio': data.get('start_date') or data.get('fecha_inicio'),
            'fecha_limite_inscripcion': data.get('deadline') or data.get('fecha_limite'),
            'descripcion': data.get('description') or data.get('descripcion'),
            'requisitos': data.get('requirements') or data.get('requisitos') or []
        }
    
    @staticmethod
    def _guardar_cursos(cursos: List[Dict]):
        """Guarda o actualiza cursos en la base de datos"""
        db = get_db()
        
        for curso_data in cursos:
            try:
                # Buscar si ya existe
                curso_existente = db.query(Curso).filter(
                    Curso.nombre == curso_data['nombre'],
                    Curso.escuela == curso_data.get('escuela')
                ).first()
                
                if curso_existente:
                    # Actualizar
                    for key, value in curso_data.items():
                        if hasattr(curso_existente, key):
                            setattr(curso_existente, key, value)
                    curso_existente.updated_at = datetime.utcnow()
                else:
                    # Crear nuevo
                    nuevo_curso = Curso(**curso_data)
                    db.add(nuevo_curso)
                
                db.commit()
            except Exception as e:
                print(f"Error guardando curso: {e}")
                db.rollback()
    
    @staticmethod
    def filtrar_cursos(
        especialidad: str = None,
        duracion: int = None,
        ciudad: str = None,
        nivel_idioma: str = None,
        precio_max: float = None
    ) -> List[Curso]:
        """
        Filtra cursos según criterios del estudiante
        
        Args:
            especialidad: Área de estudio (ej: 'informatica', 'medicina', etc.)
            duracion: Duración en meses
            ciudad: Ciudad de preferencia
            nivel_idioma: Nivel de español requerido (A1, A2, B1, B2, C1, C2)
            precio_max: Precio máximo
            
        Returns:
            Lista de cursos que cumplen los criterios
        """
        db = get_db()
        query = db.query(Curso).filter(Curso.activo == True)
        
        if especialidad:
            query = query.filter(Curso.especialidad.ilike(f'%{especialidad}%'))
        
        if duracion:
            # Rango de +/- 2 meses
            query = query.filter(
                Curso.duracion_meses >= duracion - 2,
                Curso.duracion_meses <= duracion + 2
            )
        
        if ciudad:
            query = query.filter(Curso.ciudad.ilike(f'%{ciudad}%'))
        
        if nivel_idioma:
            # Convertir niveles a números para comparar
            niveles = {'a1': 1, 'a2': 2, 'b1': 3, 'b2': 4, 'c1': 5, 'c2': 6}
            nivel_estudiante = niveles.get(nivel_idioma.lower(), 0)
            
            # Filtrar cursos donde el nivel requerido sea <= nivel del estudiante
            cursos_temp = query.all()
            cursos_filtrados = []
            for curso in cursos_temp:
                if curso.nivel_idioma_requerido:
                    nivel_requerido = niveles.get(curso.nivel_idioma_requerido.lower(), 6)
                    if nivel_estudiante >= nivel_requerido:
                        cursos_filtrados.append(curso)
                else:
                    cursos_filtrados.append(curso)
            
            return cursos_filtrados
        
        if precio_max:
            query = query.filter(Curso.precio <= precio_max)
        
        return query.all()
    
    @staticmethod
    def alertar_nuevos_cursos(telegram_id: int = None) -> List[Dict]:
        """
        Identifica nuevos cursos o cambios importantes y genera alertas
        
        Args:
            telegram_id: ID del usuario para enviar alerta específica
            
        Returns:
            Lista de alertas generadas
        """
        db = get_db()
        alertas = []
        
        # Cursos agregados en las últimas 24 horas
        from datetime import timedelta
        hace_24h = datetime.utcnow() - timedelta(hours=24)
        
        cursos_nuevos = db.query(Curso).filter(
            Curso.created_at >= hace_24h,
            Curso.activo == True
        ).all()
        
        for curso in cursos_nuevos:
            alerta = {
                'tipo': 'nuevo_curso',
                'curso_id': curso.id,
                'titulo': f'🆕 Nuevo curso disponible: {curso.nombre}',
                'mensaje': f"""
**{curso.nombre}**

🏫 Escuela: {curso.escuela}
🌍 Ciudad: {curso.ciudad}
⏱️ Duración: {curso.duracion_meses} meses
💰 Precio: {curso.precio}€
🗣️ Nivel idioma: {curso.nivel_idioma_requerido or 'No especificado'}

📋 Descripción: {curso.descripcion[:200] if curso.descripcion else 'N/A'}...

🔗 [Más información]({curso.link_inscripcion})
""",
                'fecha': curso.created_at
            }
            alertas.append(alerta)
        
        # Cursos con fecha límite próxima (7 días)
        en_7_dias = datetime.utcnow() + timedelta(days=7)
        
        cursos_urgentes = db.query(Curso).filter(
            Curso.fecha_limite_inscripcion <= en_7_dias,
            Curso.fecha_limite_inscripcion >= datetime.utcnow(),
            Curso.activo == True
        ).all()
        
        for curso in cursos_urgentes:
            dias_restantes = (curso.fecha_limite_inscripcion - datetime.utcnow()).days
            alerta = {
                'tipo': 'deadline_proximo',
                'curso_id': curso.id,
                'titulo': f'⚠️ URGENTE: {curso.nombre} - Cierra en {dias_restantes} días',
                'mensaje': f"""
⏰ **FECHA LÍMITE PRÓXIMA**

{curso.nombre}
🏫 {curso.escuela}

📅 Fecha límite inscripción: {curso.fecha_limite_inscripcion.strftime('%d/%m/%Y')}
⚠️ Quedan solo {dias_restantes} días

🔗 [Inscribirse ahora]({curso.link_inscripcion})
""",
                'fecha': datetime.utcnow(),
                'urgente': True
            }
            alertas.append(alerta)
        
        return alertas
    
    @staticmethod
    def buscar_cursos_texto(texto: str, limite: int = 10) -> List[Curso]:
        """
        Búsqueda de texto completo en cursos
        
        Args:
            texto: Término de búsqueda
            limite: Número máximo de resultados
            
        Returns:
            Lista de cursos que coinciden
        """
        db = get_db()
        
        cursos = db.query(Curso).filter(
            Curso.activo == True
        ).filter(
            (Curso.nombre.ilike(f'%{texto}%')) |
            (Curso.especialidad.ilike(f'%{texto}%')) |
            (Curso.descripcion.ilike(f'%{texto}%')) |
            (Curso.escuela.ilike(f'%{texto}%'))
        ).limit(limite).all()
        
        return cursos
    
    @staticmethod
    def obtener_curso_por_id(curso_id: int) -> Optional[Curso]:
        """Obtiene un curso específico por ID"""
        db = get_db()
        return db.query(Curso).filter(Curso.id == curso_id).first()
    
    @staticmethod
    def registrar_escuela(datos_escuela: Dict) -> Escuela:
        """
        Registra una nueva escuela en el sistema
        
        Args:
            datos_escuela: Diccionario con información de la escuela
            
        Returns:
            Objeto Escuela creado
        """
        db = get_db()
        
        escuela = Escuela(**datos_escuela)
        db.add(escuela)
        db.commit()
        db.refresh(escuela)
        
        return escuela
    
    @staticmethod
    def listar_escuelas(activas_solo: bool = True) -> List[Escuela]:
        """Lista todas las escuelas registradas"""
        db = get_db()
        query = db.query(Escuela)
        
        if activas_solo:
            query = query.filter(Escuela.activa == True)
        
        return query.all()
    
    @staticmethod
    def sincronizar_cursos_todas_escuelas():
        """
        Sincroniza cursos de todas las escuelas con API o scraping
        Usar en tareas programadas (cron job)
        """
        escuelas = GestorCursos.listar_escuelas()
        resultados = {
            'exitosas': 0,
            'fallidas': 0,
            'cursos_nuevos': 0
        }
        
        for escuela in escuelas:
            try:
                cursos_antes = len(GestorCursos.filtrar_cursos())
                GestorCursos.obtener_cursos(escuela_id=escuela.id)
                cursos_despues = len(GestorCursos.filtrar_cursos())
                
                resultados['exitosas'] += 1
                resultados['cursos_nuevos'] += (cursos_despues - cursos_antes)
                
            except Exception as e:
                print(f"Error sincronizando {escuela.nombre}: {e}")
                resultados['fallidas'] += 1
        
        return resultados


# Ejemplos de escuelas predefinidas para Cuba -> España
ESCUELAS_PREDEFINIDAS = [
    {
        'nombre': 'Universidad Complutense de Madrid',
        'ciudad': 'Madrid',
        'tipo': 'universidad_publica',
        'website': 'https://www.ucm.es',
        'descripcion': 'Una de las universidades más antiguas y prestigiosas de España'
    },
    {
        'nombre': 'Universidad de Barcelona',
        'ciudad': 'Barcelona',
        'tipo': 'universidad_publica',
        'website': 'https://www.ub.edu',
        'descripcion': 'Principal universidad de Cataluña'
    },
    {
        'nombre': 'Instituto Cervantes',
        'ciudad': 'Múltiples ciudades',
        'tipo': 'escuela_idiomas',
        'website': 'https://www.cervantes.es',
        'descripcion': 'Red de centros para la enseñanza del español'
    },
    {
        'nombre': 'Universidad Autónoma de Madrid',
        'ciudad': 'Madrid',
        'tipo': 'universidad_publica',
        'website': 'https://www.uam.es',
        'descripcion': 'Universidad pública de alto prestigio académico'
    }
]


def inicializar_escuelas_predefinidas():
    """Carga escuelas predefinidas en la base de datos"""
    for escuela_data in ESCUELAS_PREDEFINIDAS:
        try:
            db = get_db()
            existe = db.query(Escuela).filter(
                Escuela.nombre == escuela_data['nombre']
            ).first()
            
            if not existe:
                GestorCursos.registrar_escuela(escuela_data)
                print(f"✅ Escuela registrada: {escuela_data['nombre']}")
        except Exception as e:
            print(f"Error registrando escuela: {e}")
