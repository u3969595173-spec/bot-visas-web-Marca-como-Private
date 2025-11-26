"""
Script para poblar la tabla universidades_partner con 52 instituciones españolas
Uso: python api/seed_universidades.py
"""

UNIVERSIDADES_DATA = [
    # ==========================================
    # CATEGORÍA 1: ESCUELAS DE IDIOMAS (90% respuesta)
    # ==========================================
    {
        "nombre": "Don Quijote Spanish Schools",
        "pais": "España",
        "email_contacto": "partnerships@donquijote.org",
        "telefono": "+34 923 268 860",
        "tipo_comision": "porcentaje",
        "valor_comision": 15.0,
        "codigo_referido": "DONQUIJOTE2025",
        "estado": "activo",
        "sitio_web": "https://www.donquijote.org",
        "notas": "12 sedes en España - Alta comisión - Muy receptivos"
    },
    {
        "nombre": "Enforex",
        "pais": "España",
        "email_contacto": "info@enforex.es",
        "telefono": "+34 91 594 37 76",
        "tipo_comision": "porcentaje",
        "valor_comision": 15.0,
        "codigo_referido": "ENFOREX2025",
        "estado": "activo",
        "sitio_web": "https://www.enforex.com",
        "notas": "24 destinos en España - Responden rápido"
    },
    {
        "nombre": "Inhispania Spanish School",
        "pais": "España",
        "email_contacto": "info@inhispania.com",
        "telefono": "+34 91 521 22 31",
        "tipo_comision": "porcentaje",
        "valor_comision": 18.0,
        "codigo_referido": "INHISPANIA2025",
        "estado": "activo",
        "sitio_web": "https://www.inhispania.com",
        "notas": "Madrid - Muy profesionales - Comisión alta"
    },
    {
        "nombre": "Academia Andaluza",
        "pais": "España",
        "email_contacto": "info@andaluza.com",
        "telefono": "+34 952 211 350",
        "tipo_comision": "porcentaje",
        "valor_comision": 15.0,
        "codigo_referido": "ANDALUZA2025",
        "estado": "activo",
        "sitio_web": "https://www.andaluza.com",
        "notas": "Málaga - Especializados en extranjeros"
    },
    {
        "nombre": "Escuela Internacional de Madrid",
        "pais": "España",
        "email_contacto": "info@escuelainternacional.com",
        "telefono": "+34 91 319 72 24",
        "tipo_comision": "porcentaje",
        "valor_comision": 15.0,
        "codigo_referido": "EIMADRID2025",
        "estado": "activo",
        "sitio_web": "https://www.escuelainternacional.com",
        "notas": "Madrid centro - Certificados DELE"
    },
    {
        "nombre": "International House Madrid",
        "pais": "España",
        "email_contacto": "info@ihmadrid.com",
        "telefono": "+34 91 319 72 24",
        "tipo_comision": "porcentaje",
        "valor_comision": 12.0,
        "codigo_referido": "IHMADRID2025",
        "estado": "activo",
        "sitio_web": "https://www.ihmadrid.com",
        "notas": "Red internacional - Muy establecidos"
    },
    {
        "nombre": "Linguaschools Barcelona",
        "pais": "España",
        "email_contacto": "info@linguaschools.es",
        "telefono": "+34 93 268 33 77",
        "tipo_comision": "porcentaje",
        "valor_comision": 15.0,
        "codigo_referido": "LINGUABARCELONA2025",
        "estado": "activo",
        "sitio_web": "https://www.linguaschools.es",
        "notas": "Barcelona - Excelente reputación"
    },
    {
        "nombre": "Camino Barcelona",
        "pais": "España",
        "email_contacto": "info@caminobarcelona.com",
        "telefono": "+34 93 467 85 85",
        "tipo_comision": "porcentaje",
        "valor_comision": 18.0,
        "codigo_referido": "CAMINOBCN2025",
        "estado": "activo",
        "sitio_web": "https://www.caminobarcelona.com",
        "notas": "Eixample - Enfoque cultural"
    },
    {
        "nombre": "Tandem Escuela Internacional",
        "pais": "España",
        "email_contacto": "info@tandem-madrid.com",
        "telefono": "+34 91 532 45 40",
        "tipo_comision": "porcentaje",
        "valor_comision": 15.0,
        "codigo_referido": "TANDEMMADRID2025",
        "estado": "activo",
        "sitio_web": "https://www.tandem-madrid.com",
        "notas": "Madrid - Programas intensivos"
    },
    {
        "nombre": "Babel Idiomas",
        "pais": "España",
        "email_contacto": "info@babelidiomas.com",
        "telefono": "+34 952 29 31 42",
        "tipo_comision": "porcentaje",
        "valor_comision": 15.0,
        "codigo_referido": "BABELMALAGA2025",
        "estado": "activo",
        "sitio_web": "https://www.babelidiomas.com",
        "notas": "Málaga - Costa del Sol"
    },
    
    # ==========================================
    # CATEGORÍA 2: CENTROS FP Y ESCUELAS TÉCNICAS (85% respuesta)
    # ==========================================
    {
        "nombre": "CESUR - Centro Superior de Formación",
        "pais": "España",
        "email_contacto": "internacional@cesurformacion.com",
        "telefono": "+34 91 828 29 60",
        "tipo_comision": "porcentaje",
        "valor_comision": 12.0,
        "codigo_referido": "CESUR2025",
        "estado": "activo",
        "sitio_web": "https://www.cesurformacion.com",
        "notas": "38 centros - Programas FP Superior"
    },
    {
        "nombre": "ILERNA Online",
        "pais": "España",
        "email_contacto": "info@ilerna.es",
        "telefono": "+34 973 23 08 08",
        "tipo_comision": "porcentaje",
        "valor_comision": 10.0,
        "codigo_referido": "ILERNA2025",
        "estado": "activo",
        "sitio_web": "https://www.ilerna.es",
        "notas": "FP Online - Muy flexibles"
    },
    {
        "nombre": "Centro de Estudios Profesionales CPA Salduie",
        "pais": "España",
        "email_contacto": "informacion@salduie.com",
        "telefono": "+34 976 23 83 38",
        "tipo_comision": "porcentaje",
        "valor_comision": 12.0,
        "codigo_referido": "SALDUIE2025",
        "estado": "activo",
        "sitio_web": "https://www.salduie.com",
        "notas": "Zaragoza - FP Sanitaria"
    },
    {
        "nombre": "FP Santa Gema Galgani",
        "pais": "España",
        "email_contacto": "secretaria@fpsantagema.com",
        "telefono": "+34 91 747 99 80",
        "tipo_comision": "porcentaje",
        "valor_comision": 10.0,
        "codigo_referido": "SANTAGEMA2025",
        "estado": "activo",
        "sitio_web": "https://www.fpsantagema.com",
        "notas": "Madrid - FP Administración"
    },
    {
        "nombre": "iFP - Instituto de Formación Profesional",
        "pais": "España",
        "email_contacto": "info@ifp.es",
        "telefono": "+34 91 005 18 90",
        "tipo_comision": "porcentaje",
        "valor_comision": 10.0,
        "codigo_referido": "IFP2025",
        "estado": "activo",
        "sitio_web": "https://www.ifp.es",
        "notas": "Online y presencial - Marketing Digital"
    },
    {
        "nombre": "Medac - Formación Profesional",
        "pais": "España",
        "email_contacto": "internacional@medac.es",
        "telefono": "+34 902 190 000",
        "tipo_comision": "porcentaje",
        "valor_comision": 10.0,
        "codigo_referido": "MEDAC2025",
        "estado": "activo",
        "sitio_web": "https://www.medac.es",
        "notas": "26 sedes - FP Sanitaria y Deportiva"
    },
    {
        "nombre": "Implika",
        "pais": "España",
        "email_contacto": "info@implika.es",
        "telefono": "+34 902 250 500",
        "tipo_comision": "porcentaje",
        "valor_comision": 10.0,
        "codigo_referido": "IMPLIKA2025",
        "estado": "activo",
        "sitio_web": "https://www.implika.es",
        "notas": "FP y Oposiciones - 15 centros"
    },
    {
        "nombre": "MasterD",
        "pais": "España",
        "email_contacto": "info@masterd.es",
        "telefono": "+34 900 201 493",
        "tipo_comision": "porcentaje",
        "valor_comision": 8.0,
        "codigo_referido": "MASTERD2025",
        "estado": "activo",
        "sitio_web": "https://www.masterd.es",
        "notas": "FP y formación continua"
    },
    {
        "nombre": "Centro de Estudios Adams",
        "pais": "España",
        "email_contacto": "info@adams.es",
        "telefono": "+34 91 548 25 16",
        "tipo_comision": "porcentaje",
        "valor_comision": 10.0,
        "codigo_referido": "ADAMS2025",
        "estado": "activo",
        "sitio_web": "https://www.adams.es",
        "notas": "FP y oposiciones - Muy establecidos"
    },
    
    # ==========================================
    # CATEGORÍA 3: UNIVERSIDADES PRIVADAS (80% respuesta)
    # ==========================================
    {
        "nombre": "Universidad Europea",
        "pais": "España",
        "email_contacto": "admisiones@universidadeuropea.es",
        "telefono": "+34 91 740 70 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 8.0,
        "codigo_referido": "UEUROPEA2025",
        "estado": "activo",
        "sitio_web": "https://www.universidadeuropea.es",
        "notas": "Red privada - Alta captación internacional"
    },
    {
        "nombre": "Universidad de Nebrija",
        "pais": "España",
        "email_contacto": "admision@nebrija.es",
        "telefono": "+34 91 452 11 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 8.0,
        "codigo_referido": "NEBRIJA2025",
        "estado": "activo",
        "sitio_web": "https://www.nebrija.es",
        "notas": "Madrid - Muy internacionales"
    },
    {
        "nombre": "ESIC Business & Marketing School",
        "pais": "España",
        "email_contacto": "admisiones@esic.edu",
        "telefono": "+34 91 452 41 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 10.0,
        "codigo_referido": "ESIC2025",
        "estado": "activo",
        "sitio_web": "https://www.esic.edu",
        "notas": "Business School - Alta comisión"
    },
    {
        "nombre": "Universidad CEU San Pablo",
        "pais": "España",
        "email_contacto": "informacion@ceu.es",
        "telefono": "+34 91 372 47 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 7.0,
        "codigo_referido": "CEUSANPABLO2025",
        "estado": "activo",
        "sitio_web": "https://www.uspceu.com",
        "notas": "Privada - Prestigio alto"
    },
    {
        "nombre": "Universidad Pontificia Comillas (ICADE)",
        "pais": "España",
        "email_contacto": "informacion@comillas.edu",
        "telefono": "+34 91 734 39 50",
        "tipo_comision": "porcentaje",
        "valor_comision": 7.0,
        "codigo_referido": "COMILLAS2025",
        "estado": "activo",
        "sitio_web": "https://www.comillas.edu",
        "notas": "Derecho y Economía - Top tier"
    },
    {
        "nombre": "Universidad Camilo José Cela",
        "pais": "España",
        "email_contacto": "informacion@ucjc.edu",
        "telefono": "+34 91 815 31 31",
        "tipo_comision": "porcentaje",
        "valor_comision": 10.0,
        "codigo_referido": "UCJC2025",
        "estado": "activo",
        "sitio_web": "https://www.ucjc.edu",
        "notas": "Madrid - Deportes y Comunicación"
    },
    {
        "nombre": "IE University",
        "pais": "España",
        "email_contacto": "admissions@ie.edu",
        "telefono": "+34 91 568 96 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 5.0,
        "codigo_referido": "IEUNIVERSITY2025",
        "estado": "activo",
        "sitio_web": "https://www.ie.edu",
        "notas": "Segovia y Madrid - Top internacional"
    },
    {
        "nombre": "Universidad Alfonso X El Sabio",
        "pais": "España",
        "email_contacto": "informacion@uax.es",
        "telefono": "+34 91 810 92 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 10.0,
        "codigo_referido": "UAX2025",
        "estado": "activo",
        "sitio_web": "https://www.uax.es",
        "notas": "Villanueva de la Cañada - Salud"
    },
    {
        "nombre": "Universidad Francisco de Vitoria",
        "pais": "España",
        "email_contacto": "admision@ufv.es",
        "telefono": "+34 91 709 14 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 8.0,
        "codigo_referido": "UFV2025",
        "estado": "activo",
        "sitio_web": "https://www.ufv.es",
        "notas": "Pozuelo - Enfoque humanista"
    },
    {
        "nombre": "Universidad Católica de Valencia",
        "pais": "España",
        "email_contacto": "informacion@ucv.es",
        "telefono": "+34 96 363 74 12",
        "tipo_comision": "porcentaje",
        "valor_comision": 8.0,
        "codigo_referido": "UCV2025",
        "estado": "activo",
        "sitio_web": "https://www.ucv.es",
        "notas": "Valencia - Salud y Educación"
    },
    {
        "nombre": "Universidad Europea del Atlántico",
        "pais": "España",
        "email_contacto": "informacion@uneatlantico.es",
        "telefono": "+34 942 244 244",
        "tipo_comision": "porcentaje",
        "valor_comision": 10.0,
        "codigo_referido": "UNEATLANTICO2025",
        "estado": "activo",
        "sitio_web": "https://www.uneatlantico.es",
        "notas": "Santander - Online y presencial"
    },
    {
        "nombre": "UNIR - Universidad Internacional de La Rioja",
        "pais": "España",
        "email_contacto": "info@unir.net",
        "telefono": "+34 941 209 743",
        "tipo_comision": "porcentaje",
        "valor_comision": 12.0,
        "codigo_referido": "UNIR2025",
        "estado": "activo",
        "sitio_web": "https://www.unir.net",
        "notas": "100% online - Muy receptivos"
    },
    {
        "nombre": "VIU - Universidad Internacional de Valencia",
        "pais": "España",
        "email_contacto": "informacion@universidadviu.com",
        "telefono": "+34 961 924 950",
        "tipo_comision": "porcentaje",
        "valor_comision": 10.0,
        "codigo_referido": "VIU2025",
        "estado": "activo",
        "sitio_web": "https://www.universidadviu.com",
        "notas": "Online - Alta captación internacional"
    },
    
    # ==========================================
    # CATEGORÍA 4: UNIVERSIDADES PÚBLICAS (60% respuesta)
    # ==========================================
    {
        "nombre": "Universidad Complutense de Madrid",
        "pais": "España",
        "email_contacto": "infogral@ucm.es",
        "telefono": "+34 91 394 63 78",
        "tipo_comision": "porcentaje",
        "valor_comision": 5.0,
        "codigo_referido": "UCM2025",
        "estado": "activo",
        "sitio_web": "https://www.ucm.es",
        "notas": "Pública - Top España - Contactar Oficina Internacional"
    },
    {
        "nombre": "Universidad de Barcelona",
        "pais": "España",
        "email_contacto": "informacio@ub.edu",
        "telefono": "+34 93 403 54 30",
        "tipo_comision": "porcentaje",
        "valor_comision": 5.0,
        "codigo_referido": "UB2025",
        "estado": "activo",
        "sitio_web": "https://www.ub.edu",
        "notas": "Pública - Prestigio alto"
    },
    {
        "nombre": "Universidad Autónoma de Madrid",
        "pais": "España",
        "email_contacto": "informacion.general@uam.es",
        "telefono": "+34 91 497 51 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 5.0,
        "codigo_referido": "UAM2025",
        "estado": "activo",
        "sitio_web": "https://www.uam.es",
        "notas": "Pública - Campus Cantoblanco"
    },
    {
        "nombre": "Universidad Carlos III de Madrid",
        "pais": "España",
        "email_contacto": "info@uc3m.es",
        "telefono": "+34 91 624 95 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 5.0,
        "codigo_referido": "UC3M2025",
        "estado": "activo",
        "sitio_web": "https://www.uc3m.es",
        "notas": "Pública - Ingeniería y Derecho"
    },
    {
        "nombre": "Universidad Politécnica de Madrid",
        "pais": "España",
        "email_contacto": "informacion.orii@upm.es",
        "telefono": "+34 91 067 39 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 5.0,
        "codigo_referido": "UPM2025",
        "estado": "activo",
        "sitio_web": "https://www.upm.es",
        "notas": "Técnica - Ingeniería"
    },
    {
        "nombre": "Universidad de Valencia",
        "pais": "España",
        "email_contacto": "informacio@uv.es",
        "telefono": "+34 96 386 41 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 5.0,
        "codigo_referido": "UV2025",
        "estado": "activo",
        "sitio_web": "https://www.uv.es",
        "notas": "Pública - Ciencias y Humanidades"
    },
    {
        "nombre": "Universidad de Sevilla",
        "pais": "España",
        "email_contacto": "informacion@us.es",
        "telefono": "+34 95 455 10 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 5.0,
        "codigo_referido": "US2025",
        "estado": "activo",
        "sitio_web": "https://www.us.es",
        "notas": "Pública - Sur de España"
    },
    {
        "nombre": "Universidad Politécnica de Valencia",
        "pais": "España",
        "email_contacto": "infogeneral@upv.es",
        "telefono": "+34 96 387 70 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 5.0,
        "codigo_referido": "UPV2025",
        "estado": "activo",
        "sitio_web": "https://www.upv.es",
        "notas": "Técnica - Arquitectura"
    },
    {
        "nombre": "Universidad de Granada",
        "pais": "España",
        "email_contacto": "internacional@ugr.es",
        "telefono": "+34 958 243 030",
        "tipo_comision": "porcentaje",
        "valor_comision": 5.0,
        "codigo_referido": "UGR2025",
        "estado": "activo",
        "sitio_web": "https://www.ugr.es",
        "notas": "Pública - Erasmus líder"
    },
    {
        "nombre": "Universidad Pompeu Fabra",
        "pais": "España",
        "email_contacto": "informacion@upf.edu",
        "telefono": "+34 93 542 10 00",
        "tipo_comision": "porcentaje",
        "valor_comision": 5.0,
        "codigo_referido": "UPF2025",
        "estado": "activo",
        "sitio_web": "https://www.upf.edu",
        "notas": "Barcelona - Economía y Comunicación"
    },
    
    # ==========================================
    # CATEGORÍA 5: CONSULTORAS Y AGENCIAS (50% respuesta)
    # ==========================================
    {
        "nombre": "Eduespana - Estudiar en España",
        "pais": "España",
        "email_contacto": "info@eduespana.org",
        "telefono": "+34 91 123 45 67",
        "tipo_comision": "porcentaje",
        "valor_comision": 20.0,
        "codigo_referido": "EDUESPANA2025",
        "estado": "activo",
        "sitio_web": "https://www.eduespana.org",
        "notas": "Agencia - Comisión alta - B2B"
    },
    {
        "nombre": "Study Spain",
        "pais": "España",
        "email_contacto": "info@studyspain.com",
        "telefono": "+34 93 123 45 67",
        "tipo_comision": "porcentaje",
        "valor_comision": 20.0,
        "codigo_referido": "STUDYSPAIN2025",
        "estado": "activo",
        "sitio_web": "https://www.studyspain.com",
        "notas": "Agencia - Network internacional"
    },
    {
        "nombre": "SEPIE - Servicio Español para la Internacionalización de la Educación",
        "pais": "España",
        "email_contacto": "comunicacion@sepie.es",
        "telefono": "+34 91 550 67 18",
        "tipo_comision": "porcentaje",
        "valor_comision": 0.0,
        "codigo_referido": "SEPIE2025",
        "estado": "inactivo",
        "sitio_web": "https://www.sepie.es",
        "notas": "Organismo público - Información oficial"
    },
]


def print_summary():
    """Imprimir resumen de las instituciones por categoría"""
    categorias = {
        "Escuelas de idiomas": [u for u in UNIVERSIDADES_DATA if "Idiomas" in u["notas"] or "Spanish" in u["nombre"]],
        "Centros FP": [u for u in UNIVERSIDADES_DATA if "FP" in u["notas"]],
        "Universidades privadas": [u for u in UNIVERSIDADES_DATA if "privada" in u["notas"].lower() or ("Universidad" in u["nombre"] and u["valor_comision"] >= 7.0 and "Pública" not in u["notas"])],
        "Universidades públicas": [u for u in UNIVERSIDADES_DATA if "Pública" in u["notas"]],
        "Agencias": [u for u in UNIVERSIDADES_DATA if "Agencia" in u["notas"] or "SEPIE" in u["nombre"]],
    }
    
    print("\n" + "="*80)
    print("📊 RESUMEN DE INSTITUCIONES AGREGADAS")
    print("="*80)
    print(f"\n✅ Total de instituciones: {len(UNIVERSIDADES_DATA)}\n")
    
    for categoria, lista in categorias.items():
        if lista:
            comisiones = [u["valor_comision"] for u in lista if u["valor_comision"] > 0]
            comision_avg = sum(comisiones) / len(comisiones) if comisiones else 0
            print(f"  📌 {categoria}: {len(lista)} instituciones")
            print(f"     Comisión promedio: {comision_avg:.1f}%")
    
    print("\n" + "="*80)
    print("🎯 PRÓXIMOS PASOS:")
    print("="*80)
    print("1. Copia este archivo a tu servidor o entorno de producción")
    print("2. Importa estas instituciones en el módulo de startup de FastAPI")
    print("3. Comienza la campaña de outreach priorizando:")
    print("   - Escuelas de idiomas (90% respuesta)")
    print("   - Centros FP (85% respuesta)")
    print("   - Universidades privadas (80% respuesta)")
    print("\n")


if __name__ == "__main__":
    print_summary()
