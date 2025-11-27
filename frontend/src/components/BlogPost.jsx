import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'
import './Blog.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'

function BlogPost() {
  const { slug } = useParams()
  const [post, setPost] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    cargarPost()
  }, [slug])

  const cargarPost = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_URL}/api/blog/${slug}`)
      if (response.data.success) {
        setPost(response.data.post)
      }
    } catch (error) {
      console.error('Error cargando post:', error)
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

  if (loading) {
    return <div className="loading-blog">Cargando post...</div>
  }

  if (!post) {
    return (
      <div className="blog-container">
        <div className="post-no-encontrado">
          <h2>❌ Post no encontrado</h2>
          <Link to="/blog" className="btn-volver">← Volver al blog</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="blog-container">
      <article className="post-completo">
        <Link to="/blog" className="btn-volver-top">← Volver al blog</Link>
        
        {post.imagen_portada && (
          <div className="post-portada">
            <img src={post.imagen_portada} alt={post.titulo} />
          </div>
        )}

        <header className="post-header">
          <span className="post-categoria-badge">{post.categoria}</span>
          <h1>{post.titulo}</h1>
          <div className="post-meta-completo">
            <span>✍️ {post.autor_nombre}</span>
            <span>📅 {formatearFecha(post.fecha_publicacion)}</span>
            <span>👁️ {post.visitas} visitas</span>
          </div>
        </header>

        <div 
          className="post-contenido-html"
          dangerouslySetInnerHTML={{ __html: post.contenido }}
        />

        <footer className="post-footer">
          <Link to="/blog" className="btn-volver">← Volver al blog</Link>
        </footer>
      </article>
    </div>
  )
}

export default BlogPost
