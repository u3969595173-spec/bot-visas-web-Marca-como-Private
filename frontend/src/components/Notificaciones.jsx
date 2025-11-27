import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'
import './Notificaciones.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'

function Notificaciones({ estudianteId }) {
  const [notificaciones, setNotificaciones] = useState([])
  const [noLeidas, setNoLeidas] = useState(0)
  const [mostrarDropdown, setMostrarDropdown] = useState(false)
  const [loading, setLoading] = useState(false)

  // Cargar contador de no leídas cada 30 segundos
  useEffect(() => {
    if (!estudianteId) return

    cargarContador()
    const interval = setInterval(cargarContador, 30000) // 30 segundos

    return () => clearInterval(interval)
  }, [estudianteId])

  // Cargar notificaciones cuando se abre el dropdown
  useEffect(() => {
    if (mostrarDropdown && estudianteId) {
      cargarNotificaciones()
    }
  }, [mostrarDropdown, estudianteId])

  const cargarContador = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/notificaciones/${estudianteId}/contar`)
      if (response.data.success) {
        setNoLeidas(response.data.no_leidas)
      }
    } catch (error) {
      console.error('Error cargando contador:', error)
    }
  }

  const cargarNotificaciones = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_URL}/api/notificaciones/${estudianteId}?limit=20`)
      if (response.data.success) {
        setNotificaciones(response.data.notificaciones)
      }
    } catch (error) {
      console.error('Error cargando notificaciones:', error)
    } finally {
      setLoading(false)
    }
  }

  const marcarLeida = async (notificacionId) => {
    try {
      await axios.post(`${API_URL}/api/notificaciones/${notificacionId}/marcar-leida`)
      
      // Actualizar estado local
      setNotificaciones(prev =>
        prev.map(n =>
          n.id === notificacionId ? { ...n, leida: true } : n
        )
      )
      
      // Actualizar contador
      setNoLeidas(prev => Math.max(0, prev - 1))
    } catch (error) {
      console.error('Error marcando leída:', error)
    }
  }

  const marcarTodasLeidas = async () => {
    try {
      await axios.post(`${API_URL}/api/notificaciones/${estudianteId}/marcar-todas-leidas`)
      
      // Actualizar estado local
      setNotificaciones(prev =>
        prev.map(n => ({ ...n, leida: true }))
      )
      setNoLeidas(0)
    } catch (error) {
      console.error('Error marcando todas leídas:', error)
    }
  }

  const handleNotificacionClick = (notificacion) => {
    if (!notificacion.leida) {
      marcarLeida(notificacion.id)
    }
    
    // Si tiene URL de acción, navegar
    if (notificacion.url_accion) {
      setMostrarDropdown(false)
      // El Link en el JSX manejará la navegación
    }
  }

  const formatearTiempo = (fecha) => {
    const ahora = new Date()
    const entonces = new Date(fecha)
    const diffMs = ahora - entonces
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)

    if (diffMins < 1) return 'Ahora'
    if (diffMins < 60) return `Hace ${diffMins}m`
    if (diffHours < 24) return `Hace ${diffHours}h`
    if (diffDays < 7) return `Hace ${diffDays}d`
    return entonces.toLocaleDateString()
  }

  if (!estudianteId) {
    return null
  }

  return (
    <div className="notificaciones-container">
      <button
        className="notificaciones-campana"
        onClick={() => setMostrarDropdown(!mostrarDropdown)}
        title="Notificaciones"
      >
        🔔
        {noLeidas > 0 && (
          <span className="notificaciones-badge">{noLeidas > 99 ? '99+' : noLeidas}</span>
        )}
      </button>

      {mostrarDropdown && (
        <>
          <div
            className="notificaciones-overlay"
            onClick={() => setMostrarDropdown(false)}
          />
          <div className="notificaciones-dropdown">
            <div className="notificaciones-header">
              <h3>🔔 Notificaciones</h3>
              {noLeidas > 0 && (
                <button
                  className="btn-marcar-todas"
                  onClick={marcarTodasLeidas}
                >
                  Marcar todas leídas
                </button>
              )}
            </div>

            <div className="notificaciones-lista">
              {loading ? (
                <div className="notificaciones-loading">Cargando...</div>
              ) : notificaciones.length === 0 ? (
                <div className="notificaciones-vacio">
                  <p>📭 No tienes notificaciones</p>
                </div>
              ) : (
                notificaciones.map(notif => (
                  <div
                    key={notif.id}
                    className={`notificacion-item ${!notif.leida ? 'no-leida' : ''} prioridad-${notif.prioridad}`}
                    onClick={() => handleNotificacionClick(notif)}
                  >
                    {notif.url_accion ? (
                      <Link to={notif.url_accion} className="notificacion-link">
                        <div className="notificacion-icono">{notif.icono}</div>
                        <div className="notificacion-contenido">
                          <div className="notificacion-titulo">{notif.titulo}</div>
                          <div className="notificacion-mensaje">{notif.mensaje}</div>
                          <div className="notificacion-tiempo">{formatearTiempo(notif.created_at)}</div>
                        </div>
                        {!notif.leida && <div className="notificacion-punto"></div>}
                      </Link>
                    ) : (
                      <>
                        <div className="notificacion-icono">{notif.icono}</div>
                        <div className="notificacion-contenido">
                          <div className="notificacion-titulo">{notif.titulo}</div>
                          <div className="notificacion-mensaje">{notif.mensaje}</div>
                          <div className="notificacion-tiempo">{formatearTiempo(notif.created_at)}</div>
                        </div>
                        {!notif.leida && <div className="notificacion-punto"></div>}
                      </>
                    )}
                  </div>
                ))
              )}
            </div>

            {notificaciones.length > 0 && (
              <div className="notificaciones-footer">
                <Link to="/estudiante/notificaciones" onClick={() => setMostrarDropdown(false)}>
                  Ver todas las notificaciones
                </Link>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}

export default Notificaciones
