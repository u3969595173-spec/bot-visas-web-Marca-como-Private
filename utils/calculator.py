from config import MONTHLY_MAINTENANCE, INSURANCE_COST, ACCOMMODATION_ESTIMATE

class FundsCalculator:
    """Calculate minimum funds required for visa application"""
    
    @staticmethod
    def calculate_minimum_funds(course_cost: float, duration_months: int) -> dict:
        """
        Calculate minimum funds required based on course cost and duration
        
        Args:
            course_cost: Total cost of the course in euros
            duration_months: Duration of the course in months
            
        Returns:
            dict with breakdown of costs
        """
        maintenance = MONTHLY_MAINTENANCE * duration_months
        accommodation = ACCOMMODATION_ESTIMATE * duration_months
        insurance = INSURANCE_COST
        
        total = course_cost + maintenance + accommodation + insurance
        
        return {
            'course_cost': course_cost,
            'maintenance': maintenance,
            'accommodation': accommodation,
            'insurance': insurance,
            'total_minimum': total,
            'recommended': total * 1.1,  # 10% extra recommended
            'breakdown': f"""
💰 **CÁLCULO DE FONDOS ECONÓMICOS**

📚 Matrícula curso: {course_cost:,.2f}€
🍽️ Manutención mínima: {MONTHLY_MAINTENANCE}€/mes × {duration_months} = {maintenance:,.2f}€
🏠 Alojamiento estimado: {ACCOMMODATION_ESTIMATE}€/mes × {duration_months} = {accommodation:,.2f}€
🏥 Seguro médico: {insurance:,.2f}€

**TOTAL MÍNIMO: {total:,.2f}€**
**RECOMENDADO (+10%): {total * 1.1:,.2f}€**

📊 **Formas de demostrar fondos:**
1. Cuenta bancaria propia (extracto 6 meses)
2. Cuenta bancaria padres + carta aval
3. Beca universidad/gobierno (certificado)
4. Préstamo estudiantil (contrato aprobado)
5. Combinación de las anteriores
"""
        }
    
    @staticmethod
    def evaluate_funds_sufficiency(required: float, available: float) -> dict:
        """
        Evaluate if available funds are sufficient
        
        Args:
            required: Minimum required funds
            available: Available funds
            
        Returns:
            dict with evaluation result
        """
        percentage = (available / required) * 100
        surplus = available - required
        
        if percentage >= 120:
            status = '✅ EXCELENTE'
            message = f'Tienes {surplus:,.2f}€ extra ({percentage-100:.0f}% más del mínimo)'
            points = 25
        elif percentage >= 110:
            status = '✅ MUY BIEN'
            message = f'Tienes {surplus:,.2f}€ extra ({percentage-100:.0f}% más del mínimo)'
            points = 20
        elif percentage >= 100:
            status = '✅ SUFICIENTE'
            message = 'Cumples el mínimo requerido'
            points = 15
        elif percentage >= 90:
            status = '⚠️ JUSTO'
            message = f'Te faltan {abs(surplus):,.2f}€ para el mínimo'
            points = 5
        else:
            status = '❌ INSUFICIENTE'
            message = f'Te faltan {abs(surplus):,.2f}€ para el mínimo'
            points = 0
        
        return {
            'status': status,
            'message': message,
            'percentage': percentage,
            'surplus': surplus,
            'points': points,
            'sufficient': percentage >= 100
        }
