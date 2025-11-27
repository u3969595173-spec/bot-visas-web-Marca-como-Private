import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'
import './Blog.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'

function BlogLista() {
  const [posts, setPosts] = useState([])
  const [categorias, setCategorias] = useState([])
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    cargarCategorias()
    cargarPosts()
  }, [])

  useEffect(() => {
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
      const params = categoriaSeleccionada ? `?categoria=${categoriaSeleccionada}` : ''
      const response = await axios.get(`${API_URL}/api/blog${params}`)
      if (response.data.success) {
        setPosts(response.data.posts)
      }
    } catch (error) {
      console.error('Error cargando posts:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="blog-container">
      <div className="blog-header">
        <h1>📝 Blog y Noticias</h1>
        <p>Información actualizada sobre visas, estudios y vida en España</p>
      </div>

      <div className="blog-filtros">
        <button 
          className={!categoriaSeleccionada ? 'activo' : ''}
          onClick={() => setCategoriaSeleccionada('')}
        >
          Todos
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
        <div className="loading">Cargando posts...</div>
      ) : (
        <div className="posts-grid">
          {posts.map(post => (
            <article key={post.id} className="post-card">
              {post.imagen_portada && (
                <img src={post.imagen_portada} alt={post.titulo} className="post-imagen" />
              )}
              <div className="post-contenido">
                {post.categoria && (
                  <span className="post-categoria">{post.categoria}</span>
                )}
                {post.destacado && (
                  <span className="post-destacado">⭐ Destacado</span>
                )}
                <h2>{post.titulo}</h2>
                <p className="post-extracto">{post.extracto}</p>
                <div className="post-footer">
                  <span className="post-autor">✍️ {post.autor_nombre}</span>
                  <span className="post-fecha">
                    {new Date(post.fecha_publicacion).toLocaleDateString('es-ES')}
                  </span>
                  <span className="post-visitas">👁️ {post.visitas}</span>
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
        <div className="sin-resultados">
          <p>📭 No hay posts en esta categoría</p>
        </div>
      )}
    </div>
  )
}

export default BlogLista
