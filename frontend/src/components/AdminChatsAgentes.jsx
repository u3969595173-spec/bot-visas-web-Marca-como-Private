import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import '../components/AdminUniversidades.css'
import './ChatAdmin.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://botvisas.onrender.com'

function AdminChatsAgentes() {
  const [agentes, setAgentes] = useState([])
  const [agenteActivo, setAgenteActivo] = useState(null)
  const [mensajes, setMensajes] = useState([])
  const [mensaje, setMensaje] = useState('')
  const [loading, setLoading] = useState(false)
  const [noLeidos, setNoLeidos] = useState(0)
  const mensajesEndRef = useRef(null)

  useEffect(() => {
    cargarAgentes()
    cargarNoLeidos()
    const interval = setInterval(() => {
      cargarNoLeidos()
      if (agenteActivo) {
        cargarMensajes(agenteActivo.id)
      }
    }, 10000) // Actualizar cada 10s
    return () => clearInterval(interval)
  }, [agenteActivo])

  useEffect(() => {
    mensajesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [mensajes])

  const cargarAgentes = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/api/admin/agentes/estadisticas`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setAgentes(response.data.agentes || [])
    } catch (error) {
      console.error('Error cargando agentes:', error)
    }
  }

  const cargarNoLeidos = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/api/admin/agentes/mensajes/no-leidos`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setNoLeidos(response.data.no_leidos || 0)
    } catch (error) {
      console.error('Error cargando no leídos:', error)
    }
  }

  const cargarMensajes = async (agenteId) => {
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/api/admin/agentes/${agenteId}/mensajes`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setMensajes(response.data.mensajes || [])
      cargarNoLeidos() // Actualizar contador después de marcar como leídos
    } catch (error) {
      console.error('Error cargando mensajes:', error)
    } finally {
      setLoading(false)
    }
  }

  const seleccionarAgente = (agente) => {
    setAgenteActivo(agente)
    cargarMensajes(agente.id)
  }

  const enviarMensaje = async (e) => {
    e.preventDefault()
    if (!mensaje.trim() || !agenteActivo) return

    try {
      const token = localStorage.getItem('token')
      await axios.post(
        `${API_URL}/api/admin/agentes/${agenteActivo.id}/enviar-mensaje`,
        { mensaje: mensaje.trim() },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      
      setMensaje('')
      cargarMensajes(agenteActivo.id)
    } catch (error) {
      console.error('Error enviando mensaje:', error)
      alert('Error enviando mensaje')
    }
  }

  const formatearFecha = (fecha) => {
    if (!fecha) return ''
    const d = new Date(fecha)
    const hoy = new Date()
    const esHoy = d.toDateString() === hoy.toDateString()
    
    if (esHoy) {
      return d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
    }
    return d.toLocaleString('es-ES', { 
      day: '2-digit', 
      month: 'short', 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <div className="admin-chats-container">
      <div className="chats-layout">
        {/* Lista de Agentes */}
        <div className="conversaciones-list">
          <div className="conversaciones-header">
            <h3>💼 Agentes {noLeidos > 0 && <span className="badge-no-leidos">{noLeidos}</span>}</h3>
          </div>
          
          {agentes.length === 0 ? (
            <div className="no-conversaciones">
              <p>No hay agentes registrados</p>
            </div>
          ) : (
            <div className="conversaciones-items">
              {agentes.map(agente => (
                <div
                  key={agente.id}
                  className={`conversacion-item ${agenteActivo?.id === agente.id ? 'active' : ''}`}
                  onClick={() => seleccionarAgente(agente)}
                >
                  <div className="conversacion-info">
                    <div className="conversacion-nombre">
                      {agente.nombre}
                    </div>
                    <div className="conversacion-email">
                      {agente.email}
                    </div>
                  </div>
                  <div className="conversacion-meta">
                    <div className="conversacion-codigo">
                      Código: {agente.codigo_referido}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Chat Activo */}
        <div className="chat-area">
          {!agenteActivo ? (
            <div className="no-chat-seleccionado">
              <p>👈 Selecciona un agente para ver la conversación</p>
            </div>
          ) : (
            <>
              <div className="chat-header">
                <div className="chat-header-info">
                  <h3>{agenteActivo.nombre}</h3>
                  <p>{agenteActivo.email}</p>
                </div>
              </div>

              <div className="chat-mensajes">
                {loading ? (
                  <div className="loading-mensajes">Cargando mensajes...</div>
                ) : mensajes.length === 0 ? (
                  <div className="no-mensajes">
                    <p>No hay mensajes. Inicia la conversación 👇</p>
                  </div>
                ) : (
                  mensajes.map(msg => (
                    <div
                      key={msg.id}
                      className={`mensaje ${msg.remitente === 'admin' ? 'mensaje-admin' : 'mensaje-usuario'}`}
                    >
                      <div className="mensaje-contenido">
                        <div className="mensaje-texto">{msg.mensaje}</div>
                        <div className="mensaje-fecha">{formatearFecha(msg.fecha)}</div>
                      </div>
                    </div>
                  ))
                )}
                <div ref={mensajesEndRef} />
              </div>

              <form className="chat-input-form" onSubmit={enviarMensaje}>
                <input
                  type="text"
                  value={mensaje}
                  onChange={(e) => setMensaje(e.target.value)}
                  placeholder="Escribe un mensaje..."
                  className="chat-input"
                />
                <button type="submit" className="btn-enviar-mensaje">
                  📤 Enviar
                </button>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminChatsAgentes
