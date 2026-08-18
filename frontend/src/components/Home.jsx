import React from 'react'
import { useNavigate } from 'react-router-dom'
import './Home.css'

function Home() {
  const navigate = useNavigate()

  return (
    <div className="home-container">
      <section className="hero-fullscreen">
        {/* Animated background */}
        <div className="hero-bg">
          <div className="orb orb-1"></div>
          <div className="orb orb-2"></div>
          <div className="orb orb-3"></div>
          <div className="grid-lines"></div>
        </div>

        {/* Main content */}
        <div className="hero-main">
          <div className="hero-logo-badge">
            <div className="logo-icon">CT</div>
            <span className="logo-badge-text">Capital Trade Iberia</span>
          </div>

          <h1 className="hero-company-name">
            <span className="text-white">Capital</span>
            <span className="text-gold">Trade Iberia</span>
          </h1>

          <p className="hero-tagline">
            Operaciones comerciales con estructura, transparencia y participación definida.
          </p>

          <div className="hero-divider"></div>

          <div className="hero-cta-group">
            <button className="cta-main" onClick={() => navigate('/registro')}>
              Solicitar información
            </button>
            <button className="cta-ghost" onClick={() => navigate('/operaciones')}>
              Ver operaciones
            </button>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="scroll-indicator">
          <div className="scroll-line"></div>
        </div>

        {/* Bottom bar */}
        <div className="hero-bottom-bar">
          <div className="bottom-item">
            <span className="bottom-dot"></span>
            España · Cuba
          </div>
          <div className="bottom-item">
            <span className="bottom-dot"></span>
            Operaciones activas
          </div>
          <div className="bottom-item">
            <span className="bottom-dot"></span>
            Participación por operación
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home
