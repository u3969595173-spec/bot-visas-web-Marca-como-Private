"""
Generador de Documentos Oficiales para Estudiantes
Sistema de generación automática de documentos PDF con plantillas profesionales
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime


class GeneradorDocumentosOficiales:
    
    @staticmethod
    def _get_estilos():
        """Estilos personalizados para los documentos"""
        styles = getSampleStyleSheet()
        
        # Título principal
        styles.add(ParagraphStyle(
            name='TituloDocumento',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1a365d'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        styles.add(ParagraphStyle(
            name='SubtituloDocumento',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2d3748'),
            spaceAfter=15,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal justificado
        styles.add(ParagraphStyle(
            name='TextoJustificado',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16
        ))
        
        # Firma
        styles.add(ParagraphStyle(
            name='Firma',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=6
        ))
        
        return styles
    
    @staticmethod
    def _crear_encabezado(elements, titulo):
        """Encabezado común para todos los documentos"""
        styles = GeneradorDocumentosOficiales._get_estilos()
        
        # Logo/Nombre de la agencia
        elements.append(Paragraph(
            "🎓 AGENCIA EDUCATIVA ESPAÑA",
            ParagraphStyle('LogoStyle', fontSize=16, textColor=colors.HexColor('#667eea'), 
                          alignment=TA_CENTER, fontName='Helvetica-Bold')
        ))
        elements.append(Spacer(1, 0.3*cm))
        
        elements.append(Paragraph(
            "Especialistas en Visas de Estudiante para España",
            ParagraphStyle('SublogoStyle', fontSize=10, textColor=colors.grey, alignment=TA_CENTER)
        ))
        elements.append(Spacer(1, 0.5*cm))
        
        # Línea decorativa
        line_table = Table([['']], colWidths=[18*cm])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#667eea')),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.8*cm))
        
        # Título del documento
        elements.append(Paragraph(titulo, styles['TituloDocumento']))
        elements.append(Spacer(1, 0.5*cm))
    
    @staticmethod
    def _crear_pie_pagina(elements):
        """Pie de página común"""
        elements.append(Spacer(1, 1.5*cm))
        
        # Línea decorativa
        line_table = Table([['']], colWidths=[18*cm])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.grey),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.3*cm))
        
        # Información de contacto
        contacto_style = ParagraphStyle('ContactoStyle', fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
        elements.append(Paragraph(
            "📧 info@agenciaeducativaespana.com | 📞 +34 900 123 456 | 🌐 www.agenciaeducativaespana.com",
            contacto_style
        ))
        elements.append(Paragraph(
            "Madrid, España - Registro Mercantil: B-12345678",
            contacto_style
        ))
    
    @staticmethod
    def generar_carta_aceptacion(datos_estudiante):
        """
        Genera carta de aceptación oficial
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              leftMargin=2*cm, rightMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
        
        elements = []
        styles = GeneradorDocumentosOficiales._get_estilos()
        
        # Encabezado
        GeneradorDocumentosOficiales._crear_encabezado(elements, "CARTA DE ACEPTACIÓN")
        
        # Fecha y referencia
        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        elements.append(Paragraph(
            f"<b>Fecha:</b> {fecha_actual}<br/>"
            f"<b>Referencia:</b> EST-{datos_estudiante.get('id', '000')}-2025<br/>"
            f"<b>A quien corresponda:</b>",
            styles['Normal']
        ))
        elements.append(Spacer(1, 0.8*cm))
        
        # Cuerpo de la carta
        nombre = datos_estudiante.get('nombre', 'ESTUDIANTE')
        nacionalidad = datos_estudiante.get('nacionalidad', 'PAÍS')
        pasaporte = datos_estudiante.get('pasaporte', 'XXXXXXXXX')
        especialidad = datos_estudiante.get('especialidad', 'programa académico')
        
        texto_carta = f"""
        Por medio de la presente, la <b>AGENCIA EDUCATIVA ESPAÑA</b>, con sede en Madrid, España, 
        certifica que el/la señor/a <b>{nombre}</b>, de nacionalidad <b>{nacionalidad}</b>, 
        con pasaporte número <b>{pasaporte}</b>, ha sido <b>ACEPTADO/A</b> para participar en 
        nuestro programa de <b>{especialidad}</b>.
        <br/><br/>
        El período de estudios está programado para iniciar en el año académico 2025-2026, 
        con una duración estimada según el plan de estudios correspondiente. El estudiante 
        recibirá el apoyo necesario en todos los trámites de documentación, visado y 
        asesoramiento durante su estancia en España.
        <br/><br/>
        Este documento es emitido a solicitud del interesado para los fines que estime convenientes, 
        especialmente para su presentación ante las autoridades consulares españolas en el 
        proceso de solicitud de visa de estudiante.
        <br/><br/>
        La presente certificación incluye:
        """
        
        elements.append(Paragraph(texto_carta, styles['TextoJustificado']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Lista de beneficios
        beneficios = [
            ['✓', 'Aceptación oficial en programa educativo'],
            ['✓', 'Soporte en trámites de visa y documentación'],
            ['✓', 'Asesoramiento sobre alojamiento en España'],
            ['✓', 'Orientación académica y cultural'],
            ['✓', 'Asistencia durante toda la estancia'],
        ]
        
        tabla_beneficios = Table(beneficios, colWidths=[1*cm, 16*cm])
        tabla_beneficios.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#48bb78')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(tabla_beneficios)
        elements.append(Spacer(1, 0.8*cm))
        
        # Cierre
        elements.append(Paragraph(
            "Sin otro particular, quedamos a su disposición para cualquier aclaración adicional.",
            styles['TextoJustificado']
        ))
        elements.append(Spacer(1, 1.5*cm))
        
        # Firma
        elements.append(Paragraph("Atentamente,", styles['Firma']))
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("_________________________", styles['Firma']))
        elements.append(Paragraph("<b>Director General</b>", styles['Firma']))
        elements.append(Paragraph("Agencia Educativa España", styles['Firma']))
        
        # Pie de página
        GeneradorDocumentosOficiales._crear_pie_pagina(elements)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_carta_motivacion(datos_estudiante):
        """
        Genera carta de motivación pre-llenada
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                              leftMargin=2*cm, rightMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
        
        elements = []
        styles = GeneradorDocumentosOficiales._get_estilos()
        
        # Encabezado
        GeneradorDocumentosOficiales._crear_encabezado(elements, "CARTA DE MOTIVACIÓN")
        
        # Datos personales
        nombre = datos_estudiante.get('nombre', 'ESTUDIANTE')
        nacionalidad = datos_estudiante.get('nacionalidad', 'PAÍS')
        especialidad = datos_estudiante.get('especialidad', 'programa')
        ciudad_origen = datos_estudiante.get('ciudad_origen', 'ciudad')
        
        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        elements.append(Paragraph(f"{ciudad_origen}, {fecha_actual}", 
                                 ParagraphStyle('FechaStyle', fontSize=10, alignment=TA_RIGHT)))
        elements.append(Spacer(1, 0.8*cm))
        
        # Saludo
        elements.append(Paragraph("Estimados señores del Consulado de España:", styles['Normal']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Cuerpo
        texto = f"""
        Mi nombre es <b>{nombre}</b>, soy ciudadano/a de <b>{nacionalidad}</b>, y me dirijo a ustedes 
        con el propósito de expresar mi gran interés y motivación para estudiar <b>{especialidad}</b> en España.
        <br/><br/>
        España representa para mí una oportunidad única de crecimiento académico y personal. La calidad 
        de su sistema educativo, su rica cultura y su ambiente multicultural son factores que me atraen 
        profundamente. He elegido este país no solo por su excelencia académica, sino también por la 
        posibilidad de desarrollarme en un entorno internacional que ampliará mi visión del mundo.
        <br/><br/>
        Mi objetivo es aprovechar al máximo esta experiencia educativa para adquirir conocimientos y 
        habilidades que me permitan contribuir al desarrollo de mi país al regresar. Estoy plenamente 
        comprometido/a con mi formación académica y cuento con los medios económicos necesarios para 
        cubrir mis gastos durante mi estancia en España.
        <br/><br/>
        Agradezco de antemano la atención prestada a mi solicitud y quedo a su disposición para 
        proporcionar cualquier información adicional que consideren necesaria.
        """
        
        elements.append(Paragraph(texto, styles['TextoJustificado']))
        elements.append(Spacer(1, 1.5*cm))
        
        # Despedida
        elements.append(Paragraph("Atentamente,", styles['Normal']))
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("_________________________", styles['Firma']))
        elements.append(Paragraph(f"<b>{nombre}</b>", styles['Firma']))
        
        # Pie de página
        GeneradorDocumentosOficiales._crear_pie_pagina(elements)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_formulario_solicitud(datos_estudiante):
        """
        Genera formulario de solicitud pre-llenado
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                              leftMargin=2*cm, rightMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
        
        elements = []
        styles = GeneradorDocumentosOficiales._get_estilos()
        
        # Encabezado
        GeneradorDocumentosOficiales._crear_encabezado(elements, "FORMULARIO DE SOLICITUD")
        
        elements.append(Paragraph("Datos del Solicitante", styles['SubtituloDocumento']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Tabla con datos
        datos = [
            ['<b>Campo</b>', '<b>Información</b>'],
            ['Nombre Completo:', datos_estudiante.get('nombre', 'N/A')],
            ['Email:', datos_estudiante.get('email', 'N/A')],
            ['Teléfono:', datos_estudiante.get('telefono', 'N/A')],
            ['Pasaporte:', datos_estudiante.get('pasaporte', 'N/A')],
            ['Edad:', str(datos_estudiante.get('edad') or 'N/A')],
            ['Nacionalidad:', datos_estudiante.get('nacionalidad', 'N/A')],
            ['Ciudad de Origen:', datos_estudiante.get('ciudad_origen', 'N/A')],
            ['Especialidad:', datos_estudiante.get('especialidad', 'N/A')],
            ['Nivel de Español:', (datos_estudiante.get('nivel_espanol') or 'N/A').capitalize()],
            ['Tipo de Visa:', (datos_estudiante.get('tipo_visa') or 'N/A').replace('_', ' ').title()],
        ]
        
        tabla = Table(datos, colWidths=[7*cm, 10*cm])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ]))
        
        elements.append(tabla)
        elements.append(Spacer(1, 1*cm))
        
        # Declaración
        elements.append(Paragraph("Declaración del Solicitante", styles['SubtituloDocumento']))
        elements.append(Spacer(1, 0.3*cm))
        
        declaracion = """
        Yo, <b>{}</b>, declaro que toda la información proporcionada en este formulario es 
        verdadera y completa. Comprendo que cualquier información falsa o incompleta puede resultar 
        en el rechazo de mi solicitud o la cancelación de mi visa.
        """.format(datos_estudiante.get('nombre', 'ESTUDIANTE'))
        
        elements.append(Paragraph(declaracion, styles['TextoJustificado']))
        elements.append(Spacer(1, 1*cm))
        
        # Fecha y firma
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        elements.append(Paragraph(f"Fecha: {fecha_actual}", styles['Normal']))
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("_________________________", styles['Firma']))
        elements.append(Paragraph("Firma del Solicitante", styles['Firma']))
        
        # Pie de página
        GeneradorDocumentosOficiales._crear_pie_pagina(elements)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_certificado_matricula(datos_estudiante):
        """
        Genera certificado de matrícula
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                              leftMargin=2*cm, rightMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
        
        elements = []
        styles = GeneradorDocumentosOficiales._get_estilos()
        
        # Encabezado
        GeneradorDocumentosOficiales._crear_encabezado(elements, "CERTIFICADO DE MATRÍCULA")
        
        # Número de certificado
        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        numero_cert = f"CERT-{datos_estudiante.get('id', '000')}-{datetime.now().year}"
        
        elements.append(Paragraph(
            f"<b>Número de Certificado:</b> {numero_cert}<br/>"
            f"<b>Fecha de Emisión:</b> {fecha_actual}",
            styles['Normal']
        ))
        elements.append(Spacer(1, 1*cm))
        
        # Certificación
        nombre = datos_estudiante.get('nombre', 'ESTUDIANTE')
        pasaporte = datos_estudiante.get('pasaporte', 'XXXXXXXXX')
        nacionalidad = datos_estudiante.get('nacionalidad', 'PAÍS')
        especialidad = datos_estudiante.get('especialidad', 'programa')
        
        texto_cert = f"""
        <b>LA AGENCIA EDUCATIVA ESPAÑA</b> certifica que:
        <br/><br/>
        El/La estudiante <b>{nombre}</b>, con pasaporte número <b>{pasaporte}</b>, 
        de nacionalidad <b>{nacionalidad}</b>, se encuentra <b>MATRICULADO/A</b> en 
        nuestro programa de <b>{especialidad}</b>.
        <br/><br/>
        El estudiante ha cumplido con todos los requisitos de admisión y se encuentra 
        en pleno derecho de cursar los estudios correspondientes durante el período académico 
        2025-2026.
        <br/><br/>
        Este certificado se expide a petición del interesado para los fines que estime convenientes, 
        especialmente para presentación ante autoridades migratorias.
        """
        
        elements.append(Paragraph(texto_cert, styles['TextoJustificado']))
        elements.append(Spacer(1, 1.5*cm))
        
        # Sello oficial (simulado con tabla)
        sello_data = [['SELLO OFICIAL\nAGENCIA EDUCATIVA ESPAÑA\n' + datetime.now().strftime("%Y")]]
        sello_table = Table(sello_data, colWidths=[6*cm], rowHeights=[3*cm])
        sello_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#667eea')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#667eea')),
        ]))
        
        # Tabla para firma y sello lado a lado
        firma_sello = Table([
            ['_________________________', sello_table],
            ['Firma Autorizada', ''],
            ['Director General', '']
        ], colWidths=[9*cm, 8*cm])
        firma_sello.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 1), (0, -1), 10),
        ]))
        
        elements.append(firma_sello)
        
        # Pie de página
        GeneradorDocumentosOficiales._crear_pie_pagina(elements)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
