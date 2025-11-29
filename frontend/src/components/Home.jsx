import React from 'react'
import { useNavigate } from 'react-router-dom'
import './Home.css'

function Home() {
  const navigate = useNavigate()

  return (
    <div className="home-container">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Bienvenido a Estudia en España</h1>
          <p className="hero-subtitle">
            Tu agencia educativa para estudiar en España
          </p>
          <p className="hero-description">
            Tramitamos tu visa de estudiante, te ayudamos a encontrar el curso
            perfecto, te preparamos para todo y gestionamos todo el proceso de manera profesional.
          </p>

          <div className="hero-cta">
            <button
              className="btn-primary"
              onClick={() => navigate('/registro')}
            >
              Registrarme Ahora
            </button>
            <button
              className="btn-secondary"
              onClick={() => navigate('/portal')}
            >
              Ver Mi Estado
            </button>
          </div>
        </div>
      </div>

      <div className="disclaimer-banner">
        ⚖️ <strong>Disclaimer:</strong> Aunque no garantizamos la aprobación al 100% (decisión del Consulado), un trámite impecable tiene más de 90% de éxito. Nosotros nos encargamos de que tu expediente esté perfecto.
      </div>

      <div className="features-section">
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📚</div>
            <h3>Cursos Verificados</h3>
            <p>Accede a cientos de cursos en universidades españolas verificados y aprobados.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">✅</div>
            <h3>Proceso Simplificado</h3>
            <p>Te guiamos paso a paso en todo el trámite de visa con expertos legales.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🏠</div>
            <h3>Alojamiento</h3>
            <p>Te ayudamos a encontrar el alojamiento ideal para tu estancia en España.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home

