import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './ProcesoVisa.css'

function ProcesoVisa({ estudianteId }) {
  const [proceso, setProceso] = useState(null)
  const [loading, setLoading] = useState(true)
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const fases = [
    {
      id: 1,
      nombre: 'INSCRIPCIÓN',
      icon: '📝',
      pasos: [
        { key: 'paso_inscripcion', nombre: 'Inscripción Completada', descripcion: 'Registro en plataforma y creación de perfil' },
        { key: 'paso_pago_inicial', nombre: 'Pago Inicial', descripcion: 'Pago de cuota de servicio de asesoría' },
        { key: 'paso_documentos_personales', nombre: 'Documentos Personales', descripcion: 'Pasaporte, títulos, expediente académico' }
      ]
    },
    {
      id: 2,
      nombre: 'UNIVERSIDAD',
      icon: '🎓',
      pasos: [
        { key: 'paso_seleccion_universidad', nombre: 'Selección de Universidad', descripcion: 'Elegir programa y universidad destino' },
        { key: 'paso_solicitud_universidad', nombre: 'Solicitud Enviada', descripcion: 'Aplicación enviada a la universidad' },
        { key: 'paso_carta_aceptacion', nombre: 'Carta de Aceptación', descripcion: 'Carta oficial recibida de la universidad' }
      ]
    },
    {
      id: 3,
      nombre: 'DOCUMENTOS LEGALES',
      icon: '📄',
      pasos: [
        { key: 'paso_antecedentes_solicitados', nombre: 'Antecedentes Solicitados', descripcion: 'Certificado de antecedentes penales solicitado' },
        { key: 'paso_antecedentes_recibidos', nombre: 'Antecedentes Recibidos', descripcion: 'Certificado recibido y verificado' },
        { key: 'paso_apostilla_haya', nombre: 'Apostilla de La Haya', descripcion: 'Documentos apostillados para validez internacional' },
        { key: 'paso_traduccion_documentos', nombre: 'Traducción Jurada', descripcion: 'Documentos traducidos al español por traductor oficial' }
      ]
    },
    {
      id: 4,
      nombre: 'SEGURO Y FONDOS',
      icon: '💰',
      pasos: [
        { key: 'paso_seguro_medico', nombre: 'Seguro Médico', descripcion: 'Seguro válido para Schengen (€30,000 mínimo)' },
        { key: 'paso_comprobante_fondos', nombre: 'Comprobante de Fondos', descripcion: 'Demostración de medios económicos (€6,000-8,000)' },
        { key: 'paso_carta_banco', nombre: 'Carta del Banco', descripcion: 'Carta oficial del banco certificando fondos' }
      ]
    },
    {
      id: 5,
      nombre: 'FORMULARIOS',
      icon: '📋',
      pasos: [
        { key: 'paso_formulario_visa', nombre: 'Formulario de Visa', descripcion: 'Formulario Nacional de Visado completado y firmado' },
        { key: 'paso_fotos_biometricas', nombre: 'Fotos Biométricas', descripcion: 'Fotografías tamaño pasaporte (fondo blanco)' },
        { key: 'paso_pago_tasa_visa', nombre: 'Pago Tasa Consular', descripcion: 'Pago de tasa de visa (€80-160)' }
      ]
    },
    {
      id: 6,
      nombre: 'CITA EMBAJADA',
      icon: '🏛️',
      pasos: [
        { key: 'paso_cita_agendada', nombre: 'Cita Agendada', descripcion: 'Fecha y hora de cita consular confirmada' },
        { key: 'paso_documentos_revisados', nombre: 'Documentos Revisados', descripcion: 'Verificación final de documentación completa' },
        { key: 'paso_simulacro_entrevista', nombre: 'Simulacro de Entrevista', descripcion: 'Preparación y práctica para entrevista consular' }
      ]
    },
    {
      id: 7,
      nombre: 'ENTREVISTA',
      icon: '🎤',
      pasos: [
        { key: 'paso_entrevista_completada', nombre: 'Entrevista Realizada', descripcion: 'Entrevista consular completada' }
      ]
    },
    {
      id: 8,
      nombre: 'VISA OTORGADA',
      icon: '✈️',
      pasos: [
        { key: 'paso_pasaporte_recogido', nombre: 'Pasaporte Recogido', descripcion: 'Pasaporte retirado del consulado' },
        { key: 'paso_visa_otorgada', nombre: '🎉 Visa Aprobada', descripcion: '¡Felicidades! Visa de estudiante otorgada' }
      ]
    }
  ]

  useEffect(() => {
    cargarProceso()
  }, [])

  const cargarProceso = async () => {
    try {
      const token = localStorage.getItem('token')
      const res = await axios.get(
        `${apiUrl}/api/estudiantes/${estudianteId}/proceso-visa`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setProceso(res.data)
    } catch (err) {
      console.error('Error cargando proceso:', err)
    } finally {
      setLoading(false)
    }
  }

  const calcularProgreso = () => {
    if (!proceso) return 0
    const totalPasos = fases.reduce((sum, fase) => sum + fase.pasos.length, 0)
    const pasosCompletados = fases.reduce((sum, fase) => {
      return sum + fase.pasos.filter(p => proceso[p.key] === true).length
    }, 0)
    return Math.round((pasosCompletados / totalPasos) * 100)
  }

  const obtenerFaseActual = () => {
    if (!proceso) return 1
    for (let i = 0; i < fases.length; i++) {
      const fase = fases[i]
      const todosCompletos = fase.pasos.every(p => proceso[p.key] === true)
      if (!todosCompletos) return fase.id
    }
    return fases.length
  }

  const formatearFecha = (fecha) => {
    if (!fecha) return null
    const d = new Date(fecha)
    return d.toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' })
  }

  if (loading) {
    return <div className="proceso-loading">⏳ Cargando proceso de visa...</div>
  }

  const progreso = calcularProgreso()
  const faseActual = obtenerFaseActual()

  return (
    <div className="proceso-visa-container">
      {/* Header con progreso */}
      <div className="proceso-header">
        <h2>📊 Tu Proceso de Visa de Estudiante</h2>
        <div className="progreso-principal">
          <div className="progreso-circle">
            <svg width="120" height="120">
              <circle cx="60" cy="60" r="50" fill="none" stroke="#e0e0e0" strokeWidth="8" />
              <circle 
                cx="60" 
                cy="60" 
                r="50" 
                fill="none" 
                stroke="#4CAF50" 
                strokeWidth="8"
                strokeDasharray={`${2 * Math.PI * 50}`}
                strokeDashoffset={`${2 * Math.PI * 50 * (1 - progreso / 100)}`}
                transform="rotate(-90 60 60)"
              />
            </svg>
            <div className="progreso-texto">
              <span className="progreso-numero">{progreso}%</span>
              <span className="progreso-label">Completo</span>
            </div>
          </div>
          <div className="progreso-info">
            <p><strong>Fase Actual:</strong> {fases[faseActual - 1]?.nombre}</p>
            <p className="fase-descripcion">{fases[faseActual - 1]?.icon} {fases[faseActual - 1]?.pasos[0]?.descripcion}</p>
          </div>
        </div>
      </div>

      {/* Timeline de fases */}
      <div className="fases-timeline">
        {fases.map((fase, index) => {
          const todosCompletos = fase.pasos.every(p => proceso[p.key] === true)
          const algunoCompleto = fase.pasos.some(p => proceso[p.key] === true)
          const esActual = fase.id === faseActual

          return (
            <div key={fase.id} className="fase-container">
              <div className={`fase-header ${todosCompletos ? 'completada' : algunoCompleto ? 'en-progreso' : ''} ${esActual ? 'actual' : ''}`}>
                <div className="fase-icon">{fase.icon}</div>
                <div className="fase-info">
                  <h3>Fase {fase.id}: {fase.nombre}</h3>
                  <div className="fase-progreso-mini">
                    {fase.pasos.filter(p => proceso[p.key]).length} / {fase.pasos.length} pasos
                  </div>
                </div>
                <div className="fase-status">
                  {todosCompletos ? '✅' : algunoCompleto ? '🔄' : '⏳'}
                </div>
              </div>

              {/* Pasos de la fase */}
              <div className="fase-pasos">
                {fase.pasos.map((paso) => {
                  const completado = proceso[paso.key] === true
                  const fechaKey = paso.key.replace('paso_', 'fecha_')
                  const fecha = proceso[fechaKey]

                  return (
                    <div key={paso.key} className={`paso-item ${completado ? 'paso-completado' : 'paso-pendiente'}`}>
                      <div className="paso-checkbox">
                        {completado ? (
                          <div className="checkbox-checked">✓</div>
                        ) : (
                          <div className="checkbox-unchecked"></div>
                        )}
                      </div>
                      <div className="paso-contenido">
                        <h4>{paso.nombre}</h4>
                        <p>{paso.descripcion}</p>
                        {completado && fecha && (
                          <span className="paso-fecha">✅ Completado: {formatearFecha(fecha)}</span>
                        )}
                        {!completado && (
                          <span className="paso-pendiente-label">⏳ Pendiente</span>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          )
        })}
      </div>

      {/* Información de cita si está agendada */}
      {proceso.paso_cita_agendada && proceso.fecha_cita_embajada && (
        <div className="cita-info-box">
          <h3>📅 Tu Cita en la Embajada</h3>
          <div className="cita-detalles">
            <div className="cita-fecha">
              <span className="cita-label">Fecha y Hora:</span>
              <span className="cita-valor">{new Date(proceso.fecha_cita_embajada).toLocaleString('es-ES', { 
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              })}</span>
            </div>
            <div className="cita-recordatorio">
              ⚠️ <strong>Recuerda:</strong> Llegar 15 minutos antes con TODOS los documentos originales
            </div>
          </div>
        </div>
      )}

      {/* Resultado de entrevista */}
      {proceso.resultado_entrevista && (
        <div className={`resultado-box resultado-${proceso.resultado_entrevista}`}>
          {proceso.resultado_entrevista === 'aprobada' && (
            <>
              <h3>🎉 ¡FELICIDADES!</h3>
              <p>Tu visa de estudiante ha sido APROBADA. Pronto podrás comenzar tu aventura en España.</p>
            </>
          )}
          {proceso.resultado_entrevista === 'rechazada' && (
            <>
              <h3>❌ Visa No Aprobada</h3>
              <p>Lamentablemente la visa no fue otorgada. Contacta con tu asesor para analizar opciones.</p>
            </>
          )}
          {proceso.resultado_entrevista === 'pendiente_documentos' && (
            <>
              <h3>📄 Documentos Adicionales Requeridos</h3>
              <p>El consulado solicita documentación adicional. Revisa tu email y sube los documentos lo antes posible.</p>
            </>
          )}
        </div>
      )}

      {/* Notas del administrador */}
      {proceso.notas_admin && (
        <div className="notas-admin-box">
          <h4>📝 Notas del Asesor</h4>
          <div className="notas-contenido">
            {proceso.notas_admin.split('\n\n').map((nota, i) => (
              <p key={i}>{nota}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ProcesoVisa
