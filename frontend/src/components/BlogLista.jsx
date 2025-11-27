import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import './Blog.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'

function BlogLista() {
  const [posts, setPosts] = useState([])
  const [categorias, setCategorias] = useState([])
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    cargarCategorias()
    cargarPosts()
  }, [categoriaSeleccionada])

  const cargarCategorias = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/blog/categorias/listar`)
      if (response.data.success) {
        setCategorias(response.data.categorias)
      }
    } catch (error) {
      console.error('Error cargando categorías:', error)
    }
  }

  const cargarPosts = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (categoriaSeleccionada) params.append('categoria', categoriaSeleccionada)
      
      const response = await axios.get(`${API_URL}/api/blog?${params}`)
      if (response.data.success) {
        setPosts(response.data.posts)
      }
    } catch (error) {
      console.error('Error cargando posts:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatearFecha = (fecha) => {
    if (!fecha) return ''
    return new Date(fecha).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  return (
    <div className="blog-container">
      <div className="blog-header">
        <h1>📝 Blog y Noticias</h1>
        <p>Últimas noticias sobre visas, estudios y vida en España</p>
      </div>

      <div className="blog-filtros">
        <button
          className={categoriaSeleccionada === '' ? 'activo' : ''}
          onClick={() => setCategoriaSeleccionada('')}
        >
          Todas
        </button>
        {categorias.map(cat => (
          <button
            key={cat.nombre}
            className={categoriaSeleccionada === cat.nombre ? 'activo' : ''}
            onClick={() => setCategoriaSeleccionada(cat.nombre)}
          >
            {cat.nombre} ({cat.total_posts})
          </button>
        ))}
      </div>

      {loading ? (
        <div className="loading-blog">Cargando posts...</div>
      ) : (
        <div className="posts-grid">
          {posts.map(post => (
            <article key={post.id} className={`post-card ${post.destacado ? 'destacado' : ''}`}>
              {post.imagen_portada && (
                <div className="post-imagen">
                  <img src={post.imagen_portada} alt={post.titulo} />
                  {post.destacado && <span className="badge-destacado">⭐ Destacado</span>}
                </div>
              )}
              <div className="post-contenido">
                <span className="post-categoria">{post.categoria}</span>
                <h2>
                  <Link to={`/blog/${post.slug}`}>{post.titulo}</Link>
                </h2>
                <p className="post-extracto">{post.extracto}</p>
                <div className="post-meta">
                  <span>👤 {post.autor_nombre}</span>
                  <span>📅 {formatearFecha(post.fecha_publicacion)}</span>
                  <span>👁️ {post.visitas}</span>
                </div>
                <Link to={`/blog/${post.slug}`} className="btn-leer-mas">
                  Leer más →
                </Link>
              </div>
            </article>
          ))}
        </div>
      )}

      {!loading && posts.length === 0 && (
        <div className="sin-posts">
          <p>📭 No hay posts en esta categoría</p>
        </div>
      )}
    </div>
  )
}

export default BlogLista
