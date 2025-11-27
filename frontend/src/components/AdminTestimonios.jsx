import React, { useState, useEffect } from 'react'
import axios from 'axios'
import '../components/AdminUniversidades.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'

function AdminTestimonios() {
  const [testimonios, setTestimonios] = useState([])
  const [pendientes, setPendientes] = useState([])
  const [loading, setLoading] = useState(false)
  const [mostrarPendientes, setMostrarPendientes] = useState(true)

  useEffect(() => {
    cargarTestimonios()
    cargarPendientes()
  }, [])

  const cargarTestimonios = async () => {
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/api/admin/testimonios`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (response.data.success) {
        setTestimonios(response.data.testimonios)
      }
    } catch (error) {
      console.error('Error cargando testimonios:', error)
      alert('Error cargando testimonios')
    } finally {
      setLoading(false)
    }
  }

  const cargarPendientes = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/api/admin/testimonios/pendientes`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (response.data.success) {
        setPendientes(response.data.testimonios)
      }
    } catch (error) {
      console.error('Error cargando pendientes:', error)
    }
  }

  const aprobarTestimonio = async (id, destacar = false) => {
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        `${API_URL}/api/admin/testimonios/${id}/aprobar`,
        { destacar },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      if (response.data.success) {
        alert('Testimonio aprobado')
        cargarTestimonios()
        cargarPendientes()
      }
    } catch (error) {
      console.error('Error aprobando:', error)
      alert('Error al aprobar testimonio')
    } finally {
      setLoading(false)
    }
  }

  const rechazarTestimonio = async (id) => {
    if (!confirm('¿Rechazar este testimonio? Se ocultará del público.')) return
    
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        `${API_URL}/api/admin/testimonios/${id}/rechazar`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      if (response.data.success) {
        alert('Testimonio rechazado')
        cargarTestimonios()
        cargarPendientes()
      }
    } catch (error) {
      console.error('Error rechazando:', error)
      alert('Error al rechazar testimonio')
    } finally {
      setLoading(false)
    }
  }

  const toggleDestacado = async (id) => {
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await axios.put(
        `${API_URL}/api/admin/testimonios/${id}/destacar`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      if (response.data.success) {
        cargarTestimonios()
      }
    } catch (error) {
      console.error('Error cambiando destacado:', error)
    } finally {
      setLoading(false)
    }
  }

  const eliminarTestimonio = async (id, nombre) => {
    if (!confirm(`¿Eliminar permanentemente el testimonio de ${nombre}?`)) return
    
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      await axios.delete(`${API_URL}/api/admin/testimonios/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      alert('Testimonio eliminado')
      cargarTestimonios()
      cargarPendientes()
    } catch (error) {
      console.error('Error eliminando:', error)
      alert('Error al eliminar testimonio')
    } finally {
      setLoading(false)
    }
  }

  const renderEstrellas = (rating) => {
    return '⭐'.repeat(rating || 5)
  }

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>⭐ Gestión de Testimonios</h1>
        <div className="admin-actions">
          <button 
            className={mostrarPendientes ? 'btn-primary' : 'btn-secondary'}
            onClick={() => setMostrarPendientes(!mostrarPendientes)}
          >
            {mostrarPendientes ? '📋 Ver todos' : '⏰ Ver pendientes'}
            {pendientes.length > 0 && mostrarPendientes && (
              <span className="badge">{pendientes.length}</span>
            )}
          </button>
        </div>
      </div>

      {loading && <div className="loading">Cargando...</div>}

      {mostrarPendientes && (
        <div className="seccion-pendientes">
          <h2>⏰ Pendientes de aprobar ({pendientes.length})</h2>
          {pendientes.length === 0 ? (
            <p className="mensaje-vacio">✅ No hay testimonios pendientes</p>
          ) : (
            <div className="tabla-container">
              <table className="tabla-admin">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Rating</th>
                    <th>País</th>
                    <th>Universidad</th>
                    <th>Testimonio</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {pendientes.map(t => (
                    <tr key={t.id}>
                      <td>{t.id}</td>
                      <td>{t.nombre_completo}</td>
                      <td>{renderEstrellas(t.rating)}</td>
                      <td>{t.pais_origen}</td>
                      <td>{t.universidad || '-'}</td>
                      <td className="testimonio-preview">
                        {t.titulo && <strong>{t.titulo}</strong>}
                        <div>{t.testimonio.substring(0, 100)}...</div>
                      </td>
                      <td>
                        <div className="acciones-grupo">
                          <button
                            className="btn-aprobar"
                            onClick={() => aprobarTestimonio(t.id, false)}
                            title="Aprobar"
                          >
                            ✅
                          </button>
                          <button
                            className="btn-destacar"
                            onClick={() => aprobarTestimonio(t.id, true)}
                            title="Aprobar y Destacar"
                          >
                            ⭐
                          </button>
                          <button
                            className="btn-eliminar"
                            onClick={() => rechazarTestimonio(t.id)}
                            title="Rechazar"
                          >
                            ❌
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {!mostrarPendientes && (
        <div className="seccion-todos">
          <h2>📋 Todos los testimonios ({testimonios.length})</h2>
          {testimonios.length === 0 ? (
            <p className="mensaje-vacio">No hay testimonios</p>
          ) : (
            <div className="tabla-container">
              <table className="tabla-admin">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Rating</th>
                    <th>Aprobado</th>
                    <th>Destacado</th>
                    <th>Visible</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {testimonios.map(t => (
                    <tr key={t.id}>
                      <td>{t.id}</td>
                      <td>{t.nombre_completo}</td>
                      <td>{renderEstrellas(t.rating)}</td>
                      <td>{t.aprobado ? '✅' : '⏰'}</td>
                      <td>{t.destacado ? '⭐' : ''}</td>
                      <td>{t.visible ? '👁️' : '🚫'}</td>
                      <td>{new Date(t.created_at).toLocaleDateString()}</td>
                      <td>
                        <div className="acciones-grupo">
                          {t.aprobado && (
                            <button
                              className={t.destacado ? 'btn-destacado-activo' : 'btn-destacar'}
                              onClick={() => toggleDestacado(t.id)}
                              title={t.destacado ? 'Quitar destacado' : 'Destacar'}
                            >
                              ⭐
                            </button>
                          )}
                          {!t.aprobado && (
                            <button
                              className="btn-aprobar"
                              onClick={() => aprobarTestimonio(t.id)}
                              title="Aprobar"
                            >
                              ✅
                            </button>
                          )}
                          <button
                            className="btn-eliminar"
                            onClick={() => eliminarTestimonio(t.id, t.nombre_completo)}
                            title="Eliminar"
                          >
                            🗑️
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      <div className="admin-stats">
        <p>Total: {testimonios.length} testimonios | Pendientes: {pendientes.length}</p>
      </div>
    </div>
  )
}

export default AdminTestimonios
