import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import './DashboardAdminExpandido.css';

const DashboardAgente = () => {
  const { agenteId } = useParams();
  const navigate = useNavigate();
  
  const [activeTab, setActiveTab] = useState('inicio');
  const [perfil, setPerfil] = useState(null);
  const [estadisticas, setEstadisticas] = useState(null);
  const [referidos, setReferidos] = useState([]);
  const [retiros, setRetiros] = useState([]);
  const [mensajes, setMensajes] = useState([]);
  const [noLeidos, setNoLeidos] = useState(0);
  const [mensaje, setMensaje] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [copiado, setCopiado] = useState(false);
  const [mostrarGuia, setMostrarGuia] = useState(false);
  const [mostrarFormRetiro, setMostrarFormRetiro] = useState(false);
  const [montoRetiro, setMontoRetiro] = useState('');
  const [notasRetiro, setNotasRetiro] = useState('');

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    cargarDatos();
    cargarNoLeidos();
    const interval = setInterval(cargarNoLeidos, 10000);
    return () => clearInterval(interval);
  }, [agenteId, activeTab]);

  const cargarDatos = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const perfilRes = await axios.get(`${apiUrl}/api/agentes/perfil`, { headers });
      setPerfil(perfilRes.data);

      if (activeTab === 'inicio') {
        const statsRes = await axios.get(`${apiUrl}/api/agentes/estadisticas`, { headers });
        setEstadisticas(statsRes.data);
      } else if (activeTab === 'referidos') {
        const refRes = await axios.get(`${apiUrl}/api/agentes/referidos`, { headers });
        setReferidos(refRes.data);
      } else if (activeTab === 'retiros') {
        const retirosRes = await axios.get(`${apiUrl}/api/agentes/retiros`, { headers });
        setRetiros(retirosRes.data);
      } else if (activeTab === 'mensajes') {
        const mensajesRes = await axios.get(`${apiUrl}/api/agentes/mensajes`, { headers });
        setMensajes(mensajesRes.data);
        cargarNoLeidos();
      } else if (activeTab === 'estadisticas') {
        const statsRes = await axios.get(`${apiUrl}/api/agentes/estadisticas`, { headers });
        setEstadisticas(statsRes.data);
      }

      setLoading(false);
    } catch (err) {
      console.error('Error cargando datos:', err);
      setError(err.response?.data?.detail || 'Error al cargar datos');
      if (err.response?.status === 401) {
        navigate('/agente/login');
      }
      setLoading(false);
    }
  };

  const copiarLinkReferido = () => {
    if (!perfil?.codigo_referido) {
      alert('⚠️ Espera a que cargue tu código de referido');
      return;
    }
    
    const link = `https://fortunariocash.com/registro?ref=${perfil.codigo_referido}`;
    const tempInput = document.createElement('input');
    tempInput.value = link;
    document.body.appendChild(tempInput);
    tempInput.select();
    tempInput.setSelectionRange(0, 99999);
    
    try {
      const successful = document.execCommand('copy');
      if (successful) {
        setCopiado(true);
        setTimeout(() => setCopiado(false), 3000);
        alert('✅ Enlace copiado: ' + link);
      } else {
        alert('📋 Copia este enlace manualmente:\n\n' + link);
      }
    } catch (err) {
      alert('📋 Copia este enlace manualmente:\n\n' + link);
    }
    
    document.body.removeChild(tempInput);
  };

  const compartirLink = () => {
    if (!perfil?.codigo_referido) {
      alert('⚠️ Espera a que cargue tu código de referido');
      return;
    }
    
    const link = `https://fortunariocash.com/registro?ref=${perfil.codigo_referido}`;
    const mensaje = `¡Hola! 👋

¿Quieres estudiar en el extranjero? 🎓✈️

Te invito a registrarte en Fortunario Cash, donde te ayudamos con todo el proceso de visa de estudiante para España.

🔗 Regístrate con mi enlace: ${link}

¡Cumple tu sueño de estudiar en Europa! 🇪🇸`;

    const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(mensaje)}`;
    window.open(whatsappUrl, '_blank');
  };

  const solicitarRetiro = async () => {
    if (!montoRetiro || parseFloat(montoRetiro) <= 0) {
      alert('❌ Ingresa un monto válido');
      return;
    }

    const monto = parseFloat(montoRetiro);
    if (monto > perfil.credito_disponible) {
      alert(`❌ No tienes suficiente crédito disponible. Disponible: ${perfil.credito_disponible.toFixed(2)}€`);
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `${apiUrl}/api/agentes/solicitar-retiro`,
        { monto, notas: notasRetiro },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      alert('✅ Solicitud de retiro enviada al administrador');
      setMostrarFormRetiro(false);
      setMontoRetiro('');
      setNotasRetiro('');
      cargarDatos();
    } catch (err) {
      alert('❌ Error: ' + (err.response?.data?.detail || err.message));
    }
  };

  const cargarNoLeidos = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${apiUrl}/api/agentes/mensajes/no-leidos`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setNoLeidos(response.data.no_leidos || 0);
    } catch (error) {
      console.error('Error cargando no leídos:', error);
    }
  };

  const enviarMensaje = async (e) => {
    e.preventDefault();
    if (!mensaje.trim()) return;

    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `${apiUrl}/api/agentes/enviar-mensaje`,
        { mensaje: mensaje.trim() },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      setMensaje('');
      cargarDatos();
    } catch (error) {
      console.error('Error enviando mensaje:', error);
      alert('Error enviando mensaje');
    }
  };

  const formatearFecha = (fecha) => {
    if (!fecha) return '';
    const d = new Date(fecha);
    const hoy = new Date();
    const esHoy = d.toDateString() === hoy.toDateString();
    
    if (esHoy) {
      return d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    }
    return d.toLocaleString('es-ES', { 
      day: '2-digit', 
      month: 'short', 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const cerrarSesion = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('agente_id');
    localStorage.removeItem('agente_nombre');
    localStorage.removeItem('tipo_usuario');
    navigate('/agente/login');
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Cargando...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <div className="header-content">
          <div>
            <h1>🎯 Panel de Agente</h1>
            <p>Bienvenido, {perfil?.nombre}</p>
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button 
              onClick={() => setMostrarGuia(true)} 
              style={{
                backgroundColor: '#3b82f6',
                color: 'white',
                padding: '10px 20px',
                borderRadius: '8px',
                border: 'none',
                cursor: 'pointer',
                fontWeight: '600',
                fontSize: '14px'
              }}
            >
              📖 Guía
            </button>
            <button onClick={cerrarSesion} className="btn-logout">
              🚪 Salir
            </button>
          </div>
        </div>
      </div>

      {/* TABS GRANDES CON COLORES */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
        gap: '15px', 
        padding: '20px',
        maxWidth: '1400px',
        margin: '0 auto'
      }}>
        <button
          onClick={() => setActiveTab('inicio')}
          style={{
            padding: '25px 20px',
            fontSize: '17px',
            fontWeight: '700',
            borderRadius: '15px',
            border: 'none',
            cursor: 'pointer',
            background: activeTab === 'inicio' 
              ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
              : '#f3f4f6',
            color: activeTab === 'inicio' ? 'white' : '#374151',
            boxShadow: activeTab === 'inicio' ? '0 6px 20px rgba(102, 126, 234, 0.5)' : 'none',
            transform: activeTab === 'inicio' ? 'translateY(-3px) scale(1.02)' : 'none',
            transition: 'all 0.3s ease'
          }}
        >
          🏠 Inicio
        </button>
        
        <button
          onClick={() => setActiveTab('referidos')}
          style={{
            padding: '25px 20px',
            fontSize: '17px',
            fontWeight: '700',
            borderRadius: '15px',
            border: 'none',
            cursor: 'pointer',
            background: activeTab === 'referidos' 
              ? 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
              : '#f3f4f6',
            color: activeTab === 'referidos' ? 'white' : '#374151',
            boxShadow: activeTab === 'referidos' ? '0 6px 20px rgba(240, 147, 251, 0.5)' : 'none',
            transform: activeTab === 'referidos' ? 'translateY(-3px) scale(1.02)' : 'none',
            transition: 'all 0.3s ease'
          }}
        >
          👥 Referidos<br/><span style={{fontSize: '14px'}}>({perfil?.total_referidos || 0})</span>
        </button>
        
        <button
          onClick={() => setActiveTab('retiros')}
          style={{
            padding: '25px 20px',
            fontSize: '17px',
            fontWeight: '700',
            borderRadius: '15px',
            border: 'none',
            cursor: 'pointer',
            background: activeTab === 'retiros' 
              ? 'linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%)'
              : '#f3f4f6',
            color: activeTab === 'retiros' ? 'white' : '#374151',
            boxShadow: activeTab === 'retiros' ? '0 6px 20px rgba(251, 194, 235, 0.5)' : 'none',
            transform: activeTab === 'retiros' ? 'translateY(-3px) scale(1.02)' : 'none',
            transition: 'all 0.3s ease'
          }}
        >
          💰 Retiros
        </button>
        
        <button
          onClick={() => setActiveTab('mensajes')}
          style={{
            padding: '25px 20px',
            fontSize: '17px',
            fontWeight: '700',
            borderRadius: '15px',
            border: 'none',
            cursor: 'pointer',
            background: activeTab === 'mensajes' 
              ? 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
              : '#f3f4f6',
            color: activeTab === 'mensajes' ? 'white' : '#374151',
            boxShadow: activeTab === 'mensajes' ? '0 6px 20px rgba(79, 172, 254, 0.5)' : 'none',
            transform: activeTab === 'mensajes' ? 'translateY(-3px) scale(1.02)' : 'none',
            transition: 'all 0.3s ease',
            position: 'relative'
          }}
        >
          💬 Mensajes
          {noLeidos > 0 && (
            <span style={{
              position: 'absolute',
              top: '8px',
              right: '8px',
              backgroundColor: '#ef4444',
              color: 'white',
              borderRadius: '50%',
              width: '26px',
              height: '26px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '13px',
              fontWeight: '700',
              boxShadow: '0 2px 8px rgba(0,0,0,0.3)'
            }}>
              {noLeidos}
            </span>
          )}
        </button>
        
        <button
          onClick={() => setActiveTab('estadisticas')}
          style={{
            padding: '25px 20px',
            fontSize: '17px',
            fontWeight: '700',
            borderRadius: '15px',
            border: 'none',
            cursor: 'pointer',
            background: activeTab === 'estadisticas' 
              ? 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
              : '#f3f4f6',
            color: activeTab === 'estadisticas' ? 'white' : '#374151',
            boxShadow: activeTab === 'estadisticas' ? '0 6px 20px rgba(67, 233, 123, 0.5)' : 'none',
            transform: activeTab === 'estadisticas' ? 'translateY(-3px) scale(1.02)' : 'none',
            transition: 'all 0.3s ease'
          }}
        >
          📈 Estadísticas
        </button>
      </div>

      {/* CONTENIDO */}
      <div className="dashboard-content">
        {/* TAB: INICIO */}
        {activeTab === 'inicio' && (
          <div className="tab-content">
            {/* Código de Referido compacto */}
            <div style={{ 
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              padding: '20px',
              borderRadius: '15px',
              marginBottom: '25px',
              color: 'white',
              boxShadow: '0 8px 25px rgba(102, 126, 234, 0.4)'
            }}>
              <h3 style={{ margin: '0 0 15px 0', fontSize: '18px' }}>🔗 Tu Código de Referido</h3>
              <div style={{
                backgroundColor: 'rgba(255,255,255,0.25)',
                padding: '20px',
                borderRadius: '12px',
                textAlign: 'center',
                marginBottom: '15px'
              }}>
                <div style={{
                  fontSize: '36px',
                  fontWeight: '700',
                  letterSpacing: '4px',
                  fontFamily: 'monospace'
                }}>
                  {perfil?.codigo_referido}
                </div>
              </div>
              
              <div style={{
                backgroundColor: 'rgba(255,255,255,0.15)',
                padding: '15px',
                borderRadius: '10px',
                fontSize: '13px'
              }}>
                <div style={{ marginBottom: '10px', opacity: 0.95, fontWeight: '600' }}>📋 Enlace completo:</div>
                <div style={{
                  display: 'flex',
                  gap: '10px',
                  backgroundColor: 'rgba(255,255,255,0.25)',
                  padding: '12px',
                  borderRadius: '8px',
                  alignItems: 'center'
                }}>
                  <input
                    type="text"
                    readOnly
                    value={`https://fortunariocash.com/registro?ref=${perfil?.codigo_referido || ''}`}
                    style={{
                      flex: 1,
                      background: 'transparent',
                      border: 'none',
                      color: 'white',
                      fontSize: '12px',
                      outline: 'none'
                    }}
                  />
                  <button
                    onClick={copiarLinkReferido}
                    style={{
                      padding: '10px 16px',
                      backgroundColor: 'rgba(255,255,255,0.35)',
                      border: 'none',
                      borderRadius: '8px',
                      color: 'white',
                      fontWeight: '700',
                      cursor: 'pointer',
                      fontSize: '12px'
                    }}
                  >
                    {copiado ? '✅ Copiado' : '📋 Copiar'}
                  </button>
                  <button
                    onClick={compartirLink}
                    style={{
                      padding: '10px 16px',
                      backgroundColor: '#25D366',
                      border: 'none',
                      borderRadius: '8px',
                      color: 'white',
                      fontWeight: '700',
                      cursor: 'pointer',
                      fontSize: '12px'
                    }}
                  >
                    📱 WhatsApp
                  </button>
                </div>
              </div>
            </div>

            {/* Tarjetas de resumen */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '20px' }}>
              <div style={{
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                padding: '30px 25px',
                borderRadius: '15px',
                color: 'white',
                boxShadow: '0 6px 20px rgba(240, 147, 251, 0.4)'
              }}>
                <div style={{ fontSize: '15px', opacity: 0.9, marginBottom: '10px' }}>👥 Total Referidos</div>
                <div style={{ fontSize: '48px', fontWeight: '700', lineHeight: '1' }}>{perfil?.total_referidos || 0}</div>
              </div>

              <div style={{
                background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
                padding: '30px 25px',
                borderRadius: '15px',
                color: 'white',
                boxShadow: '0 6px 20px rgba(67, 233, 123, 0.4)'
              }}>
                <div style={{ fontSize: '15px', opacity: 0.9, marginBottom: '10px' }}>💰 Crédito Disponible</div>
                <div style={{ fontSize: '48px', fontWeight: '700', lineHeight: '1' }}>{perfil?.credito_disponible?.toFixed(2) || '0.00'}€</div>
              </div>

              <div style={{
                background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                padding: '30px 25px',
                borderRadius: '15px',
                color: 'white',
                boxShadow: '0 6px 20px rgba(79, 172, 254, 0.4)'
              }}>
                <div style={{ fontSize: '15px', opacity: 0.9, marginBottom: '10px' }}>💎 Comisión Total</div>
                <div style={{ fontSize: '48px', fontWeight: '700', lineHeight: '1' }}>{perfil?.comision_total?.toFixed(2) || '0.00'}€</div>
              </div>

              <div style={{
                background: 'linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%)',
                padding: '30px 25px',
                borderRadius: '15px',
                color: 'white',
                boxShadow: '0 6px 20px rgba(251, 194, 235, 0.4)'
              }}>
                <div style={{ fontSize: '15px', opacity: 0.9, marginBottom: '10px' }}>🏦 Crédito Retirado</div>
                <div style={{ fontSize: '48px', fontWeight: '700', lineHeight: '1' }}>{perfil?.credito_retirado?.toFixed(2) || '0.00'}€</div>
              </div>
            </div>
          </div>
        )}

        {/* TAB: REFERIDOS */}
        {activeTab === 'referidos' && (
          <div className="tab-content">
            <div className="card">
              <h2>👥 Mis Estudiantes Referidos</h2>
              {referidos.length === 0 ? (
                <div className="no-data">
                  <p>Aún no has referido ningún estudiante</p>
                </div>
              ) : (
                <div className="tabla-wrapper">
                  <table className="tabla-estudiantes">
                    <thead>
                      <tr>
                        <th>Estudiante</th>
                        <th>Email</th>
                        <th>Estado</th>
                        <th>Presupuesto</th>
                        <th>Comisión</th>
                        <th>Fecha Registro</th>
                      </tr>
                    </thead>
                    <tbody>
                      {referidos.map((referido) => (
                        <tr key={referido.id}>
                          <td style={{ fontWeight: '600' }}>{referido.nombre}</td>
                          <td>{referido.email}</td>
                          <td>
                            <span className={`badge badge-${referido.estado}`}>
                              {referido.estado === 'aprobado' && '✅ Aprobado'}
                              {referido.estado === 'pendiente' && '⏳ Pendiente'}
                              {referido.estado === 'rechazado' && '❌ Rechazado'}
                            </span>
                          </td>
                          <td style={{ fontWeight: '700', color: '#3b82f6' }}>
                            {referido.presupuesto ? `${referido.presupuesto.toFixed(2)}€` : '-'}
                          </td>
                          <td style={{ fontWeight: '700', color: '#10b981' }}>
                            {referido.comision ? `${referido.comision.toFixed(2)}€` : '-'}
                          </td>
                          <td>{new Date(referido.fecha_registro).toLocaleDateString('es-ES')}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB: RETIROS */}
        {activeTab === 'retiros' && (
          <div className="tab-content">
            <div className="card" style={{ marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>💰 Solicitar Retiro</h2>
                <div style={{ fontSize: '20px', fontWeight: '700', color: '#10b981' }}>
                  Disponible: {perfil?.credito_disponible?.toFixed(2) || '0.00'}€
                </div>
              </div>

              {!mostrarFormRetiro ? (
                <button
                  onClick={() => setMostrarFormRetiro(true)}
                  style={{
                    width: '100%',
                    padding: '18px',
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '12px',
                    fontSize: '17px',
                    fontWeight: '700',
                    cursor: 'pointer',
                    boxShadow: '0 4px 15px rgba(16, 185, 129, 0.3)'
                  }}
                >
                  ➕ Nueva Solicitud de Retiro
                </button>
              ) : (
                <div style={{ backgroundColor: '#f9fafb', padding: '25px', borderRadius: '12px', border: '1px solid #e5e7eb' }}>
                  <div style={{ marginBottom: '20px' }}>
                    <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', fontSize: '15px' }}>Monto a retirar (€)</label>
                    <input
                      type="number"
                      step="0.01"
                      value={montoRetiro}
                      onChange={(e) => setMontoRetiro(e.target.value)}
                      placeholder="0.00"
                      style={{
                        width: '100%',
                        padding: '12px 15px',
                        borderRadius: '8px',
                        border: '2px solid #d1d5db',
                        fontSize: '17px'
                      }}
                    />
                  </div>

                  <div style={{ marginBottom: '20px' }}>
                    <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', fontSize: '15px' }}>Notas (opcional)</label>
                    <textarea
                      value={notasRetiro}
                      onChange={(e) => setNotasRetiro(e.target.value)}
                      placeholder="Ej: Número de cuenta, PayPal, etc."
                      rows="3"
                      style={{
                        width: '100%',
                        padding: '12px 15px',
                        borderRadius: '8px',
                        border: '2px solid #d1d5db',
                        fontSize: '15px'
                      }}
                    />
                  </div>

                  <div style={{ display: 'flex', gap: '12px' }}>
                    <button
                      onClick={solicitarRetiro}
                      style={{
                        flex: 1,
                        padding: '14px',
                        background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '10px',
                        fontSize: '16px',
                        fontWeight: '700',
                        cursor: 'pointer'
                      }}
                    >
                      ✅ Enviar Solicitud
                    </button>
                    <button
                      onClick={() => {
                        setMostrarFormRetiro(false);
                        setMontoRetiro('');
                        setNotasRetiro('');
                      }}
                      style={{
                        padding: '14px 25px',
                        backgroundColor: '#6b7280',
                        color: 'white',
                        border: 'none',
                        borderRadius: '10px',
                        fontSize: '16px',
                        fontWeight: '600',
                        cursor: 'pointer'
                      }}
                    >
                      ❌ Cancelar
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div className="card">
              <h3>📋 Historial de Retiros</h3>
              
              {retiros.length === 0 ? (
                <div className="no-data">
                  <p>No has solicitado ningún retiro aún</p>
                </div>
              ) : (
                <div className="tabla-responsive">
                  <table>
                    <thead>
                      <tr>
                        <th>Fecha</th>
                        <th>Monto</th>
                        <th>Estado</th>
                        <th>Notas</th>
                        <th>Respuesta Admin</th>
                      </tr>
                    </thead>
                    <tbody>
                      {retiros.map((retiro) => (
                        <tr key={retiro.id}>
                          <td>{new Date(retiro.fecha_solicitud).toLocaleDateString('es-ES')}</td>
                          <td style={{ fontWeight: 'bold', color: '#10b981' }}>{retiro.monto.toFixed(2)}€</td>
                          <td>
                            <span className={`badge badge-${retiro.estado}`}>
                              {retiro.estado === 'pendiente' && '⏳ Pendiente'}
                              {retiro.estado === 'aprobado' && '✅ Aprobado'}
                              {retiro.estado === 'rechazado' && '❌ Rechazado'}
                            </span>
                          </td>
                          <td>{retiro.notas_agente || '-'}</td>
                          <td>{retiro.comentarios_admin || '-'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB: MENSAJES */}
        {activeTab === 'mensajes' && (
          <div className="tab-content">
            <div className="card">
              <h2>💬 Mensajes con Administrador</h2>
              
              <div style={{ 
                border: '2px solid #e5e7eb', 
                borderRadius: '15px', 
                overflow: 'hidden',
                marginTop: '20px'
              }}>
                <div style={{ 
                  height: '450px', 
                  overflowY: 'auto', 
                  padding: '25px',
                  backgroundColor: '#f9fafb'
                }}>
                  {mensajes.length === 0 ? (
                    <div style={{ textAlign: 'center', color: '#6b7280', padding: '60px 20px' }}>
                      <div style={{ fontSize: '48px', marginBottom: '15px' }}>💬</div>
                      <p style={{ fontSize: '16px' }}>No hay mensajes aún. Inicia la conversación 👇</p>
                    </div>
                  ) : (
                    mensajes.map(msg => (
                      <div
                        key={msg.id}
                        style={{
                          marginBottom: '18px',
                          display: 'flex',
                          justifyContent: msg.remitente === 'agente' ? 'flex-end' : 'flex-start'
                        }}
                      >
                        <div style={{
                          maxWidth: '70%',
                          padding: '14px 18px',
                          borderRadius: '15px',
                          backgroundColor: msg.remitente === 'agente' ? '#3b82f6' : '#e5e7eb',
                          color: msg.remitente === 'agente' ? 'white' : '#1f2937',
                          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                        }}>
                          <div style={{ fontSize: '15px', lineHeight: '1.5' }}>{msg.mensaje}</div>
                          <div style={{ 
                            fontSize: '11px', 
                            marginTop: '6px',
                            opacity: 0.7
                          }}>
                            {formatearFecha(msg.fecha)}
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>

                <form 
                  onSubmit={enviarMensaje}
                  style={{ 
                    display: 'flex', 
                    gap: '12px', 
                    padding: '20px',
                    backgroundColor: 'white',
                    borderTop: '2px solid #e5e7eb'
                  }}
                >
                  <input
                    type="text"
                    value={mensaje}
                    onChange={(e) => setMensaje(e.target.value)}
                    placeholder="Escribe un mensaje..."
                    style={{
                      flex: 1,
                      padding: '12px 18px',
                      border: '2px solid #d1d5db',
                      borderRadius: '10px',
                      fontSize: '15px'
                    }}
                  />
                  <button
                    type="submit"
                    style={{
                      padding: '12px 24px',
                      background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                      color: 'white',
                      border: 'none',
                      borderRadius: '10px',
                      cursor: 'pointer',
                      fontSize: '15px',
                      fontWeight: '700',
                      boxShadow: '0 4px 12px rgba(59, 130, 246, 0.3)'
                    }}
                  >
                    📤 Enviar
                  </button>
                </form>
              </div>
            </div>
          </div>
        )}

        {/* TAB: ESTADÍSTICAS */}
        {activeTab === 'estadisticas' && (
          <div className="tab-content">
            <div className="card">
              <h2>📈 Estadísticas Detalladas</h2>
              
              {estadisticas && (
                <div>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px', marginBottom: '30px' }}>
                    <div style={{ padding: '25px', backgroundColor: '#dbeafe', borderRadius: '15px', boxShadow: '0 4px 12px rgba(59, 130, 246, 0.15)' }}>
                      <div style={{ fontSize: '14px', color: '#1e40af', marginBottom: '8px', fontWeight: '600' }}>Referidos Aprobados</div>
                      <div style={{ fontSize: '42px', fontWeight: '700', color: '#1e40af' }}>
                        {estadisticas.referidos_aprobados || 0}
                      </div>
                    </div>

                    <div style={{ padding: '25px', backgroundColor: '#fef3c7', borderRadius: '15px', boxShadow: '0 4px 12px rgba(245, 158, 11, 0.15)' }}>
                      <div style={{ fontSize: '14px', color: '#92400e', marginBottom: '8px', fontWeight: '600' }}>Referidos Pendientes</div>
                      <div style={{ fontSize: '42px', fontWeight: '700', color: '#92400e' }}>
                        {estadisticas.referidos_pendientes || 0}
                      </div>
                    </div>

                    <div style={{ padding: '25px', backgroundColor: '#d1fae5', borderRadius: '15px', boxShadow: '0 4px 12px rgba(16, 185, 129, 0.15)' }}>
                      <div style={{ fontSize: '14px', color: '#065f46', marginBottom: '8px', fontWeight: '600' }}>Presupuestos Aceptados</div>
                      <div style={{ fontSize: '42px', fontWeight: '700', color: '#065f46' }}>
                        {estadisticas.presupuestos_aceptados || 0}
                      </div>
                    </div>

                    <div style={{ padding: '25px', backgroundColor: '#fce7f3', borderRadius: '15px', boxShadow: '0 4px 12px rgba(236, 72, 153, 0.15)' }}>
                      <div style={{ fontSize: '14px', color: '#9f1239', marginBottom: '8px', fontWeight: '600' }}>Presupuestos Generados</div>
                      <div style={{ fontSize: '42px', fontWeight: '700', color: '#9f1239' }}>
                        {estadisticas.presupuestos_generados || 0}
                      </div>
                    </div>
                  </div>

                  <div style={{
                    padding: '30px',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    borderRadius: '15px',
                    color: 'white',
                    boxShadow: '0 8px 25px rgba(102, 126, 234, 0.4)'
                  }}>
                    <h3 style={{ marginTop: 0, fontSize: '22px' }}>💰 Resumen Financiero</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '25px' }}>
                      <div>
                        <div style={{ fontSize: '15px', opacity: 0.9, marginBottom: '8px' }}>Valor Total</div>
                        <div style={{ fontSize: '32px', fontWeight: '700' }}>
                          {(estadisticas.valor_total_presupuestos || 0).toFixed(2)}€
                        </div>
                      </div>
                      <div>
                        <div style={{ fontSize: '15px', opacity: 0.9, marginBottom: '8px' }}>Comisión Total</div>
                        <div style={{ fontSize: '32px', fontWeight: '700' }}>
                          {(estadisticas.comision_total || 0).toFixed(2)}€
                        </div>
                      </div>
                      <div>
                        <div style={{ fontSize: '15px', opacity: 0.9, marginBottom: '8px' }}>Disponible</div>
                        <div style={{ fontSize: '32px', fontWeight: '700' }}>
                          {(perfil?.credito_disponible || 0).toFixed(2)}€
                        </div>
                      </div>
                      <div>
                        <div style={{ fontSize: '15px', opacity: 0.9, marginBottom: '8px' }}>Retirado</div>
                        <div style={{ fontSize: '32px', fontWeight: '700' }}>
                          {(perfil?.credito_retirado || 0).toFixed(2)}€
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* MODAL GUÍA */}
      {mostrarGuia && (
        <div className="modal-overlay" onClick={() => setMostrarGuia(false)}>
          <div className="modal-content-large" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '800px', maxHeight: '90vh', overflowY: 'auto' }}>
            <div className="modal-header">
              <h2>📖 Guía del Agente</h2>
              <button className="modal-close" onClick={() => setMostrarGuia(false)}>✕</button>
            </div>

            <div style={{ padding: '25px' }}>
              <div style={{ marginBottom: '25px', padding: '20px', backgroundColor: '#eff6ff', borderRadius: '12px', border: '2px solid #3b82f6' }}>
                <h3 style={{ color: '#1e40af', marginTop: 0 }}>🎯 1. Tu Rol como Agente</h3>
                <p style={{ color: '#374151', lineHeight: '1.6', margin: 0 }}>
                  Como agente de <strong>Fortunario Cash</strong>, tu objetivo es <strong>referir estudiantes</strong> que quieran estudiar en España. 
                  Por cada estudiante que se registre usando tu código y complete su proceso, <strong>ganas una comisión del 10%</strong>.
                </p>
              </div>

              <div style={{ marginBottom: '25px', padding: '20px', backgroundColor: '#f0fdf4', borderRadius: '12px', border: '2px solid #10b981' }}>
                <h3 style={{ color: '#065f46', marginTop: 0 }}>🔗 2. Cómo Compartir tu Código</h3>
                <p style={{ color: '#374151', lineHeight: '1.6' }}>
                  Usa el botón "Copiar" o "WhatsApp" para compartir tu enlace de referido con estudiantes interesados.
                </p>
              </div>

              <div style={{ marginBottom: '25px', padding: '20px', backgroundColor: '#fefce8', borderRadius: '12px', border: '2px solid #eab308' }}>
                <h3 style={{ color: '#854d0e', marginTop: 0 }}>💰 3. Sistema de Comisiones (10%)</h3>
                <p style={{ color: '#374151', lineHeight: '1.6' }}>
                  Ganas el <strong>10% de comisión</strong> sobre todos los pagos que realicen tus estudiantes referidos.
                </p>
              </div>

              <div style={{ textAlign: 'center', paddingTop: '20px', borderTop: '2px solid #e5e7eb' }}>
                <button 
                  onClick={() => setMostrarGuia(false)}
                  style={{
                    background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                    color: 'white',
                    padding: '14px 32px',
                    borderRadius: '10px',
                    border: 'none',
                    cursor: 'pointer',
                    fontSize: '16px',
                    fontWeight: '700',
                    boxShadow: '0 4px 15px rgba(59, 130, 246, 0.3)'
                  }}
                >
                  ✅ Entendido
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardAgente;
