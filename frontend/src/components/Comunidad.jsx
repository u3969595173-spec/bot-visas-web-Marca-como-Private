import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Comunidad.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function Comunidad() {
    const navigate = useNavigate();
    const [mensajes, setMensajes] = useState([]);
    const [texto, setTexto] = useState('');
    const [enviando, setEnviando] = useState(false);
    const [error, setError] = useState('');
    const [cargando, setCargando] = useState(true);
    const bottomRef = useRef(null);
    const pollingRef = useRef(null);

    const getToken = () => localStorage.getItem('token');
    const getUser = () => {
        try { return JSON.parse(localStorage.getItem('capital_trade_user') || 'null'); }
        catch { return null; }
    };

    const userActual = getUser();

    const fetchMensajes = async (silencioso = false) => {
        const token = getToken();
        if (!token) { navigate('/login'); return; }
        try {
            const res = await axios.get(`${API}/api/comunidad/mensajes`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setMensajes(res.data.mensajes || []);
            if (!silencioso) setCargando(false);
        } catch (e) {
            if (!silencioso) {
                if (e.response?.status === 401) { navigate('/login'); }
                else { setCargando(false); setError('Error al cargar los mensajes.'); }
            }
        }
    };

    useEffect(() => {
        fetchMensajes(false);
        pollingRef.current = setInterval(() => fetchMensajes(true), 3000);
        return () => clearInterval(pollingRef.current);
    }, []);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [mensajes]);

    const enviar = async (e) => {
        e.preventDefault();
        if (!texto.trim() || enviando) return;
        setEnviando(true);
        setError('');
        try {
            const token = getToken();
            await axios.post(
                `${API}/api/comunidad/mensajes`,
                { mensaje: texto.trim() },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setTexto('');
            await fetchMensajes(true);
        } catch (e) {
            setError(e.response?.data?.detail || 'Error al enviar el mensaje.');
        } finally {
            setEnviando(false);
        }
    };

    const formatHora = (iso) => {
        if (!iso) return '';
        try {
            return new Date(iso).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
        } catch { return ''; }
    };

    const formatFecha = (iso) => {
        if (!iso) return '';
        try {
            return new Date(iso).toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
        } catch { return ''; }
    };

    const esHoy = (iso) => {
        if (!iso) return false;
        const d = new Date(iso);
        const hoy = new Date();
        return d.toDateString() === hoy.toDateString();
    };

    // Shows "Juan G." instead of full name
    const maskName = (nombre) => {
        if (!nombre) return '?';
        const parts = nombre.trim().split(/\s+/);
        if (parts.length === 1) return parts[0].length > 3 ? parts[0].slice(0, 3) + '***' : parts[0];
        return `${parts[0]} ${parts[1][0]}.`;
    };

    let ultimaFecha = null;

    return (
        <div className="comunidad-shell">
            {/* Header */}
            <div className="comunidad-header">
                <button className="comunidad-back" onClick={() => navigate(-1)}>←</button>
                <div className="comunidad-header-info">
                    <div className="comunidad-dot" />
                    <div>
                        <h1>Comunidad</h1>
                        <p>Chat de inversores — Capital Iberia</p>
                    </div>
                </div>
            </div>

            {/* Mensajes */}
            <div className="comunidad-messages">
                {cargando ? (
                    <div className="comunidad-loading">
                        <div className="comunidad-spinner" />
                        <p>Cargando mensajes...</p>
                    </div>
                ) : mensajes.length === 0 ? (
                    <div className="comunidad-empty">
                        <span>💬</span>
                        <p>No hay mensajes aún. ¡Sé el primero en escribir!</p>
                    </div>
                ) : (
                    mensajes.map((msg) => {
                        const esAdmin = msg.autor_rol === 'admin';
                        const esMio = (
                            msg.autor_id === String(userActual?.id) ||
                            msg.autor_nombre === (userActual?.nombre || userActual?.name)
                        );
                        const fechaStr = esHoy(msg.created_at) ? null : formatFecha(msg.created_at);
                        const mostrarFecha = fechaStr !== ultimaFecha;
                        ultimaFecha = fechaStr;

                        return (
                            <React.Fragment key={msg.id}>
                                {mostrarFecha && fechaStr && (
                                    <div className="comunidad-date-divider">{fechaStr}</div>
                                )}
                                <div className={`comunidad-msg ${esMio ? 'msg-mio' : 'msg-otro'}`}>
                                    {!esMio && (
                                        <div className="msg-avatar">
                                            {esAdmin ? '👑' : maskName(msg.autor_nombre)?.[0]?.toUpperCase() || '?'}
                                        </div>
                                    )}
                                    <div className={`msg-bubble ${esAdmin ? 'bubble-admin' : esMio ? 'bubble-mio' : 'bubble-otro'}`}>
                                        {!esMio && (
                                            <div className="msg-autor">
                                                <span className="msg-nombre">{esAdmin ? msg.autor_nombre : maskName(msg.autor_nombre)}</span>
                                                {esAdmin && <span className="badge-admin">ADMIN</span>}
                                            </div>
                                        )}
                                        <p className="msg-texto">{msg.mensaje}</p>
                                        <span className="msg-hora">{formatHora(msg.created_at)}</span>
                                    </div>
                                </div>
                            </React.Fragment>
                        );
                    })
                )}
                <div ref={bottomRef} />
            </div>

            {/* Input */}
            <form className="comunidad-input-bar" onSubmit={enviar}>
                {error && <div className="comunidad-error">{error}</div>}
                <div className="comunidad-input-row">
                    <input
                        type="text"
                        className="comunidad-input"
                        placeholder="Escribe un mensaje..."
                        value={texto}
                        onChange={(e) => setTexto(e.target.value)}
                        maxLength={1000}
                        disabled={enviando}
                    />
                    <button
                        type="submit"
                        className="comunidad-send-btn"
                        disabled={!texto.trim() || enviando}
                    >
                        {enviando ? '...' : '➤'}
                    </button>
                </div>
            </form>
        </div>
    );
}

export default Comunidad;
