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
          <button onClick={cerrarSesion} className="btn-logout">
            🚪 Cerrar Sesión
          </button>
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
                <button onClick={copiarLinkReferido} className="btn-copiar">
                  {copiado ? '✅ ¡Copiado!' : '📋 Copiar Link'}
                </button>
              </div>
              <p className="codigo-info">
                📱 Comparte este código con estudiantes interesados. 
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
    </div>
  );
};

export default DashboardAgente;
