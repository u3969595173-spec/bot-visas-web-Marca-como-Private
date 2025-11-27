"""
Calculadora de probabilidad de visa
Analiza el perfil del estudiante y calcula probabilidad de aprobación
"""
from typing import Dict, Any

class CalculadoraProbabilidadVisa:
    
    @staticmethod
    def calcular_probabilidad(estudiante_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula la probabilidad de aprobación de visa basado en múltiples factores
        
        Factores evaluados:
        - Edad (18-35 años = mejor)
        - Nivel de español (mayor nivel = más puntos)
        - Tipo de visa (estudiante > idiomas > doctorado)
        - Completitud del perfil
        - Nacionalidad (factor de riesgo migratorio)
        """
        
        puntos_total = 0
        max_puntos = 100
        factores_detalle = []
        
        # Factor 1: Edad (20 puntos)
        edad = estudiante_data.get('edad') or 0
        if 18 <= edad <= 25:
            puntos_edad = 20
            factores_detalle.append({
                'factor': 'Edad',
                'puntos': 20,
                'max': 20,
                'comentario': 'Edad ideal para estudios (18-25 años)'
            })
        elif 26 <= edad <= 30:
            puntos_edad = 15
            factores_detalle.append({
                'factor': 'Edad',
                'puntos': 15,
                'max': 20,
                'comentario': 'Edad adecuada para estudios (26-30 años)'
            })
        elif 31 <= edad <= 35:
            puntos_edad = 10
            factores_detalle.append({
                'factor': 'Edad',
                'puntos': 10,
                'max': 20,
                'comentario': 'Edad aceptable (31-35 años)'
            })
        else:
            puntos_edad = 5
            factores_detalle.append({
                'factor': 'Edad',
                'puntos': 5,
                'max': 20,
                'comentario': 'Edad fuera del rango ideal'
            })
        puntos_total += puntos_edad
        
        # Factor 2: Nivel de español (25 puntos)
        nivel_espanol = (estudiante_data.get('nivel_espanol') or '').lower()
        if nivel_espanol == 'nativo':
            puntos_espanol = 25
            comentario_espanol = 'Nivel nativo - excelente'
        elif nivel_espanol == 'avanzado':
            puntos_espanol = 20
            comentario_espanol = 'Nivel avanzado (C1-C2) - muy bueno'
        elif nivel_espanol == 'intermedio':
            puntos_espanol = 15
            comentario_espanol = 'Nivel intermedio (B1-B2) - adecuado'
        else:
            puntos_espanol = 8
            comentario_espanol = 'Nivel básico - se recomienda mejorarlo'
        
        factores_detalle.append({
            'factor': 'Nivel de Español',
            'puntos': puntos_espanol,
            'max': 25,
            'comentario': comentario_espanol
        })
        puntos_total += puntos_espanol
        
        # Factor 3: Tipo de visa (15 puntos)
        tipo_visa = (estudiante_data.get('tipo_visa') or '').lower()
        if tipo_visa == 'estudiante':
            puntos_visa = 15
            comentario_visa = 'Visa de estudiante - alta probabilidad'
        elif tipo_visa == 'idiomas':
            puntos_visa = 12
            comentario_visa = 'Curso de idiomas - buena opción'
        elif tipo_visa == 'doctorado':
            puntos_visa = 10
            comentario_visa = 'Doctorado - requiere más documentación'
        else:
            puntos_visa = 10
            comentario_visa = 'Tipo de visa estándar'
        
        factores_detalle.append({
            'factor': 'Tipo de Visa',
            'puntos': puntos_visa,
            'max': 15,
            'comentario': comentario_visa
        })
        puntos_total += puntos_visa
        
        # Factor 4: Completitud del perfil (20 puntos)
        campos_requeridos = ['nombre', 'email', 'telefono', 'pasaporte', 'nacionalidad', 
                            'ciudad_origen', 'especialidad']
        campos_completos = sum(1 for campo in campos_requeridos 
                              if estudiante_data.get(campo))
        puntos_completitud = int((campos_completos / len(campos_requeridos)) * 20)
        
        factores_detalle.append({
            'factor': 'Completitud del Perfil',
            'puntos': puntos_completitud,
            'max': 20,
            'comentario': f'{campos_completos}/{len(campos_requeridos)} campos completos'
        })
        puntos_total += puntos_completitud
        
        # Factor 5: Nacionalidad (20 puntos)
        # Países con bajo riesgo migratorio reciben más puntos
        nacionalidad = (estudiante_data.get('nacionalidad') or '').lower()
        paises_alto_riesgo = ['venezuela', 'colombia', 'ecuador', 'perú', 'bolivia']
        paises_medio_riesgo = ['méxico', 'argentina', 'chile', 'brasil']
        
        if any(pais in nacionalidad for pais in paises_alto_riesgo):
            puntos_nacionalidad = 10
            comentario_nacionalidad = 'Nacionalidad con mayor control migratorio'
        elif any(pais in nacionalidad for pais in paises_medio_riesgo):
            puntos_nacionalidad = 15
            comentario_nacionalidad = 'Nacionalidad con control migratorio estándar'
        else:
            puntos_nacionalidad = 20
            comentario_nacionalidad = 'Nacionalidad con facilidades migratorias'
        
        factores_detalle.append({
            'factor': 'Nacionalidad',
            'puntos': puntos_nacionalidad,
            'max': 20,
            'comentario': comentario_nacionalidad
        })
        puntos_total += puntos_nacionalidad
        
        # Calcular porcentaje
        probabilidad = int((puntos_total / max_puntos) * 100)
        
        # Determinar nivel de riesgo y recomendaciones
        if probabilidad >= 80:
            nivel_riesgo = 'BAJO'
            color = '#10b981'  # Verde
            mensaje = '¡Excelente perfil! Alta probabilidad de aprobación.'
            recomendaciones = [
                'Mantén toda tu documentación actualizada',
                'Prepara carta de motivación sólida',
                'Ten listo comprobante de fondos económicos'
            ]
        elif probabilidad >= 60:
            nivel_riesgo = 'MEDIO'
            color = '#f59e0b'  # Amarillo
            mensaje = 'Buen perfil, pero hay áreas de mejora.'
            recomendaciones = [
                'Mejora tu nivel de español si es posible',
                'Asegura tener documentación completa',
                'Considera carta de recomendación académica',
                'Prepara justificación de vínculos con país de origen'
            ]
        else:
            nivel_riesgo = 'ALTO'
            color = '#ef4444'  # Rojo
            mensaje = 'Se requieren mejoras significativas en tu perfil.'
            recomendaciones = [
                'URGENTE: Mejorar nivel de español',
                'Completar todos los campos del perfil',
                'Obtener carta de aceptación de universidad reconocida',
                'Preparar sólida justificación económica',
                'Considerar asesoría especializada'
            ]
        
        return {
            'probabilidad': probabilidad,
            'puntos_total': puntos_total,
            'puntos_maximos': max_puntos,
            'nivel_riesgo': nivel_riesgo,
            'color': color,
            'mensaje': mensaje,
            'factores': factores_detalle,
            'recomendaciones': recomendaciones,
            'siguiente_paso': 'Agendar consulta con asesor para revisar documentación'
        }
    
    @staticmethod
    def generar_informe_html(analisis: Dict[str, Any], estudiante_nombre: str) -> str:
        """Genera HTML del informe de probabilidad"""
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
            <h2 style="color: #333;">Análisis de Probabilidad de Visa</h2>
            <p><strong>Estudiante:</strong> {estudiante_nombre}</p>
            
            <div style="background: {analisis['color']}; color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                <h1 style="margin: 0; font-size: 48px;">{analisis['probabilidad']}%</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px;">{analisis['mensaje']}</p>
                <p style="margin: 5px 0 0 0;"><strong>Riesgo: {analisis['nivel_riesgo']}</strong></p>
            </div>
            
            <h3>Factores Evaluados:</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #f3f4f6;">
                    <th style="padding: 10px; text-align: left;">Factor</th>
                    <th style="padding: 10px; text-align: center;">Puntos</th>
                    <th style="padding: 10px; text-align: left;">Comentario</th>
                </tr>
        """
        
        for factor in analisis['factores']:
            html += f"""
                <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 10px;"><strong>{factor['factor']}</strong></td>
                    <td style="padding: 10px; text-align: center;">{factor['puntos']}/{factor['max']}</td>
                    <td style="padding: 10px;">{factor['comentario']}</td>
                </tr>
            """
        
        html += f"""
            </table>
            
            <h3 style="margin-top: 30px;">Recomendaciones:</h3>
            <ul>
        """
        
        for rec in analisis['recomendaciones']:
            html += f"<li style='margin: 10px 0;'>{rec}</li>"
        
        html += f"""
            </ul>
            
            <div style="background: #eff6ff; padding: 15px; border-left: 4px solid #3b82f6; margin-top: 30px;">
                <strong>Siguiente Paso:</strong> {analisis['siguiente_paso']}
            </div>
        </div>
        """
        
        return html
