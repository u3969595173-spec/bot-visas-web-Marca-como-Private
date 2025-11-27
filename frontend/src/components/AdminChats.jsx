import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import '../components/AdminUniversidades.css'
import './ChatAdmin.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'
const WS_URL = API_URL.replace('https://', 'wss://').replace('http://', 'ws://')

function AdminChats() {
  const [conversaciones, setConversaciones] = useState([])
  const [conversacionActiva, setConversacionActiva] = useState(null)
  const [mensajes, setMensajes] = useState([])
  const [mensaje, setMensaje] = useState('')
  const [conectado, setConectado] = useState(false)
  const [loading, setLoading] = useState(false)
  const wsRef = useRef(null)
  const mensajesEndRef = useRef(null)

  useEffect(() => {
    cargarConversaciones()
    const interval = setInterval(cargarConversaciones, 30000) // Actualizar cada 30s
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    if (conversacionActiva) {
      cargarMensajes(conversacionActiva.estudiante_id)
      conectarWebSocket(conversacionActiva.estudiante_id)
    }
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [conversacionActiva])

  useEffect(() => {
    mensajesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [mensajes])

  const cargarConversaciones = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/api/admin/chat/conversaciones`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (response.data.success) {
        setConversaciones(response.data.conversaciones)
      }
    } catch (error) {
      console.error('Error cargando conversaciones:', error)
    }
  }

  const cargarMensajes = async (estudianteId) => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_URL}/api/chat/${estudianteId}/mensajes`)
      if (response.data.success) {
        setMensajes(response.data.mensajes)
      }
    } catch (error) {
      console.error('Error cargando mensajes:', error)
    } finally {
      setLoading(false)
    }
  }

  const conectarWebSocket = (estudianteId) => {
    try {
      const ws = new WebSocket(`${WS_URL}/api/ws/chat/${estudianteId}/admin`)
      
      ws.onopen = () => {
        console.log('✅ Admin WebSocket conectado')
        setConectado(true)
      }
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        console.log('📩 Mensaje recibido:', data)
        
        if (data.type === 'nuevo_mensaje_estudiante') {
          // Actualizar contador de conversaciones
          cargarConversaciones()
          // Si es la conversación activa, agregar mensaje
          if (data.estudiante_id === conversacionActiva?.estudiante_id) {
            setMensajes(prev => [...prev, data.message])
          }
        } else {
          // Mensaje normal
          setMensajes(prev => [...prev, data])
        }
      }
      
      ws.onclose = () => {
        console.log('❌ Admin WebSocket desconectado')
        setConectado(false)
      }
      
      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
        setConectado(false)
      }
      
      wsRef.current = ws
    } catch (error) {
      console.error('Error conectando WebSocket:', error)
    }
  }

  const enviarMensaje = () => {
    if (!mensaje.trim() || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      return
    }

    const mensajeData = {
      estudiante_id: conversacionActiva.estudiante_id,
      mensaje: mensaje,
      remitente: 'admin',
      admin_id: 1, // TODO: obtener ID real del admin
      tipo: 'texto'
    }

    wsRef.current.send(JSON.stringify(mensajeData))
    setMensaje('')
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      enviarMensaje()
    }
  }

  const formatearHora = (fecha) => {
    return new Date(fecha).toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const formatearFecha = (fecha) => {
    const date = new Date(fecha)
    const hoy = new Date()
    const ayer = new Date(hoy)
    ayer.setDate(ayer.getDate() - 1)

    if (date.toDateString() === hoy.toDateString()) {
      return 'Hoy'
    } else if (date.toDateString() === ayer.toDateString()) {
      return 'Ayer'
    } else {
      return date.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' })
    }
  }

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>💬 Chat con Estudiantes</h1>
      </div>

      <div className="chat-admin-layout">
        {/* Lista de conversaciones */}
        <div className="chat-conversaciones-panel">
          <h3>Conversaciones ({conversaciones.length})</h3>
          {conversaciones.length === 0 ? (
            <p className="mensaje-vacio">No hay conversaciones activas</p>
          ) : (
            <div className="conversaciones-lista">
              {conversaciones.map(conv => (
                <div
                  key={conv.estudiante_id}
                  className={`conversacion-item ${conversacionActiva?.estudiante_id === conv.estudiante_id ? 'activa' : ''}`}
                  onClick={() => setConversacionActiva(conv)}
                >
                  <div className="conversacion-avatar">
                    {conv.nombre?.charAt(0) || '?'}
                  </div>
                  <div className="conversacion-info">
                    <div className="conversacion-nombre">{conv.nombre}</div>
                    <div className="conversacion-email">{conv.email}</div>
                    <div className="conversacion-fecha">
                      {formatearFecha(conv.ultimo_mensaje)}
                    </div>
                  </div>
                  {conv.no_leidos > 0 && (
                    <span className="conversacion-badge">{conv.no_leidos}</span>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Chat activo */}
        <div className="chat-mensajes-panel">
          {!conversacionActiva ? (
            <div className="chat-sin-seleccionar">
              <p>👈 Selecciona una conversación para comenzar</p>
            </div>
          ) : (
            <>
              <div className="chat-mensajes-header">
                <div>
                  <h3>{conversacionActiva.nombre}</h3>
                  <p>{conversacionActiva.email}</p>
                </div>
                <span className={`chat-status ${conectado ? 'conectado' : 'desconectado'}`}>
                  {conectado ? '● Conectado' : '○ Desconectado'}
                </span>
              </div>

              <div className="chat-mensajes-contenido">
                {loading ? (
                  <div className="loading">Cargando mensajes...</div>
                ) : mensajes.length === 0 ? (
                  <div className="chat-vacio">
                    <p>No hay mensajes en esta conversación</p>
                  </div>
                ) : (
                  mensajes.map((msg, index) => (
                    <div
                      key={msg.id || index}
                      className={`chat-mensaje ${msg.remitente === 'admin' ? 'admin' : 'estudiante'}`}
                    >
                      <div className="chat-mensaje-contenido">
                        {msg.mensaje}
                      </div>
                      <div className="chat-mensaje-hora">
                        {formatearHora(msg.created_at)}
                      </div>
                    </div>
                  ))
                )}
                <div ref={mensajesEndRef} />
              </div>

              <div className="chat-mensajes-input">
                <textarea
                  value={mensaje}
                  onChange={(e) => setMensaje(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Escribe tu respuesta..."
                  rows="3"
                  disabled={!conectado}
                />
                <button
                  className="btn-enviar-mensaje"
                  onClick={enviarMensaje}
                  disabled={!conectado || !mensaje.trim()}
                >
                  ➤ Enviar
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminChats
