"""
Banco completo de 100+ preguntas reales de entrevistas consulares
Cada pregunta incluye tips y respuesta modelo
"""

BANCO_PREGUNTAS_COMPLETO = [
    # === MOTIVACIÓN Y PLANES (20 preguntas) ===
    {
        "pregunta": "¿Por qué quieres estudiar en España y no en tu país?",
        "categoria": "motivacion",
        "tips": "Habla sobre la calidad educativa, programas específicos no disponibles en tu país, reconocimiento internacional del título.",
        "respuesta_modelo": "Quiero estudiar en España porque ofrece programas de alta calidad reconocidos internacionalmente. Específicamente, el programa de Medicina en la Universidad Complutense no está disponible con este nivel de especialización en mi país."
    },
    {
        "pregunta": "¿Planeas regresar a tu país después de terminar los estudios?",
        "categoria": "intencion_retorno",
        "tips": "SIEMPRE di que sí planeas regresar. Es una pregunta clave para demostrar no-inmigración.",
        "respuesta_modelo": "Sí, definitivamente planeo regresar. Mi familia está allá y quiero aplicar los conocimientos adquiridos para contribuir al desarrollo del sector salud en mi país, donde hay gran necesidad de profesionales especializados."
    },
    {
        "pregunta": "¿Qué harás cuando termines tus estudios en España?",
        "categoria": "planes_futuros",
        "tips": "Menciona planes concretos de regresar: trabajo específico, familia, proyectos.",
        "respuesta_modelo": "Regresaré a trabajar en el Hospital Central de mi ciudad, donde ya tengo contactos profesionales. También planeo abrir una consulta privada y colaborar con la universidad local como docente."
    },
    {
        "pregunta": "¿Por qué elegiste esta universidad específicamente?",
        "categoria": "universidad",
        "tips": "Investiga ranking, profesores destacados, instalaciones, empleabilidad de egresados.",
        "respuesta_modelo": "La Universidad Complutense está rankeada #3 en España en Medicina. El programa incluye prácticas en hospitales de referencia y tiene convenios internacionales. Me interesa especialmente el enfoque en investigación clínica."
    },
    {
        "pregunta": "¿Qué sabes sobre el programa al que aplicas?",
        "categoria": "conocimiento_programa",
        "tips": "Menciona duración, créditos ECTS, asignaturas clave, prácticas.",
        "respuesta_modelo": "Es un Máster de 60 ECTS durante un año académico. Incluye asignaturas como Diagnóstico Avanzado, Cirugía Especializada, y 300 horas de prácticas en hospitales. Termina con un TFM de investigación."
    },
    {
        "pregunta": "¿Por qué elegiste esta carrera?",
        "categoria": "vocacion",
        "tips": "Conecta con tu experiencia previa, tus metas profesionales, y por qué esta carrera específica.",
        "respuesta_modelo": "Elegí Medicina porque tengo experiencia como enfermero durante 5 años y quiero especializarme en cirugía. Mi objetivo es convertirme en cirujano cardiovascular y esta especialización me permitirá lograrlo."
    },
    {
        "pregunta": "¿Cuánto tiempo llevas preparando este viaje?",
        "categoria": "preparacion",
        "tips": "Demuestra que no es una decisión impulsiva. Menciona meses de investigación y preparación.",
        "respuesta_modelo": "Llevo 8 meses preparándome: investigué universidades, estudié español intensivamente, ahorré dinero, y completé todos los trámites de apostilla de documentos. Es un proyecto muy planificado."
    },
    {
        "pregunta": "¿Qué esperas lograr con estos estudios?",
        "categoria": "objetivos",
        "tips": "Sé específico: certificación profesional, título reconocido, habilidades concretas.",
        "respuesta_modelo": "Espero obtener un título reconocido internacionalmente que me permita ejercer en mi país con mayor especialización. También adquirir experiencia práctica en hospitales europeos de referencia y crear una red profesional internacional."
    },
    {
        "pregunta": "¿Has aplicado a otras universidades?",
        "categoria": "opciones",
        "tips": "Está bien mencionar otras opciones pero explica por qué esta es tu primera elección.",
        "respuesta_modelo": "Sí, también he considerado la Universidad de Barcelona y la Autónoma de Madrid, pero la Complutense es mi primera opción por su prestigio en investigación médica y sus convenios con hospitales líderes."
    },
    {
        "pregunta": "¿Qué harás si no te aceptan en esta universidad?",
        "categoria": "plan_b",
        "tips": "Muestra que tienes opciones pero que esta es tu primera elección por razones específicas.",
        "respuesta_modelo": "Esta es mi primera opción por las razones que mencioné, pero también he aplicado a la Universidad de Valencia que ofrece un programa similar de calidad. Lo importante es estudiar en España por su excelencia educativa."
    },
    {
        "pregunta": "¿Conoces a alguien que haya estudiado en España?",
        "categoria": "referencias",
        "tips": "Si conoces a alguien, menciona su experiencia positiva pero resalta tu independencia.",
        "respuesta_modelo": "Sí, mi primo estudió Ingeniería en Madrid hace 3 años. Su experiencia fue excelente y me orientó sobre el sistema educativo español, pero mi decisión es completamente independiente basada en mi investigación."
    },
    {
        "pregunta": "¿Por qué España y no otro país europeo?",
        "categoria": "eleccion_pais",
        "tips": "Menciona idioma, cultura, calidad educativa, costos razonables.",
        "respuesta_modelo": "España ofrece educación de calidad a costos más accesibles que otros países europeos. Además, hablo español lo cual facilita mi adaptación, y el sistema educativo español tiene convenios de reconocimiento con mi país."
    },
    {
        "pregunta": "¿Qué diferencia hay entre estudiar aquí y en tu país?",
        "categoria": "comparacion",
        "tips": "Menciona ventajas específicas sin criticar tu país: especialización, tecnología, reconocimiento.",
        "respuesta_modelo": "En España tendré acceso a tecnología médica de última generación, prácticas en hospitales de referencia europea, y un título con reconocimiento internacional que no está disponible en mi país para esta especialidad."
    },
    {
        "pregunta": "¿Cuándo planeas comenzar tus estudios?",
        "categoria": "fechas",
        "tips": "Sé específico con fechas de inicio, duración del programa.",
        "respuesta_modelo": "El programa comienza en septiembre 2025 y dura un año académico completo. Planeo llegar a España en agosto para adaptarme, buscar alojamiento y familiarizarme con la ciudad antes de iniciar clases."
    },
    {
        "pregunta": "¿Qué te motiva a dejar tu país temporalmente?",
        "categoria": "motivacion_personal",
        "tips": "Enfatiza crecimiento profesional, no problemas económicos o políticos de tu país.",
        "respuesta_modelo": "Me motiva crecer profesionalmente y adquirir experiencia internacional que beneficiará mi desarrollo. No es que quiera dejar mi país, sino enriquecerme con conocimientos que luego aportaré allá."
    },
    {
        "pregunta": "¿Tienes alguna beca o ayuda económica?",
        "categoria": "becas",
        "tips": "Si aplicas a becas, menciona cuáles y estado. Si no, está bien decir que cuentas con recursos propios.",
        "respuesta_modelo": "He aplicado a la beca MAEC-AECID y estoy esperando respuesta. Sin embargo, cuento con recursos propios suficientes para cubrir todos los gastos en caso de no obtenerla."
    },
    {
        "pregunta": "¿Qué sabes sobre el sistema educativo español?",
        "categoria": "conocimiento_sistema",
        "tips": "Menciona ECTS, estructura de grado/máster, evaluación continua.",
        "respuesta_modelo": "Sé que España usa el sistema de créditos ECTS del Espacio Europeo. Los programas tienen evaluación continua, no solo exámenes finales. También hay obligatoriedad de asistencia y trabajos prácticos constantes."
    },
    {
        "pregunta": "¿Cómo te enteraste de esta universidad?",
        "categoria": "investigacion",
        "tips": "Muestra que investigaste activamente: rankings, web oficial, exalumnos, ferias educativas.",
        "respuesta_modelo": "Investigué en rankings internacionales, visité la web oficial de la universidad, hablé con exalumnos en LinkedIn, y asistí a una feria educativa donde representantes de la universidad presentaron el programa."
    },
    {
        "pregunta": "¿Estás trabajando actualmente?",
        "categoria": "situacion_laboral",
        "tips": "Si trabajas, menciona que pedirás excedencia o licencia. Demuestra vínculos laborales que te harán regresar.",
        "respuesta_modelo": "Sí, trabajo como enfermero en el Hospital General desde hace 5 años. He solicitado una excedencia por estudios que me garantiza reincorporación a mi puesto al regresar con la especialización."
    },
    {
        "pregunta": "¿Qué esperas de la experiencia de estudiar en el extranjero?",
        "categoria": "expectativas",
        "tips": "Menciona crecimiento académico, personal, cultural, profesional.",
        "respuesta_modelo": "Espero crecimiento académico con profesores expertos, experiencia práctica en hospitales de primer nivel, intercambio cultural con compañeros internacionales, y desarrollo de independencia personal que me hará mejor profesional."
    },

    # === FINANCIACIÓN (20 preguntas) ===
    {
        "pregunta": "¿Cómo vas a financiar tus estudios y manutención?",
        "categoria": "fondos",
        "tips": "Menciona tus ahorros, apoyo familiar, becas. Sé específico con cantidades y muestra evidencia.",
        "respuesta_modelo": "Cuento con €15,000 en ahorros personales y el apoyo económico de mi familia que puede demostrar ingresos mensuales de €3,000. También he aplicado a la beca MAEC que cubre €700 mensuales."
    },
    {
        "pregunta": "¿Cuánto dinero traerás a España inicialmente?",
        "categoria": "fondos_iniciales",
        "tips": "Menciona cantidad específica que cubra al menos 3-6 meses, muestra extractos bancarios.",
        "respuesta_modelo": "Traeré €10,000 inicialmente, que cubren 6 meses de matrícula y manutención. Tengo extractos bancarios de los últimos 6 meses que demuestran estos fondos en mi cuenta."
    },
    {
        "pregunta": "¿Quién te patrocina económicamente?",
        "categoria": "patrocinio",
        "tips": "Explica relación, muestra carta de patrocinio y evidencia de ingresos del patrocinador.",
        "respuesta_modelo": "Mis padres son mis patrocinadores. Mi padre es ingeniero con ingresos mensuales de €2,500 y mi madre es contadora con €1,800 mensuales. Tengo carta de patrocinio notariada y sus certificados laborales."
    },
    {
        "pregunta": "¿Cuánto cuesta tu matrícula?",
        "categoria": "costos_matricula",
        "tips": "Sé exacto con el monto, demuestra que conoces todos los costos.",
        "respuesta_modelo": "La matrícula del máster es €4,200 por el año completo. Además, debo pagar €150 de tasas administrativas y €80 de seguro escolar obligatorio, totalizando €4,430."
    },
    {
        "pregunta": "¿Cuánto calculas que gastarás mensualmente en España?",
        "categoria": "presupuesto_mensual",
        "tips": "Demuestra que has investigado: alquiler, comida, transporte, seguro médico.",
        "respuesta_modelo": "He calculado €1,200 mensuales: alquiler €500, comida €300, transporte €50, seguro médico €50, libros y materiales €100, y €200 para imprevistos. Es un presupuesto realista según mi investigación."
    },
    {
        "pregunta": "¿Tienes ahorros propios o dependes completamente de tu familia?",
        "categoria": "independencia_financiera",
        "tips": "Idealmente muestra que tienes ahorros propios, aunque sea con apoyo familiar adicional.",
        "respuesta_modelo": "Tengo €8,000 en ahorros propios de mi trabajo durante 3 años. Adicionalmente, mi familia me apoyará con €500 mensuales para gastos complementarios. No dependo completamente de ellos."
    },
    {
        "pregunta": "¿Cómo demostraste que tienes fondos suficientes?",
        "categoria": "evidencia_fondos",
        "tips": "Menciona documentos específicos: extractos bancarios, cartas de patrocinio, certificados laborales.",
        "respuesta_modelo": "Presenté extractos bancarios de los últimos 6 meses mostrando €15,000, carta de patrocinio notariada de mis padres, sus certificados laborales, y últimas 3 declaraciones de impuestos que demuestran ingresos estables."
    },
    {
        "pregunta": "¿Planeas trabajar mientras estudias?",
        "categoria": "trabajo_estudiante",
        "tips": "Con visa de estudiante puedes trabajar 20h/semana. Menciona que es opcional, no necesario.",
        "respuesta_modelo": "No dependo de trabajar porque tengo fondos suficientes, pero sé que legalmente puedo trabajar hasta 20 horas semanales. Si surge una oportunidad relacionada con mi campo de estudio, la consideraré para ganar experiencia."
    },
    {
        "pregunta": "¿Tus padres pueden seguir apoyándote económicamente durante todo el programa?",
        "categoria": "sostenibilidad_apoyo",
        "tips": "Muestra que el apoyo es sostenible con ingresos estables demostrables.",
        "respuesta_modelo": "Sí, mis padres tienen empleos estables con antigüedad de más de 10 años. Sus ingresos combinados de €4,300 mensuales les permiten apoyarme sin problemas. Además, no tienen deudas significativas."
    },
    {
        "pregunta": "¿Qué harás si se te acaba el dinero durante tus estudios?",
        "categoria": "plan_emergencia",
        "tips": "Muestra que tienes plan B: apoyo familiar adicional, posibilidad de trabajar legalmente.",
        "respuesta_modelo": "Tengo un fondo de emergencia adicional de €3,000 que no he mencionado. También mis padres tienen capacidad de enviar dinero adicional si es necesario. Y legalmente puedo trabajar part-time si surge la necesidad."
    },
    {
        "pregunta": "¿Has comprado el seguro médico obligatorio?",
        "categoria": "seguro_medico",
        "tips": "Menciona que contratarás/has contratado seguro de estudiante internacional con cobertura completa.",
        "respuesta_modelo": "Sí, he contratado seguro médico con Asisa Estudiantes que cubre €50,000 con cobertura completa, sin copagos, incluye hospitalización, cirugías y repatriación. Cuesta €50 mensuales."
    },
    {
        "pregunta": "¿Tienes propiedades o bienes a tu nombre?",
        "categoria": "patrimonio",
        "tips": "Si tienes propiedades, vehículo, cuentas bancarias, menciónalos como vínculos con tu país.",
        "respuesta_modelo": "Sí, tengo un apartamento a mi nombre valorado en €40,000 que estoy alquilando durante mi ausencia. También un vehículo valorado en €8,000 y €15,000 en cuentas bancarias."
    },
    {
        "pregunta": "¿Cómo enviarán dinero tus padres desde tu país?",
        "categoria": "transferencias",
        "tips": "Menciona método específico: transferencia bancaria internacional, Western Union, TransferWise.",
        "respuesta_modelo": "Mis padres enviarán dinero mediante transferencias bancarias internacionales directas a mi cuenta en España. Ya hemos verificado que su banco ofrece este servicio con comisiones razonables de €15 por transferencia."
    },
    {
        "pregunta": "¿Cuánto cuesta el alojamiento donde vivirás?",
        "categoria": "alojamiento_costo",
        "tips": "Sé específico, muestra que has investigado o reservado.",
        "respuesta_modelo": "He encontrado habitación en piso compartido cerca de la universidad por €450 mensuales incluyendo servicios. También investigué residencias estudiantiles que cuestan €600-800 con comidas incluidas."
    },
    {
        "pregunta": "¿Tienes cuenta bancaria en España?",
        "categoria": "cuenta_bancaria",
        "tips": "Puedes abrirla al llegar. Menciona que investigaste requisitos.",
        "respuesta_modelo": "Todavía no porque requiero el NIE que obtendré al llegar. He investigado y planeo abrir cuenta en Santander o BBVA que ofrecen cuentas para estudiantes internacionales sin comisiones."
    },
    {
        "pregunta": "¿Cómo pagarás la matrícula?",
        "categoria": "pago_matricula",
        "tips": "Menciona si es pago único o fraccionado, método de pago.",
        "respuesta_modelo": "La universidad permite pago fraccionado en 3 cuotas: €1,500 al matricularme, €1,500 en enero, y €1,200 en abril. Pagaré mediante transferencia bancaria internacional desde mi cuenta."
    },
    {
        "pregunta": "¿Tienes deudas en tu país?",
        "categoria": "deudas",
        "tips": "Idealmente di que no. Si tienes deudas manejables, explica que están bajo control.",
        "respuesta_modelo": "No tengo deudas. He ahorrado durante 3 años específicamente para estos estudios y mi familia tampoco tiene deudas significativas, lo cual nos permite financiar este proyecto sin problemas."
    },
    {
        "pregunta": "¿Recibirás algún tipo de beca de tu gobierno?",
        "categoria": "beca_gobierno",
        "tips": "Si aplicas, menciona nombre del programa y monto. Si no, está bien decirlo.",
        "respuesta_modelo": "He aplicado a la beca estatal para estudios en el extranjero que otorga €800 mensuales. Estoy en lista de espera pero no dependo de ella porque tengo fondos propios suficientes."
    },
    {
        "pregunta": "¿Cómo demostraste solvencia económica en tu solicitud?",
        "categoria": "documentacion_economica",
        "tips": "Lista todos los documentos económicos que presentaste.",
        "respuesta_modelo": "Presenté: extractos bancarios de 6 meses, carta de patrocinio notariada, certificados laborales de mis padres con salario, últimas 3 declaraciones de renta, y certificado de propiedad de bienes inmuebles."
    },
    {
        "pregunta": "¿Cuánto dinero necesitas demostrar para la visa de estudiante?",
        "categoria": "requisito_minimo",
        "tips": "Menciona el monto oficial requerido (IPREM x meses).",
        "respuesta_modelo": "Para visa de estudiante de un año académico debo demostrar el 100% del IPREM mensual por 12 meses, lo cual equivale aproximadamente a €7,200-€10,000 dependiendo de la duración exacta del programa."
    },

    # === IDIOMA Y ADAPTACIÓN (15 preguntas) ===
    {
        "pregunta": "¿Cómo es tu nivel de español?",
        "categoria": "idioma",
        "tips": "Sé honesto sobre tu nivel. Si es básico, menciona planes de tomar curso intensivo.",
        "respuesta_modelo": "Mi nivel actual es B2-intermedio alto. He estudiado español durante 2 años en un instituto certificado y obtuve diploma DELE B2. Planeo tomar curso intensivo antes de iniciar para alcanzar nivel C1."
    },
    {
        "pregunta": "¿Tienes certificado de español?",
        "categoria": "certificacion_idioma",
        "tips": "DELE, SIELE son los más reconocidos. Menciona nivel y fecha de obtención.",
        "respuesta_modelo": "Sí, tengo certificado DELE B2 otorgado por el Instituto Cervantes en marzo 2024. También he estado practicando conversación con nativos online para mejorar mi fluidez."
    },
    {
        "pregunta": "¿Entiendes perfectamente lo que te estoy preguntando ahora?",
        "categoria": "comprension",
        "tips": "Esta pregunta prueba tu español real. Responde con seguridad y claridad.",
        "respuesta_modelo": "Sí, entiendo perfectamente. Usted me está preguntando sobre mi comprensión del español y puedo responder con claridad a todas sus preguntas tanto en este proceso como en mis estudios."
    },
    {
        "pregunta": "¿Cómo te prepararás para adaptarte a la vida en España?",
        "categoria": "adaptacion_cultural",
        "tips": "Menciona investigación cultural, contacto con estudiantes, mentalidad abierta.",
        "respuesta_modelo": "He investigado la cultura española, costumbres y sistema educativo. Planeo llegar semanas antes para adaptarme, inscribirme en grupos de estudiantes internacionales, y mantener mentalidad abierta para aprender de la cultura local."
    },
    {
        "pregunta": "¿Conoces la ciudad donde estudiarás?",
        "categoria": "conocimiento_ciudad",
        "tips": "Menciona características de la ciudad: transporte, zonas, clima, actividades.",
        "respuesta_modelo": "Sí, Madrid es la capital con 3.2 millones de habitantes. Tiene excelente transporte público con metro y autobuses. El clima es continental con veranos calurosos e inviernos fríos. Hay muchas actividades culturales y es muy cosmopolita."
    },
    {
        "pregunta": "¿Has visitado España antes?",
        "categoria": "visitas_previas",
        "tips": "Si visitaste, menciona cuándo y qué conociste. Si no, está bien decirlo.",
        "respuesta_modelo": "No he visitado España aún, pero he investigado extensamente sobre la cultura, visto documentales, hablado con personas que viven allá, y estoy muy preparado para la experiencia de vivir en el país."
    },
    {
        "pregunta": "¿Cómo manejarás estar lejos de tu familia?",
        "categoria": "separacion_familiar",
        "tips": "Muestra madurez emocional, menciona videollamadas, visitas programadas.",
        "respuesta_modelo": "Aunque será un desafío, soy una persona madura y independiente. Mantendremos contacto frecuente por videollamadas. Planeo visitarlos en vacaciones de Navidad. Esta separación temporal es una inversión en mi futuro profesional."
    },
    {
        "pregunta": "¿Tienes amigos o conocidos en España?",
        "categoria": "red_social",
        "tips": "Si tienes contactos, menciona que te ayudarán con adaptación pero eres independiente.",
        "respuesta_modelo": "Tengo un primo que estudió en Madrid y me ha dado consejos útiles sobre alojamiento y adaptación. También contacté a estudiantes de mi país en grupos de Facebook que me han orientado, pero soy completamente independiente."
    },
    {
        "pregunta": "¿Qué harás si te sientes solo o nostálgico?",
        "categoria": "salud_emocional",
        "tips": "Menciona estrategias: actividades sociales, deportes, clubs estudiantiles.",
        "respuesta_modelo": "Me uniré a clubs estudiantiles y asociaciones de mi carrera para conocer gente. Haré deporte regularmente, mantendré contacto con familia, y si es necesario buscaré apoyo psicológico que ofrecen las universidades españolas."
    },
    {
        "pregunta": "¿Conoces las diferencias culturales entre tu país y España?",
        "categoria": "diferencias_culturales",
        "tips": "Menciona horarios, comidas, costumbres sociales. Muestra respeto y apertura.",
        "respuesta_modelo": "Sí, en España los horarios son diferentes: se cena más tarde cerca de las 9-10pm, hay siesta en algunas regiones, y los españoles son más directos en la comunicación. Respeto estas diferencias y tengo mentalidad abierta para adaptarme."
    },
    {
        "pregunta": "¿Hablas algún otro idioma además del español?",
        "categoria": "idiomas_adicionales",
        "tips": "Menciona nivel de inglés u otros idiomas. Es un plus.",
        "respuesta_modelo": "Sí, hablo inglés a nivel intermedio B1, lo cual me ayudará en bibliografía académica y comunicación con estudiantes internacionales. También estoy aprendiendo catalán básico por si es útil."
    },
    {
        "pregunta": "¿Cómo practicas tu español actualmente?",
        "categoria": "practica_idioma",
        "tips": "Menciona métodos activos: clases, intercambio, apps, series, libros.",
        "respuesta_modelo": "Tomo clases de español 3 veces por semana, practico conversación con nativos en Tandem app, veo series españolas sin subtítulos, leo noticias en español, y escucho podcasts educativos diariamente."
    },
    {
        "pregunta": "¿Entiendes el acento español?",
        "categoria": "acento",
        "tips": "Si tienes dudas, di que te estás familiarizando y adaptarás rápido.",
        "respuesta_modelo": "Sí, me he familiarizado con el acento español viendo series y hablando con españoles online. Aunque hay diferencias con el español latinoamericano, entiendo bien la pronunciación con la 'z' y puedo adaptarme rápidamente."
    },
    {
        "pregunta": "¿Qué te preocupa sobre vivir en España?",
        "categoria": "preocupaciones",
        "tips": "Menciona preocupaciones normales pero muestra que tienes plan para manejarlas.",
        "respuesta_modelo": "Mi única preocupación es adaptarme rápido al sistema educativo y los horarios españoles, pero he investigado mucho y sé que las universidades ofrecen apoyo a estudiantes internacionales. Confío en que me adaptaré bien."
    },
    {
        "pregunta": "¿Conoces estudiantes de tu país que estén en España?",
        "categoria": "red_paisanos",
        "tips": "Si conoces, menciona que te pueden orientar pero no dependes de ellos.",
        "respuesta_modelo": "Sí, conozco 3 estudiantes de mi país en Madrid a través de grupos de Facebook. Me han dado consejos prácticos sobre alojamiento y documentación, pero planeo ser independiente y también integrarme con estudiantes españoles e internacionales."
    },

    # === UNIVERSIDAD Y PROGRAMA (15 preguntas) ===
    {
        "pregunta": "¿Ya tienes la carta de admisión de la universidad?",
        "categoria": "admision",
        "tips": "Lleva copia de la carta de admisión, menciona fecha de emisión.",
        "respuesta_modelo": "Sí, recibí mi carta de admisión el 15 de mayo de 2024. Está firmada por el Decano de la Facultad de Medicina y confirma mi plaza para el año académico 2024-2025. Traigo copia oficial."
    },
    {
        "pregunta": "¿Cuántas horas de clase tendrás por semana?",
        "categoria": "carga_academica",
        "tips": "Menciona horas teóricas, prácticas, horario general.",
        "respuesta_modelo": "El programa tiene aproximadamente 25 horas semanales: 15 horas de clases teóricas y 10 horas de prácticas en laboratorio o hospital. El horario es de lunes a viernes, generalmente de 9am a 2pm y algunas tardes."
    },
    {
        "pregunta": "¿Qué requisitos académicos cumpliste para ser admitido?",
        "categoria": "requisitos_admision",
        "tips": "Menciona título previo, promedio, documentos apostillados, homologación.",
        "respuesta_modelo": "Completé licenciatura en Enfermería con promedio 8.5/10, obtuve apostilla de La Haya de mi título, hice homologación en el Ministerio de Educación español, presenté certificado de notas traducido oficialmente, y cumplí requisito de español B2."
    },
    {
        "pregunta": "¿Dónde vivirás durante tus estudios?",
        "categoria": "alojamiento",
        "tips": "Muestra que has investigado o reservado: residencia, piso compartido, ubicación.",
        "respuesta_modelo": "Viviré en piso compartido en el barrio de Argüelles, cerca del campus. Ya tengo reserva confirmada con contrato firmado por €450 mensuales incluyendo servicios. Es habitación individual en piso de 3 estudiantes."
    },
    {
        "pregunta": "¿Qué asignaturas cursarás en tu programa?",
        "categoria": "plan_estudios",
        "tips": "Menciona 4-5 asignaturas principales del primer semestre.",
        "respuesta_modelo": "En primer semestre cursaré: Diagnóstico Clínico Avanzado, Farmacología Especializada, Técnicas Quirúrgicas I, Bioestadística Aplicada, y Ética Médica. En segundo semestre tendré Técnicas Quirúrgicas II, Investigación Clínica, y prácticas hospitalarias."
    },
    {
        "pregunta": "¿Quién es el director del programa al que aplicas?",
        "categoria": "conocimiento_profundo",
        "tips": "Investiga nombre del director o coordinador del programa, su especialidad.",
        "respuesta_modelo": "El Dr. Carlos Martínez López es el director del programa. Es especialista en cirugía cardiovascular con más de 30 publicaciones internacionales. He leído varios de sus artículos y me interesa su línea de investigación."
    },
    {
        "pregunta": "¿Cómo es el sistema de evaluación en tu programa?",
        "categoria": "evaluacion",
        "tips": "Menciona exámenes, trabajos, prácticas, evaluación continua.",
        "respuesta_modelo": "La evaluación es continua: 40% exámenes parciales, 30% trabajos prácticos y presentaciones, 20% prácticas en hospital, y 10% participación. También debo aprobar examen final y defender un TFM al terminar el máster."
    },
    {
        "pregunta": "¿Incluye prácticas profesionales tu programa?",
        "categoria": "practicas",
        "tips": "Menciona horas, lugares, supervisión, importancia para tu formación.",
        "respuesta_modelo": "Sí, incluye 300 horas de prácticas en hospitales asociados como Hospital Clínico San Carlos y Hospital La Paz. Estaré supervisado por médicos especialistas y estas prácticas son fundamentales para mi formación práctica."
    },
    {
        "pregunta": "¿Tu título será válido en tu país?",
        "categoria": "reconocimiento_titulo",
        "tips": "Investiga convenios de reconocimiento, homologación, validez internacional.",
        "respuesta_modelo": "Sí, España y mi país tienen convenio de reconocimiento mutuo de títulos universitarios. Además, tendré que hacer proceso de homologación en el Ministerio de Educación de mi país, pero el título será plenamente válido."
    },
    {
        "pregunta": "¿Cuándo termina tu programa?",
        "categoria": "duracion",
        "tips": "Sé específico con fecha de inicio y fin, duración total.",
        "respuesta_modelo": "El programa inicia el 15 de septiembre de 2024 y termina el 30 de junio de 2025. Es un máster de un año académico completo (60 ECTS). Defenderé mi TFM en julio 2025 y recibiré el título en septiembre 2025."
    },
    {
        "pregunta": "¿Qué especialidad o mención elegirás?",
        "categoria": "especializacion",
        "tips": "Si el programa tiene menciones, especifica cuál y por qué.",
        "respuesta_modelo": "El máster ofrece dos menciones: Cirugía General y Cirugía Cardiovascular. Elegiré la mención en Cirugía Cardiovascular porque es mi área de interés y tiene mayor demanda en mi país."
    },
    {
        "pregunta": "¿Has contactado a algún profesor del programa?",
        "categoria": "contacto_profesores",
        "tips": "Si contactaste, menciona nombre y tema. Si no, no es obligatorio.",
        "respuesta_modelo": "Sí, contacté por email a la Dra. Ana Gómez, coordinadora de prácticas, para consultar sobre las rotaciones hospitalarias. Me respondió muy amablemente y me dio detalles sobre las especialidades disponibles."
    },
    {
        "pregunta": "¿Qué investigarás en tu trabajo final de máster?",
        "categoria": "tfm",
        "tips": "Menciona área de interés, aunque sea preliminar. Muestra que has pensado en ello.",
        "respuesta_modelo": "Me interesa investigar sobre técnicas mínimamente invasivas en cirugía cardiovascular. Planeo hacer una revisión sistemática de outcomes en pacientes operados con estas técnicas versus cirugía abierta tradicional."
    },
    {
        "pregunta": "¿Sabes qué documentación necesitarás al llegar?",
        "categoria": "tramites",
        "tips": "Menciona NIE, empadronamiento, tarjeta sanitaria, cuenta bancaria.",
        "respuesta_modelo": "Sí, debo obtener el NIE en Oficina de Extranjería, empadronarme en el Ayuntamiento, tramitar tarjeta sanitaria europea o seguro privado, abrir cuenta bancaria, y matricularme oficialmente en la universidad presentando documentos apostillados."
    },
    {
        "pregunta": "¿Qué pasa si repruebas alguna asignatura?",
        "categoria": "plan_contingencia",
        "tips": "Menciona que hay convocatorias de recuperación, pero confías en aprobar todo.",
        "respuesta_modelo": "Si repruebo, hay convocatoria extraordinaria en septiembre. Sin embargo, confío en aprobar todas las asignaturas en primera convocatoria porque he mantenido buen rendimiento académico durante toda mi carrera con promedio de 8.5/10."
    },

    # === INTENCIÓN DE RETORNO (15 preguntas) ===
    {
        "pregunta": "¿Tienes familia en tu país que dependa de ti?",
        "categoria": "vinculos_familiares",
        "tips": "Menciona padres, hermanos, cónyuge como razones fuertes para regresar.",
        "respuesta_modelo": "Sí, mis padres tienen 60 y 58 años y soy hijo único. Aunque son independientes ahora, en el futuro necesitarán mi apoyo. También tengo mi novia con quien planeo casarme cuando regrese."
    },
    {
        "pregunta": "¿Tienes propiedades en tu país?",
        "categoria": "bienes",
        "tips": "Propiedades son vínculos fuertes. Menciona si tienes casa, terreno, negocio.",
        "respuesta_modelo": "Sí, tengo un apartamento a mi nombre valorado en €40,000 que compré hace 2 años. Lo estoy alquilando durante mi ausencia pero planeo regresar a vivir allí. También mis padres tienen una casa familiar."
    },
    {
        "pregunta": "¿Qué oportunidades laborales tendrás al regresar?",
        "categoria": "oportunidades_laborales",
        "tips": "Menciona demanda de tu profesión, contactos, posibles empleadores.",
        "respuesta_modelo": "En mi país hay gran demanda de cirujanos cardiovasculares especializados. El Hospital Central de mi ciudad me ha expresado interés en contratarme cuando regrese. También puedo abrir consulta privada que tiene alta rentabilidad."
    },
    {
        "pregunta": "¿Tu pareja está de acuerdo con que estudies en el extranjero?",
        "categoria": "relacion_pareja",
        "tips": "Si tienes pareja, menciona que te apoya y esperarán. Refuerza que regresarás.",
        "respuesta_modelo": "Sí, mi pareja me apoya completamente en este proyecto. Mantendremos relación a distancia durante este año. Planeo visitarla en vacaciones y ella está dispuesta a esperarme porque sabe que regresaré con mejor preparación."
    },
    {
        "pregunta": "¿Por qué no quieres quedarte a trabajar en España?",
        "categoria": "intencion_quedarse",
        "tips": "Di claramente que no planeas quedarte: vínculos familiares, oportunidades en tu país.",
        "respuesta_modelo": "No planeo quedarme en España porque mi vida, familia y futuro están en mi país. Voy específicamente por la formación académica. En mi país tengo mejores oportunidades laborales, mi red de contactos, y el compromiso con mi familia."
    },
    {
        "pregunta": "¿Qué pasará con tu trabajo actual?",
        "categoria": "situacion_laboral_retorno",
        "tips": "Si tienes trabajo, menciona excedencia o garantía de reincorporación.",
        "respuesta_modelo": "He solicitado excedencia por estudios en mi hospital durante un año. Mi jefe me ha garantizado por escrito que podré reincorporarme a mi puesto cuando regrese, incluso con mejor posición por mi especialización."
    },
    {
        "pregunta": "¿Conoces a alguien que se haya quedado ilegalmente en España?",
        "categoria": "inmigracion_ilegal",
        "tips": "Di claramente que NO conoces a nadie y que no es tu intención.",
        "respuesta_modelo": "No conozco a nadie en esa situación y definitivamente no es mi intención. Voy legalmente con visa de estudiante por un año específico y regresaré al terminar. Respeto completamente las leyes migratorias españolas."
    },
    {
        "pregunta": "¿Tienes parientes en España o Europa?",
        "categoria": "familiares_europa",
        "tips": "Si tienes familiares, sé honesto pero aclara que no dependerás de ellos ni te quedarás.",
        "respuesta_modelo": "No tengo familiares directos en España. Un primo lejano vive en Barcelona pero no tenemos contacto frecuente. Voy exclusivamente por mis estudios y mi familia directa está toda en mi país esperando mi regreso."
    },
    {
        "pregunta": "¿Qué te haría cambiar de opinión sobre regresar a tu país?",
        "categoria": "condiciones_cambio",
        "tips": "Di firmemente que NADA te haría cambiar de opinión. Tu compromiso es regresar.",
        "respuesta_modelo": "Nada me haría cambiar de opinión. Mi compromiso es regresar porque mi familia, mi pareja, mis propiedades y mi futuro profesional están allá. España es solo un destino temporal para formarme académicamente."
    },
    {
        "pregunta": "¿Sabes que puedes solicitar residencia después de estudiar?",
        "categoria": "conocimiento_residencia",
        "tips": "Di que sabes que existe esa posibilidad pero NO es tu intención.",
        "respuesta_modelo": "Sé que legalmente existe esa posibilidad, pero no es mi intención. Voy específicamente por un año académico y regresaré al terminar. Tengo obligaciones familiares y profesionales en mi país que requieren mi retorno."
    },
    {
        "pregunta": "¿Qué diferencia hay entre vivir en España y en tu país?",
        "categoria": "calidad_vida",
        "tips": "No critiques tu país. Menciona que España es bueno para estudios pero tu vida está en casa.",
        "respuesta_modelo": "España tiene excelente calidad educativa y servicios, pero mi país también ofrece buena calidad de vida, costo de vida menor, y allá tengo mi red familiar y profesional. No busco migrar sino formarme y regresar."
    },
    {
        "pregunta": "¿Cómo demuestras que regresarás?",
        "categoria": "prueba_retorno",
        "tips": "Resume todos tus vínculos: familia, trabajo, propiedades, pareja.",
        "respuesta_modelo": "Tengo múltiples vínculos: mis padres ancianos que me necesitan, propiedades a mi nombre, pareja esperándome, excedencia laboral garantizada, y mis estudios están diseñados para ejercer en mi país, no en España."
    },
    {
        "pregunta": "¿Te gustaría trabajar en España si tuvieras oportunidad?",
        "categoria": "interes_laboral",
        "tips": "Di que NO porque tu plan es regresar. Puedes mencionar que España es bueno pero no es tu objetivo.",
        "respuesta_modelo": "Aunque España ofrece buenas oportunidades, no es mi objetivo trabajar aquí. Mi plan siempre ha sido formarme y regresar. Las oportunidades en mi país son mejores para mí considerando mi red de contactos y vínculos familiares."
    },
    {
        "pregunta": "¿Qué harías si te ofrecen trabajo muy bien pagado en España?",
        "categoria": "hipotetico_laboral",
        "tips": "Di que agradecerías pero rechazarías porque tu compromiso es regresar.",
        "respuesta_modelo": "Agradecería la oferta pero la rechazaría porque mi compromiso es con mi país y mi familia. El dinero no es mi única motivación. Tengo obligaciones y proyectos de vida en mi país que son prioritarios."
    },
    {
        "pregunta": "¿Tus padres quieren que regreses o prefieres quedarte?",
        "categoria": "deseo_familiar",
        "tips": "Di que tus padres esperan tu regreso y tú también quieres volver.",
        "respuesta_modelo": "Mis padres definitivamente esperan mi regreso. Ellos apoyan mis estudios pero con la condición de que regrese al terminar. Yo también quiero regresar porque mi vida y futuro están allá, no aquí."
    },

    # === PREPARACIÓN Y LOGÍSTICA (15 preguntas) ===
    {
        "pregunta": "¿Cuándo planeas viajar a España?",
        "categoria": "fecha_viaje",
        "tips": "Menciona fecha específica, dale tiempo para instalarte antes de clases.",
        "respuesta_modelo": "Planeo viajar el 20 de agosto de 2024, tres semanas antes del inicio de clases el 15 de septiembre. Esto me dará tiempo para buscar alojamiento definitivo, obtener NIE, empadronarme, y familiarizarme con la ciudad."
    },
    {
        "pregunta": "¿Ya compraste tu boleto de avión?",
        "categoria": "boleto",
        "tips": "Si compraste, menciona aerolínea y fecha. Si no, explica que esperabas la visa.",
        "respuesta_modelo": "Todavía no he comprado el boleto porque esperaba recibir la visa primero. Pero he cotizado vuelos con Iberia para el 20 de agosto por aproximadamente €800 ida y vuelta. Compraré en cuanto tenga la visa aprobada."
    },
    {
        "pregunta": "¿Dónde te alojarás las primeras noches al llegar?",
        "categoria": "alojamiento_inicial",
        "tips": "Menciona hotel, hostal, Airbnb reservado para primeros días.",
        "respuesta_modelo": "He reservado habitación en hostal cerca de la universidad por 7 noches a €30 por noche. Durante esa semana buscaré alojamiento permanente, aunque ya tengo algunas opciones pre-seleccionadas que he visto online."
    },
    {
        "pregunta": "¿Qué documentos llevarás en tu equipaje?",
        "categoria": "documentos_viaje",
        "tips": "Lista documentos importantes: pasaporte, visa, carta admisión, seguro, fondos.",
        "respuesta_modelo": "Llevaré: pasaporte con visa, carta de admisión original, comprobantes de pago de matrícula, seguro médico, extractos bancarios, certificados académicos apostillados, fotografías tamaño pasaporte, y copia de reserva de alojamiento."
    },
    {
        "pregunta": "¿Tienes seguro de viaje internacional?",
        "categoria": "seguro_viaje",
        "tips": "Menciona cobertura para equipaje, cancelaciones, emergencias médicas.",
        "respuesta_modelo": "Sí, contraté seguro de viaje internacional con AXA que cubre emergencias médicas hasta €50,000, pérdida de equipaje, cancelaciones de vuelo, y repatriación. Es válido desde el día que salgo hasta que regreso."
    },
    {
        "pregunta": "¿Sabes cómo llegar del aeropuerto a tu alojamiento?",
        "categoria": "transporte_inicial",
        "tips": "Demuestra que investigaste: metro, bus, taxi, costo aproximado.",
        "respuesta_modelo": "Sí, desde el aeropuerto de Barajas tomaré el Metro Línea 8 hasta Nuevos Ministerios, luego Línea 6 hasta Argüelles cerca de mi alojamiento. El viaje dura aproximadamente 45 minutos y cuesta €5 con tarjeta de transporte."
    },
    {
        "pregunta": "¿Qué equipaje llevarás?",
        "categoria": "equipaje",
        "tips": "Menciona maleta permitida, artículos esenciales, clima español.",
        "respuesta_modelo": "Llevaré una maleta de 23kg en bodega y mochila de mano. Incluiré ropa para clima continental (veranos calurosos, inviernos fríos), documentos importantes, laptop, medicamentos personales, y artículos de higiene. Compraré lo demás en España."
    },
    {
        "pregunta": "¿Llevarás medicamentos?",
        "categoria": "medicamentos",
        "tips": "Si llevas medicamentos, menciona que están en envase original con receta.",
        "respuesta_modelo": "Sí, llevo antihistamínicos y analgésicos básicos en sus envases originales con receta médica traducida. No tengo condiciones médicas graves que requieran medicamentos especiales. También llevaré botiquín de primeros auxilios básico."
    },
    {
        "pregunta": "¿Sabes usar el transporte público en Madrid?",
        "categoria": "transporte_publico",
        "tips": "Menciona que investigaste metro, bus, abonos de transporte.",
        "respuesta_modelo": "He investigado que Madrid tiene excelente metro con 12 líneas, autobuses urbanos, y Cercanías para zonas más alejadas. Compraré abono joven mensual que cuesta €20 para menores de 26 años y permite viajes ilimitados."
    },
    {
        "pregunta": "¿Qué harás si pierdes tu pasaporte en España?",
        "categoria": "emergencia_documentos",
        "tips": "Menciona que contactarás embajada, tienes copias digitales.",
        "respuesta_modelo": "Contactaré inmediatamente a la embajada de mi país en Madrid para reportar pérdida y solicitar pasaporte temporal. Llevo copias digitales escaneadas en mi email y copias físicas separadas. También tengo números de emergencia guardados."
    },
    {
        "pregunta": "¿Conoces el número de emergencias en España?",
        "categoria": "emergencias",
        "tips": "112 es el número único de emergencias en España.",
        "respuesta_modelo": "Sí, el 112 es el número de emergencias único en España para policía, ambulancia, bomberos. También tengo guardados números de mi embajada (91-xxx-xxxx), universidad, y contactos de emergencia en mi país."
    },
    {
        "pregunta": "¿Tienes plan de teléfono móvil para España?",
        "categoria": "telefono",
        "tips": "Menciona que comprarás SIM prepago o plan mensual al llegar.",
        "respuesta_modelo": "Compraré tarjeta SIM prepago de Vodafone u Orange al llegar en el aeropuerto por €10-20. Luego evaluaré planes mensuales de €15-25 con datos ilimitados. Mantendré mi número de mi país activo por WhatsApp."
    },
    {
        "pregunta": "¿Sabes qué vacunas necesitas?",
        "categoria": "vacunas",
        "tips": "España no requiere vacunas específicas, pero menciona COVID si aplica.",
        "respuesta_modelo": "España no requiere vacunas específicas para estudiantes. Tengo todas las vacunas básicas actualizadas: tétanos, hepatitis B, MMR. También tengo esquema completo de COVID-19 con certificado internacional que llevaré por si lo requieren."
    },
    {
        "pregunta": "¿Llevarás dinero en efectivo o tarjetas?",
        "categoria": "dinero_viaje",
        "tips": "Menciona mix: algo de efectivo para primeros días, tarjetas internacionales.",
        "respuesta_modelo": "Llevaré €500 en efectivo para los primeros días (transporte, comidas, emergencias). También llevo tarjeta de débito internacional Visa y tarjeta de crédito Mastercard. Abriré cuenta bancaria en España en la primera semana."
    },
    {
        "pregunta": "¿Qué harás si llegas y hay problema con tu alojamiento?",
        "categoria": "plan_contingencia_alojamiento",
        "tips": "Menciona alternativas: hostal, hotel económico, contactos de emergencia.",
        "respuesta_modelo": "Tengo respaldo: he guardado contactos de 3 hostales baratos cerca de la universidad (€25-35/noche). También tengo números de agencias de alojamiento estudiantil. En último caso, mi primo en Barcelona me ha ofrecido ayuda si hay emergencia extrema."
    }
]
