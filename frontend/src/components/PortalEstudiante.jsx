import React, { useState } from 'react'
import axios from 'axios'

function PortalEstudiante() {
  const [estudianteId, setEstudianteId] = useState('')
  const [estudiante, setEstudiante] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleBuscar = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setEstudiante(null)

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}/estado`)
      setEstudiante(response.data)
    } catch (err) {
      setError('No se encontró ningún estudiante con ese ID. Verifica el número.')
    } finally {
      setLoading(false)
    }
  }

  const getEstadoBadge = (estado) => {
    const badges = {
      registrado: { class: 'badge-info', text: '📝 Registrado' },
      procesado_automaticamente: { class: 'badge-warning', text: '⚙️ En Proceso' },
      pendiente_revision_admin: { class: 'badge-warning', text: '👀 En Revisión' },
      aprobado_admin: { class: 'badge-success', text: '✅ Aprobado' },
      enviado_estudiante: { class: 'badge-success', text: '📧 Información Enviada' },
      rechazado_admin: { class: 'badge-danger', text: '⚠️ Requiere Información' },
    }
    return badges[estado] || { class: 'badge-info', text: estado }
  }

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: '700px', margin: '0 auto' }}>
        <h2 style={{ marginBottom: '10px' }}>🔍 Consultar Estado</h2>
        <p style={{ color: '#718096', marginBottom: '30px' }}>
          Ingresa tu ID de seguimiento para ver el estado de tu solicitud
        </p>

        <form onSubmit={handleBuscar} style={{ marginBottom: '30px' }}>
          <div style={{ display: 'flex', gap: '10px' }}>
            <input
              type="number"
              value={estudianteId}
              onChange={(e) => setEstudianteId(e.target.value)}
              placeholder="Ingresa tu ID de seguimiento (ej: 1)"
              required
              style={{
                flex: 1,
                padding: '12px',
                border: '2px solid #e2e8f0',
                borderRadius: '5px',
                fontSize: '16px',
              }}
            />
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Buscando...' : 'Buscar'}
            </button>
          </div>
        </form>

        {error && <div className="error">{error}</div>}

        {estudiante && (
          <div>
            <div style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              padding: '30px',
              borderRadius: '10px',
              marginBottom: '20px',
            }}>
              <h3 style={{ marginBottom: '15px' }}>
                Hola, {estudiante.nombre}! 👋
              </h3>
              <div style={{ fontSize: '18px', marginBottom: '10px' }}>
                Estado de tu solicitud:
              </div>
              <div style={{
                background: 'rgba(255,255,255,0.2)',
                padding: '15px',
                borderRadius: '5px',
                fontSize: '24px',
                fontWeight: 'bold',
              }}>
                {getEstadoBadge(estudiante.estado_procesamiento).text}
              </div>
            </div>

            <div style={{
              background: '#f7fafc',
              padding: '20px',
              borderRadius: '10px',
              marginBottom: '20px',
            }}>
              <p style={{ fontSize: '16px', lineHeight: '1.6', margin: 0 }}>
                {estudiante.mensaje}
              </p>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '15px',
            }}>
              <div style={{
                padding: '15px',
                background: '#edf2f7',
                borderRadius: '5px',
              }}>
                <div style={{ fontSize: '12px', color: '#718096', marginBottom: '5px' }}>
                  Estado de Visa
                </div>
                <div style={{ fontSize: '18px', fontWeight: '600' }}>
                  {estudiante.estado_visa}
                </div>
              </div>

              <div style={{
                padding: '15px',
                background: '#edf2f7',
                borderRadius: '5px',
              }}>
                <div style={{ fontSize: '12px', color: '#718096', marginBottom: '5px' }}>
                  Fecha de Registro
                </div>
                <div style={{ fontSize: '18px', fontWeight: '600' }}>
                  {new Date(estudiante.fecha_registro).toLocaleDateString('es-ES')}
                </div>
              </div>
            </div>

            {estudiante.curso_seleccionado && (
              <div style={{
                marginTop: '20px',
                padding: '15px',
                background: '#e6fffa',
                borderRadius: '5px',
                border: '2px solid #81e6d9',
              }}>
                <div style={{ fontSize: '14px', fontWeight: '600', marginBottom: '5px' }}>
                  ✅ Curso Seleccionado
                </div>
                <div>
                  Curso ID: {estudiante.curso_seleccionado}
                </div>
              </div>
            )}
          </div>
        )}

        {!estudiante && !error && (
          <div style={{ textAlign: 'center', padding: '40px', color: '#718096' }}>
            <div style={{ fontSize: '64px', marginBottom: '15px' }}>📋</div>
            <p>Ingresa tu ID de seguimiento para ver tu estado</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default PortalEstudiante
