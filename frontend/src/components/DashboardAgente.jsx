import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import './DashboardAdminExpandido.css'; // Reutilizamos estilos del admin

const DashboardAgente = () => {
  const { agenteId } = useParams();
  const navigate = useNavigate();
  
  const [activeTab, setActiveTab] = useState('inicio');
  const [perfil, setPerfil] = useState(null);
  const [estadisticas, setEstadisticas] = useState(null);
  const [referidos, setReferidos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [copiado, setCopiado] = useState(false);
  const [mostrarGuia, setMostrarGuia] = useState(false);

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    cargarDatos();
  }, [agenteId, activeTab]);

  const cargarDatos = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      // Cargar perfil siempre
      const perfilRes = await axios.get(`${apiUrl}/api/agentes/perfil`, { headers });
      setPerfil(perfilRes.data);

      if (activeTab === 'inicio') {
        const statsRes = await axios.get(`${apiUrl}/api/agentes/estadisticas`, { headers });
        setEstadisticas(statsRes.data);
      } else if (activeTab === 'referidos') {
        const refRes = await axios.get(`${apiUrl}/api/agentes/referidos`, { headers });
        setReferidos(refRes.data);
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
    const link = `${window.location.origin}/registro?ref=${perfil.codigo_referido}`;
    navigator.clipboard.writeText(link);
    setCopiado(true);
    setTimeout(() => setCopiado(false), 3000);
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
      {/* HEADER */}
      <div className="dashboard-header">
        <div className="header-content">
          <div>
            <h1>🎯 Panel de Agente</h1>
            <p>Bienvenido, {perfil?.nombre}</p>
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button 
              onClick={() => setMostrarGuia(true)} 
              className="btn-guia"
              style={{
                backgroundColor: '#3b82f6',
                color: 'white',
                padding: '10px 20px',
                borderRadius: '8px',
                border: 'none',
                cursor: 'pointer',
                fontWeight: '600',
                fontSize: '14px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              📖 Guía del Agente
            </button>
            <button onClick={cerrarSesion} className="btn-logout">
              🚪 Cerrar Sesión
            </button>
          </div>
        </div>
      </div>

      {/* TABS */}
      <div className="dashboard-tabs">
        <button
          className={`tab ${activeTab === 'inicio' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('inicio')}
        >
          🏠 Inicio
        </button>
        <button
          className={`tab ${activeTab === 'referidos' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('referidos')}
        >
          👥 Mis Referidos ({perfil?.total_referidos || 0})
        </button>
        <button
          className={`tab ${activeTab === 'estadisticas' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('estadisticas')}
        >
          📈 Estadísticas
        </button>
      </div>

      {/* CONTENIDO */}
      <div className="dashboard-content">
        {/* TAB: INICIO */}
        {activeTab === 'inicio' && (
          <div className="tab-content">
            {/* Código de Referido */}
            <div className="card highlight-card">
              <h2>🔗 Tu Código de Referido</h2>
              <div className="codigo-referido-display">
                <div className="codigo-box">
                  {perfil?.codigo_referido}
                </div>
              </div>
              
              {/* Link completo para copiar */}
              <div style={{ 
                marginTop: '15px', 
                padding: '15px', 
                backgroundColor: '#f3f4f6', 
                borderRadius: '8px',
                border: '1px solid #d1d5db'
              }}>
                <p style={{ margin: '0 0 10px 0', fontSize: '14px', color: '#6b7280', fontWeight: '600' }}>
                  🔗 Tu enlace de referido:
                </p>
                <div style={{ 
                  display: 'flex', 
                  gap: '10px', 
                  alignItems: 'center',
                  backgroundColor: 'white',
                  padding: '10px',
                  borderRadius: '6px',
                  border: '1px solid #e5e7eb'
                }}>
                  <input 
                    type="text" 
                    readOnly 
                    value={`${window.location.origin}/registro?ref=${perfil?.codigo_referido || ''}`}
                    style={{
                      flex: 1,
                      border: 'none',
                      outline: 'none',
                      fontSize: '14px',
                      color: '#1f2937',
                      fontFamily: 'monospace',
                      backgroundColor: 'transparent'
                    }}
                    onClick={(e) => e.target.select()}
                  />
                  <button onClick={copiarLinkReferido} className="btn-copiar" style={{
                    padding: '8px 16px',
                    fontSize: '14px',
                    whiteSpace: 'nowrap'
                  }}>
                    {copiado ? '✅ ¡Copiado!' : '📋 Copiar'}
                  </button>
                </div>
              </div>

              <p className="codigo-info">
                📱 Comparte este enlace con estudiantes interesados. 
                <br/>
                💰 Ganas <strong>10%</strong> de comisión por cada presupuesto aceptado.
              </p>
            </div>

            {/* Métricas */}
            <div className="metricas-grid">
              <div className="metrica-card">
                <div className="metrica-icono">👥</div>
                <div className="metrica-info">
                  <div className="metrica-valor">{estadisticas?.total_referidos || 0}</div>
                  <div className="metrica-label">Total Referidos</div>
                </div>
              </div>

              <div className="metrica-card">
                <div className="metrica-icono">✅</div>
                <div className="metrica-info">
                  <div className="metrica-valor">{estadisticas?.referidos_activos || 0}</div>
                  <div className="metrica-label">Referidos Activos</div>
                </div>
              </div>

              <div className="metrica-card">
                <div className="metrica-icono">💰</div>
                <div className="metrica-info">
                  <div className="metrica-valor">{estadisticas?.comision_total?.toFixed(2) || '0.00'}€</div>
                  <div className="metrica-label">Comisión Total</div>
                </div>
              </div>

              <div className="metrica-card">
                <div className="metrica-icono">📊</div>
                <div className="metrica-info">
                  <div className="metrica-valor">{estadisticas?.presupuestos_aceptados || 0}</div>
                  <div className="metrica-label">Presupuestos Aceptados</div>
                </div>
              </div>
            </div>

            {/* Referidos Recientes */}
            {estadisticas?.referidos_recientes?.length > 0 && (
              <div className="card">
                <h3>📝 Referidos Recientes</h3>
                <div className="lista-referidos-recientes">
                  {estadisticas.referidos_recientes.map((ref) => (
                    <div key={ref.id} className="referido-item">
                      <div>
                        <strong>{ref.nombre}</strong>
                        <div className="referido-email">{ref.email}</div>
                      </div>
                      <span className={`badge badge-${ref.estado}`}>
                        {ref.estado}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* TAB: MIS REFERIDOS */}
        {activeTab === 'referidos' && (
          <div className="tab-content">
            <div className="card">
              <h2>👥 Lista de Referidos</h2>
              
              {referidos.length === 0 ? (
                <div className="no-data">
                  <p>📭 Aún no tienes referidos</p>
                  <p>Comparte tu código de referido para empezar a ganar comisiones</p>
                </div>
              ) : (
                <div className="tabla-wrapper">
                  <table className="tabla-estudiantes">
                    <thead>
                      <tr>
                        <th>Estudiante</th>
                        <th>Carrera</th>
                        <th>Estado</th>
                        <th>Perfil Completo</th>
                        <th>Comisión Generada</th>
                        <th>Fecha Registro</th>
                        <th>Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      {referidos.map((est) => (
                        <tr key={est.id}>
                          <td>
                            <div style={{fontWeight: '600'}}>{est.nombre}</div>
                            <div style={{fontSize: '13px', color: '#718096'}}>{est.email}</div>
                            <div style={{fontSize: '12px', color: '#a0aec0'}}>{est.telefono}</div>
                          </td>
                          <td>{est.carrera_deseada || '-'}</td>
                          <td>
                            <span className={`badge badge-${est.estado}`}>
                              {est.estado}
                            </span>
                          </td>
                          <td>
                            {est.perfil_completo ? (
                              <span style={{color: '#10b981'}}>✅ Completo</span>
                            ) : (
                              <span style={{color: '#f59e0b'}}>⏳ Pendiente</span>
                            )}
                          </td>
                          <td style={{fontWeight: '700', color: '#10b981'}}>
                            {est.comision_generada?.toFixed(2) || '0.00'}€
                          </td>
                          <td>{new Date(est.fecha_registro).toLocaleDateString()}</td>
                          <td>
                            <button
                              className="btn-small btn-primary"
                              onClick={() => navigate(`/agente/estudiante/${est.id}`)}
                            >
                              👁️ Ver Detalle
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB: ESTADÍSTICAS */}
        {activeTab === 'estadisticas' && (
          <div className="tab-content">
            <div className="card">
              <h2>📈 Estadísticas Detalladas</h2>
              
              <div className="stats-grid">
                <div className="stat-box">
                  <h3>Resumen General</h3>
                  <p>Total Referidos: <strong>{perfil?.total_referidos || 0}</strong></p>
                  <p>Comisión Total: <strong>{perfil?.comision_total?.toFixed(2) || '0.00'}€</strong></p>
                  <p>Crédito Disponible: <strong>{perfil?.credito_disponible?.toFixed(2) || '0.00'}€</strong></p>
                </div>

                <div className="stat-box">
                  <h3>Información de Contacto</h3>
                  <p>Email: <strong>{perfil?.email}</strong></p>
                  <p>Teléfono: <strong>{perfil?.telefono || 'No especificado'}</strong></p>
                  <p>Código: <strong>{perfil?.codigo_referido}</strong></p>
                </div>
              </div>

              <div className="info-comision">
                <h3>💰 Sistema de Comisiones</h3>
                <p>Como agente, ganas el <strong>10%</strong> del valor de cada presupuesto aceptado por tus referidos.</p>
                <p>Los pagos son gestionados por el administrador.</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* MODAL GUÍA DEL AGENTE */}
      {mostrarGuia && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.7)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000,
          padding: '20px'
        }}
        onClick={() => setMostrarGuia(false)}
        >
          <div style={{
            backgroundColor: 'white',
            borderRadius: '16px',
            maxWidth: '800px',
            width: '100%',
            maxHeight: '90vh',
            overflow: 'auto',
            padding: '30px',
            boxShadow: '0 20px 60px rgba(0,0,0,0.3)'
          }}
          onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 style={{ margin: 0, color: '#1f2937', fontSize: '28px' }}>📖 Guía Completa del Agente</h2>
              <button 
                onClick={() => setMostrarGuia(false)}
                style={{
                  background: 'none',
                  border: 'none',
                  fontSize: '28px',
                  cursor: 'pointer',
                  color: '#6b7280'
                }}
              >×</button>
            </div>

            {/* Sección 1: Código de Referido */}
            <div style={{ marginBottom: '30px', padding: '20px', backgroundColor: '#f0f9ff', borderRadius: '12px', border: '2px solid #3b82f6' }}>
              <h3 style={{ color: '#1e40af', marginTop: 0, display: 'flex', alignItems: 'center', gap: '10px' }}>
                🎯 1. Tu Código de Referido
              </h3>
              <p style={{ color: '#1f2937', lineHeight: '1.6', marginBottom: '10px' }}>
                <strong>Tu código único:</strong> <span style={{ backgroundColor: '#dbeafe', padding: '4px 12px', borderRadius: '6px', fontFamily: 'monospace', fontSize: '16px' }}>{perfil?.codigo_referido}</span>
              </p>
              <ul style={{ color: '#374151', lineHeight: '1.8' }}>
                <li>Este código está visible en la parte superior de tu dashboard</li>
                <li>Copia el link completo con el botón "📋 Copiar Link"</li>
                <li>Compártelo por WhatsApp, redes sociales, email, etc.</li>
              </ul>
            </div>

            {/* Sección 2: Captación de Estudiantes */}
            <div style={{ marginBottom: '30px', padding: '20px', backgroundColor: '#f0fdf4', borderRadius: '12px', border: '2px solid #10b981' }}>
              <h3 style={{ color: '#065f46', marginTop: 0, display: 'flex', alignItems: 'center', gap: '10px' }}>
                👥 2. Cómo Captar Estudiantes
              </h3>
              <ul style={{ color: '#374151', lineHeight: '1.8' }}>
                <li><strong>Comparte tu link de referido</strong> con personas interesadas en estudiar en el extranjero</li>
                <li>El estudiante debe <strong>registrarse usando tu link</strong> o ingresar tu código manualmente</li>
                <li>Una vez registrado, aparecerá automáticamente en tu lista de "Mis Referidos"</li>
                <li><strong>Importante:</strong> El código debe ingresarse al momento del registro, no se puede agregar después</li>
              </ul>
              <div style={{ backgroundColor: '#d1fae5', padding: '15px', borderRadius: '8px', marginTop: '15px' }}>
                <p style={{ margin: 0, color: '#065f46', fontSize: '14px' }}>
                  💡 <strong>Tip:</strong> Crea un mensaje atractivo explicando los beneficios de estudiar en el extranjero y comparte tu link de referido.
                </p>
              </div>
            </div>

            {/* Sección 3: Sistema de Comisiones */}
            <div style={{ marginBottom: '30px', padding: '20px', backgroundColor: '#fefce8', borderRadius: '12px', border: '2px solid #eab308' }}>
              <h3 style={{ color: '#854d0e', marginTop: 0, display: 'flex', alignItems: 'center', gap: '10px' }}>
                💰 3. Sistema de Comisiones (10%)
              </h3>
              <p style={{ color: '#374151', lineHeight: '1.6', marginBottom: '15px' }}>
                Ganas el <strong>10% de comisión</strong> sobre todos los pagos que realicen tus estudiantes referidos:
              </p>
              <div style={{ backgroundColor: 'white', padding: '15px', borderRadius: '8px', marginBottom: '15px' }}>
                <p style={{ margin: '0 0 10px 0', color: '#1f2937' }}><strong>📊 Ejemplos prácticos:</strong></p>
                <ul style={{ color: '#374151', lineHeight: '1.8', marginTop: 0 }}>
                  <li>Estudiante paga 500€ → Tú ganas <strong>50€</strong></li>
                  <li>Estudiante paga 1,000€ → Tú ganas <strong>100€</strong></li>
                  <li>Estudiante paga 2,500€ → Tú ganas <strong>250€</strong></li>
                  <li>5 estudiantes pagan 1,000€ c/u → Tú ganas <strong>500€</strong></li>
                </ul>
              </div>
              <p style={{ color: '#374151', lineHeight: '1.6' }}>
                ✅ Las comisiones se acumulan automáticamente en tu <strong>"Crédito Disponible"</strong>
                <br/>
                ✅ Puedes ver el detalle de cada comisión en la sección "Mis Referidos"
              </p>
            </div>

            {/* Sección 4: Solicitud de Retiros */}
            <div style={{ marginBottom: '30px', padding: '20px', backgroundColor: '#fef2f2', borderRadius: '12px', border: '2px solid #ef4444' }}>
              <h3 style={{ color: '#991b1b', marginTop: 0, display: 'flex', alignItems: 'center', gap: '10px' }}>
                💳 4. Solicitar Retiro de Comisiones
              </h3>
              <ol style={{ color: '#374151', lineHeight: '1.8' }}>
                <li>Acumula el crédito disponible en tu cuenta</li>
                <li>Cuando quieras retirar, solicita el retiro desde tu dashboard</li>
                <li>El administrador revisará y aprobará tu solicitud</li>
                <li>Recibirás el pago mediante el método acordado (transferencia, PayPal, etc.)</li>
              </ol>
              <div style={{ backgroundColor: '#fee2e2', padding: '15px', borderRadius: '8px', marginTop: '15px' }}>
                <p style={{ margin: 0, color: '#991b1b', fontSize: '14px' }}>
                  ⚠️ <strong>Importante:</strong> Solo puedes retirar el crédito disponible. El crédito retirado se descuenta automáticamente.
                </p>
              </div>
            </div>

            {/* Sección 5: Seguimiento */}
            <div style={{ marginBottom: '30px', padding: '20px', backgroundColor: '#f5f3ff', borderRadius: '12px', border: '2px solid #8b5cf6' }}>
              <h3 style={{ color: '#5b21b6', marginTop: 0, display: 'flex', alignItems: 'center', gap: '10px' }}>
                📊 5. Seguimiento de tus Estudiantes
              </h3>
              <p style={{ color: '#374151', lineHeight: '1.6', marginBottom: '10px' }}>
                En la pestaña <strong>"Mis Referidos"</strong> puedes:
              </p>
              <ul style={{ color: '#374151', lineHeight: '1.8' }}>
                <li>Ver la lista completa de estudiantes que has referido</li>
                <li>Conocer el estado de cada estudiante (activo, inactivo, etc.)</li>
                <li>Ver cuánto ha pagado cada uno y tu comisión generada</li>
                <li>Revisar el historial de pagos</li>
                <li>Monitorear el progreso de tus referidos</li>
              </ul>
            </div>

            {/* Sección 6: Soporte */}
            <div style={{ marginBottom: '20px', padding: '20px', backgroundColor: '#fef3c7', borderRadius: '12px', border: '2px solid #f59e0b' }}>
              <h3 style={{ color: '#92400e', marginTop: 0, display: 'flex', alignItems: 'center', gap: '10px' }}>
                📞 6. Soporte y Contacto
              </h3>
              <p style={{ color: '#374151', lineHeight: '1.6' }}>
                Si tienes dudas sobre:
              </p>
              <ul style={{ color: '#374151', lineHeight: '1.8' }}>
                <li>Cálculo de comisiones</li>
                <li>Proceso de retiros</li>
                <li>Estado de tus referidos</li>
                <li>Cualquier otra consulta</li>
              </ul>
              <p style={{ color: '#374151', lineHeight: '1.6', marginBottom: 0 }}>
                👉 Contacta directamente con el administrador a través del sistema de mensajería o email.
              </p>
            </div>

            <div style={{ textAlign: 'center', paddingTop: '20px', borderTop: '2px solid #e5e7eb' }}>
              <button 
                onClick={() => setMostrarGuia(false)}
                style={{
                  backgroundColor: '#3b82f6',
                  color: 'white',
                  padding: '12px 30px',
                  borderRadius: '8px',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '16px',
                  fontWeight: '600'
                }}
              >
                ✅ Entendido, ¡Empecemos!
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardAgente;
