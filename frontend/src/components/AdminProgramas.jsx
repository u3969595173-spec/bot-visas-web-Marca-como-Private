import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './AdminUniversidades.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'

function AdminProgramas() {
  const [programas, setProgramas] = useState([])
  const [universidades, setUniversidades] = useState([])
  const [loading, setLoading] = useState(false)
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [editando, setEditando] = useState(null)
  const [universidadSeleccionada, setUniversidadSeleccionada] = useState('')

  const [formulario, setFormulario] = useState({
    universidad_id: '',
    nombre: '',
    tipo_programa: 'grado',
    area_estudio: '',
    duracion_anos: 4,
    creditos_ects: 240,
    idioma: 'español',
    modalidad: 'presencial',
    precio_anual_eur: '',
    plazas_disponibles: '',
    nota_corte: '',
    url_info: '',
    requisitos: '',
    descripcion: ''
  })

  useEffect(() => {
    cargarUniversidades()
  }, [])

  useEffect(() => {
    if (universidadSeleccionada) {
      cargarProgramas()
    }
  }, [universidadSeleccionada])

  const cargarUniversidades = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/universidades`)
      if (response.data.success) {
        setUniversidades(response.data.universidades)
      }
    } catch (error) {
      console.error('Error cargando universidades:', error)
    }
  }

  const cargarProgramas = async () => {
    if (!universidadSeleccionada) return
    setLoading(true)
    try {
      const response = await axios.get(
        `${API_URL}/api/universidades/${universidadSeleccionada}/programas`
      )
      if (response.data.success) {
        setProgramas(response.data.programas)
      }
    } catch (error) {
      console.error('Error cargando programas:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormulario(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (editando) {
        const response = await axios.put(
          `${API_URL}/api/admin/programas/${editando}`,
          formulario
        )
        if (response.data.success) {
          alert('Programa actualizado exitosamente')
          resetFormulario()
          cargarProgramas()
        }
      } else {
        const response = await axios.post(
          `${API_URL}/api/admin/programas`,
          { ...formulario, universidad_id: parseInt(universidadSeleccionada) }
        )
        if (response.data.success) {
          alert(`Programa "${response.data.nombre}" creado exitosamente`)
          resetFormulario()
          cargarProgramas()
        }
      }
    } catch (error) {
      console.error('Error guardando programa:', error)
      alert('Error al guardar programa: ' + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  const editarPrograma = (programa) => {
    setFormulario({
      universidad_id: programa.universidad_id,
      nombre: programa.nombre,
      tipo_programa: programa.tipo_programa || 'grado',
      area_estudio: programa.area_estudio || '',
      duracion_anos: programa.duracion_anos || 4,
      creditos_ects: programa.creditos_ects || 240,
      idioma: programa.idioma || 'español',
      modalidad: programa.modalidad || 'presencial',
      precio_anual_eur: programa.precio_anual_eur || '',
      plazas_disponibles: programa.plazas_disponibles || '',
      nota_corte: programa.nota_corte || '',
      url_info: programa.url_info || '',
      requisitos: programa.requisitos || '',
      descripcion: programa.descripcion || ''
    })
    setEditando(programa.id)
    setMostrarFormulario(true)
  }

  const eliminarPrograma = async (id, nombre) => {
    if (!confirm(`¿Desactivar programa "${nombre}"?`)) return

    try {
      const response = await axios.delete(`${API_URL}/api/admin/programas/${id}`)
      if (response.data.success) {
        alert('Programa desactivado')
        cargarProgramas()
      }
    } catch (error) {
      console.error('Error eliminando programa:', error)
      alert('Error al eliminar programa')
    }
  }

  const resetFormulario = () => {
    setFormulario({
      universidad_id: '',
      nombre: '',
      tipo_programa: 'grado',
      area_estudio: '',
      duracion_anos: 4,
      creditos_ects: 240,
      idioma: 'español',
      modalidad: 'presencial',
      precio_anual_eur: '',
      plazas_disponibles: '',
      nota_corte: '',
      url_info: '',
      requisitos: '',
      descripcion: ''
    })
    setEditando(null)
    setMostrarFormulario(false)
  }

  return (
    <div className="admin-universidades-container">
      <div className="header-admin-uni">
        <h1>📚 Gestión de Programas Académicos</h1>
        {universidadSeleccionada && (
          <button 
            className="btn-nuevo"
            onClick={() => {
              resetFormulario()
              setMostrarFormulario(!mostrarFormulario)
            }}
          >
            {mostrarFormulario ? '❌ Cancelar' : '➕ Nuevo Programa'}
          </button>
        )}
      </div>

      <div className="filtros-admin">
        <select
          value={universidadSeleccionada}
          onChange={(e) => setUniversidadSeleccionada(e.target.value)}
          style={{flex: 1, padding: '12px', fontSize: '16px'}}
        >
          <option value="">🏛️ Selecciona una universidad...</option>
          {universidades.map(uni => (
            <option key={uni.id} value={uni.id}>
              {uni.nombre} ({uni.ciudad})
            </option>
          ))}
        </select>
      </div>

      {!universidadSeleccionada && (
        <div className="sin-resultados">
          <p>👆 Selecciona una universidad para ver sus programas</p>
        </div>
      )}

      {universidadSeleccionada && mostrarFormulario && (
        <div className="formulario-universidad">
          <h2>{editando ? '✏️ Editar Programa' : '➕ Nuevo Programa'}</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group full-width">
                <label>Nombre del Programa *</label>
                <input
                  type="text"
                  name="nombre"
                  value={formulario.nombre}
                  onChange={handleInputChange}
                  required
                  placeholder="Ej: Grado en Ingeniería Informática"
                />
              </div>

              <div className="form-group">
                <label>Tipo *</label>
                <select
                  name="tipo_programa"
                  value={formulario.tipo_programa}
                  onChange={handleInputChange}
                  required
                >
                  <option value="grado">Grado</option>
                  <option value="master">Máster</option>
                  <option value="doctorado">Doctorado</option>
                  <option value="diplomatura">Diplomatura</option>
                </select>
              </div>

              <div className="form-group">
                <label>Área de Estudio</label>
                <input
                  type="text"
                  name="area_estudio"
                  value={formulario.area_estudio}
                  onChange={handleInputChange}
                  placeholder="Ej: Ingeniería y Tecnología"
                />
              </div>

              <div className="form-group">
                <label>Duración (años)</label>
                <input
                  type="number"
                  name="duracion_anos"
                  value={formulario.duracion_anos}
                  onChange={handleInputChange}
                  min="1"
                  max="10"
                />
              </div>

              <div className="form-group">
                <label>Créditos ECTS</label>
                <input
                  type="number"
                  name="creditos_ects"
                  value={formulario.creditos_ects}
                  onChange={handleInputChange}
                  placeholder="240"
                />
              </div>

              <div className="form-group">
                <label>Idioma</label>
                <input
                  type="text"
                  name="idioma"
                  value={formulario.idioma}
                  onChange={handleInputChange}
                  placeholder="español, inglés, catalán..."
                />
              </div>

              <div className="form-group">
                <label>Modalidad</label>
                <select
                  name="modalidad"
                  value={formulario.modalidad}
                  onChange={handleInputChange}
                >
                  <option value="presencial">Presencial</option>
                  <option value="online">Online</option>
                  <option value="semipresencial">Semipresencial</option>
                </select>
              </div>

              <div className="form-group">
                <label>Precio Anual (EUR)</label>
                <input
                  type="number"
                  name="precio_anual_eur"
                  value={formulario.precio_anual_eur}
                  onChange={handleInputChange}
                  placeholder="1500"
                />
              </div>

              <div className="form-group">
                <label>Plazas Disponibles</label>
                <input
                  type="number"
                  name="plazas_disponibles"
                  value={formulario.plazas_disponibles}
                  onChange={handleInputChange}
                  placeholder="50"
                />
              </div>

              <div className="form-group">
                <label>Nota de Corte</label>
                <input
                  type="number"
                  step="0.01"
                  name="nota_corte"
                  value={formulario.nota_corte}
                  onChange={handleInputChange}
                  placeholder="7.50"
                />
              </div>

              <div className="form-group">
                <label>URL Info</label>
                <input
                  type="url"
                  name="url_info"
                  value={formulario.url_info}
                  onChange={handleInputChange}
                  placeholder="https://..."
                />
              </div>

              <div className="form-group full-width">
                <label>Requisitos</label>
                <textarea
                  name="requisitos"
                  value={formulario.requisitos}
                  onChange={handleInputChange}
                  rows="2"
                  placeholder="Ej: Bachillerato, prueba de acceso..."
                />
              </div>

              <div className="form-group full-width">
                <label>Descripción</label>
                <textarea
                  name="descripcion"
                  value={formulario.descripcion}
                  onChange={handleInputChange}
                  rows="3"
                  placeholder="Breve descripción del programa..."
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-guardar" disabled={loading}>
                {loading ? '⏳ Guardando...' : (editando ? '💾 Actualizar' : '➕ Crear')}
              </button>
              <button type="button" className="btn-cancelar" onClick={resetFormulario}>
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {universidadSeleccionada && !mostrarFormulario && (
        <>
          {loading ? (
            <div className="loading">Cargando programas...</div>
          ) : (
            <div className="tabla-universidades">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Tipo</th>
                    <th>Duración</th>
                    <th>ECTS</th>
                    <th>Idioma</th>
                    <th>Precio (EUR)</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {programas.map(prog => (
                    <tr key={prog.id}>
                      <td>{prog.id}</td>
                      <td><strong>{prog.nombre}</strong></td>
                      <td>
                        <span className={`badge-tipo ${prog.tipo_programa}`}>
                          {prog.tipo_programa}
                        </span>
                      </td>
                      <td>{prog.duracion_anos} años</td>
                      <td>{prog.creditos_ects}</td>
                      <td>{prog.idioma}</td>
                      <td>{prog.precio_anual_eur ? `€${prog.precio_anual_eur.toLocaleString()}` : 'N/A'}</td>
                      <td className="acciones">
                        <button 
                          className="btn-editar"
                          onClick={() => editarPrograma(prog)}
                          title="Editar"
                        >
                          ✏️
                        </button>
                        <button 
                          className="btn-eliminar"
                          onClick={() => eliminarPrograma(prog.id, prog.nombre)}
                          title="Desactivar"
                        >
                          🗑️
                        </button>
                        {prog.url_info && (
                          <a 
                            href={prog.url_info}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn-web"
                            title="Ver info"
                          >
                            🌐
                          </a>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {programas.length === 0 && (
                <div className="sin-resultados">
                  <p>📚 No hay programas registrados para esta universidad</p>
                  <p>Haz clic en "Nuevo Programa" para agregar uno</p>
                </div>
              )}
            </div>
          )}

          <div className="stats-footer">
            <p><strong>Total:</strong> {programas.length} programas</p>
          </div>
        </>
      )}
    </div>
  )
}

export default AdminProgramas
