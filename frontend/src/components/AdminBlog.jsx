import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './AdminUniversidades.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'

function AdminBlog() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(false)
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [editando, setEditando] = useState(null)
  
  const [formulario, setFormulario] = useState({
    titulo: '',
    contenido: '',
    extracto: '',
    categoria: 'general',
    autor_nombre: 'Equipo Editorial',
    imagen_portada: '',
    meta_description: '',
    meta_keywords: '',
    publicado: false,
    destacado: false
  })

  const categorias = ['visas', 'estudios', 'vida_espana', 'noticias', 'consejos', 'general']

  useEffect(() => {
    cargarPosts()
  }, [])

  const cargarPosts = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_URL}/api/admin/blog`)
      if (response.data.success) {
        setPosts(response.data.posts)
      }
    } catch (error) {
      console.error('Error cargando posts:', error)
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
        const response = await axios.put(`${API_URL}/api/admin/blog/${editando}`, formulario)
        if (response.data.success) {
          alert('Post actualizado')
          resetFormulario()
          cargarPosts()
        }
      } else {
        const response = await axios.post(`${API_URL}/api/admin/blog`, formulario)
        if (response.data.success) {
          alert(`Post creado: ${response.data.slug}`)
          resetFormulario()
          cargarPosts()
        }
      }
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  const editarPost = (post) => {
    setFormulario({
      titulo: post.titulo,
      contenido: post.contenido || '',
      extracto: post.extracto || '',
      categoria: post.categoria || 'general',
      autor_nombre: post.autor_nombre || 'Equipo Editorial',
      imagen_portada: post.imagen_portada || '',
      meta_description: post.meta_description || '',
      meta_keywords: post.meta_keywords || '',
      publicado: post.publicado,
      destacado: post.destacado
    })
    setEditando(post.id)
    setMostrarFormulario(true)
  }

  const eliminarPost = async (id, titulo) => {
    if (!confirm(`¿Eliminar "${titulo}"?`)) return

    try {
      const response = await axios.delete(`${API_URL}/api/admin/blog/${id}`)
      if (response.data.success) {
        alert('Post eliminado')
        cargarPosts()
      }
    } catch (error) {
      alert('Error al eliminar')
    }
  }

  const resetFormulario = () => {
    setFormulario({
      titulo: '',
      contenido: '',
      extracto: '',
      categoria: 'general',
      autor_nombre: 'Equipo Editorial',
      imagen_portada: '',
      meta_description: '',
      meta_keywords: '',
      publicado: false,
      destacado: false
    })
    setEditando(null)
    setMostrarFormulario(false)
  }

  return (
    <div className="admin-universidades-container">
      <div className="header-admin-uni">
        <h1>📝 Gestión de Blog</h1>
        <button 
          className="btn-nuevo"
          onClick={() => {
            resetFormulario()
            setMostrarFormulario(!mostrarFormulario)
          }}
        >
          {mostrarFormulario ? '❌ Cancelar' : '➕ Nuevo Post'}
        </button>
      </div>

      {mostrarFormulario && (
        <div className="formulario-universidad">
          <h2>{editando ? '✏️ Editar Post' : '➕ Nuevo Post'}</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group full-width">
                <label>Título *</label>
                <input
                  type="text"
                  name="titulo"
                  value={formulario.titulo}
                  onChange={handleInputChange}
                  required
                  placeholder="Ej: Guía completa para obtener visa de estudiante"
                />
              </div>

              <div className="form-group full-width">
                <label>Contenido * (HTML permitido)</label>
                <textarea
                  name="contenido"
                  value={formulario.contenido}
                  onChange={handleInputChange}
                  required
                  rows="12"
                  placeholder="<p>Contenido del post...</p>"
                />
              </div>

              <div className="form-group full-width">
                <label>Extracto</label>
                <textarea
                  name="extracto"
                  value={formulario.extracto}
                  onChange={handleInputChange}
                  rows="3"
                  placeholder="Breve resumen del post (aparece en tarjetas)"
                />
              </div>

              <div className="form-group">
                <label>Categoría</label>
                <select
                  name="categoria"
                  value={formulario.categoria}
                  onChange={handleInputChange}
                >
                  {categorias.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Autor</label>
                <input
                  type="text"
                  name="autor_nombre"
                  value={formulario.autor_nombre}
                  onChange={handleInputChange}
                />
              </div>

              <div className="form-group full-width">
                <label>URL Imagen Portada</label>
                <input
                  type="url"
                  name="imagen_portada"
                  value={formulario.imagen_portada}
                  onChange={handleInputChange}
                  placeholder="https://..."
                />
              </div>

              <div className="form-group full-width">
                <label>Meta Description (SEO)</label>
                <input
                  type="text"
                  name="meta_description"
                  value={formulario.meta_description}
                  onChange={handleInputChange}
                  placeholder="Descripción para buscadores (max 160 caracteres)"
                  maxLength="160"
                />
              </div>

              <div className="form-group full-width">
                <label>Keywords (SEO, separadas por comas)</label>
                <input
                  type="text"
                  name="meta_keywords"
                  value={formulario.meta_keywords}
                  onChange={handleInputChange}
                  placeholder="visa estudiante, españa, universidad"
                />
              </div>

              <div className="form-group full-width">
                <label>
                  <input
                    type="checkbox"
                    name="publicado"
                    checked={formulario.publicado}
                    onChange={handleInputChange}
                  />
                  {' '}Publicado (visible para público)
                </label>
              </div>

              <div className="form-group full-width">
                <label>
                  <input
                    type="checkbox"
                    name="destacado"
                    checked={formulario.destacado}
                    onChange={handleInputChange}
                  />
                  {' '}Destacado
                </label>
              </div>
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

      {loading ? (
        <div className="loading">Cargando...</div>
      ) : (
        <div className="tabla-universidades">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Título</th>
                <th>Categoría</th>
                <th>Autor</th>
                <th>Estado</th>
                <th>Visitas</th>
                <th>Fecha</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {posts.map(post => (
                <tr key={post.id}>
                  <td>{post.id}</td>
                  <td>
                    <strong>{post.titulo}</strong>
                    {post.destacado && <span style={{color: '#ffc107'}}> ⭐</span>}
                  </td>
                  <td><span className="badge-tipo">{post.categoria}</span></td>
                  <td>{post.autor_nombre}</td>
                  <td>
                    <span className={`badge-tipo ${post.publicado ? 'publica' : 'privada'}`}>
                      {post.publicado ? '✅ Publicado' : '📝 Borrador'}
                    </span>
                  </td>
                  <td>{post.visitas}</td>
                  <td>{new Date(post.created_at).toLocaleDateString('es-ES')}</td>
                  <td className="acciones">
                    <button 
                      className="btn-editar"
                      onClick={() => editarPost(post)}
                      title="Editar"
                    >
                      ✏️
                    </button>
                    <button 
                      className="btn-eliminar"
                      onClick={() => eliminarPost(post.id, post.titulo)}
                      title="Eliminar"
                    >
                      🗑️
                    </button>
                    {post.publicado && (
                      <a 
                        href={`/blog/${post.slug}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn-web"
                        title="Ver post"
                      >
                        👁️
                      </a>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {posts.length === 0 && (
            <div className="sin-resultados">
              <p>No hay posts creados. Haz clic en "Nuevo Post" para empezar.</p>
            </div>
          )}
        </div>
      )}

      <div className="stats-footer">
        <p><strong>Total:</strong> {posts.length} posts</p>
      </div>
    </div>
  )
}

export default AdminBlog
