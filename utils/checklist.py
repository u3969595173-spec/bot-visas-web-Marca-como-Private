from config import MANDATORY_DOCUMENTS, RECOMMENDED_DOCUMENTS, STUDY_TYPES

class ChecklistGenerator:
    """Generate personalized document checklist based on user's situation"""
    
    @staticmethod
    def generate_checklist(application_data: dict) -> dict:
        """
        Generate personalized checklist based on application data
        
        Args:
            application_data: Dictionary with user's application information
            
        Returns:
            dict with mandatory, recommended, and not needed documents
        """
        country = application_data.get('country_origin', '').lower()
        study_type = application_data.get('study_type', 'master')
        duration_months = application_data.get('duration_months', 12)
        university_type = application_data.get('university_type', 'publica')
        
        # Base mandatory documents
        mandatory = [
            {
                'id': 'pasaporte',
                'name': 'Pasaporte vigente',
                'description': 'Vigente mínimo 6 meses después de fecha prevista regreso',
                'requirements': ['Original', 'Al menos 2 páginas en blanco', 'Foto legible'],
                'icon': '🛂'
            },
            {
                'id': 'carta_aceptacion',
                'name': 'Carta de aceptación universidad',
                'description': 'Original emitida por la universidad',
                'requirements': ['Original firmada y sellada', 'Debe incluir: nombre curso, duración, matrícula'],
                'icon': '🎓'
            },
            {
                'id': 'seguro_medico',
                'name': 'Seguro médico',
                'description': f'Cobertura mínima 30,000€ durante toda la estancia',
                'requirements': ['Cobertura: 30,000€', 'Incluir repatriación', 'Vigente todo el periodo'],
                'icon': '🏥'
            },
            {
                'id': 'antecedentes',
                'name': 'Certificado antecedentes penales',
                'description': f'Emitido por autoridades de {country.title()}',
                'requirements': ['Apostillado', 'Máximo 3 meses antigüedad', 'Traducido al español'],
                'icon': '📋'
            },
            {
                'id': 'certificado_medico',
                'name': 'Certificado médico',
                'description': 'Certifica que no padeces enfermedades cuarentenables',
                'requirements': ['Máximo 3 meses antigüedad', 'Firmado por médico colegiado'],
                'icon': '⚕️'
            },
            {
                'id': 'prueba_fondos',
                'name': 'Prueba de fondos económicos',
                'description': 'Demostrar capacidad económica para mantenerse',
                'requirements': [
                    f'Mínimo: 600€/mes × {duration_months} meses',
                    'Extractos bancarios últimos 6 meses',
                    'Carta aval padres si aplica'
                ],
                'icon': '💰'
            },
            {
                'id': 'formulario_ex00',
                'name': 'Formulario EX-00',
                'description': 'Solicitud de visado nacional',
                'requirements': ['Cumplimentado completamente', 'Firmado', '2 copias'],
                'icon': '📝'
            },
            {
                'id': 'fotos',
                'name': 'Fotografías tamaño carnet',
                'description': 'Fotos recientes fondo blanco',
                'requirements': ['2 fotos', 'Tamaño: 35×45 mm', 'Fondo blanco', 'Máximo 6 meses antigüedad'],
                'icon': '📸'
            }
        ]
        
        # Recommended documents (increase approval chances)
        recommended = [
            {
                'id': 'carta_recomendacion',
                'name': 'Cartas de recomendación',
                'description': 'De profesores o empleadores',
                'benefit': '+15% probabilidad de aprobación',
                'requirements': ['1-2 cartas', 'Profesores o empleadores', 'En español o inglés'],
                'icon': '✉️'
            },
            {
                'id': 'certificado_espanol',
                'name': 'Certificado nivel español',
                'description': 'DELE B2 o superior',
                'benefit': '+10% probabilidad',
                'requirements': ['DELE, SIELE o similar', 'Nivel B1 mínimo, B2+ recomendado'],
                'icon': '🗣️'
            },
            {
                'id': 'extractos_bancarios',
                'name': 'Extractos bancarios detallados',
                'description': 'Últimos 6 meses completos',
                'benefit': '+8% probabilidad',
                'requirements': ['6 meses', 'Mostrar movimientos regulares', 'Saldo estable'],
                'icon': '🏦'
            }
        ]
        
        # Add conditional recommended documents
        if duration_months >= 12:
            recommended.append({
                'id': 'certificado_alojamiento',
                'name': 'Certificado de alojamiento',
                'description': 'Carta de reserva o pre-contrato',
                'benefit': '+5% probabilidad',
                'requirements': ['No necesario comprar antes', 'Reserva o carta universidad'],
                'icon': '🏠'
            })
        
        if study_type in ['master', 'doctorado']:
            recommended.append({
                'id': 'titulos_previos',
                'name': 'Títulos académicos previos',
                'description': 'Grado, licenciatura o equivalente',
                'benefit': '+5% probabilidad',
                'requirements': ['Apostillados', 'Traducidos al español'],
                'icon': '🎓'
            })
        
        # Documents NOT needed (save time)
        not_needed = [
            {
                'id': 'carta_invitacion',
                'name': 'Carta de invitación',
                'reason': 'No aplica para visas de estudiante',
                'icon': '❌'
            },
            {
                'id': 'contrato_alquiler',
                'name': 'Contrato de alquiler firmado',
                'reason': 'No necesario antes de llegar',
                'icon': '❌'
            },
            {
                'id': 'billete_avion',
                'name': 'Billete de avión comprado',
                'reason': 'No comprar hasta tener visa aprobada',
                'icon': '❌'
            }
        ]
        
        return {
            'mandatory': mandatory,
            'recommended': recommended,
            'not_needed': not_needed,
            'total_mandatory': len(mandatory),
            'total_recommended': len(recommended),
            'formatted_checklist': ChecklistGenerator._format_checklist(
                mandatory, recommended, not_needed, application_data
            )
        }
    
    @staticmethod
    def _format_checklist(mandatory, recommended, not_needed, application_data):
        """Format checklist for display"""
        country = application_data.get('country_origin', 'tu país').title()
        study_type = application_data.get('study_type', 'Máster').replace('_', ' ').title()
        university = application_data.get('university', 'Universidad')
        duration_months = application_data.get('duration_months', 12)
        
        checklist = f"""
📋 **CHECKLIST PERSONALIZADO DE DOCUMENTOS**

**Tu perfil:**
🌍 País: {country}
🎓 Estudio: {study_type}
🏛️ Universidad: {university}
⏱️ Duración: {duration_months} meses

━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ **DOCUMENTOS OBLIGATORIOS** ({len(mandatory)}):

"""
        for i, doc in enumerate(mandatory, 1):
            checklist += f"{i}. {doc['icon']} **{doc['name']}**\n"
            checklist += f"   {doc['description']}\n"
            checklist += f"   Requisitos:\n"
            for req in doc['requirements']:
                checklist += f"   • {req}\n"
            checklist += "\n"
        
        checklist += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ **DOCUMENTOS RECOMENDADOS** ({len(recommended)}):
_(Aumentan significativamente tus posibilidades)_

"""
        for i, doc in enumerate(recommended, 1):
            checklist += f"{i}. {doc['icon']} **{doc['name']}** - {doc['benefit']}\n"
            checklist += f"   {doc['description']}\n"
            checklist += f"   Requisitos:\n"
            for req in doc['requirements']:
                checklist += f"   • {req}\n"
            checklist += "\n"
        
        checklist += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ **NO NECESITAS** (ahorra tiempo y dinero):

"""
        for doc in not_needed:
            checklist += f"{doc['icon']} **{doc['name']}**\n"
            checklist += f"   Razón: {doc['reason']}\n\n"
        
        return checklist
