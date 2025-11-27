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
import CalculadoraFondos from './components/CalculadoraFondos'
import AlertasFechas from './components/AlertasFechas'
import BuscadorUniversidades from './components/BuscadorUniversidades'
import AdminUniversidades from './components/AdminUniversidades'
import AdminProgramas from './components/AdminProgramas'
import BlogLista from './components/BlogLista'
import BlogPost from './components/BlogPost'
import AdminBlog from './components/AdminBlog'
import TestimoniosLista from './components/TestimoniosLista'
import AdminTestimonios from './components/AdminTestimonios'
import Notificaciones from './components/Notificaciones'
import ChatWidget from './components/ChatWidget'
import AdminChats from './components/AdminChats'
import DashboardAnalytics from './components/DashboardAnalytics'
import GestorDocumentos from './components/GestorDocumentos'
import AdminDocumentos from './components/AdminDocumentos'
import AdminServicios from './components/AdminServicios'
import ContactarUniversidades from './components/ContactarUniversidades'
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
          <div style={styles.navContainer}>
            <Link to="/" style={styles.logo}>
              🎓 Agencia Educativa España
            </Link>
            <div style={styles.navLinks}>
              {estudianteId && <Notificaciones estudianteId={estudianteId} />}
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
                  <Link to="/estudiante/calculadora-fondos" style={styles.navLink}>
                    💰 Calculadora
                  </Link>
                  <Link to="/estudiante/alertas" style={styles.navLink}>
                    📅 Alertas
                  </Link>
                  <Link to="/estudiante/documentos" style={styles.navLink}>
                    📂 Documentos
                  </Link>
                  <Link to="/estudiante/universidades" style={styles.navLink}>
                    🎓 Universidades
                  </Link>
                </>
              )}
              <Link to="/blog" style={styles.navLink}>
                📝 Blog
              </Link>
              <Link to="/testimonios" style={styles.navLink}>
                ⭐ Testimonios
              </Link>
              <Link to="/portal" style={styles.navLink}>
                Consultar Estado
              </Link>
              {!isAuthenticated ? (
                <Link to="/admin/login" style={styles.navLink}>
                  Admin
                </Link>
              ) : (
                <Link to="/admin/login" style={styles.navLink}>
                  Admin
                </Link>
              )}
              {isAuthenticated && (
                <>
                  <Link to="/admin/universidades" style={styles.navLink}>
                    🎓 Universidades
                  </Link>
                  <Link to="/admin/programas" style={styles.navLink}>
                    📚 Programas
                  </Link>
                  <Link to="/admin/blog" style={styles.navLink}>
                    📝 Blog
                  </Link>
                  <Link to="/admin/testimonios" style={styles.navLink}>
                    ⭐ Testimonios
                  </Link>
                  <Link to="/admin/chats" style={styles.navLink}>
                    💬 Chats
                  </Link>
                  <Link to="/admin/analytics" style={styles.navLink}>
                    📊 Analytics
                  </Link>
                  <Link to="/admin/documentos" style={styles.navLink}>
                    📂 Documentos
                  </Link>
                </>
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
            path="/estudiante/calculadora-fondos"
            element={
              estudianteId ? (
                <CalculadoraFondos estudianteId={estudianteId} />
              ) : (
                <Navigate to="/portal" />
              )
            }
          />
          <Route
            path="/estudiante/alertas"
            element={
              estudianteId ? (
                <AlertasFechas estudianteId={estudianteId} />
              ) : (
                <Navigate to="/portal" />
              )
            }
          />
          <Route
            path="/estudiante/universidades"
            element={
              estudianteId ? (
                <BuscadorUniversidades estudianteId={estudianteId} />
              ) : (
                <Navigate to="/portal" />
              )
            }
          />
          <Route
            path="/estudiante/documentos"
            element={
              estudianteId ? (
                <GestorDocumentos estudianteId={estudianteId} />
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
          <Route
            path="/admin/universidades"
            element={
              isAuthenticated ? (
                <AdminUniversidades />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
          <Route
            path="/admin/programas"
            element={
              isAuthenticated ? (
                <AdminProgramas />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
          <Route path="/blog" element={<BlogLista />} />
          <Route path="/blog/:slug" element={<BlogPost />} />
          <Route path="/testimonios" element={<TestimoniosLista />} />
          <Route
            path="/admin/blog"
            element={
              isAuthenticated ? (
                <AdminBlog />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
          <Route
            path="/admin/testimonios"
            element={
              isAuthenticated ? (
                <AdminTestimonios />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
          <Route
            path="/admin/chats"
            element={
              isAuthenticated ? (
                <AdminChats />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
          <Route
            path="/admin/analytics"
            element={
              isAuthenticated ? (
                <DashboardAnalytics />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
          <Route
            path="/admin/documentos"
            element={
              isAuthenticated ? (
                <AdminDocumentos />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
          <Route
            path="/admin/servicios"
            element={
              isAuthenticated ? (
                <AdminServicios />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
          <Route
            path="/admin/contactar-universidades"
            element={
              isAuthenticated ? (
                <ContactarUniversidades />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
        </Routes>
        
        {/* Chat widget flotante para estudiantes */}
        {estudianteId && <ChatWidget estudianteId={estudianteId} />}
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
    width: '100%',
  },
  navContainer: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: '15px',
  },
  logo: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#667eea',
    textDecoration: 'none',
    whiteSpace: 'nowrap',
  },
  navLinks: {
    display: 'flex',
    gap: '15px',
    flexWrap: 'wrap',
    alignItems: 'center',
  },
  navLink: {
    color: '#2d3748',
    textDecoration: 'none',
    fontWeight: '500',
    fontSize: '14px',
    padding: '8px 12px',
    borderRadius: '5px',
    transition: 'all 0.3s',
    whiteSpace: 'nowrap',
  },
}

export default App
