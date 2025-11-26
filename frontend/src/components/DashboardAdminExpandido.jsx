import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import './DashboardAdminExpandido.css'

function DashboardAdminExpandido({ onLogout }) {
  const [activeTab, setActiveTab] = useState('estudiantes')
  const [estudiantes, setEstudiantes] = useState([])
  const [documentosGenerados, setDocumentosGenerados] = useState([])
  const [cursos, setCursos] = useState([])
  const [alojamientos, setAlojamientos] = useState([])
  const [estadisticas, setEstadisticas] = useState(null)
  const [reporteEstudiantes, setReporteEstudiantes] = useState(null)
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
    const cumpleFiltro = filtro === 'todos' || est.estado === filtro
    const cumpleBusqueda = !busqueda || 
      est.nombre?.toLowerCase().includes(busqueda.toLowerCase()) ||
      est.email?.toLowerCase().includes(busqueda.toLowerCase()) ||
      est.especialidad?.toLowerCase().includes(busqueda.toLowerCase())
    
    return cumpleFiltro && cumpleBusqueda
  })

  const generarDocumentos = async (estudianteId) => {
    if (!confirm('¿Generar todos los documentos oficiales para este estudiante?')) return
    
    setGenerandoDocs(true)
    try {
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteId}/generar-documentos`, {
        tipos_documentos: ['carta_aceptacion', 'carta_motivacion', 'formulario_solicitud', 'certificado_matricula']
      })
      alert('Documentos generados correctamente')
      setActiveTab('documentos')
      cargarDatos()
    } catch (err) {
      alert('Error al generar documentos: ' + (err.response?.data?.detail || err.message))
    } finally {
      setGenerandoDocs(false)
    }
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
          className={`tab ${activeTab === 'reportes' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('reportes')}
        >
          📊 Reportes
        </button>
      </div>

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
        <h2>Gestión de Estudiantes ({estudiantesFiltrados.length})</h2>
        
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
                    <td>{est.nombre || 'N/A'}</td>
                    <td>{est.email || 'N/A'}</td>
                    <td>{est.especialidad || 'N/A'}</td>
                    <td>{est.tipo_visa || 'N/A'}</td>
                    <td>
                      <span className={`badge badge-${est.estado}`}>
                        {est.estado?.toUpperCase()}
                      </span>
                    </td>
                    <td>
                      <div className="acciones">
                        {est.estado === 'pendiente' && (
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
                          onClick={() => generarDocumentos(est.id)}
                          className="btn-generar-docs"
                          title="Generar Documentos"
                          disabled={generandoDocs}
                        >
                          📄
                        </button>
                        {est.estado !== 'pendiente' && !generandoDocs && (
                          <span className="sin-acciones">-</span>
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
            <button onClick={() => setShowAddCursoModal(true)} className="btn-add">
              + Agregar Curso
            </button>
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
    </div>
  )
}

export default DashboardAdminExpandido
