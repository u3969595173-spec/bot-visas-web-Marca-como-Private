import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function DashboardAdmin({ onLogout }) {
  const [estudiantes, setEstudiantes] = useState([])
  const [estadisticas, setEstadisticas] = useState(null)
  const [filtroEstado, setFiltroEstado] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const navigate = useNavigate()

  // Configurar token en axios
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
  }, [])

  // Cargar datos iniciales
  useEffect(() => {
    cargarDatos()
  }, [filtroEstado])

  const cargarDatos = async () => {
    setLoading(true)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const [estudiantesRes, estadisticasRes] = await Promise.all([
        axios.get(`${apiUrl}/api/admin/estudiantes`, {
          params: filtroEstado ? { estado: filtroEstado } : {},
        }),
        axios.get(`${apiUrl}/api/admin/estadisticas`),
      ])

      setEstudiantes(estudiantesRes.data)
      setEstadisticas(estadisticasRes.data)
      setError('')
    } catch (err) {
      if (err.response?.status === 401) {
        handleLogout()
      } else {
        setError('Error al cargar datos')
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

  const handleAprobar = async (estudianteId, nombre) => {
    if (!confirm(`¿Aprobar solicitud de ${nombre}?`)) return

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteId}/aprobar`)
      setSuccess(`✅ Estudiante ${nombre} aprobado correctamente`)
      cargarDatos()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Error al aprobar estudiante')
    }
  }

  const handleRechazar = async (estudianteId, nombre) => {
    const motivo = prompt(`¿Por qué rechazar a ${nombre}?`, 'Faltan documentos')
    if (!motivo) return

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteId}/rechazar`, null, {
        params: { motivo },
      })
      setSuccess(`⚠️ Estudiante ${nombre} marcado para revisión`)
      cargarDatos()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Error al rechazar estudiante')
    }
  }

  const getEstadoBadge = (estado) => {
    const badges = {
      registrado: 'badge-info',
      procesado_automaticamente: 'badge-warning',
      pendiente_revision_admin: 'badge-warning',
      aprobado_admin: 'badge-success',
      enviado_estudiante: 'badge-success',
      rechazado_admin: 'badge-danger',
    }
    return badges[estado] || 'badge-info'
  }

  if (loading && !estudiantes.length) {
    return (
      <div className="container">
        <div className="loading">Cargando dashboard...</div>
      </div>
    )
  }

  return (
    <div className="container">
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '30px',
      }}>
        <div>
          <h1 style={{ color: 'white', marginBottom: '5px' }}>
            Panel de Administración
          </h1>
          <p style={{ color: 'rgba(255,255,255,0.9)' }}>
            Bienvenido, {localStorage.getItem('usuario')}
          </p>
        </div>
        <button
          onClick={handleLogout}
          className="btn"
          style={{ background: 'white', color: '#667eea' }}
        >
          Cerrar Sesión
        </button>
      </div>

      {/* Botones de Acceso Rápido */}
      <div style={{
        display: 'flex',
        gap: '15px',
        marginBottom: '30px',
        flexWrap: 'wrap'
      }}>
        <button
          onClick={() => navigate('/admin/tesoro')}
          className="btn"
          style={{
            background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            color: 'white',
            border: 'none',
            fontWeight: '600',
            padding: '15px 25px',
            borderRadius: '10px',
            fontSize: '16px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          💰 Tesoro de Pagos
        </button>
        <button
          onClick={() => navigate('/admin/presupuestos')}
          className="btn"
          style={{
            background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
            color: 'white',
            border: 'none',
            fontWeight: '600',
            padding: '15px 25px',
            borderRadius: '10px',
            fontSize: '16px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          📋 Gestionar Presupuestos
        </button>
      </div>

      {/* Estadísticas */}
      {estadisticas && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '20px',
          marginBottom: '30px',
        }}>
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#667eea' }}>
              {estadisticas.total_estudiantes}
            </div>
            <div style={{ color: '#718096', marginTop: '5px' }}>
              Total Estudiantes
            </div>
          </div>
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#ed8936' }}>
              {estadisticas.pendientes_revision}
            </div>
            <div style={{ color: '#718096', marginTop: '5px' }}>
              Pendientes Revisión
            </div>
          </div>
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#48bb78' }}>
              {estadisticas.aprobados}
            </div>
            <div style={{ color: '#718096', marginTop: '5px' }}>
              Aprobados
            </div>
          </div>
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#4299e1' }}>
              {estadisticas.enviados}
            </div>
            <div style={{ color: '#718096', marginTop: '5px' }}>
              Enviados
            </div>
          </div>
        </div>
      )}

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      {/* Lista de Estudiantes */}
      <div className="card">
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
        }}>
          <h2 style={{ margin: 0 }}>📋 Estudiantes</h2>
          <select
            value={filtroEstado}
            onChange={(e) => setFiltroEstado(e.target.value)}
            style={{
              padding: '8px',
              border: '2px solid #e2e8f0',
              borderRadius: '5px',
            }}
          >
            <option value="">Todos los estados</option>
            <option value="registrado">Registrado</option>
            <option value="procesado_automaticamente">En Proceso</option>
            <option value="pendiente_revision_admin">Pendiente Revisión</option>
            <option value="aprobado_admin">Aprobado</option>
            <option value="enviado_estudiante">Enviado</option>
          </select>
        </div>

        {estudiantes.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#718096' }}>
            No hay estudiantes con este filtro
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>Email</th>
                  <th>Especialidad</th>
                  <th>Estado</th>
                  <th>Fecha</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {estudiantes.map((est) => (
                  <tr key={est.id}>
                    <td>#{est.id}</td>
                    <td>{est.nombre_completo}</td>
                    <td>{est.email}</td>
                    <td>{est.especialidad_interes}</td>
                    <td>
                      <span className={`badge ${getEstadoBadge(est.estado_procesamiento)}`}>
                        {est.estado_procesamiento}
                      </span>
                    </td>
                    <td>
                      {new Date(est.created_at).toLocaleDateString('es-ES')}
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '5px' }}>
                        {est.estado_procesamiento === 'pendiente_revision_admin' && (
                          <>
                            <button
                              onClick={() => handleAprobar(est.id, est.nombre_completo)}
                              className="btn btn-success"
                              style={{ padding: '6px 12px', fontSize: '14px' }}
                            >
                              ✅
                            </button>
                            <button
                              onClick={() => handleRechazar(est.id, est.nombre_completo)}
                              className="btn btn-danger"
                              style={{ padding: '6px 12px', fontSize: '14px' }}
                            >
                              ❌
                            </button>
                          </>
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
    </div>
  )
}

export default DashboardAdmin
