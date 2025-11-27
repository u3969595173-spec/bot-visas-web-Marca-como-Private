import React from 'react'
import { useNavigate } from 'react-router-dom'

function Home() {
  const navigate = useNavigate()

  return (
    <div className="container">
      <div style={styles.hero}>
        <h1 style={styles.title}>🎓 Bienvenido a Bot Visas Estudio</h1>
        <p style={styles.subtitle}>
          Tu agencia educativa para estudiar en España
        </p>
        <p style={styles.description}>
          Tramitamos tu visa de estudiante, te ayudamos a encontrar el curso
          perfecto y gestionamos todo el proceso de manera profesional.
        </p>

        <div style={styles.features}>
          <div style={styles.feature}>
            <div style={styles.featureIcon}>📚</div>
            <h3>Cursos Verificados</h3>
            <p>Accede a cientos de cursos en universidades españolas</p>
          </div>
          <div style={styles.feature}>
            <div style={styles.featureIcon}>✅</div>
            <h3>Proceso Simplificado</h3>
            <p>Te guiamos paso a paso en todo el trámite de visa</p>
          </div>
          <div style={styles.feature}>
            <div style={styles.featureIcon}>🏠</div>
            <h3>Alojamiento</h3>
            <p>Te ayudamos a encontrar alojamiento en España</p>
          </div>
        </div>

        <div style={styles.cta}>
          <button
            className="btn btn-primary"
            style={styles.ctaButton}
            onClick={() => navigate('/registro')}
          >
            Registrarme Ahora
          </button>
          <button
            className="btn"
            style={styles.ctaButtonSecondary}
            onClick={() => navigate('/portal')}
          >
            Ver Mi Estado
          </button>
        </div>
      </div>
    </div>
  )
}

const styles = {
  hero: {
    textAlign: 'center',
    padding: '60px 20px',
  },
  title: {
    fontSize: '48px',
    color: '#1a202c',
    marginBottom: '20px',
    textShadow: '2px 2px 4px rgba(0,0,0,0.1)',
  },
  subtitle: {
    fontSize: '24px',
    color: '#2d3748',
    marginBottom: '15px',
  },
  description: {
    fontSize: '18px',
    color: '#4a5568',
    marginBottom: '50px',
    maxWidth: '700px',
    margin: '0 auto 50px',
  },
  features: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '30px',
    marginBottom: '50px',
  },
  feature: {
    background: 'white',
    padding: '30px',
    borderRadius: '10px',
    boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
  },
  featureIcon: {
    fontSize: '48px',
    marginBottom: '15px',
  },
  cta: {
    display: 'flex',
    gap: '20px',
    justifyContent: 'center',
    flexWrap: 'wrap',
  },
  ctaButton: {
    fontSize: '18px',
    padding: '15px 40px',
  },
  ctaButtonSecondary: {
    fontSize: '18px',
    padding: '15px 40px',
    background: 'white',
    color: '#667eea',
  },
}

export default Home
