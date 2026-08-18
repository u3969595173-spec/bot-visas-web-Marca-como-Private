import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './LoginEstudiante.css';

const getApiUrl = () => {
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  const hostname = window.location.hostname;
  return (hostname === 'localhost' || hostname === '127.0.0.1')
    ? 'http://localhost:8000'
    : `http://${hostname}:8000`;
};

const LoginInversor = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const apiUrl = getApiUrl();
      const response = await axios.post(`${apiUrl}/api/inversores/login`, {
        email: email.trim().toLowerCase(),
        password: password.trim()
      }, { timeout: 8000 });

      const { token, inversor } = response.data;

      const userSession = {
        id: inversor.id,
        name: inversor.nombre,
        email: inversor.email,
        role: 'inversor'
      };

      localStorage.setItem('token', token);
      localStorage.setItem('usuario', userSession.name);
      localStorage.setItem('capital_trade_user', JSON.stringify(userSession));
      window.dispatchEvent(new Event('capital-trade-sync'));
      navigate('/dashboard');
    } catch (err) {
      let errorMsg = 'Credenciales incorrectas o usuario no registrado.';

      if (err.code === 'ECONNABORTED' || err.code === 'ERR_NETWORK') {
        errorMsg = 'No se puede conectar al servidor. Inténtalo más tarde.';
      } else if (err.response?.status === 401 || err.response?.status === 403) {
        errorMsg = 'Correo o contraseña incorrectos.';
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

  return (
    <div className="login-estudiante-container">
      <div className="login-estudiante-card">
        <div className="login-header">
          <p className="section-label">Portal de inversor</p>
          <h1>Acceso institucional</h1>
          <p>Consulta operaciones, capital y documentación asociada a tus participaciones.</p>
        </div>

        <div className="portal-cta-group">
          <button className="portal-cta btn-primary">Inversor</button>
          <button className="portal-cta btn-secondary" onClick={() => navigate('/admin/login')}>Administrador</button>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Correo electrónico</label>
            <input
              id="email"
              type="email"
              className="form-control"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="tucorreo@email.com"
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
              autoComplete="current-password"
            />
          </div>

          {error && <div className="alert alert-error">⚠️ {error}</div>}

          <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
            {loading ? 'Entrando...' : 'Acceder'}
          </button>
        </form>

        <div className="login-footer">
          <p>¿No tienes cuenta?</p>
          <button className="btn btn-secondary" onClick={() => navigate('/registro')}>Solicitar información</button>
        </div>
      </div>
    </div>
  );
};

export default LoginInversor;
