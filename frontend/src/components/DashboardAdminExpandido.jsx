import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function DashboardAdminExpandido({ onLogout }) {
  const [activeSection, setActiveSection] = useState('estudiantes')
  const [estudiantes, setEstudiantes] = useState([])
  const [cursos, setCursos] = useState([])
  const [alojamientos, setAlojamientos] = useState([])
  const [estadisticas, setEstadisticas] = useState(null)
  const [reportes, setReportes] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    cargarDatos()
  }, [activeSection])

  const cargarDatos = async () => {
    setLoading(true)
    try {
      if (activeSection === 'estudiantes' || activeSection === 'inicio') {
        const [estRes, statsRes] = await Promise.all([
          axios.get('/api/admin/estudiantes'),
          axios.get('/api/admin/estadisticas')
        ])
        setEstudiantes(estRes.data)
        setEstadisticas(statsRes.data)
      } else if (activeSection === 'cursos') {
        const res = await axios.get('/api/cursos', { params: { limit: 100 } })
        setCursos(res.data.cursos)
      } else if (activeSection === 'alojamiento') {
        const res = await axios.get('/api/alojamientos', { params: { limit: 100 } })
        setAlojamientos(res.data.alojamientos)
      } else if (activeSection === 'reportes') {
        const res = await axios.get('/api/admin/reportes/mensual')
        setReportes(res.data)
      }
    } catch (err) {
      console.error('Error:', err)
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

  const crearCurso = async (datos) => {
    try {
      await axios.post('/api/admin/cursos', datos)
      alert('Curso creado correctamente')
      cargarDatos()
      setShowModal(null)
    } catch (err) {
      alert('Error al crear curso')
    }
  }

  const crearAlojamiento = async (datos) => {
    try {
      await axios.post('/api/admin/alojamientos', datos)
      alert('Alojamiento creado correctamente')
      cargarDatos()
      setShowModal(null)
    } catch (err) {
      alert('Error al crear alojamiento')
    }
  }

  return (
    <div className="container" style={{ paddingBottom: '40px' }}>
      {/* Header */}
      <div style={{
        background: 'white',
        padding: '20px',
        borderRadius: '10px',
        marginBottom: '30px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div>
          <h1 style={{ marginBottom: '5px' }}>Panel de Administración</h1>
          <p style={{ color: '#718096' }}>
            Bienvenido, {localStorage.getItem('usuario')}
          </p>
        </div>
        <button onClick={handleLogout} className="btn btn-danger">
          Cerrar Sesión
        </button>
      </div>

      {/* Menú lateral */}
      <div style={{ display: 'grid', gridTemplateColumns: '250px 1fr', gap: '20px' }}>
        {/* Sidebar */}
        <div className="card" style={{ height: 'fit-content' }}>
          <h3 style={{ marginBottom: '20px' }}>Secciones</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {[
              { id: 'inicio', label: '📊 Inicio', icon: '📊' },
              { id: 'estudiantes', label: '👥 Estudiantes', icon: '👥' },
              { id: 'cursos', label: '📚 Cursos', icon: '📚' },
              { id: 'alojamiento', label: '🏠 Alojamiento', icon: '🏠' },
              { id: 'documentos', label: '📄 Documentos', icon: '📄' },
              { id: 'reportes', label: '📈 Reportes', icon: '📈' }
            ].map(section => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className="btn"
                style={{
                  background: activeSection === section.id ? '#667eea' : 'transparent',
                  color: activeSection === section.id ? 'white' : '#2d3748',
                  border: activeSection === section.id ? 'none' : '2px solid #e2e8f0',
                  textAlign: 'left',
                  padding: '12px 20px'
                }}
              >
                {section.icon} {section.label}
              </button>
            ))}
          </div>
        </div>

        {/* Contenido principal */}
        <div>
          {loading && <div className="loading">Cargando...</div>}

          {/* SECCIÓN: INICIO */}
          {activeSection === 'inicio' && estadisticas && !loading && (
            <div>
              <h2 style={{ marginBottom: '20px' }}>Dashboard General</h2>
              
              {/* Tarjetas de estadísticas */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '20px',
                marginBottom: '30px'
              }}>
                <div className="card" style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '48px', marginBottom: '10px' }}>👥</div>
                  <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#667eea' }}>
                    {estadisticas.total_estudiantes}
                  </div>
                  <div style={{ color: '#718096' }}>Total Estudiantes</div>
                </div>
                
                <div className="card" style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '48px', marginBottom: '10px' }}>⏳</div>
                  <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#ed8936' }}>
                    {estadisticas.pendientes_revision}
                  </div>
                  <div style={{ color: '#718096' }}>Pendientes Revisión</div>
                </div>
                
                <div className="card" style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '48px', marginBottom: '10px' }}>✅</div>
                  <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#48bb78' }}>
                    {estadisticas.aprobados}
                  </div>
                  <div style={{ color: '#718096' }}>Aprobados</div>
                </div>
                
                <div className="card" style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '48px', marginBottom: '10px' }}>📧</div>
                  <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#4299e1' }}>
                    {estadisticas.enviados}
                  </div>
                  <div style={{ color: '#718096' }}>Enviados</div>
                </div>
              </div>

              {/* Gráfico de especialidades */}
              <div className="card">
                <h3 style={{ marginBottom: '20px' }}>Estudiantes por Especialidad</h3>
                <div style={{ display: 'grid', gap: '10px' }}>
                  {Object.entries(estadisticas.por_especialidad || {}).map(([esp, count]) => (
                    <div key={esp} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '10px',
                      background: '#f7fafc',
                      borderRadius: '5px'
                    }}>
                      <span>{esp}</span>
                      <span style={{ fontWeight: 'bold', color: '#667eea' }}>{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* SECCIÓN: ESTUDIANTES */}
          {activeSection === 'estudiantes' && !loading && (
            <div className="card">
              <h2 style={{ marginBottom: '20px' }}>Gestión de Estudiantes</h2>
              <table className="table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Especialidad</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {estudiantes.map(est => (
                    <tr key={est.id}>
                      <td>#{est.id}</td>
                      <td>{est.nombre_completo}</td>
                      <td>{est.email}</td>
                      <td>{est.especialidad_interes}</td>
                      <td>
                        <span className={`badge ${
                          est.estado_procesamiento === 'aprobado_admin' ? 'badge-success' :
                          est.estado_procesamiento === 'pendiente_revision_admin' ? 'badge-warning' :
                          'badge-info'
                        }`}>
                          {est.estado_procesamiento}
                        </span>
                      </td>
                      <td>
                        <button className="btn" style={{ padding: '5px 10px', fontSize: '12px' }}>
                          Ver Detalles
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* SECCIÓN: CURSOS */}
          {activeSection === 'cursos' && !loading && (
            <div>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '20px'
              }}>
                <h2>Gestión de Cursos</h2>
                <button
                  className="btn btn-primary"
                  onClick={() => setShowModal('curso')}
                >
                  + Nuevo Curso
                </button>
              </div>

              <div className="card">
                <table className="table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Nombre</th>
                      <th>Escuela</th>
                      <th>Ciudad</th>
                      <th>Precio</th>
                      <th>Duración</th>
                      <th>Estado</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {cursos.map(curso => (
                      <tr key={curso.id}>
                        <td>#{curso.id}</td>
                        <td>{curso.nombre}</td>
                        <td>{curso.escuela}</td>
                        <td>{curso.ciudad}</td>
                        <td>{curso.precio}€</td>
                        <td>{curso.duracion_meses}m</td>
                        <td>
                          <span className={`badge ${curso.disponible ? 'badge-success' : 'badge-danger'}`}>
                            {curso.disponible ? 'Activo' : 'Inactivo'}
                          </span>
                        </td>
                        <td>
                          <button className="btn" style={{ padding: '5px 10px', fontSize: '12px' }}>
                            Editar
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* SECCIÓN: ALOJAMIENTO */}
          {activeSection === 'alojamiento' && !loading && (
            <div>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '20px'
              }}>
                <h2>Gestión de Alojamientos</h2>
                <button
                  className="btn btn-primary"
                  onClick={() => setShowModal('alojamiento')}
                >
                  + Nuevo Alojamiento
                </button>
              </div>

              <div style={{ display: 'grid', gap: '20px' }}>
                {alojamientos.map(aloj => (
                  <div key={aloj.id} className="card">
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <div>
                        <h3>{aloj.tipo.replace('_', ' ')}</h3>
                        <p style={{ color: '#718096' }}>
                          📍 {aloj.direccion}, {aloj.ciudad}
                        </p>
                        <div style={{ marginTop: '10px' }}>
                          <strong>{aloj.precio_mensual}€/mes</strong> •
                          {aloj.num_habitaciones} hab • {aloj.metros_cuadrados}m²
                        </div>
                      </div>
                      <div>
                        <span className={`badge ${aloj.disponible ? 'badge-success' : 'badge-danger'}`}>
                          {aloj.disponible ? 'Disponible' : 'Ocupado'}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* SECCIÓN: REPORTES */}
          {activeSection === 'reportes' && reportes && !loading && (
            <div>
              <h2 style={{ marginBottom: '20px' }}>Reportes y Análisis</h2>
              
              <div className="card">
                <h3>Resumen Ejecutivo</h3>
                <pre style={{ background: '#f7fafc', padding: '20px', borderRadius: '5px', overflow: 'auto' }}>
                  {JSON.stringify(reportes.resumen_ejecutivo, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Modal para crear curso */}
      {showModal === 'curso' && (
        <Modal onClose={() => setShowModal(null)}>
          <FormularioCurso onSubmit={crearCurso} onCancel={() => setShowModal(null)} />
        </Modal>
      )}

      {/* Modal para crear alojamiento */}
      {showModal === 'alojamiento' && (
        <Modal onClose={() => setShowModal(null)}>
          <FormularioAlojamiento onSubmit={crearAlojamiento} onCancel={() => setShowModal(null)} />
        </Modal>
      )}
    </div>
  )
}

// Componente Modal
function Modal({ children, onClose }) {
  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0,0,0,0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }} onClick={onClose}>
      <div
        className="card"
        style={{ maxWidth: '600px', width: '90%', maxHeight: '90vh', overflow: 'auto' }}
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </div>
    </div>
  )
}

// Formulario de curso
function FormularioCurso({ onSubmit, onCancel }) {
  const [datos, setDatos] = useState({
    nombre: '',
    escuela: '',
    ciudad: '',
    especialidad: '',
    precio: '',
    duracion_meses: '',
    nivel_minimo_espanol: 'B1',
    descripcion: '',
    requisitos: ''
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit({
      ...datos,
      precio: parseFloat(datos.precio),
      duracion_meses: parseInt(datos.duracion_meses)
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2 style={{ marginBottom: '20px' }}>Nuevo Curso</h2>
      
      <div className="form-group">
        <label>Nombre del Curso *</label>
        <input
          type="text"
          value={datos.nombre}
          onChange={(e) => setDatos({ ...datos, nombre: e.target.value })}
          required
        />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
        <div className="form-group">
          <label>Escuela *</label>
          <input
            type="text"
            value={datos.escuela}
            onChange={(e) => setDatos({ ...datos, escuela: e.target.value })}
            required
          />
        </div>

        <div className="form-group">
          <label>Ciudad *</label>
          <input
            type="text"
            value={datos.ciudad}
            onChange={(e) => setDatos({ ...datos, ciudad: e.target.value })}
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label>Especialidad *</label>
        <input
          type="text"
          value={datos.especialidad}
          onChange={(e) => setDatos({ ...datos, especialidad: e.target.value })}
          required
        />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
        <div className="form-group">
          <label>Precio (€) *</label>
          <input
            type="number"
            value={datos.precio}
            onChange={(e) => setDatos({ ...datos, precio: e.target.value })}
            required
          />
        </div>

        <div className="form-group">
          <label>Duración (meses) *</label>
          <input
            type="number"
            value={datos.duracion_meses}
            onChange={(e) => setDatos({ ...datos, duracion_meses: e.target.value })}
            required
          />
        </div>
      </div>

      <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
        <button type="submit" className="btn btn-primary">
          Crear Curso
        </button>
        <button type="button" className="btn" onClick={onCancel}>
          Cancelar
        </button>
      </div>
    </form>
  )
}

// Formulario de alojamiento
function FormularioAlojamiento({ onSubmit, onCancel }) {
  const [datos, setDatos] = useState({
    tipo: 'piso_compartido',
    direccion: '',
    ciudad: '',
    precio_mensual: '',
    gastos_incluidos: false,
    num_habitaciones: '1',
    num_banos: '1',
    metros_cuadrados: ''
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit({
      ...datos,
      precio_mensual: parseFloat(datos.precio_mensual),
      num_habitaciones: parseInt(datos.num_habitaciones),
      num_banos: parseInt(datos.num_banos),
      metros_cuadrados: parseInt(datos.metros_cuadrados)
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2 style={{ marginBottom: '20px' }}>Nuevo Alojamiento</h2>
      
      <div className="form-group">
        <label>Tipo *</label>
        <select
          value={datos.tipo}
          onChange={(e) => setDatos({ ...datos, tipo: e.target.value })}
          required
        >
          <option value="piso_compartido">Piso Compartido</option>
          <option value="estudio">Estudio</option>
          <option value="residencia">Residencia</option>
          <option value="habitacion">Habitación</option>
        </select>
      </div>

      <div className="form-group">
        <label>Dirección *</label>
        <input
          type="text"
          value={datos.direccion}
          onChange={(e) => setDatos({ ...datos, direccion: e.target.value })}
          required
        />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
        <div className="form-group">
          <label>Ciudad *</label>
          <input
            type="text"
            value={datos.ciudad}
            onChange={(e) => setDatos({ ...datos, ciudad: e.target.value })}
            required
          />
        </div>

        <div className="form-group">
          <label>Precio Mensual (€) *</label>
          <input
            type="number"
            value={datos.precio_mensual}
            onChange={(e) => setDatos({ ...datos, precio_mensual: e.target.value })}
            required
          />
        </div>
      </div>

      <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
        <button type="submit" className="btn btn-primary">
          Crear Alojamiento
        </button>
        <button type="button" className="btn" onClick={onCancel}>
          Cancelar
        </button>
      </div>
    </form>
  )
}

export default DashboardAdminExpandido
