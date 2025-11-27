import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './BuscadorUniversidades.css'

const BuscadorUniversidades = () => {
  const [universidades, setUniversidades] = useState([])
  const [programas, setProgramas] = useState([])
  const [loading, setLoading] = useState(false)
  const [vistaActual, setVistaActual] = useState('universidades') // 'universidades' o 'programas'
  
  // Filtros
  const [filtros, setFiltros] = useState({
    ciudad: '',
    comunidad: '',
    tipo: '',
    busquedaPrograma: '',
    tipoProgramaBusqueda: ''
  })
  
  const [universidadSeleccionada, setUniversidadSeleccionada] = useState(null)

  const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'

  const comunidades = [
    'Andalucía', 'Aragón', 'Cantabria', 'Castilla y León', 'Castilla-La Mancha',
    'Cataluña', 'Comunidad de Madrid', 'Comunidad Valenciana', 'Extremadura',
    'Galicia', 'Islas Baleares', 'Islas Canarias', 'La Rioja', 'Navarra',
    'País Vasco', 'Principado de Asturias', 'Región de Murcia'
  ]

  const tiposProgramas = [
    { value: 'grado', label: '🎓 Grado' },
    { value: 'master', label: '🎯 Máster' },
    { value: 'doctorado', label: '🔬 Doctorado' },
    { value: 'curso', label: '📚 Curso/Diploma' }
  ]

  useEffect(() => {
    cargarUniversidades()
  }, [])

  const cargarUniversidades = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (filtros.ciudad) params.append('ciudad', filtros.ciudad)
      if (filtros.comunidad) params.append('comunidad', filtros.comunidad)
      if (filtros.tipo) params.append('tipo', filtros.tipo)
      
      const response = await axios.get(`${API_URL}/api/universidades?${params}`)
      if (response.data.success) {
        setUniversidades(response.data.universidades)
      }
    } catch (error) {
      console.error('Error cargando universidades:', error)
    } finally {
      setLoading(false)
    }
  }

  const buscarProgramas = async () => {
    if (!filtros.busquedaPrograma || filtros.busquedaPrograma.length < 3) {
      alert('Escribe al menos 3 caracteres para buscar')
      return
    }

    try {
      setLoading(true)
      const params = new URLSearchParams()
      params.append('query', filtros.busquedaPrograma)
      if (filtros.ciudad) params.append('ciudad', filtros.ciudad)
      if (filtros.tipoProgramaBusqueda) params.append('tipo_programa', filtros.tipoProgramaBusqueda)
      
      const response = await axios.get(`${API_URL}/api/programas/buscar?${params}`)
      if (response.data.success) {
        setProgramas(response.data.resultados)
        setVistaActual('programas')
      }
    } catch (error) {
      console.error('Error buscando programas:', error)
    } finally {
      setLoading(false)
    }
  }

  const verProgramasUniversidad = async (universidad) => {
    try {
      setLoading(true)
      setUniversidadSeleccionada(universidad)
      
      const response = await axios.get(`${API_URL}/api/universidades/${universidad.id}/programas`)
      if (response.data.success) {
        setProgramas(response.data.programas.map(p => ({
          programa: p,
          universidad: universidad
        })))
        setVistaActual('programas')
      }
    } catch (error) {
      console.error('Error cargando programas:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFiltroChange = (e) => {
    const { name, value } = e.target
    setFiltros(prev => ({ ...prev, [name]: value }))
  }

  const aplicarFiltros = () => {
    setVistaActual('universidades')
    cargarUniversidades()
  }

  const limpiarFiltros = () => {
    setFiltros({
      ciudad: '',
      comunidad: '',
      tipo: '',
      busquedaPrograma: '',
      tipoProgramaBusqueda: ''
    })
    setVistaActual('universidades')
    cargarUniversidades()
  }

  return (
    <div className="buscador-container">
      <div className="buscador-header">
        <h1>🎓 Universidades de España</h1>
        <p className="subtitle">Explora más de 50 universidades y miles de programas académicos</p>
      </div>

      {/* Panel de filtros */}
      <div className="filtros-panel">
        <div className="tabs-busqueda">
          <button 
            className={vistaActual === 'universidades' ? 'active' : ''}
            onClick={() => setVistaActual('universidades')}
          >
            🏛️ Buscar Universidades
          </button>
          <button 
            className={vistaActual === 'programas' ? 'active' : ''}
            onClick={() => setVistaActual('programas')}
          >
            📚 Buscar Programas
          </button>
        </div>

        {vistaActual === 'universidades' ? (
          <div className="filtros-universidades">
            <div className="filtro-grupo">
              <label>Ciudad</label>
              <input 
                type="text" 
                name="ciudad"
                placeholder="Ej: Madrid, Barcelona..."
                value={filtros.ciudad}
                onChange={handleFiltroChange}
              />
            </div>

            <div className="filtro-grupo">
              <label>Comunidad Autónoma</label>
              <select name="comunidad" value={filtros.comunidad} onChange={handleFiltroChange}>
                <option value="">Todas</option>
                {comunidades.map(com => (
                  <option key={com} value={com}>{com}</option>
                ))}
              </select>
            </div>

            <div className="filtro-grupo">
              <label>Tipo</label>
              <select name="tipo" value={filtros.tipo} onChange={handleFiltroChange}>
                <option value="">Todas</option>
                <option value="publica">🏛️ Pública</option>
                <option value="privada">🏢 Privada</option>
              </select>
            </div>

            <div className="filtro-acciones">
              <button className="btn-aplicar" onClick={aplicarFiltros}>
                🔍 Buscar
              </button>
              <button className="btn-limpiar" onClick={limpiarFiltros}>
                ✕ Limpiar
              </button>
            </div>
          </div>
        ) : (
          <div className="filtros-programas">
            <div className="filtro-grupo-grande">
              <label>¿Qué quieres estudiar?</label>
              <input 
                type="text" 
                name="busquedaPrograma"
                placeholder="Ej: Ingeniería Informática, Medicina, Derecho..."
                value={filtros.busquedaPrograma}
                onChange={handleFiltroChange}
                onKeyPress={(e) => e.key === 'Enter' && buscarProgramas()}
              />
            </div>

            <div className="filtro-grupo">
              <label>Tipo de Programa</label>
              <select name="tipoProgramaBusqueda" value={filtros.tipoProgramaBusqueda} onChange={handleFiltroChange}>
                <option value="">Todos</option>
                {tiposProgramas.map(tipo => (
                  <option key={tipo.value} value={tipo.value}>{tipo.label}</option>
                ))}
              </select>
            </div>

            <div className="filtro-grupo">
              <label>Ciudad</label>
              <input 
                type="text" 
                name="ciudad"
                placeholder="Cualquier ciudad"
                value={filtros.ciudad}
                onChange={handleFiltroChange}
              />
            </div>

            <div className="filtro-acciones">
              <button className="btn-aplicar" onClick={buscarProgramas}>
                🔍 Buscar Programas
              </button>
              {universidadSeleccionada && (
                <button className="btn-volver" onClick={() => {
                  setVistaActual('universidades')
                  setUniversidadSeleccionada(null)
                }}>
                  ← Volver a Universidades
                </button>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Resultados */}
      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Cargando información...</p>
        </div>
      ) : vistaActual === 'universidades' ? (
        <div className="resultados-universidades">
          <div className="resultados-header">
            <h3>📊 {universidades.length} Universidades Encontradas</h3>
          </div>

          <div className="universidades-grid">
            {universidades.map(uni => (
              <div key={uni.id} className="universidad-card">
                <div className="uni-header">
                  <div className="uni-logo">
                    {uni.siglas || uni.nombre.substring(0, 3).toUpperCase()}
                  </div>
                  <div className="uni-info">
                    <h4>{uni.nombre}</h4>
                    <p className="uni-tipo">
                      {uni.tipo === 'publica' ? '🏛️ Pública' : '🏢 Privada'}
                    </p>
                  </div>
                </div>

                <div className="uni-detalles">
                  <div className="detalle-item">
                    <span className="icono">📍</span>
                    <span>{uni.ciudad}, {uni.comunidad_autonoma}</span>
                  </div>
                  {uni.total_alumnos && (
                    <div className="detalle-item">
                      <span className="icono">👥</span>
                      <span>{uni.total_alumnos.toLocaleString()} estudiantes</span>
                    </div>
                  )}
                  {uni.ranking_nacional && (
                    <div className="detalle-item">
                      <span className="icono">🏆</span>
                      <span>Ranking Nacional: #{uni.ranking_nacional}</span>
                    </div>
                  )}
                  {uni.acepta_extranjeros && (
                    <div className="badge-extranjeros">
                      ✓ Acepta estudiantes extranjeros
                    </div>
                  )}
                </div>

                <div className="uni-acciones">
                  <button 
                    className="btn-ver-programas"
                    onClick={() => verProgramasUniversidad(uni)}
                  >
                    📚 Ver Programas
                  </button>
                  {uni.url_oficial && (
                    <a 
                      href={uni.url_oficial}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn-web"
                    >
                      🌐 Sitio Web
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>

          {universidades.length === 0 && (
            <div className="sin-resultados">
              <div className="icono-grande">🔍</div>
              <h3>No se encontraron universidades</h3>
              <p>Intenta ajustar tus filtros de búsqueda</p>
            </div>
          )}
        </div>
      ) : (
        <div className="resultados-programas">
          <div className="resultados-header">
            {universidadSeleccionada ? (
              <h3>📚 Programas en {universidadSeleccionada.nombre}</h3>
            ) : (
              <h3>📊 {programas.length} Programas Encontrados</h3>
            )}
          </div>

          <div className="programas-lista">
            {programas.map((item, index) => (
              <div key={index} className="programa-card">
                <div className="programa-header">
                  <h4>{item.programa.nombre}</h4>
                  <span className="programa-tipo">
                    {tiposProgramas.find(t => t.value === item.programa.tipo_programa)?.label || item.programa.tipo_programa}
                  </span>
                </div>

                <div className="programa-universidad">
                  <strong>{item.universidad.nombre}</strong>
                  <span>📍 {item.universidad.ciudad}</span>
                </div>

                <div className="programa-detalles">
                  {item.programa.duracion_anos && (
                    <div className="detalle">
                      <span className="label">Duración:</span>
                      <span>{item.programa.duracion_anos} años</span>
                    </div>
                  )}
                  {item.programa.idioma && (
                    <div className="detalle">
                      <span className="label">Idioma:</span>
                      <span>{item.programa.idioma}</span>
                    </div>
                  )}
                  {item.programa.modalidad && (
                    <div className="detalle">
                      <span className="label">Modalidad:</span>
                      <span>{item.programa.modalidad}</span>
                    </div>
                  )}
                  {item.programa.precio_anual_eur && (
                    <div className="detalle">
                      <span className="label">Precio:</span>
                      <span className="precio">{item.programa.precio_anual_eur}€/año</span>
                    </div>
                  )}
                </div>

                {item.programa.url_info && (
                  <a 
                    href={item.programa.url_info}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-mas-info"
                  >
                    ℹ️ Más Información
                  </a>
                )}
              </div>
            ))}
          </div>

          {programas.length === 0 && (
            <div className="sin-resultados">
              <div className="icono-grande">📚</div>
              <h3>No se encontraron programas</h3>
              <p>Intenta con otras palabras clave o ajusta los filtros</p>
            </div>
          )}
        </div>
      )}

      {/* Info footer */}
      <div className="info-footer-universidades">
        <div className="info-card-uni">
          <h4>🔄 Actualización Continua</h4>
          <p>Nuestro sistema actualiza automáticamente la información de todas las universidades</p>
        </div>
        <div className="info-card-uni">
          <h4>✅ Verificado</h4>
          <p>Información oficial de más de 50 universidades públicas y privadas</p>
        </div>
        <div className="info-card-uni">
          <h4>🌍 Estudiantes Internacionales</h4>
          <p>Todas las universidades listadas aceptan estudiantes extranjeros</p>
        </div>
      </div>
    </div>
  )
}

export default BuscadorUniversidades
