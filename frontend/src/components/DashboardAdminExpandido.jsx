import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import './DashboardAdminExpandido.css'
import PartnersAdmin from './PartnersAdmin'
import AlertasAdmin from './AlertasAdmin'

function DashboardAdminExpandido({ onLogout }) {
  const [activeTab, setActiveTab] = useState('estudiantes')
  const [estudiantes, setEstudiantes] = useState([])
  const [documentosGenerados, setDocumentosGenerados] = useState([])
  const [cursos, setCursos] = useState([])
  const [alojamientos, setAlojamientos] = useState([])
  const [estadisticas, setEstadisticas] = useState(null)
  const [reporteEstudiantes, setReporteEstudiantes] = useState(null)
  const [alertasDocumentos, setAlertasDocumentos] = useState([])
  const [mostrarAlertas, setMostrarAlertas] = useState(false)
  const [loading, setLoading] = useState(true)
  const [filtro, setFiltro] = useState('todos')
  const [busqueda, setBusqueda] = useState('')
  const [motivoRechazo, setMotivoRechazo] = useState('')
  const [estudianteSeleccionado, setEstudianteSeleccionado] = useState(null)
  const [generandoDocs, setGenerandoDocs] = useState(false)
  const [showAddCursoModal, setShowAddCursoModal] = useState(false)
  const [showAddAlojamientoModal, setShowAddAlojamientoModal] = useState(false)
  const [showCursosSugeridosModal, setShowCursosSugeridosModal] = useState(false)
  const [cursosSugeridos, setCursosSugeridos] = useState([])
  const [estudianteParaCurso, setEstudianteParaCurso] = useState(null)
  const [nuevoCurso, setNuevoCurso] = useState({ nombre: '', descripcion: '', duracion_meses: 6, precio_eur: 0, ciudad: '', nivel_espanol_requerido: '', cupos_disponibles: 0 })
  const [nuevoAlojamiento, setNuevoAlojamiento] = useState({ tipo: '', direccion: '', ciudad: '', precio_mensual_eur: 0, capacidad: 1, disponible: true, descripcion: '', servicios: '' })
  const [showMensajeModal, setShowMensajeModal] = useState(false)
  const [estudianteParaMensaje, setEstudianteParaMensaje] = useState(null)
  const [nuevoMensaje, setNuevoMensaje] = useState({ asunto: '', tipo: 'informacion', mensaje: '', documento_solicitado: '' })
  const [enviandoMensaje, setEnviandoMensaje] = useState(false)
  const [showModalGenerarDocs, setShowModalGenerarDocs] = useState(false)
  const [estudiantesAprobados, setEstudiantesAprobados] = useState([])
  const navigate = useNavigate()

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    cargarDatos()
  }, [activeTab])

  const cargarDatos = async () => {
    setLoading(true)
    try {
      if (activeTab === 'estudiantes') {
        const [estRes, statsRes] = await Promise.all([
          axios.get(`${apiUrl}/api/admin/estudiantes`),
          axios.get(`${apiUrl}/api/admin/estadisticas`)
        ])
        setEstudiantes(estRes.data)
        setEstadisticas(statsRes.data)
        
        // Cargar alertas de documentos
        try {
          const alertasRes = await axios.get(`${apiUrl}/api/admin/alertas-documentos`)
          setAlertasDocumentos(alertasRes.data.alertas || [])
        } catch (err) {
          console.error('Error cargando alertas:', err)
        }
      } else if (activeTab === 'documentos') {
        const docsRes = await axios.get(`${apiUrl}/api/admin/documentos-generados`)
        setDocumentosGenerados(docsRes.data)
      } else if (activeTab === 'cursos') {
        const cursosRes = await axios.get(`${apiUrl}/api/admin/cursos`)
        setCursos(cursosRes.data)
      } else if (activeTab === 'alojamientos') {
        const alojRes = await axios.get(`${apiUrl}/api/admin/alojamientos`)
        setAlojamientos(alojRes.data)
      } else if (activeTab === 'reportes') {
        const reporteRes = await axios.get(`${apiUrl}/api/admin/reportes/estudiantes`)
        setReporteEstudiantes(reporteRes.data)
      }
    } catch (err) {
      console.error('Error:', err)
      if (err.response?.status === 401) {
        handleLogout()
      }
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('usuario')
    delete axios.defaults.headers.common['Authorization']
    onLogout()
    navigate('/admin/login')
  }

  const aprobarEstudiante = async (id) => {
    // Primero mostrar cursos sugeridos
    try {
      const res = await axios.get(`${apiUrl}/api/admin/estudiantes/${id}/sugerir-cursos`)
      setCursosSugeridos(res.data.cursos_sugeridos)
      setEstudianteParaCurso(id)
      setShowCursosSugeridosModal(true)
    } catch (err) {
      // Si no hay cursos o falla, aprobar directamente
      if (confirm('¿Está seguro de aprobar este estudiante sin asignar curso?')) {
        try {
          await axios.post(`${apiUrl}/api/admin/estudiantes/${id}/aprobar`)
          alert('Estudiante aprobado correctamente')
          cargarDatos()
        } catch (err2) {
          alert('Error: ' + (err2.response?.data?.detail || err2.message))
        }
      }
    }
  }

  const aprobarConCurso = async (cursoId = null) => {
    try {
      // Asignar curso si fue seleccionado
      if (cursoId) {
        await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteParaCurso}/asignar-curso`, null, {
          params: { curso_id: cursoId }
        })
      }
      
      // Aprobar estudiante
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteParaCurso}/aprobar`)
      
      alert('Estudiante aprobado' + (cursoId ? ' y curso asignado' : ''))
      setShowCursosSugeridosModal(false)
      setCursosSugeridos([])
      setEstudianteParaCurso(null)
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const rechazarEstudiante = async (id) => {
    setEstudianteSeleccionado(id)
  }

  const confirmarRechazo = async () => {
    if (!motivoRechazo.trim()) {
      alert('Por favor ingrese un motivo de rechazo')
      return
    }

    try {
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteSeleccionado}/rechazar`, {
        motivo: motivoRechazo
      })
      alert('Estudiante rechazado')
      setEstudianteSeleccionado(null)
      setMotivoRechazo('')
      cargarDatos()
    } catch (err) {
      alert('Error al rechazar estudiante: ' + (err.response?.data?.detail || err.message))
    }
  }

  const estudiantesFiltrados = estudiantes.filter(est => {
    // Normalizar estado (puede venir como 'estado' o 'estado_procesamiento')
    const estadoActual = est.estado || est.estado_procesamiento || 'pendiente'
    const cumpleFiltro = filtro === 'todos' || estadoActual === filtro
    const cumpleBusqueda = !busqueda || 
      est.nombre?.toLowerCase().includes(busqueda.toLowerCase()) ||
      est.nombre_completo?.toLowerCase().includes(busqueda.toLowerCase()) ||
      est.email?.toLowerCase().includes(busqueda.toLowerCase()) ||
      est.especialidad?.toLowerCase().includes(busqueda.toLowerCase()) ||
      est.especialidad_interes?.toLowerCase().includes(busqueda.toLowerCase())
    
    return cumpleFiltro && cumpleBusqueda
  })

  const generarDocumentos = async (estudianteId) => {
    if (!confirm('¿Generar todos los documentos oficiales para este estudiante?')) return
    
    setGenerandoDocs(true)
    try {
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteId}/generar-documentos`, {
        tipos_documentos: ['carta_aceptacion', 'carta_motivacion', 'formulario_solicitud', 'certificado_matricula']
      })
      alert('✅ Documentos generados correctamente')
      setShowModalGenerarDocs(false)
      setActiveTab('documentos')
      cargarDatos()
    } catch (err) {
      alert('Error al generar documentos: ' + (err.response?.data?.detail || err.message))
    } finally {
      setGenerandoDocs(false)
    }
  }

  const abrirModalGenerarDocs = () => {
    // Filtrar solo estudiantes aprobados
    const aprobados = estudiantes.filter(est => 
      est.estado === 'aprobado' || 
      est.estado === 'aprobado_admin' ||
      est.estado_procesamiento === 'aprobado'
    )
    setEstudiantesAprobados(aprobados)
    setShowModalGenerarDocs(true)
  }

  const aprobarDocumento = async (docId) => {
    if (!confirm('¿Aprobar este documento y enviarlo al estudiante?')) return
    
    try {
      await axios.put(`${apiUrl}/api/admin/documentos-generados/${docId}/aprobar`, {
        enviar_a_estudiante: true
      })
      alert('Documento aprobado y enviado')
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const descargarDocumento = (docId) => {
    window.open(`${apiUrl}/api/admin/documentos-generados/${docId}/descargar`, '_blank')
  }

  const abrirModalMensaje = (estudiante) => {
    setEstudianteParaMensaje(estudiante)
    setNuevoMensaje({ 
      asunto: `Mensaje para ${estudiante.nombre || estudiante.nombre_completo}`, 
      tipo: 'informacion', 
      mensaje: '', 
      documento_solicitado: '' 
    })
    setShowMensajeModal(true)
  }

  const enviarMensaje = async () => {
    if (!nuevoMensaje.mensaje.trim()) {
      alert('El mensaje no puede estar vacío')
      return
    }

    setEnviandoMensaje(true)
    try {
      const response = await axios.post(
        `${apiUrl}/api/admin/estudiantes/${estudianteParaMensaje.id}/enviar-mensaje`,
        nuevoMensaje
      )
      
      alert(`✅ Mensaje enviado correctamente${response.data.email_enviado ? ' y notificación por email enviada' : ''}`)
      setShowMensajeModal(false)
      setEstudianteParaMensaje(null)
      setNuevoMensaje({ asunto: '', tipo: 'informacion', mensaje: '', documento_solicitado: '' })
    } catch (err) {
      alert('Error al enviar mensaje: ' + (err.response?.data?.detail || err.message))
    } finally {
      setEnviandoMensaje(false)
    }
  }

  const crearCurso = async () => {
    try {
      await axios.post(`${apiUrl}/api/admin/cursos`, nuevoCurso)
      alert('Curso creado correctamente')
      setShowAddCursoModal(false)
      setNuevoCurso({ nombre: '', descripcion: '', duracion_meses: 6, precio_eur: 0, ciudad: '', nivel_espanol_requerido: '', cupos_disponibles: 0 })
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const crearAlojamiento = async () => {
    try {
      await axios.post(`${apiUrl}/api/admin/alojamientos`, nuevoAlojamiento)
      alert('Alojamiento creado correctamente')
      setShowAddAlojamientoModal(false)
      setNuevoAlojamiento({ tipo: '', direccion: '', ciudad: '', precio_mensual_eur: 0, capacidad: 1, disponible: true, descripcion: '', servicios: '' })
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const asignarCurso = async (estudianteId, cursoId) => {
    try {
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteId}/asignar-curso`, null, {
        params: { curso_id: cursoId }
      })
      alert('Curso asignado correctamente')
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const asignarAlojamiento = async (estudianteId, alojamientoId) => {
    try {
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteId}/asignar-alojamiento`, null, {
        params: { alojamiento_id: alojamientoId }
      })
      alert('Alojamiento asignado correctamente')
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const enviarRecordatorios = async () => {
    if (!confirm('¿Enviar recordatorios a todos los estudiantes con documentos pendientes?')) return
    
    try {
      const res = await axios.post(`${apiUrl}/api/admin/enviar-recordatorios`)
      alert(res.data.mensaje)
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const actualizarEstadoEstudiante = async (estudianteId, nuevoEstado) => {
    try {
      await axios.put(`${apiUrl}/api/admin/estudiantes/${estudianteId}/actualizar-estado`, null, {
        params: { nuevo_estado: nuevoEstado }
      })
      alert('Estado actualizado correctamente')
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const sincronizarCursosEscuelas = async () => {
    if (!confirm('¿Sincronizar cursos desde APIs de escuelas? Esto actualizará precios y disponibilidad.')) return
    
    setLoading(true)
    try {
      const res = await axios.get(`${apiUrl}/api/admin/sincronizar-cursos-escuelas`)
      alert(`✅ Sincronización completada!\n\n` +
            `📚 Cursos encontrados: ${res.data.cursos_encontrados}\n` +
            `➕ Cursos nuevos insertados: ${res.data.cursos_insertados}\n` +
            `🔄 Cursos actualizados: ${res.data.cursos_actualizados}`)
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    } finally {
      setLoading(false)
    }
  }

  const verificarDisponibilidadCurso = async (cursoId) => {
    try {
      const res = await axios.get(`${apiUrl}/api/cursos/${cursoId}/verificar-disponibilidad`)
      alert(`Disponibilidad verificada:\n\n` +
            `📚 ${res.data.nombre}\n` +
            `🎫 Cupos disponibles: ${res.data.cupos_disponibles}\n` +
            `${res.data.disponible ? '✅ Curso disponible' : '❌ Sin cupos'}`)
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  if (loading) {
    return <div className="loading">Cargando...</div>
  }

  return (
    <div className="dashboard-admin-expandido">
      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h1>Panel de Administración</h1>
          <p className="bienvenida">Bienvenido, {localStorage.getItem('usuario')}</p>
        </div>
        <button onClick={handleLogout} className="btn-logout">
          Cerrar Sesión
        </button>
      </div>

      {/* Estadísticas */}
      {estadisticas && (
        <div className="estadisticas-grid">
          <div className="stat-card stat-total">
            <div className="stat-icon">👥</div>
            <div className="stat-info">
              <h3>{estadisticas.total}</h3>
              <p>Total Estudiantes</p>
            </div>
          </div>
          
          <div className="stat-card stat-aprobados">
            <div className="stat-icon">✅</div>
            <div className="stat-info">
              <h3>{estadisticas.aprobados}</h3>
              <p>Aprobados</p>
            </div>
          </div>
          
          <div className="stat-card stat-pendientes">
            <div className="stat-icon">⏳</div>
            <div className="stat-info">
              <h3>{estadisticas.pendientes}</h3>
              <p>Pendientes</p>
            </div>
          </div>
          
          <div className="stat-card stat-rechazados">
            <div className="stat-icon">❌</div>
            <div className="stat-info">
              <h3>{estadisticas.rechazados}</h3>
              <p>Rechazados</p>
            </div>
          </div>
        </div>
      )}

      {/* Alertas de Documentos */}
      {alertasDocumentos.length > 0 && (
        <div className="alertas-panel">
          <div className="alertas-header" onClick={() => setMostrarAlertas(!mostrarAlertas)}>
            <h3>⚠️ Alertas de Documentación ({alertasDocumentos.length})</h3>
            <button className="btn-toggle">{mostrarAlertas ? '▼' : '▶'}</button>
          </div>
          {mostrarAlertas && (
            <div className="alertas-content">
              <div className="alertas-acciones">
                <button onClick={enviarRecordatorios} className="btn-recordatorios">
                  📧 Enviar Recordatorios Masivos
                </button>
              </div>
              <div className="alertas-lista">
                {alertasDocumentos.map(alerta => (
                  <div key={alerta.estudiante_id} className={`alerta-item urgencia-${alerta.urgencia}`}>
                    <div className="alerta-info">
                      <strong>{alerta.nombre}</strong>
                      <span className="alerta-estado">{alerta.estado}</span>
                    </div>
                    <div className="alerta-detalles">
                      <span>📄 {alerta.docs_subidos}/3 docs subidos</span>
                      <span>✓ {alerta.docs_generados}/4 docs generados</span>
                      <span>🕐 {alerta.dias_desde_registro} días</span>
                    </div>
                    <span className={`badge-urgencia ${alerta.urgencia}`}>
                      {alerta.urgencia.toUpperCase()}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tabs */}
      <div className="tabs-container">
        <button 
          className={`tab ${activeTab === 'estudiantes' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('estudiantes')}
        >
          👥 Estudiantes
        </button>
        <button 
          className={`tab ${activeTab === 'documentos' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('documentos')}
        >
          📄 Documentos Generados
        </button>
        <button 
          className={`tab ${activeTab === 'alertas' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('alertas')}
        >
          📅 Alertas de Fechas
        </button>
        <button 
          className={`tab ${activeTab === 'cursos' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('cursos')}
        >
          📚 Cursos
        </button>
        <button 
          className={`tab ${activeTab === 'alojamientos' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('alojamientos')}
        >
          🏠 Alojamientos
        </button>
        <button 
          className={`tab ${activeTab === 'partners' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('partners')}
        >
          🤝 Partnerships
        </button>
        <button 
          className={`tab ${activeTab === 'reportes' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('reportes')}
        >
          📊 Reportes
        </button>
      </div>

      {/* SECCIÓN: PARTNERSHIPS */}
      {activeTab === 'partners' && <PartnersAdmin />}

      {/* SECCIÓN: ALERTAS DE FECHAS */}
      {activeTab === 'alertas' && <AlertasAdmin apiUrl={apiUrl} />}

      {/* SECCIÓN: ESTUDIANTES */}
      {activeTab === 'estudiantes' && (
        <>
          {/* Filtros y búsqueda */}
          <div className="controles">
        <div className="filtros">
          <button 
            className={filtro === 'todos' ? 'filtro-activo' : ''}
            onClick={() => setFiltro('todos')}
          >
            Todos
          </button>
          <button 
            className={filtro === 'pendiente' ? 'filtro-activo' : ''}
            onClick={() => setFiltro('pendiente')}
          >
            Pendientes
          </button>
          <button 
            className={filtro === 'aprobado' ? 'filtro-activo' : ''}
            onClick={() => setFiltro('aprobado')}
          >
            Aprobados
          </button>
          <button 
            className={filtro === 'rechazado' ? 'filtro-activo' : ''}
            onClick={() => setFiltro('rechazado')}
          >
            Rechazados
          </button>
        </div>
        
        <input
          type="text"
          placeholder="Buscar por nombre, email o especialidad..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
          className="buscador"
        />
      </div>

      {/* Lista de estudiantes */}
      <div className="estudiantes-section">
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
          <h2>Gestión de Estudiantes ({estudiantesFiltrados.length})</h2>
          <button
            onClick={abrirModalGenerarDocs}
            style={{
              backgroundColor: '#10b981',
              color: 'white',
              padding: '12px 24px',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            📄 Generar Documentos
          </button>
        </div>
        
        {estudiantesFiltrados.length === 0 ? (
          <p className="no-resultados">No se encontraron estudiantes</p>
        ) : (
          <div className="tabla-container">
            <table className="tabla-estudiantes">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>Email</th>
                  <th>Especialidad</th>
                  <th>Tipo Visa</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {estudiantesFiltrados.map(est => (
                  <tr key={est.id}>
                    <td>{est.id}</td>
                    <td>{est.nombre || est.nombre_completo || 'N/A'}</td>
                    <td>{est.email || 'N/A'}</td>
                    <td>{est.especialidad || est.especialidad_interes || 'N/A'}</td>
                    <td>{est.tipo_visa || 'N/A'}</td>
                    <td>
                      <span className={`badge badge-${est.estado || est.estado_procesamiento || 'pendiente'}`}>
                        {(est.estado || est.estado_procesamiento || 'pendiente').toUpperCase()}
                      </span>
                    </td>
                    <td>
                      <div className="acciones">
                        {(est.estado === 'pendiente' || est.estado_procesamiento === 'pendiente' || (!est.estado && !est.estado_procesamiento)) && (
                          <>
                            <button 
                              onClick={() => aprobarEstudiante(est.id)}
                              className="btn-aprobar"
                              title="Aprobar"
                            >
                              ✓
                            </button>
                            <button 
                              onClick={() => rechazarEstudiante(est.id)}
                              className="btn-rechazar"
                              title="Rechazar"
                            >
                              ✗
                            </button>
                          </>
                        )}
                        <button 
                          onClick={() => abrirModalMensaje(est)}
                          className="btn-mensaje"
                          title="Enviar Mensaje"
                          style={{backgroundColor: '#3b82f6', color: 'white', padding: '6px 10px', border: 'none', borderRadius: '5px', cursor: 'pointer', fontSize: '16px'}}
                        >
                          ✉️
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      </>
      )}

      {/* SECCIÓN: DOCUMENTOS GENERADOS */}
      {activeTab === 'documentos' && (
        <div className="documentos-section">
          <h2>Documentos Generados ({documentosGenerados.length})</h2>
          
          <div className="documentos-info">
            <p>📄 Aquí puedes generar documentos oficiales para los estudiantes, revisarlos y aprobarlos.</p>
          </div>

          {documentosGenerados.length === 0 ? (
            <div className="no-documentos">
              <p>No hay documentos generados aún</p>
              <p>Ve a la pestaña de Estudiantes y genera documentos para cada estudiante</p>
            </div>
          ) : (
            <div className="tabla-container">
              <table className="tabla-documentos">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Estudiante</th>
                    <th>Tipo Documento</th>
                    <th>Archivo</th>
                    <th>Estado</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {documentosGenerados.map(doc => (
                    <tr key={doc.id}>
                      <td>{doc.id}</td>
                      <td>{doc.estudiante_nombre}</td>
                      <td>{doc.tipo_documento.replace('_', ' ').toUpperCase()}</td>
                      <td>{doc.nombre_archivo}</td>
                      <td>
                        <span className={`badge badge-${doc.estado}`}>
                          {doc.estado.toUpperCase()}
                        </span>
                      </td>
                      <td>{new Date(doc.fecha_generacion).toLocaleDateString()}</td>
                      <td>
                        <div className="acciones">
                          <button 
                            onClick={() => descargarDocumento(doc.id)}
                            className="btn-descargar"
                            title="Descargar PDF"
                          >
                            📥
                          </button>
                          {doc.estado === 'generado' && (
                            <button 
                              onClick={() => aprobarDocumento(doc.id)}
                              className="btn-aprobar"
                              title="Aprobar y Enviar"
                            >
                              ✓
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* SECCIÓN: CURSOS */}
      {activeTab === 'cursos' && (
        <div className="cursos-section">
          <div className="section-header">
            <h2>📚 Gestión de Cursos</h2>
            <div className="header-actions">
              <button onClick={sincronizarCursosEscuelas} className="btn-sync">
                🔄 Sincronizar con Escuelas
              </button>
              <button onClick={() => setShowAddCursoModal(true)} className="btn-add">
                + Agregar Curso
              </button>
            </div>
          </div>

          {cursos.length === 0 ? (
            <div className="no-data">No hay cursos registrados</div>
          ) : (
            <div className="tabla-wrapper">
              <table className="tabla-cursos">
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Duración</th>
                    <th>Precio</th>
                    <th>Ciudad</th>
                    <th>Nivel Español</th>
                    <th>Cupos</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {cursos.map(curso => (
                    <tr key={curso.id}>
                      <td>{curso.nombre}</td>
                      <td>{curso.duracion_meses} meses</td>
                      <td>€{curso.precio_eur}</td>
                      <td>{curso.ciudad}</td>
                      <td>{curso.nivel_espanol_requerido}</td>
                      <td>{curso.cupos_disponibles}</td>
                      <td>
                        <span className={`badge ${curso.activo ? 'badge-success' : 'badge-inactive'}`}>
                          {curso.activo ? 'Activo' : 'Inactivo'}
                        </span>
                      </td>
                      <td>
                        <button 
                          onClick={() => verificarDisponibilidadCurso(curso.id)}
                          className="btn-verificar"
                          title="Verificar disponibilidad en tiempo real"
                        >
                          🔍
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* SECCIÓN: ALOJAMIENTOS */}
      {activeTab === 'alojamientos' && (
        <div className="alojamientos-section">
          <div className="section-header">
            <h2>🏠 Gestión de Alojamientos</h2>
            <button onClick={() => setShowAddAlojamientoModal(true)} className="btn-add">
              + Agregar Alojamiento
            </button>
          </div>

          {alojamientos.length === 0 ? (
            <div className="no-data">No hay alojamientos registrados</div>
          ) : (
            <div className="tabla-wrapper">
              <table className="tabla-alojamientos">
                <thead>
                  <tr>
                    <th>Tipo</th>
                    <th>Dirección</th>
                    <th>Ciudad</th>
                    <th>Precio/Mes</th>
                    <th>Capacidad</th>
                    <th>Disponible</th>
                  </tr>
                </thead>
                <tbody>
                  {alojamientos.map(aloj => (
                    <tr key={aloj.id}>
                      <td>{aloj.tipo}</td>
                      <td>{aloj.direccion}</td>
                      <td>{aloj.ciudad}</td>
                      <td>€{aloj.precio_mensual_eur}/mes</td>
                      <td>{aloj.capacidad} personas</td>
                      <td>
                        <span className={`badge ${aloj.disponible ? 'badge-success' : 'badge-danger'}`}>
                          {aloj.disponible ? 'Disponible' : 'Ocupado'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Modal: Agregar Curso */}
      {showAddCursoModal && (
        <div className="modal-overlay" onClick={() => setShowAddCursoModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Agregar Nuevo Curso</h3>
            <div className="form-group">
              <label>Nombre del Curso</label>
              <input 
                type="text" 
                value={nuevoCurso.nombre} 
                onChange={(e) => setNuevoCurso({...nuevoCurso, nombre: e.target.value})}
                placeholder="Ej: Curso de Español Intensivo"
              />
            </div>
            <div className="form-group">
              <label>Descripción</label>
              <textarea 
                value={nuevoCurso.descripcion} 
                onChange={(e) => setNuevoCurso({...nuevoCurso, descripcion: e.target.value})}
                placeholder="Descripción del curso"
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Duración (meses)</label>
                <input 
                  type="number" 
                  value={nuevoCurso.duracion_meses} 
                  onChange={(e) => setNuevoCurso({...nuevoCurso, duracion_meses: parseInt(e.target.value)})}
                />
              </div>
              <div className="form-group">
                <label>Precio (EUR)</label>
                <input 
                  type="number" 
                  value={nuevoCurso.precio_eur} 
                  onChange={(e) => setNuevoCurso({...nuevoCurso, precio_eur: parseFloat(e.target.value)})}
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Ciudad</label>
                <input 
                  type="text" 
                  value={nuevoCurso.ciudad} 
                  onChange={(e) => setNuevoCurso({...nuevoCurso, ciudad: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Nivel Español Requerido</label>
                <input 
                  type="text" 
                  value={nuevoCurso.nivel_espanol_requerido} 
                  onChange={(e) => setNuevoCurso({...nuevoCurso, nivel_espanol_requerido: e.target.value})}
                  placeholder="Ej: A2, B1, B2"
                />
              </div>
            </div>
            <div className="form-group">
              <label>Cupos Disponibles</label>
              <input 
                type="number" 
                value={nuevoCurso.cupos_disponibles} 
                onChange={(e) => setNuevoCurso({...nuevoCurso, cupos_disponibles: parseInt(e.target.value)})}
              />
            </div>
            <div className="modal-actions">
              <button onClick={() => setShowAddCursoModal(false)} className="btn-cancel">
                Cancelar
              </button>
              <button onClick={crearCurso} className="btn-submit">
                Crear Curso
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Agregar Alojamiento */}
      {showAddAlojamientoModal && (
        <div className="modal-overlay" onClick={() => setShowAddAlojamientoModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Agregar Nuevo Alojamiento</h3>
            <div className="form-group">
              <label>Tipo de Alojamiento</label>
              <input 
                type="text" 
                value={nuevoAlojamiento.tipo} 
                onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, tipo: e.target.value})}
                placeholder="Ej: Apartamento, Residencia, Familia"
              />
            </div>
            <div className="form-group">
              <label>Dirección</label>
              <input 
                type="text" 
                value={nuevoAlojamiento.direccion} 
                onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, direccion: e.target.value})}
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Ciudad</label>
                <input 
                  type="text" 
                  value={nuevoAlojamiento.ciudad} 
                  onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, ciudad: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Precio Mensual (EUR)</label>
                <input 
                  type="number" 
                  value={nuevoAlojamiento.precio_mensual_eur} 
                  onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, precio_mensual_eur: parseFloat(e.target.value)})}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Capacidad (personas)</label>
              <input 
                type="number" 
                value={nuevoAlojamiento.capacidad} 
                onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, capacidad: parseInt(e.target.value)})}
              />
            </div>
            <div className="form-group">
              <label>Descripción</label>
              <textarea 
                value={nuevoAlojamiento.descripcion} 
                onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, descripcion: e.target.value})}
                placeholder="Descripción del alojamiento"
              />
            </div>
            <div className="form-group">
              <label>Servicios</label>
              <textarea 
                value={nuevoAlojamiento.servicios} 
                onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, servicios: e.target.value})}
                placeholder="Ej: WiFi, Cocina, Limpieza"
              />
            </div>
            <div className="modal-actions">
              <button onClick={() => setShowAddAlojamientoModal(false)} className="btn-cancel">
                Cancelar
              </button>
              <button onClick={crearAlojamiento} className="btn-submit">
                Crear Alojamiento
              </button>
            </div>
          </div>
        </div>
      )}

      {/* SECCIÓN: REPORTES */}
      {activeTab === 'reportes' && (
        <div className="reportes-section">
          <h2>📊 Reportes y Estadísticas</h2>
          
          {!reporteEstudiantes ? (
            <div className="loading">Cargando reportes...</div>
          ) : (
            <>
              {/* Resumen general */}
              <div className="reporte-resumen">
                <div className="reporte-card">
                  <h3>Total Registrados</h3>
                  <div className="reporte-numero">{reporteEstudiantes.total}</div>
                </div>
                <div className="reporte-card">
                  <h3>Aprobados</h3>
                  <div className="reporte-numero success">
                    {reporteEstudiantes.estudiantes.filter(e => e.estado === 'aprobado').length}
                  </div>
                </div>
                <div className="reporte-card">
                  <h3>Pendientes</h3>
                  <div className="reporte-numero warning">
                    {reporteEstudiantes.estudiantes.filter(e => e.estado === 'pendiente').length}
                  </div>
                </div>
                <div className="reporte-card">
                  <h3>Rechazados</h3>
                  <div className="reporte-numero danger">
                    {reporteEstudiantes.estudiantes.filter(e => e.estado === 'rechazado').length}
                  </div>
                </div>
              </div>

              {/* Estadísticas por nacionalidad */}
              <div className="reporte-seccion">
                <h3>Estudiantes por Nacionalidad</h3>
                <div className="tabla-wrapper">
                  <table className="tabla-reportes">
                    <thead>
                      <tr>
                        <th>Nacionalidad</th>
                        <th>Total</th>
                        <th>Aprobados</th>
                        <th>Tasa Éxito</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(
                        reporteEstudiantes.estudiantes.reduce((acc, est) => {
                          const nac = est.nacionalidad || 'Sin especificar'
                          if (!acc[nac]) acc[nac] = { total: 0, aprobados: 0 }
                          acc[nac].total++
                          if (est.estado === 'aprobado') acc[nac].aprobados++
                          return acc
                        }, {})
                      ).map(([nac, stats]) => (
                        <tr key={nac}>
                          <td>{nac}</td>
                          <td>{stats.total}</td>
                          <td>{stats.aprobados}</td>
                          <td>
                            <span className={`badge ${stats.aprobados / stats.total > 0.7 ? 'badge-success' : stats.aprobados / stats.total > 0.4 ? 'badge-warning' : 'badge-danger'}`}>
                              {((stats.aprobados / stats.total) * 100).toFixed(0)}%
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Estadísticas por curso */}
              <div className="reporte-seccion">
                <h3>Estudiantes por Curso</h3>
                <div className="tabla-wrapper">
                  <table className="tabla-reportes">
                    <thead>
                      <tr>
                        <th>Curso</th>
                        <th>Estudiantes Asignados</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(
                        reporteEstudiantes.estudiantes.reduce((acc, est) => {
                          const curso = est.curso || 'Sin asignar'
                          acc[curso] = (acc[curso] || 0) + 1
                          return acc
                        }, {})
                      ).map(([curso, count]) => (
                        <tr key={curso}>
                          <td>{curso}</td>
                          <td>{count}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Botón de exportar */}
              <div className="reporte-acciones">
                <button 
                  onClick={() => {
                    const dataStr = JSON.stringify(reporteEstudiantes, null, 2)
                    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
                    const exportFileDefaultName = `reporte_estudiantes_${new Date().toISOString().split('T')[0]}.json`
                    const linkElement = document.createElement('a')
                    linkElement.setAttribute('href', dataUri)
                    linkElement.setAttribute('download', exportFileDefaultName)
                    linkElement.click()
                  }}
                  className="btn-export"
                >
                  📥 Exportar JSON
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {/* Modal: Cursos Sugeridos */}
      {showCursosSugeridosModal && (
        <div className="modal-overlay" onClick={() => setShowCursosSugeridosModal(false)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <h3>📚 Cursos Sugeridos para el Estudiante</h3>
            
            {cursosSugeridos.length === 0 ? (
              <div className="no-data">No hay cursos disponibles que coincidan con el perfil</div>
            ) : (
              <div className="cursos-sugeridos-lista">
                {cursosSugeridos.map(curso => (
                  <div key={curso.id} className="curso-sugerido-card">
                    <div className="curso-sugerido-header">
                      <h4>{curso.nombre}</h4>
                      <span className={`compatibilidad-badge compatibilidad-${Math.floor(curso.compatibilidad / 20)}`}>
                        {curso.compatibilidad}% compatible
                      </span>
                    </div>
                    <p className="curso-descripcion">{curso.descripcion}</p>
                    <div className="curso-detalles">
                      <span>🕐 {curso.duracion_meses} meses</span>
                      <span>📍 {curso.ciudad}</span>
                      <span>💶 €{curso.precio_eur}</span>
                      <span>📖 {curso.nivel_espanol_requerido}</span>
                    </div>
                    <button 
                      onClick={() => aprobarConCurso(curso.id)}
                      className="btn-seleccionar-curso"
                    >
                      ✓ Seleccionar este curso
                    </button>
                  </div>
                ))}
              </div>
            )}
            
            <div className="modal-actions">
              <button onClick={() => setShowCursosSugeridosModal(false)} className="btn-cancel">
                Cancelar
              </button>
              <button onClick={() => aprobarConCurso(null)} className="btn-submit-secondary">
                Aprobar sin asignar curso
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de rechazo */}
      {estudianteSeleccionado && (
        <div className="modal-overlay" onClick={() => setEstudianteSeleccionado(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Rechazar Estudiante</h3>
            <p>Por favor indique el motivo del rechazo:</p>
            <textarea
              value={motivoRechazo}
              onChange={(e) => setMotivoRechazo(e.target.value)}
              placeholder="Ej: Documentación incompleta"
              rows="4"
            />
            <div className="modal-actions">
              <button onClick={() => setEstudianteSeleccionado(null)} className="btn-cancelar">
                Cancelar
              </button>
              <button onClick={confirmarRechazo} className="btn-confirmar">
                Confirmar Rechazo
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Generar Documentos - Estudiantes Aprobados */}
      {showModalGenerarDocs && (
        <div className="modal-overlay" onClick={() => setShowModalGenerarDocs(false)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <h3>📄 Generar Documentos Oficiales</h3>
            <p style={{color: '#6b7280', marginBottom: '20px'}}>
              Selecciona un estudiante APROBADO para generar sus documentos oficiales
            </p>

            {estudiantesAprobados.length === 0 ? (
              <div style={{padding: '40px', textAlign: 'center', backgroundColor: '#fef3c7', borderRadius: '8px'}}>
                <p style={{fontSize: '48px', margin: '0 0 10px 0'}}>⚠️</p>
                <p style={{fontSize: '18px', fontWeight: 'bold', color: '#92400e', margin: '0 0 10px 0'}}>
                  No hay estudiantes aprobados
                </p>
                <p style={{color: '#78350f', margin: 0}}>
                  Debes aprobar estudiantes primero antes de generar documentos
                </p>
              </div>
            ) : (
              <div style={{maxHeight: '500px', overflowY: 'auto'}}>
                <table style={{width: '100%', borderCollapse: 'collapse'}}>
                  <thead style={{position: 'sticky', top: 0, backgroundColor: '#f9fafb', borderBottom: '2px solid #e5e7eb'}}>
                    <tr>
                      <th style={{padding: '12px', textAlign: 'left'}}>ID</th>
                      <th style={{padding: '12px', textAlign: 'left'}}>Nombre</th>
                      <th style={{padding: '12px', textAlign: 'left'}}>Email</th>
                      <th style={{padding: '12px', textAlign: 'left'}}>Especialidad</th>
                      <th style={{padding: '12px', textAlign: 'center'}}>Acción</th>
                    </tr>
                  </thead>
                  <tbody>
                    {estudiantesAprobados.map(est => (
                      <tr key={est.id} style={{borderBottom: '1px solid #e5e7eb'}}>
                        <td style={{padding: '12px'}}>{est.id}</td>
                        <td style={{padding: '12px', fontWeight: 'bold'}}>{est.nombre || est.nombre_completo}</td>
                        <td style={{padding: '12px', fontSize: '0.9rem', color: '#6b7280'}}>{est.email}</td>
                        <td style={{padding: '12px'}}>{est.especialidad || est.especialidad_interes || '-'}</td>
                        <td style={{padding: '12px', textAlign: 'center'}}>
                          <button
                            onClick={() => generarDocumentos(est.id)}
                            disabled={generandoDocs}
                            style={{
                              backgroundColor: '#10b981',
                              color: 'white',
                              padding: '8px 16px',
                              border: 'none',
                              borderRadius: '5px',
                              cursor: generandoDocs ? 'not-allowed' : 'pointer',
                              fontSize: '14px',
                              fontWeight: 'bold',
                              opacity: generandoDocs ? 0.5 : 1
                            }}
                          >
                            {generandoDocs ? '⏳ Generando...' : '📄 Generar'}
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            <div className="modal-actions" style={{marginTop: '20px'}}>
              <button 
                onClick={() => setShowModalGenerarDocs(false)} 
                className="btn-cancelar"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Enviar Mensaje */}
      {showMensajeModal && estudianteParaMensaje && (
        <div className="modal-overlay" onClick={() => setShowMensajeModal(false)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <h3>✉️ Enviar Mensaje a {estudianteParaMensaje.nombre || estudianteParaMensaje.nombre_completo}</h3>
            <p style={{color: '#6b7280', marginBottom: '20px'}}>
              📧 {estudianteParaMensaje.email}
            </p>
            
            <div className="form-group">
              <label>Asunto del Email:</label>
              <input
                type="text"
                value={nuevoMensaje.asunto}
                onChange={(e) => setNuevoMensaje({...nuevoMensaje, asunto: e.target.value})}
                placeholder="Ej: Solicitud de Documento Adicional"
                style={{width: '100%', padding: '10px', border: '1px solid #e5e7eb', borderRadius: '5px'}}
              />
            </div>

            <div className="form-group">
              <label>Tipo de Mensaje:</label>
              <select
                value={nuevoMensaje.tipo}
                onChange={(e) => setNuevoMensaje({...nuevoMensaje, tipo: e.target.value})}
                style={{width: '100%', padding: '10px', border: '1px solid #e5e7eb', borderRadius: '5px'}}
              >
                <option value="informacion">ℹ️ Información General</option>
                <option value="solicitud_documento">📄 Solicitud de Documento</option>
                <option value="recordatorio">⏰ Recordatorio</option>
                <option value="urgente">🚨 Urgente</option>
              </select>
            </div>

            {nuevoMensaje.tipo === 'solicitud_documento' && (
              <div className="form-group">
                <label>Documento Solicitado:</label>
                <input
                  type="text"
                  value={nuevoMensaje.documento_solicitado}
                  onChange={(e) => setNuevoMensaje({...nuevoMensaje, documento_solicitado: e.target.value})}
                  placeholder="Ej: Certificado de antecedentes penales"
                  style={{width: '100%', padding: '10px', border: '1px solid #e5e7eb', borderRadius: '5px'}}
                />
              </div>
            )}

            <div className="form-group">
              <label>Mensaje:</label>
              <textarea
                value={nuevoMensaje.mensaje}
                onChange={(e) => setNuevoMensaje({...nuevoMensaje, mensaje: e.target.value})}
                placeholder="Escribe tu mensaje aquí..."
                rows="8"
                style={{width: '100%', padding: '10px', border: '1px solid #e5e7eb', borderRadius: '5px', fontFamily: 'inherit'}}
              />
            </div>

            <div style={{backgroundColor: '#dbeafe', padding: '15px', borderRadius: '5px', marginBottom: '20px'}}>
              <p style={{margin: 0, fontSize: '14px', color: '#1e40af'}}>
                ℹ️ <strong>Nota:</strong> El estudiante recibirá este mensaje en su portal y también por email a {estudianteParaMensaje.email}
              </p>
            </div>

            <div className="modal-actions">
              <button 
                onClick={() => {
                  setShowMensajeModal(false)
                  setEstudianteParaMensaje(null)
                }} 
                className="btn-cancelar"
                disabled={enviandoMensaje}
              >
                Cancelar
              </button>
              <button 
                onClick={enviarMensaje} 
                className="btn-confirmar"
                disabled={enviandoMensaje || !nuevoMensaje.mensaje.trim()}
                style={{backgroundColor: '#3b82f6', opacity: enviandoMensaje ? 0.6 : 1}}
              >
                {enviandoMensaje ? '⏳ Enviando...' : '📤 Enviar Mensaje'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default DashboardAdminExpandido
