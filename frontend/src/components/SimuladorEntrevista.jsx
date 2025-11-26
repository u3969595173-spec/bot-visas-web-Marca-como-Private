import React, { useState } from 'react'
import './SimuladorEntrevista.css'

function SimuladorEntrevista() {
  const [preguntaActual, setPreguntaActual] = useState(0)
  const [respuestas, setRespuestas] = useState({})
  const [mostrarConsejos, setMostrarConsejos] = useState(false)

  const preguntas = [
    {
      id: 1,
      pregunta: "¿Por qué quieres estudiar en España?",
      categoria: "Motivación",
      consejos: [
        "Sé específico sobre el programa y la institución",
        "Menciona cómo se relaciona con tus objetivos profesionales",
        "Habla sobre la cultura española y tu interés en ella",
        "Evita respuestas genéricas como 'porque es un buen país'"
      ],
      respuestaEjemplo: "Quiero estudiar en España porque la Universidad de Barcelona ofrece el mejor programa de [tu especialidad] en Europa. Además, dominar el español me abrirá oportunidades profesionales en mercados latinoamericanos."
    },
    {
      id: 2,
      pregunta: "¿Cómo vas a financiar tus estudios?",
      categoria: "Financiamiento",
      consejos: [
        "Presenta evidencia clara de fondos suficientes",
        "Menciona todas las fuentes: ahorros, familia, becas",
        "Calcula costos realistas: matrícula, alojamiento, comida, transporte",
        "Ten documentos bancarios preparados"
      ],
      respuestaEjemplo: "Cuento con €15,000 en ahorros personales más el apoyo de mi familia que cubrirá €10,000 adicionales. He calculado que el costo total será aproximadamente €20,000 para el primer año."
    },
    {
      id: 3,
      pregunta: "¿Cuáles son tus planes después de terminar tus estudios?",
      categoria: "Planes Futuros",
      consejos: [
        "Demuestra intención de regresar a tu país (importante para visa)",
        "Menciona oportunidades laborales específicas en tu país",
        "Habla sobre cómo aplicarás lo aprendido",
        "Muestra que tienes vínculos fuertes con tu país de origen"
      ],
      respuestaEjemplo: "Planeo regresar a mi país para trabajar en [empresa/sector], donde hay una creciente demanda de profesionales con formación internacional en mi área. También mantengo vínculos familiares fuertes que me esperan."
    },
    {
      id: 4,
      pregunta: "¿Por qué elegiste esta universidad/programa específico?",
      categoria: "Programa Académico",
      consejos: [
        "Investiga bien la universidad y el programa",
        "Menciona profesores específicos o áreas de investigación",
        "Habla sobre rankings y reconocimientos",
        "Demuestra que no es una elección al azar"
      ],
      respuestaEjemplo: "Esta universidad está clasificada entre las top 100 en mi especialidad. El programa ofrece prácticas en empresas líderes y el profesor [nombre] es referente mundial en [área], lo cual es perfecto para mi tesis."
    },
    {
      id: 5,
      pregunta: "¿Dónde vas a vivir en España?",
      categoria: "Alojamiento",
      consejos: [
        "Ten una dirección específica confirmada",
        "Lleva contrato de alquiler o carta de alojamiento",
        "Menciona cercanía a la universidad",
        "Demuestra que has investigado el barrio"
      ],
      respuestaEjemplo: "Tengo reservada una habitación en [dirección específica], a 15 minutos en metro de la universidad. El contrato está firmado y pagado el primer mes."
    },
    {
      id: 6,
      pregunta: "¿Qué nivel de español tienes?",
      categoria: "Idioma",
      consejos: [
        "Sé honesto sobre tu nivel",
        "Menciona certificados si los tienes (DELE, SIELE)",
        "Habla sobre clases que has tomado",
        "Si es bajo, menciona planes para mejorarlo"
      ],
      respuestaEjemplo: "Tengo nivel B1 certificado por el DELE. He estado estudiando español por 2 años y planeo tomar un curso intensivo durante el primer mes en España para alcanzar el B2."
    },
    {
      id: 7,
      pregunta: "¿Tienes familia en España?",
      categoria: "Vínculos",
      consejos: [
        "Responde con la verdad",
        "Si tienes familia, menciona que no dependes de ellos",
        "Si no tienes, enfatiza tu independencia y madurez",
        "Evita que piensen que te quedarás ilegalmente"
      ],
      respuestaEjemplo: "No tengo familia en España, pero cuento con una red de contactos profesionales que me ayudarán a integrarme. Mi familia está en [país] y planeo visitarlos regularmente."
    },
    {
      id: 8,
      pregunta: "¿Has viajado al extranjero antes?",
      categoria: "Experiencia Internacional",
      consejos: [
        "Menciona viajes previos si los tienes",
        "Demuestra que siempre has cumplido con visas",
        "Si no has viajado, muestra entusiasmo por la oportunidad",
        "Habla sobre tu capacidad de adaptación"
      ],
      respuestaEjemplo: "Sí, he viajado a [países] en viajes de turismo/trabajo. Siempre he respetado los términos de las visas y regresado a mi país. Este será mi primer viaje con fines académicos."
    }
  ]

  const consejosPrincipales = [
    {
      titulo: "Antes de la Entrevista",
      consejos: [
        "Llega 15-20 minutos antes",
        "Viste formal y profesionalmente",
        "Lleva todos los documentos organizados en una carpeta",
        "Practica tus respuestas pero no las memorices",
        "Duerme bien la noche anterior"
      ]
    },
    {
      titulo: "Durante la Entrevista",
      consejos: [
        "Mantén contacto visual",
        "Habla claro y con confianza",
        "No mientas, sé honesto",
        "Si no entiendes, pide que repitan la pregunta",
        "Sonríe y mantén una actitud positiva"
      ]
    },
    {
      titulo: "Documentos Esenciales",
      consejos: [
        "Pasaporte vigente",
        "Carta de aceptación de la universidad",
        "Comprobantes de fondos económicos",
        "Seguro médico internacional",
        "Comprobante de alojamiento",
        "Certificados académicos",
        "Fotografías tamaño pasaporte"
      ]
    },
    {
      titulo: "Errores Comunes a Evitar",
      consejos: [
        "No menciones intención de trabajar ilegalmente",
        "No digas que quieres quedarte permanentemente",
        "No seas vago en tus respuestas",
        "No muestres nerviosismo excesivo",
        "No llegues sin preparación"
      ]
    }
  ]

  const handleRespuesta = (preguntaId, respuesta) => {
    setRespuestas({
      ...respuestas,
      [preguntaId]: respuesta
    })
  }

  const siguientePregunta = () => {
    if (preguntaActual < preguntas.length - 1) {
      setPreguntaActual(preguntaActual + 1)
    }
  }

  const preguntaAnterior = () => {
    if (preguntaActual > 0) {
      setPreguntaActual(preguntaActual - 1)
    }
  }

  const pregunta = preguntas[preguntaActual]

  return (
    <div className="simulador-entrevista">
      <div className="simulador-header">
        <h1>🎤 Simulador de Entrevista Consular</h1>
        <p>Prepárate para tu entrevista de visa de estudiante con estas preguntas frecuentes</p>
      </div>

      <div className="progreso-bar">
        <div 
          className="progreso-fill" 
          style={{ width: `${((preguntaActual + 1) / preguntas.length) * 100}%` }}
        />
        <span className="progreso-text">
          Pregunta {preguntaActual + 1} de {preguntas.length}
        </span>
      </div>

      <div className="simulador-content">
        <div className="pregunta-card">
          <div className="pregunta-categoria">{pregunta.categoria}</div>
          <h2 className="pregunta-texto">{pregunta.pregunta}</h2>

          <div className="respuesta-area">
            <label>Tu respuesta:</label>
            <textarea
              value={respuestas[pregunta.id] || ''}
              onChange={(e) => handleRespuesta(pregunta.id, e.target.value)}
              placeholder="Escribe tu respuesta aquí..."
              rows="6"
            />
          </div>

          <button 
            onClick={() => setMostrarConsejos(!mostrarConsejos)}
            className="btn-consejos"
          >
            {mostrarConsejos ? '▼ Ocultar Consejos' : '▶ Ver Consejos y Ejemplo'}
          </button>

          {mostrarConsejos && (
            <div className="consejos-section">
              <h3>💡 Consejos para esta pregunta:</h3>
              <ul>
                {pregunta.consejos.map((consejo, index) => (
                  <li key={index}>{consejo}</li>
                ))}
              </ul>

              <div className="respuesta-ejemplo">
                <h4>📝 Ejemplo de buena respuesta:</h4>
                <p>{pregunta.respuestaEjemplo}</p>
              </div>
            </div>
          )}

          <div className="navegacion-botones">
            <button 
              onClick={preguntaAnterior}
              disabled={preguntaActual === 0}
              className="btn-nav"
            >
              ← Anterior
            </button>
            <button 
              onClick={siguientePregunta}
              disabled={preguntaActual === preguntas.length - 1}
              className="btn-nav btn-siguiente"
            >
              Siguiente →
            </button>
          </div>
        </div>

        <div className="consejos-generales">
          <h3>📋 Consejos Generales</h3>
          {consejosPrincipales.map((seccion, index) => (
            <div key={index} className="consejo-seccion">
              <h4>{seccion.titulo}</h4>
              <ul>
                {seccion.consejos.map((consejo, idx) => (
                  <li key={idx}>{consejo}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default SimuladorEntrevista
