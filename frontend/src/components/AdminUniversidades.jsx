import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './AdminUniversidades.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'

function AdminUniversidades() {
  const [universidades, setUniversidades] = useState([])
  const [loading, setLoading] = useState(false)
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [editando, setEditando] = useState(null)
  const [filtros, setFiltros] = useState({
    ciudad: '',
    comunidad: '',
    tipo: ''
  })

  const [formulario, setFormulario] = useState({
    nombre: '',
    siglas: '',
    ciudad: '',
    comunidad_autonoma: '',
    tipo: 'publica',
    url_oficial: '',
    email_contacto: '',
    telefono: '',
    descripcion: '',
    ranking_nacional: '',
    total_alumnos: '',
    acepta_extranjeros: true,
    requisitos_extranjeros: '',
    metodo_scraping: 'beautifulsoup'
  })

  const comunidades = [
    'Andalucía', 'Aragón', 'Asturias', 'Islas Baleares', 'Canarias',
    'Cantabria', 'Castilla-La Mancha', 'Castilla y León', 'Cataluña',
    'Comunidad Valenciana', 'Extremadura', 'Galicia', 'La Rioja',
    'Comunidad de Madrid', 'Murcia', 'Navarra', 'País Vasco'
  ]

  useEffect(() => {
    cargarUniversidades()
  }, [])

  const cargarUniversidades = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (filtros.ciudad) params.append('ciudad', filtros.ciudad)
      if (filtros.comunidad) params.append('comunidad', filtros.comunidad)
      if (filtros.tipo) params.append('tipo', filtros.tipo)

      const response = await axios.get(`${API_URL}/api/universidades?${params}`)
      if (response.data.success) {
        setUniversidades(response.data.universidades)
      }
    } catch (error) {
      console.error('Error cargando universidades:', error)
      alert('Error al cargar universidades')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormulario(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (editando) {
        // Actualizar
        const response = await axios.put(
          `${API_URL}/api/admin/universidades/${editando}`,
          formulario
        )
        if (response.data.success) {
          alert('Universidad actualizada exitosamente')
          resetFormulario()
          cargarUniversidades()
        }
      } else {
        // Crear nueva
        const response = await axios.post(
          `${API_URL}/api/admin/universidades`,
          formulario
        )
        if (response.data.success) {
          alert(`Universidad "${response.data.nombre}" creada exitosamente`)
          resetFormulario()
          cargarUniversidades()
        }
      }
    } catch (error) {
      console.error('Error guardando universidad:', error)
      alert('Error al guardar universidad: ' + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  const editarUniversidad = (universidad) => {
    setFormulario({
      nombre: universidad.nombre,
      siglas: universidad.siglas || '',
      ciudad: universidad.ciudad || '',
      comunidad_autonoma: universidad.comunidad_autonoma || '',
      tipo: universidad.tipo || 'publica',
      url_oficial: universidad.url_oficial || '',
      email_contacto: universidad.email_contacto || '',
      telefono: universidad.telefono || '',
      descripcion: universidad.descripcion || '',
      ranking_nacional: universidad.ranking_nacional || '',
      total_alumnos: universidad.total_alumnos || '',
      acepta_extranjeros: universidad.acepta_extranjeros !== false,
      requisitos_extranjeros: universidad.requisitos_extranjeros || '',
      metodo_scraping: universidad.metodo_scraping || 'beautifulsoup'
    })
    setEditando(universidad.id)
    setMostrarFormulario(true)
  }

  const eliminarUniversidad = async (id, nombre) => {
    if (!confirm(`¿Desactivar universidad "${nombre}"?`)) return

    try {
      const response = await axios.delete(`${API_URL}/api/admin/universidades/${id}`)
      if (response.data.success) {
        alert('Universidad desactivada')
        cargarUniversidades()
      }
    } catch (error) {
      console.error('Error eliminando universidad:', error)
      alert('Error al eliminar universidad')
    }
  }

  const resetFormulario = () => {
    setFormulario({
      nombre: '',
      siglas: '',
      ciudad: '',
      comunidad_autonoma: '',
      tipo: 'publica',
      url_oficial: '',
      email_contacto: '',
      telefono: '',
      descripcion: '',
      ranking_nacional: '',
      total_alumnos: '',
      acepta_extranjeros: true,
      requisitos_extranjeros: '',
      metodo_scraping: 'beautifulsoup'
    })
    setEditando(null)
    setMostrarFormulario(false)
  }

  return (
    <div className="admin-universidades-container">
      <div className="header-admin-uni">
        <h1>🎓 Gestión de Universidades</h1>
        <button 
          className="btn-nuevo"
          onClick={() => {
            resetFormulario()
            setMostrarFormulario(!mostrarFormulario)
          }}
        >
          {mostrarFormulario ? '❌ Cancelar' : '➕ Nueva Universidad'}
        </button>
      </div>

      {mostrarFormulario && (
        <div className="formulario-universidad">
          <h2>{editando ? '✏️ Editar Universidad' : '➕ Nueva Universidad'}</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group">
                <label>Nombre Completo *</label>
                <input
                  type="text"
                  name="nombre"
                  value={formulario.nombre}
                  onChange={handleInputChange}
                  required
                  placeholder="Universidad Complutense de Madrid"
                />
              </div>

              <div className="form-group">
                <label>Siglas</label>
                <input
                  type="text"
                  name="siglas"
                  value={formulario.siglas}
                  onChange={handleInputChange}
                  placeholder="UCM"
                />
              </div>

              <div className="form-group">
                <label>Ciudad *</label>
                <input
                  type="text"
                  name="ciudad"
                  value={formulario.ciudad}
                  onChange={handleInputChange}
                  required
                  placeholder="Madrid"
                />
              </div>

              <div className="form-group">
                <label>Comunidad Autónoma *</label>
                <select
                  name="comunidad_autonoma"
                  value={formulario.comunidad_autonoma}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Seleccionar...</option>
                  {comunidades.map(com => (
                    <option key={com} value={com}>{com}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Tipo *</label>
                <select
                  name="tipo"
                  value={formulario.tipo}
                  onChange={handleInputChange}
                  required
                >
                  <option value="publica">Pública</option>
                  <option value="privada">Privada</option>
                </select>
              </div>

              <div className="form-group">
                <label>URL Oficial *</label>
                <input
                  type="url"
                  name="url_oficial"
                  value={formulario.url_oficial}
                  onChange={handleInputChange}
                  required
                  placeholder="https://www.universidad.es"
                />
              </div>

              <div className="form-group">
                <label>Email Contacto</label>
                <input
                  type="email"
                  name="email_contacto"
                  value={formulario.email_contacto}
                  onChange={handleInputChange}
                  placeholder="info@universidad.es"
                />
              </div>

              <div className="form-group">
                <label>Teléfono</label>
                <input
                  type="tel"
                  name="telefono"
                  value={formulario.telefono}
                  onChange={handleInputChange}
                  placeholder="+34 91 123 4567"
                />
              </div>

              <div className="form-group">
                <label>Ranking Nacional</label>
                <input
                  type="number"
                  name="ranking_nacional"
                  value={formulario.ranking_nacional}
                  onChange={handleInputChange}
                  placeholder="1-100"
                />
              </div>

              <div className="form-group">
                <label>Total Alumnos</label>
                <input
                  type="number"
                  name="total_alumnos"
                  value={formulario.total_alumnos}
                  onChange={handleInputChange}
                  placeholder="50000"
                />
              </div>

              <div className="form-group full-width">
                <label>Descripción</label>
                <textarea
                  name="descripcion"
                  value={formulario.descripcion}
                  onChange={handleInputChange}
                  rows="3"
                  placeholder="Breve descripción de la universidad..."
                />
              </div>

              <div className="form-group full-width">
                <label>
                  <input
                    type="checkbox"
                    name="acepta_extranjeros"
                    checked={formulario.acepta_extranjeros}
                    onChange={handleInputChange}
                  />
                  {' '}Acepta Estudiantes Extranjeros
                </label>
              </div>

              {formulario.acepta_extranjeros && (
                <div className="form-group full-width">
                  <label>Requisitos para Extranjeros</label>
                  <textarea
                    name="requisitos_extranjeros"
                    value={formulario.requisitos_extranjeros}
                    onChange={handleInputChange}
                    rows="3"
                    placeholder="Visa de estudiante, nivel B2 español..."
                  />
                </div>
              )}
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-guardar" disabled={loading}>
                {loading ? '⏳ Guardando...' : (editando ? '💾 Actualizar' : '➕ Crear')}
              </button>
              <button type="button" className="btn-cancelar" onClick={resetFormulario}>
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="filtros-admin">
        <input
          type="text"
          placeholder="🔍 Buscar por ciudad..."
          value={filtros.ciudad}
          onChange={(e) => setFiltros({...filtros, ciudad: e.target.value})}
        />
        <select
          value={filtros.comunidad}
          onChange={(e) => setFiltros({...filtros, comunidad: e.target.value})}
        >
          <option value="">Todas las comunidades</option>
          {comunidades.map(com => (
            <option key={com} value={com}>{com}</option>
          ))}
        </select>
        <select
          value={filtros.tipo}
          onChange={(e) => setFiltros({...filtros, tipo: e.target.value})}
        >
          <option value="">Todos los tipos</option>
          <option value="publica">Pública</option>
          <option value="privada">Privada</option>
        </select>
        <button onClick={cargarUniversidades} className="btn-buscar">
          🔍 Buscar
        </button>
      </div>

      {loading ? (
        <div className="loading">Cargando...</div>
      ) : (
        <div className="tabla-universidades">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Siglas</th>
                <th>Ciudad</th>
                <th>Comunidad</th>
                <th>Tipo</th>
                <th>Alumnos</th>
                <th>Ranking</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {universidades.map(uni => (
                <tr key={uni.id}>
                  <td>{uni.id}</td>
                  <td>{uni.nombre}</td>
                  <td><strong>{uni.siglas}</strong></td>
                  <td>{uni.ciudad}</td>
                  <td>{uni.comunidad_autonoma}</td>
                  <td>
                    <span className={`badge-tipo ${uni.tipo}`}>
                      {uni.tipo}
                    </span>
                  </td>
                  <td>{uni.total_alumnos?.toLocaleString() || 'N/A'}</td>
                  <td>#{uni.ranking_nacional || 'N/A'}</td>
                  <td className="acciones">
                    <button 
                      className="btn-editar"
                      onClick={() => editarUniversidad(uni)}
                      title="Editar"
                    >
                      ✏️
                    </button>
                    <button 
                      className="btn-eliminar"
                      onClick={() => eliminarUniversidad(uni.id, uni.nombre)}
                      title="Desactivar"
                    >
                      🗑️
                    </button>
                    <a 
                      href={uni.url_oficial}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn-web"
                      title="Ver sitio web"
                    >
                      🌐
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {universidades.length === 0 && (
            <div className="sin-resultados">
              <p>No se encontraron universidades</p>
            </div>
          )}
        </div>
      )}

      <div className="stats-footer">
        <p><strong>Total:</strong> {universidades.length} universidades</p>
      </div>
    </div>
  )
}

export default AdminUniversidades
