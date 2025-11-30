import React, { useState, useEffect, useRef } from 'react'
import './ChatWidget.css'

const API_URL = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com'
const WS_URL = API_URL.replace('https://', 'wss://').replace('http://', 'ws://')

function ChatWidget({ estudianteId }) {
  const [abierto, setAbierto] = useState(false)
  const [mensajes, setMensajes] = useState([])
  const [mensaje, setMensaje] = useState('')
  const [conectado, setConectado] = useState(false)
  const [noLeidos, setNoLeidos] = useState(0)
  const wsRef = useRef(null)
  const mensajesEndRef = useRef(null)

  // Cargar historial al abrir
  useEffect(() => {
    if (abierto && estudianteId) {
      cargarHistorial()
      conectarWebSocket()
      // Marcar como leídos al abrir el chat
      marcarComoLeido()
    }
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [abierto, estudianteId])

  // Scroll automático al último mensaje
  useEffect(() => {
    mensajesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [mensajes])

  // Polling no leídos cada 30s
  useEffect(() => {
    if (!estudianteId) return
    
    cargarNoLeidos()
    const interval = setInterval(cargarNoLeidos, 30000)
    return () => clearInterval(interval)
  }, [estudianteId])

  const cargarHistorial = async () => {
    try {
      const response = await fetch(`${API_URL}/api/chat/${estudianteId}/mensajes`)
      const data = await response.json()
      if (data.success) {
        setMensajes(data.mensajes)
      }
    } catch (error) {
      console.error('Error cargando historial:', error)
    }
  }

  const cargarNoLeidos = async () => {
    try {
      const response = await fetch(`${API_URL}/api/chat/${estudianteId}/no-leidos?remitente=admin`)
      const data = await response.json()
      if (data.success) {
        setNoLeidos(data.no_leidos)
      }
    } catch (error) {
      console.error('Error cargando no leídos:', error)
    }
  }

  const conectarWebSocket = () => {
    try {
      const ws = new WebSocket(`${WS_URL}/api/ws/chat/${estudianteId}/estudiante`)
      
      ws.onopen = () => {
        console.log('✅ WebSocket conectado')
        setConectado(true)
      }
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        console.log('📩 Mensaje recibido:', data)
        
        // Agregar nuevo mensaje a la lista
        setMensajes(prev => [...prev, data])
        
        // Si es mensaje del admin, incrementar no leídos si chat cerrado
        if (data.remitente === 'admin' && !abierto) {
          setNoLeidos(prev => prev + 1)
        }
      }
      
      ws.onclose = () => {
        console.log('❌ WebSocket desconectado')
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
    if (!mensaje.trim()) {
      return
    }

    const mensajeTexto = mensaje.trim();
    
    // Crear mensaje temporal para mostrar inmediatamente
    const mensajeTemporal = {
      id: `temp-${Date.now()}`,
      estudiante_id: estudianteId,
      mensaje: mensajeTexto,
      remitente: 'estudiante',
      tipo: 'texto',
      created_at: new Date().toISOString()
    }

    // Mostrar inmediatamente en la UI
    setMensajes(prev => [...prev, mensajeTemporal])
    setMensaje('')

    // Si hay WebSocket conectado, enviar por ahí
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      const mensajeData = {
        estudiante_id: estudianteId,
        mensaje: mensajeTexto,
        remitente: 'estudiante',
        tipo: 'texto'
      }
      wsRef.current.send(JSON.stringify(mensajeData))
    } else {
      // Fallback: enviar por HTTP si WebSocket no está disponible
      fetch(`${API_URL}/api/estudiantes/${estudianteId}/mensajes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          remitente: 'estudiante',
          mensaje: mensajeTexto
        })
      }).catch(err => console.error('Error enviando mensaje:', err))
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      enviarMensaje()
    }
  }

  const marcarComoLeido = async () => {
    try {
      const response = await fetch(`${API_URL}/api/estudiante/chat/${estudianteId}/marcar-leidos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      if (response.ok) {
        setNoLeidos(0)
        console.log('✅ Mensajes marcados como leídos')
        // Recargar contador después de marcar
        setTimeout(() => cargarNoLeidos(), 500)
      }
    } catch (error) {
      console.error('Error marcando como leído:', error)
    }
  }

  const toggleChat = () => {
    const nuevoEstado = !abierto
    setAbierto(nuevoEstado)
    if (nuevoEstado) {
      // Marcar mensajes como leídos cuando se abre el chat
      setTimeout(() => marcarComoLeido(), 1000)
    }
  }

  const formatearHora = (fecha) => {
    return new Date(fecha).toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (!estudianteId) {
    return null
  }

  return (
    <>
      {/* Botón flotante */}
      <button
        className={`chat-widget-button ${abierto ? 'abierto' : ''}`}
        onClick={toggleChat}
        title="Chat con soporte"
      >
        💬
        {noLeidos > 0 && !abierto && (
          <span className="chat-badge">{noLeidos > 99 ? '99+' : noLeidos}</span>
        )}
      </button>

      {/* Ventana de chat */}
      {abierto && (
        <div className="chat-widget-container">
          <div className="chat-widget-header">
            <div className="chat-header-info">
              <h3>💬 Chat con Soporte</h3>
              <span className={`chat-status ${conectado ? 'conectado' : 'desconectado'}`}>
                {conectado ? '● En línea' : '○ Desconectado'}
              </span>
            </div>
            <button className="chat-close-button" onClick={toggleChat}>✕</button>
          </div>

          <div className="chat-widget-mensajes">
            {mensajes.length === 0 ? (
              <div className="chat-vacio">
                <p>👋 ¡Hola! Estamos aquí para ayudarte.</p>
                <p>Envía un mensaje y te responderemos pronto.</p>
              </div>
            ) : (
              mensajes.map((msg, index) => (
                <div
                  key={msg.id || index}
                  className={`chat-mensaje ${msg.remitente === 'estudiante' ? 'propio' : 'ajeno'}`}
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

          <div className="chat-widget-input">
            <textarea
              value={mensaje}
              onChange={(e) => setMensaje(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Escribe tu mensaje..."
              rows="2"
            />
            <button
              className="chat-send-button"
              onClick={enviarMensaje}
              disabled={!mensaje.trim()}
            >
              ➤
            </button>
          </div>
        </div>
      )}
    </>
  )
}

export default ChatWidget
