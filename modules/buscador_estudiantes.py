"""
Sistema de Búsqueda y Filtros Avanzados
Permite búsquedas complejas de estudiantes
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from modules.estudiantes import Estudiante
from database.models import get_db
from sqlalchemy import or_, and_


class BuscadorEstudiantes:
    """Sistema avanzado de búsqueda de estudiantes"""
    
    @staticmethod
    def buscar(
        nombre: str = None,
        nacionalidad: str = None,
        especialidad: str = None,
        estado_procesamiento: str = None,
        estado_visa: str = None,
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None,
        edad_min: int = None,
        edad_max: int = None,
        ciudad: str = None,
        nivel_espanol: str = None,
        admin_revisor_id: int = None,
        fondos_suficientes: bool = None,
        documentos_completos: bool = None
    ) -> List[Estudiante]:
        """
        Búsqueda avanzada con múltiples filtros
        
        Args:
            Múltiples parámetros opcionales de búsqueda
            
        Returns:
            Lista de estudiantes que coinciden
        """
        db = get_db()
        
        try:
            query = db.query(Estudiante)
            
            # Filtro por nombre (búsqueda parcial)
            if nombre:
                query = query.filter(Estudiante.nombre_completo.ilike(f'%{nombre}%'))
            
            # Filtro por nacionalidad
            if nacionalidad:
                query = query.filter(Estudiante.nacionalidad.ilike(f'%{nacionalidad}%'))
            
            # Filtro por especialidad
            if especialidad:
                query = query.filter(Estudiante.especialidad_interes.ilike(f'%{especialidad}%'))
            
            # Filtro por estado de procesamiento
            if estado_procesamiento:
                query = query.filter(Estudiante.estado_procesamiento == estado_procesamiento)
            
            # Filtro por estado de visa
            if estado_visa:
                query = query.filter(Estudiante.estado_visa == estado_visa)
            
            # Filtro por rango de fechas
            if fecha_desde:
                query = query.filter(Estudiante.created_at >= fecha_desde)
            
            if fecha_hasta:
                query = query.filter(Estudiante.created_at <= fecha_hasta)
            
            # Filtro por edad
            if edad_min:
                query = query.filter(Estudiante.edad >= edad_min)
            
            if edad_max:
                query = query.filter(Estudiante.edad <= edad_max)
            
            # Filtro por ciudad
            if ciudad:
                query = query.filter(Estudiante.ciudad_origen.ilike(f'%{ciudad}%'))
            
            # Filtro por nivel de español
            if nivel_espanol:
                query = query.filter(Estudiante.nivel_espanol == nivel_espanol)
            
            # Filtro por admin revisor
            if admin_revisor_id:
                query = query.filter(Estudiante.admin_revisor_id == admin_revisor_id)
            
            resultados = query.all()
            
            # Filtros adicionales (post-query)
            if fondos_suficientes is not None or documentos_completos is not None:
                resultados_filtrados = []
                
                for est in resultados:
                    incluir = True
                    
                    if fondos_suficientes is not None:
                        from modules.fondos import GestorFondos
                        try:
                            verificacion = GestorFondos.verificar_fondos(est.id)
                            if verificacion['fondos_suficientes'] != fondos_suficientes:
                                incluir = False
                        except:
                            incluir = False
                    
                    if documentos_completos is not None and incluir:
                        total_docs = len(est.documentos_completados or []) + len(est.documentos_pendientes or [])
                        completos = len(est.documentos_completados or []) == total_docs if total_docs > 0 else False
                        if completos != documentos_completos:
                            incluir = False
                    
                    if incluir:
                        resultados_filtrados.append(est)
                
                return resultados_filtrados
            
            return resultados
            
        finally:
            db.close()
    
    @staticmethod
    def busqueda_rapida(texto: str) -> List[Estudiante]:
        """
        Búsqueda rápida por nombre, pasaporte o email
        
        Args:
            texto: Texto a buscar
            
        Returns:
            Lista de estudiantes
        """
        db = get_db()
        
        try:
            resultados = db.query(Estudiante).filter(
                or_(
                    Estudiante.nombre_completo.ilike(f'%{texto}%'),
                    Estudiante.numero_pasaporte.ilike(f'%{texto}%'),
                    Estudiante.email.ilike(f'%{texto}%')
                )
            ).limit(20).all()
            
            return resultados
            
        finally:
            db.close()
    
    @staticmethod
    def filtros_predefinidos(filtro: str) -> List[Estudiante]:
        """
        Filtros predefinidos comunes
        
        Args:
            filtro: Nombre del filtro ('pendientes', 'urgentes', 'sin_fondos', 'sin_documentos')
            
        Returns:
            Lista de estudiantes
        """
        if filtro == 'pendientes':
            return BuscadorEstudiantes.buscar(
                estado_procesamiento='pendiente_revision_admin'
            )
        
        elif filtro == 'urgentes':
            fecha_limite = datetime.now() + timedelta(days=30)
            return BuscadorEstudiantes.buscar(
                fecha_hasta=fecha_limite
            )
        
        elif filtro == 'sin_fondos':
            return BuscadorEstudiantes.buscar(fondos_suficientes=False)
        
        elif filtro == 'sin_documentos':
            return BuscadorEstudiantes.buscar(documentos_completos=False)
        
        else:
            return []
