import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu } from 'lucide-react';
import './Navbar.css';

const Navbar = ({ isAuthenticated, setCurrentUser }) => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);
  const [currentUser, setUserState] = React.useState(null);

  React.useEffect(() => {
    const syncUser = () => {
      const saved = localStorage.getItem('capital_trade_user');
      if (saved) {
        try {
          setUserState(JSON.parse(saved));
        } catch {
          setUserState(null);
        }
      } else {
        setUserState(null);
      }
    };

    syncUser();
    window.addEventListener('storage', syncUser);
    window.addEventListener('capital-trade-sync', syncUser);

    return () => {
      window.removeEventListener('storage', syncUser);
      window.removeEventListener('capital-trade-sync', syncUser);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('capital_trade_user');
    localStorage.removeItem('token');
    setUserState(null);
    if (setCurrentUser) setCurrentUser();
    window.location.href = '/';
  };

  const isActive = (path) => {
    return location.pathname === path ? 'active' : 'inactive';
  };

  const closeMobileMenu = () => {
    setMobileMenuOpen(false);
  };

  const userIsAuthenticated = isAuthenticated || !!currentUser;
  const isAdmin = currentUser?.role === 'admin';

  return (
    <header className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <div className="logo-box">
            <span className="logo-text-short">CT</span>
          </div>
          <span className="logo-text-full">Capital Iberia</span>
        </Link>

        <nav className="navbar-links">
          <Link to="/como-funciona" className={`nav-link ${isActive('/como-funciona')}`}>Cómo funciona</Link>
          <Link to="/programa" className={`nav-link ${isActive('/programa')}`} style={{ background: 'linear-gradient(135deg, #f6c453, #dba93a)', color: '#0a0f1a', padding: '6px 14px', borderRadius: 8, fontWeight: 700 }}>👑 Programa Líderes</Link>
          <Link to="/programa-partner" className={`nav-link ${isActive('/programa-partner')}`} style={{ background: 'linear-gradient(135deg, #10b981, #059669)', color: '#0a0f1a', padding: '6px 14px', borderRadius: 8, fontWeight: 700 }}>💎 Programa Partner</Link>
          <Link to="/programa-combinado" className={`nav-link ${isActive('/programa-combinado')}`} style={{ background: 'linear-gradient(135deg, #ef4444, #b91c1c)', color: '#fff', padding: '6px 14px', borderRadius: 8, fontWeight: 700 }}>🔥 Programa Combinado</Link>
          <Link to="/operaciones" className={`nav-link ${isActive('/operaciones')}`}>Operaciones</Link>
          <Link to="/sobre-nosotros" className={`nav-link ${isActive('/sobre-nosotros')}`}>Nosotros</Link>
          <Link to="/contacto" className={`nav-link ${isActive('/contacto')}`}>Contacto</Link>

          {!userIsAuthenticated && (
            <>
              <Link to="/login" className={`nav-link ${isActive('/login')}`}>Acceso</Link>
              <Link to="/registro" className={`nav-link ${isActive('/registro')}`}>Registro</Link>
            </>
          )}

          {userIsAuthenticated && !isAdmin && (
            <>
              <Link to="/dashboard" className={`nav-link ${isActive('/dashboard')}`}>Dashboard</Link>
              <Link to="/mercado" className={`nav-link ${isActive('/mercado')}`}>Mercado</Link>
              <Link to="/comunidad" className={`nav-link ${isActive('/comunidad')}`}>Comunidad</Link>
              <Link to="/perfil" className={`nav-link ${isActive('/perfil')}`}>Perfil</Link>
              <button onClick={handleLogout} className="logout-btn">Salir</button>
            </>
          )}

          {isAdmin && (
            <>
              <Link to="/admin" className={`nav-link ${isActive('/admin')}`}>Panel Admin</Link>
              <Link to="/comunidad" className={`nav-link ${isActive('/comunidad')}`}>Comunidad</Link>
              <button onClick={handleLogout} className="logout-btn">Salir</button>
            </>
          )}
        </nav>

        <div className="navbar-actions">
          <button className="icon-btn mobile-menu-btn" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            <Menu size={20} />
          </button>
        </div>
      </div>

      {mobileMenuOpen && (
        <div className="mobile-menu">
          <div className="mobile-menu-content">
            <Link to="/como-funciona" className="mobile-menu-link" onClick={closeMobileMenu}>Cómo funciona</Link>
            <Link to="/programa" className="mobile-menu-link" onClick={closeMobileMenu}>Programa Líderes</Link>
            <Link to="/programa-partner" className="mobile-menu-link" onClick={closeMobileMenu}>Programa Partner</Link>
            <Link to="/programa-combinado" className="mobile-menu-link" onClick={closeMobileMenu}>Programa Combinado</Link>
            <Link to="/operaciones" className="mobile-menu-link" onClick={closeMobileMenu}>Operaciones</Link>
            <Link to="/sobre-nosotros" className="mobile-menu-link" onClick={closeMobileMenu}>Nosotros</Link>
            <Link to="/contacto" className="mobile-menu-link" onClick={closeMobileMenu}>Contacto</Link>

            {!userIsAuthenticated && (
              <>
                <Link to="/login" className="mobile-menu-link" onClick={closeMobileMenu}>Acceso</Link>
                <Link to="/registro" className="mobile-menu-link" onClick={closeMobileMenu}>Registro</Link>
              </>
            )}

            {userIsAuthenticated && !isAdmin && (
              <>
                <Link to="/dashboard" className="mobile-menu-link" onClick={closeMobileMenu}>Dashboard</Link>
                <Link to="/mercado" className="mobile-menu-link" onClick={closeMobileMenu}>Mercado</Link>
                <Link to="/comunidad" className="mobile-menu-link" onClick={closeMobileMenu}>Comunidad</Link>
                <Link to="/perfil" className="mobile-menu-link" onClick={closeMobileMenu}>Perfil</Link>
                <button onClick={() => { handleLogout(); closeMobileMenu(); }} className="mobile-menu-logout">Cerrar sesión</button>
              </>
            )}

            {isAdmin && (
              <>
                <Link to="/admin" className="mobile-menu-link" onClick={closeMobileMenu}>Panel Admin</Link>
                <Link to="/comunidad" className="mobile-menu-link" onClick={closeMobileMenu}>Comunidad</Link>
                <button onClick={() => { handleLogout(); closeMobileMenu(); }} className="mobile-menu-logout">Cerrar sesión</button>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

export default Navbar;
