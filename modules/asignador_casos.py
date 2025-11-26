"""
Sistema de Asignación de Casos a Admins
Distribuye estudiantes automáticamente entre admins
"""

from typing import List, Dict
from modules.estudiantes import Estudiante
from database.models import get_db
from datetime import datetime


class AsignadorCasos:
    """Asigna casos a admins automáticamente"""
    
    # Configuración de admins y sus especialidades
    ADMINS = {
        1: {'nombre': 'Admin Principal', 'especialidades': ['todas'], 'carga_maxima': 20},
        2: {'nombre': 'Especialista Ingeniería', 'especialidades': ['ingenieria', 'tecnologia'], 'carga_maxima': 15},
        3: {'nombre': 'Especialista Salud', 'especialidades': ['medicina', 'enfermeria'], 'carga_maxima': 15},
    }
    
    @staticmethod
    def asignar_automaticamente(estudiante_id: int) -> Dict:
        """
        Asigna estudiante a un admin automáticamente
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Dict con resultado de asignación
        """
        from modules.estudiantes import GestorEstudiantes
        
        db = get_db()
        
        try:
            estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
            
            if not estudiante:
                return {'exito': False, 'error': 'Estudiante no encontrado'}
            
            # Determinar mejor admin
            admin_id = AsignadorCasos._seleccionar_admin(estudiante)
            
            # Asignar
            estudiante.admin_revisor_id = admin_id
            estudiante.fecha_asignacion_admin = datetime.utcnow()
            db.commit()
            
            admin_info = AsignadorCasos.ADMINS.get(admin_id, {})
            
            return {
                'exito': True,
                'admin_id': admin_id,
                'admin_nombre': admin_info.get('nombre', f'Admin {admin_id}'),
                'motivo_asignacion': AsignadorCasos._explicar_asignacion(estudiante, admin_id)
            }
            
        finally:
            db.close()
    
    @staticmethod
    def _seleccionar_admin(estudiante: Estudiante) -> int:
        """Selecciona el mejor admin para un estudiante"""
        
        # Obtener carga actual de cada admin
        db = get_db()
        
        try:
            cargas = {}
            for admin_id in AsignadorCasos.ADMINS.keys():
                carga = db.query(Estudiante).filter(
                    Estudiante.admin_revisor_id == admin_id,
                    Estudiante.estado_procesamiento.in_([
                        'pendiente_revision_admin',
                        'aprobado_admin'
                    ])
                ).count()
                
                cargas[admin_id] = carga
            
            # Filtrar admins por especialidad
            especialidad = estudiante.especialidad_interes.lower() if estudiante.especialidad_interes else ''
            
            candidatos = []
            for admin_id, config in AsignadorCasos.ADMINS.items():
                # Verificar carga máxima
                if cargas[admin_id] >= config['carga_maxima']:
                    continue
                
                # Verificar especialidad
                if 'todas' in config['especialidades']:
                    candidatos.append((admin_id, 100))  # Score máximo
                else:
                    for esp in config['especialidades']:
                        if esp in especialidad:
                            candidatos.append((admin_id, 90))  # Score alto
                            break
            
            # Si no hay especialistas, asignar a quien tenga menos carga
            if not candidatos:
                admin_menos_carga = min(cargas.items(), key=lambda x: x[1])
                return admin_menos_carga[0]
            
            # Retornar admin con mejor score y menos carga
            candidatos_ordenados = sorted(candidatos, key=lambda x: (x[1], -cargas[x[0]]), reverse=True)
            return candidatos_ordenados[0][0]
            
        finally:
            db.close()
    
    @staticmethod
    def _explicar_asignacion(estudiante: Estudiante, admin_id: int) -> str:
        """Explica por qué se asignó a ese admin"""
        admin = AsignadorCasos.ADMINS.get(admin_id, {})
        
        if 'todas' in admin.get('especialidades', []):
            return "Admin principal - Maneja todas las especialidades"
        
        for esp in admin.get('especialidades', []):
            if estudiante.especialidad_interes and esp in estudiante.especialidad_interes.lower():
                return f"Especialista en {esp.title()}"
        
        return "Asignación por carga de trabajo equilibrada"
    
    @staticmethod
    def reasignar_admin(estudiante_id: int, nuevo_admin_id: int, motivo: str) -> Dict:
        """Reasigna estudiante a otro admin"""
        db = get_db()
        
        try:
            estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
            
            if not estudiante:
                return {'exito': False, 'error': 'Estudiante no encontrado'}
            
            admin_anterior = estudiante.admin_revisor_id
            estudiante.admin_revisor_id = nuevo_admin_id
            estudiante.fecha_asignacion_admin = datetime.utcnow()
            
            db.commit()
            
            # Registrar en auditoría
            from modules.auditoria import AuditoriaEstudiante
            AuditoriaEstudiante.registrar_cambio(
                estudiante_id=estudiante_id,
                admin_id=nuevo_admin_id,
                tipo_accion='reasignacion',
                motivo=motivo,
                campo_modificado='admin_revisor_id',
                valor_anterior=str(admin_anterior),
                valor_nuevo=str(nuevo_admin_id)
            )
            
            return {'exito': True, 'nuevo_admin': nuevo_admin_id}
            
        finally:
            db.close()
    
    @staticmethod
    def estadisticas_carga() -> Dict:
        """Estadísticas de carga por admin"""
        db = get_db()
        
        try:
            stats = {}
            
            for admin_id, config in AsignadorCasos.ADMINS.items():
                pendientes = db.query(Estudiante).filter(
                    Estudiante.admin_revisor_id == admin_id,
                    Estudiante.estado_procesamiento == 'pendiente_revision_admin'
                ).count()
                
                total_asignados = db.query(Estudiante).filter(
                    Estudiante.admin_revisor_id == admin_id
                ).count()
                
                stats[admin_id] = {
                    'nombre': config['nombre'],
                    'pendientes': pendientes,
                    'total_asignados': total_asignados,
                    'carga_maxima': config['carga_maxima'],
                    'porcentaje_carga': (pendientes / config['carga_maxima']) * 100
                }
            
            return stats
            
        finally:
            db.close()
