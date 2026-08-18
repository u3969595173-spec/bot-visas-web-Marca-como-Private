import React from 'react';
import './Platform.css';

function PerfilInversor() {
  const userSession = React.useMemo(() => {
    try {
      return JSON.parse(localStorage.getItem('capital_trade_user') || 'null');
    } catch {
      return null;
    }
  }, []);

  const nombre = userSession?.name || userSession?.nombre || localStorage.getItem('usuario') || 'Inversor';
  const email = userSession?.email || '—';
  const pais = userSession?.pais || 'España';

  return (
    <div className="platform-page">
      <div className="platform-card">
        <div className="platform-header">
          <div>
            <p className="section-label">Cuenta</p>
            <h1>Perfil de inversor</h1>
          </div>
          <button className="secondary-btn" onClick={() => alert('Edición de perfil disponible próximamente. Contáctanos en contacto@capitaltradeiberia.com')}>Editar perfil</button>
        </div>

        <div className="stats-grid">
          <div className="stat-box">
            <span>Nombre</span>
            <strong>{nombre}</strong>
          </div>
          <div className="stat-box">
            <span>Perfil</span>
            <strong>Particular</strong>
          </div>
          <div className="stat-box">
            <span>Estado</span>
            <strong>Verificado</strong>
          </div>
        </div>

        <div className="content-grid">
          <div className="document-list">
            <h2>Datos básicos</h2>
            <div className="document-item">
              <strong>Email</strong>
              <p>{email}</p>
            </div>
            <div className="document-item">
              <strong>País</strong>
              <p>{pais}</p>
            </div>
            <div className="document-item">
              <strong>Objetivo</strong>
              <p>Participar en operaciones de compra y exportación con estructura definida.</p>
            </div>
          </div>

          <div className="movement-list">
            <h2>Riesgo y aptitud</h2>
            <div className="movement-item">
              <strong>Perfil de riesgo</strong>
              <p>Medio</p>
            </div>
            <div className="movement-item">
              <strong>Documentación</strong>
              <p>Identidad y perfil cargados</p>
            </div>
            <div className="movement-item">
              <strong>Observaciones</strong>
              <p>Se requiere validación del administrador antes de formalizar aportaciones.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PerfilInversor;

