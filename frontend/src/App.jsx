import React from 'react'
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom'
import RegistroEstudiante from './components/RegistroEstudiante'
import LoginEstudiante from './components/LoginEstudiante'
import LoginAdmin from './components/LoginAdmin'
import DashboardAdminExpandido from './components/DashboardAdminExpandido'
import DashboardUsuario from './components/DashboardUsuario'
import PortalEstudiante from './components/PortalEstudiante'
import PoliticaPrivacidad from './components/PoliticaPrivacidad'
import TerminosCondiciones from './components/TerminosCondiciones'
import SimuladorEntrevista from './components/SimuladorEntrevista'
import Home from './components/Home'

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(
    !!localStorage.getItem('token')
  )
  const [estudianteId, setEstudianteId] = React.useState(null)

  // Verificar localStorage al cargar
  React.useEffect(() => {
    const storedId = localStorage.getItem('estudiante_id')
    if (storedId) {
      setEstudianteId(storedId)
    }
  }, [])

  return (
    <BrowserRouter>
      <div className="app">
        <nav style={styles.nav}>
          <div className="container" style={styles.navContainer}>
            <Link to="/" style={styles.logo}>
              🎓 Agencia Educativa España
            </Link>
            <div style={styles.navLinks}>
              <Link to="/estudiante/login" style={styles.navLink}>
                🎓 Acceso Estudiantes
              </Link>
              {!estudianteId && (
                <Link to="/registro" style={styles.navLink}>
                  Registrarse
                </Link>
              )}
              {estudianteId && (
                <>
                  <Link to="/estudiante/dashboard" style={styles.navLink}>
                    Mi Portal
                  </Link>
                  <Link to="/estudiante/simulador" style={styles.navLink}>
                    🎭 Simulador
                  </Link>
                </>
              )}
              <Link to="/portal" style={styles.navLink}>
                Consultar Estado
              </Link>
              {!isAuthenticated ? (
                <Link to="/admin/login" style={styles.navLink}>
                  Admin
                </Link>
              ) : (
                <Link to="/admin/dashboard" style={styles.navLink}>
                  Dashboard Admin
                </Link>
              )}
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/estudiante/login" element={<LoginEstudiante />} />
          <Route 
            path="/registro" 
            element={<RegistroEstudiante onRegistro={(id) => {
              setEstudianteId(id)
              localStorage.setItem('estudiante_id', id)
            }} />} 
          />
          <Route path="/portal" element={<PortalEstudiante />} />
          <Route path="/politica-privacidad" element={<PoliticaPrivacidad />} />
          <Route path="/terminos-condiciones" element={<TerminosCondiciones />} />
          <Route
            path="/estudiante/simulador"
            element={
              estudianteId ? (
                <SimuladorEntrevista estudianteId={estudianteId} />
              ) : (
                <Navigate to="/portal" />
              )
            }
          />
          <Route
            path="/estudiante/dashboard"
            element={
              estudianteId ? (
                <DashboardUsuario estudianteId={estudianteId} />
              ) : (
                <Navigate to="/portal" />
              )
            }
          />
          <Route
            path="/dashboard-usuario/:id"
            element={<DashboardUsuario />}
          />
          <Route
            path="/admin/login"
            element={<LoginAdmin onLogin={() => setIsAuthenticated(true)} />}
          />
          <Route
            path="/admin/dashboard"
            element={
              isAuthenticated ? (
                <DashboardAdminExpandido onLogout={() => setIsAuthenticated(false)} />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

const styles = {
  nav: {
    background: 'white',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    padding: '15px 0',
    marginBottom: '30px',
  },
  navContainer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  logo: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#667eea',
    textDecoration: 'none',
  },
  navLinks: {
    display: 'flex',
    gap: '20px',
  },
  navLink: {
    color: '#2d3748',
    textDecoration: 'none',
    fontWeight: '500',
    transition: 'color 0.3s',
  },
}

export default App
