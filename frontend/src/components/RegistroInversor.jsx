import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './RegistroEstudiante.css';

const getApiUrl = () => {
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  const hostname = window.location.hostname;
  return (hostname === 'localhost' || hostname === '127.0.0.1')
    ? 'http://localhost:8000'
    : `http://${hostname}:8000`;
};

const RegistroInversor = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    telefono: '',
    pais: 'España',
    password: '',
    confirmarPassword: '',
    acepto_terminos: false,
    codigo_patrocinio: ''
  });

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const ref = params.get('ref');
    if (ref) {
      setFormData(prev => ({ ...prev, codigo_patrocinio: ref }));
    }
  }, []);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const nombre = formData.nombre.trim();
    const email = formData.email.trim();
    const telefono = formData.telefono.trim();
    const password = formData.password.trim();
    const confirmarPassword = formData.confirmarPassword.trim();

    if (!nombre || !email || !telefono) {
      setError('Completa nombre, correo y teléfono para continuar.');
      return;
    }
    if (!password || !confirmarPassword) {
      setError('Debes crear una contraseña y confirmarla.');
      return;
    }
    if (password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres.');
      return;
    }
    if (password !== confirmarPassword) {
      setError('Las contraseñas no coinciden.');
      return;
    }
    if (!formData.acepto_terminos) {
      setError('Debes aceptar la información y condiciones para continuar.');
      return;
    }

    setLoading(true);
    try {
      const apiUrl = getApiUrl();
      const response = await axios.post(`${apiUrl}/api/inversores/registro`, {
        nombre,
        email: email.toLowerCase(),
        telefono,
        pais: formData.pais.trim() || 'España',
        password,
        codigo_patrocinio: formData.codigo_patrocinio.trim()
      }, { timeout: 10000 });

      const { token, inversor } = response.data;

      const userSession = {
        id: inversor.id,
        name: inversor.nombre,
        email: inversor.email,
        telefono: formData.telefono.trim(),
        pais: formData.pais.trim() || 'España',
        role: 'inversor'
      };

      localStorage.setItem('token', token);
      localStorage.setItem('usuario', userSession.name);
      localStorage.setItem('capital_trade_user', JSON.stringify(userSession));
      window.dispatchEvent(new Event('capital-trade-sync'));
      setSuccess(true);
    } catch (err) {
      let errorMsg = 'Error al registrarse. Inténtalo de nuevo.';

      if (err.code === 'ECONNABORTED' || err.code === 'ERR_NETWORK') {
        errorMsg = 'No se puede conectar al servidor. Inténtalo más tarde.';
      } else if (err.response?.status === 409) {
        errorMsg = 'Ya existe un usuario registrado con ese correo electrónico.';
      } else if (err.response?.data?.detail) {
        errorMsg = Array.isArray(err.response.data.detail)
          ? err.response.data.detail[0]?.msg || errorMsg
          : err.response.data.detail;
      }

      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="registro-success">
        <div className="success-card">
          <div className="success-icon">✓</div>
          <h2>Solicitud enviada</h2>
          <p>Hemos recibido tu interés en participar en operaciones comerciales.</p>
          <div className="success-panel">
            <p>Tu perfil ha quedado registrado como inversor.</p>
            <p>Próximo paso: revisaremos tus datos y te contactaremos con la información de la operación.</p>
          </div>
          <div className="success-actions">
            <button onClick={() => navigate('/dashboard')} className="submit-button" style={{ width: 'auto' }}>Ir a mi panel</button>
            <button onClick={() => navigate('/operaciones')} className="btn btn-secondary" style={{ width: 'auto' }}>Ver operaciones</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="registro-container">
      <div className="registro-card">
        <div className="registro-header">
          <p className="section-label">Inversores</p>
          <h1>Registro</h1>
          <p>Completa tus datos para recibir información sobre oportunidades comerciales.</p>
        </div>

        <form onSubmit={handleSubmit} className="registro-form">
          <div className="form-section">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="nombre">Nombre completo *</label>
                <input id="nombre" name="nombre" value={formData.nombre} onChange={handleChange} required placeholder="Ej: Carlos Fernández" />
              </div>

              <div className="form-group">
                <label htmlFor="email">Correo electrónico *</label>
                <input id="email" name="email" type="email" value={formData.email} onChange={handleChange} required placeholder="tucorreo@email.com" />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="telefono">Teléfono *</label>
                <input id="telefono" name="telefono" value={formData.telefono} onChange={handleChange} required placeholder="+34 600 000 000" />
              </div>

              <div className="form-group">
                <label htmlFor="pais">País</label>
                <input id="pais" name="pais" value={formData.pais} onChange={handleChange} placeholder="España" />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="password">Contraseña *</label>
                <input id="password" name="password" type="password" value={formData.password} onChange={handleChange} required placeholder="Mínimo 6 caracteres" autoComplete="new-password" />
              </div>

              <div className="form-group">
                <label htmlFor="confirmarPassword">Confirmar contraseña *</label>
                <input id="confirmarPassword" name="confirmarPassword" type="password" value={formData.confirmarPassword} onChange={handleChange} required placeholder="Repite tu contraseña" autoComplete="new-password" />
              </div>
            </div>

            {formData.codigo_patrocinio && (
              <div className="form-row">
                <div className="form-group" style={{ width: '100%' }}>
                  <label htmlFor="codigo_patrocinio" style={{ color: '#d4af37' }}>Afiliado por el Patrocinador VIP:</label>
                  <input id="codigo_patrocinio" value={formData.codigo_patrocinio} disabled style={{ backgroundColor: 'rgba(212,175,55,0.1)', color: '#d4af37', border: '1px dashed #d4af37', fontWeight: 'bold' }} />
                </div>
              </div>
            )}
          </div>

          <div className="form-section">
            <div className="form-group checkbox-row" style={{ marginBottom: 0 }}>
              <label className="checkbox-label">
                <input type="checkbox" name="acepto_terminos" checked={formData.acepto_terminos} onChange={handleChange} />
                <span>Acepto que mis datos se utilicen para contactar conmigo sobre oportunidades comerciales y condiciones de participación.</span>
              </label>
            </div>
          </div>

          {error && <div className="error-message">⚠️ {error}</div>}

          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? 'Registrando...' : 'Registrarse'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default RegistroInversor;
