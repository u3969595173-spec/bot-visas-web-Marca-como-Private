import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import './DashboardAdminExpandido.css'

function DashboardAdminExpandido({ onLogout }) {
  const [estudiantes, setEstudiantes] = useState([])
  const [estadisticas, setEstadisticas] = useState(null)
  const [loading, setLoading] = useState(true)
  const [filtro, setFiltro] = useState('todos')
  const [busqueda, setBusqueda] = useState('')
  const [motivoRechazo, setMotivoRechazo] = useState('')
  const [estudianteSeleccionado, setEstudianteSeleccionado] = useState(null)
  const navigate = useNavigate()

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    cargarDatos()
  }, [])

  const cargarDatos = async () => {
    setLoading(true)
    try {
      const [estRes, statsRes] = await Promise.all([
        axios.get(`${apiUrl}/api/admin/estudiantes`),
        axios.get(`${apiUrl}/api/admin/estadisticas`)
      ])
      setEstudiantes(estRes.data)
      setEstadisticas(statsRes.data)
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
    if (!confirm('¿Está seguro de aprobar este estudiante?')) return
    
    try {
      await axios.post(`${apiUrl}/api/admin/estudiantes/${id}/aprobar`)
      alert('Estudiante aprobado correctamente')
      cargarDatos()
    } catch (err) {
      alert('Error al aprobar estudiante: ' + (err.response?.data?.detail || err.message))
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
                        {est.estado !== 'pendiente' && (
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
