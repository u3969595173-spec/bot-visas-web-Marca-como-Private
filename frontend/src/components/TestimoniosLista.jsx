import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './Testimonios.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'

function TestimoniosLista() {
  const [testimonios, setTestimonios] = useState([])
  const [loading, setLoading] = useState(true)
  const [mostrarFormulario, setMostrarFormulario] = useState(false)

  const [formulario, setFormulario] = useState({
    nombre_completo: '',
    pais_origen: '',
    programa_estudio: '',
    universidad: '',
    ciudad_espana: '',
    rating: 5,
    titulo: '',
    testimonio: '',
    foto_url: '',
    email_contacto: ''
  })

  useEffect(() => {
    cargarTestimonios()
  }, [])

  const cargarTestimonios = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_URL}/api/testimonios?limit=50`)
      if (response.data.success) {
        setTestimonios(response.data.testimonios)
      }
    } catch (error) {
      console.error('Error cargando testimonios:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormulario(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/testimonios`, formulario)
      if (response.data.success) {
        alert('¡Gracias por tu testimonio! Será revisado por nuestro equipo.')
        setFormulario({
          nombre_completo: '',
          pais_origen: '',
          programa_estudio: '',
          universidad: '',
          ciudad_espana: '',
          rating: 5,
          titulo: '',
          testimonio: '',
          foto_url: '',
          email_contacto: ''
        })
        setMostrarFormulario(false)
      }
    } catch (error) {
      console.error('Error enviando testimonio:', error)
      alert('Error al enviar testimonio')
    } finally {
      setLoading(false)
    }
  }

  const renderEstrellas = (rating) => {
    return '⭐'.repeat(rating || 5)
  }

  return (
    <div className="testimonios-container">
      <div className="testimonios-header">
        <h1>⭐ Testimonios de Estudiantes</h1>
        <p>Conoce las experiencias de estudiantes que han confiado en nosotros</p>
        <button 
          className="btn-compartir-testimonio"
          onClick={() => setMostrarFormulario(!mostrarFormulario)}
        >
          {mostrarFormulario ? '❌ Cancelar' : '📝 Compartir mi experiencia'}
        </button>
      </div>

      {mostrarFormulario && (
        <div className="formulario-testimonio">
          <h2>✍️ Comparte tu experiencia</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-grid-testimonio">
              <div className="form-group">
                <label>Nombre completo *</label>
                <input
                  type="text"
                  name="nombre_completo"
                  value={formulario.nombre_completo}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>País de origen *</label>
                <input
                  type="text"
                  name="pais_origen"
                  value={formulario.pais_origen}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Programa de estudio</label>
                <input
                  type="text"
                  name="programa_estudio"
                  value={formulario.programa_estudio}
                  onChange={handleInputChange}
                />
              </div>

              <div className="form-group">
                <label>Universidad</label>
                <input
                  type="text"
                  name="universidad"
                  value={formulario.universidad}
                  onChange={handleInputChange}
                />
              </div>

              <div className="form-group">
                <label>Ciudad en España</label>
                <input
                  type="text"
                  name="ciudad_espana"
                  value={formulario.ciudad_espana}
                  onChange={handleInputChange}
                />
              </div>

              <div className="form-group">
                <label>Calificación</label>
                <select
                  name="rating"
                  value={formulario.rating}
                  onChange={handleInputChange}
                >
                  <option value="5">⭐⭐⭐⭐⭐ Excelente</option>
                  <option value="4">⭐⭐⭐⭐ Muy bueno</option>
                  <option value="3">⭐⭐⭐ Bueno</option>
                  <option value="2">⭐⭐ Regular</option>
                  <option value="1">⭐ Mejorable</option>
                </select>
              </div>

              <div className="form-group full-width">
                <label>Título (opcional)</label>
                <input
                  type="text"
                  name="titulo"
                  value={formulario.titulo}
                  onChange={handleInputChange}
                  placeholder="Ej: Excelente experiencia en Madrid"
                />
              </div>

              <div className="form-group full-width">
                <label>Tu testimonio *</label>
                <textarea
                  name="testimonio"
                  value={formulario.testimonio}
                  onChange={handleInputChange}
                  required
                  rows="5"
                  placeholder="Cuéntanos tu experiencia..."
                />
              </div>

              <div className="form-group">
                <label>URL foto (opcional)</label>
                <input
                  type="url"
                  name="foto_url"
                  value={formulario.foto_url}
                  onChange={handleInputChange}
                  placeholder="https://..."
                />
              </div>

              <div className="form-group">
                <label>Email de contacto</label>
                <input
                  type="email"
                  name="email_contacto"
                  value={formulario.email_contacto}
                  onChange={handleInputChange}
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-enviar" disabled={loading}>
                {loading ? '⏳ Enviando...' : '📤 Enviar testimonio'}
              </button>
            </div>
          </form>
        </div>
      )}

      {loading ? (
        <div className="loading-testimonios">Cargando testimonios...</div>
      ) : (
        <div className="testimonios-grid">
          {testimonios.map(t => (
            <div key={t.id} className={`testimonio-card ${t.destacado ? 'destacado' : ''}`}>
              {t.foto_url && (
                <div className="testimonio-foto">
                  <img src={t.foto_url} alt={t.nombre_completo} />
                </div>
              )}
              {!t.foto_url && (
                <div className="testimonio-avatar">
                  {t.nombre_completo.charAt(0).toUpperCase()}
                </div>
              )}

              <div className="testimonio-contenido">
                <div className="testimonio-rating">
                  {renderEstrellas(t.rating)}
                </div>
                
                {t.titulo && (
                  <h3 className="testimonio-titulo">{t.titulo}</h3>
                )}
                
                <p className="testimonio-texto">{t.testimonio}</p>
                
                <div className="testimonio-autor">
                  <strong>{t.nombre_completo}</strong>
                  <p>{t.pais_origen}</p>
                  {t.programa_estudio && (
                    <p className="testimonio-programa">{t.programa_estudio}</p>
                  )}
                  {t.universidad && (
                    <p className="testimonio-universidad">🎓 {t.universidad}</p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {!loading && testimonios.length === 0 && (
        <div className="sin-testimonios">
          <p>📭 No hay testimonios aún. ¡Sé el primero en compartir tu experiencia!</p>
        </div>
      )}
    </div>
  )
}

export default TestimoniosLista
