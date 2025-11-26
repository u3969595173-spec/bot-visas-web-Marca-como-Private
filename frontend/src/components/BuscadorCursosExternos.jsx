import React, { useState } from 'react'
import axios from 'axios'
import './BuscadorCursosExternos.css'

function BuscadorCursosExternos() {
  const [especialidad, setEspecialidad] = useState('')
  const [ciudad, setCiudad] = useState('')
  const [presupuestoMax, setPresupuestoMax] = useState('')
  const [cursos, setCursos] = useState([])
  const [loading, setLoading] = useState(false)
  const [busquedaRealizada, setBusquedaRealizada] = useState(false)

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const buscarCursos = async () => {
    setLoading(true)
    setBusquedaRealizada(true)
    
    try {
      const params = {}
      if (especialidad) params.especialidad = especialidad
      if (ciudad) params.ciudad = ciudad
      if (presupuestoMax) params.presupuesto_max = parseFloat(presupuestoMax)

      const res = await axios.get(`${apiUrl}/api/cursos/buscar-externos`, { params })
      setCursos(res.data.cursos)
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
      setCursos([])
    } finally {
      setLoading(false)
    }
  }

  const limpiarFiltros = () => {
    setEspecialidad('')
    setCiudad('')
    setPresupuestoMax('')
    setCursos([])
    setBusquedaRealizada(false)
  }

  return (
    <div className="buscador-cursos-externos">
      <div className="buscador-header">
        <h2>🔍 Buscar Cursos en Escuelas Españolas</h2>
        <p className="buscador-descripcion">
          Busca cursos en tiempo real desde múltiples universidades y escuelas de idiomas en España
        </p>
      </div>

      <div className="filtros-busqueda">
        <div className="form-group">
          <label>Especialidad / Área de Interés</label>
          <input
            type="text"
            value={especialidad}
            onChange={(e) => setEspecialidad(e.target.value)}
            placeholder="Ej: Ingeniería, Administración, Español, Medicina..."
          />
        </div>

        <div className="form-group">
          <label>Ciudad</label>
          <select value={ciudad} onChange={(e) => setCiudad(e.target.value)}>
            <option value="">Todas las ciudades</option>
            <option value="Madrid">Madrid</option>
            <option value="Barcelona">Barcelona</option>
            <option value="Valencia">Valencia</option>
            <option value="Sevilla">Sevilla</option>
            <option value="Málaga">Málaga</option>
            <option value="Bilbao">Bilbao</option>
          </select>
        </div>

        <div className="form-group">
          <label>Presupuesto Máximo (€)</label>
          <input
            type="number"
            value={presupuestoMax}
            onChange={(e) => setPresupuestoMax(e.target.value)}
            placeholder="Ej: 5000"
            min="0"
          />
        </div>

        <div className="botones-busqueda">
          <button onClick={buscarCursos} className="btn-buscar" disabled={loading}>
            {loading ? '🔄 Buscando...' : '🔍 Buscar Cursos'}
          </button>
          <button onClick={limpiarFiltros} className="btn-limpiar">
            🗑️ Limpiar Filtros
          </button>
        </div>
      </div>

      {loading && (
        <div className="loading-cursos">
          <div className="spinner"></div>
          <p>Consultando múltiples escuelas...</p>
        </div>
      )}

      {busquedaRealizada && !loading && cursos.length === 0 && (
        <div className="sin-resultados">
          <p>❌ No se encontraron cursos con los criterios seleccionados.</p>
          <p>Intenta ajustar los filtros o buscar con criterios más amplios.</p>
        </div>
      )}

      {cursos.length > 0 && (
        <div className="resultados-cursos">
          <h3>📚 {cursos.length} cursos encontrados</h3>
          
          <div className="cursos-grid">
            {cursos.map((curso, index) => (
              <div key={index} className="curso-card">
                <div className="curso-universidad">{curso.universidad}</div>
                <h4>{curso.nombre}</h4>
                <p className="curso-descripcion">{curso.descripcion}</p>
                
                <div className="curso-detalles">
                  <div className="detalle-item">
                    <span className="detalle-icono">📍</span>
                    <span>{curso.ciudad}</span>
                  </div>
                  <div className="detalle-item">
                    <span className="detalle-icono">⏱️</span>
                    <span>{curso.duracion_meses} meses</span>
                  </div>
                  <div className="detalle-item">
                    <span className="detalle-icono">💰</span>
                    <span>€{curso.precio_eur}</span>
                  </div>
                  <div className="detalle-item">
                    <span className="detalle-icono">🗣️</span>
                    <span>Nivel {curso.nivel_espanol_requerido}</span>
                  </div>
                  <div className="detalle-item">
                    <span className="detalle-icono">🎫</span>
                    <span>{curso.cupos_disponibles} cupos</span>
                  </div>
                  <div className="detalle-item">
                    <span className="detalle-icono">📚</span>
                    <span>{curso.modalidad}</span>
                  </div>
                </div>

                <div className="curso-requisitos">
                  <h5>Requisitos:</h5>
                  <ul>
                    {curso.requisitos.map((req, i) => (
                      <li key={i}>{req}</li>
                    ))}
                  </ul>
                </div>

                <div className="curso-footer">
                  <span className="curso-fecha">
                    📅 Inicio: {new Date(curso.fecha_inicio).toLocaleDateString('es-ES')}
                  </span>
                  {curso.url && (
                    <a 
                      href={curso.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="btn-mas-info"
                    >
                      Más información →
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default BuscadorCursosExternos
