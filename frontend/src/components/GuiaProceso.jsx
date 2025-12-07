import React, { useState } from 'react'
import './GuiaProceso.css'

const GuiaProceso = () => {
  const [faseExpandida, setFaseExpandida] = useState(null)

  const toggleFase = (faseId) => {
    setFaseExpandida(faseExpandida === faseId ? null : faseId)
  }

  const fases = [
    {
      id: 1,
      nombre: "FASE 1: CAPTACIÓN Y REGISTRO",
      duracion: "Días 1-3",
      color: "#667eea",
      pasos: [
        {
          numero: 0,
          titulo: "Primer Contacto",
          queHace: "Estudiante llega por redes sociales/referidos/web",
          accionAgencia: "Responder en <24h, explicar servicios y tarifas",
          documentos: ["Ninguno aún"],
          sistema: "Crear lead en CRM",
          tiempo: "1 día",
          importante: true
        },
        {
          numero: 1,
          titulo: "Registro Inicial",
          queHace: "Estudiante llena formulario web o bot Telegram",
          accionAgencia: "Revisar datos básicos: nombre, email, pasaporte, edad, nacionalidad, ciudad origen",
          documentos: ["Copia de pasaporte (foto o PDF)", "Foto del estudiante"],
          sistema: "Crear registro en BD tabla 'estudiantes', asignar ID único",
          tiempo: "1 día"
        },
        {
          numero: 2,
          titulo: "Evaluación Preliminar",
          queHace: "Analizar perfil y viabilidad del estudiante",
          accionAgencia: [
            "Verificar fondos económicos suficientes (mínimo IPREM × duración)",
            "Revisar nivel educativo (título secundaria completa)",
            "Evaluar probabilidad de aprobación usando IA predictor",
            "Informar al estudiante si es viable o no"
          ],
          documentos: ["Extractos bancarios preliminares (últimos 3 meses)", "Título de bachillerato (copia)"],
          sistema: "Cambiar estado a 'evaluacion', generar score de probabilidad",
          tiempo: "1-2 días"
        }
      ]
    },
    {
      id: 2,
      nombre: "FASE 2: SELECCIÓN DE UNIVERSIDAD",
      duracion: "Días 4-10",
      color: "#48bb78",
      pasos: [
        {
          numero: 3,
          titulo: "Asesoría Académica",
          queHace: "Reunión 1:1 (videollamada Zoom/Meet o presencial)",
          accionAgencia: [
            "Recomendar 3-5 universidades según perfil y presupuesto",
            "Explicar diferencias entre públicas y privadas",
            "Mostrar programas disponibles y requisitos",
            "Discutir ciudades y costo de vida"
          ],
          documentos: ["Catálogos de universidades", "Lista de costos de matrícula", "Comparativa de ciudades"],
          sistema: "Registrar en proceso_visa.paso_seleccion_universidad = true",
          tiempo: "2-3 días"
        },
        {
          numero: 4,
          titulo: "Solicitud a Universidad",
          queHace: "Aplicar a 2-3 universidades seleccionadas",
          accionAgencia: [
            "Generar carta de motivación automática (sistema)",
            "Generar formulario de solicitud pre-llenado (sistema)",
            "Revisar y personalizar documentos con estudiante",
            "Enviar aplicaciones por email o plataforma universitaria",
            "Registrar fechas de envío"
          ],
          documentos: [
            "✅ Carta de motivación (generada automáticamente)",
            "✅ Formulario de solicitud (generado automáticamente)",
            "Título de bachillerato apostillado",
            "Notas académicas traducidas al español",
            "Copia de pasaporte"
          ],
          sistema: "Marcar paso_solicitud_universidad = true, enviar emails automáticos",
          tiempo: "2-3 días",
          importante: true
        },
        {
          numero: 5,
          titulo: "Esperar Carta de Aceptación",
          queHace: "Universidad revisa solicitud y emite respuesta (7-30 días según universidad)",
          accionAgencia: [
            "Hacer seguimiento semanal con universidades por email",
            "Responder dudas adicionales de la universidad",
            "Si rechaza 1 universidad, aplicar a otra de respaldo",
            "Cuando llegue carta de aceptación, verificar datos correctos"
          ],
          documentos: ["📄 CARTA DE ACEPTACIÓN (la emite la universidad, NO la agencia)"],
          sistema: "Cuando llegue → Subir PDF a sistema, marcar paso_carta_aceptacion = true, notificar estudiante",
          tiempo: "7-30 días",
          importante: true
        }
      ]
    },
    {
      id: 3,
      nombre: "FASE 3: DOCUMENTACIÓN LEGAL",
      duracion: "Días 11-25",
      color: "#f6ad55",
      pasos: [
        {
          numero: 6,
          titulo: "Recolectar y Revisar Documentos del Estudiante",
          queHace: "Verificar que el estudiante suba TODOS los documentos necesarios",
          accionAgencia: [
            "✅ VERIFICAR que el estudiante haya subido estos 7 documentos en el sistema:",
            "1️⃣ PASAPORTE válido (mínimo 6 meses de vigencia)",
            "2️⃣ TÍTULO UNIVERSITARIO (original o copia certificada)",
            "3️⃣ NOTAS ACADÉMICAS completas (transcript oficial)",
            "4️⃣ CERTIFICADO MÉDICO reciente (máx 3 meses antigüedad)",
            "5️⃣ EXTRACTOS BANCARIOS (últimos 6 meses mostrando fondos)",
            "6️⃣ SEGURO MÉDICO INTERNACIONAL (póliza con cobertura 30,000€ mínimo)",
            "7️⃣ FOTO TIPO PASAPORTE (fondo blanco, reciente)",
            "",
            "🔴 IMPORTANTE: Revisar calidad de los documentos:",
            "• ¿Las fotos/PDFs son legibles?",
            "• ¿Los documentos están completos?",
            "• ¿Las fechas son válidas?",
            "• ¿Los nombres coinciden exactamente?",
            "",
            "📧 Si falta algo: Contactar al estudiante de inmediato",
            "✅ Si todo OK: Marcar como verificado en el sistema"
          ],
          documentos: [
            "📄 PASAPORTE (vigente +6 meses)",
            "🎓 TÍTULO UNIVERSITARIO",
            "📊 NOTAS ACADÉMICAS (transcript completo)",
            "🏥 CERTIFICADO MÉDICO (máx 3 meses antigüedad)",
            "💰 EXTRACTOS BANCARIOS (últimos 6 meses)",
            "🩺 SEGURO MÉDICO INTERNACIONAL (30,000€ cobertura)",
            "📸 FOTO TIPO PASAPORTE (fondo blanco)"
          ],
          sistema: "Verificar en Admin → Estudiantes → Ver Documentos que los 7 archivos estén subidos",
          tiempo: "1-2 días (depende del estudiante)",
          importante: true
        },
        {
          numero: 7,
          titulo: "Apostillar Documentos",
          queHace: "Legalizar documentos del país de origen ante La Haya",
          accionAgencia: [
            "Enviar checklist detallado de documentos a apostillar",
            "Explicar proceso de apostilla según país",
            "Recomendar gestorías confiables en país de origen",
            "Verificar que apostilla tenga sello oficial"
          ],
          documentos: [
            "Título universitario APOSTILLADO",
            "Notas académicas APOSTILLADAS",
            "Certificado de nacimiento APOSTILLADO",
            "Antecedentes penales APOSTILLADOS (TÚ lo sacas)"
          ],
          sistema: "Marcar paso_apostillado_documentos = true",
          tiempo: "5-10 días",
          importante: true
        },
        {
          numero: 8,
          titulo: "Traducción Jurada",
          queHace: "Traducir todos los documentos apostillados al español por traductor oficial",
          accionAgencia: [
            "Contactar traductor jurado certificado por España",
            "Enviar documentos apostillados al traductor",
            "Revisar que traducciones coincidan con originales",
            "Verificar sello y firma del traductor"
          ],
          documentos: ["Todos los apostillados traducidos por traductor jurado certificado"],
          sistema: "Marcar paso_traduccion_documentos = true",
          tiempo: "3-5 días"
        },
        {
          numero: 9,
          titulo: "Certificado Médico Oficial",
          queHace: "Examen médico oficial para visa (ADEMÁS del que subió el estudiante)",
          accionAgencia: [
            "Dar lista de clínicas autorizadas por consulado",
            "Explicar qué exámenes necesita (general, rayos X, sangre)",
            "Verificar que certificado incluya sello oficial y firma médico",
            "Nota: Esto es ADICIONAL al certificado que ya subió el estudiante"
          ],
          documentos: ["Certificado médico oficial del consulado (vigencia máxima 3 meses)"],
          sistema: "Marcar paso_certificado_medico = true",
          tiempo: "1-2 días"
        },
        {
          numero: 10,
          titulo: "Antecedentes Penales (TÚ los sacas)",
          queHace: "Solicitar certificado de antecedentes penales del país de origen",
          accionAgencia: [
            "🔴 LA AGENCIA saca este documento, NO el estudiante",
            "Guiar proceso según país (varía mucho)",
            "Verificar que sea reciente (máximo 90 días antigüedad)",
            "Confirmar que esté apostillado"
          ],
          documentos: ["Certificado de antecedentes penales apostillado (vigencia 90 días)"],
          sistema: "Marcar paso_antecedentes_penales = true",
          tiempo: "3-7 días"
        }
      ]
    },
    {
      id: 4,
      nombre: "FASE 4: SEGURO Y FONDOS",
      duracion: "Días 26-35",
      color: "#9f7aea",
      pasos: [
        {
          numero: 11,
          titulo: "Seguro Médico Internacional (Ya está subido)",
          queHace: "VERIFICAR que el estudiante subió el seguro médico internacional",
          accionAgencia: [
            "✅ El estudiante YA subió este documento en el paso 6",
            "Verificar que la póliza tenga:",
            "• Cobertura mínima 30,000€",
            "• Cubra repatriación",
            "• Vigencia desde fecha de entrada a España",
            "• Aseguradoras recomendadas: Asisa, Sanitas, DKV, Adeslas"
          ],
          documentos: ["Póliza de seguro médico (YA SUBIDA por el estudiante)"],
          sistema: "Marcar paso_seguro_medico = true, guardar número de póliza",
          tiempo: "1 día (solo verificación)",
          importante: true
        },
        {
          numero: 12,
          titulo: "Demostración de Fondos",
          queHace: "Preparar prueba de solvencia económica suficiente",
          accionAgencia: [
            "Calcular monto mínimo: IPREM (600€/mes) × duración estudios + matrícula",
            "Generar declaración jurada de fondos automáticamente (sistema)",
            "Si tiene patrocinador → Generar carta de patrocinio (sistema)",
            "Revisar extractos bancarios que ya subió el estudiante (paso 6)",
            "Verificar documentos de ingresos del patrocinador si aplica"
          ],
          documentos: [
            "Extractos bancarios (YA SUBIDOS en paso 6)",
            "✅ Declaración jurada de fondos (generada automáticamente)",
            "✅ Carta de patrocinio (si aplica, generada automáticamente)",
            "Certificados laborales y de ingresos del patrocinador",
            "Carta del banco confirmando saldo disponible"
          ],
          sistema: "Marcar paso_demostracion_fondos = true, guardar monto_fondos",
          tiempo: "3-5 días",
          importante: true
        }
      ]
    },
    {
      id: 5,
      nombre: "FASE 5: FORMULARIOS OFICIALES",
      duracion: "Días 36-40",
      color: "#ed64a6",
      pasos: [
        {
          numero: 13,
          titulo: "Formulario Nacional de Visado",
          queHace: "Llenar formulario oficial del consulado español",
          accionAgencia: [
            "Descargar formulario EX-00 del consulado español del país",
            "Ayudar a llenar cada campo correctamente (muy importante no errores)",
            "Revisar 3 veces que no haya errores ni tachones",
            "Imprimir en buena calidad",
            "Firmar en presencia del estudiante"
          ],
          documentos: ["Formulario EX-00 (Nacional) firmado y sin errores"],
          sistema: "Marcar paso_formulario_nacional = true",
          tiempo: "1 día",
          importante: true
        },
        {
          numero: 14,
          titulo: "Formulario Schengen (si aplica)",
          queHace: "Llenar formulario europeo de visa Schengen",
          accionAgencia: [
            "Verificar si país requiere este formulario adicional",
            "Descargar formulario oficial",
            "Llenar con datos idénticos al formulario nacional",
            "Firmar y fechar"
          ],
          documentos: ["Formulario Schengen firmado (si lo requiere el país)"],
          sistema: "Marcar paso_formulario_schengen = true",
          tiempo: "1 día"
        },
        {
          numero: 15,
          titulo: "Pago de Tasas Consulares",
          queHace: "Pagar tasas oficiales del consulado",
          accionAgencia: [
            "Informar monto exacto (varía por país: 60-160€ aprox)",
            "Dar datos bancarios oficiales del consulado",
            "Verificar que comprobante tenga sello o número de referencia",
            "Guardar copia del comprobante"
          ],
          documentos: ["Comprobante de pago de tasas consulares"],
          sistema: "Marcar paso_pago_tasa = true",
          tiempo: "1 día"
        }
      ]
    },
    {
      id: 6,
      nombre: "FASE 6: CITA EN CONSULADO",
      duracion: "Días 41-50",
      color: "#4299e1",
      pasos: [
        {
          numero: 16,
          titulo: "Agendar Cita en Consulado",
          queHace: "Sacar cita oficial en consulado español del país",
          accionAgencia: [
            "Explicar cómo usar sistema de citas online del consulado",
            "Intentar conseguir fecha lo más pronto posible (pueden tardar semanas)",
            "Si no hay citas, revisar diariamente por cancelaciones",
            "Confirmar cita por email"
          ],
          documentos: ["Confirmación de cita impresa (llevar el día de la cita)"],
          sistema: "Guardar fecha en tabla fecha_cita_embajada, marcar paso_agendamiento_cita = true, crear alerta",
          tiempo: "Inmediato pero cita puede ser en 2-8 semanas",
          importante: true
        },
        {
          numero: 17,
          titulo: "Preparación para Entrevista",
          queHace: "Ensayar respuestas a preguntas típicas del oficial consular",
          accionAgencia: [
            "Realizar simulación de entrevista (sistema tiene módulo IA)",
            "Dar tips de vestimenta: formal, pulcro",
            "Explicar importancia de puntualidad (llegar 30 min antes)",
            "Organizar documentos en folder transparente (orden lógico)",
            "Lista de preguntas frecuentes y cómo responderlas"
          ],
          documentos: ["Todos los documentos anteriores organizados en carpeta con separadores"],
          sistema: "Usar módulo ai/interview.py para simulación, marcar paso_preparacion_entrevista = true",
          tiempo: "2-3 días antes de cita"
        },
        {
          numero: 18,
          titulo: "Revisión Final de Expediente",
          queHace: "Verificar que absolutamente TODO esté completo y correcto",
          accionAgencia: [
            "Generar checklist automático de 30 puntos (sistema)",
            "Verificar vigencia de todos los documentos (médico <3 meses, antecedentes <90 días)",
            "Hacer copias completas de respaldo de todo",
            "Verificar que traducciones tengan sello del traductor",
            "Confirmar que extractos bancarios muestren fondos suficientes"
          ],
          documentos: ["Expediente completo en folder: originales + copias + checklist"],
          sistema: "Generar checklist con utils/checklist.py, marcar paso_revision_final = true",
          tiempo: "1 día antes de cita",
          importante: true
        },
        {
          numero: 19,
          titulo: "Asistir a Cita en Consulado",
          queHace: "Ir al consulado español en fecha y hora exacta",
          accionAgencia: [
            "Enviar recordatorio por email 24h antes",
            "Enviar mensaje WhatsApp en la mañana de la cita",
            "Estar disponible por WhatsApp durante la cita por si surge algo",
            "Llamar después para saber cómo fue"
          ],
          documentos: ["Llevar TODO: originales, copias, pasaporte, confirmación cita"],
          sistema: "Marcar paso_asistencia_cita = true",
          tiempo: "Día de la cita",
          importante: true
        }
      ]
    },
    {
      id: 7,
      nombre: "FASE 7: RESULTADO Y SEGUIMIENTO",
      duracion: "Días 51-90",
      color: "#38b2ac",
      pasos: [
        {
          numero: 20,
          titulo: "Entrevista Consular",
          queHace: "Oficial consular entrevista al estudiante (5-15 minutos típicamente)",
          accionAgencia: [
            "Llamar al estudiante después de la cita",
            "Preguntar qué le preguntaron y cómo respondió",
            "Registrar comentarios del oficial consular",
            "Evaluar probabilidad de aprobación según cómo fue"
          ],
          documentos: ["Ninguno, solo responder preguntas del oficial"],
          sistema: "Guardar en resultado_entrevista campo TEXT con detalles",
          tiempo: "5-15 minutos",
          importante: true
        },
        {
          numero: 21,
          titulo: "Entrega de Documentos",
          queHace: "Dejar expediente completo en consulado",
          accionAgencia: [
            "Confirmar que recibieron todos los documentos",
            "Anotar número de expediente que dan",
            "Preguntar tiempo estimado de respuesta",
            "Guardar recibo que entregan"
          ],
          documentos: ["Expediente completo se queda en consulado"],
          sistema: "Marcar paso_entrega_documentos = true, guardar numero_expediente",
          tiempo: "Mismo día de cita"
        },
        {
          numero: 22,
          titulo: "Período de Espera",
          queHace: "Esperar resolución del consulado (15-60 días típicamente)",
          accionAgencia: [
            "Consultar estado del expediente cada semana",
            "Mantener al estudiante informado",
            "Tranquilizar ansiedades (es normal que tarde)",
            "Si pasan 45 días, hacer seguimiento más activo"
          ],
          documentos: ["Ninguno, solo esperar"],
          sistema: "Marcar paso_espera_resolucion = true, crear alertas semanales",
          tiempo: "15-60 días (varía por país)"
        },
        {
          numero: 23,
          titulo: "Notificación de Resultado",
          queHace: "Consulado informa decisión final (aprobado/rechazado)",
          accionAgencia: [
            "SI APROBADO: Felicitar inmediatamente, pasar a Paso 24",
            "SI RECHAZADO: Analizar motivos del rechazo detalladamente",
            "SI RECHAZADO: Evaluar si procede apelar o rehacer solicitud",
            "SI RECHAZADO: Ofrecer análisis de qué falló para mejorar",
            "Actualizar estado en sistema inmediatamente"
          ],
          documentos: ["Carta de resolución oficial del consulado"],
          sistema: "Actualizar estado_procesamiento = 'aprobado' o 'rechazado', enviar notificación email automática",
          tiempo: "1 día",
          importante: true
        }
      ]
    },
    {
      id: 8,
      nombre: "FASE 8: VISA OTORGADA",
      duracion: "Días 91-100",
      color: "#48bb78",
      pasos: [
        {
          numero: 24,
          titulo: "Recoger Visa en Consulado",
          queHace: "Ir a consulado a recoger pasaporte con visa estampada",
          accionAgencia: [
            "Informar horarios de recogida del consulado",
            "Verificar que visa tenga todos los datos correctos (nombre, vigencia, tipo)",
            "Verificar fechas de entrada permitidas",
            "Hacer foto de la visa para respaldo",
            "Confirmar que pasaporte no tenga daños"
          ],
          documentos: ["Pasaporte con visa de estudiante estampada"],
          sistema: "Marcar paso_visa_otorgada = true, subir foto de visa al sistema",
          tiempo: "1 día",
          importante: true
        },
        {
          numero: 25,
          titulo: "Preparativos de Viaje a España",
          queHace: "Organizar viaje y llegada a España",
          accionAgencia: [
            "Ayudar a buscar vuelos en fechas permitidas por visa",
            "Coordinar alojamiento inicial en España (primera semana)",
            "Enviar guía de adaptación a España (cultura, transporte, etc)",
            "Activar código de estudiante en sistema para seguimiento",
            "Dar contactos de emergencia en España",
            "Explicar trámites al llegar: NIE, empadronamiento, tarjeta sanitaria"
          ],
          documentos: [
            "Boleto de avión confirmado",
            "Reserva de alojamiento (primera semana mínimo)",
            "Seguro médico vigente desde fecha de entrada",
            "Carta de aceptación universitaria",
            "Comprobante de fondos"
          ],
          sistema: "Marcar paso_preparativos_viaje = true, enviar email con Guía de Llegada PDF, crear alertas post-llegada",
          tiempo: "5-10 días antes de viaje",
          importante: true
        }
      ]
    }
  ]

  return (
    <div className="guia-proceso-container">
      <div className="guia-header">
        <h1>📋 GUÍA COMPLETA DEL PROCESO DE VISA</h1>
        <p className="guia-subtitle">De estudiante a visa aprobada: 24 pasos en 8 fases (~90-100 días)</p>
        <div className="guia-stats">
          <div className="stat-card">
            <span className="stat-number">8</span>
            <span className="stat-label">Fases</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">24</span>
            <span className="stat-label">Pasos</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">90-100</span>
            <span className="stat-label">Días</span>
          </div>
        </div>
      </div>

      <div className="fases-container">
        {fases.map((fase) => (
          <div key={fase.id} className="fase-card">
            <div 
              className="fase-header" 
              style={{ borderLeftColor: fase.color }}
              onClick={() => toggleFase(fase.id)}
            >
              <div className="fase-titulo-container">
                <h2 className="fase-titulo">{fase.nombre}</h2>
                <span className="fase-duracion">{fase.duracion}</span>
              </div>
              <button className="fase-toggle">
                {faseExpandida === fase.id ? '−' : '+'}
              </button>
            </div>

            {faseExpandida === fase.id && (
              <div className="fase-contenido">
                {fase.pasos.map((paso) => (
                  <div key={paso.numero} className={`paso-card ${paso.importante ? 'paso-importante' : ''}`}>
                    <div className="paso-header">
                      <div className="paso-numero-badge" style={{ backgroundColor: fase.color }}>
                        Paso {paso.numero}
                      </div>
                      <h3 className="paso-titulo">{paso.titulo}</h3>
                      {paso.importante && <span className="badge-importante">⭐ CRÍTICO</span>}
                      <span className="paso-tiempo">⏱️ {paso.tiempo}</span>
                    </div>

                    <div className="paso-contenido">
                      <div className="paso-seccion">
                        <h4 className="seccion-titulo">🎯 ¿Qué hace el estudiante?</h4>
                        <p className="seccion-texto">{paso.queHace}</p>
                      </div>

                      <div className="paso-seccion">
                        <h4 className="seccion-titulo">🏢 Acción de la agencia:</h4>
                        {Array.isArray(paso.accionAgencia) ? (
                          <ul className="lista-acciones">
                            {paso.accionAgencia.map((accion, idx) => (
                              <li key={idx}>{accion}</li>
                            ))}
                          </ul>
                        ) : (
                          <p className="seccion-texto">{paso.accionAgencia}</p>
                        )}
                      </div>

                      <div className="paso-seccion">
                        <h4 className="seccion-titulo">📄 Documentos necesarios:</h4>
                        <ul className="lista-documentos">
                          {paso.documentos.map((doc, idx) => (
                            <li key={idx} className={doc.includes('✅') ? 'doc-automatico' : ''}>
                              {doc}
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div className="paso-seccion">
                        <h4 className="seccion-titulo">💻 Registro en sistema:</h4>
                        <div className="sistema-badge">{paso.sistema}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="guia-resumen">
        <h2>📊 RESUMEN DE DOCUMENTOS</h2>
        
        <div className="resumen-grid">
          <div className="resumen-card">
            <h3>📤 Estudiante debe aportar:</h3>
            <ul>
              <li>Pasaporte vigente (mínimo 6 meses)</li>
              <li>Título de bachillerato apostillado</li>
              <li>Notas académicas apostilladas y traducidas</li>
              <li>Certificado de nacimiento apostillado</li>
              <li>Antecedentes penales apostillados</li>
              <li>Certificado médico oficial</li>
              <li>Extractos bancarios (últimos 6 meses)</li>
              <li>Fotos tamaño pasaporte (recientes)</li>
            </ul>
          </div>

          <div className="resumen-card automatico">
            <h3>✅ Agencia genera automáticamente:</h3>
            <ul>
              <li>✅ Carta de motivación personalizada</li>
              <li>✅ Formulario de solicitud pre-llenado</li>
              <li>✅ Declaración jurada de fondos</li>
              <li>✅ Carta de patrocinio (si aplica)</li>
            </ul>
          </div>

          <div className="resumen-card universidad">
            <h3>🏛️ Universidad emite:</h3>
            <ul>
              <li>Carta de aceptación oficial</li>
              <li>Certificado de matrícula (después de visa)</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="guia-notas">
        <h3>📝 Notas Importantes:</h3>
        <ul>
          <li><strong>Tiempos variables:</strong> Los plazos son estimados y pueden variar según país y época del año</li>
          <li><strong>Documentos vigentes:</strong> Verificar siempre fechas de vigencia (médico 3 meses, antecedentes 90 días)</li>
          <li><strong>Seguimiento activo:</strong> Contactar estudiante mínimo 1 vez por semana durante todo el proceso</li>
          <li><strong>Backup de documentos:</strong> Siempre hacer copias digitales de TODOS los documentos</li>
          <li><strong>Comunicación clara:</strong> Explicar cada paso al estudiante, no asumir que entiende</li>
        </ul>
      </div>
    </div>
  )
}

export default GuiaProceso
