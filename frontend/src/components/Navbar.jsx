import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { User, Menu } from 'lucide-react';
import Notificaciones from './Notificaciones';
import './Navbar.css';

const Navbar = ({ estudianteId, isAuthenticated, setEstudianteId }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  const handleLogout = () => {
    localStorage.removeItem('estudiante_id');
    localStorage.removeItem('codigo_acceso');
    if (setEstudianteId) setEstudianteId(null);
    window.location.href = '/';
  };

  const isActive = (path) => {
    return location.pathname === path ? 'active' : 'inactive';
  };

  const closeMobileMenu = () => {
    setMobileMenuOpen(false);
  };

  return (
    <header className="navbar">
      <div className="navbar-container">
        {/* Logo */}
        <Link to="/" className="navbar-logo">
          <div className="logo-box">
            <span className="logo-text-short">AE</span>
          </div>
          <span className="logo-text-full">Agencia Educativa España</span>
        </Link>

        {/* Navigation Links - Desktop */}
        <nav className="navbar-links">
          {estudianteId && <Notificaciones estudianteId={estudianteId} />}

          {/* Menú cuando hay estudiante logueado */}
          {estudianteId && (
            <>
              <Link to="/estudiante/dashboard" className={`nav-link ${isActive('/estudiante/dashboard')}`}>
                Mi Portal
              </Link>
              <Link to="/estudiante/simulador" className={`nav-link ${isActive('/estudiante/simulador')}`}>
                Simulador
              </Link>
              <Link to="/estudiante/calculadora-fondos" className={`nav-link ${isActive('/estudiante/calculadora-fondos')}`}>
                Calculadora
              </Link>
              <Link to="/estudiante/documentos" className={`nav-link ${isActive('/estudiante/documentos')}`}>
                Documentos
              </Link>
            </>
          )}

          {/* Enlaces cuando NO hay estudiante logueado */}
          {!estudianteId && (
            <>
              <Link to="/estudiante/login" className={`nav-link ${isActive('/estudiante/login')}`}>
                Acceso
              </Link>
              <Link to="/registro" className={`nav-link ${isActive('/registro')}`}>
                Registro
              </Link>
            </>
          )}

          {/* Botón Cerrar Sesión al final */}
          {estudianteId && (
            <button
              onClick={handleLogout}
              className="logout-btn"
            >
              Salir
            </button>
          )}
        </nav>

        {/* Mobile Menu Button */}
        <div className="navbar-actions">
          <button 
            className="icon-btn mobile-menu-btn"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <Menu size={20} />
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="mobile-menu">
          <div className="mobile-menu-content">
            {estudianteId && (
              <>
                <Link to="/estudiante/dashboard" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Mi Portal
                </Link>
                <Link to="/estudiante/simulador" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Simulador
                </Link>
                <Link to="/estudiante/calculadora-fondos" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Calculadora
                </Link>
                <Link to="/estudiante/alertas" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Alertas
                </Link>
                <Link to="/estudiante/documentos" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Documentos
                </Link>
                <Link to="/estudiante/universidades" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Universidades
                </Link>
                <button onClick={() => { handleLogout(); closeMobileMenu(); }} className="mobile-menu-logout">
                  Cerrar Sesión
                </button>
              </>
            )}

            {!estudianteId && (
              <>
                <Link to="/estudiante/login" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Acceso Estudiantes
                </Link>
                <Link to="/registro" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Registrarse
                </Link>
                <Link to="/portal" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Consultar Estado
                </Link>
              </>
            )}

            {isAuthenticated && (
              <>
                <Link to="/admin/chats" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Chats
                </Link>
                <Link to="/admin/analytics" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Analytics
                </Link>
                <Link to="/admin/documentos" className="mobile-menu-link" onClick={closeMobileMenu}>
                  Documentos
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

export default Navbar;
