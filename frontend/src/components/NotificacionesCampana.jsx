import React, { useState, useEffect, useRef } from 'react';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const NotificacionesCampana = () => {
    const [notificaciones, setNotificaciones] = useState([]);
    const [abierto, setAbierto] = useState(false);
    const menuRef = useRef(null);

    const fetchNotificaciones = async () => {
        try {
            const token = localStorage.getItem('capital_trade_token');
            if (!token) return;

            const res = await fetch(`${API}/api/notificaciones`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setNotificaciones(data.notificaciones || []);
            }
        } catch (error) {
            console.error("Error obteniendo notificaciones", error);
        }
    };

    useEffect(() => {
        fetchNotificaciones();
        // Auto-refresh cada 60 segundos
        const interval = setInterval(fetchNotificaciones, 60000);
        return () => clearInterval(interval);
    }, []);

    // Cerrar al clickear fuera
    useEffect(() => {
        const handleClickFuera = (event) => {
            if (menuRef.current && !menuRef.current.contains(event.target)) {
                setAbierto(false);
            }
        };
        document.addEventListener("mousedown", handleClickFuera);
        return () => document.removeEventListener("mousedown", handleClickFuera);
    }, []);

    const marcarComoLeida = async (id) => {
        try {
            const token = localStorage.getItem('capital_trade_token');
            await fetch(`${API}/api/notificaciones/${id}/leida`, {
                method: 'PUT',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            setNotificaciones(notificaciones.map(n => n.id === id ? { ...n, leida: true } : n));
        } catch (err) { }
    };

    const marcarTodasLeidas = async () => {
        try {
            const token = localStorage.getItem('capital_trade_token');
            await fetch(`${API}/api/notificaciones/leer-todas`, {
                method: 'PUT',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            setNotificaciones(notificaciones.map(n => ({ ...n, leida: true })));
        } catch (err) { }
    };

    const getIcono = (tipo) => {
        switch (tipo) {
            case 'INGRESO': return '💰';
            case 'RETIRO': return '💳';
            case 'REFERIDO': return '👤';
            default: return '🔔';
        }
    };

    const noLeidas = notificaciones.filter(n => !n.leida).length;

    const esMobile = window.innerWidth <= 768;

    return (
        <div style={{ position: 'relative' }} ref={menuRef}>
            <button
                onClick={() => setAbierto(!abierto)}
                style={{
                    background: 'none', border: 'none', fontSize: '22px',
                    cursor: 'pointer', position: 'relative', padding: '8px',
                    color: '#f8fafc', transition: 'transform 0.2s',
                    transform: abierto ? 'scale(1.1)' : 'scale(1)'
                }}
            >
                <span>🔔</span>
                {noLeidas > 0 && (
                    <span style={{
                        position: 'absolute', top: '0px', right: '0px',
                        backgroundColor: '#ef4444', color: 'white',
                        borderRadius: '50%', width: '18px', height: '18px',
                        fontSize: '11px', display: 'flex', alignItems: 'center',
                        justifyContent: 'center', fontWeight: 'bold',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.3)'
                    }}>
                        {noLeidas > 9 ? '9+' : noLeidas}
                    </span>
                )}
            </button>

            {abierto && (
                <div style={{
                    position: 'absolute', top: '45px', right: esMobile ? '-25px' : '0',
                    width: '90vw', maxWidth: '350px', maxHeight: '75vh', backgroundColor: '#0f172a',
                    border: '1px solid #1e293b', borderRadius: '12px',
                    boxShadow: '0 10px 40px rgba(0,0,0,0.6)', zIndex: 999,
                    display: 'flex', flexDirection: 'column', overflow: 'hidden'
                }}>
                    <div style={{
                        padding: '12px 16px', borderBottom: '1px solid #1e293b',
                        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                        backgroundColor: 'rgba(30, 41, 59, 0.5)'
                    }}>
                        <h4 style={{ margin: 0, color: '#f8fafc', fontSize: '15px' }}>Notificaciones</h4>
                        {noLeidas > 0 && (
                            <button
                                onClick={marcarTodasLeidas}
                                style={{
                                    background: 'none', border: 'none', color: '#3b82f6',
                                    fontSize: '12px', cursor: 'pointer', fontWeight: 'bold', padding: 0
                                }}
                            >
                                Marcar leídas
                            </button>
                        )}
                    </div>

                    <div style={{ overflowY: 'auto', flex: 1, maxHeight: '330px' }}>
                        {notificaciones.length === 0 ? (
                            <div style={{ padding: '2rem 1rem', textAlign: 'center', color: '#64748b' }}>
                                <div style={{ fontSize: '30px', marginBottom: '10px' }}>📭</div>
                                No tienes notificaciones
                            </div>
                        ) : (
                            notificaciones.map((notif) => (
                                <div
                                    key={notif.id}
                                    onClick={() => !notif.leida && marcarComoLeida(notif.id)}
                                    style={{
                                        padding: '12px 16px',
                                        borderBottom: '1px solid #1e293b',
                                        backgroundColor: notif.leida ? 'transparent' : 'rgba(59, 130, 246, 0.1)',
                                        display: 'flex', gap: '12px', alignItems: 'flex-start',
                                        cursor: notif.leida ? 'default' : 'pointer',
                                        transition: 'background-color 0.2s'
                                    }}
                                >
                                    <div style={{ fontSize: '20px', padding: '4px', backgroundColor: 'rgba(30, 41, 59, 0.4)', borderRadius: '50%' }}>
                                        {getIcono(notif.tipo)}
                                    </div>
                                    <div>
                                        <p style={{
                                            margin: '0 0 4px 0', fontSize: '13px',
                                            color: notif.leida ? '#94a3b8' : '#f8fafc',
                                            fontWeight: notif.leida ? 'normal' : '500',
                                            lineHeight: '1.4'
                                        }}>
                                            {notif.mensaje}
                                        </p>
                                        <span style={{ fontSize: '10px', color: '#64748b' }}>
                                            {new Date(notif.created_at).toLocaleString('es-ES', { dateStyle: 'short', timeStyle: 'short' })}
                                        </span>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default NotificacionesCampana;
