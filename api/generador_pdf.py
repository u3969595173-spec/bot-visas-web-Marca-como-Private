"""
Generador de reportes PDF
Crea PDFs con análisis de visa y recomendaciones
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime

class GeneradorReportesPDF:
    
    @staticmethod
    def generar_reporte_analisis_visa(estudiante: dict, analisis: dict) -> BytesIO:
        """
        Genera un PDF con el análisis de probabilidad de visa
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para el título
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        # Título
        elements.append(Paragraph("📊 ANÁLISIS DE PROBABILIDAD DE VISA", titulo_style))
        elements.append(Spacer(1, 12))
        
        # Información del estudiante
        info_estudiante = [
            ['Nombre:', estudiante.get('nombre', 'N/A')],
            ['Email:', estudiante.get('email', 'N/A')],
            ['Nacionalidad:', estudiante.get('nacionalidad', 'N/A')],
            ['Especialidad:', estudiante.get('especialidad', 'N/A')],
            ['Fecha del Análisis:', datetime.now().strftime('%d/%m/%Y')]
        ]
        
        tabla_info = Table(info_estudiante, colWidths=[2*inch, 4*inch])
        tabla_info.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        elements.append(tabla_info)
        elements.append(Spacer(1, 20))
        
        # Resultado principal
        prob = analisis['probabilidad']
        color_resultado = colors.green if prob >= 80 else colors.orange if prob >= 60 else colors.red
        
        resultado_data = [[f"{prob}%\nProbabilidad de Aprobación"]]
        tabla_resultado = Table(resultado_data, colWidths=[6*inch])
        tabla_resultado.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), color_resultado),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 24),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ]))
        
        elements.append(tabla_resultado)
        elements.append(Spacer(1, 12))
        
        elements.append(Paragraph(
            f"<b>Nivel de Riesgo:</b> {analisis['nivel_riesgo']}",
            styles['Normal']
        ))
        elements.append(Paragraph(analisis['mensaje'], styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Factores evaluados
        elements.append(Paragraph("<b>FACTORES EVALUADOS</b>", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        factores_data = [['Factor', 'Puntos', 'Comentario']]
        for factor in analisis['factores']:
            factores_data.append([
                factor['factor'],
                f"{factor['puntos']}/{factor['max']}",
                factor['comentario']
            ])
        
        tabla_factores = Table(factores_data, colWidths=[1.8*inch, 1*inch, 3.2*inch])
        tabla_factores.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        
        elements.append(tabla_factores)
        elements.append(Spacer(1, 20))
        
        # Recomendaciones
        elements.append(Paragraph("<b>RECOMENDACIONES PERSONALIZADAS</b>", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        for i, rec in enumerate(analisis['recomendaciones'], 1):
            elements.append(Paragraph(f"{i}. {rec}", styles['Normal']))
            elements.append(Spacer(1, 6))
        
        elements.append(Spacer(1, 20))
        
        # Siguiente paso
        siguiente_paso_style = ParagraphStyle(
            'NextStep',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=10,
            leftIndent=20,
            rightIndent=20
        )
        
        elements.append(Paragraph("<b>💡 SIGUIENTE PASO:</b>", styles['Heading3']))
        elements.append(Paragraph(analisis['siguiente_paso'], siguiente_paso_style))
        
        # Footer
        elements.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(
            "© 2024 Fortunario Cash - Agencia Educativa España<br/>www.fortunariocash.com",
            footer_style
        ))
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_reporte_completo_estudiante(estudiante: dict) -> BytesIO:
        """
        Genera un PDF con toda la información del estudiante
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        styles = getSampleStyleSheet()
        
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#667eea'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        elements.append(Paragraph("📋 REPORTE COMPLETO DEL ESTUDIANTE", titulo_style))
        elements.append(Spacer(1, 20))
        
        # Datos personales
        elements.append(Paragraph("<b>DATOS PERSONALES</b>", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        datos_personales = [
            ['Nombre Completo:', estudiante.get('nombre', 'N/A')],
            ['Email:', estudiante.get('email', 'N/A')],
            ['Teléfono:', estudiante.get('telefono', 'N/A')],
            ['Pasaporte:', estudiante.get('pasaporte', 'N/A')],
            ['Edad:', str(estudiante.get('edad', 'N/A'))],
            ['Nacionalidad:', estudiante.get('nacionalidad', 'N/A')],
            ['Ciudad de Origen:', estudiante.get('ciudad_origen', 'N/A')]
        ]
        
        tabla_datos = Table(datos_personales, colWidths=[2.5*inch, 3.5*inch])
        tabla_datos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        elements.append(tabla_datos)
        elements.append(Spacer(1, 20))
        
        # Información académica
        elements.append(Paragraph("<b>INFORMACIÓN ACADÉMICA</b>", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        datos_academicos = [
            ['Especialidad:', estudiante.get('especialidad', 'N/A')],
            ['Nivel de Español:', estudiante.get('nivel_espanol', 'N/A')],
            ['Tipo de Visa:', estudiante.get('tipo_visa', 'N/A')]
        ]
        
        tabla_academicos = Table(datos_academicos, colWidths=[2.5*inch, 3.5*inch])
        tabla_academicos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        elements.append(tabla_academicos)
        elements.append(Spacer(1, 20))
        
        # Estado de la solicitud
        elements.append(Paragraph("<b>ESTADO DE LA SOLICITUD</b>", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        estado = estudiante.get('estado', 'pendiente').upper()
        color_estado = colors.green if estado == 'APROBADO' else colors.orange if estado == 'PENDIENTE' else colors.red
        
        estado_data = [[f"Estado: {estado}"]]
        tabla_estado = Table(estado_data, colWidths=[6*inch])
        tabla_estado.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), color_estado),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        elements.append(tabla_estado)
        
        if estudiante.get('notas'):
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(f"<b>Notas:</b> {estudiante['notas']}", styles['Normal']))
        
        # Footer
        elements.append(Spacer(1, 40))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(
            f"Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}<br/>"
            "© 2024 Fortunario Cash - Agencia Educativa España",
            footer_style
        ))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
