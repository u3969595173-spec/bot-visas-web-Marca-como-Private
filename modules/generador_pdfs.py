"""
Generador de PDFs Personalizados Profesionales
Genera documentos PDF completos con logo, timeline, info detallada
"""

from datetime import datetime, timedelta
from typing import Dict
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
import io


class GeneradorPDFs:
    """Genera PDFs personalizados profesionales"""
    
    @staticmethod
    def generar_paquete_completo(estudiante_id: int, incluir_logo: bool = True) -> bytes:
        """
        Genera PDF completo con toda la información del estudiante
        
        Args:
            estudiante_id: ID del estudiante
            incluir_logo: Si incluir logo de la agencia
            
        Returns:
            Bytes del PDF generado
        """
        from modules.estudiantes import GestorEstudiantes
        from modules.cursos import GestorCursos
        from modules.fondos import GestorFondos
        from modules.panel_revision_admin import PanelRevisionAdmin
        
        # Obtener información completa
        info = PanelRevisionAdmin._obtener_info_completa_estudiante(estudiante_id)
        estudiante = info['datos_personales']
        
        # Crear PDF en memoria
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        # Estilos
        styles = getSampleStyleSheet()
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        subtitulo_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3498DB'),
            spaceAfter=12
        )
        
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        
        # Contenido del PDF
        elementos = []
        
        # PORTADA
        elementos.append(Spacer(1, 1*inch))
        elementos.append(Paragraph("🎓 PLAN DE ESTUDIOS EN ESPAÑA", titulo_style))
        elementos.append(Spacer(1, 0.3*inch))
        elementos.append(Paragraph(f"<b>{estudiante['nombre_completo']}</b>", subtitulo_style))
        elementos.append(Paragraph(f"Pasaporte: {estudiante['numero_pasaporte']}", normal_style))
        elementos.append(Paragraph(f"Generado: {datetime.now().strftime('%d de %B de %Y')}", normal_style))
        elementos.append(Spacer(1, 0.5*inch))
        elementos.append(Paragraph("Agencia Educativa Internacional", normal_style))
        elementos.append(PageBreak())
        
        # INFORMACIÓN PERSONAL
        elementos.append(Paragraph("📋 INFORMACIÓN PERSONAL", subtitulo_style))
        elementos.append(Spacer(1, 0.2*inch))
        
        datos_personales = [
            ['Nombre completo:', estudiante['nombre_completo']],
            ['Edad:', str(estudiante['edad'])],
            ['Nacionalidad:', estudiante['nacionalidad']],
            ['Ciudad de origen:', estudiante['ciudad_origen']],
            ['Carrera actual:', estudiante['carrera_actual']],
            ['Nivel de español:', estudiante['nivel_espanol']],
            ['Especialidad de interés:', estudiante['especialidad_interes']],
            ['Email:', estudiante['email']],
            ['Teléfono:', estudiante['telefono']]
        ]
        
        tabla_personal = Table(datos_personales, colWidths=[2*inch, 4*inch])
        tabla_personal.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        elementos.append(tabla_personal)
        elementos.append(Spacer(1, 0.5*inch))
        
        # CURSO SELECCIONADO
        if info['cursos_sugeridos']:
            elementos.append(Paragraph("🎓 CURSO SELECCIONADO", subtitulo_style))
            elementos.append(Spacer(1, 0.2*inch))
            
            curso = info['cursos_sugeridos'][0]
            
            datos_curso = [
                ['Nombre del curso:', curso['nombre']],
                ['Escuela:', curso['escuela']],
                ['Ciudad:', curso['ciudad']],
                ['Duración:', f"{curso['duracion_meses']} meses"],
                ['Precio:', f"{curso['precio']:,.2f}€"],
                ['Nivel idioma requerido:', curso['nivel_idioma_requerido']],
                ['Fecha de inicio:', curso['fecha_inicio'].strftime('%d/%m/%Y') if curso['fecha_inicio'] else 'Por confirmar'],
                ['Enlace inscripción:', curso['enlace_inscripcion']]
            ]
            
            tabla_curso = Table(datos_curso, colWidths=[2*inch, 4*inch])
            tabla_curso.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            
            elementos.append(tabla_curso)
            elementos.append(Spacer(1, 0.5*inch))
        
        # SITUACIÓN ECONÓMICA
        elementos.append(Paragraph("💰 SITUACIÓN ECONÓMICA", subtitulo_style))
        elementos.append(Spacer(1, 0.2*inch))
        
        fondos = info['verificacion_fondos']
        
        estado_fondos = "✅ SUFICIENTE" if fondos['fondos_suficientes'] else "⚠️ INSUFICIENTE"
        color_fondo = colors.HexColor('#27AE60') if fondos['fondos_suficientes'] else colors.HexColor('#E74C3C')
        
        datos_fondos = [
            ['Fondos disponibles:', f"{fondos['fondos_disponibles']:,.2f}€"],
            ['Fondos requeridos:', f"{fondos['fondos_minimos_requeridos']:,.2f}€"],
            ['Cobertura:', f"{fondos['porcentaje_cobertura']:.1f}%"],
            ['Estado:', estado_fondos]
        ]
        
        tabla_fondos = Table(datos_fondos, colWidths=[2*inch, 4*inch])
        tabla_fondos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('BACKGROUND', (1, -1), (1, -1), color_fondo),
            ('TEXTCOLOR', (1, -1), (1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, -1), (1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        elementos.append(tabla_fondos)
        elementos.append(PageBreak())
        
        # DOCUMENTOS NECESARIOS
        elementos.append(Paragraph("📄 CHECKLIST DE DOCUMENTOS", subtitulo_style))
        elementos.append(Spacer(1, 0.2*inch))
        
        checklist = info['checklist_documentos']
        
        elementos.append(Paragraph(f"<b>Progreso: {checklist['porcentaje_completado']:.0f}%</b>", normal_style))
        elementos.append(Spacer(1, 0.2*inch))
        
        # Documentos obligatorios
        elementos.append(Paragraph("<b>Documentos Obligatorios:</b>", normal_style))
        elementos.append(Spacer(1, 0.1*inch))
        
        docs_data = [['Estado', 'Documento', 'Categoría']]
        
        for doc in checklist['obligatorios']:
            estado = '✅' if doc['completado'] else '⏳'
            docs_data.append([estado, doc['nombre'], doc['categoria']])
        
        tabla_docs = Table(docs_data, colWidths=[0.5*inch, 3*inch, 2*inch])
        tabla_docs.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')])
        ]))
        
        elementos.append(tabla_docs)
        elementos.append(Spacer(1, 0.5*inch))
        
        # TIMELINE VISUAL
        elementos.append(Paragraph("📅 CRONOGRAMA ESTIMADO", subtitulo_style))
        elementos.append(Spacer(1, 0.2*inch))
        
        hoy = datetime.now()
        timeline_data = [
            ['Fase', 'Actividad', 'Plazo estimado'],
            ['1', 'Completar documentos', f'{hoy.strftime("%d/%m/%Y")} - {(hoy + timedelta(days=14)).strftime("%d/%m/%Y")}'],
            ['2', 'Inscripción en curso', f'{(hoy + timedelta(days=15)).strftime("%d/%m/%Y")} - {(hoy + timedelta(days=30)).strftime("%d/%m/%Y")}'],
            ['3', 'Solicitud de visa', f'{(hoy + timedelta(days=31)).strftime("%d/%m/%Y")} - {(hoy + timedelta(days=45)).strftime("%d/%m/%Y")}'],
            ['4', 'Entrevista consular', f'{(hoy + timedelta(days=46)).strftime("%d/%m/%Y")} - {(hoy + timedelta(days=60)).strftime("%d/%m/%Y")}'],
            ['5', 'Aprobación visa', f'{(hoy + timedelta(days=61)).strftime("%d/%m/%Y")} - {(hoy + timedelta(days=75)).strftime("%d/%m/%Y")}'],
            ['6', 'Viaje a España', f'{(hoy + timedelta(days=76)).strftime("%d/%m/%Y")}']
        ]
        
        tabla_timeline = Table(timeline_data, colWidths=[0.5*inch, 2.5*inch, 3*inch])
        tabla_timeline.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9B59B6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4ECF7')])
        ]))
        
        elementos.append(tabla_timeline)
        elementos.append(Spacer(1, 0.5*inch))
        
        # CONTACTO
        elementos.append(Paragraph("📞 INFORMACIÓN DE CONTACTO", subtitulo_style))
        elementos.append(Spacer(1, 0.2*inch))
        elementos.append(Paragraph("<b>Agencia Educativa Internacional</b>", normal_style))
        elementos.append(Paragraph("Email: info@agenciaeducativa.com", normal_style))
        elementos.append(Paragraph("WhatsApp: +34 600 123 456", normal_style))
        elementos.append(Paragraph("Telegram: @AgenciaEducativaBot", normal_style))
        elementos.append(Spacer(1, 0.2*inch))
        elementos.append(Paragraph("Estamos aquí para ayudarte en cada paso del proceso.", normal_style))
        
        # Construir PDF
        doc.build(elementos)
        
        # Obtener bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    @staticmethod
    def guardar_pdf(pdf_bytes: bytes, nombre_archivo: str):
        """
        Guarda PDF en disco
        
        Args:
            pdf_bytes: Bytes del PDF
            nombre_archivo: Nombre del archivo (sin extensión)
        """
        with open(f"{nombre_archivo}.pdf", 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF guardado: {nombre_archivo}.pdf")
