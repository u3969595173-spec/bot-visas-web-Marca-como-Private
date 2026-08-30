#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de PDF Founding Partner - Capital Iberia
Crea un PDF futurista y profesional con el programa de partners
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.platypus import KeepTogether
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from datetime import datetime
import os

class PDFFundingPartner:
    def __init__(self, filename="Founding_Partner_Program.pdf"):
        self.filename = filename
        self.color_primary = HexColor("#00D9FF")  # Cyan futurista
        self.color_secondary = HexColor("#FF00FF")  # Magenta
        self.color_dark = HexColor("#0A0E27")  # Dark blue
        self.color_gold = HexColor("#FFD700")  # Gold accent
        self.color_white = HexColor("#FFFFFF")
        
    def crear_pdf(self):
        """Crea el PDF completo"""
        # Configurar documento
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Crear contenido
        story = []
        styles = self.get_custom_styles()
        
        # PORTADA
        story.append(self._crear_portada(styles))
        story.append(PageBreak())
        
        # RESUMEN DE LA PLATAFORMA
        story.append(self._crear_seccion_plataforma(styles))
        story.append(PageBreak())
        
        # PROGRAMA FOUNDING PARTNER
        story.append(self._crear_introduccion_partner(styles))
        story.append(Spacer(1, 0.2*inch))
        
        # Secciones del programa
        story.append(self._crear_condiciones_especiales(styles))
        story.append(Spacer(1, 0.15*inch))
        
        story.append(self._crear_comunidad_propia(styles))
        story.append(Spacer(1, 0.15*inch))
        
        story.append(self._crear_oportunidades(styles))
        story.append(PageBreak())
        
        # FONDO DE COMUNIDAD
        story.append(self._crear_fondo_comunidad(styles))
        story.append(Spacer(1, 0.15*inch))
        
        story.append(self._crear_patrocinio_eventos(styles))
        story.append(PageBreak())
        
        # PANEL Y SISTEMA DE OBJETIVOS
        story.append(self._crear_panel_partner(styles))
        story.append(Spacer(1, 0.15*inch))
        
        story.append(self._crear_sistema_objetivos(styles))
        story.append(Spacer(1, 0.2*inch))
        
        story.append(self._crear_vision_final(styles))
        
        # Generar PDF
        doc.build(story)
        print(f"✅ PDF creado: {os.path.abspath(self.filename)}")
    
    def get_custom_styles(self):
        """Define estilos personalizados"""
        styles = getSampleStyleSheet()
        
        # Títulos principales
        styles.add(ParagraphStyle(
            name='TituloPortada',
            parent=styles['Heading1'],
            fontSize=48,
            textColor=self.color_primary,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulos
        styles.add(ParagraphStyle(
            name='SubtituloPortada',
            parent=styles['Heading2'],
            fontSize=20,
            textColor=self.color_white,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Títulos de sección
        styles.add(ParagraphStyle(
            name='TituloSeccion',
            parent=styles['Heading2'],
            fontSize=24,
            textColor=self.color_gold,
            spaceAfter=12,
            spaceBefore=6,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulos de subsección
        styles.add(ParagraphStyle(
            name='SubtituloSeccion',
            fontSize=14,
            textColor=self.color_primary,
            spaceAfter=8,
            spaceBefore=4,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal
        styles.add(ParagraphStyle(
            name='TextoNormal',
            fontSize=11,
            textColor=HexColor("#333333"),
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            leading=16
        ))
        
        # Destacado
        styles.add(ParagraphStyle(
            name='TextoDestacado',
            fontSize=12,
            textColor=self.color_secondary,
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))
        
        return styles
    
    def _crear_portada(self, styles):
        """Crea la portada del PDF"""
        content = []
        
        content.append(Spacer(1, 1*inch))
        
        # Logo/Título
        content.append(Paragraph(
            "CAPITAL TRADE IBERIA",
            styles['TituloPortada']
        ))
        
        content.append(Spacer(1, 0.3*inch))
        
        # Subtítulo principal
        content.append(Paragraph(
            "PROGRAMA FOUNDING PARTNER",
            ParagraphStyle(
                name='TituloFP',
                fontSize=36,
                textColor=self.color_gold,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                spaceAfter=20
            )
        ))
        
        content.append(Spacer(1, 0.5*inch))
        
        # Descripción
        content.append(Paragraph(
            "Conviértete en Líder de Comunidad desde el Comienzo",
            styles['SubtituloPortada']
        ))
        
        content.append(Spacer(1, 0.3*inch))
        
        content.append(Paragraph(
            "Acceso Exclusivo · Beneficios Especiales · Oportunidades Prioritarias",
            ParagraphStyle(
                name='Lema',
                fontSize=13,
                textColor=self.color_primary,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
        ))
        
        content.append(Spacer(1, 1.2*inch))
        
        # Fecha y versión
        content.append(Paragraph(
            f"Documento Informativo - {datetime.now().strftime('%B %Y')}",
            ParagraphStyle(
                name='Footer',
                fontSize=9,
                textColor=HexColor("#999999"),
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique'
            )
        ))
        
        return KeepTogether(content)
    
    def _crear_seccion_plataforma(self, styles):
        """Crea la sección sobre qué hace la plataforma"""
        content = []
        
        content.append(Paragraph("SOBRE CAPITAL TRADE IBERIA", styles['TituloSeccion']))
        content.append(Spacer(1, 0.15*inch))
        
        content.append(Paragraph(
            """
            <b>Capital Iberia</b> es una plataforma de <b>operaciones comerciales con estructura y transparencia</b>, 
            diseñada para conectar inversores con oportunidades de participación en proyectos comerciales entre 
            España y Cuba.
            """,
            styles['TextoNormal']
        ))
        
        content.append(Spacer(1, 0.1*inch))
        
        # Características principales
        caracteristicas = [
            ("<b>🎯 Operaciones definidas:</b> Cada proyecto se presenta con condiciones específicas, capital requerido, plazo y documentación.",
             styles['TextoNormal']),
            ("<b>📊 Transparencia total:</b> Acceso a información completa antes de participar. No hay condiciones ocultas.",
             styles['TextoNormal']),
            ("<b>💼 Participación estructurada:</b> Definición clara de roles, capital, plazo y resultado esperado.",
             styles['TextoNormal']),
            ("<b>🔒 Seguridad y control:</b> Documentación legal, trazabilidad del proceso y validación administrativa.",
             styles['TextoNormal']),
            ("<b>👥 Comunidad activa:</b> Interacción entre inversores, compartir experiencias y aprender de otros participantes.",
             styles['TextoNormal']),
        ]
        
        for char, style in caracteristicas:
            content.append(Paragraph(char, style))
            content.append(Spacer(1, 0.05*inch))
        
        content.append(Spacer(1, 0.15*inch))
        
        # Alcance geográfico
        content.append(Paragraph(
            "<b>📍 Alcance:</b> Operaciones principalmente entre España y Cuba, con foco en logística, " +
            "exportación, financiación y oportunidades comerciales internacionales.",
            styles['TextoNormal']
        ))
        
        content.append(Spacer(1, 0.1*inch))
        
        # Importante
        content.append(Paragraph(
            "<b>⚠️ Declaración importante:</b> Toda operación conlleva riesgo comercial. " +
            "No se ofrecen rentabilidades garantizadas ni resultados asegurados. " +
            "Cada inversor debe evaluar el riesgo según su perfil y capacidad financiera.",
            ParagraphStyle(
                name='Importante',
                fontSize=10,
                textColor=self.color_secondary,
                alignment=TA_JUSTIFY,
                fontName='Helvetica-Bold',
                borderColor=self.color_secondary,
                borderWidth=1,
                borderPadding=8,
                spaceAfter=8
            )
        ))
        
        return KeepTogether(content)
    
    def _crear_introduccion_partner(self, styles):
        """Introducción al programa Founding Partner"""
        content = []
        
        content.append(Paragraph("FOUNDING PARTNER PROGRAM", styles['TituloSeccion']))
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph(
            """
            No buscamos simplemente afiliados o referidos. Buscamos <b>líderes de comunidad</b> que quieran 
            <b>construir desde el comienzo</b> dentro de Capital Iberia.
            <br/><br/>
            <i>"No queremos que seas un referido más. Queremos que seas uno de los líderes 
            que construyan la comunidad desde el inicio."</i>
            """,
            ParagraphStyle(
                name='Intro',
                fontSize=11,
                textColor=HexColor("#444444"),
                alignment=TA_JUSTIFY,
                leading=18,
                spaceAfter=12
            )
        ))
        
        content.append(Spacer(1, 0.1*inch))
        
        # Propuesta de valor
        content.append(Paragraph(
            "<b>TÚ APORTAS:</b> Comunidad consolidada, liderazgo y capacidad de crecimiento",
            ParagraphStyle(
                name='AportasHeader',
                fontSize=12,
                textColor=self.color_gold,
                fontName='Helvetica-Bold',
                spaceAfter=6
            )
        ))
        
        content.append(Paragraph(
            "NOSOTROS APORTAMOS: Plataforma, herramientas, promociones, oportunidades y recursos para desarrollar esa comunidad",
            ParagraphStyle(
                name='AportamosHeader',
                fontSize=12,
                textColor=self.color_primary,
                fontName='Helvetica-Bold',
                spaceAfter=12
            )
        ))
        
        return KeepTogether(content)
    
    def _crear_condiciones_especiales(self, styles):
        """Sección 1: Condiciones especiales"""
        content = []
        
        content.append(Paragraph("1️⃣ CONDICIONES ESPECIALES PARA EL PARTNER", styles['TituloSeccion']))
        content.append(Spacer(1, 0.1*inch))
        
        condiciones = [
            "✨ <b>Rango Executive Partner</b> - Nivel de acceso privilegiado dentro de la plataforma",
            "🏆 <b>Condiciones especiales</b> - Términos diferenciados en operaciones y oportunidades",
            "⚡ <b>Acceso prioritario</b> - Primero en ver y acceder a determinadas oportunidades",
            "🎁 <b>Promociones exclusivas</b> - Ofertas especiales no disponibles para otros usuarios",
            "👑 <b>Beneficios especiales</b> - Ventajas personalizadas según el crecimiento de tu comunidad",
        ]
        
        for cond in condiciones:
            content.append(Paragraph(cond, styles['TextoNormal']))
            content.append(Spacer(1, 0.05*inch))
        
        return KeepTogether(content)
    
    def _crear_comunidad_propia(self, styles):
        """Sección 2: Comunidad propia"""
        content = []
        
        content.append(Paragraph("2️⃣ TU PROPIA COMUNIDAD EN LA PLATAFORMA", styles['TituloSeccion']))
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph(
            "Como Founding Partner, podrás desarrollar y gestionar tu propia comunidad dentro de la plataforma. " +
            "Los miembros de tu comunidad tendrán acceso a beneficios exclusivos:",
            styles['TextoNormal']
        ))
        
        content.append(Spacer(1, 0.08*inch))
        
        beneficios = [
            "💰 Ofertas exclusivas reservadas para la comunidad",
            "🏷️ Descuentos especiales en operaciones",
            "🚀 Promociones prioritarias y acceso anticipado",
            "🎯 Oportunidades reservadas únicamente para tu comunidad",
            "🎉 Premios y acciones especiales",
        ]
        
        for ben in beneficios:
            content.append(Paragraph(ben, styles['TextoNormal']))
            content.append(Spacer(1, 0.04*inch))
        
        content.append(Spacer(1, 0.08*inch))
        
        content.append(Paragraph(
            "<b>Idea principal:</b> El líder puede ofrecer <b>ventajas reales y tangibles</b> a las personas " +
            "que forman parte de su comunidad, creando un ecosistema de valor compartido.",
            ParagraphStyle(
                name='Idea',
                fontSize=11,
                textColor=self.color_secondary,
                fontName='Helvetica-Bold',
                alignment=TA_JUSTIFY
            )
        ))
        
        return KeepTogether(content)
    
    def _crear_oportunidades(self, styles):
        """Sección 3: Oportunidades especiales"""
        content = []
        
        content.append(Paragraph("3️⃣ OPORTUNIDADES ESPECIALES Y PRIORITARIAS", styles['TituloSeccion']))
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph(
            "La plataforma lanzará <b>oportunidades comerciales puntuales</b> con capital o plazas limitadas. " +
            "Los Founding Partners y sus comunidades tendrán <b>acceso prioritario</b>.",
            styles['TextoNormal']
        ))
        
        content.append(Spacer(1, 0.08*inch))
        
        content.append(Paragraph(
            "<b>Características de las oportunidades:</b>",
            styles['SubtituloSeccion']
        ))
        
        content.append(Spacer(1, 0.05*inch))
        
        caract = [
            "Cada oportunidad tiene sus <b>propias condiciones</b> específicas",
            "<b>Plazo definido</b> para acceder a ellas",
            "<b>Capital limitado</b> disponible",
            "<b>Características únicas</b> según el tipo de operación",
        ]
        
        for c in caract:
            content.append(Paragraph(f"• {c}", styles['TextoNormal']))
            content.append(Spacer(1, 0.04*inch))
        
        return KeepTogether(content)
    
    def _crear_fondo_comunidad(self, styles):
        """Sección 4: Fondo de Comunidad"""
        content = []
        
        content.append(Paragraph("4️⃣ FONDO DE COMUNIDAD - TU PRESUPUESTO PARA CRECER", styles['TituloSeccion']))
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph(
            "Uno de los <b>principales beneficios</b> es el Fondo de Comunidad. A medida que tu comunidad " +
            "crece y cumple objetivos, <b>desbloquearás recursos</b> para desarrollarla.",
            ParagraphStyle(
                name='FondoIntro',
                fontSize=11,
                textColor=self.color_primary,
                fontName='Helvetica-Bold',
                alignment=TA_JUSTIFY
            )
        ))
        
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph("<b>Usos del Fondo:</b>", styles['SubtituloSeccion']))
        
        usos = [
            "🎪 Eventos y reuniones comunitarias",
            "🏢 Alquiler de locales",
            "📢 Publicidad y marketing",
            "🎨 Material promocional y merchandising",
            "🎁 Premios y acciones especiales",
            "✨ Actividades para la comunidad",
        ]
        
        for uso in usos:
            content.append(Paragraph(uso, styles['TextoNormal']))
            content.append(Spacer(1, 0.04*inch))
        
        content.append(Spacer(1, 0.12*inch))
        
        # Tabla de escalas
        content.append(Paragraph("<b>Ejemplo de escalas de desbloqueado (orientativo):</b>", styles['SubtituloSeccion']))
        content.append(Spacer(1, 0.08*inch))
        
        data = [
            [Paragraph("<b>Miembros Activos</b>", ParagraphStyle(name='HeaderTabla', fontSize=10, fontName='Helvetica-Bold', textColor=white, alignment=TA_CENTER)),
             Paragraph("<b>Fondo Desbloqueado</b>", ParagraphStyle(name='HeaderTabla', fontSize=10, fontName='Helvetica-Bold', textColor=white, alignment=TA_CENTER))],
            ["50", "hasta 500 €"],
            ["100", "hasta 1.000 €"],
            ["250", "hasta 2.500 €"],
            ["500", "hasta 5.000 €"],
            ["1.000+", "recursos personalizados"],
        ]
        
        table = Table(data, colWidths=[2.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor("#00D9FF")),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor("#F5F5F5")),
            ('GRID', (0, 0), (-1, -1), 1, HexColor("#CCCCCC")),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor("#F9F9F9")]),
        ]))
        
        content.append(table)
        
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph(
            "<i>Los límites definitivos dependerán del tamaño, actividad y evolución de cada comunidad.</i>",
            ParagraphStyle(
                name='Nota',
                fontSize=9,
                textColor=HexColor("#666666"),
                fontName='Helvetica-Oblique'
            )
        ))
        
        return KeepTogether(content)
    
    def _crear_patrocinio_eventos(self, styles):
        """Sección 5: Patrocinio de eventos"""
        content = []
        
        content.append(Paragraph("5️⃣ PATROCINIO DE EVENTOS", styles['TituloSeccion']))
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph(
            "Los Founding Partners podrán solicitar <b>apoyo de la plataforma</b> para organizar eventos " +
            "significativos de su comunidad. Capital Iberia puede participar como <b>patrocinador</b>.",
            styles['TextoNormal']
        ))
        
        content.append(Spacer(1, 0.08*inch))
        
        content.append(Paragraph("<b>Recursos disponibles como patrocinio:</b>", styles['SubtituloSeccion']))
        
        recursos = [
            "🏛️ Local para el evento",
            "📣 Publicidad y promoción",
            "🎥 Producción y contenido",
            "🎪 Material y equipamiento",
            "🎁 Merchandising y premios",
            "📱 Contenido para redes sociales",
        ]
        
        for rec in recursos:
            content.append(Paragraph(rec, styles['TextoNormal']))
            content.append(Spacer(1, 0.04*inch))
        
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph(
            "<b>Resultado:</b> El crecimiento de tu comunidad se convierte en <b>eventos y experiencias reales</b>, " +
            "generando conexión e impacto tangible.",
            ParagraphStyle(
                name='Resultado',
                fontSize=11,
                textColor=self.color_gold,
                fontName='Helvetica-Bold'
            )
        ))
        
        return KeepTogether(content)
    
    def _crear_panel_partner(self, styles):
        """Sección 6: Panel exclusivo"""
        content = []
        
        content.append(Paragraph("6️⃣ PANEL EXCLUSIVO DE PARTNER", styles['TituloSeccion']))
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph(
            "Cada líder tendrá acceso a un <b>panel personalizado</b> para controlar y monitorear " +
            "la evolución de su comunidad en tiempo real.",
            styles['TextoNormal']
        ))
        
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph("<b>Métricas principales del Panel:</b>", styles['SubtituloSeccion']))
        content.append(Spacer(1, 0.05*inch))
        
        metricas = [
            ("👥 <b>Miembros</b>", "Cantidad total de personas en tu comunidad"),
            ("🟢 <b>Usuarios activos</b>", "Miembros participando activamente en la plataforma"),
            ("🏆 <b>Nivel de Partner</b>", "Tu estatus actual y progreso hacia el siguiente nivel"),
            ("🎁 <b>Beneficios desbloqueados</b>", "Ventajas que ya tienes disponibles"),
            ("💰 <b>Fondo de Comunidad disponible</b>", "Dinero o recursos listos para utilizar"),
            ("🔥 <b>Próximo objetivo</b>", "Meta para desbloquear nuevos beneficios"),
        ]
        
        for metrica, desc in metricas:
            content.append(Paragraph(f"{metrica}: {desc}", styles['TextoNormal']))
            content.append(Spacer(1, 0.05*inch))
        
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph(
            "De esta forma, <b>ves claramente el crecimiento</b> de tu comunidad y los <b>beneficios que vas desbloqueando</b> " +
            "en tiempo real.",
            ParagraphStyle(
                name='PanelConclusion',
                fontSize=11,
                textColor=self.color_secondary,
                fontName='Helvetica-Bold',
                alignment=TA_JUSTIFY
            )
        ))
        
        return KeepTogether(content)
    
    def _crear_sistema_objetivos(self, styles):
        """Sección 7: Sistema de objetivos"""
        content = []
        
        content.append(Paragraph("7️⃣ SISTEMA DE NIVELES Y OBJETIVOS", styles['TituloSeccion']))
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph(
            "El programa tiene <b>diferentes niveles</b> para los líderes. A medida que tu comunidad aumenta, " +
            "desbloquearás progresivamente mayores beneficios.",
            styles['TextoNormal']
        ))
        
        content.append(Spacer(1, 0.1*inch))
        
        content.append(Paragraph("<b>Beneficios que se desbloquean:</b>", styles['SubtituloSeccion']))
        
        desbloqueos = [
            "📈 Mayor Fondo de Comunidad disponible",
            "🎯 Mejores promociones en operaciones",
            "⚡ Mayor acceso y prioridad a oportunidades",
            "👥 Más beneficios para tus miembros",
            "🎪 Eventos de mayor categoría y presupuesto",
            "👑 Recompensas y reconocimientos adicionales",
        ]
        
        for desbloq in desbloqueos:
            content.append(Paragraph(desbloq, styles['TextoNormal']))
            content.append(Spacer(1, 0.05*inch))
        
        return KeepTogether(content)
    
    def _crear_vision_final(self, styles):
        """Sección final con la visión"""
        content = []
        
        content.append(Spacer(1, 0.2*inch))
        
        content.append(Paragraph(
            "🚀 LA IDEA FINAL",
            ParagraphStyle(
                name='VisionTitle',
                fontSize=22,
                textColor=self.color_gold,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
        ))
        
        content.append(Spacer(1, 0.15*inch))
        
        content.append(Paragraph(
            """
            No buscamos simplemente ampliar nuestro alcance con referidos tradicionales.
            <br/><br/>
            Buscamos <b>construir líderes comunitarios</b> desde el comienzo, que sean 
            <b>propietarios del crecimiento</b> junto con nosotros.
            <br/><br/>
            <b>Founding Partners</b> significa ser <b>pionero en la construcción de 
            una comunidad</b> dentro de Capital Iberia, con beneficios exclusivos, 
            recursos dedicados y crecimiento compartido.
            <br/><br/>
            <i>"Tu comunidad es nuestro comunidad. Tu éxito es nuestro éxito."</i>
            """,
            ParagraphStyle(
                name='VisionText',
                fontSize=12,
                textColor=HexColor("#333333"),
                alignment=TA_CENTER,
                leading=20,
                spaceAfter=16
            )
        ))
        
        content.append(Spacer(1, 0.2*inch))
        
        # Disclaimer legal
        content.append(Paragraph(
            """
            <b>Declaración legal:</b> Las condiciones económicas, recompensas y cualquier producto 
            de inversión se establecerán de acuerdo con la estructura jurídica y regulatoria aplicable 
            antes de ofrecerlas al público. Este documento es informativo y no constituye una oferta 
            vinculante.
            """,
            ParagraphStyle(
                name='Disclaimer',
                fontSize=8,
                textColor=HexColor("#666666"),
                alignment=TA_JUSTIFY,
                borderColor=HexColor("#CCCCCC"),
                borderWidth=1,
                borderPadding=6,
                fontName='Helvetica-Oblique'
            )
        ))
        
        content.append(Spacer(1, 0.15*inch))
        
        # Footer
        content.append(Paragraph(
            f"Capital Iberia | www.capitaliberia.com | {datetime.now().strftime('%d de %B de %Y')}",
            ParagraphStyle(
                name='PDFFooter',
                fontSize=8,
                textColor=HexColor("#999999"),
                alignment=TA_CENTER
            )
        ))
        
        return KeepTogether(content)

if __name__ == "__main__":
    # Crear y generar PDF
    pdf = PDFFundingPartner("Founding_Partner_Program.pdf")
    pdf.crear_pdf()
    print("\n✨ PDF Founding Partner generado exitosamente!")
    print("📍 Ubicación: Founding_Partner_Program.pdf")
