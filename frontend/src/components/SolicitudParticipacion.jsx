import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Platform.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const initialForm = {
  nombre: '',
  email: '',
  telefono: '',
  perfil: 'Particular',
  operacion: 'Compra y exportación de cemento',
  monto: '',
  moneda: 'USDT BEP-20',
  plazo: '6-10 meses',
  objetivo: '',
  acepta: false
};

function SolicitudParticipacion() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const [metodosPago, setMetodosPago] = useState([]);
  const [metodoPago, setMetodoPago] = useState(null);

  useEffect(() => {
    fetch(`${API}/api/metodos-pago`)
      .then(r => r.json())
      .then(d => {
        setMetodosPago(d.metodos || []);
        if (d.metodos?.length) setMetodoPago(d.metodos[0]);
      })
      .catch(() => { });
  }, []);

  const handleMonedaChange = (moneda) => {
    setForm(f => ({ ...f, moneda }));
    setMetodoPago(metodosPago.find(m => m.moneda === moneda) || null);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!form.nombre || !form.email || !form.telefono || !form.monto) {
      setError('Completa nombre, correo, teléfono y monto para continuar.');
      return;
    }

    if (!form.acepta) {
      setError('Debes aceptar la información previa antes de continuar.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API}/api/solicitudes-participacion`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      if (response.ok) {
        setSuccess(true);
      } else {
        const data = await response.json().catch(() => ({}));
        setError(data.detail || 'Error al enviar la solicitud. Inténtalo de nuevo.');
      }
    } catch (err) {
      console.error(err);
      setError('No se pudo conectar con el servidor. Verifica tu conexión.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="detail-shell">
        <div className="detail-card success-panel-card">
          <div className="success-icon">✓</div>
          <h2>Solicitud registrada</h2>
          <p>Hemos recibido tu interés en participar en la operación seleccionada.</p>
          <p>El equipo revisará tu perfil y te contactará con la documentación y condiciones específicas.</p>
          <div className="detail-cta">
            <button className="primary-btn" onClick={() => navigate('/dashboard')}>Ir al panel</button>
            <button className="secondary-btn" onClick={() => navigate('/operaciones')}>Volver a operaciones</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="detail-shell">
      <div className="detail-card">
        <div className="detail-header" style={{ marginBottom: '1.5rem' }}>
          <p className="section-label">Participación</p>
          <h1>Solicitar información de operación</h1>
        </div>

        <form className="participation-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label>Nombre completo</label>
              <input name="nombre" value={form.nombre} onChange={handleChange} placeholder="Tu nombre" />
            </div>
            <div className="form-group">
              <label>Correo electrónico</label>
              <input name="email" type="email" value={form.email} onChange={handleChange} placeholder="correo@email.com" />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Teléfono</label>
              <input name="telefono" value={form.telefono} onChange={handleChange} placeholder="+34 600 000 000" />
            </div>
            <div className="form-group">
              <label>Perfil</label>
              <select name="perfil" value={form.perfil} onChange={handleChange}>
                <option>Particular</option>
                <option>Empresario</option>
                <option>Institucional</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Operación de interés</label>
              <select name="operacion" value={form.operacion} onChange={handleChange}>
                <option>Compra y exportación de cemento</option>
                <option>Compra y exportación de paneles</option>
                <option>Materiales de construcción</option>
              </select>
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Monto estimado</label>
              <input name="monto" value={form.monto} onChange={handleChange} placeholder="1.000" />
            </div>
            <div className="form-group">
              <label>Moneda de aportación</label>
              <select value={form.moneda} onChange={e => handleMonedaChange(e.target.value)}>
                {metodosPago.length > 0
                  ? metodosPago.map(m => <option key={m.moneda} value={m.moneda}>{m.moneda}</option>)
                  : ['USDT BEP-20', 'EUR'].map(m => <option key={m} value={m}>{m}</option>)
                }
              </select>
            </div>
          </div>

          {/* Datos de pago */}
          {metodoPago && (
            <div style={{ background: 'rgba(246,196,83,0.06)', border: '1px solid rgba(246,196,83,0.25)', borderRadius: 12, padding: '1.2rem', marginBottom: '1rem' }}>
              <p style={{ margin: '0 0 0.8rem', fontWeight: 700, color: '#f6c453', fontSize: 15 }}>
                {metodoPago.tipo === 'wallet' ? '💎' : '🏦'} Datos para tu aportación en {metodoPago.moneda}
              </p>
              {metodoPago.tipo === 'wallet' ? (
                <div>
                  <p style={{ margin: '0 0 4px', fontSize: 13, color: '#94a3b8' }}>Dirección wallet ({metodoPago.red}):</p>
                  <p style={{ margin: '0 0 8px', fontFamily: 'monospace', fontSize: 14, color: '#f1f5f9', wordBreak: 'break-all' }}>{metodoPago.wallet || '—'}</p>
                </div>
              ) : metodoPago.tipo === 'iban' ? (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                  {metodoPago.titular && <div style={{ gridColumn: 'span 2' }}><span style={{ fontSize: 12, color: '#94a3b8' }}>Titular: </span><strong>{metodoPago.titular}</strong></div>}
                  {metodoPago.iban && <div style={{ gridColumn: 'span 2' }}><span style={{ fontSize: 12, color: '#94a3b8' }}>IBAN: </span><strong style={{ fontFamily: 'monospace' }}>{metodoPago.iban}</strong></div>}
                  {metodoPago.concepto && <div style={{ gridColumn: 'span 2' }}><span style={{ fontSize: 12, color: '#94a3b8' }}>Concepto: </span><strong>{metodoPago.concepto}</strong></div>}
                </div>
              ) : (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '0.5rem' }}>
                  {metodoPago.numero && <div><span style={{ fontSize: 12, color: '#94a3b8' }}>Nº de cuenta/tarjeta: </span><strong style={{ fontFamily: 'monospace' }}>{metodoPago.numero}</strong></div>}
                </div>
              )}
              {metodoPago.instrucciones && <p style={{ margin: '8px 0 0', fontSize: 13, color: '#94a3b8' }}>ℹ️ {metodoPago.instrucciones}</p>}
            </div>
          )}

          <div className="form-row">
            <div className="form-group">
              <label>Plazo deseado</label>
              <input name="plazo" value={form.plazo} onChange={handleChange} placeholder="6-10 meses" />
            </div>
            <div className="form-group">
              <label>Objetivo principal</label>
              <input name="objetivo" value={form.objetivo} onChange={handleChange} placeholder="Participar con capital en la operación" />
            </div>
          </div>

          <div className="form-group">
            <label>Comentarios</label>
            <textarea name="comentarios" rows="4" value={form.comentarios || ''} onChange={handleChange} placeholder="Queremos entender mejor tu perfil, objetivos y nivel de participación." />
          </div>

          <div className="form-group checkbox-row">
            <label className="checkbox-label">
              <input type="checkbox" name="acepta" checked={form.acepta} onChange={handleChange} />
              <span>Acepto que la información se utilice para evaluar la participación en la operación y que cada operación tiene condiciones, riesgo y plazo específicos.</span>
            </label>
          </div>

          {error && <div className="error-message">⚠️ {error}</div>}

          <div className="detail-cta">
            <button type="submit" className="primary-btn" disabled={loading}>
              {loading ? 'Enviando...' : 'Enviar solicitud'}
            </button>
            <button type="button" className="secondary-btn" onClick={() => navigate('/operaciones')}>Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default SolicitudParticipacion;
