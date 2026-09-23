from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR / "frontend" / "public" / "assets" / "reglas-torneo-domino-iberia.pdf"


def footer(canvas, document):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D6B86A"))
    canvas.line(2 * cm, 1.6 * cm, A4[0] - 2 * cm, 1.6 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#315749"))
    canvas.drawString(2 * cm, 1.1 * cm, "DOMINO IBERIA | Reglamento de torneo")
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"Pagina {document.page}")
    canvas.restoreState()


def paragraph(text, style):
    return Paragraph(text, style)


def build_pdf():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.7 * cm,
        bottomMargin=2.3 * cm,
        title="Reglamento del Torneo de Domino Iberia",
        author="Capital Iberia",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "DominoTitle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=27, leading=32, textColor=colors.HexColor("#0A4133"), alignment=TA_CENTER,
        spaceAfter=8,
    )
    subtitle = ParagraphStyle(
        "DominoSubtitle", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=11, leading=16, textColor=colors.HexColor("#8A6B22"), alignment=TA_CENTER,
        spaceAfter=22,
    )
    heading = ParagraphStyle(
        "DominoHeading", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=15, leading=19, textColor=colors.HexColor("#0A4133"), spaceBefore=12, spaceAfter=8,
    )
    body = ParagraphStyle(
        "DominoBody", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=10.3, leading=15, alignment=TA_JUSTIFY, textColor=colors.HexColor("#142A22"), spaceAfter=7,
    )
    bullet = ParagraphStyle(
        "DominoBullet", parent=body, leftIndent=13, firstLineIndent=-10, spaceAfter=5,
    )
    note = ParagraphStyle(
        "DominoNote", parent=body, fontName="Helvetica-Bold", textColor=colors.HexColor("#0A4133"),
        borderColor=colors.HexColor("#D6B86A"), borderWidth=1, borderPadding=9,
        backColor=colors.HexColor("#F8F1DD"), spaceBefore=8, spaceAfter=12,
    )

    story = [
        paragraph("REGLAMENTO", title),
        paragraph("TORNEO DE DOMINO IBERIA | Modalidad suiza con fase final", subtitle),
        paragraph("Este documento explica como se juega una partida oficial y como funciona el torneo dentro de la plataforma Domino Iberia.", body),
        paragraph("1. INSCRIPCION Y PAREJAS", heading),
        paragraph("- Cada participacion es por <b>pareja</b>: dos jugadores forman un equipo.", bullet),
        paragraph("- Un jugador crea un codigo de pareja y se lo comparte a su companero. El companero usa ese codigo para unirse.", bullet),
        paragraph("- La pareja queda pendiente hasta que el administrador la apruebe. Solo las parejas aprobadas entran al ranking y a las rondas.", bullet),
        paragraph("- El administrador define el minimo de parejas para iniciar. El torneo puede aceptar hasta 30 parejas.", bullet),
        paragraph("- La inscripcion se indica en fichas virtuales por pareja y se muestra en la ficha del torneo.", bullet),
        paragraph("- Para jugar, ambos integrantes de una pareja deben activar la ubicacion del navegador y estar separados por al menos 1 km.", bullet),
        paragraph("Importante: las mesas oficiales se crean desde el torneo; no existen mesas libres fuera de sus rondas.", note),
        paragraph("2. FORMATO DE LA PARTIDA", heading),
        paragraph("- Cada mesa tiene cuatro jugadores, organizados en dos parejas. Los companeros se sientan frente a frente.", bullet),
        paragraph("- Se juega con domino doble-seis: 28 fichas. Cada jugador recibe 7 fichas al inicio de cada mano.", bullet),
        paragraph("- En la primera mano comienza quien tenga el doble-seis [6|6]. En las manos siguientes el turno inicial rota.", bullet),
        paragraph("- En tu turno debes colocar una ficha que coincida con uno de los extremos abiertos de la mesa. Puedes elegir el extremo izquierdo o derecho si la jugada es valida.", bullet),
        paragraph("- Si no tienes una ficha valida, debes pasar. No se toman fichas adicionales.", bullet),
        paragraph("- La mano termina cuando un jugador se queda sin fichas o cuando el juego queda cerrado despues de los pases correspondientes.", bullet),
        paragraph("- Al cerrar una mano, la pareja ganadora suma los puntos de las fichas restantes. Si existe empate al cerrar, gana la pareja que inicio la mano.", bullet),
        paragraph("- La partida termina cuando una pareja llega o supera 200 puntos.", bullet),
        PageBreak(),
        paragraph("3. RONDAS SUIZAS", heading),
        paragraph("- El torneo disputa 10 rondas suizas. Todas las parejas aprobadas siguen participando durante estas rondas.", bullet),
        paragraph("- El administrador genera la siguiente ronda solo cuando todas las mesas de la ronda anterior terminaron.", bullet),
        paragraph("- La primera ronda se empareja de forma aleatoria. En las siguientes, las parejas se cruzan segun su posicion en el ranking.", bullet),
        paragraph("- El sistema evita repetir rivales durante el torneo.", bullet),
        paragraph("- Cada pareja recibe una mesa oficial con acceso dentro de la plataforma. El estado de mesas, ranking e inscritos se actualiza automaticamente.", bullet),
        paragraph("4. RANKING", heading),
        paragraph("El ranking se ordena por los siguientes criterios:", body),
    ]

    ranking_table = Table([
        ["Orden", "Criterio", "Detalle"],
        ["1", "Victorias", "Gana la pareja que vence mas partidas."],
        ["2", "Diferencia", "Puntos a favor menos puntos en contra. Ejemplo: 200-50 = +150."],
        ["3", "Puntos a favor", "Se usa como desempate adicional."],
    ], colWidths=[1.2 * cm, 4 * cm, 10.3 * cm])
    ranking_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0A4133")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("LEADING", (0, 0), (-1, -1), 13),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C9D5CE")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F8F5EA"), colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ]))
    story.extend([
        ranking_table,
        Spacer(1, 12),
        paragraph("5. FASE FINAL", heading),
        paragraph("Al terminar las 10 rondas suizas, las ocho primeras parejas del ranking clasifican a eliminatorias:", body),
        paragraph("- Cuartos de final: 1 vs 8, 2 vs 7, 3 vs 6 y 4 vs 5.", bullet),
        paragraph("- Semifinales: los ganadores de cuartos disputan dos llaves.", bullet),
        paragraph("- Final: los ganadores de semifinales compiten por el primer lugar.", bullet),
        paragraph("- Tercer puesto: los perdedores de semifinales juegan por el tercer lugar.", bullet),
        paragraph("- Premios: ademas del podio, las parejas que finalicen del 4. al 8. lugar tambien reciben el premio configurado para esa posicion.", bullet),
        paragraph("6. BUENAS PRACTICAS", heading),
        paragraph("- Mantente conectado durante tu mesa y revisa el tablero con frecuencia.", bullet),
        paragraph("- Activa la ubicacion antes de jugar para evitar bloqueos de turno.", bullet),
        paragraph("- Usa el codigo de pareja solo con la persona que sera tu companero en el torneo.", bullet),
        paragraph("- El administrador aprueba las parejas y genera las rondas oficiales. Las decisiones de organizacion se reflejan en la pantalla del torneo.", bullet),
        paragraph("Domino Iberia promueve partidas limpias, competitivas y respetuosas. Buena suerte a todas las parejas.", note),
    ])

    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"PDF creado: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()