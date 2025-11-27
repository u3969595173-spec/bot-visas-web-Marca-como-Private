import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SimuladorEntrevista.css';

const SimuladorEntrevista = ({ estudianteId }) => {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const [entrevista, setEntrevista] = useState(null);
  const [loading, setLoading] = useState(true);
  const [preguntaActual, setPreguntaActual] = useState(0);
  const [respuestas, setRespuestas] = useState({});
  const [respuestaActual, setRespuestaActual] = useState('');
  const [modo, setModo] = useState('preparacion'); // preparacion, practica, completado
  const [evaluaciones, setEvaluaciones] = useState({});
  const [mostrandoTips, setMostrandoTips] = useState(false);

  useEffect(() => {
    cargarEntrevista();
  }, [estudianteId]);

  const cargarEntrevista = async () => {
    try {
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}/simulador-entrevista`);
      setEntrevista(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error cargando entrevista:', err);
      setLoading(false);
    }
  };

  const iniciarSimulador = () => {
    setModo('practica');
    setPreguntaActual(0);
    setRespuestas({});
    setEvaluaciones({});
  };

  const guardarRespuesta = async () => {
    const pregunta = entrevista.preguntas[preguntaActual];
    
    // Guardar respuesta
    const nuevasRespuestas = {
      ...respuestas,
      [preguntaActual]: respuestaActual
    };
    setRespuestas(nuevasRespuestas);

    // Evaluar respuesta con objeto pregunta completo
    try {
      const response = await axios.post(`${apiUrl}/api/simulador-entrevista/evaluar`, {
        pregunta_id: preguntaActual,
        respuesta: respuestaActual,
        pregunta: pregunta  // Enviar pregunta completa para tips
      });
      
      setEvaluaciones({
        ...evaluaciones,
        [preguntaActual]: response.data
      });
    } catch (err) {
      console.error('Error evaluando respuesta:', err);
    }

    // Limpiar campo y avanzar
    setRespuestaActual('');
    
    if (preguntaActual < entrevista.preguntas.length - 1) {
      setPreguntaActual(preguntaActual + 1);
      setMostrandoTips(false);
    } else {
      setModo('completado');
    }
  };

  const calcularPromedio = () => {
    const puntuaciones = Object.values(evaluaciones).map(e => e.puntuacion);
    if (puntuaciones.length === 0) return 0;
    return Math.round(puntuaciones.reduce((a, b) => a + b, 0) / puntuaciones.length);
  };

  if (loading) {
    return (
      <div className="simulador-loading">
        <div className="spinner"></div>
        <p>Generando tu entrevista personalizada...</p>
      </div>
    );
  }

  if (!entrevista) {
    return (
      <div className="simulador-error">
        <p>❌ Error al cargar el simulador</p>
      </div>
    );
  }

  // PANTALLA: PREPARACIÓN
  if (modo === 'preparacion') {
    return (
      <div className="simulador-container">
        <div className="simulador-header">
          <h1>🎭 Simulador de Entrevista Consular</h1>
          <p className="simulador-subtitle">Prepárate con preguntas reales adaptadas a tu perfil</p>
        </div>

        <div className="simulador-info-cards">
          <div className="info-card">
            <div className="info-icon">📋</div>
            <div className="info-content">
              <h3>{entrevista.total_preguntas} Preguntas</h3>
              <p>Duración estimada: {entrevista.duracion_estimada}</p>
            </div>
          </div>

          <div className="info-card">
            <div className="info-icon">🎯</div>
            <div className="info-content">
              <h3>Personalizado</h3>
              <p>Adaptado a tu perfil específico</p>
            </div>
          </div>

          <div className="info-card">
            <div className="info-icon">💡</div>
            <div className="info-content">
              <h3>Con Feedback</h3>
              <p>Evaluación y tips en cada respuesta</p>
            </div>
          </div>
        </div>

        {/* Contexto personalizado */}
        <div className="simulador-contexto">
          <h2>📊 Tu Perfil</h2>
          
          {entrevista.contexto_personalizado.puntos_fuertes.length > 0 && (
            <div className="contexto-section">
              <h3 style={{color: '#28a745'}}>Puntos Fuertes:</h3>
              <ul>
                {entrevista.contexto_personalizado.puntos_fuertes.map((punto, i) => (
                  <li key={i}>{punto}</li>
                ))}
              </ul>
            </div>
          )}

          {entrevista.contexto_personalizado.areas_a_mejorar.length > 0 && (
            <div className="contexto-section">
              <h3 style={{color: '#ffc107'}}>Áreas a Reforzar:</h3>
              <ul>
                {entrevista.contexto_personalizado.areas_a_mejorar.map((area, i) => (
                  <li key={i}>{area}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="contexto-recomendacion">
            <strong>💡 Recomendación Principal:</strong>
            <p>{entrevista.contexto_personalizado.recomendacion_principal}</p>
          </div>
        </div>

        {/* Consejos generales */}
        <div className="simulador-consejos">
          <h2>📌 Consejos para la Entrevista</h2>
          <div className="consejos-grid">
            {entrevista.consejos_generales.map((consejo, i) => (
              <div key={i} className="consejo-card">
                <div className="consejo-icono">{consejo.icono}</div>
                <h4>{consejo.titulo}</h4>
                <p>{consejo.consejo}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="simulador-actions">
          <button className="btn-iniciar" onClick={iniciarSimulador}>
            🚀 Iniciar Simulador
          </button>
        </div>
      </div>
    );
  }

  // PANTALLA: PRÁCTICA
  if (modo === 'practica') {
    const pregunta = entrevista.preguntas[preguntaActual];
    const progreso = Math.round(((preguntaActual + 1) / entrevista.preguntas.length) * 100);

    return (
      <div className="simulador-container simulador-practica">
        <div className="practica-header">
          <div className="practica-progreso">
            <span>Pregunta {preguntaActual + 1} de {entrevista.preguntas.length}</span>
            <div className="progreso-bar">
              <div className="progreso-fill" style={{width: `${progreso}%`}}></div>
            </div>
          </div>
        </div>

        <div className="pregunta-card">
          <div className="pregunta-numero">Pregunta #{preguntaActual + 1}</div>
          <h2 className="pregunta-texto">{pregunta.pregunta}</h2>
          <div className="pregunta-categoria">
            Categoría: <span className="badge">{pregunta.categoria}</span>
          </div>

          <div className="respuesta-section">
            <label htmlFor="respuesta">✍️ Tu Respuesta:</label>
            <textarea
              id="respuesta"
              value={respuestaActual}
              onChange={(e) => setRespuestaActual(e.target.value)}
              placeholder="Escribe tu respuesta aquí... Sé específico y detallado."
              rows={8}
              className="respuesta-textarea"
            />
            <div className="respuesta-info">
              <span>{respuestaActual.split(' ').filter(w => w).length} palabras</span>
              <button 
                className="btn-tips" 
                onClick={() => setMostrandoTips(!mostrandoTips)}
              >
                {mostrandoTips ? '❌ Ocultar' : '💡 Ver Tips'}
              </button>
            </div>
          </div>

          {mostrandoTips && (
            <div className="tips-box">
              <h4>💡 Tips para esta pregunta:</h4>
              <p>{pregunta.tips}</p>
              <div className="modelo-respuesta">
                <h5>📝 Ejemplo de respuesta:</h5>
                <p className="respuesta-modelo">{pregunta.respuesta_modelo}</p>
              </div>
            </div>
          )}

          {evaluaciones[preguntaActual - 1] && (
            <div className="evaluacion-anterior">
              <h4>📊 Evaluación de tu respuesta anterior:</h4>
              <div className="evaluacion-content">
                <div className="evaluacion-puntos">
                  <span className="puntuacion">{evaluaciones[preguntaActual - 1].puntuacion}/100</span>
                  <span className="calidad">{evaluaciones[preguntaActual - 1].calidad}</span>
                </div>
                <p>{evaluaciones[preguntaActual - 1].feedback}</p>
              </div>
            </div>
          )}

          <div className="practica-actions">
            {preguntaActual > 0 && (
              <button 
                className="btn-anterior" 
                onClick={() => setPreguntaActual(preguntaActual - 1)}
              >
                ← Anterior
              </button>
            )}
            <button 
              className="btn-siguiente" 
              onClick={guardarRespuesta}
              disabled={respuestaActual.trim().length < 10}
            >
              {preguntaActual < entrevista.preguntas.length - 1 ? 'Siguiente →' : '✅ Finalizar'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // PANTALLA: COMPLETADO
  if (modo === 'completado') {
    const promedio = calcularPromedio();
    let mensajeFinal = '';
    let colorFinal = '';

    if (promedio >= 80) {
      mensajeFinal = '¡Excelente! Estás muy bien preparado para la entrevista.';
      colorFinal = '#28a745';
    } else if (promedio >= 60) {
      mensajeFinal = 'Bien. Sigue practicando y mejorando tus respuestas.';
      colorFinal = '#17a2b8';
    } else {
      mensajeFinal = 'Necesitas más preparación. Revisa los tips y practica de nuevo.';
      colorFinal = '#ffc107';
    }

    return (
      <div className="simulador-container simulador-completado">
        <div className="completado-header">
          <div className="completado-icono">🎉</div>
          <h1>¡Simulación Completada!</h1>
          <div className="completado-puntuacion" style={{color: colorFinal}}>
            <span className="puntuacion-numero">{promedio}</span>
            <span className="puntuacion-max">/100</span>
          </div>
          <p className="completado-mensaje">{mensajeFinal}</p>
        </div>

        <div className="resumen-respuestas">
          <h2>📝 Resumen de tus Respuestas</h2>
          {entrevista.preguntas.map((pregunta, index) => {
            const evaluacion = evaluaciones[index];
            return (
              <div key={index} className="resumen-item">
                <h4>#{index + 1}: {pregunta.pregunta}</h4>
                <div className="resumen-respuesta">
                  <p><strong>Tu respuesta:</strong> {respuestas[index] || '(Sin respuesta)'}</p>
                </div>
                {evaluacion && (
                  <div className="resumen-evaluacion">
                    <div className="eval-header">
                      <span className={`eval-puntos puntos-${evaluacion.puntuacion >= 80 ? 'alta' : evaluacion.puntuacion >= 60 ? 'media' : 'baja'}`}>
                        {evaluacion.puntuacion}/100
                      </span>
                      <span className="eval-calidad">{evaluacion.calidad}</span>
                    </div>
                    <p className="eval-feedback">{evaluacion.feedback}</p>
                    
                    {evaluacion.problemas && evaluacion.problemas.length > 0 && (
                      <div className="eval-problemas">
                        <strong>⚠️ Problemas detectados:</strong>
                        <ul>
                          {evaluacion.problemas.map((problema, i) => (
                            <li key={i}>{problema}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {evaluacion.recomendaciones && evaluacion.recomendaciones.length > 0 && (
                      <div className="eval-recomendaciones">
                        <strong>💡 Recomendaciones:</strong>
                        <ul>
                          {evaluacion.recomendaciones.map((rec, i) => (
                            <li key={i}>{rec}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {evaluacion.tips && (
                      <div className="eval-tips">
                        <strong>📌 Tip:</strong>
                        <p>{evaluacion.tips}</p>
                      </div>
                    )}
                    
                    {evaluacion.respuesta_modelo && (
                      <div className="eval-modelo">
                        <strong>✨ Ejemplo de respuesta ideal:</strong>
                        <p className="respuesta-modelo-texto">{evaluacion.respuesta_modelo}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="completado-actions">
          <button className="btn-repetir" onClick={() => setModo('preparacion')}>
            🔄 Volver a Practicar
          </button>
          <button className="btn-descargar" onClick={() => window.print()}>
            📄 Descargar Resultados
          </button>
        </div>
      </div>
    );
  }

  return null;
};

export default SimuladorEntrevista;
