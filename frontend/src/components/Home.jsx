import React from 'react'
import { useNavigate, Link } from 'react-router-dom'
import './Home.css'

function Home() {
  const navigate = useNavigate()

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        {/* Background Image */}
        <img
          src="/assets/hero-bg.png"
          alt="Campus"
          className="hero-bg-img"
        />

        {/* Dark Overlay */}
        <div className="hero-overlay"></div>

        {/* Content */}
        <div className="hero-content-wrapper">
          <div className="hero-content-inner">
            {/* Semi-transparent container */}
            <div className="glass-card">
              <h1 className="hero-title">
                Tu Puerta de
                <br />
                Entrada a Europa
              </h1>

              <p className="hero-subtitle">
                Expertos en visas de estudio y admisión
                <br />
                universitaria en España
              </p>

              {/* Buttons */}
              <div className="hero-buttons">
                <button
                  className="btn-primary"
                  onClick={() => navigate('/registro')}
                >
                  Comenzar Trámite
                </button>
                <button
                  className="btn-secondary"
                  onClick={() => navigate('/portal')}
                >
                  Más Información
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="services-section">
        <div className="services-container">
          <div className="services-grid">
            {/* Service Card 1 */}
            <div className="service-card">
              <div className="icon-box">
                <div className="icon-text">📋</div>
              </div>
              <h3 className="service-title">Asesoría Personalizada</h3>
              <p className="service-desc">Evaluamos tu perfil y te guiamos paso a paso en tu proceso de visa de estudiante.</p>
            </div>

            {/* Service Card 2 */}
            <div className="service-card">
              <div className="icon-box">
                <div className="icon-text">📄</div>
              </div>
              <h3 className="service-title">Documentos Oficiales y Legalizaciones Express</h3>
              <p className="service-desc">Generamos automáticamente todos los documentos necesarios para tu solicitud.</p>
            </div>

            {/* Service Card 3 */}
            <div className="service-card">
              <div className="icon-box">
                <div className="icon-text">🎯</div>
              </div>
              <h3 className="service-title">Seguimiento Completo</h3>
              <p className="service-desc">
                Monitoreo en tiempo real de tu expediente con notificaciones automáticas.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-container">
          {/* Footer Content */}
          <div className="footer-top">
            {/* Links */}
            <nav className="footer-nav">
              <Link to="/" className="footer-link">
                Inicio
              </Link>
              <Link to="/blog" className="footer-link">
                Blog
              </Link>
              <Link to="/testimonios" className="footer-link">
                Testimonios
              </Link>
              <Link to="/admin/login" className="footer-link">
                Acceso Admin
              </Link>
            </nav>

            {/* Social Icons */}
            <div className="social-icons">
              <a href="#" className="social-btn">
                <span className="text-white">f</span>
              </a>
              <a href="#" className="social-btn">
                <span className="text-white">𝕏</span>
              </a>
              <a href="#" className="social-btn">
                <span className="text-white">📷</span>
              </a>
              <a href="#" className="social-btn">
                <span className="text-white">▶</span>
              </a>
            </div>
          </div>

          {/* Contact Info */}
          <div className="footer-contact">
            <div className="contact-item">
              <span className="text-gray-400">📞</span>
              <span className="contact-text">+34654034110</span>
            </div>
            <div className="contact-item">
              <span className="text-gray-400">✉</span>
              <span className="contact-text">estudiovisaespana@gmail.com</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Home
