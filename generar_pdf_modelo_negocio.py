from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT_PATH = Path(__file__).with_name("Carta_Presentacion_Modelo_Negocio_Capital_Trade_Iberia.pdf")

NAVY = colors.HexColor("#07111F")
BLUE = colors.HexColor("#0E7490")
GOLD = colors.HexColor("#C58E22")
PALE_GOLD = colors.HexColor("#FFF7E6")
SLATE = colors.HexColor("#475569")
LIGHT = colors.HexColor("#F8FAFC")
BORDER = colors.HexColor("#CBD5E1")
RED = colors.HexColor("#B91C1C")


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CoverBrand", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=29, leading=34, textColor=colors.white, alignment=TA_CENTER, spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle", parent=styles["Normal"], fontName="Helvetica",
        fontSize=14, leading=20, textColor=colors.HexColor("#D7E3F0"), alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="Heading", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=18, leading=23, textColor=NAVY, spaceBefore=6, spaceAfter=11,
    ))
    styles.add(ParagraphStyle(
        name="Subheading", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=12.5, leading=16, textColor=BLUE, spaceBefore=10, spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name="Body", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=9.7, leading=14.5, textColor=SLATE, spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name="Small", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=8.5, leading=12, textColor=SLATE, spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name="BulletText", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=9.5, leading=14, textColor=SLATE, leftIndent=13, firstLineIndent=-9, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="Callout", parent=styles["BodyText"], fontName="Helvetica-Bold",
        fontSize=10, leading=14.5, textColor=NAVY, spaceAfter=0,
    ))
    styles.add(ParagraphStyle(
        name="Risk", parent=styles["BodyText"], fontName="Helvetica-Bold",
        fontSize=9.5, leading=14, textColor=RED, spaceAfter=5,
    ))
    return styles


def paragraph(text, style):
    return Paragraph(text, style)


def info_box(text, styles, color=PALE_GOLD):
    table = Table([[paragraph(text, styles["Callout"])]], colWidths=[17.2 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("BOX", (0, 0), (-1, -1), 0.75, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return table


def bullet(text, styles):
    return paragraph(f"<b>•</b> {text}", styles["BulletText"])


def page_header_footer(canvas, document):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1)
    canvas.line(1.5 * cm, height - 1.25 * cm, width - 1.5 * cm, height - 1.25 * cm)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(1.5 * cm, height - 0.95 * cm, "CAPITAL TRADE IBERIA")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(SLATE)
    canvas.drawRightString(width - 1.5 * cm, 0.8 * cm, f"Modelo de negocio | Pagina {document.page}")
    canvas.restoreState()


def make_document():
    styles = build_styles()
    document = SimpleDocTemplate(
        str(OUTPUT_PATH), pagesize=A4,
        rightMargin=1.5 * cm, leftMargin=1.5 * cm,
        topMargin=1.7 * cm, bottomMargin=1.35 * cm,
        title="Carta de presentacion - Modelo de negocio - Capital Trade Iberia",
        author="Capital Trade Iberia",
    )
    story = []

    cover = Table([[""], [paragraph("CAPITAL TRADE IBERIA", styles["CoverBrand"])], [paragraph(
        "Carta de presentacion del modelo de negocio y funcionamiento de la plataforma", styles["CoverSubtitle"]
    )], [""], [paragraph(
        "Informacion para usuarios interesados", styles["CoverSubtitle"]
    )], [paragraph(
        f"Version informativa | {date.today().strftime('%d/%m/%Y')}", styles["CoverSubtitle"]
    )]], colWidths=[17.2 * cm], rowHeights=[4 * cm, None, None, 6.7 * cm, None, None])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LINEBELOW", (0, 1), (0, 1), 2, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story += [Spacer(1, 2.1 * cm), cover, PageBreak()]

    story += [
        paragraph("1. Carta de presentacion", styles["Heading"]),
        paragraph(
            "Capital Trade Iberia es una plataforma digital de gestion e informacion sobre participaciones en operaciones comerciales. "
            "Su objetivo es organizar el acceso de usuarios a oportunidades comerciales, facilitar la trazabilidad de las solicitudes y permitir el seguimiento de cada participacion desde un panel personal.",
            styles["Body"],
        ),
        paragraph(
            "La plataforma no sustituye el analisis individual de cada usuario ni actua como entidad financiera regulada o asesor de inversion homologado. "
            "Las condiciones finales de cada participacion se comunican y documentan antes de formalizarla.",
            styles["Body"],
        ),
        info_box(
            "Principio de transparencia: cada aportacion se registra como una operacion individual, con importe, moneda, fecha, estado y movimientos propios. "
            "Una nueva aportacion no modifica la fecha, el bloqueo ni el avance de las anteriores.", styles,
        ),
        Spacer(1, 10),
        paragraph("Contenido de esta guia", styles["Subheading"]),
        bullet("Que tipo de operaciones se presentan y como se estructura el capital.", styles),
        bullet("Como se registra, valida y activa una participacion.", styles),
        bullet("Como se reflejan rentabilidad, limites, referidos, retiros y programas de rango.", styles),
        bullet("Que controles, responsabilidades y riesgos debe conocer cualquier usuario antes de participar.", styles),
        PageBreak(),
    ]

    story += [
        paragraph("2. Que hacemos", styles["Heading"]),
        paragraph(
            "La actividad se orienta a la presentacion y gestion operativa de oportunidades comerciales. Entre las lineas que pueden analizarse se encuentran compraventa y logistica de materiales, "
            "operaciones de alimentacion y exportacion, proyectos de apoyo a MYPIMEs, remesas y otras operaciones de comercio internacional. "
            "Cada oportunidad tiene condiciones, necesidades de capital, documentos y plazos que deben revisarse de forma particular.", styles["Body"]
        ),
        paragraph("Ciclo general de una operacion", styles["Subheading"]),
    ]
    rows = [
        ["Etapa", "Descripcion"],
        ["1. Analisis", "La administracion identifica una necesidad comercial y define informacion, capital objetivo, contexto y condiciones de participacion."],
        ["2. Presentacion", "La oportunidad se muestra o se comunica a los usuarios que correspondan, junto con sus datos operativos disponibles."],
        ["3. Participacion", "El usuario solicita una aportacion en la moneda y el metodo habilitados, y aporta el comprobante requerido."],
        ["4. Validacion", "La administracion revisa la solicitud y el comprobante. Una participacion solo entra en el ciclo cuando se valida."],
        ["5. Seguimiento", "El panel refleja el estado de la aportacion, sus movimientos y las comunicaciones operativas publicadas."],
    ]
    table = Table([[paragraph(cell, styles["Small"]) for cell in row] for row in rows], colWidths=[3.3 * cm, 13.9 * cm])
    table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story += [table, Spacer(1, 10), info_box(
        "Una operacion comercial puede tener riesgos de mercado, logistica, contraparte, regulacion, divisa y ejecucion. La existencia de una oportunidad en la plataforma no elimina esos riesgos.",
        styles, colors.HexColor("#FFF1F2"),
    ), PageBreak()]

    story += [
        paragraph("3. Como participa un usuario", styles["Heading"]),
        paragraph("El recorrido se ha disenado para que el usuario pueda revisar y controlar cada paso desde su cuenta.", styles["Body"]),
        paragraph("Paso 1. Registro y acceso", styles["Subheading"]),
        paragraph("El usuario crea una cuenta con datos veraces y mantiene sus credenciales de acceso de forma personal y confidencial. La cuenta permite consultar las opciones disponibles, solicitudes, avisos, movimientos y documentacion asociada.", styles["Body"]),
        paragraph("Paso 2. Eleccion de importe y moneda", styles["Subheading"]),
        paragraph("Desde el panel se selecciona el importe y una moneda o metodo que este configurado en ese momento. La configuracion puede incluir MLC, CUP, EUR o USDT por red BEP-20. Los minimos de participacion actualmente configurados son 50 MLC, 25.000 CUP y 50 USDT. Las cuentas receptoras e instrucciones deben revisarse en el momento de la solicitud.", styles["Body"]),
        paragraph("Paso 3. Transferencia y comprobante", styles["Subheading"]),
        paragraph("El usuario realiza la transferencia siguiendo los datos mostrados y carga el comprobante. La solicitud queda registrada como pendiente de validacion; el usuario no debe considerar una aportacion activa antes de la revision administrativa.", styles["Body"]),
        paragraph("Paso 4. Revision y activacion", styles["Subheading"]),
        paragraph("La administracion valida o rechaza la solicitud. Al validarse, se registra una fecha de aprobacion para esa aportacion concreta. El panel muestra la situacion de cada contrato de forma independiente.", styles["Body"]),
        PageBreak(),
    ]

    story += [
        paragraph("4. Contratos independientes, bloqueo y evolucion", styles["Heading"]),
        paragraph(
            "Cada aportacion constituye un contrato separado. Si una persona aporta 1.000 USDT hoy y otros 1.000 USDT en una fecha posterior, el sistema conserva dos identificadores, dos fechas de aprobacion, dos bloques de seguimiento y dos avances distintos.", styles["Body"]
        ),
        paragraph("Bloqueo de seguridad de 72 horas", styles["Subheading"]),
        paragraph(
            "Tras la aprobacion, la aportacion permanece bloqueada durante 72 horas. Es el tiempo operativo en el que el dinero se incorpora, organiza y posiciona dentro del ciclo comercial del negocio antes de quedar disponible para su seguimiento. Mientras ese periodo sigue vigente, la aportacion se visualiza como bloqueada o retenida y no se incluye como capital liberado para la distribucion diaria. Cada reloj pertenece unicamente a la aportacion a la que acompana.", styles["Body"]
        ),
        paragraph("Distribucion diaria gestionada por administracion", styles["Subheading"]),
        paragraph(
            "Una vez superado el bloqueo, la administracion puede aplicar manualmente una distribucion diaria variable a las aportaciones elegibles. Como referencia operativa, ese rendimiento diario puede situarse entre el 0,5% y el 1,5%, segun las condiciones de las operaciones comerciales en curso. No existe un calendario automatico que prometa un porcentaje fijo: cualquier porcentaje, frecuencia o resultado depende de las condiciones aplicables, la operacion y la gestion administrativa.", styles["Body"]
        ),
        paragraph("Referencia del limite del 300%", styles["Subheading"]),
        paragraph(
            "El sistema usa para cada aportacion un limite de seguimiento equivalente a tres veces el importe inicial. Cuando las ganancias registradas de ese contrato alcanzan su limite, el contrato se marca como completado. Este limite es una regla tecnica de control del modelo y no una garantia de rentabilidad, recuperacion de capital ni plazo de cobro.", styles["Body"]
        ),
        info_box("Lo importante para el usuario: una aportacion nueva no se fusiona con una anterior. Por ello, puede haber contratos bloqueados, activos o completados al mismo tiempo.", styles),
        PageBreak(),
    ]

    story += [
        paragraph("5. Referidos, rangos y ofertas", styles["Heading"]),
        paragraph("Codigo de referido y aceleracion", styles["Subheading"]),
        paragraph(
            "El panel puede asignar a cada usuario un codigo de referido. Cuando un referido directo realiza una aportacion que la administracion valida, el modelo contempla una aceleracion equivalente al 10% del importe de esa aportacion para el patrocinador.", styles["Body"]
        ),
        paragraph(
            "La aceleracion no crea un contrato nuevo ni se presenta como un retiro separado. Se registra como ganancia acelerada dentro de los contratos del patrocinador. La asignacion sigue orden de antiguedad: se aplica primero al contrato activo mas antiguo con espacio hasta su limite; si lo completa y queda remanente, el sistema continua con el siguiente contrato elegible.", styles["Body"]
        ),
        paragraph("Programas de rango", styles["Subheading"]),
        paragraph(
            "La plataforma dispone de dos programas de fidelizacion independientes: Partner, para quien crece mediante capital propio, y Comunidad, para quien desarrolla una red de referidos activos. Una persona puede cumplir las condiciones de ambos al mismo tiempo y recibir los beneficios temporales que correspondan a cada programa, conforme a sus reglas vigentes.", styles["Body"]
        ),
        paragraph("Programa Partner: requiere inversion propia, no requiere referidos", styles["Subheading"]),
        paragraph(
            "Este es el programa para quien desea avanzar solo con su propia participacion de capital. Para entrar se debe mantener capital propio dentro del programa; no se exige atraer ni mantener referidos. El rango se determina por el capital total propio y no por las aportaciones de otras personas.", styles["Body"]
        ),
        bullet("Partner: de 500 a 999 USDT de capital propio. Beneficio de 25 USDT al mes durante 2 meses.", styles),
        bullet("Premium Partner: de 1.000 a 2.499 USDT. Beneficio de 50 USDT al mes durante 3 meses.", styles),
        bullet("VIP Partner: de 2.500 a 4.999 USDT. Beneficio de 100 USDT al mes durante 4 meses.", styles),
        bullet("Strategic Partner: de 5.000 a 9.999 USDT. Beneficio de 150 USDT al mes durante 6 meses.", styles),
        bullet("Founding Partner: desde 10.000 USDT. Beneficio de 250 USDT al mes durante 12 meses.", styles),
        paragraph(
            "Al aumentar el capital propio, el panel actualiza el rango que corresponda. Ademas del beneficio temporal indicado, los niveles pueden dar acceso a promociones, descuentos, ofertas especiales, campanas anticipadas o condiciones preferentes, siempre segun disponibilidad y condiciones de cada campana.", styles["Body"]
        ),
        paragraph("Programa Comunidad: no exige inversion propia, requiere red activa", styles["Subheading"]),
        paragraph(
            "Este programa esta pensado para quien desarrolla una comunidad. No pide que el titular tenga una inversion propia para alcanzar el rango. Lo que cuenta son los referidos directos activos: para que una persona de la red cuente, debe haber realizado y mantener al menos 100 USDT de inversion activa. Los referidos que no alcanzan ese minimo no se incluyen en el contador del rango.", styles["Body"]
        ),
        bullet("Community: de 5 a 24 referidos directos activos. Bonus de 25 USDT al mes durante 2 meses.", styles),
        bullet("Leader: de 25 a 49 referidos directos activos. Bonus de 50 USDT al mes durante 3 meses.", styles),
        bullet("Senior Leader: de 50 a 99 referidos directos activos. Bonus de 100 USDT al mes durante 4 meses.", styles),
        bullet("Elite Leader: de 100 a 199 referidos directos activos. Bonus de 150 USDT al mes durante 6 meses.", styles),
        bullet("Executive Leader: de 200 a 499 referidos directos activos. Bonus de 250 USDT al mes durante 12 meses.", styles),
        bullet("Founding Leader: desde 500 referidos directos activos. Bonus de 400 USDT al mes durante 12 meses.", styles),
        info_box(
            "En resumen: Partner se obtiene con capital propio y puede disfrutarse sin referidos. Comunidad se obtiene con referidos directos activos y no exige capital propio del lider. Los dos programas pueden combinarse, pero los beneficios son temporales, dependen de mantener las condiciones de cada nivel y estan sujetos a las reglas y campañas vigentes.", styles,
        ),
        paragraph("Ofertas especiales", styles["Subheading"]),
        paragraph(
            "Las ofertas especiales son operaciones comerciales concretas, separadas de la distribucion diaria ordinaria. Se publican para oportunidades de ciclo rapido o con una necesidad de capital definida y pueden estar disponibles solo para determinados rangos. Cada oferta indica su presupuesto objetivo, cupos, condiciones, plazo estimado, moneda, forma de participacion y reglas de distribucion antes de que el usuario solicite entrar.", styles["Body"]),
        paragraph("Como funciona una oferta especial", styles["Subheading"]),
        bullet("La administracion publica la oportunidad y comunica el capital total que se necesita reunir, los rangos habilitados, los cupos y las condiciones especificas.", styles),
        bullet("El usuario revisa la informacion, solicita el importe que desea aportar y adjunta el comprobante cuando corresponda. La participacion solo queda confirmada tras la validacion administrativa.", styles),
        bullet("Cuando se completa el cupo, la operacion comercial se ejecuta y el panel muestra sus novedades o el resultado que se comunique para ese tramo.", styles),
        bullet("Al cerrarse la operacion, la administracion registra la liquidacion segun sus condiciones publicadas. El porcentaje o importe que corresponda a cada participante depende de su rango y del acuerdo concreto de esa oferta.", styles),
        paragraph("Ejemplo informativo: contenedor de cemento", styles["Subheading"]),
        paragraph(
            "Un ejemplo mostrado en la web es una operacion de compra y venta de un contenedor de cemento. El presupuesto total requerido para reunir el tramo es de 10.000 USDT. Si la venta y ejecucion de la operacion generan una liquidez total de 13.000 USDT, el margen neto de la operacion seria de 3.000 USDT. Ese margen se distribuye entre los participantes del tramo conforme al rango y a las condiciones que se hayan publicado para la oferta antes de su validacion.", styles["Body"]),
        info_box(
            "Este ejemplo explica la mecanica de una oferta: se publica un cupo, se reúne el capital, se ejecuta una operacion comercial y se liquida el resultado segun las reglas de ese tramo. Los importes de 10.000, 13.000 y 3.000 USDT son ilustrativos del ejemplo de cemento y no constituyen una promesa de resultado para futuras ofertas.", styles,
        ),
        paragraph(
            "Cada oferta debe evaluarse de manera independiente. La disponibilidad de una oferta, el rango requerido, el cupo, el plazo y su resultado pueden variar; por ello no constituye una recomendacion personalizada ni una garantia de resultado.", styles["Body"]),
        PageBreak(),
    ]

    story += [
        paragraph("6. Panel del inversor y retiros", styles["Heading"]),
        paragraph("El panel centraliza la informacion operativa de cada usuario. Entre otras funciones, permite consultar:", styles["Body"]),
        bullet("Aportaciones y solicitudes con su importe, moneda, estado y fecha.", styles),
        bullet("Relojes de bloqueo individual de las aportaciones aun retenidas.", styles),
        bullet("Capital liberado, ganancias registradas y retiros, separados por moneda para no mezclar valores de MLC, CUP, EUR y USDT.", styles),
        bullet("Avisos de operaciones, documentacion, ofertas que correspondan y comunicacion de soporte.", styles),
        paragraph("Comunidad interna de usuarios", styles["Subheading"]),
        paragraph(
            "Dentro de la web existe una Comunidad, un chat interno donde los usuarios que han iniciado sesion pueden interactuar entre si. Desde este espacio pueden leer los mensajes publicados por otros miembros, compartir consultas o experiencias y enviar sus propios mensajes sin salir de la plataforma.", styles["Body"]
        ),
        paragraph(
            "Los mensajes se actualizan periodicamente para mantener la conversacion al dia. Las publicaciones del administrador aparecen identificadas como tales y, para proteger la privacidad, los nombres de los demas usuarios se muestran de forma parcial en el chat. La Comunidad sirve para la comunicacion general entre usuarios; las consultas personales sobre cuentas, retiros o datos sensibles deben gestionarse por los canales de soporte.", styles["Body"]
        ),
        paragraph("Fondo Solidario Cuba", styles["Subheading"]),
        paragraph(
            "La plataforma incorpora un Fondo Solidario separado del capital de inversion. Su finalidad es reunir recursos para ayudas verificadas a familias vulnerables en Cuba y en otros lugares del mundo donde la comunidad identifique necesidades reales. El fondo no utiliza las aportaciones, ganancias ni saldos disponibles de los usuarios: se registra por movimientos propios, visibles en su apartado de transparencia.", styles["Body"]
        ),
        paragraph(
            "Cada retiro tiene un cargo total del 5% por procesamiento. De ese cargo, el 2% se destina de forma fija al Fondo Solidario y el 3% restante cubre costes operativos, comisiones bancarias y, cuando corresponda, comisiones de red. Ademas, la empresa realiza un aporte obligatorio al fondo. Los recursos procedentes del 2% de los fees y los aportes de la empresa se registran por separado, con su importe y referencia, para que la comunidad pueda conocer cuanto corresponde a cada origen.", styles["Body"]
        ),
        paragraph("Como se propone, verifica y entrega una ayuda", styles["Subheading"]),
        bullet("La comunidad puede proponer casos mediante el chat interno, y tambien se pueden recibir propuestas por los canales de soporte.", styles),
        bullet("La administracion revisa la informacion del caso antes de seleccionarlo. Solo los casos verificados pueden hacerse visibles en el apartado publico del fondo.", styles),
        bullet("Una vez seleccionado un caso, representantes o equipos de la comunidad pueden realizar la entrega. La administracion registra el importe utilizado, que se entrego, quien estuvo a cargo y el resumen de la ayuda.", styles),
        bullet("Cuando exista autorizacion, se puede adjuntar evidencia de la entrega. La plataforma conserva el registro para comprobar que los recursos se destinaron a la ayuda anunciada, sin publicar datos sensibles de las familias.", styles),
        info_box(
            "Transparencia del fondo: el panel muestra por separado lo acumulado desde el 2% de los fees y el aporte obligatorio de la empresa, ademas del total entregado, el saldo disponible y las ayudas verificadas. Asi, la comunidad puede seguir el destino de los recursos sin mezclar este fondo con inversiones o retiros personales.", styles, colors.HexColor("#EAF7FB"),
        ),
        paragraph("Proceso de retiro", styles["Subheading"]),
        paragraph(
            "Cuando exista saldo disponible conforme a las reglas aplicables, el usuario puede solicitar un retiro desde su panel. Elige la moneda correspondiente a su participacion y facilita los datos requeridos. La solicitud pasa por revision administrativa y cambia de estado a medida que se procesa.", styles["Body"]
        ),
        paragraph(
            "Los retiros son internos y manuales: una solicitud no equivale a una transferencia instantanea. Antes de solicitarla, el usuario debe revisar posibles costes, comisiones, requisitos de identificacion, datos de destino y restricciones aplicables al metodo de pago o a la red seleccionada.", styles["Body"]
        ),
        paragraph("Cargo de procesamiento del retiro", styles["Subheading"]),
        paragraph(
            "A cada retiro se le aplica una deduccion del 5% sobre el importe solicitado. Este cargo se descuenta antes del envio y se destina a cubrir los costes de procesamiento, las comisiones bancarias y, cuando corresponda, las comisiones de red o blockchain (gas fee) de la administracion.", styles["Body"]
        ),
        paragraph(
            "Ejemplo: si el usuario solicita retirar 100 USDT, el cargo de procesamiento es de 5 USDT y el importe neto a enviar es de 95 USDT. El panel y la solicitud deben revisarse antes de confirmar el retiro.", styles["Body"]
        ),
        paragraph("Plazos orientativos de procesamiento", styles["Subheading"]),
        bullet("Retiros en MLC y CUP: se procesan manualmente con un plazo maximo estimado de hasta 24 horas. Este margen considera la situacion operativa y de conectividad del pais, asi como la revision de cada solicitud.", styles),
        bullet("Retiros en USDT: se procesan manualmente con un plazo maximo estimado de hasta 3 horas, una vez verificados los datos de la red y de la billetera de destino.", styles),
        paragraph(
            "Los plazos se cuentan desde que la solicitud contiene la informacion completa y supera la revision administrativa. Una incidencia tecnica, datos incorrectos, controles de seguridad o limitaciones externas pueden requerir una comunicacion adicional antes de completar el retiro.", styles["Body"]
        ),
        info_box(
            "Regla de moneda: los saldos y retiros se gestionan por moneda. Una participacion en USDT no debe presentarse ni retirarse como EUR, y una participacion en MLC o CUP conserva igualmente su moneda de origen.", styles,
        ),
        PageBreak(),
    ]

    story += [paragraph("7. Proximo paso", styles["Heading"])]
    story += [
        paragraph("Si deseas conocer una operacion o iniciar una solicitud, revisa primero el panel, las condiciones disponibles y la documentacion relacionada. Para consultas generales, soporte o aclaraciones sobre el uso de la plataforma:", styles["Body"]),
        info_box("Capital Trade Iberia<br/>Web: capitaltradeiberia.com<br/>Email: contacto@capitaltradeiberia.com<br/>Soporte: WhatsApp +34 677 412 858<br/>Horario de soporte: todos los dias, de 08:00 a 00:00", styles, colors.HexColor("#EAF7FB")),
        Spacer(1, 18),
        paragraph("Gracias por dedicar tiempo a comprender el modelo. Una participacion responsable comienza con informacion clara, verificacion de condiciones y una decision personal informada.", styles["Body"]),
    ]

    document.build(story, onFirstPage=lambda canvas, doc: None, onLaterPages=page_header_footer)
    print(f"PDF creado: {OUTPUT_PATH}")


if __name__ == "__main__":
    make_document()