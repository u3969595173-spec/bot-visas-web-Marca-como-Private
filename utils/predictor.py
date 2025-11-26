from config import COUNTRIES, UNIVERSITY_TYPES, STUDY_TYPES

class SuccessPredictor:
    """Predict visa approval success rate based on multiple factors"""
    
    @staticmethod
    def calculate_score(application_data: dict) -> dict:
        """
        Calculate approval probability based on application data
        
        Args:
            application_data: Dictionary with application information
            
        Returns:
            dict with score, probability, and detailed breakdown
        """
        score = 0
        max_score = 160
        breakdown = []
        
        # 1. Country of Origin (max 20 points)
        country = application_data.get('country_origin', 'otros').lower()
        country_data = COUNTRIES.get(country, COUNTRIES['otros'])
        country_points = country_data['points']
        score += country_points
        breakdown.append({
            'factor': 'País de origen',
            'value': country.title(),
            'points': country_points,
            'max_points': 20,
            'icon': '🌍'
        })
        
        # 2. University Type (max 30 points)
        university_type = application_data.get('university_type', 'privada')
        uni_data = UNIVERSITY_TYPES.get(university_type, UNIVERSITY_TYPES['privada'])
        uni_points = uni_data['points']
        score += uni_points
        breakdown.append({
            'factor': 'Tipo de universidad',
            'value': application_data.get('university', 'Universidad'),
            'points': uni_points,
            'max_points': 30,
            'icon': '🎓'
        })
        
        # 3. Economic Funds (max 25 points)
        funds_evaluation = application_data.get('funds_evaluation', {})
        funds_points = funds_evaluation.get('points', 0)
        score += funds_points
        breakdown.append({
            'factor': 'Fondos económicos',
            'value': funds_evaluation.get('status', 'No evaluado'),
            'points': funds_points,
            'max_points': 25,
            'icon': '💰'
        })
        
        # 4. Clean Background (max 20 points)
        clean_background = application_data.get('clean_background', True)
        background_points = 20 if clean_background else 0
        score += background_points
        breakdown.append({
            'factor': 'Antecedentes penales',
            'value': 'Limpios' if clean_background else 'Con antecedentes',
            'points': background_points,
            'max_points': 20,
            'icon': '📋'
        })
        
        # 5. Medical Insurance (max 10 points)
        has_insurance = application_data.get('has_insurance', False)
        insurance_quality = application_data.get('insurance_quality', 'standard')
        insurance_points = 10 if has_insurance and insurance_quality == 'recognized' else (7 if has_insurance else 0)
        score += insurance_points
        breakdown.append({
            'factor': 'Seguro médico',
            'value': 'Reconocido' if insurance_quality == 'recognized' else ('Sí' if has_insurance else 'No'),
            'points': insurance_points,
            'max_points': 10,
            'icon': '🏥'
        })
        
        # 6. Document Completeness (max 20 points)
        documents_complete = application_data.get('documents_complete_percentage', 0)
        doc_points = int(20 * (documents_complete / 100))
        score += doc_points
        breakdown.append({
            'factor': 'Completitud de documentos',
            'value': f'{documents_complete}%',
            'points': doc_points,
            'max_points': 20,
            'icon': '📄'
        })
        
        # 7. Recommendation Letters (max 15 points)
        has_recommendations = application_data.get('has_recommendations', False)
        num_recommendations = application_data.get('num_recommendations', 0)
        rec_points = min(num_recommendations * 7.5, 15) if has_recommendations else 0
        score += rec_points
        breakdown.append({
            'factor': 'Cartas de recomendación',
            'value': f'{num_recommendations} cartas' if has_recommendations else 'Ninguna',
            'points': rec_points,
            'max_points': 15,
            'icon': '✉️'
        })
        
        # 8. Spanish Language Level (max 10 points)
        spanish_level = application_data.get('spanish_level', 'none')
        spanish_points = {
            'c2': 10,
            'c1': 10,
            'b2': 10,
            'b1': 7,
            'a2': 4,
            'a1': 2,
            'none': 0
        }.get(spanish_level.lower(), 0)
        score += spanish_points
        breakdown.append({
            'factor': 'Nivel de español',
            'value': spanish_level.upper() if spanish_level != 'none' else 'Sin certificado',
            'points': spanish_points,
            'max_points': 10,
            'icon': '🗣️'
        })
        
        # 9. Study Type (max 10 points)
        study_type = application_data.get('study_type', 'curso_idiomas')
        study_data = STUDY_TYPES.get(study_type, STUDY_TYPES['curso_idiomas'])
        study_points = min(study_data['points'] / 3.5, 10)
        score += study_points
        breakdown.append({
            'factor': 'Tipo de estudio',
            'value': study_type.replace('_', ' ').title(),
            'points': study_points,
            'max_points': 10,
            'icon': '📚'
        })
        
        # Calculate probability
        percentage = (score / max_score) * 100
        probability = min(percentage * 0.95, 98)  # Cap at 98%
        
        # Determine status
        if probability >= 90:
            status = '🟢 EXCELENTE'
            recommendation = 'Proceder con solicitud inmediatamente'
        elif probability >= 75:
            status = '🟡 BUENO'
            recommendation = 'Mejorar algunos aspectos antes de solicitar'
        elif probability >= 60:
            status = '🟠 MODERADO'
            recommendation = 'Reforzar documentación y fondos'
        else:
            status = '🔴 BAJO'
            recommendation = 'Mejorar significativamente antes de solicitar'
        
        # Risk factors
        risk_factors = []
        if funds_evaluation.get('percentage', 100) < 110:
            risk_factors.append('Fondos justos - agregar más si es posible')
        if not has_recommendations:
            risk_factors.append('Sin cartas de recomendación')
        if spanish_level in ['none', 'a1', 'a2'] and study_type != 'curso_idiomas':
            risk_factors.append('Nivel de español bajo para el tipo de estudio')
        if documents_complete < 100:
            risk_factors.append('Documentación incompleta')
        
        # Improvement suggestions
        improvements = []
        if funds_evaluation.get('percentage', 100) < 120:
            improvements.append(f"💡 Agregar +{2000}€ adicionales (+2% probabilidad)")
        if num_recommendations < 2:
            improvements.append("💡 Incluir 2da carta de recomendación (+2% probabilidad)")
        if spanish_level in ['none', 'a1', 'a2']:
            improvements.append("💡 Obtener certificado DELE B1+ (+3% probabilidad)")
        if documents_complete < 100:
            improvements.append("💡 Completar documentación faltante (+5% probabilidad)")
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': percentage,
            'probability': probability,
            'status': status,
            'recommendation': recommendation,
            'breakdown': breakdown,
            'risk_factors': risk_factors if risk_factors else ['NINGUNO'],
            'improvements': improvements,
            'formatted_report': SuccessPredictor._format_report(
                score, max_score, probability, status, breakdown, risk_factors, improvements
            )
        }
    
    @staticmethod
    def _format_report(score, max_score, probability, status, breakdown, risk_factors, improvements):
        """Format the prediction report for display"""
        report = f"""
📊 **ANÁLISIS COMPLETO DE PROBABILIDAD**

"""
        for item in breakdown:
            report += f"{item['icon']} **{item['factor']}:** {item['value']}\n"
            report += f"   +{item['points']} puntos (máx: {item['max_points']})\n\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━
**PUNTUACIÓN TOTAL: {score}/{max_score}**

🎯 **PROBABILIDAD DE APROBACIÓN: {probability:.0f}%**

**Estado:** {status}

⚠️ **Riesgos detectados:**
"""
        for risk in risk_factors:
            report += f"• {risk}\n"
        
        if improvements:
            report += f"""
📈 **Cómo mejorar tu probabilidad:**
"""
            for improvement in improvements:
                report += f"{improvement}\n"
        
        return report
