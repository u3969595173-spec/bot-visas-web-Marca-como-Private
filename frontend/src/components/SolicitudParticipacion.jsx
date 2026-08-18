import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Platform.css';

const initialForm = {
  nombre: '',
  email: '',
  telefono: '',
  perfil: 'Particular',
  operacion: 'Compra y exportación de cemento',
  monto: '',
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

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
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
    setTimeout(() => {
      setLoading(false);
      setSuccess(true);
      localStorage.setItem('solicitud_participacion', JSON.stringify(form));
    }, 600);
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
            <div className="form-group">
              <label>Monto estimado</label>
              <input name="monto" value={form.monto} onChange={handleChange} placeholder="€20.000" />
            </div>
          </div>

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
