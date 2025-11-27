import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './ChatMensajes.css';

const ChatMensajes = ({ estudianteId, remitente = 'estudiante' }) => {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const [mensajes, setMensajes] = useState([]);
  const [nuevoMensaje, setNuevoMensaje] = useState('');
  const [loading, setLoading] = useState(true);
  const [enviando, setEnviando] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    cargarMensajes();
    const interval = setInterval(cargarMensajes, 10000); // Actualizar cada 10 segundos
    return () => clearInterval(interval);
  }, [estudianteId]);

  useEffect(() => {
    scrollToBottom();
  }, [mensajes]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const cargarMensajes = async () => {
    try {
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}/mensajes`);
      setMensajes(response.data.mensajes);
      setLoading(false);
    } catch (err) {
      console.error('Error cargando mensajes:', err);
      setLoading(false);
    }
  };

  const enviarMensaje = async (e) => {
    e.preventDefault();
    if (!nuevoMensaje.trim()) return;

    const mensajeTexto = nuevoMensaje.trim();
    
    // Crear mensaje temporal para mostrar inmediatamente (optimistic UI)
    const mensajeTemporal = {
      id: `temp-${Date.now()}`,
      remitente,
      mensaje: mensajeTexto,
      created_at: new Date().toISOString(),
      temporal: true
    };

    // Mostrar inmediatamente en la interfaz
    setMensajes(prev => [...prev, mensajeTemporal]);
    setNuevoMensaje('');
    setEnviando(true);

    try {
      // Enviar al servidor
      await axios.post(`${apiUrl}/api/estudiantes/${estudianteId}/mensajes`, {
        remitente,
        mensaje: mensajeTexto
      });

      // Recargar mensajes del servidor para obtener el mensaje real
      await cargarMensajes();
    } catch (err) {
      console.error('Error enviando mensaje:', err);
      // Si falla, quitar el mensaje temporal
      setMensajes(prev => prev.filter(m => m.id !== mensajeTemporal.id));
      alert('Error al enviar el mensaje. Por favor intenta de nuevo.');
    } finally {
      setEnviando(false);
    }
  };

  const formatearFecha = (fecha) => {
    const date = new Date(fecha);
    const ahora = new Date();
    const diff = ahora - date;
    
    if (diff < 60000) return 'Hace un momento';
    if (diff < 3600000) return `Hace ${Math.floor(diff / 60000)} min`;
    if (diff < 86400000) return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    return date.toLocaleDateString('es-ES', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
  };

  if (loading) {
    return (
      <div className="chat-loading">
        <div className="spinner"></div>
        <p>Cargando mensajes...</p>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h3>💬 Mensajes con tu Asesor</h3>
        <p>Respuesta típica en menos de 24 horas</p>
      </div>

      <div className="chat-mensajes">
        {mensajes.length === 0 ? (
          <div className="chat-empty">
            <p style={{ fontSize: '48px', marginBottom: '15px' }}>💬</p>
            <p>No hay mensajes aún</p>
            <p style={{ color: '#999', fontSize: '14px' }}>
              Envía tu primera pregunta a nuestro equipo
            </p>
          </div>
        ) : (
          mensajes.map((msg) => (
            <div
              key={msg.id}
              className={`mensaje ${msg.remitente === 'admin' ? 'mensaje-admin' : 'mensaje-estudiante'}`}
            >
              <div className="mensaje-avatar">
                {msg.remitente === 'admin' ? '👨‍💼' : '👤'}
              </div>
              <div className="mensaje-contenido">
                <div className="mensaje-header">
                  <span className="mensaje-remitente">
                    {msg.remitente === 'admin' ? 'Asesor' : 'Tú'}
                  </span>
                  <span className="mensaje-fecha">
                    {formatearFecha(msg.created_at)}
                  </span>
                </div>
                <div className="mensaje-texto">
                  {msg.mensaje}
                </div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={enviarMensaje} className="chat-input">
        <input
          type="text"
          placeholder="Escribe tu mensaje..."
          value={nuevoMensaje}
          onChange={(e) => setNuevoMensaje(e.target.value)}
          disabled={enviando}
        />
        <button type="submit" disabled={enviando || !nuevoMensaje.trim()}>
          {enviando ? '⏳' : '📤'}
        </button>
      </form>
    </div>
  );
};

export default ChatMensajes;
