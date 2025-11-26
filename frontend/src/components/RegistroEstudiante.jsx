import React, { useState } from 'react'
import axios from 'axios'

function RegistroEstudiante({ onRegistro }) {
  const [formData, setFormData] = useState({
    nombre_completo: '',
    numero_pasaporte: '',
    edad: '',
    nacionalidad: 'Cubana',
    ciudad_origen: '',
    email: '',
    telefono: '',
    especialidad_interes: '',
    nivel_espanol: 'B1',
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [estudianteId, setEstudianteId] = useState(null)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await axios.post('/api/estudiantes', {
        ...formData,
        edad: parseInt(formData.edad),
      })

      setSuccess(true)
      setEstudianteId(response.data.id)
      setFormData({
        nombre_completo: '',
        numero_pasaporte: '',
        edad: '',
        nacionalidad: 'Cubana',
        ciudad_origen: '',
        email: '',
        telefono: '',
        especialidad_interes: '',
        nivel_espanol: 'B1',
      })
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Error al registrar. Intenta de nuevo.'
      )
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    // Llamar callback si existe
    if (onRegistro) {
      onRegistro(estudianteId)
    }

    return (
      <div className="container">
        <div className="card" style={{ maxWidth: '600px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '64px', marginBottom: '20px' }}>✅</div>
            <h2 style={{ color: '#48bb78', marginBottom: '20px' }}>
              ¡Registro Exitoso!
            </h2>
            <p style={{ marginBottom: '20px', fontSize: '18px' }}>
              Tu solicitud ha sido recibida correctamente.
            </p>
            <div
              style={{
                background: '#f7fafc',
                padding: '20px',
                borderRadius: '5px',
                marginBottom: '20px',
              }}
            >
              <p style={{ marginBottom: '10px' }}>
                <strong>Tu ID de seguimiento:</strong>
              </p>
              <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#667eea' }}>
                #{estudianteId}
              </p>
              <p style={{ fontSize: '14px', color: '#718096', marginTop: '10px' }}>
                Guarda este número para consultar tu estado
              </p>
            </div>
            <p style={{ marginBottom: '30px' }}>
              Recibirás un email de confirmación pronto. Nuestro equipo revisará
              tu perfil y te contactaremos en las próximas 24-48 horas.
            </p>
            <button
              className="btn btn-primary"
              onClick={() => window.location.href = '/estudiante/dashboard'}
              style={{ marginBottom: '10px', width: '100%' }}
            >
              Ir a Mi Portal
            </button>
            <button
              className="btn"
              onClick={() => {
                setSuccess(false)
                setEstudianteId(null)
              }}
              style={{ width: '100%', background: 'white', color: '#667eea', border: '2px solid #667eea' }}
            >
              Registrar Otro Estudiante
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: '700px', margin: '0 auto' }}>
        <h2 style={{ marginBottom: '10px' }}>📝 Registro de Estudiante</h2>
        <p style={{ color: '#718096', marginBottom: '30px' }}>
          Completa el formulario para comenzar tu proceso de visa
        </p>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Nombre Completo *</label>
            <input
              type="text"
              name="nombre_completo"
              value={formData.nombre_completo}
              onChange={handleChange}
              required
              placeholder="Ej: Carlos Pérez García"
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div className="form-group">
              <label>Número de Pasaporte *</label>
              <input
                type="text"
                name="numero_pasaporte"
                value={formData.numero_pasaporte}
                onChange={handleChange}
                required
                placeholder="ABC123456"
              />
            </div>

            <div className="form-group">
              <label>Edad *</label>
              <input
                type="number"
                name="edad"
                value={formData.edad}
                onChange={handleChange}
                required
                min="18"
                max="65"
                placeholder="24"
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div className="form-group">
              <label>Nacionalidad *</label>
              <select
                name="nacionalidad"
                value={formData.nacionalidad}
                onChange={handleChange}
                required
              >
                <option value="Cubana">Cubana</option>
                <option value="Mexicana">Mexicana</option>
                <option value="Colombiana">Colombiana</option>
                <option value="Argentina">Argentina</option>
                <option value="Venezolana">Venezolana</option>
                <option value="Otra">Otra</option>
              </select>
            </div>

            <div className="form-group">
              <label>Ciudad de Origen *</label>
              <input
                type="text"
                name="ciudad_origen"
                value={formData.ciudad_origen}
                onChange={handleChange}
                required
                placeholder="La Habana"
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div className="form-group">
              <label>Email *</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="tu@email.com"
              />
            </div>

            <div className="form-group">
              <label>Teléfono *</label>
              <input
                type="tel"
                name="telefono"
                value={formData.telefono}
                onChange={handleChange}
                required
                placeholder="+53 5512 3456"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Especialidad de Interés *</label>
            <input
              type="text"
              name="especialidad_interes"
              value={formData.especialidad_interes}
              onChange={handleChange}
              required
              placeholder="Ej: Ingeniería de Software, Medicina, Administración..."
            />
          </div>

          <div className="form-group">
            <label>Nivel de Español *</label>
            <select
              name="nivel_espanol"
              value={formData.nivel_espanol}
              onChange={handleChange}
              required
            >
              <option value="Nativo">Nativo</option>
              <option value="C2">C2 - Dominio</option>
              <option value="C1">C1 - Avanzado</option>
              <option value="B2">B2 - Intermedio Alto</option>
              <option value="B1">B1 - Intermedio</option>
              <option value="A2">A2 - Básico Alto</option>
              <option value="A1">A1 - Principiante</option>
            </select>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ width: '100%', marginTop: '10px' }}
          >
            {loading ? 'Registrando...' : 'Registrarse'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default RegistroEstudiante
