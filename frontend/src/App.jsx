import React from 'react'
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom'
import RegistroEstudiante from './components/RegistroEstudiante'
import CompletarPerfil from './components/CompletarPerfil'
import LoginEstudiante from './components/LoginEstudiante'
import LoginAdmin from './components/LoginAdmin'
import LoginAgente from './components/LoginAgente'
import DashboardAgente from './components/DashboardAgente'
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
import DashboardAnalytics from './components/DashboardAnalytics'
import GestorDocumentos from './components/GestorDocumentos'
import AdminDocumentos from './components/AdminDocumentos'
import AdminServicios from './components/AdminServicios'
import ContactarUniversidades from './components/ContactarUniversidades'
import PanelProcesoAdmin from './components/PanelProcesoAdmin'
import InformacionFinanciera from './components/InformacionFinanciera'
import InformacionAlojamiento from './components/InformacionAlojamiento'
import InformacionSeguroMedico from './components/InformacionSeguroMedico'
import TesoroAdmin from './components/TesoroAdmin'
import PresupuestosAdmin from './components/PresupuestosAdmin'
import Home from './components/Home'
import Navbar from './components/Navbar'

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(
    !!localStorage.getItem('token')
  )
  const [estudianteId, setEstudianteId] = React.useState(null)

  // Verificar localStorage al cargar y cuando cambie
  React.useEffect(() => {
    const checkAuth = () => {
      const storedId = localStorage.getItem('estudiante_id')
      if (storedId) {
        setEstudianteId(storedId)
      } else {
        setEstudianteId(null)
      }
    }

    checkAuth()

    // Escuchar cambios en localStorage (desde otras pestañas)
    window.addEventListener('storage', checkAuth)

    // Verificar periódicamente (para cambios en la misma pestaña)
    const interval = setInterval(checkAuth, 500)

    return () => {
      window.removeEventListener('storage', checkAuth)
      clearInterval(interval)
    }
  }, [])

  return (
    <BrowserRouter>
      <div className="app">
        <Navbar
          estudianteId={estudianteId}
          isAuthenticated={isAuthenticated}
          setEstudianteId={setEstudianteId}
        />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/estudiante/login" element={<LoginEstudiante />} />
          <Route path="/agente/login" element={<LoginAgente />} />
          <Route path="/dashboard-agente/:agenteId" element={<DashboardAgente />} />
          <Route
            path="/registro"
            element={<RegistroEstudiante onRegistro={(id) => {
              setEstudianteId(id)
              localStorage.setItem('estudiante_id', id)
            }} />}
          />
          <Route
            path="/completar-perfil/:estudianteId"
            element={<CompletarPerfil />}
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
            path="/estudiante/informacion-financiera"
            element={
              estudianteId ? (
                <InformacionFinanciera estudianteId={estudianteId} />
              ) : (
                <Navigate to="/portal" />
              )
            }
          />
          <Route
            path="/estudiante/informacion-alojamiento"
            element={
              estudianteId ? (
                <InformacionAlojamiento estudianteId={estudianteId} />
              ) : (
                <Navigate to="/portal" />
              )
            }
          />
          <Route
            path="/estudiante/informacion-seguro-medico"
            element={
              estudianteId ? (
                <InformacionSeguroMedico estudianteId={estudianteId} />
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
          <Route
            path="/admin/proceso-visa"
            element={
              isAuthenticated ? (
                <PanelProcesoAdmin />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
          <Route
            path="/admin/tesoro"
            element={
              isAuthenticated ? (
                <TesoroAdmin />
              ) : (
                <Navigate to="/admin/login" />
              )
            }
          />
          <Route
            path="/admin/presupuestos"
            element={
              isAuthenticated ? (
                <PresupuestosAdmin />
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

const styles = {}

export default App
