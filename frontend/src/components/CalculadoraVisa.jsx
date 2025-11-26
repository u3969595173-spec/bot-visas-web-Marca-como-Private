import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './CalculadoraVisa.css';

const CalculadoraVisa = ({ estudianteId }) => {
  const [analisis, setAnalisis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    calcularProbabilidad();
  }, [estudianteId]);

  const calcularProbabilidad = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}/probabilidad-visa`);
      setAnalisis(response.data.analisis);
      setLoading(false);
    } catch (err) {
      setError('Error al calcular probabilidad');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="calculadora-loading">
        <div className="spinner"></div>
        <p>Calculando probabilidad...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="calculadora-error">
        <p>❌ {error}</p>
      </div>
    );
  }

  if (!analisis) return null;

  const getCircleColor = () => {
    if (analisis.probabilidad >= 80) return '#10b981';
    if (analisis.probabilidad >= 60) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="calculadora-container">
      <div className="calculadora-header">
        <h2>📊 Análisis de Probabilidad de Visa</h2>
        <p>Evaluación automática basada en tu perfil</p>
      </div>

      <div className="resultado-principal">
        <div className="probabilidad-circulo" style={{ borderColor: getCircleColor() }}>
          <div className="probabilidad-inner" style={{ background: getCircleColor() }}>
            <span className="probabilidad-numero">{analisis.probabilidad}%</span>
            <span className="probabilidad-label">Probabilidad</span>
          </div>
        </div>
        
        <div className="resultado-info">
          <div className="resultado-badge" style={{ background: analisis.color }}>
            Riesgo: {analisis.nivel_riesgo}
          </div>
          <p className="resultado-mensaje">{analisis.mensaje}</p>
          <div className="resultado-puntos">
            {analisis.puntos_total} / {analisis.puntos_maximos} puntos
          </div>
        </div>
      </div>

      <div className="factores-section">
        <h3>Factores Evaluados</h3>
        <div className="factores-grid">
          {analisis.factores.map((factor, index) => (
            <div key={index} className="factor-card">
              <div className="factor-header">
                <span className="factor-nombre">{factor.factor}</span>
                <span className="factor-puntos">
                  {factor.puntos}/{factor.max}
                </span>
              </div>
              <div className="factor-barra">
                <div 
                  className="factor-barra-fill"
                  style={{ 
                    width: `${(factor.puntos / factor.max) * 100}%`,
                    background: factor.puntos / factor.max >= 0.7 ? '#10b981' : 
                               factor.puntos / factor.max >= 0.5 ? '#f59e0b' : '#ef4444'
                  }}
                ></div>
              </div>
              <p className="factor-comentario">{factor.comentario}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="recomendaciones-section">
        <h3>📋 Recomendaciones Personalizadas</h3>
        <ul className="recomendaciones-lista">
          {analisis.recomendaciones.map((rec, index) => (
            <li key={index} className={rec.includes('URGENTE') ? 'recomendacion-urgente' : ''}>
              {rec}
            </li>
          ))}
        </ul>
      </div>

      <div className="siguiente-paso">
        <div className="siguiente-paso-icon">💡</div>
        <div>
          <h4>Siguiente Paso</h4>
          <p>{analisis.siguiente_paso}</p>
        </div>
      </div>

      <button 
        className="btn-recalcular"
        onClick={calcularProbabilidad}
      >
        🔄 Recalcular Probabilidad
      </button>
    </div>
  );
};

export default CalculadoraVisa;
