import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function DashboardUsuario({ estudianteId }) {
  const [estudiante, setEstudiante] = useState(null)
  const [cursos, setCursos] = useState([])
  const [fondos, setFondos] = useState(null)
  const [documentos, setDocumentos] = useState(null)
  const [alojamientos, setAlojamientos] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('inicio')
  const navigate = useNavigate()

  useEffect(() => {
    cargarDatos()
  }, [estudianteId])

  const cargarDatos = async () => {
    try {
      const [estRes, cursosRes, fondosRes, docsRes] = await Promise.all([
        axios.get(`/api/estudiantes/${estudianteId}`),
        axios.get('/api/cursos', {
          params: { especialidad: null, limit: 10 }
        }),
        axios.get(`/api/estudiantes/${estudianteId}/fondos`),
        axios.get(`/api/estudiantes/${estudianteId}/documentos`)
      ])

      setEstudiante(estRes.data)
      setCursos(cursosRes.data.cursos)
      setFondos(fondosRes.data)
      setDocumentos(docsRes.data)
    } catch (err) {
      console.error('Error cargando datos:', err)
    } finally {
      setLoading(false)
    }
  }

  const buscarAlojamientos = async () => {
    if (estudiante?.curso_seleccionado_id) {
      const cursoRes = await axios.get(`/api/cursos/${estudiante.curso_seleccionado_id}`)
      const alojRes = await axios.get('/api/alojamientos', {
        params: { ciudad: cursoRes.data.ciudad }
      })
      setAlojamientos(alojRes.data.alojamientos)
    }
  }

  const subirDocumento = async (tipo, archivo) => {
    const formData = new FormData()
    formData.append('archivo', archivo)
    formData.append('tipo_documento', tipo)

    try {
      await axios.post(
        `/api/estudiantes/${estudianteId}/documentos/upload`,
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      )
      alert('Documento subido correctamente')
      cargarDatos()
    } catch (err) {
      alert('Error al subir documento')
    }
  }

  if (loading) {
    return <div className="loading">Cargando tu información...</div>
  }

  return (
    <div className="container" style={{ paddingBottom: '40px' }}>
      {/* Header Usuario */}
      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        padding: '40px',
        borderRadius: '10px',
        marginBottom: '30px'
      }}>
        <h1 style={{ marginBottom: '10px' }}>
          Hola, {estudiante?.nombre_completo}! 👋
        </h1>
        <p style={{ fontSize: '18px', opacity: 0.9 }}>
          Bienvenido a tu portal de estudiante
        </p>
      </div>

      {/* Tabs de navegación */}
      <div style={{
        background: 'white',
        borderRadius: '10px',
        padding: '10px',
        marginBottom: '30px',
        display: 'flex',
        gap: '10px',
        flexWrap: 'wrap'
      }}>
        {['inicio', 'cursos', 'documentos', 'fondos', 'alojamiento'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className="btn"
            style={{
              background: activeTab === tab ? '#667eea' : 'transparent',
              color: activeTab === tab ? 'white' : '#2d3748',
              border: activeTab === tab ? 'none' : '2px solid #e2e8f0'
            }}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* TAB: Inicio */}
      {activeTab === 'inicio' && (
        <div>
          {/* Estado de Solicitud */}
          <div className="card">
            <h2 style={{ marginBottom: '20px' }}>📊 Estado de tu Solicitud</h2>
            <div style={{
              background: '#f7fafc',
              padding: '30px',
              borderRadius: '10px',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '48px', marginBottom: '15px' }}>
                {estudiante?.estado_procesamiento === 'aprobado_admin' ? '✅' :
                 estudiante?.estado_procesamiento === 'pendiente_revision_admin' ? '⏳' :
                 estudiante?.estado_procesamiento === 'enviado_estudiante' ? '📧' : '📝'}
              </div>
              <h3>{estudiante?.estado_procesamiento}</h3>
              <p style={{ color: '#718096', marginTop: '10px' }}>
                {estudiante?.estado_procesamiento === 'aprobado_admin' && 
                  '¡Felicitaciones! Tu solicitud ha sido aprobada. Revisa tu email.'}
                {estudiante?.estado_procesamiento === 'pendiente_revision_admin' && 
                  'Nuestro equipo está revisando tu solicitud. Te contactaremos pronto.'}
                {estudiante?.estado_procesamiento === 'registrado' && 
                  'Tu solicitud ha sido recibida. Estamos procesando tu información.'}
              </p>
            </div>
          </div>

          {/* Resumen Rápido */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '20px',
            marginTop: '20px'
          }}>
            <div className="card" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '36px', marginBottom: '10px' }}>📚</div>
              <h3>Cursos</h3>
              <p>{cursos.length} disponibles</p>
              <button
                className="btn btn-primary"
                onClick={() => setActiveTab('cursos')}
                style={{ marginTop: '10px' }}
              >
                Ver Cursos
              </button>
            </div>

            <div className="card" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '36px', marginBottom: '10px' }}>📄</div>
              <h3>Documentos</h3>
              <p>{documentos?.total_obligatorios || 0} requeridos</p>
              <button
                className="btn btn-primary"
                onClick={() => setActiveTab('documentos')}
                style={{ marginTop: '10px' }}
              >
                Gestionar
              </button>
            </div>

            <div className="card" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '36px', marginBottom: '10px' }}>💰</div>
              <h3>Fondos</h3>
              <p>{fondos?.porcentaje_cobertura || 0}% cubierto</p>
              <button
                className="btn btn-primary"
                onClick={() => setActiveTab('fondos')}
                style={{ marginTop: '10px' }}
              >
                Ver Detalles
              </button>
            </div>
          </div>
        </div>
      )}

      {/* TAB: Cursos */}
      {activeTab === 'cursos' && (
        <div className="card">
          <h2 style={{ marginBottom: '20px' }}>📚 Cursos Disponibles</h2>
          <div style={{ display: 'grid', gap: '20px' }}>
            {cursos.map(curso => (
              <div key={curso.id} style={{
                border: '2px solid #e2e8f0',
                borderRadius: '10px',
                padding: '20px'
              }}>
                <h3>{curso.nombre}</h3>
                <p style={{ color: '#718096', marginBottom: '10px' }}>
                  🏫 {curso.escuela} • 📍 {curso.ciudad}
                </p>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(3, 1fr)',
                  gap: '15px',
                  marginBottom: '15px'
                }}>
                  <div>
                    <strong>Precio:</strong><br />
                    {curso.precio}€
                  </div>
                  <div>
                    <strong>Duración:</strong><br />
                    {curso.duracion_meses} meses
                  </div>
                  <div>
                    <strong>Español:</strong><br />
                    {curso.nivel_minimo_espanol}
                  </div>
                </div>
                <button className="btn btn-primary">
                  Más Información
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB: Documentos */}
      {activeTab === 'documentos' && (
        <div className="card">
          <h2 style={{ marginBottom: '20px' }}>📄 Mis Documentos</h2>
          
          {documentos && (
            <>
              <div style={{
                background: '#f7fafc',
                padding: '20px',
                borderRadius: '10px',
                marginBottom: '20px'
              }}>
                <h3>Checklist de Documentos</h3>
                <p>
                  <strong>Obligatorios:</strong> {documentos.total_obligatorios} •
                  <strong> Recomendados:</strong> {documentos.total_recomendados}
                </p>
              </div>

              <div style={{ marginBottom: '30px' }}>
                <h3 style={{ marginBottom: '15px' }}>Subir Documento</h3>
                <input
                  type="file"
                  onChange={(e) => {
                    const tipo = prompt('Tipo de documento (ej: pasaporte, titulo):')
                    if (tipo && e.target.files[0]) {
                      subirDocumento(tipo, e.target.files[0])
                    }
                  }}
                  style={{
                    padding: '12px',
                    border: '2px solid #e2e8f0',
                    borderRadius: '5px',
                    width: '100%'
                  }}
                />
              </div>

              <p style={{ color: '#718096', fontSize: '14px' }}>
                * Los documentos serán revisados por nuestro equipo
              </p>
            </>
          )}
        </div>
      )}

      {/* TAB: Fondos */}
      {activeTab === 'fondos' && fondos && (
        <div className="card">
          <h2 style={{ marginBottom: '20px' }}>💰 Situación Económica</h2>
          
          <div style={{
            background: fondos.fondos_suficientes ? '#c6f6d5' : '#fed7d7',
            color: fondos.fondos_suficientes ? '#22543d' : '#742a2a',
            padding: '20px',
            borderRadius: '10px',
            marginBottom: '20px',
            textAlign: 'center'
          }}>
            <h3>{fondos.fondos_suficientes ? '✅ Fondos Suficientes' : '⚠️ Fondos Insuficientes'}</h3>
            <p style={{ fontSize: '18px', marginTop: '10px' }}>
              {fondos.fondos_disponibles.toFixed(2)}€ / {fondos.fondos_minimos_requeridos.toFixed(2)}€
            </p>
            <div style={{
              width: '100%',
              height: '20px',
              background: 'rgba(0,0,0,0.1)',
              borderRadius: '10px',
              marginTop: '15px',
              overflow: 'hidden'
            }}>
              <div style={{
                width: `${Math.min(fondos.porcentaje_cobertura, 100)}%`,
                height: '100%',
                background: fondos.fondos_suficientes ? '#48bb78' : '#f56565',
                transition: 'width 0.3s'
              }} />
            </div>
            <p style={{ marginTop: '10px' }}>{fondos.porcentaje_cobertura.toFixed(0)}% cubierto</p>
          </div>

          <h3 style={{ marginBottom: '15px' }}>Desglose de Costos</h3>
          <table className="table">
            <tbody>
              <tr>
                <td>Matrícula</td>
                <td style={{ textAlign: 'right' }}>{fondos.desglose.matricula.toFixed(2)}€</td>
              </tr>
              <tr>
                <td>Manutención (6 meses)</td>
                <td style={{ textAlign: 'right' }}>{fondos.desglose.manutencion.toFixed(2)}€</td>
              </tr>
              <tr>
                <td>Alojamiento</td>
                <td style={{ textAlign: 'right' }}>{fondos.desglose.alojamiento.toFixed(2)}€</td>
              </tr>
              <tr>
                <td>Seguro</td>
                <td style={{ textAlign: 'right' }}>{fondos.desglose.seguro.toFixed(2)}€</td>
              </tr>
              <tr style={{ borderTop: '2px solid #2d3748', fontWeight: 'bold' }}>
                <td>TOTAL</td>
                <td style={{ textAlign: 'right' }}>{fondos.fondos_minimos_requeridos.toFixed(2)}€</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {/* TAB: Alojamiento */}
      {activeTab === 'alojamiento' && (
        <div className="card">
          <h2 style={{ marginBottom: '20px' }}>🏠 Alojamiento</h2>
          
          {alojamientos.length === 0 && (
            <div style={{ textAlign: 'center', padding: '40px' }}>
              <button
                className="btn btn-primary"
                onClick={buscarAlojamientos}
              >
                Buscar Alojamientos
              </button>
            </div>
          )}

          {alojamientos.length > 0 && (
            <div style={{ display: 'grid', gap: '20px' }}>
              {alojamientos.map(aloj => (
                <div key={aloj.id} style={{
                  border: '2px solid #e2e8f0',
                  borderRadius: '10px',
                  padding: '20px'
                }}>
                  <h3>{aloj.tipo.replace('_', ' ')}</h3>
                  <p style={{ color: '#718096' }}>
                    📍 {aloj.direccion}, {aloj.ciudad}
                  </p>
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(3, 1fr)',
                    gap: '15px',
                    marginTop: '15px'
                  }}>
                    <div>
                      <strong>Precio:</strong><br />
                      {aloj.precio_mensual}€/mes
                    </div>
                    <div>
                      <strong>Habitaciones:</strong><br />
                      {aloj.num_habitaciones}
                    </div>
                    <div>
                      <strong>Tamaño:</strong><br />
                      {aloj.metros_cuadrados}m²
                    </div>
                  </div>
                  <button
                    className="btn btn-primary"
                    style={{ marginTop: '15px' }}
                  >
                    Más Información
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default DashboardUsuario
