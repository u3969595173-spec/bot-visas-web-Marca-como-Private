"""
Comparador de Cursos Lado a Lado
Herramienta para comparar múltiples cursos visualmente
"""

from typing import List, Dict
from modules.cursos import Curso, GestorCursos
from database.models import get_db


class ComparadorCursos:
    """Compara múltiples cursos lado a lado"""
    
    @staticmethod
    def comparar_cursos(curso_ids: List[int]) -> Dict:
        """
        Compara 2 o más cursos mostrando sus diferencias
        
        Args:
            curso_ids: Lista de IDs de cursos a comparar (max 4)
            
        Returns:
            Diccionario con comparación estructurada
        """
        if len(curso_ids) < 2:
            raise ValueError("Se necesitan al menos 2 cursos para comparar")
        
        if len(curso_ids) > 4:
            raise ValueError("Máximo 4 cursos para comparar")
        
        db = get_db()
        
        try:
            cursos = []
            for curso_id in curso_ids:
                curso = db.query(Curso).filter(Curso.id == curso_id).first()
                if curso:
                    cursos.append(curso)
            
            if len(cursos) < 2:
                raise ValueError("No se encontraron suficientes cursos válidos")
            
            # Estructura de comparación
            comparacion = {
                'total_cursos': len(cursos),
                'cursos': [],
                'comparacion_campos': ComparadorCursos._comparar_campos(cursos),
                'recomendacion': ComparadorCursos._generar_recomendacion(cursos)
            }
            
            # Agregar datos de cada curso
            for curso in cursos:
                comparacion['cursos'].append({
                    'id': curso.id,
                    'nombre': curso.nombre,
                    'escuela': curso.escuela,
                    'ciudad': curso.ciudad,
                    'precio': curso.precio,
                    'duracion_meses': curso.duracion_meses,
                    'nivel_idioma_requerido': curso.nivel_idioma_requerido,
                    'fecha_inicio': curso.fecha_inicio.strftime('%d/%m/%Y') if curso.fecha_inicio else 'Por confirmar',
                    'modalidad': curso.modalidad,
                    'especialidad': curso.especialidad,
                    'creditos': curso.creditos,
                    'enlace_inscripcion': curso.enlace_inscripcion
                })
            
            return comparacion
            
        finally:
            db.close()
    
    @staticmethod
    def _comparar_campos(cursos: List[Curso]) -> Dict:
        """Compara campos específicos entre cursos"""
        
        precios = [c.precio for c in cursos if c.precio]
        duraciones = [c.duracion_meses for c in cursos if c.duracion_meses]
        
        comparacion = {
            'precio': {
                'minimo': min(precios) if precios else 0,
                'maximo': max(precios) if precios else 0,
                'promedio': sum(precios) / len(precios) if precios else 0,
                'diferencia': max(precios) - min(precios) if precios else 0,
                'curso_mas_barato': cursos[precios.index(min(precios))].nombre if precios else None,
                'curso_mas_caro': cursos[precios.index(max(precios))].nombre if precios else None
            },
            'duracion': {
                'minima': min(duraciones) if duraciones else 0,
                'maxima': max(duraciones) if duraciones else 0,
                'promedio': sum(duraciones) / len(duraciones) if duraciones else 0,
                'curso_mas_corto': cursos[duraciones.index(min(duraciones))].nombre if duraciones else None,
                'curso_mas_largo': cursos[duraciones.index(max(duraciones))].nombre if duraciones else None
            },
            'ciudades': list(set([c.ciudad for c in cursos if c.ciudad])),
            'modalidades': list(set([c.modalidad for c in cursos if c.modalidad])),
            'niveles_idioma': list(set([c.nivel_idioma_requerido for c in cursos if c.nivel_idioma_requerido]))
        }
        
        return comparacion
    
    @staticmethod
    def _generar_recomendacion(cursos: List[Curso]) -> Dict:
        """Genera recomendación basada en la comparación"""
        
        precios = [(c, c.precio) for c in cursos if c.precio]
        duraciones = [(c, c.duracion_meses) for c in cursos if c.duracion_meses]
        
        recomendacion = {
            'mejor_precio': min(precios, key=lambda x: x[1])[0].nombre if precios else None,
            'mejor_duracion': None,  # Depende si prefiere corto o largo
            'mejor_relacion_calidad_precio': None,
            'notas': []
        }
        
        # Calcular relación calidad-precio (precio por mes)
        if precios and duraciones:
            precio_por_mes = []
            for curso in cursos:
                if curso.precio and curso.duracion_meses:
                    ppm = curso.precio / curso.duracion_meses
                    precio_por_mes.append((curso, ppm))
            
            if precio_por_mes:
                mejor = min(precio_por_mes, key=lambda x: x[1])
                recomendacion['mejor_relacion_calidad_precio'] = {
                    'curso': mejor[0].nombre,
                    'precio_por_mes': f"{mejor[1]:.2f}€"
                }
        
        # Notas adicionales
        if len(set([c.ciudad for c in cursos])) > 1:
            recomendacion['notas'].append("Los cursos están en diferentes ciudades. Considera costo de vida.")
        
        if len(set([c.modalidad for c in cursos])) > 1:
            recomendacion['notas'].append("Hay cursos presenciales y online. Elige según preferencia.")
        
        precios_vals = [p[1] for p in precios]
        if precios_vals and (max(precios_vals) - min(precios_vals)) > 3000:
            recomendacion['notas'].append("Gran diferencia de precio. Verifica qué incluye cada curso.")
        
        return recomendacion
    
    @staticmethod
    def generar_tabla_comparacion(curso_ids: List[int]) -> str:
        """
        Genera una tabla visual de comparación
        
        Args:
            curso_ids: Lista de IDs de cursos
            
        Returns:
            String con tabla formateada
        """
        comparacion = ComparadorCursos.comparar_cursos(curso_ids)
        
        cursos = comparacion['cursos']
        comp = comparacion['comparacion_campos']
        rec = comparacion['recomendacion']
        
        tabla = f"""
╔══════════════════════════════════════════════════════════════╗
║              COMPARADOR DE CURSOS - {len(cursos)} OPCIONES               ║
╚══════════════════════════════════════════════════════════════╝

"""
        
        # Nombres de cursos
        for i, curso in enumerate(cursos, 1):
            tabla += f"CURSO {i}: {curso['nombre']}\n"
        
        tabla += "\n" + "="*60 + "\n\n"
        
        # Tabla comparativa
        tabla += f"{'CAMPO':<25}"
        for i in range(len(cursos)):
            tabla += f"{'CURSO ' + str(i+1):<20}"
        tabla += "\n" + "-"*60 + "\n"
        
        # Escuela
        tabla += f"{'Escuela':<25}"
        for curso in cursos:
            tabla += f"{curso['escuela'][:18]:<20}"
        tabla += "\n"
        
        # Ciudad
        tabla += f"{'Ciudad':<25}"
        for curso in cursos:
            tabla += f"{curso['ciudad']:<20}"
        tabla += "\n"
        
        # Precio
        tabla += f"{'Precio':<25}"
        for curso in cursos:
            precio_str = f"{curso['precio']:,.0f}€" if curso['precio'] else "N/D"
            tabla += f"{precio_str:<20}"
        tabla += "\n"
        
        # Duración
        tabla += f"{'Duración':<25}"
        for curso in cursos:
            dur_str = f"{curso['duracion_meses']} meses" if curso['duracion_meses'] else "N/D"
            tabla += f"{dur_str:<20}"
        tabla += "\n"
        
        # Nivel idioma
        tabla += f"{'Nivel idioma req.':<25}"
        for curso in cursos:
            tabla += f"{curso['nivel_idioma_requerido'] or 'N/D':<20}"
        tabla += "\n"
        
        # Fecha inicio
        tabla += f"{'Fecha inicio':<25}"
        for curso in cursos:
            tabla += f"{curso['fecha_inicio']:<20}"
        tabla += "\n"
        
        # Modalidad
        tabla += f"{'Modalidad':<25}"
        for curso in cursos:
            tabla += f"{curso['modalidad'] or 'N/D':<20}"
        tabla += "\n"
        
        tabla += "\n" + "="*60 + "\n"
        
        # Estadísticas
        tabla += f"""
📊 ESTADÍSTICAS:

💰 PRECIO:
   • Más barato: {comp['precio']['curso_mas_barato']} ({comp['precio']['minimo']:,.0f}€)
   • Más caro: {comp['precio']['curso_mas_caro']} ({comp['precio']['maximo']:,.0f}€)
   • Diferencia: {comp['precio']['diferencia']:,.0f}€

⏱️ DURACIÓN:
   • Más corto: {comp['duracion']['curso_mas_corto']} ({comp['duracion']['minima']} meses)
   • Más largo: {comp['duracion']['curso_mas_largo']} ({comp['duracion']['maxima']} meses)

"""
        
        # Recomendación
        tabla += "💡 RECOMENDACIÓN:\n\n"
        
        if rec['mejor_precio']:
            tabla += f"   • Mejor precio: {rec['mejor_precio']}\n"
        
        if rec['mejor_relacion_calidad_precio']:
            tabla += f"   • Mejor relación calidad-precio: {rec['mejor_relacion_calidad_precio']['curso']}\n"
            tabla += f"     ({rec['mejor_relacion_calidad_precio']['precio_por_mes']}/mes)\n"
        
        if rec['notas']:
            tabla += "\n   📝 Notas:\n"
            for nota in rec['notas']:
                tabla += f"   • {nota}\n"
        
        return tabla
    
    @staticmethod
    def comparar_por_estudiante(
        estudiante_id: int,
        limite: int = 3
    ) -> Dict:
        """
        Encuentra y compara los mejores cursos para un estudiante específico
        
        Args:
            estudiante_id: ID del estudiante
            limite: Número de cursos a comparar
            
        Returns:
            Diccionario con comparación y recomendación personalizada
        """
        from modules.estudiantes import GestorEstudiantes
        
        estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=estudiante_id)
        
        if not estudiante:
            raise ValueError("Estudiante no encontrado")
        
        # Buscar cursos relevantes
        cursos = GestorCursos.filtrar_cursos(
            especialidad=estudiante.especialidad_interes.lower() if estudiante.especialidad_interes else None,
            nivel_idioma=estudiante.nivel_espanol.lower() if estudiante.nivel_espanol else None
        )
        
        if not cursos:
            return {'error': 'No se encontraron cursos relevantes'}
        
        # Tomar los mejores según criterios
        cursos_top = cursos[:limite]
        curso_ids = [c.id for c in cursos_top]
        
        # Comparar
        comparacion = ComparadorCursos.comparar_cursos(curso_ids)
        
        # Agregar información personalizada del estudiante
        comparacion['estudiante'] = {
            'nombre': estudiante.nombre_completo,
            'especialidad': estudiante.especialidad_interes,
            'nivel_espanol': estudiante.nivel_espanol,
            'presupuesto': getattr(estudiante, 'presupuesto_curso', None)
        }
        
        return comparacion
