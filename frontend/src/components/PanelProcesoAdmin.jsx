import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './PanelProcesoAdmin.css'

function PanelProcesoAdmin() {
  const [estudiantes, setEstudiantes] = useState([])
  const [estudianteSeleccionado, setEstudianteSeleccionado] = useState(null)
  const [proceso, setProceso] = useState(null)
  const [loading, setLoading] = useState(true)
  const [guardando, setGuardando] = useState(false)
  const [notas, setNotas] = useState('')
  const [fechaCita, setFechaCita] = useState('')
  const [resultadoEntrevista, setResultadoEntrevista] = useState('')

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const fases = [
    {
      id: 1,
      nombre: 'INSCRIPCIÓN',
      icon: '📝',
      pasos: [
        { key: 'paso_inscripcion', nombre: 'Inscripción Completada' },
        { key: 'paso_pago_inicial', nombre: 'Pago Inicial' },
        { key: 'paso_documentos_personales', nombre: 'Documentos Personales' }
      ]
    },
    {
      id: 2,
      nombre: 'UNIVERSIDAD',
      icon: '🎓',
      pasos: [
        { key: 'paso_seleccion_universidad', nombre: 'Selección de Universidad' },
        { key: 'paso_solicitud_universidad', nombre: 'Solicitud Enviada' },
        { key: 'paso_carta_aceptacion', nombre: 'Carta de Aceptación' }
      ]
    },
    {
      id: 3,
      nombre: 'DOCUMENTOS LEGALES',
      icon: '📄',
      pasos: [
        { key: 'paso_antecedentes_solicitados', nombre: 'Antecedentes Solicitados' },
        { key: 'paso_antecedentes_recibidos', nombre: 'Antecedentes Recibidos' },
        { key: 'paso_apostilla_haya', nombre: 'Apostilla de La Haya' },
        { key: 'paso_traduccion_documentos', nombre: 'Traducción Jurada' }
      ]
    },
    {
      id: 4,
      nombre: 'SEGURO Y FONDOS',
      icon: '💰',
      pasos: [
        { key: 'paso_seguro_medico', nombre: 'Seguro Médico' },
        { key: 'paso_comprobante_fondos', nombre: 'Comprobante de Fondos' },
        { key: 'paso_carta_banco', nombre: 'Carta del Banco' }
      ]
    },
    {
      id: 5,
      nombre: 'FORMULARIOS',
      icon: '📋',
      pasos: [
        { key: 'paso_formulario_visa', nombre: 'Formulario de Visa' },
        { key: 'paso_fotos_biometricas', nombre: 'Fotos Biométricas' },
        { key: 'paso_pago_tasa_visa', nombre: 'Pago Tasa Consular' }
      ]
    },
    {
      id: 6,
      nombre: 'CITA EMBAJADA',
      icon: '🏛️',
      pasos: [
        { key: 'paso_cita_agendada', nombre: 'Cita Agendada' },
        { key: 'paso_documentos_revisados', nombre: 'Documentos Revisados' },
        { key: 'paso_simulacro_entrevista', nombre: 'Simulacro de Entrevista' }
      ]
    },
    {
      id: 7,
      nombre: 'ENTREVISTA',
      icon: '🎤',
      pasos: [
        { key: 'paso_entrevista_completada', nombre: 'Entrevista Realizada' }
      ]
    },
    {
      id: 8,
      nombre: 'VISA OTORGADA',
      icon: '✈️',
      pasos: [
        { key: 'paso_pasaporte_recogido', nombre: 'Pasaporte Recogido' },
        { key: 'paso_visa_otorgada', nombre: 'Visa Aprobada' }
      ]
    }
  ]

  useEffect(() => {
    cargarEstudiantes()
  }, [])

  const cargarEstudiantes = async () => {
    try {
      const token = localStorage.getItem('token')
      const res = await axios.get(`${apiUrl}/api/admin/estudiantes`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setEstudiantes(res.data.estudiantes || [])
    } catch (err) {
      console.error('Error cargando estudiantes:', err)
    } finally {
      setLoading(false)
    }
  }

  const cargarProceso = async (estudianteId) => {
    try {
      const token = localStorage.getItem('token')
      const res = await axios.get(
        `${apiUrl}/api/estudiantes/${estudianteId}/proceso-visa`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setProceso(res.data)
      if (res.data.fecha_cita_embajada) {
        setFechaCita(res.data.fecha_cita_embajada.split('T')[0])
      }
      if (res.data.resultado_entrevista) {
        setResultadoEntrevista(res.data.resultado_entrevista)
      }
    } catch (err) {
      console.error('Error cargando proceso:', err)
    }
  }

  const seleccionarEstudiante = (estudiante) => {
    setEstudianteSeleccionado(estudiante)
    cargarProceso(estudiante.id)
  }

  const togglePaso = async (pasoKey, valorActual) => {
    if (!estudianteSeleccionado) return
    
    setGuardando(true)
    try {
      const token = localStorage.getItem('token')
      const data = {
        paso: pasoKey,
        completado: !valorActual
      }

      // Añadir fecha de cita si es paso_cita_agendada
      if (pasoKey === 'paso_cita_agendada' && fechaCita) {
        data.fecha_cita = fechaCita
      }

      // Añadir resultado si es paso_entrevista_completada
      if (pasoKey === 'paso_entrevista_completada' && resultadoEntrevista) {
        data.resultado = resultadoEntrevista
      }

      // Añadir notas si existen
      if (notas.trim()) {
        data.notas = notas
      }

      await axios.put(
        `${apiUrl}/api/admin/estudiantes/${estudianteSeleccionado.id}/proceso-visa`,
        data,
        { headers: { Authorization: `Bearer ${token}` } }
      )

      // Recargar proceso
      await cargarProceso(estudianteSeleccionado.id)
      setNotas('')
      alert('✅ Paso actualizado')
    } catch (err) {
      alert('❌ Error actualizando paso')
      console.error(err)
    } finally {
      setGuardando(false)
    }
  }

  const calcularProgreso = (estudianteId) => {
    // Aquí podrías hacer una llamada para obtener el proceso del estudiante
    // Por ahora retornamos un placeholder
    return 0
  }

  const formatearFecha = (fecha) => {
    if (!fecha) return 'N/A'
    return new Date(fecha).toLocaleDateString('es-ES', { 
      day: '2-digit', 
      month: 'short', 
      year: 'numeric' 
    })
  }

  if (loading) {
    return <div className="admin-loading">⏳ Cargando estudiantes...</div>
  }

  return (
    <div className="panel-proceso-admin">
      <div className="admin-header">
        <h1>📊 Panel de Seguimiento de Proceso de Visa</h1>
        <p>Administra el proceso completo de cada estudiante desde inscripción hasta visa otorgada</p>
      </div>

      <div className="admin-layout">
        {/* Lista de estudiantes */}
        <div className="estudiantes-sidebar">
          <h3>📋 Estudiantes ({estudiantes.length})</h3>
          <div className="estudiantes-lista">
            {estudiantes.map(est => (
              <div
                key={est.id}
                className={`estudiante-card ${estudianteSeleccionado?.id === est.id ? 'activo' : ''}`}
                onClick={() => seleccionarEstudiante(est)}
              >
                <div className="estudiante-info">
                  <div className="estudiante-nombre">{est.nombre}</div>
                  <div className="estudiante-email">{est.email}</div>
                  <div className="estudiante-estado">{est.estado || 'En proceso'}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Panel de proceso del estudiante seleccionado */}
        <div className="proceso-panel">
          {!estudianteSeleccionado ? (
            <div className="no-seleccionado">
              <h3>👈 Selecciona un estudiante para ver su proceso</h3>
            </div>
          ) : !proceso ? (
            <div className="cargando-proceso">⏳ Cargando proceso...</div>
          ) : (
            <>
              <div className="proceso-estudiante-header">
                <h2>{estudianteSeleccionado.nombre}</h2>
                <p>{estudianteSeleccionado.email}</p>
                <div className="progreso-badge">
                  {(() => {
                    const totalPasos = fases.reduce((sum, fase) => sum + fase.pasos.length, 0)
                    const completados = fases.reduce((sum, fase) => {
                      return sum + fase.pasos.filter(p => proceso[p.key] === true).length
                    }, 0)
                    const porcentaje = Math.round((completados / totalPasos) * 100)
                    return `${porcentaje}% Completado (${completados}/${totalPasos} pasos)`
                  })()}
                </div>
              </div>

              {/* Campo de notas globales */}
              <div className="notas-section">
                <label>📝 Añadir Nota:</label>
                <textarea
                  value={notas}
                  onChange={(e) => setNotas(e.target.value)}
                  placeholder="Escribe una nota que se guardará al marcar el próximo paso..."
                  rows="3"
                />
              </div>

              {/* Fases y pasos */}
              {fases.map(fase => (
                <div key={fase.id} className="fase-admin">
                  <div className="fase-admin-header">
                    <span className="fase-icon">{fase.icon}</span>
                    <h3>Fase {fase.id}: {fase.nombre}</h3>
                    <span className="fase-progreso">
                      {fase.pasos.filter(p => proceso[p.key]).length}/{fase.pasos.length}
                    </span>
                  </div>

                  <div className="pasos-admin">
                    {fase.pasos.map(paso => {
                      const completado = proceso[paso.key] === true
                      const fechaKey = paso.key.replace('paso_', 'fecha_')
                      const fecha = proceso[fechaKey]

                      return (
                        <div key={paso.key} className="paso-admin">
                          <label className="paso-checkbox-label">
                            <input
                              type="checkbox"
                              checked={completado}
                              onChange={() => togglePaso(paso.key, completado)}
                              disabled={guardando}
                            />
                            <span className="checkbox-custom"></span>
                            <div className="paso-info">
                              <span className="paso-nombre">{paso.nombre}</span>
                              {completado && fecha && (
                                <span className="paso-fecha-admin">
                                  ✅ {formatearFecha(fecha)}
                                </span>
                              )}
                            </div>
                          </label>

                          {/* Campo especial para cita de embajada */}
                          {paso.key === 'paso_cita_agendada' && (
                            <div className="campo-extra">
                              <label>📅 Fecha de la cita:</label>
                              <input
                                type="datetime-local"
                                value={fechaCita}
                                onChange={(e) => setFechaCita(e.target.value)}
                              />
                            </div>
                          )}

                          {/* Campo especial para resultado de entrevista */}
                          {paso.key === 'paso_entrevista_completada' && (
                            <div className="campo-extra">
                              <label>📋 Resultado:</label>
                              <select
                                value={resultadoEntrevista}
                                onChange={(e) => setResultadoEntrevista(e.target.value)}
                              >
                                <option value="">Seleccionar...</option>
                                <option value="aprobada">✅ Aprobada</option>
                                <option value="rechazada">❌ Rechazada</option>
                                <option value="pendiente_documentos">📄 Pendiente Documentos</option>
                              </select>
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                </div>
              ))}

              {/* Notas históricas */}
              {proceso.notas_admin && (
                <div className="historial-notas">
                  <h3>📝 Historial de Notas</h3>
                  <div className="notas-lista">
                    {proceso.notas_admin.split('\n\n').map((nota, i) => (
                      <div key={i} className="nota-item">{nota}</div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default PanelProcesoAdmin
