import React from 'react'
import { useNavigate, Link } from 'react-router-dom'
import './Home.css'

const opDestacadas = [
  { id: 1, icon: '🌾', nombre: 'Exportaciones de alimentos', cat: 'Agricultura y exportación', capital: '€120.000' },
  { id: 2, icon: '📊', nombre: 'Financiación a MYPIMEs y TCP', cat: 'Financiamiento', capital: '€150.000' },
  { id: 3, icon: '🌍', nombre: 'Inversiones en el extranjero', cat: 'Mercados internacionales', capital: '€200.000' },
]

function Home() {
  const navigate = useNavigate()

  return (
    <div className="home-container">
      {/* ── Hero ── */}
      <section className="hero-fullscreen">
        <div className="hero-bg">
          <div className="orb orb-1"></div>
          <div className="orb orb-2"></div>
          <div className="orb orb-3"></div>
          <div className="grid-lines"></div>
        </div>

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

        <div className="scroll-indicator">
          <div className="scroll-line"></div>
        </div>

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

      {/* ── Stats ── */}
      <section className="home-stats">
        <div className="home-stats-inner">
          <div className="stat-item">
            <span className="stat-number">€760k</span>
            <span className="stat-label">Capital total</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">6</span>
            <span className="stat-label">Operaciones</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">2</span>
            <span className="stat-label">Mercados</span>
          </div>
        </div>
      </section>

      {/* ── Operaciones destacadas ── */}
      <section className="home-ops">
        <div className="home-section-header">
          <div>
            <p className="section-tag">Oportunidades</p>
            <h2>Operaciones disponibles</h2>
            <p className="section-sub">Selecciona la operación que se ajuste a tu perfil</p>
          </div>
          <Link to="/operaciones" className="view-all-link">Ver todas →</Link>
        </div>

        <div className="ops-grid">
          {opDestacadas.map((op) => (
            <div key={op.id} className="op-card">
              <span className="op-card-icon">{op.icon}</span>
              <span className="op-card-cat">{op.cat}</span>
              <span className="op-card-name">{op.nombre}</span>
              <span className="op-card-capital">{op.capital}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── Cómo funciona ── */}
      <section className="home-how">
        <div className="home-how-inner">
          <div className="home-section-header">
            <div>
              <p className="section-tag">Proceso</p>
              <h2>Cómo funciona</h2>
              <p className="section-sub">Seis pasos desde tu registro hasta avanzar de nivel</p>
            </div>
            <Link to="/como-funciona" className="view-all-link">Ver detalle →</Link>
          </div>

          <div className="how-steps">
            <div className="how-step">
              <div className="how-step-num">1</div>
              <span className="how-step-emoji">👤</span>
              <h4>Crea tu cuenta</h4>
              <p>Regístrate y accede a tu área personal.</p>
            </div>
            <div className="how-step">
              <div className="how-step-num">2</div>
              <span className="how-step-emoji">💰</span>
              <h4>Realiza tu aportación</h4>
              <p>Elige la cantidad dentro de las condiciones disponibles.</p>
            </div>
            <div className="how-step">
              <div className="how-step-num">3</div>
              <span className="how-step-emoji">⚙️</span>
              <h4>Gestionamos las operaciones</h4>
              <p>Nuestro equipo destina los recursos según nuestra estrategia.</p>
            </div>
            <div className="how-step">
              <div className="how-step-num">4</div>
              <span className="how-step-emoji">📈</span>
              <h4>Obtén tus resultados</h4>
              <p>Los resultados se reflejan en tu cuenta al finalizar el periodo.</p>
            </div>
          </div>
        </div>
      </section>

      {/* ── CTA final ── */}
      <section className="home-cta-final">
        <p className="section-tag">Empieza hoy</p>
        <h2>¿Listo para participar?</h2>
        <p>Regístrate y recibe información detallada sobre las operaciones disponibles.</p>
        <button className="cta-main" onClick={() => navigate('/registro')}>
          Solicitar información
        </button>
      </section>
    </div>
  )
}

export default Home
