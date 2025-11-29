import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './ProcesoVisa.css'

function ProcesoVisa({ estudianteId }) {
  const [proceso, setProceso] = useState(null)
  const [servicios, setServicios] = useState([])
  const [loading, setLoading] = useState(true)
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  // Mapeo de servicios a fases del proceso
  const mapeoServiciosFases = {
    'Búsqueda de Universidad': [1, 2], // Inscripción y Universidad
    'Gestión de Matrícula': [2], // Universidad
    'Asesoría de Visa': [3, 4, 5, 6, 7, 8], // Todas las fases de visa
    'Traducción de Documentos': [3], // Documentos Legales
    'Apostilla de Documentos': [3], // Documentos Legales
    'Seguro Médico': [4], // Seguro y Fondos
    'Búsqueda de Alojamiento': [1], // Solo inscripción
    'Gestión de Documentos': [3], // Documentos Legales
    'Preparación para Entrevista': [6, 7], // Cita y Entrevista
    'Seguimiento Post-Visa': [8] // Visa Otorgada
  }

  const obtenerFasesRelevantes = () => {
    if (servicios.length === 0) {
      // Si no hay servicios, mostrar todas las fases
      return [1, 2, 3, 4, 5, 6, 7, 8]
    }
    
    const fasesSet = new Set()
    servicios.forEach(servicio => {
      const fases = mapeoServiciosFases[servicio] || [1, 2, 3, 4, 5, 6, 7, 8]
      fases.forEach(fase => fasesSet.add(fase))
    })
    
    return Array.from(fasesSet).sort((a, b) => a - b)
  }

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
        { key: 'fecha_cita_embajada', nombre: 'Fecha Confirmada', descripcion: 'Día y hora específicos de tu cita en embajada', esFecha: true },
        { key: 'paso_documentos_revisados', nombre: 'Documentos Revisados', descripcion: 'Verificación final de documentación completa' },
        { key: 'paso_simulacro_entrevista', nombre: 'Simulacro de Entrevista', descripcion: 'Preparación y práctica para entrevista consular' }
      ]
    },
    {
      id: 7,
      nombre: 'ENTREVISTA',
      icon: '🎤',
      pasos: [
        { key: 'paso_entrevista_completada', nombre: 'Entrevista Realizada', descripcion: 'Entrevista consular completada' },
        { key: 'resultado_entrevista', nombre: 'Resultado', descripcion: 'Resultado oficial de la entrevista consular', esResultado: true }
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
    cargarServicios()
  }, [])

  const cargarProceso = async () => {
    try {
      const res = await axios.get(
        `${apiUrl}/api/estudiantes/${estudianteId}/proceso-visa`
      )
      console.log('Proceso cargado:', res.data)
      setProceso(res.data || {})
    } catch (err) {
      console.error('Error cargando proceso:', err)
      console.error('Detalles del error:', err.response?.data)
      // Establecer proceso vacío para evitar pantalla en blanco
      setProceso({})
    } finally {
      setLoading(false)
    }
  }

  const cargarServicios = async () => {
    try {
      const codigo = localStorage.getItem('codigo_acceso')
      const res = await axios.get(
        `${apiUrl}/api/presupuestos/estudiante/${estudianteId}?codigo_acceso=${codigo}`
      )
      // Filtrar presupuestos aceptados y obtener servicios
      const aceptados = res.data.filter(p => p.estado === 'aceptado')
      if (aceptados.length > 0 && aceptados[0].servicios_solicitados) {
        setServicios(aceptados[0].servicios_solicitados)
      }
    } catch (err) {
      console.error('Error cargando servicios:', err)
    }
  }

  const calcularProgreso = () => {
    if (!proceso) return 0
    const fasesRelevantes = obtenerFasesRelevantes()
    const fasesFiltradasData = fases.filter(f => fasesRelevantes.includes(f.id))
    const totalPasos = fasesFiltradasData.reduce((sum, fase) => sum + fase.pasos.length, 0)
    const pasosCompletados = fasesFiltradasData.reduce((sum, fase) => {
      return sum + fase.pasos.filter(p => proceso[p.key] === true).length
    }, 0)
    return totalPasos > 0 ? Math.round((pasosCompletados / totalPasos) * 100) : 0
  }

  const obtenerFaseActual = () => {
    if (!proceso) return 1
    const fasesRelevantes = obtenerFasesRelevantes()
    const fasesFiltradasData = fases.filter(f => fasesRelevantes.includes(f.id))
    
    for (let i = 0; i < fasesFiltradasData.length; i++) {
      const fase = fasesFiltradasData[i]
      const todosCompletos = fase.pasos.every(p => proceso[p.key] === true)
      if (!todosCompletos) return fase.id
    }
    return fasesFiltradasData.length > 0 ? fasesFiltradasData[fasesFiltradasData.length - 1].id : 1
  }

  const formatearFecha = (fecha) => {
    if (!fecha) return null
    const d = new Date(fecha)
    return d.toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' })
  }

  if (loading) {
    return <div className="proceso-loading">⏳ Cargando proceso de visa...</div>
  }

  if (!proceso) {
    return (
      <div className="proceso-error">
        <h3>⚠️ No se pudo cargar el proceso</h3>
        <p>Intenta recargar la página</p>
        <button onClick={cargarProceso}>🔄 Reintentar</button>
      </div>
    )
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

      {/* Servicios contratados */}
      {servicios.length > 0 && (
        <div style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          padding: '20px',
          borderRadius: '12px',
          marginBottom: '30px',
          boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ 
            color: 'white', 
            margin: '0 0 15px 0',
            fontSize: '18px',
            fontWeight: '600',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <span style={{fontSize: '24px'}}>💼</span>
            Tus Servicios Contratados
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '10px' }}>
            {servicios.map((servicio, idx) => (
              <div key={idx} style={{
                background: 'rgba(255,255,255,0.95)',
                padding: '12px 16px',
                borderRadius: '8px',
                color: '#2d3748',
                fontSize: '14px',
                fontWeight: '500',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
              }}>
                <span style={{ 
                  fontSize: '18px',
                  minWidth: '24px'
                }}>✅</span>
                <span>{servicio}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Timeline de fases */}
      <div className="fases-timeline">
        {fases.filter(fase => obtenerFasesRelevantes().includes(fase.id)).map((fase, index) => {
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
                  // Manejo especial para campos que no son booleanos
                  let completado = false
                  let valorMostrar = null
                  
                  if (paso.esFecha) {
                    // Es un campo de fecha
                    completado = !!proceso[paso.key]
                    valorMostrar = proceso[paso.key] ? formatearFecha(proceso[paso.key]) : null
                  } else if (paso.esResultado) {
                    // Es el resultado de entrevista
                    completado = !!proceso[paso.key]
                    valorMostrar = proceso[paso.key]
                  } else {
                    // Es un campo booleano normal
                    completado = proceso[paso.key] === true
                  }
                  
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
                        {completado && paso.esFecha && valorMostrar && (
                          <span className="paso-fecha">📅 {formatearFecha(valorMostrar)}</span>
                        )}
                        {completado && paso.esResultado && valorMostrar && (
                          <span className={`paso-resultado resultado-${valorMostrar}`}>
                            {valorMostrar === 'aprobada' && '✅ Aprobada'}
                            {valorMostrar === 'rechazada' && '❌ No Aprobada'}
                            {valorMostrar === 'pendiente_documentos' && '📄 Docs. Adicionales'}
                          </span>
                        )}
                        {completado && !paso.esFecha && !paso.esResultado && fecha && (
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
