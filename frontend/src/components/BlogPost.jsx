import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { useParams, Link } from 'react-router-dom'
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

  if (loading) return <div className="loading">Cargando...</div>

  if (!post) return (
    <div className="sin-resultados">
      <p>❌ Post no encontrado</p>
      <Link to="/blog" className="btn-volver">← Volver al blog</Link>
    </div>
  )

  return (
    <div className="blog-post-container">
      <Link to="/blog" className="btn-volver-post">← Volver al blog</Link>
      
      <article className="post-individual">
        {post.imagen_portada && (
          <img src={post.imagen_portada} alt={post.titulo} className="post-portada" />
        )}
        
        <div className="post-header">
          {post.categoria && (
            <span className="post-categoria">{post.categoria}</span>
          )}
          <h1>{post.titulo}</h1>
          <div className="post-meta">
            <span>✍️ {post.autor_nombre}</span>
            <span>📅 {new Date(post.fecha_publicacion).toLocaleDateString('es-ES', {
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}</span>
            <span>👁️ {post.visitas} visitas</span>
          </div>
        </div>

        <div 
          className="post-body"
          dangerouslySetInnerHTML={{ __html: post.contenido }}
        />

        <div className="post-compartir">
          <h3>Compartir este artículo</h3>
          <div className="compartir-botones">
            <a 
              href={`https://www.facebook.com/sharer/sharer.php?u=${window.location.href}`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-compartir facebook"
            >
              Facebook
            </a>
            <a 
              href={`https://twitter.com/intent/tweet?url=${window.location.href}&text=${post.titulo}`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-compartir twitter"
            >
              Twitter
            </a>
            <a 
              href={`https://www.linkedin.com/shareArticle?mini=true&url=${window.location.href}&title=${post.titulo}`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-compartir linkedin"
            >
              LinkedIn
            </a>
          </div>
        </div>
      </article>
    </div>
  )
}

export default BlogPost
