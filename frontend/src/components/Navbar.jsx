import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import Notificaciones from './Notificaciones';
import './Navbar.css';

const Navbar = ({ estudianteId, isAuthenticated, setEstudianteId }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('estudiante_id');
    localStorage.removeItem('codigo_acceso');
    if (setEstudianteId) setEstudianteId(null);
    window.location.href = '/';
  };

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <span>🎓</span> Agencia Educativa España
        </Link>

        <div className="navbar-links">
          {estudianteId && <Notificaciones estudianteId={estudianteId} />}

          {/* Menú Estudiante */}
          {estudianteId && (
            <>
              <Link to="/estudiante/dashboard" className={`nav-link ${isActive('/estudiante/dashboard')}`}>
                Mi Portal
              </Link>
              <Link to="/estudiante/simulador" className={`nav-link ${isActive('/estudiante/simulador')}`}>
                🎭 Simulador
              </Link>
              <Link to="/estudiante/calculadora-fondos" className={`nav-link ${isActive('/estudiante/calculadora-fondos')}`}>
                💰 Calculadora
              </Link>
              <Link to="/estudiante/alertas" className={`nav-link ${isActive('/estudiante/alertas')}`}>
                📅 Alertas
              </Link>
              <Link to="/estudiante/documentos" className={`nav-link ${isActive('/estudiante/documentos')}`}>
                📂 Documentos
              </Link>
              <Link to="/estudiante/universidades" className={`nav-link ${isActive('/estudiante/universidades')}`}>
                🎓 Universidades
              </Link>
            </>
          )}

          {/* Menú Público */}
          {!estudianteId && !isAuthenticated && (
            <>
              <Link to="/estudiante/login" className={`nav-link ${isActive('/estudiante/login')}`}>
                🎓 Acceso Estudiantes
              </Link>
              <Link to="/registro" className={`nav-link ${isActive('/registro')}`}>
                Registrarse
              </Link>
              <Link to="/portal" className={`nav-link ${isActive('/portal')}`}>
                Consultar Estado
              </Link>
              <Link to="/admin/login" className={`nav-link ${isActive('/admin/login')}`}>
                🔐 Admin
              </Link>
            </>
          )}

          {/* Enlaces Comunes */}
          <Link to="/blog" className={`nav-link ${isActive('/blog')}`}>
            📝 Blog
          </Link>
          <Link to="/testimonios" className={`nav-link ${isActive('/testimonios')}`}>
            ⭐ Testimonios
          </Link>

          {/* Menú Admin */}
          {isAuthenticated && (
            <>
              <Link to="/admin/universidades" className={`nav-link ${isActive('/admin/universidades')}`}>
                🎓 Universidades
              </Link>
              <Link to="/admin/programas" className={`nav-link ${isActive('/admin/programas')}`}>
                📚 Programas
              </Link>
              <Link to="/admin/blog" className={`nav-link ${isActive('/admin/blog')}`}>
                📝 Blog
              </Link>
              <Link to="/admin/testimonios" className={`nav-link ${isActive('/admin/testimonios')}`}>
                ⭐ Testimonios
              </Link>
              <Link to="/admin/chats" className={`nav-link ${isActive('/admin/chats')}`}>
                💬 Chats
              </Link>
              <Link to="/admin/analytics" className={`nav-link ${isActive('/admin/analytics')}`}>
                📊 Analytics
              </Link>
              <Link to="/admin/documentos" className={`nav-link ${isActive('/admin/documentos')}`}>
                📂 Documentos
              </Link>
            </>
          )}

          {/* Botón Logout */}
          {estudianteId && (
            <button onClick={handleLogout} className="nav-btn nav-btn-logout">
              🚪 Cerrar Sesión
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
