import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './CalculadoraFondos.css';

const CalculadoraFondos = () => {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  
  const [ciudades, setCiudades] = useState([]);
  const [programas, setProgramas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState(null);
  
  const [formulario, setFormulario] = useState({
    ciudad: 'madrid',
    tipo_alojamiento: 'piso_compartido',
    tipo_programa: 'grado_publico',
    duracion_meses: 10,
    con_pareja: false,
    num_hijos: 0,
    fondos_disponibles: 0
  });

  useEffect(() => {
    cargarDatosIniciales();
  }, []);

  const cargarDatosIniciales = async () => {
    try {
      const [resCiudades, resProgramas] = await Promise.all([
        axios.get(`${apiUrl}/api/calculadora-fondos/ciudades`),
        axios.get(`${apiUrl}/api/calculadora-fondos/programas`)
      ]);
      setCiudades(resCiudades.data);
      setProgramas(resProgramas.data);
    } catch (err) {
      console.error('Error cargando datos:', err);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormulario({
      ...formulario,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const calcularFondos = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${apiUrl}/api/calculadora-fondos`, formulario);
      setResultado(response.data);
    } catch (err) {
      console.error('Error calculando fondos:', err);
      alert('Error al calcular fondos');
    } finally {
      setLoading(false);
    }
  };

  const formatearMoneda = (cantidad) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    }).format(cantidad);
  };

  return (
    <div className="calculadora-fondos-container">
      <div className="calculadora-header">
        <h1>💰 Calculadora de Fondos</h1>
        <p className="calculadora-subtitle">Calcula cuánto dinero necesitas para estudiar en España</p>
        <div className="disclaimer-importante">
          ⚠️ <strong>IMPORTANTE:</strong> Estas son estimaciones generales basadas en promedios. 
          Los costos reales pueden variar. <strong>Nosotros te ayudamos</strong> a planificar tu presupuesto detallado.
        </div>
      </div>

      <div className="calculadora-formulario">
        <div className="form-section">
          <h3>📍 Ubicación y Alojamiento</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Ciudad:</label>
              <select name="ciudad" value={formulario.ciudad} onChange={handleChange}>
                {ciudades.map(ciudad => (
                  <option key={ciudad.key} value={ciudad.key}>{ciudad.nombre}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Tipo de Alojamiento:</label>
              <select name="tipo_alojamiento" value={formulario.tipo_alojamiento} onChange={handleChange}>
                <option value="piso_compartido">Piso Compartido (habitación)</option>
                <option value="residencia">Residencia Estudiantil</option>
                <option value="piso_individual">Piso Individual</option>
              </select>
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>🎓 Programa de Estudios</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Tipo de Programa:</label>
              <select name="tipo_programa" value={formulario.tipo_programa} onChange={handleChange}>
                {programas.map(prog => (
                  <option key={prog.key} value={prog.key}>
                    {prog.nombre} (€{prog.rango})
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Duración (meses):</label>
              <input
                type="number"
                name="duracion_meses"
                value={formulario.duracion_meses}
                onChange={handleChange}
                min="1"
                max="48"
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>👨‍👩‍👧 Situación Familiar</h3>
          <div className="form-row">
            <div className="form-group checkbox-group">
              <label>
                <input
                  type="checkbox"
                  name="con_pareja"
                  checked={formulario.con_pareja}
                  onChange={handleChange}
                />
                Viajaré con pareja
              </label>
            </div>
            <div className="form-group">
              <label>Número de hijos:</label>
              <input
                type="number"
                name="num_hijos"
                value={formulario.num_hijos}
                onChange={handleChange}
                min="0"
                max="5"
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>💵 Tus Fondos Disponibles</h3>
          <div className="form-group">
            <label>Fondos que tienes actualmente (€):</label>
            <input
              type="number"
              name="fondos_disponibles"
              value={formulario.fondos_disponibles}
              onChange={handleChange}
              min="0"
              placeholder="Ej: 10000"
            />
            <small>Incluye ahorros + apoyo familiar + becas</small>
          </div>
        </div>

        <button className="btn-calcular" onClick={calcularFondos} disabled={loading}>
          {loading ? '⏳ Calculando...' : '🧮 Calcular Fondos Necesarios'}
        </button>
      </div>

      {resultado && (
        <div className="calculadora-resultados">
          <h2>📊 Resultados del Cálculo</h2>
          
          <div className="resultado-header">
            <div className="resultado-principal">
              <h3>Total Estimado</h3>
              <div className="monto-total">{formatearMoneda(resultado.total_general)}</div>
              <p>Para {resultado.duracion_meses} meses en {resultado.ciudad}</p>
            </div>
            
            <div className={`resultado-comparacion ${resultado.suficiente ? 'suficiente' : 'insuficiente'}`}>
              <h4>Tus fondos: {formatearMoneda(resultado.fondos_disponibles)}</h4>
              {resultado.suficiente ? (
                <div className="estado-positivo">
                  ✅ ¡Tienes fondos suficientes!<br/>
                  Excedente: {formatearMoneda(resultado.diferencia)}
                </div>
              ) : (
                <div className="estado-negativo">
                  ⚠️ Necesitas más fondos<br/>
                  Faltan: {formatearMoneda(Math.abs(resultado.diferencia))}
                </div>
              )}
            </div>
          </div>

          <div className="desglose-cards">
            <div className="desglose-card">
              <h4>💳 Matrícula</h4>
              <div className="monto-card">{formatearMoneda(resultado.matricula)}</div>
              <small>Rango: €{resultado.rango_matricula}</small>
            </div>
            <div className="desglose-card">
              <h4>🏠 Manutención Total</h4>
              <div className="monto-card">{formatearMoneda(resultado.total_manutención)}</div>
              <small>{resultado.duracion_meses} meses × {formatearMoneda(resultado.total_mensual)}/mes</small>
            </div>
            <div className="desglose-card">
              <h4>✈️ Costos Iniciales</h4>
              <div className="monto-card">{formatearMoneda(resultado.total_inicial)}</div>
              <small>Vuelo, depósito, instalación</small>
            </div>
          </div>

          <div className="desglose-mensual">
            <h3>📅 Desglose Mensual</h3>
            <div className="tabla-desglose">
              <div className="desglose-item">
                <span>🏠 Alojamiento ({resultado.tipo_alojamiento}):</span>
                <strong>{formatearMoneda(resultado.desglose_mensual.alojamiento)}</strong>
              </div>
              <div className="desglose-item">
                <span>🍽️ Comida:</span>
                <strong>{formatearMoneda(resultado.desglose_mensual.comida)}</strong>
              </div>
              <div className="desglose-item">
                <span>🚇 Transporte:</span>
                <strong>{formatearMoneda(resultado.desglose_mensual.transporte)}</strong>
              </div>
              <div className="desglose-item">
                <span>🏥 Seguro Médico:</span>
                <strong>{formatearMoneda(resultado.desglose_mensual.seguro_medico)}</strong>
              </div>
              <div className="desglose-item">
                <span>📱 Otros gastos:</span>
                <strong>{formatearMoneda(resultado.desglose_mensual.otros)}</strong>
              </div>
              {resultado.desglose_mensual.pareja_adicional && (
                <div className="desglose-item adicional">
                  <span>👫 Pareja adicional:</span>
                  <strong>+{formatearMoneda(resultado.desglose_mensual.pareja_adicional)}</strong>
                </div>
              )}
              {resultado.desglose_mensual.hijos_adicional && (
                <div className="desglose-item adicional">
                  <span>👶 Hijos ({resultado.num_hijos}):</span>
                  <strong>+{formatearMoneda(resultado.desglose_mensual.hijos_adicional)}</strong>
                </div>
              )}
              <div className="desglose-item total">
                <span><strong>Total Mensual:</strong></span>
                <strong className="monto-destacado">{formatearMoneda(resultado.total_mensual)}</strong>
              </div>
            </div>
          </div>

          <div className="costos-iniciales-detalle">
            <h3>✈️ Costos Iniciales (una vez)</h3>
            <div className="tabla-desglose">
              {Object.entries(resultado.costos_iniciales).map(([key, value]) => (
                <div className="desglose-item" key={key}>
                  <span>{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</span>
                  <strong>{formatearMoneda(value)}</strong>
                </div>
              ))}
            </div>
          </div>

          <div className="recomendaciones">
            <h3>💡 Recomendaciones Personalizadas</h3>
            <ul>
              {resultado.recomendaciones.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>

          <div className="disclaimer-final">
            {resultado.disclaimer}
          </div>
        </div>
      )}
    </div>
  );
};

export default CalculadoraFondos;
