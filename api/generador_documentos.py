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
    def generar_declaracion_jurada_fondos(datos_estudiante):
        """
        Genera declaración jurada de fondos económicos
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              leftMargin=2*cm, rightMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
        
        elements = []
        styles = GeneradorDocumentosOficiales._get_estilos()
        
        # Encabezado
        GeneradorDocumentosOficiales._crear_encabezado(elements, "DECLARACIÓN JURADA DE FONDOS ECONÓMICOS")
        
        # Fecha y referencia
        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        nombre = datos_estudiante.get('nombre', 'ESTUDIANTE')
        pasaporte = datos_estudiante.get('pasaporte', 'XXXXXXXXX')
        nacionalidad = datos_estudiante.get('nacionalidad', 'PAÍS')
        ciudad_origen = datos_estudiante.get('ciudad_origen', 'ciudad')
        
        elements.append(Paragraph(
            f"<b>Lugar y Fecha:</b> {ciudad_origen}, {fecha_actual}<br/>"
            f"<b>Referencia:</b> DECL-FONDOS-{datos_estudiante.get('id', '000')}-2025",
            styles['Normal']
        ))
        elements.append(Spacer(1, 0.8*cm))
        
        # Declaración
        texto_declaracion = f"""
        Yo, <b>{nombre}</b>, con pasaporte número <b>{pasaporte}</b>, de nacionalidad <b>{nacionalidad}</b>, 
        declaro bajo juramento que:
        <br/><br/>
        <b>1. MEDIOS ECONÓMICOS SUFICIENTES:</b><br/>
        Cuento con los medios económicos necesarios para cubrir todos los gastos derivados de mi estancia 
        en España durante el período de estudios, incluyendo pero no limitándose a: matrícula universitaria, 
        alojamiento, alimentación, transporte, seguro médico, y gastos personales.
        <br/><br/>
        <b>2. FUENTES DE FINANCIAMIENTO:</b><br/>
        Los fondos provienen de fuentes lícitas y legítimas, incluyendo ahorros personales, apoyo familiar, 
        becas, o combinación de las anteriores.
        <br/><br/>
        <b>3. SOLVENCIA ECONÓMICA:</b><br/>
        Me comprometo a mantener la solvencia económica durante toda mi estancia en España y a no constituir 
        una carga para el sistema de asistencia social español.
        <br/><br/>
        <b>4. DOCUMENTACIÓN RESPALDATORIA:</b><br/>
        Adjunto a esta declaración los documentos que acreditan mi capacidad económica (extractos bancarios, 
        cartas de patrocinio, certificados de ingresos, etc.).
        """
        
        elements.append(Paragraph(texto_declaracion, styles['TextoJustificado']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Tabla de estimación de gastos mensuales
        elements.append(Paragraph("<b>Estimación de Gastos Mensuales en España:</b>", styles['SubtituloDocumento']))
        elements.append(Spacer(1, 0.3*cm))
        
        gastos = [
            ['<b>Concepto</b>', '<b>Monto Estimado (EUR)</b>'],
            ['Alojamiento', '400 - 700'],
            ['Alimentación', '250 - 350'],
            ['Transporte', '40 - 60'],
            ['Seguro Médico', '50 - 100'],
            ['Material de Estudio', '50 - 100'],
            ['Gastos Personales', '100 - 200'],
            ['<b>TOTAL MENSUAL</b>', '<b>890 - 1,510 EUR</b>'],
        ]
        
        tabla_gastos = Table(gastos, colWidths=[10*cm, 7*cm])
        tabla_gastos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f7fafc')]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#edf2f7')),
        ]))
        elements.append(tabla_gastos)
        elements.append(Spacer(1, 1*cm))
        
        # Compromiso final
        elements.append(Paragraph(
            "Declaro que toda la información proporcionada es veraz y que asumo plena responsabilidad "
            "sobre la misma. Estoy consciente de las implicaciones legales de proporcionar información falsa.",
            styles['TextoJustificado']
        ))
        elements.append(Spacer(1, 1.5*cm))
        
        # Firma
        elements.append(Paragraph("_________________________", styles['Firma']))
        elements.append(Paragraph(f"<b>{nombre}</b>", styles['Firma']))
        elements.append(Paragraph(f"Pasaporte: {pasaporte}", styles['Firma']))
        
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
    def generar_carta_patrocinio(datos_estudiante):
        """
        Genera carta de patrocinio económico
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                              leftMargin=2*cm, rightMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
        
        elements = []
        styles = GeneradorDocumentosOficiales._get_estilos()
        
        # Encabezado
        GeneradorDocumentosOficiales._crear_encabezado(elements, "CARTA DE PATROCINIO ECONÓMICO")
        
        # Fecha y referencia
        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        numero_ref = f"PATR-{datos_estudiante.get('id', '000')}-{datetime.now().year}"
        
        nombre = datos_estudiante.get('nombre', 'ESTUDIANTE')
        pasaporte = datos_estudiante.get('pasaporte', 'XXXXXXXXX')
        nacionalidad = datos_estudiante.get('nacionalidad', 'PAÍS')
        especialidad = datos_estudiante.get('especialidad', 'programa')
        ciudad_origen = datos_estudiante.get('ciudad_origen', 'ciudad')
        
        elements.append(Paragraph(
            f"<b>Lugar y Fecha:</b> {ciudad_origen}, {fecha_actual}<br/>"
            f"<b>Referencia:</b> {numero_ref}<br/>"
            f"<b>A quien corresponda:</b>",
            styles['Normal']
        ))
        elements.append(Spacer(1, 0.8*cm))
        
        # Carta de patrocinio
        texto_patrocinio = f"""
        Por medio de la presente, yo <b>[NOMBRE DEL PATROCINADOR]</b>, con documento de identidad 
        número <b>[DOCUMENTO]</b>, residente en <b>[DIRECCIÓN COMPLETA]</b>, manifiesto que:
        <br/><br/>
        <b>DECLARO:</b>
        <br/><br/>
        <b>1. COMPROMISO DE PATROCINIO:</b><br/>
        Me comprometo a patrocinar económicamente al/la estudiante <b>{nombre}</b>, con pasaporte 
        número <b>{pasaporte}</b>, de nacionalidad <b>{nacionalidad}</b>, durante su estancia en 
        España para cursar estudios de <b>{especialidad}</b>.
        <br/><br/>
        <b>2. COBERTURA ECONÓMICA:</b><br/>
        Me comprometo a cubrir todos los gastos necesarios para la estancia del estudiante en España, 
        incluyendo:
        """
        
        elements.append(Paragraph(texto_patrocinio, styles['TextoJustificado']))
        elements.append(Spacer(1, 0.3*cm))
        
        # Lista de gastos cubiertos
        gastos_cubiertos = [
            ['✓', 'Matrícula universitaria y costos académicos'],
            ['✓', 'Alojamiento durante toda la estancia'],
            ['✓', 'Alimentación y gastos de manutención'],
            ['✓', 'Seguro médico internacional'],
            ['✓', 'Transporte y movilidad'],
            ['✓', 'Gastos personales y emergencias'],
        ]
        
        tabla_gastos = Table(gastos_cubiertos, colWidths=[1*cm, 16*cm])
        tabla_gastos.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#48bb78')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(tabla_gastos)
        elements.append(Spacer(1, 0.5*cm))
        
        # Continuación
        texto_cont = """
        <b>3. CAPACIDAD ECONÓMICA:</b><br/>
        Cuento con la capacidad económica suficiente para cumplir con este compromiso, como lo 
        demuestran los documentos adjuntos (extractos bancarios, certificados de ingresos, etc.).
        <br/><br/>
        <b>4. RELACIÓN CON EL ESTUDIANTE:</b><br/>
        Mi relación con el/la estudiante es: <b>[ESPECIFICAR: Padre/Madre/Familiar/Otro]</b>.
        <br/><br/>
        <b>5. DATOS DE CONTACTO:</b><br/>
        Teléfono: <b>[TELÉFONO DEL PATROCINADOR]</b><br/>
        Email: <b>[EMAIL DEL PATROCINADOR]</b>
        <br/><br/>
        Esta carta se emite de manera voluntaria para respaldar la solicitud de visa de estudiante 
        del beneficiario ante las autoridades consulares españolas.
        """
        
        elements.append(Paragraph(texto_cont, styles['TextoJustificado']))
        elements.append(Spacer(1, 1*cm))
        
        # Nota importante
        nota_style = ParagraphStyle(
            'NotaStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#e53e3e'),
            borderColor=colors.HexColor('#e53e3e'),
            borderWidth=1,
            borderPadding=10,
            spaceAfter=10
        )
        elements.append(Paragraph(
            "<b>NOTA:</b> Esta carta debe ser completada con los datos reales del patrocinador, "
            "firmada y acompañada de documentación que acredite la solvencia económica del mismo.",
            nota_style
        ))
        elements.append(Spacer(1, 1*cm))
        
        # Firma del patrocinador
        elements.append(Paragraph("Atentamente,", styles['Normal']))
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("_________________________", styles['Firma']))
        elements.append(Paragraph("<b>[Nombre del Patrocinador]</b>", styles['Firma']))
        elements.append(Paragraph("[Documento de Identidad]", styles['Firma']))
        elements.append(Paragraph("[Firma]", styles['Firma']))
        
        # Pie de página
        GeneradorDocumentosOficiales._crear_pie_pagina(elements)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
