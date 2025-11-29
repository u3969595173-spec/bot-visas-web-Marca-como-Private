import React from 'react'
import { useNavigate } from 'react-router-dom'
import './Home.css'

// Placeholder SVG icons as data URIs
const graduationIcon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Cg fill='%230d9488'%3E%3Cpath d='M100 40l60 30v40c0 20-20 40-60 50-40-10-60-30-60-50V70z'/%3E%3Cpath d='M100 90c-11 0-20-9-20-20s9-20 20-20 20 9 20 20-9 20-20 20z' fill='%2314b8a6'/%3E%3C/g%3E%3C/svg%3E";
const passportIcon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Cg fill='%230d9488'%3E%3Crect x='50' y='30' width='100' height='140' rx='10' fill='%2314b8a6'/%3E%3Ccircle cx='100' cy='80' r='20' fill='%23fff'/%3E%3Cpath d='M80 120h40M80 135h40M80 150h40' stroke='%23fff' stroke-width='4'/%3E%3C/g%3E%3C/svg%3E";
const buildingIcon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Cg fill='%230d9488'%3E%3Crect x='60' y='40' width='80' height='120' fill='%2314b8a6'/%3E%3Crect x='75' y='60' width='15' height='15' fill='%23fff'/%3E%3Crect x='110' y='60' width='15' height='15' fill='%23fff'/%3E%3Crect x='75' y='90' width='15' height='15' fill='%23fff'/%3E%3Crect x='110' y='90' width='15' height='15' fill='%23fff'/%3E%3Crect x='85' y='130' width='30' height='30' fill='%23fff'/%3E%3C/g%3E%3C/svg%3E";

function Home() {
  const navigate = useNavigate()

  return (
    <div className="home-container">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Tu Puerta de Entrada a Europa</h1>
          <p className="hero-subtitle">
            Expertos en visas de estudio y admisión universitaria en España
          </p>

          <div className="hero-cta">
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

      <div className="features-section">
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <img src={graduationIcon} alt="Graduation" />
            </div>
            <h3>Admisión Garantizada</h3>
            <p>Aseguramos tu plaza en universidades de prestigio.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <img src={passportIcon} alt="Passport" />
            </div>
            <h3>Visa Express</h3>
            <p>Agilizamos tus trámites para un proceso sin estrés.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <img src={buildingIcon} alt="Building" />
            </div>
            <h3>Alojamiento Premium</h3>
            <p>Opciones de vivienda seguras y confortables para estudiantes.</p>
          </div>
        </div>

        <div className="disclaimer-banner">
          ⚖️ <strong>Nota Legal:</strong> Gestionamos tu expediente con los más altos estándares de calidad para maximizar tus probabilidades de éxito (tasa 90%). La decisión final depende del Consulado.
        </div>
      </div>
    </div>
  )
}

export default Home
