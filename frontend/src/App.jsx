import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import RegistroInversor from './components/RegistroInversor'
import LoginInversor from './components/LoginInversor'
import LoginAdmin from './components/LoginAdmin'
import DashboardAdminExpandido from './components/DashboardAdminExpandido'
import DashboardInversionista from './components/DashboardInversionista'
import OperacionDetalle from './components/OperacionDetalle'
import CatalogoOperaciones from './components/CatalogoOperaciones'
import SolicitudParticipacion from './components/SolicitudParticipacion'
import PerfilInversor from './components/PerfilInversor'
import AdminOperaciones from './components/AdminOperaciones'
import Home from './components/Home'
import Navbar from './components/Navbar'
import ComoFunciona from './components/ComoFunciona'
import PoliticaPrivacidad from './components/PoliticaPrivacidad'
import TerminosCondiciones from './components/TerminosCondiciones'
import Comunidad from './components/Comunidad'
import Programa from './components/Programa'
import ProgramaPartner from './components/ProgramaPartner'
import ProgramaCombinado from './components/ProgramaCombinado'

function SobreNosotros() {
  return (
    <div className="page-shell">
      <div className="page-card">
        <h1>Sobre Nosotros</h1>
        <p style={{ fontSize: '1.2rem', fontWeight: '600', color: '#f6c453' }}>Construimos oportunidades. Creamos comunidad.</p>
        <p>Capital Trade Iberia nace con una visión sencilla: crear una plataforma que conecte personas, oportunidades comerciales y comunidades dentro de un mismo ecosistema.</p>
        <p>Trabajamos con un modelo basado en la gestión de operaciones comerciales y en el desarrollo de una comunidad que pueda crecer junto al proyecto.</p>
        <p>Nuestro objetivo es ofrecer una experiencia clara, organizada y transparente, donde cada usuario pueda gestionar su cuenta, consultar sus movimientos y acceder a los diferentes beneficios disponibles dentro de la plataforma.</p>

        <h2 style={{ marginTop: '2rem' }}>Nuestra comunidad</h2>
        <p>Creemos que el crecimiento no tiene por qué ser individual.</p>
        <p>Por eso hemos desarrollado un Programa de Partners, pensado para personas con capacidad de crear y liderar comunidades. Los Partners pueden desarrollar su propia comunidad dentro de la plataforma y acceder a beneficios especiales, promociones, oportunidades, apoyo para eventos y un Fondo de Comunidad destinado a impulsar el crecimiento de sus comunidades.</p>

        <h2 style={{ marginTop: '2rem' }}>Nuestro enfoque</h2>
        <div className="info-grid">
          <div className="info-box">
            <h3>🔹 Clara</h3>
            <p>Información organizada y fácil de consultar.</p>
          </div>
          <div className="info-box">
            <h3>🔹 Dinámica</h3>
            <p>Con nuevas oportunidades y promociones.</p>
          </div>
          <div className="info-box">
            <h3>🔹 Comunitaria</h3>
            <p>Donde los líderes puedan desarrollar sus propias comunidades.</p>
          </div>
          <div className="info-box">
            <h3>🔹 Orientada al crecimiento</h3>
            <p>Con un sistema de rangos, objetivos y beneficios.</p>
          </div>
        </div>

        <h2 style={{ marginTop: '2rem' }}>Nuestra visión</h2>
        <p>Queremos construir una comunidad internacional alrededor de un ecosistema de oportunidades comerciales, donde usuarios y Partners puedan crecer junto al desarrollo de la plataforma.</p>

        <div style={{ marginTop: '2.5rem', textAlign: 'center', borderTop: '1px solid rgba(246,196,83,0.2)', paddingTop: '2rem' }}>
          <p style={{ fontSize: '1.1rem', fontWeight: '700', color: '#f8fafc' }}>Capital Trade Iberia</p>
          <p style={{ color: '#f6c453', fontWeight: '600' }}>Crece. Conecta. Avanza.</p>
        </div>
      </div>
    </div>
  )
}

function AvisosLegales() {
  return (
    <div className="page-shell">
      <div className="page-card">
        <h1>Avisos legales y condiciones</h1>
        <p>La plataforma está diseñada para presentar información de operaciones comerciales con carácter informativo y de evaluación de interés para el inversor.</p>
        <div className="info-grid">
          <div className="info-box">
            <h3>1. Riesgo financiero</h3>
            <p>Toda operación conlleva riesgo comercial, operativo y de ejecución. No se ofrecen garantías de rentabilidad ni resultados asegurados.</p>
          </div>
          <div className="info-box">
            <h3>2. Transparencia</h3>
            <p>Se informa del capital requerido, tramos disponibles, riesgo estimado y condiciones antes de avanzar en una participación concreta.</p>
          </div>
          <div className="info-box">
            <h3>3. Documentación</h3>
            <p>La documentación de cada operación se revisa y comparte con el inversor antes de cualquier formalización.</p>
          </div>
          <div className="info-box">
            <h3>4. Responsabilidad</h3>
            <p>Las decisiones de inversión deben ser valoradas por cada usuario según su perfil, objetivo y capacidad de asumir riesgos financieros.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

function Faq() {
  const faqs = [
    {
      q: '¿Hay rentabilidad garantizada?',
      a: 'No. Las operaciones tienen condiciones, plazo, riesgo y resultado variables. No se ofrecen rendimientos garantizados ni resultados asegurados. Cada operación se evalúa por sus propias condiciones comerciales.'
    },
    {
      q: '¿Cuál es el capital mínimo para participar?',
      a: 'Depende de la operación concreta y del capital disponible definido para cada tramo. Cada operación indica el capital total requerido y los tramos de participación disponibles.'
    },
    {
      q: '¿Cuándo se conocen las condiciones definitivas?',
      a: 'Se exponen antes de confirmar cualquier participación, junto con el plazo estimado, el nivel de riesgo y la documentación asociada. No se formaliza ninguna participación sin que el inversor conozca y acepte todas las condiciones.'
    },
    {
      q: '¿Cómo puedo participar en una operación?',
      a: 'Regístrate en la plataforma, revisa el catálogo de operaciones disponibles y envía una solicitud de participación. El equipo la revisará y se pondrá en contacto contigo con la información completa.'
    },
    {
      q: '¿Puedo perder el capital que aporto?',
      a: 'Sí. Toda operación comercial conlleva riesgo. El capital puede verse afectado por el resultado operativo, condiciones del mercado o imprevistos en la ejecución. Te recomendamos evaluar cada operación con criterio propio antes de participar.'
    },
    {
      q: '¿En qué tipo de operaciones puedo participar?',
      a: 'Actualmente operamos en exportaciones de alimentos, materiales de construcción, remesas, financiación a MYPIMEs cubanas, participación accionaria y operaciones en mercados internacionales. Consulta el catálogo para ver las operaciones activas.'
    },
    {
      q: '¿Cuánto dura una operación típica?',
      a: 'Los plazos varían según cada operación. Se indica el plazo estimado antes de formalizar la participación. Puedes consultar el estado de cada operación en tiempo real desde tu panel de inversor.'
    },
    {
      q: '¿Cómo se documenta mi participación?',
      a: 'Cada participación queda documentada con un acuerdo o contrato específico que detalla capital, condiciones, plazo y resultado esperado. Toda la documentación es accesible desde tu panel personal.'
    },
    {
      q: '¿Mis datos están seguros?',
      a: 'Sí. Tratamos tus datos conforme al RGPD europeo. Para más información consulta nuestra Política de Privacidad en /privacidad.'
    },
    {
      q: '¿Cómo puedo contactar con el equipo?',
      a: 'Puedes escribirnos a contacto@capitaltradeiberia.com. Respondemos en horario de lunes a viernes, 9:00 a 18:00 (CET).'
    }
  ]

  return (
    <div className="page-shell">
      <div className="page-card">
        <h1>Preguntas frecuentes</h1>
        {faqs.map((item) => (
          <div className="faq-item" key={item.q}>
            <h3>{item.q}</h3>
            <p>{item.a}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

function RiesgosCondiciones() {
  return (
    <div className="page-shell">
      <div className="page-card">
        <h1>Riesgos y condiciones</h1>
        <p>Cada operación se presenta con sus propias condiciones, capital disponible, plazo estimado, riesgo y documentación asociada.</p>
        <ul className="check-list">
          <li>La participación depende de la operación concreta.</li>
          <li>No se ofrecen rentabilidades garantizadas.</li>
          <li>El capital puede estar sujeto a plazos, condiciones y resultado operativo.</li>
          <li>Los datos se mantienen bajo revisión y validación por parte del equipo administrativo.</li>
        </ul>
      </div>
    </div>
  )
}

function Contacto() {
  return (
    <div className="page-shell">
      <div className="page-card">
        <h1>Contacto</h1>
        <p>Solicita información sobre operaciones activas, condiciones de participación y tramos disponibles.</p>
        <div className="contact-box">
          <p><strong>Email:</strong> contacto@capitaltradeiberia.com</p>
          <p><strong>WhatsApp:</strong> +34 677 412 858</p>
          <p><strong>Horario:</strong> Lunes a viernes, 9:00 - 18:00</p>
        </div>
      </div>
    </div>
  )
}

function App() {
  const [currentUser, setCurrentUser] = React.useState(() => {
    try {
      const saved = localStorage.getItem('capital_trade_user')
      return saved ? JSON.parse(saved) : null
    } catch {
      return null
    }
  })

  const isAuthenticated = !!currentUser

  React.useEffect(() => {
    // Interceptor global de enlaces de patrocinador
    const params = new URLSearchParams(window.location.search);
    const ref = params.get('ref');
    if (ref) {
      localStorage.setItem('ref_code', ref);
    }

    const checkAuth = () => {
      try {
        const saved = localStorage.getItem('capital_trade_user')
        setCurrentUser(saved ? JSON.parse(saved) : null)
      } catch {
        setCurrentUser(null)
      }
    }

    checkAuth()
    window.addEventListener('storage', checkAuth)
    window.addEventListener('capital-trade-sync', checkAuth)
    const interval = setInterval(checkAuth, 500)

    return () => {
      window.removeEventListener('storage', checkAuth)
      window.removeEventListener('capital-trade-sync', checkAuth)
      clearInterval(interval)
    }
  }, [])

  return (
    <BrowserRouter>
      <div className="app-shell">
        <Navbar isAuthenticated={isAuthenticated} setCurrentUser={() => setCurrentUser(null)} />
        <Routes>
          {/* RUTAS PÚBLICAS */}
          <Route path="/" element={<Home />} />
          <Route path="/como-funciona" element={<ComoFunciona />} />
          <Route path="/programa" element={<Programa />} />
          <Route path="/programa-partner" element={<ProgramaPartner />} />
          <Route path="/operaciones" element={<CatalogoOperaciones />} />
          <Route path="/sobre-nosotros" element={<SobreNosotros />} />
          <Route path="/aviso-legal" element={<AvisosLegales />} />
          <Route path="/faq" element={<Faq />} />
          <Route path="/riesgos" element={<RiesgosCondiciones />} />
          <Route path="/contacto" element={<Contacto />} />
          <Route path="/privacidad" element={<PoliticaPrivacidad />} />
          <Route path="/terminos" element={<TerminosCondiciones />} />

          {/* RUTAS INVERSOR */}
          {/* RUTAS INVERSOR */}
          <Route path="/login" element={<LoginInversor />} />
          <Route path="/registro" element={<RegistroInversor />} />
          <Route path="/programa-combinado" element={<ProgramaCombinado />} />
          <Route
            path="/dashboard"
            element={isAuthenticated ? <DashboardInversionista /> : <Navigate to="/login" />}
          />
          <Route path="/operacion/:id" element={<OperacionDetalle />} />
          <Route path="/solicitud-participacion" element={<SolicitudParticipacion />} />
          <Route path="/perfil" element={<PerfilInversor />} />
          <Route
            path="/comunidad"
            element={isAuthenticated ? <Comunidad /> : <Navigate to="/login" />}
          />

          {/* RUTAS ADMIN */}
          <Route
            path="/admin/login"
            element={<LoginAdmin onLogin={(userData) => setCurrentUser(userData)} />}
          />
          <Route
            path="/admin"
            element={currentUser?.role === 'admin' ? <DashboardAdminExpandido onLogout={() => setCurrentUser(null)} /> : <Navigate to="/admin/login" />}
          />
          <Route
            path="/admin/operaciones"
            element={currentUser?.role === 'admin' ? <AdminOperaciones /> : <Navigate to="/admin/login" />}
          />

          {/* REDIRECTS */}
          <Route path="/portal" element={<Navigate to="/dashboard" replace />} />

          {/* 404 */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
