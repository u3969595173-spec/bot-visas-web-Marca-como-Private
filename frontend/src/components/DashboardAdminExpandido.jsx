import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import './DashboardAdminExpandido.css'
import PartnersAdmin from './PartnersAdmin'
import AlertasAdmin from './AlertasAdmin'
import GuiaProceso from './GuiaProceso'
import AdminChats from './AdminChats'
import TesoroAdmin from './TesoroAdmin'
import PresupuestosAdmin from './PresupuestosAdmin'

function DashboardAdminExpandido({ onLogout }) {
  const [activeTab, setActiveTab] = useState('estudiantes')
  const activeTabRef = useRef('estudiantes') // Referencia para mantener valor actualizado
  const [estudiantes, setEstudiantes] = useState([])
  const [documentosGenerados, setDocumentosGenerados] = useState([])
  const [cursos, setCursos] = useState([])
  const [alojamientos, setAlojamientos] = useState([])
  const [estadisticas, setEstadisticas] = useState(null)
  const [reporteEstudiantes, setReporteEstudiantes] = useState(null)
  const [alertasDocumentos, setAlertasDocumentos] = useState([])
  const [alertasNoVistas, setAlertasNoVistas] = useState(0)
  const [mostrarAlertas, setMostrarAlertas] = useState(false)
  const [loading, setLoading] = useState(true)
  const [filtro, setFiltro] = useState('todos')
  const [busqueda, setBusqueda] = useState('')
  const [motivoRechazo, setMotivoRechazo] = useState('')
  const [estudianteSeleccionado, setEstudianteSeleccionado] = useState(null)
  const [generandoDocs, setGenerandoDocs] = useState(false)
  const [showAddCursoModal, setShowAddCursoModal] = useState(false)
  const [showAddAlojamientoModal, setShowAddAlojamientoModal] = useState(false)
  const [showCursosSugeridosModal, setShowCursosSugeridosModal] = useState(false)
  const [cursosSugeridos, setCursosSugeridos] = useState([])
  const [estudianteParaCurso, setEstudianteParaCurso] = useState(null)
  const [nuevoCurso, setNuevoCurso] = useState({ nombre: '', descripcion: '', duracion_meses: 6, precio_eur: 0, ciudad: '', nivel_espanol_requerido: '', cupos_disponibles: 0 })
  const [nuevoAlojamiento, setNuevoAlojamiento] = useState({ tipo: '', direccion: '', ciudad: '', precio_mensual_eur: 0, capacidad: 1, disponible: true, descripcion: '', servicios: '' })
  const [showMensajeModal, setShowMensajeModal] = useState(false)
  const [estudianteParaMensaje, setEstudianteParaMensaje] = useState(null)
  const [nuevoMensaje, setNuevoMensaje] = useState({ asunto: '', tipo: 'informacion', mensaje: '', documento_solicitado: '' })
  const [enviandoMensaje, setEnviandoMensaje] = useState(false)
  const [showModalGenerarDocs, setShowModalGenerarDocs] = useState(false)
  const [estudiantesAprobados, setEstudiantesAprobados] = useState([])
  const [showEditarEstudianteModal, setShowEditarEstudianteModal] = useState(false)
  const [estudianteEditar, setEstudianteEditar] = useState(null)
  const [presupuestos, setPresupuestos] = useState([])
  const [showContraofertaModal, setShowContraofertaModal] = useState(false)
  const [presupuestoSeleccionado, setPresupuestoSeleccionado] = useState(null)
  const [contraoferta, setContraoferta] = useState({ 
    precio_al_empezar: '', 
    precio_con_visa: '', 
    precio_financiado: '', 
    comentarios_admin: '' 
  })
  const [referidos, setReferidos] = useState([])
  const [showAjustarCreditoModal, setShowAjustarCreditoModal] = useState(false)
  const [estudianteReferido, setEstudianteReferido] = useState(null)
  const [ajusteCredito, setAjusteCredito] = useState({ credito: 0, tipo_recompensa: 'dinero' })
  const [solicitudesCredito, setSolicitudesCredito] = useState([])
  const [solicitudesFinancieras, setSolicitudesFinancieras] = useState([])
  const [solicitudesAlojamiento, setSolicitudesAlojamiento] = useState([])
  const [solicitudesSeguroMedico, setSolicitudesSeguroMedico] = useState([])
  const [mensajesNoLeidos, setMensajesNoLeidos] = useState(0)
  const navigate = useNavigate()

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  // Sincronizar activeTab con ref
  useEffect(() => {
    activeTabRef.current = activeTab
  }, [activeTab])

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    cargarDatos()
    cargarContadorMensajes() // Cargar contador inicial
    
    // Actualizar contador cada 30 segundos
    const interval = setInterval(cargarContadorMensajes, 30000)
    return () => clearInterval(interval)
  }, [activeTab])

  const cargarContadorMensajes = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${apiUrl}/api/admin/chat/total-no-leidos`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (response.data.success) {
        // Usar ref para obtener valor actual, no el capturado en closure
        if (activeTabRef.current !== 'chat') {
          setMensajesNoLeidos(response.data.total_no_leidos || 0)
        }
      }
    } catch (error) {
      console.error('Error cargando contador de mensajes:', error)
      // No resetear a 0 si hay error, mantener el valor actual
    }
  }

  const cargarDatos = async () => {
    setLoading(true)
    try {
      if (activeTab === 'estudiantes') {
        const [estRes, statsRes] = await Promise.all([
          axios.get(`${apiUrl}/api/admin/estudiantes`),
          axios.get(`${apiUrl}/api/admin/estadisticas`)
        ])
        setEstudiantes(estRes.data)
        setEstadisticas(statsRes.data)
        
        // Cargar alertas de documentos
        try {
          const alertasRes = await axios.get(`${apiUrl}/api/admin/alertas-documentos`)
          const alertas = alertasRes.data.alertas || []
          setAlertasDocumentos(alertas)
          // Solo actualizar contador si no están viendo las alertas actualmente
          if (!mostrarAlertas) {
            setAlertasNoVistas(alertas.length)
          }
        } catch (err) {
          console.error('Error cargando alertas:', err)
        }
      } else if (activeTab === 'documentos') {
        try {
          const docsRes = await axios.get(`${apiUrl}/api/admin/documentos-generados`)
          console.log('Documentos cargados:', docsRes.data)
          setDocumentosGenerados(Array.isArray(docsRes.data) ? docsRes.data : [])
        } catch (err) {
          console.error('Error cargando documentos:', err)
          setDocumentosGenerados([])
          alert('Error al cargar documentos: ' + (err.response?.data?.detail || err.message))
        }
      } else if (activeTab === 'cursos') {
        const cursosRes = await axios.get(`${apiUrl}/api/admin/cursos`)
        setCursos(cursosRes.data)
      } else if (activeTab === 'alojamientos') {
        const alojRes = await axios.get(`${apiUrl}/api/admin/alojamientos`)
        setAlojamientos(alojRes.data)
      } else if (activeTab === 'reportes') {
        const reporteRes = await axios.get(`${apiUrl}/api/admin/reportes/estudiantes`)
        setReporteEstudiantes(reporteRes.data)
      } else if (activeTab === 'presupuestos') {
        const presRes = await axios.get(`${apiUrl}/api/admin/presupuestos`)
        setPresupuestos(presRes.data)
      } else if (activeTab === 'trabajos') {
        const presRes = await axios.get(`${apiUrl}/api/admin/presupuestos`)
        setPresupuestos(presRes.data)
      } else if (activeTab === 'referidos') {
        const [refRes, solRes] = await Promise.all([
          axios.get(`${apiUrl}/api/admin/referidos`),
          axios.get(`${apiUrl}/api/admin/solicitudes-credito`)
        ])
        setReferidos(refRes.data)
        setSolicitudesCredito(solRes.data)
      } else if (activeTab === 'informacion-financiera') {
        const response = await axios.get(`${apiUrl}/api/admin/solicitudes-financieras`)
        setSolicitudesFinancieras(response.data)
      } else if (activeTab === 'informacion-alojamiento') {
        const response = await axios.get(`${apiUrl}/api/admin/solicitudes-alojamiento`)
        setSolicitudesAlojamiento(response.data)
      } else if (activeTab === 'informacion-seguro-medico') {
        const response = await axios.get(`${apiUrl}/api/admin/solicitudes-seguro-medico`)
        setSolicitudesSeguroMedico(response.data)
      }
    } catch (err) {
      console.error('Error:', err)
      if (err.response?.status === 401) {
        handleLogout()
      }
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('usuario')
    delete axios.defaults.headers.common['Authorization']
    onLogout()
    navigate('/admin/login')
  }

  const aprobarEstudiante = async (id) => {
    // Primero mostrar cursos sugeridos
    try {
      const res = await axios.get(`${apiUrl}/api/admin/estudiantes/${id}/sugerir-cursos`)
      setCursosSugeridos(res.data.cursos_sugeridos)
      setEstudianteParaCurso(id)
      setShowCursosSugeridosModal(true)
    } catch (err) {
      // Si no hay cursos o falla, aprobar directamente
      if (confirm('¿Está seguro de aprobar este estudiante sin asignar curso?')) {
        try {
          await axios.post(`${apiUrl}/api/admin/estudiantes/${id}/aprobar`)
          alert('Estudiante aprobado correctamente')
          cargarDatos()
        } catch (err2) {
          alert('Error: ' + (err2.response?.data?.detail || err2.message))
        }
      }
    }
  }

  const aprobarConCurso = async (cursoId = null) => {
    try {
      // Asignar curso si fue seleccionado
      if (cursoId) {
        await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteParaCurso}/asignar-curso`, null, {
          params: { curso_id: cursoId }
        })
      }
      
      // Aprobar estudiante
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteParaCurso}/aprobar`)
      
      alert('Estudiante aprobado' + (cursoId ? ' y curso asignado' : ''))
      setShowCursosSugeridosModal(false)
      setCursosSugeridos([])
      setEstudianteParaCurso(null)
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const rechazarEstudiante = async (id) => {
    setEstudianteSeleccionado(id)
  }

  const confirmarRechazo = async () => {
    if (!motivoRechazo.trim()) {
      alert('Por favor ingrese un motivo de rechazo')
      return
    }

    try {
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteSeleccionado}/rechazar`, {
        motivo: motivoRechazo
      })
      alert('Estudiante rechazado')
      setEstudianteSeleccionado(null)
      setMotivoRechazo('')
      cargarDatos()
    } catch (err) {
      alert('Error al rechazar estudiante: ' + (err.response?.data?.detail || err.message))
    }
  }

  const responderSolicitudCredito = async (solicitudId, accion) => {
    const solicitud = solicitudesCredito.find(s => s.id === solicitudId)
    if (!solicitud) return

    const textoAccion = accion === 'aprobar' ? 'APROBAR' : 'RECHAZAR'
    const textoTipo = solicitud.tipo === 'retiro' ? 'retiro de dinero' : 'descuento en trámite'
    
    if (!confirm(`¿${textoAccion} solicitud de ${textoTipo} por ${solicitud.monto.toFixed(2)}€ de ${solicitud.nombre}?`)) {
      return
    }

    try {
      await axios.put(`${apiUrl}/api/admin/solicitudes-credito/${solicitudId}/responder`, {
        accion: accion
      })
      
      alert(`✅ Solicitud ${accion === 'aprobar' ? 'APROBADA' : 'RECHAZADA'} exitosamente`)
      cargarDatos()
    } catch (err) {
      alert('❌ Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const estudiantesFiltrados = estudiantes.filter(est => {
    // Normalizar estado (puede venir como 'estado' o 'estado_procesamiento')
    const estadoActual = est.estado || est.estado_procesamiento || 'pendiente'
    const cumpleFiltro = filtro === 'todos' || estadoActual === filtro
    const cumpleBusqueda = !busqueda || 
      est.nombre?.toLowerCase().includes(busqueda.toLowerCase()) ||
      est.nombre_completo?.toLowerCase().includes(busqueda.toLowerCase()) ||
      est.email?.toLowerCase().includes(busqueda.toLowerCase()) ||
      est.especialidad?.toLowerCase().includes(busqueda.toLowerCase()) ||
      est.especialidad_interes?.toLowerCase().includes(busqueda.toLowerCase())
    
    return cumpleFiltro && cumpleBusqueda
  })

  const generarDocumentos = async (estudianteId) => {
    if (!confirm('¿Generar todos los documentos oficiales para este estudiante?')) return
    
    setGenerandoDocs(true)
    try {
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteId}/generar-documentos`, {
        tipos_documentos: ['carta_motivacion', 'formulario_solicitud', 'declaracion_jurada_fondos', 'carta_patrocinio']
      })
      alert('✅ Documentos generados correctamente')
      setShowModalGenerarDocs(false)
      setActiveTab('documentos')
      cargarDatos()
    } catch (err) {
      alert('Error al generar documentos: ' + (err.response?.data?.detail || err.message))
    } finally {
      setGenerandoDocs(false)
    }
  }

  const abrirModalGenerarDocs = () => {
    // Filtrar solo estudiantes aprobados
    const aprobados = estudiantes.filter(est => 
      est.estado === 'aprobado' || 
      est.estado === 'aprobado_admin' ||
      est.estado_procesamiento === 'aprobado'
    )
    setEstudiantesAprobados(aprobados)
    setShowModalGenerarDocs(true)
  }

  const aprobarDocumento = async (docId) => {
    if (!confirm('¿Aprobar este documento y enviarlo al estudiante?')) return
    
    try {
      await axios.put(`${apiUrl}/api/admin/documentos-generados/${docId}/aprobar`, {
        enviar_a_estudiante: true
      })
      alert('Documento aprobado y enviado')
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const descargarDocumento = async (docId) => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(
        `${apiUrl}/api/admin/documentos-generados/${docId}/descargar`,
        {
          headers: { Authorization: `Bearer ${token}` },
          responseType: 'blob'
        }
      )
      
      // Crear URL del blob y descargar
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      
      // Obtener nombre del archivo del header Content-Disposition
      const contentDisposition = response.headers['content-disposition']
      let filename = 'documento.pdf'
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/)
        if (filenameMatch) filename = filenameMatch[1]
      }
      
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      alert('Error al descargar: ' + (err.response?.data?.detail || err.message))
    }
  }

  const eliminarDocumento = async (docId, tipoDoc) => {
    if (!confirm(`¿Eliminar documento "${tipoDoc}"?`)) return
    
    try {
      await axios.delete(`${apiUrl}/api/admin/documentos-generados/${docId}`)
      alert('✅ Documento eliminado correctamente')
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const eliminarDuplicados = async (estudianteId = null) => {
    const mensaje = estudianteId 
      ? '¿Eliminar documentos duplicados de este estudiante?' 
      : '⚠️ ¿Eliminar TODOS los documentos duplicados del sistema? (Mantiene solo el más reciente de cada tipo)'
    
    if (!confirm(mensaje)) return
    
    try {
      const url = estudianteId 
        ? `${apiUrl}/api/admin/documentos-generados/duplicados/eliminar?estudiante_id=${estudianteId}`
        : `${apiUrl}/api/admin/documentos-generados/duplicados/eliminar`
      
      const res = await axios.delete(url)
      alert(`✅ ${res.data.mensaje}\n\nEliminados: ${res.data.count}`)
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const abrirModalMensaje = (estudiante) => {
    setEstudianteParaMensaje(estudiante)
    setNuevoMensaje({ 
      asunto: `Mensaje para ${estudiante.nombre || estudiante.nombre_completo}`, 
      tipo: 'informacion', 
      mensaje: '', 
      documento_solicitado: '' 
    })
    setShowMensajeModal(true)
  }

  const abrirModalEditarEstudiante = (estudiante) => {
    setEstudianteEditar({...estudiante})
    setShowEditarEstudianteModal(true)
  }

  const guardarEstudiante = async () => {
    try {
      await axios.put(`${apiUrl}/api/admin/estudiantes/${estudianteEditar.id}`, estudianteEditar)
      alert('✅ Estudiante actualizado correctamente')
      setShowEditarEstudianteModal(false)
      cargarDatos()
    } catch (err) {
      alert('Error al actualizar: ' + (err.response?.data?.detail || err.message))
    }
  }

  const enviarMensaje = async () => {
    if (!nuevoMensaje.mensaje.trim()) {
      alert('El mensaje no puede estar vacío')
      return
    }

    setEnviandoMensaje(true)
    try {
      const response = await axios.post(
        `${apiUrl}/api/admin/estudiantes/${estudianteParaMensaje.id}/enviar-mensaje`,
        nuevoMensaje
      )
      
      alert(`✅ Mensaje enviado correctamente${response.data.email_enviado ? ' y notificación por email enviada' : ''}`)
      setShowMensajeModal(false)
      setEstudianteParaMensaje(null)
      setNuevoMensaje({ asunto: '', tipo: 'informacion', mensaje: '', documento_solicitado: '' })
    } catch (err) {
      alert('Error al enviar mensaje: ' + (err.response?.data?.detail || err.message))
    } finally {
      setEnviandoMensaje(false)
    }
  }

  const crearCurso = async () => {
    try {
      await axios.post(`${apiUrl}/api/admin/cursos`, nuevoCurso)
      alert('Curso creado correctamente')
      setShowAddCursoModal(false)
      setNuevoCurso({ nombre: '', descripcion: '', duracion_meses: 6, precio_eur: 0, ciudad: '', nivel_espanol_requerido: '', cupos_disponibles: 0 })
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const crearAlojamiento = async () => {
    try {
      await axios.post(`${apiUrl}/api/admin/alojamientos`, nuevoAlojamiento)
      alert('Alojamiento creado correctamente')
      setShowAddAlojamientoModal(false)
      setNuevoAlojamiento({ tipo: '', direccion: '', ciudad: '', precio_mensual_eur: 0, capacidad: 1, disponible: true, descripcion: '', servicios: '' })
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const asignarCurso = async (estudianteId, cursoId) => {
    try {
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteId}/asignar-curso`, null, {
        params: { curso_id: cursoId }
      })
      alert('Curso asignado correctamente')
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const asignarAlojamiento = async (estudianteId, alojamientoId) => {
    try {
      await axios.post(`${apiUrl}/api/admin/estudiantes/${estudianteId}/asignar-alojamiento`, null, {
        params: { alojamiento_id: alojamientoId }
      })
      alert('Alojamiento asignado correctamente')
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const enviarRecordatorios = async () => {
    if (!confirm('¿Enviar recordatorios a todos los estudiantes con documentos pendientes?')) return
    
    try {
      const res = await axios.post(`${apiUrl}/api/admin/enviar-recordatorios`)
      alert(res.data.mensaje)
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const gestionarPatrocinio = async (estudianteId, decision) => {
    const accion = decision === 'aceptado' ? 'aprobar' : 'rechazar'
    const mensaje = decision === 'aceptado' ? 
      '¿Aprobar la solicitud de gestión de patrocinio? El estudiante será notificado.' :
      '¿Rechazar la solicitud de gestión de patrocinio? El estudiante será notificado.'

    if (!confirm(mensaje)) return

    const comentarios = prompt('Comentarios adicionales (opcional):') || ''

    try {
      await axios.put(`${apiUrl}/api/admin/gestionar-patrocinio/${estudianteId}`, {
        accion: accion,
        comentarios: comentarios
      })
      
      alert(`Solicitud ${decision === 'aceptado' ? 'aprobada' : 'rechazada'} correctamente. El estudiante ha sido notificado.`)
      cargarDatos() // Recargar datos para actualizar la tabla
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const gestionarAlojamiento = async (estudianteId, decision) => {
    const accion = decision === 'aceptado' ? 'aprobar' : 'rechazar'
    const mensaje = decision === 'aceptado' ? 
      '¿Aprobar la solicitud de gestión de alojamiento? El estudiante será notificado.' :
      '¿Rechazar la solicitud de gestión de alojamiento? El estudiante será notificado.'

    if (!confirm(mensaje)) return

    const comentarios = prompt('Comentarios adicionales (opcional):') || ''

    try {
      await axios.put(`${apiUrl}/api/admin/gestionar-alojamiento/${estudianteId}`, {
        accion: accion,
        comentarios: comentarios
      })
      
      alert(`Solicitud ${decision === 'aceptado' ? 'aprobada' : 'rechazada'} correctamente. El estudiante ha sido notificado.`)
      cargarDatos() // Recargar datos para actualizar la tabla
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const gestionarSeguroMedico = async (estudianteId, decision) => {
    const accion = decision === 'aceptado' ? 'aprobar' : 'rechazar'
    const mensaje = decision === 'aceptado' ? 
      '¿Aprobar la solicitud de gestión de seguro médico? El estudiante será notificado.' :
      '¿Rechazar la solicitud de gestión de seguro médico? El estudiante será notificado.'

    if (!confirm(mensaje)) return

    const comentarios = prompt('Comentarios adicionales (opcional):') || ''

    try {
      await axios.put(`${apiUrl}/api/admin/gestionar-seguro-medico/${estudianteId}`, {
        accion: accion,
        comentarios: comentarios
      })
      
      alert(`Solicitud ${decision === 'aceptado' ? 'aprobada' : 'rechazada'} correctamente. El estudiante ha sido notificado.`)
      cargarDatos() // Recargar datos para actualizar la tabla
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const actualizarEstadoEstudiante = async (estudianteId, nuevoEstado) => {
    try {
      await axios.put(`${apiUrl}/api/admin/estudiantes/${estudianteId}/actualizar-estado`, null, {
        params: { nuevo_estado: nuevoEstado }
      })
      alert('Estado actualizado correctamente')
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  const sincronizarCursosEscuelas = async () => {
    if (!confirm('¿Sincronizar cursos desde APIs de escuelas? Esto actualizará precios y disponibilidad.')) return
    
    setLoading(true)
    try {
      const res = await axios.get(`${apiUrl}/api/admin/sincronizar-cursos-escuelas`)
      alert(`✅ Sincronización completada!\n\n` +
            `📚 Cursos encontrados: ${res.data.cursos_encontrados}\n` +
            `➕ Cursos nuevos insertados: ${res.data.cursos_insertados}\n` +
            `🔄 Cursos actualizados: ${res.data.cursos_actualizados}`)
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    } finally {
      setLoading(false)
    }
  }

  const verificarDisponibilidadCurso = async (cursoId) => {
    try {
      const res = await axios.get(`${apiUrl}/api/cursos/${cursoId}/verificar-disponibilidad`)
      alert(`Disponibilidad verificada:\n\n` +
            `📚 ${res.data.nombre}\n` +
            `🎫 Cupos disponibles: ${res.data.cupos_disponibles}\n` +
            `${res.data.disponible ? '✅ Curso disponible' : '❌ Sin cupos'}`)
      cargarDatos()
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  if (loading) {
    return <div className="loading">Cargando...</div>
  }

  return (
    <div className="dashboard-admin-expandido">
      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h1>Panel de Administración</h1>
          <p className="bienvenida">Bienvenido, {localStorage.getItem('usuario')}</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          {/* Campana de Alertas */}
          {alertasDocumentos.length > 0 && (
            <div className="notification-bell" onClick={() => {
              setMostrarAlertas(!mostrarAlertas)
              // Marcar como vistas al abrir el panel
              if (!mostrarAlertas) {
                setAlertasNoVistas(0)
              }
            }}>
              <div className="bell-icon">
                🔔
                {alertasNoVistas > 0 && (
                  <span className="notification-badge">{alertasNoVistas}</span>
                )}
              </div>
            </div>
          )}
          
          {/* Botón Chat con contador */}
          <div 
            className="notification-bell" 
            onClick={() => {
              setMensajesNoLeidos(0) // Resetear contador ANTES de cambiar tab
              setActiveTab('chat')
            }}
            style={{ cursor: 'pointer' }}
          >
            <div className="bell-icon">
              💬
              {mensajesNoLeidos > 0 && (
                <span className="notification-badge">
                  {mensajesNoLeidos > 99 ? '99+' : mensajesNoLeidos}
                </span>
              )}
            </div>
          </div>
          
          <button onClick={handleLogout} className="btn-logout">
            Cerrar Sesión
          </button>
        </div>
      </div>

      {/* Panel de Alertas - Solo se muestra cuando se hace clic */}
      {mostrarAlertas && alertasDocumentos.length > 0 && (
        <div className="alertas-panel-floating">
          <div className="alertas-header">
            <h3>⚠️ Alertas de Documentación ({alertasDocumentos.length})</h3>
            <button className="btn-close-alerts" onClick={() => setMostrarAlertas(false)}>✕</button>
          </div>
          <div className="alertas-content">
            <div className="alertas-acciones">
              <button onClick={enviarRecordatorios} className="btn-recordatorios">
                📧 Enviar Recordatorios Masivos
              </button>
            </div>
            <div className="alertas-lista">
              {alertasDocumentos.map(alerta => (
                <div key={alerta.estudiante_id} className={`alerta-item urgencia-${alerta.urgencia}`}>
                  <div className="alerta-info">
                    <strong>{alerta.nombre}</strong>
                    <span className="alerta-estado">{alerta.estado}</span>
                  </div>
                  <div className="alerta-detalles">
                    <span>📄 {alerta.docs_subidos}/3 docs subidos</span>
                    <span>✓ {alerta.docs_generados}/4 docs generados</span>
                    <span>🕐 {alerta.dias_desde_registro} días</span>
                  </div>
                  <span className={`badge-urgencia ${alerta.urgencia}`}>
                    {alerta.urgencia.toUpperCase()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="tabs-container">
        <button 
          className={`tab ${activeTab === 'estudiantes' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('estudiantes')}
          style={{ background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)', color: 'white', fontWeight: 'bold' }}
        >
          👥 Estudiantes
        </button>
        <button 
          className={`tab ${activeTab === 'documentos' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('documentos')}
          style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)', color: 'white', fontWeight: 'bold' }}
        >
          📄 Documentos Generados
        </button>
        <button 
          className={`tab ${activeTab === 'informacion-financiera' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('informacion-financiera')}
          style={{ background: 'linear-gradient(135deg, #ec4899 0%, #be185d 100%)', color: 'white', fontWeight: 'bold' }}
        >
          💸 Información Financiera
        </button>
        <button 
          className={`tab ${activeTab === 'informacion-alojamiento' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('informacion-alojamiento')}
          style={{ background: 'linear-gradient(135deg, #059669 0%, #047857 100%)', color: 'white', fontWeight: 'bold' }}
        >
          🏠 Gestión de Alojamiento
        </button>
        <button 
          className={`tab ${activeTab === 'informacion-seguro-medico' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('informacion-seguro-medico')}
          style={{ background: 'linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%)', color: 'white', fontWeight: 'bold' }}
        >
          🏥 Seguro Médico
        </button>
        <button 
          className={`tab ${activeTab === 'servicios' ? 'tab-active' : ''}`}
          onClick={() => navigate('/admin/servicios')}
          style={{ background: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)', color: 'white', fontWeight: 'bold' }}
        >
          💼 Servicios Solicitados
        </button>
        <button 
          className="tab"
          onClick={() => navigate('/admin/contactar-universidades')}
          style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', fontWeight: 'bold' }}
        >
          🏛️ Contactar Universidades
        </button>
        <button 
          className="tab"
          onClick={() => navigate('/admin/proceso-visa')}
          style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white', fontWeight: 'bold' }}
        >
          📊 Proceso de Visa (Tracking)
        </button>
        <button 
          className={`tab ${activeTab === 'alertas' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('alertas')}
          style={{ background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)', color: 'white', fontWeight: 'bold' }}
        >
          📅 Alertas de Fechas
        </button>
        <button 
          className={`tab ${activeTab === 'cursos' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('cursos')}
          style={{ background: 'linear-gradient(135deg, #84cc16 0%, #65a30d 100%)', color: 'white', fontWeight: 'bold' }}
        >
          📚 Cursos
        </button>
        <button 
          className={`tab ${activeTab === 'alojamientos' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('alojamientos')}
          style={{ background: 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)', color: 'white', fontWeight: 'bold' }}
        >
          🏠 Alojamientos
        </button>
        <button 
          className={`tab ${activeTab === 'partners' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('partners')}
          style={{ background: 'linear-gradient(135deg, #6366f1 0%, #4338ca 100%)', color: 'white', fontWeight: 'bold' }}
        >
          🤝 Partnerships
        </button>
        <button 
          className={`tab ${activeTab === 'guia' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('guia')}
          style={{ background: 'linear-gradient(135deg, #38b2ac 0%, #2c7a7b 100%)', color: 'white', fontWeight: 'bold' }}
        >
          📋 Guía del Proceso
        </button>
        <button 
          className={`tab ${activeTab === 'presupuestos' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('presupuestos')}
          style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', color: 'white', fontWeight: 'bold' }}
        >
          💰 Presupuestos
        </button>
        <button 
          className={`tab ${activeTab === 'tesoro' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('tesoro')}
          style={{ background: 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)', color: 'white', fontWeight: 'bold' }}
        >
          💎 Tesoro
        </button>
        <button 
          className={`tab ${activeTab === 'trabajos' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('trabajos')}
          style={{ background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', color: 'white', fontWeight: 'bold' }}
        >
          🎯 Trabajos Activos
        </button>
        <button 
          className={`tab ${activeTab === 'referidos' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('referidos')}
          style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white', fontWeight: 'bold' }}
        >
          💎 Referidos
        </button>
        <button 
          className={`tab ${activeTab === 'reportes' ? 'tab-active' : ''}`}
          onClick={() => setActiveTab('reportes')}
          style={{ background: 'linear-gradient(135deg, #64748b 0%, #475569 100%)', color: 'white', fontWeight: 'bold' }}
        >
          📊 Reportes
        </button>
      </div>

      {/* SECCIÓN: CHAT CON ESTUDIANTES */}
      {activeTab === 'chat' && (
        <div style={{margin: '-20px'}}>
          <AdminChats />
        </div>
      )}

      {/* SECCIÓN: PARTNERSHIPS */}
      {activeTab === 'partners' && <PartnersAdmin />}

      {/* SECCIÓN: ALERTAS DE FECHAS */}
      {activeTab === 'alertas' && <AlertasAdmin apiUrl={apiUrl} />}

      {/* SECCIÓN: GUÍA DEL PROCESO */}
      {activeTab === 'guia' && <GuiaProceso />}

      {/* SECCIÓN: PRESUPUESTOS */}
      {activeTab === 'presupuestos' && (
        <div style={{margin: '-20px'}}>
          <PresupuestosAdmin embedded={true} />
        </div>
      )}

      {/* SECCIÓN: TESORO */}
      {activeTab === 'tesoro' && (
        <div style={{margin: '-20px'}}>
          <TesoroAdmin embedded={true} />
        </div>
      )}

      {/* SECCIÓN: TRABAJOS ACTIVOS (Presupuestos Aceptados) */}
      {activeTab === 'trabajos' && (
        <div className="card">
          <h2 style={{marginBottom: '20px', color: '#1f2937'}}>🎯 Trabajos Activos - Presupuestos Aceptados</h2>
          
          {presupuestos.filter(p => p.estado === 'aceptado').length === 0 ? (
            <div style={{textAlign: 'center', padding: '60px', color: '#6b7280'}}>
              <div style={{fontSize: '48px', marginBottom: '15px'}}>📭</div>
              <p style={{fontSize: '18px'}}>No hay trabajos activos</p>
              <p style={{fontSize: '14px'}}>Los presupuestos aceptados aparecerán aquí</p>
            </div>
          ) : (
            <div style={{display: 'grid', gap: '20px'}}>
              {presupuestos.filter(p => p.estado === 'aceptado').map(trabajo => (
                <div key={trabajo.id} style={{
                  backgroundColor: '#ffffff',
                  border: '2px solid #f59e0b',
                  borderRadius: '10px',
                  padding: '25px',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                }}>
                  {/* Header del trabajo */}
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '20px',
                    paddingBottom: '15px',
                    borderBottom: '2px solid #fef3c7'
                  }}>
                    <div>
                      <h3 style={{margin: '0 0 8px 0', color: '#1f2937', fontSize: '20px'}}>
                        {trabajo.nombre_estudiante}
                      </h3>
                      <div style={{display: 'flex', gap: '15px', fontSize: '14px', color: '#6b7280'}}>
                        <span>📧 {trabajo.email_estudiante}</span>
                        {trabajo.telefono_estudiante && <span>📱 {trabajo.telefono_estudiante}</span>}
                      </div>
                    </div>
                    <div style={{textAlign: 'right'}}>
                      <div style={{fontSize: '32px', fontWeight: '700', color: '#f59e0b'}}>
                        {trabajo.precio_ofertado}€
                      </div>
                      <div style={{fontSize: '13px', color: '#6b7280'}}>
                        {trabajo.forma_pago}
                      </div>
                    </div>
                  </div>

                  {/* Servicios contratados */}
                  <div style={{marginBottom: '20px'}}>
                    <h4 style={{margin: '0 0 12px 0', color: '#1f2937', fontSize: '16px'}}>
                      📦 Servicios Contratados:
                    </h4>
                    <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '10px'}}>
                      {Array.isArray(trabajo.servicios) && trabajo.servicios.map((servicio, idx) => {
                        const nombres = {
                          'gestion_visa': 'Gestión completa de visa',
                          'busqueda_universidad': 'Búsqueda de universidad',
                          'carta_aceptacion': 'Gestión carta aceptación',
                          'seguro_medico': 'Seguro médico',
                          'busqueda_vivienda': 'Búsqueda de vivienda',
                          'traduccion_documentos': 'Traducción documentos',
                          'apostilla': 'Apostilla documentos',
                          'asesoria_bancaria': 'Asesoría bancaria',
                          'preparacion_entrevista': 'Preparación entrevista',
                          'tramite_urgente': 'Trámite urgente'
                        };
                        return (
                          <div key={idx} style={{
                            backgroundColor: '#fef3c7',
                            padding: '8px 12px',
                            borderRadius: '6px',
                            fontSize: '13px',
                            fontWeight: '500',
                            color: '#92400e',
                            border: '1px solid #fde68a'
                          }}>
                            ✓ {nombres[servicio] || servicio}
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Checklist de tareas */}
                  <div style={{
                    backgroundColor: '#f9fafb',
                    padding: '20px',
                    borderRadius: '8px',
                    border: '1px solid #e5e7eb'
                  }}>
                    <h4 style={{margin: '0 0 15px 0', color: '#1f2937', fontSize: '16px'}}>
                      ✅ Tareas Pendientes:
                    </h4>
                    <div style={{display: 'grid', gap: '10px'}}>
                      {trabajo.servicios.includes('gestion_visa') && (
                        <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '8px', backgroundColor: 'white', borderRadius: '5px'}}>
                          <input type="checkbox" style={{marginRight: '10px', width: '18px', height: '18px'}} />
                          <span style={{fontSize: '14px'}}>Revisar documentación del estudiante</span>
                        </label>
                      )}
                      {trabajo.servicios.includes('gestion_visa') && (
                        <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '8px', backgroundColor: 'white', borderRadius: '5px'}}>
                          <input type="checkbox" style={{marginRight: '10px', width: '18px', height: '18px'}} />
                          <span style={{fontSize: '14px'}}>Preparar formularios de visa</span>
                        </label>
                      )}
                      {trabajo.servicios.includes('busqueda_universidad') && (
                        <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '8px', backgroundColor: 'white', borderRadius: '5px'}}>
                          <input type="checkbox" style={{marginRight: '10px', width: '18px', height: '18px'}} />
                          <span style={{fontSize: '14px'}}>Buscar universidades según perfil</span>
                        </label>
                      )}
                      {trabajo.servicios.includes('busqueda_universidad') && (
                        <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '8px', backgroundColor: 'white', borderRadius: '5px'}}>
                          <input type="checkbox" style={{marginRight: '10px', width: '18px', height: '18px'}} />
                          <span style={{fontSize: '14px'}}>Enviar opciones al estudiante</span>
                        </label>
                      )}
                      {trabajo.servicios.includes('seguro_medico') && (
                        <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '8px', backgroundColor: 'white', borderRadius: '5px'}}>
                          <input type="checkbox" style={{marginRight: '10px', width: '18px', height: '18px'}} />
                          <span style={{fontSize: '14px'}}>Cotizar seguro médico</span>
                        </label>
                      )}
                      {trabajo.servicios.includes('busqueda_vivienda') && (
                        <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '8px', backgroundColor: 'white', borderRadius: '5px'}}>
                          <input type="checkbox" style={{marginRight: '10px', width: '18px', height: '18px'}} />
                          <span style={{fontSize: '14px'}}>Buscar opciones de alojamiento</span>
                        </label>
                      )}
                      {trabajo.servicios.includes('traduccion_documentos') && (
                        <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '8px', backgroundColor: 'white', borderRadius: '5px'}}>
                          <input type="checkbox" style={{marginRight: '10px', width: '18px', height: '18px'}} />
                          <span style={{fontSize: '14px'}}>Gestionar traducción oficial</span>
                        </label>
                      )}
                      {trabajo.servicios.includes('apostilla') && (
                        <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '8px', backgroundColor: 'white', borderRadius: '5px'}}>
                          <input type="checkbox" style={{marginRight: '10px', width: '18px', height: '18px'}} />
                          <span style={{fontSize: '14px'}}>Tramitar apostilla de documentos</span>
                        </label>
                      )}
                      <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '8px', backgroundColor: 'white', borderRadius: '5px'}}>
                        <input type="checkbox" style={{marginRight: '10px', width: '18px', height: '18px'}} />
                        <span style={{fontSize: '14px'}}>Contactar al estudiante para siguiente paso</span>
                      </label>
                      <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '8px', backgroundColor: 'white', borderRadius: '5px'}}>
                        <input type="checkbox" style={{marginRight: '10px', width: '18px', height: '18px'}} />
                        <span style={{fontSize: '14px'}}>Enviar actualización de progreso</span>
                      </label>
                    </div>
                  </div>

                  {/* Botón de ver perfil completo */}
                  <div style={{marginTop: '20px', display: 'flex', gap: '10px'}}>
                    <button
                      onClick={() => {
                        setActiveTab('estudiantes');
                        // Aquí podrías hacer scroll al estudiante específico
                      }}
                      style={{
                        padding: '10px 20px',
                        backgroundColor: '#3b82f6',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '500'
                      }}
                    >
                      👤 Ver Perfil Completo
                    </button>
                    <button
                      onClick={() => {
                        alert(`Trabajo marcado como completado para ${trabajo.nombre_estudiante}`);
                        // Aquí podrías agregar lógica para cambiar el estado
                      }}
                      style={{
                        padding: '10px 20px',
                        backgroundColor: '#10b981',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '500'
                      }}
                    >
                      ✅ Marcar como Completado
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* SECCIÓN: INFORMACIÓN FINANCIERA */}
      {activeTab === 'informacion-financiera' && (
        <div className="card">
          <div className="section-header">
            <h2>💸 Información Financiera</h2>
            <div style={{fontSize: '14px', color: '#718096'}}>
              Estudiantes que solicitaron gestión de patrocinio
            </div>
          </div>

          {solicitudesFinancieras.length === 0 ? (
            <div className="no-data">
              <p>📭 No hay solicitudes de gestión de patrocinio</p>
            </div>
          ) : (
            <div className="tabla-wrapper">
              <table className="tabla-estudiantes">
                <thead>
                  <tr>
                    <th>Estudiante</th>
                    <th>Email</th>
                    <th>Fondos Disponibles</th>
                    <th>Patrocinador</th>
                    <th>Estado Solicitud</th>
                    <th>Fecha Solicitud</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {solicitudesFinancieras.map((estudiante) => (
                    <tr key={estudiante.id}>
                      <td>
                        <div style={{fontWeight: '600'}}>{estudiante.nombre}</div>
                        <div style={{fontSize: '12px', color: '#666'}}>{estudiante.nacionalidad}</div>
                      </td>
                      <td>{estudiante.email}</td>
                      <td>
                        <div style={{fontWeight: '600', color: '#1f2937'}}>
                          {estudiante.fondos_disponibles} {estudiante.moneda_fondos || 'EUR'}
                        </div>
                      </td>
                      <td>
                        {estudiante.tiene_patrocinador ? (
                          <div>
                            <div style={{fontSize: '12px', fontWeight: '600', color: '#10b981'}}>✅ Sí tiene</div>
                            <div style={{fontSize: '11px', color: '#666'}}>{estudiante.nombre_patrocinador}</div>
                            <div style={{fontSize: '11px', color: '#666'}}>{estudiante.relacion_patrocinador}</div>
                          </div>
                        ) : (
                          <span style={{color: '#ef4444'}}>❌ No tiene</span>
                        )}
                      </td>
                      <td>
                        <span style={{
                          padding: '4px 8px',
                          borderRadius: '6px',
                          fontSize: '12px',
                          fontWeight: '600',
                          backgroundColor: 
                            estudiante.estado_patrocinio === 'aprobado' ? '#d1fae5' :
                            estudiante.estado_patrocinio === 'rechazado' ? '#fee2e2' : '#fef3c7',
                          color:
                            estudiante.estado_patrocinio === 'aprobado' ? '#065f46' :
                            estudiante.estado_patrocinio === 'rechazado' ? '#dc2626' : '#92400e'
                        }}>
                          {estudiante.estado_patrocinio === 'aprobado' ? '✅ Aceptado' :
                           estudiante.estado_patrocinio === 'rechazado' ? '❌ Rechazado' : '⏳ Pendiente'}
                        </span>
                      </td>
                      <td>
                        {estudiante.fecha_solicitud && estudiante.fecha_solicitud !== 'Invalid Date' ? 
                          new Date(estudiante.fecha_solicitud).toLocaleDateString('es-ES') : 
                          'Fecha no disponible'
                        }
                      </td>
                      <td>
                        {(!estudiante.estado_patrocinio || estudiante.estado_patrocinio === 'pendiente') ? (
                          <div style={{display: 'flex', gap: '8px'}}>
                            <button
                              onClick={() => gestionarPatrocinio(estudiante.id, 'aceptado')}
                              style={{
                                padding: '6px 12px',
                                background: '#10b981',
                                color: 'white',
                                border: 'none',
                                borderRadius: '6px',
                                fontSize: '12px',
                                fontWeight: '600',
                                cursor: 'pointer'
                              }}
                            >
                              ✅ Aceptar
                            </button>
                            <button
                              onClick={() => gestionarPatrocinio(estudiante.id, 'rechazado')}
                              style={{
                                padding: '6px 12px',
                                background: '#ef4444',
                                color: 'white',
                                border: 'none',
                                borderRadius: '6px',
                                fontSize: '12px',
                                fontWeight: '600',
                                cursor: 'pointer'
                              }}
                            >
                              ❌ Rechazar
                            </button>
                          </div>
                        ) : (
                          <span style={{fontSize: '12px', color: '#666'}}>
                            {estudiante.estado_patrocinio === 'aprobado' ? '✅ Procesado' : '❌ Procesado'}
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* SECCIÓN: INFORMACIÓN DE ALOJAMIENTO */}
      {activeTab === 'informacion-alojamiento' && (
        <div className="card">
          <div className="section-header">
            <h2>🏠 Solicitudes de Gestión de Alojamiento</h2>
            <div style={{fontSize: '14px', color: '#718096'}}>
              Estudiantes que solicitan que la empresa les gestione el alojamiento
            </div>
          </div>
          
          {solicitudesAlojamiento.length === 0 ? (
            <div style={{
              textAlign: 'center',
              padding: '60px 20px',
              color: '#666'
            }}>
              <div style={{fontSize: '48px', marginBottom: '16px'}}>🏠</div>
              <h3 style={{color: '#374151', marginBottom: '8px'}}>No hay solicitudes de gestión de alojamiento</h3>
              <p style={{color: '#6b7280'}}>Aquí aparecerán las solicitudes cuando los estudiantes requieran gestión de alojamiento</p>
            </div>
          ) : (
            <div style={{overflowX: 'auto'}}>
              <table style={{
                width: '100%',
                borderCollapse: 'collapse',
                backgroundColor: '#fff',
                borderRadius: '8px',
                overflow: 'hidden',
                boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
              }}>
                <thead>
                  <tr style={{backgroundColor: '#f8fafc'}}>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Estudiante</th>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Email</th>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Preferencias</th>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Estado</th>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Fecha</th>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {solicitudesAlojamiento.map((estudiante) => (
                    <tr key={estudiante.id} style={{borderBottom: '1px solid #e5e7eb'}}>
                      <td style={{padding: '16px'}}>
                        <div style={{fontWeight: '600', color: '#1f2937'}}>{estudiante.nombre}</div>
                        <div style={{fontSize: '12px', color: '#666'}}>ID: {estudiante.id}</div>
                      </td>
                      <td style={{padding: '16px'}}>{estudiante.email}</td>
                      <td style={{padding: '16px'}}>
                        {estudiante.comentarios_alojamiento ? (
                          <div style={{maxWidth: '250px'}}>
                            <div style={{fontSize: '12px', color: '#374151', fontWeight: '500'}}>
                              {estudiante.comentarios_alojamiento.substring(0, 120)}
                              {estudiante.comentarios_alojamiento.length > 120 && '...'}
                            </div>
                          </div>
                        ) : (
                          <span style={{color: '#9ca3af', fontSize: '12px'}}>Sin preferencias especificadas</span>
                        )}
                      </td>
                      <td style={{padding: '16px'}}>
                        <span style={{
                          padding: '4px 8px',
                          borderRadius: '6px',
                          fontSize: '12px',
                          fontWeight: '600',
                          backgroundColor: 
                            estudiante.estado_alojamiento === 'aprobado' ? '#d1fae5' :
                            estudiante.estado_alojamiento === 'rechazado' ? '#fee2e2' : '#fef3c7',
                          color:
                            estudiante.estado_alojamiento === 'aprobado' ? '#065f46' :
                            estudiante.estado_alojamiento === 'rechazado' ? '#dc2626' : '#92400e'
                        }}>
                          {estudiante.estado_alojamiento === 'aprobado' ? '✅ Aprobada' :
                           estudiante.estado_alojamiento === 'rechazado' ? '❌ Rechazada' : '⏳ Pendiente'}
                        </span>
                      </td>
                      <td style={{padding: '16px'}}>
                        {estudiante.fecha_solicitud && estudiante.fecha_solicitud !== 'Invalid Date' ? 
                          new Date(estudiante.fecha_solicitud).toLocaleDateString('es-ES') : 
                          'Fecha no disponible'
                        }
                      </td>
                      <td style={{padding: '16px'}}>
                        {(!estudiante.estado_alojamiento || estudiante.estado_alojamiento === 'pendiente') ? (
                          <div style={{display: 'flex', gap: '8px'}}>
                            <button
                              onClick={() => gestionarAlojamiento(estudiante.id, 'aceptado')}
                              style={{
                                padding: '6px 12px',
                                background: '#10b981',
                                color: 'white',
                                border: 'none',
                                borderRadius: '6px',
                                fontSize: '12px',
                                fontWeight: '600',
                                cursor: 'pointer'
                              }}
                            >
                              ✅ Aceptar
                            </button>
                            <button
                              onClick={() => gestionarAlojamiento(estudiante.id, 'rechazado')}
                              style={{
                                padding: '6px 12px',
                                background: '#ef4444',
                                color: 'white',
                                border: 'none',
                                borderRadius: '6px',
                                fontSize: '12px',
                                fontWeight: '600',
                                cursor: 'pointer'
                              }}
                            >
                              ❌ Rechazar
                            </button>
                          </div>
                        ) : (
                          <span style={{fontSize: '12px', color: '#666'}}>
                            {estudiante.estado_alojamiento === 'aprobado' ? '✅ Procesado' : '❌ Procesado'}
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* SECCIÓN: SEGURO MÉDICO */}
      {activeTab === 'informacion-seguro-medico' && (
        <div className="card">
          <div className="section-header">
            <h2>🏥 Solicitudes de Gestión de Seguro Médico</h2>
            <div style={{fontSize: '14px', color: '#718096'}}>
              Estudiantes que solicitan que la empresa les gestione el seguro médico
            </div>
          </div>
          
          {solicitudesSeguroMedico.length === 0 ? (
            <div style={{
              textAlign: 'center',
              padding: '60px 20px',
              color: '#666'
            }}>
              <div style={{fontSize: '48px', marginBottom: '16px'}}>🏥</div>
              <h3 style={{color: '#374151', marginBottom: '8px'}}>No hay solicitudes de gestión de seguro médico</h3>
              <p style={{color: '#6b7280'}}>Aquí aparecerán las solicitudes cuando los estudiantes requieran gestión de seguro médico</p>
            </div>
          ) : (
            <div style={{overflowX: 'auto'}}>
              <table style={{
                width: '100%',
                borderCollapse: 'collapse',
                backgroundColor: '#fff',
                borderRadius: '8px',
                overflow: 'hidden',
                boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
              }}>
                <thead>
                  <tr style={{backgroundColor: '#f8fafc'}}>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Estudiante</th>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Email</th>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Información Médica</th>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Estado</th>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Fecha</th>
                    <th style={{padding: '16px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {solicitudesSeguroMedico.map((estudiante) => (
                    <tr key={estudiante.id} style={{borderBottom: '1px solid #e5e7eb'}}>
                      <td style={{padding: '16px'}}>
                        <div style={{fontWeight: '600', color: '#1f2937'}}>{estudiante.nombre}</div>
                        <div style={{fontSize: '12px', color: '#666'}}>ID: {estudiante.id}</div>
                      </td>
                      <td style={{padding: '16px'}}>{estudiante.email}</td>
                      <td style={{padding: '16px'}}>
                        {estudiante.comentarios_seguro_medico ? (
                          <div style={{maxWidth: '250px'}}>
                            <div style={{fontSize: '12px', color: '#374151', fontWeight: '500'}}>
                              {estudiante.comentarios_seguro_medico.substring(0, 120)}
                              {estudiante.comentarios_seguro_medico.length > 120 && '...'}
                            </div>
                          </div>
                        ) : (
                          <span style={{color: '#9ca3af', fontSize: '12px'}}>Sin información especificada</span>
                        )}
                      </td>
                      <td style={{padding: '16px'}}>
                        <span style={{
                          padding: '4px 8px',
                          borderRadius: '6px',
                          fontSize: '12px',
                          fontWeight: '600',
                          backgroundColor: 
                            estudiante.estado_seguro_medico === 'aprobado' ? '#d1fae5' :
                            estudiante.estado_seguro_medico === 'rechazado' ? '#fee2e2' : '#fef3c7',
                          color:
                            estudiante.estado_seguro_medico === 'aprobado' ? '#065f46' :
                            estudiante.estado_seguro_medico === 'rechazado' ? '#dc2626' : '#92400e'
                        }}>
                          {estudiante.estado_seguro_medico === 'aprobado' ? '✅ Aprobada' :
                           estudiante.estado_seguro_medico === 'rechazado' ? '❌ Rechazada' : '⏳ Pendiente'}
                        </span>
                      </td>
                      <td style={{padding: '16px'}}>
                        {estudiante.fecha_solicitud && estudiante.fecha_solicitud !== 'Invalid Date' ? 
                          new Date(estudiante.fecha_solicitud).toLocaleDateString('es-ES') : 
                          'Fecha no disponible'
                        }
                      </td>
                      <td style={{padding: '16px'}}>
                        {(!estudiante.estado_seguro_medico || estudiante.estado_seguro_medico === 'pendiente') ? (
                          <div style={{display: 'flex', gap: '8px'}}>
                            <button
                              onClick={() => gestionarSeguroMedico(estudiante.id, 'aceptado')}
                              style={{
                                padding: '6px 12px',
                                background: '#10b981',
                                color: 'white',
                                border: 'none',
                                borderRadius: '6px',
                                fontSize: '12px',
                                fontWeight: '600',
                                cursor: 'pointer'
                              }}
                            >
                              ✅ Aceptar
                            </button>
                            <button
                              onClick={() => gestionarSeguroMedico(estudiante.id, 'rechazado')}
                              style={{
                                padding: '6px 12px',
                                background: '#ef4444',
                                color: 'white',
                                border: 'none',
                                borderRadius: '6px',
                                fontSize: '12px',
                                fontWeight: '600',
                                cursor: 'pointer'
                              }}
                            >
                              ❌ Rechazar
                            </button>
                          </div>
                        ) : (
                          <span style={{fontSize: '12px', color: '#666'}}>
                            {estudiante.estado_seguro_medico === 'aprobado' ? '✅ Procesado' : '❌ Procesado'}
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* SECCIÓN: REFERIDOS */}
      {activeTab === 'referidos' && (
        <div className="card">
          <div className="section-header">
            <h2>💎 Sistema de Referidos</h2>
            <div style={{fontSize: '14px', color: '#718096'}}>
              Comisión automática: 10% del presupuesto aceptado
            </div>
          </div>

          {referidos.length === 0 ? (
            <div className="no-data">
              <p>📭 No hay datos de referidos aún</p>
            </div>
          ) : (
            <div className="tabla-wrapper">
              <table className="tabla-estudiantes">
                <thead>
                  <tr>
                    <th>Usuario</th>
                    <th>Código Referido</th>
                    <th>Total Referidos</th>
                    <th>Comisión Total</th>
                    <th>Crédito Disponible</th>
                    <th>Tipo Recompensa</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {referidos.map((ref) => (
                    <tr key={ref.id}>
                      <td>
                        <div style={{fontWeight: '600'}}>{ref.nombre}</div>
                        <div style={{fontSize: '13px', color: '#718096'}}>{ref.email}</div>
                      </td>
                      <td>
                        <div style={{
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          color: 'white',
                          padding: '6px 12px',
                          borderRadius: '6px',
                          display: 'inline-block',
                          fontWeight: '700',
                          letterSpacing: '1px'
                        }}>
                          {ref.codigo_referido}
                        </div>
                      </td>
                      <td>
                        <span style={{
                          background: '#e0e7ff',
                          color: '#5b21b6',
                          padding: '4px 12px',
                          borderRadius: '12px',
                          fontWeight: '600',
                          fontSize: '14px'
                        }}>
                          {ref.total_referidos}
                        </span>
                      </td>
                      <td>
                        <div style={{fontSize: '16px', fontWeight: '700', color: '#10b981'}}>
                          {ref.comision_total.toFixed(2)}€
                        </div>
                      </td>
                      <td>
                        <div style={{fontSize: '16px', fontWeight: '700', color: '#f59e0b'}}>
                          {ref.credito_disponible.toFixed(2)}€
                        </div>
                      </td>
                      <td>
                        <span className={`badge ${ref.tipo_recompensa === 'dinero' ? 'badge-success' : 'badge-danger'}`}>
                          {ref.tipo_recompensa === 'dinero' ? '💰 Dinero' : '🎟️ Descuento'}
                        </span>
                      </td>
                      <td>
                        <button
                          onClick={() => {
                            setEstudianteReferido(ref);
                            setAjusteCredito({
                              credito: ref.credito_disponible,
                              tipo_recompensa: ref.tipo_recompensa
                            });
                            setShowAjustarCreditoModal(true);
                          }}
                          style={{
                            background: '#4299e1',
                            color: 'white',
                            border: 'none',
                            padding: '8px 16px',
                            borderRadius: '6px',
                            cursor: 'pointer',
                            fontSize: '14px',
                            fontWeight: '600'
                          }}
                        >
                          ⚙️ Ajustar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Solicitudes de Uso de Crédito */}
          <div style={{marginTop: '40px'}}>
            <h3 style={{marginBottom: '20px', fontSize: '20px', fontWeight: '700', color: '#1f2937'}}>
              📋 Solicitudes de Uso de Crédito ({solicitudesCredito.length})
            </h3>

            {solicitudesCredito.length === 0 ? (
              <div style={{
                textAlign: 'center',
                padding: '40px',
                backgroundColor: '#f9fafb',
                borderRadius: '10px',
                color: '#6b7280'
              }}>
                No hay solicitudes de crédito
              </div>
            ) : (
              <div style={{overflowX: 'auto'}}>
                <table style={{
                  width: '100%',
                  borderCollapse: 'collapse',
                  backgroundColor: 'white',
                  borderRadius: '10px',
                  overflow: 'hidden',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                }}>
                  <thead>
                    <tr style={{backgroundColor: '#f3f4f6'}}>
                      <th style={{padding: '12px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Estudiante</th>
                      <th style={{padding: '12px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Tipo</th>
                      <th style={{padding: '12px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Monto</th>
                      <th style={{padding: '12px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Crédito Actual</th>
                      <th style={{padding: '12px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Estado</th>
                      <th style={{padding: '12px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Fecha</th>
                      <th style={{padding: '12px', textAlign: 'left', fontWeight: '600', color: '#374151'}}>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {solicitudesCredito.map((sol) => (
                      <tr key={sol.id} style={{borderBottom: '1px solid #e5e7eb'}}>
                        <td style={{padding: '12px'}}>
                          <div>
                            <div style={{fontWeight: '600', color: '#1f2937'}}>{sol.nombre}</div>
                            <div style={{fontSize: '12px', color: '#6b7280'}}>{sol.email}</div>
                          </div>
                        </td>
                        <td style={{padding: '12px'}}>
                          <span style={{
                            padding: '4px 12px',
                            borderRadius: '9999px',
                            fontSize: '12px',
                            fontWeight: '600',
                            backgroundColor: sol.tipo === 'retiro' ? '#dbeafe' : '#fef3c7',
                            color: sol.tipo === 'retiro' ? '#1e40af' : '#92400e'
                          }}>
                            {sol.tipo === 'retiro' ? '💸 Retiro' : '🎫 Descuento'}
                          </span>
                        </td>
                        <td style={{padding: '12px', fontWeight: '700', fontSize: '16px', color: '#059669'}}>
                          {sol.monto.toFixed(2)}€
                        </td>
                        <td style={{padding: '12px', fontWeight: '600', color: '#6b7280'}}>
                          {sol.credito_disponible.toFixed(2)}€
                        </td>
                        <td style={{padding: '12px'}}>
                          <span style={{
                            padding: '4px 12px',
                            borderRadius: '9999px',
                            fontSize: '12px',
                            fontWeight: '600',
                            backgroundColor: 
                              sol.estado === 'pendiente' ? '#fef3c7' :
                              sol.estado === 'aprobada' ? '#d1fae5' : '#fee2e2',
                            color: 
                              sol.estado === 'pendiente' ? '#92400e' :
                              sol.estado === 'aprobada' ? '#065f46' : '#991b1b'
                          }}>
                            {sol.estado === 'pendiente' ? '⏳ Pendiente' :
                             sol.estado === 'aprobada' ? '✅ Aprobada' : '❌ Rechazada'}
                          </span>
                        </td>
                        <td style={{padding: '12px', fontSize: '14px', color: '#6b7280'}}>
                          {new Date(sol.fecha_solicitud).toLocaleDateString('es-ES', {
                            day: '2-digit',
                            month: '2-digit',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </td>
                        <td style={{padding: '12px'}}>
                          {sol.estado === 'pendiente' ? (
                            <div style={{display: 'flex', gap: '8px'}}>
                              <button
                                onClick={() => responderSolicitudCredito(sol.id, 'aprobar')}
                                style={{
                                  background: '#10b981',
                                  color: 'white',
                                  border: 'none',
                                  padding: '6px 12px',
                                  borderRadius: '6px',
                                  cursor: 'pointer',
                                  fontSize: '13px',
                                  fontWeight: '600'
                                }}
                              >
                                ✅ Aprobar
                              </button>
                              <button
                                onClick={() => responderSolicitudCredito(sol.id, 'rechazar')}
                                style={{
                                  background: '#ef4444',
                                  color: 'white',
                                  border: 'none',
                                  padding: '6px 12px',
                                  borderRadius: '6px',
                                  cursor: 'pointer',
                                  fontSize: '13px',
                                  fontWeight: '600'
                                }}
                              >
                                ❌ Rechazar
                              </button>
                            </div>
                          ) : (
                            <span style={{fontSize: '12px', color: '#9ca3af', fontStyle: 'italic'}}>
                              {sol.estado === 'aprobada' ? 'Procesada ✓' : 'Rechazada ✗'}
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}

      {/* SECCIÓN: ESTUDIANTES */}
      {activeTab === 'estudiantes' && (
        <>
          {/* Filtros y búsqueda */}
          <div className="controles">
        <div className="filtros">
          <button 
            className={filtro === 'todos' ? 'filtro-activo' : ''}
            onClick={() => setFiltro('todos')}
          >
            Todos
          </button>
          <button 
            className={filtro === 'pendiente' ? 'filtro-activo' : ''}
            onClick={() => setFiltro('pendiente')}
          >
            Pendientes
          </button>
          <button 
            className={filtro === 'aprobado' ? 'filtro-activo' : ''}
            onClick={() => setFiltro('aprobado')}
          >
            Aprobados
          </button>
          <button 
            className={filtro === 'rechazado' ? 'filtro-activo' : ''}
            onClick={() => setFiltro('rechazado')}
          >
            Rechazados
          </button>
        </div>
        
        <input
          type="text"
          placeholder="Buscar por nombre, email o especialidad..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
          className="buscador"
        />
      </div>

      {/* Lista de estudiantes */}
      <div className="estudiantes-section">
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
          <h2>Gestión de Estudiantes ({estudiantesFiltrados.length})</h2>
          <button
            onClick={abrirModalGenerarDocs}
            style={{
              backgroundColor: '#10b981',
              color: 'white',
              padding: '12px 24px',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            📄 Generar Documentos
          </button>
        </div>
        
        {estudiantesFiltrados.length === 0 ? (
          <p className="no-resultados">No se encontraron estudiantes</p>
        ) : (
          <div className="tabla-container">
            <table className="tabla-estudiantes">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>Email</th>
                  <th>Especialidad</th>
                  <th>Tipo Visa</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {estudiantesFiltrados.map(est => (
                  <tr key={est.id}>
                    <td>{est.id}</td>
                    <td>{est.nombre || est.nombre_completo || 'N/A'}</td>
                    <td>{est.email || 'N/A'}</td>
                    <td>{est.especialidad || est.especialidad_interes || 'N/A'}</td>
                    <td>{est.tipo_visa || 'N/A'}</td>
                    <td>
                      <span className={`badge badge-${est.estado || est.estado_procesamiento || 'pendiente'}`}>
                        {(est.estado || est.estado_procesamiento || 'pendiente').toUpperCase()}
                      </span>
                    </td>
                    <td>
                      <div className="acciones">
                        {(est.estado === 'pendiente' || est.estado_procesamiento === 'pendiente' || (!est.estado && !est.estado_procesamiento)) && (
                          <>
                            <button 
                              onClick={() => aprobarEstudiante(est.id)}
                              className="btn-aprobar"
                              title="Aprobar"
                            >
                              ✓
                            </button>
                            <button 
                              onClick={() => rechazarEstudiante(est.id)}
                              className="btn-rechazar"
                              title="Rechazar"
                            >
                              ✗
                            </button>
                          </>
                        )}
                        <button 
                          onClick={() => abrirModalEditarEstudiante(est)}
                          className="btn-editar"
                          title="Editar Detalles"
                          style={{backgroundColor: '#10b981', color: 'white', padding: '6px 10px', border: 'none', borderRadius: '5px', cursor: 'pointer', fontSize: '16px', marginRight: '5px'}}
                        >
                          ✏️
                        </button>
                        <button 
                          onClick={() => abrirModalMensaje(est)}
                          className="btn-mensaje"
                          title="Enviar Mensaje"
                          style={{backgroundColor: '#3b82f6', color: 'white', padding: '6px 10px', border: 'none', borderRadius: '5px', cursor: 'pointer', fontSize: '16px'}}
                        >
                          ✉️
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      </>
      )}

      {/* SECCIÓN: DOCUMENTOS GENERADOS */}
      {activeTab === 'documentos' && (
        <div className="documentos-section">
          {loading ? (
            <div className="loading-spinner">
              <p>⏳ Cargando documentos...</p>
            </div>
          ) : (
            <>
              <div className="section-header" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
                <h2>📄 Documentos Generados ({documentosGenerados.length})</h2>
                <div className="header-actions">
                  <button 
                    onClick={abrirModalGenerarDocs} 
                    className="btn-generar"
                    style={{marginRight: '10px'}}
                  >
                    ➕ Generar Documentos
                  </button>
                  <button 
                    onClick={() => eliminarDuplicados()} 
                    className="btn-limpiar"
                    style={{backgroundColor: '#ef4444', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '5px', cursor: 'pointer'}}
                    title="Eliminar documentos duplicados (mantiene solo el más reciente de cada tipo)"
                  >
                    🗑️ Limpiar Duplicados
                  </button>
                </div>
              </div>
              
              <div className="documentos-info">
                <p>📄 Aquí puedes generar documentos oficiales para los estudiantes, revisarlos y aprobarlos.</p>
              </div>

              {!documentosGenerados || documentosGenerados.length === 0 ? (
                <div className="no-documentos">
                  <p>No hay documentos generados aún</p>
                  <p>Ve a la pestaña de Estudiantes y genera documentos para cada estudiante</p>
                </div>
              ) : (
                <div className="tabla-container">
                  <table className="tabla-documentos">
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Estudiante</th>
                        <th>Tipo Documento</th>
                        <th>Archivo</th>
                        <th>Estado</th>
                        <th>Fecha</th>
                        <th>Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      {documentosGenerados.map(doc => (
                        <tr key={doc.id}>
                          <td>{doc.id}</td>
                          <td>{doc.estudiante_nombre}</td>
                          <td>{doc.tipo_documento.replace('_', ' ').toUpperCase()}</td>
                          <td>{doc.nombre_archivo}</td>
                          <td>
                            <span className={`badge badge-${doc.estado}`}>
                              {doc.estado.toUpperCase()}
                            </span>
                          </td>
                          <td>{new Date(doc.fecha_generacion).toLocaleDateString()}</td>
                          <td>
                            <div className="acciones">
                              <button 
                                onClick={() => descargarDocumento(doc.id)}
                                className="btn-descargar"
                                title="Descargar PDF"
                              >
                                📥
                              </button>
                              {doc.estado === 'generado' && (
                                <button 
                                  onClick={() => aprobarDocumento(doc.id)}
                                  className="btn-aprobar"
                                  title="Aprobar y Enviar"
                                >
                                  ✓
                                </button>
                              )}
                              <button 
                                onClick={() => eliminarDocumento(doc.id, doc.tipo_documento)}
                                className="btn-eliminar"
                                title="Eliminar documento"
                              >
                                🗑️
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* SECCIÓN: CURSOS */}
      {activeTab === 'cursos' && (
        <div className="cursos-section">
          <div className="section-header">
            <h2>📚 Gestión de Cursos</h2>
            <div className="header-actions">
              <button onClick={sincronizarCursosEscuelas} className="btn-sync">
                🔄 Sincronizar con Escuelas
              </button>
              <button onClick={() => setShowAddCursoModal(true)} className="btn-add">
                + Agregar Curso
              </button>
            </div>
          </div>

          {cursos.length === 0 ? (
            <div className="no-data">No hay cursos registrados</div>
          ) : (
            <div className="tabla-wrapper">
              <table className="tabla-cursos">
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Duración</th>
                    <th>Precio</th>
                    <th>Ciudad</th>
                    <th>Nivel Español</th>
                    <th>Cupos</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {cursos.map(curso => (
                    <tr key={curso.id}>
                      <td>{curso.nombre}</td>
                      <td>{curso.duracion_meses} meses</td>
                      <td>€{curso.precio_eur}</td>
                      <td>{curso.ciudad}</td>
                      <td>{curso.nivel_espanol_requerido}</td>
                      <td>{curso.cupos_disponibles}</td>
                      <td>
                        <span className={`badge ${curso.activo ? 'badge-success' : 'badge-inactive'}`}>
                          {curso.activo ? 'Activo' : 'Inactivo'}
                        </span>
                      </td>
                      <td>
                        <button 
                          onClick={() => verificarDisponibilidadCurso(curso.id)}
                          className="btn-verificar"
                          title="Verificar disponibilidad en tiempo real"
                        >
                          🔍
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* SECCIÓN: ALOJAMIENTOS */}
      {activeTab === 'alojamientos' && (
        <div className="alojamientos-section">
          <div className="section-header">
            <h2>🏠 Gestión de Alojamientos</h2>
            <button onClick={() => setShowAddAlojamientoModal(true)} className="btn-add">
              + Agregar Alojamiento
            </button>
          </div>

          {alojamientos.length === 0 ? (
            <div className="no-data">No hay alojamientos registrados</div>
          ) : (
            <div className="tabla-wrapper">
              <table className="tabla-alojamientos">
                <thead>
                  <tr>
                    <th>Tipo</th>
                    <th>Dirección</th>
                    <th>Ciudad</th>
                    <th>Precio/Mes</th>
                    <th>Capacidad</th>
                    <th>Disponible</th>
                  </tr>
                </thead>
                <tbody>
                  {alojamientos.map(aloj => (
                    <tr key={aloj.id}>
                      <td>{aloj.tipo}</td>
                      <td>{aloj.direccion}</td>
                      <td>{aloj.ciudad}</td>
                      <td>€{aloj.precio_mensual_eur}/mes</td>
                      <td>{aloj.capacidad} personas</td>
                      <td>
                        <span className={`badge ${aloj.disponible ? 'badge-success' : 'badge-danger'}`}>
                          {aloj.disponible ? 'Disponible' : 'Ocupado'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Modal: Agregar Curso */}
      {showAddCursoModal && (
        <div className="modal-overlay" onClick={() => setShowAddCursoModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Agregar Nuevo Curso</h3>
            <div className="form-group">
              <label>Nombre del Curso</label>
              <input 
                type="text" 
                value={nuevoCurso.nombre} 
                onChange={(e) => setNuevoCurso({...nuevoCurso, nombre: e.target.value})}
                placeholder="Ej: Curso de Español Intensivo"
              />
            </div>
            <div className="form-group">
              <label>Descripción</label>
              <textarea 
                value={nuevoCurso.descripcion} 
                onChange={(e) => setNuevoCurso({...nuevoCurso, descripcion: e.target.value})}
                placeholder="Descripción del curso"
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Duración (meses)</label>
                <input 
                  type="number" 
                  value={nuevoCurso.duracion_meses} 
                  onChange={(e) => setNuevoCurso({...nuevoCurso, duracion_meses: parseInt(e.target.value)})}
                />
              </div>
              <div className="form-group">
                <label>Precio (EUR)</label>
                <input 
                  type="number" 
                  value={nuevoCurso.precio_eur} 
                  onChange={(e) => setNuevoCurso({...nuevoCurso, precio_eur: parseFloat(e.target.value)})}
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Ciudad</label>
                <input 
                  type="text" 
                  value={nuevoCurso.ciudad} 
                  onChange={(e) => setNuevoCurso({...nuevoCurso, ciudad: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Nivel Español Requerido</label>
                <input 
                  type="text" 
                  value={nuevoCurso.nivel_espanol_requerido} 
                  onChange={(e) => setNuevoCurso({...nuevoCurso, nivel_espanol_requerido: e.target.value})}
                  placeholder="Ej: A2, B1, B2"
                />
              </div>
            </div>
            <div className="form-group">
              <label>Cupos Disponibles</label>
              <input 
                type="number" 
                value={nuevoCurso.cupos_disponibles} 
                onChange={(e) => setNuevoCurso({...nuevoCurso, cupos_disponibles: parseInt(e.target.value)})}
              />
            </div>
            <div className="modal-actions">
              <button onClick={() => setShowAddCursoModal(false)} className="btn-cancel">
                Cancelar
              </button>
              <button onClick={crearCurso} className="btn-submit">
                Crear Curso
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Agregar Alojamiento */}
      {showAddAlojamientoModal && (
        <div className="modal-overlay" onClick={() => setShowAddAlojamientoModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Agregar Nuevo Alojamiento</h3>
            <div className="form-group">
              <label>Tipo de Alojamiento</label>
              <input 
                type="text" 
                value={nuevoAlojamiento.tipo} 
                onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, tipo: e.target.value})}
                placeholder="Ej: Apartamento, Residencia, Familia"
              />
            </div>
            <div className="form-group">
              <label>Dirección</label>
              <input 
                type="text" 
                value={nuevoAlojamiento.direccion} 
                onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, direccion: e.target.value})}
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Ciudad</label>
                <input 
                  type="text" 
                  value={nuevoAlojamiento.ciudad} 
                  onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, ciudad: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Precio Mensual (EUR)</label>
                <input 
                  type="number" 
                  value={nuevoAlojamiento.precio_mensual_eur} 
                  onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, precio_mensual_eur: parseFloat(e.target.value)})}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Capacidad (personas)</label>
              <input 
                type="number" 
                value={nuevoAlojamiento.capacidad} 
                onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, capacidad: parseInt(e.target.value)})}
              />
            </div>
            <div className="form-group">
              <label>Descripción</label>
              <textarea 
                value={nuevoAlojamiento.descripcion} 
                onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, descripcion: e.target.value})}
                placeholder="Descripción del alojamiento"
              />
            </div>
            <div className="form-group">
              <label>Servicios</label>
              <textarea 
                value={nuevoAlojamiento.servicios} 
                onChange={(e) => setNuevoAlojamiento({...nuevoAlojamiento, servicios: e.target.value})}
                placeholder="Ej: WiFi, Cocina, Limpieza"
              />
            </div>
            <div className="modal-actions">
              <button onClick={() => setShowAddAlojamientoModal(false)} className="btn-cancel">
                Cancelar
              </button>
              <button onClick={crearAlojamiento} className="btn-submit">
                Crear Alojamiento
              </button>
            </div>
          </div>
        </div>
      )}

      {/* SECCIÓN: REPORTES */}
      {activeTab === 'reportes' && (
        <div className="reportes-section">
          <h2>📊 Reportes y Estadísticas</h2>
          
          {!reporteEstudiantes ? (
            <div className="loading">Cargando reportes...</div>
          ) : (
            <>
              {/* Resumen general */}
              <div className="reporte-resumen">
                <div className="reporte-card">
                  <h3>Total Registrados</h3>
                  <div className="reporte-numero">{reporteEstudiantes.total}</div>
                </div>
                <div className="reporte-card">
                  <h3>Aprobados</h3>
                  <div className="reporte-numero success">
                    {reporteEstudiantes.estudiantes.filter(e => e.estado === 'aprobado').length}
                  </div>
                </div>
                <div className="reporte-card">
                  <h3>Pendientes</h3>
                  <div className="reporte-numero warning">
                    {reporteEstudiantes.estudiantes.filter(e => e.estado === 'pendiente').length}
                  </div>
                </div>
                <div className="reporte-card">
                  <h3>Rechazados</h3>
                  <div className="reporte-numero danger">
                    {reporteEstudiantes.estudiantes.filter(e => e.estado === 'rechazado').length}
                  </div>
                </div>
              </div>

              {/* Estadísticas por nacionalidad */}
              <div className="reporte-seccion">
                <h3>Estudiantes por Nacionalidad</h3>
                <div className="tabla-wrapper">
                  <table className="tabla-reportes">
                    <thead>
                      <tr>
                        <th>Nacionalidad</th>
                        <th>Total</th>
                        <th>Aprobados</th>
                        <th>Tasa Éxito</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(
                        reporteEstudiantes.estudiantes.reduce((acc, est) => {
                          const nac = est.nacionalidad || 'Sin especificar'
                          if (!acc[nac]) acc[nac] = { total: 0, aprobados: 0 }
                          acc[nac].total++
                          if (est.estado === 'aprobado') acc[nac].aprobados++
                          return acc
                        }, {})
                      ).map(([nac, stats]) => (
                        <tr key={nac}>
                          <td>{nac}</td>
                          <td>{stats.total}</td>
                          <td>{stats.aprobados}</td>
                          <td>
                            <span className={`badge ${stats.aprobados / stats.total > 0.7 ? 'badge-success' : stats.aprobados / stats.total > 0.4 ? 'badge-warning' : 'badge-danger'}`}>
                              {((stats.aprobados / stats.total) * 100).toFixed(0)}%
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Estadísticas por curso */}
              <div className="reporte-seccion">
                <h3>Estudiantes por Curso</h3>
                <div className="tabla-wrapper">
                  <table className="tabla-reportes">
                    <thead>
                      <tr>
                        <th>Curso</th>
                        <th>Estudiantes Asignados</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(
                        reporteEstudiantes.estudiantes.reduce((acc, est) => {
                          const curso = est.curso || 'Sin asignar'
                          acc[curso] = (acc[curso] || 0) + 1
                          return acc
                        }, {})
                      ).map(([curso, count]) => (
                        <tr key={curso}>
                          <td>{curso}</td>
                          <td>{count}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Botón de exportar */}
              <div className="reporte-acciones">
                <button 
                  onClick={() => {
                    const dataStr = JSON.stringify(reporteEstudiantes, null, 2)
                    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
                    const exportFileDefaultName = `reporte_estudiantes_${new Date().toISOString().split('T')[0]}.json`
                    const linkElement = document.createElement('a')
                    linkElement.setAttribute('href', dataUri)
                    linkElement.setAttribute('download', exportFileDefaultName)
                    linkElement.click()
                  }}
                  className="btn-export"
                >
                  📥 Exportar JSON
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {/* Modal: Cursos Sugeridos */}
      {showCursosSugeridosModal && (
        <div className="modal-overlay" onClick={() => setShowCursosSugeridosModal(false)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <h3>📚 Cursos Sugeridos para el Estudiante</h3>
            
            {cursosSugeridos.length === 0 ? (
              <div className="no-data">No hay cursos disponibles que coincidan con el perfil</div>
            ) : (
              <div className="cursos-sugeridos-lista">
                {cursosSugeridos.map(curso => (
                  <div key={curso.id} className="curso-sugerido-card">
                    <div className="curso-sugerido-header">
                      <h4>{curso.nombre}</h4>
                      <span className={`compatibilidad-badge compatibilidad-${Math.floor(curso.compatibilidad / 20)}`}>
                        {curso.compatibilidad}% compatible
                      </span>
                    </div>
                    <p className="curso-descripcion">{curso.descripcion}</p>
                    <div className="curso-detalles">
                      <span>🕐 {curso.duracion_meses} meses</span>
                      <span>📍 {curso.ciudad}</span>
                      <span>💶 €{curso.precio_eur}</span>
                      <span>📖 {curso.nivel_espanol_requerido}</span>
                    </div>
                    <button 
                      onClick={() => aprobarConCurso(curso.id)}
                      className="btn-seleccionar-curso"
                    >
                      ✓ Seleccionar este curso
                    </button>
                  </div>
                ))}
              </div>
            )}
            
            <div className="modal-actions">
              <button onClick={() => setShowCursosSugeridosModal(false)} className="btn-cancel">
                Cancelar
              </button>
              <button onClick={() => aprobarConCurso(null)} className="btn-submit-secondary">
                Aprobar sin asignar curso
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de rechazo */}
      {estudianteSeleccionado && (
        <div className="modal-overlay" onClick={() => setEstudianteSeleccionado(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Rechazar Estudiante</h3>
            <p>Por favor indique el motivo del rechazo:</p>
            <textarea
              value={motivoRechazo}
              onChange={(e) => setMotivoRechazo(e.target.value)}
              placeholder="Ej: Documentación incompleta"
              rows="4"
            />
            <div className="modal-actions">
              <button onClick={() => setEstudianteSeleccionado(null)} className="btn-cancelar">
                Cancelar
              </button>
              <button onClick={confirmarRechazo} className="btn-confirmar">
                Confirmar Rechazo
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Generar Documentos - Estudiantes Aprobados */}
      {showModalGenerarDocs && (
        <div className="modal-overlay" onClick={() => setShowModalGenerarDocs(false)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <h3>📄 Generar Documentos Oficiales</h3>
            <p style={{color: '#6b7280', marginBottom: '20px'}}>
              Selecciona un estudiante APROBADO para generar sus documentos oficiales
            </p>

            {estudiantesAprobados.length === 0 ? (
              <div style={{padding: '40px', textAlign: 'center', backgroundColor: '#fef3c7', borderRadius: '8px'}}>
                <p style={{fontSize: '48px', margin: '0 0 10px 0'}}>⚠️</p>
                <p style={{fontSize: '18px', fontWeight: 'bold', color: '#92400e', margin: '0 0 10px 0'}}>
                  No hay estudiantes aprobados
                </p>
                <p style={{color: '#78350f', margin: 0}}>
                  Debes aprobar estudiantes primero antes de generar documentos
                </p>
              </div>
            ) : (
              <div style={{maxHeight: '500px', overflowY: 'auto'}}>
                <table style={{width: '100%', borderCollapse: 'collapse'}}>
                  <thead style={{position: 'sticky', top: 0, backgroundColor: '#f9fafb', borderBottom: '2px solid #e5e7eb'}}>
                    <tr>
                      <th style={{padding: '12px', textAlign: 'left'}}>ID</th>
                      <th style={{padding: '12px', textAlign: 'left'}}>Nombre</th>
                      <th style={{padding: '12px', textAlign: 'left'}}>Email</th>
                      <th style={{padding: '12px', textAlign: 'left'}}>Especialidad</th>
                      <th style={{padding: '12px', textAlign: 'center'}}>Acción</th>
                    </tr>
                  </thead>
                  <tbody>
                    {estudiantesAprobados.map(est => (
                      <tr key={est.id} style={{borderBottom: '1px solid #e5e7eb'}}>
                        <td style={{padding: '12px'}}>{est.id}</td>
                        <td style={{padding: '12px', fontWeight: 'bold'}}>{est.nombre || est.nombre_completo}</td>
                        <td style={{padding: '12px', fontSize: '0.9rem', color: '#6b7280'}}>{est.email}</td>
                        <td style={{padding: '12px'}}>{est.especialidad || est.especialidad_interes || '-'}</td>
                        <td style={{padding: '12px', textAlign: 'center'}}>
                          <button
                            onClick={() => generarDocumentos(est.id)}
                            disabled={generandoDocs}
                            style={{
                              backgroundColor: '#10b981',
                              color: 'white',
                              padding: '8px 16px',
                              border: 'none',
                              borderRadius: '5px',
                              cursor: generandoDocs ? 'not-allowed' : 'pointer',
                              fontSize: '14px',
                              fontWeight: 'bold',
                              opacity: generandoDocs ? 0.5 : 1
                            }}
                          >
                            {generandoDocs ? '⏳ Generando...' : '📄 Generar'}
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            <div className="modal-actions" style={{marginTop: '20px'}}>
              <button 
                onClick={() => setShowModalGenerarDocs(false)} 
                className="btn-cancelar"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Enviar Mensaje */}
      {showMensajeModal && estudianteParaMensaje && (
        <div className="modal-overlay" onClick={() => setShowMensajeModal(false)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <h3>✉️ Enviar Mensaje a {estudianteParaMensaje.nombre || estudianteParaMensaje.nombre_completo}</h3>
            <p style={{color: '#6b7280', marginBottom: '20px'}}>
              📧 {estudianteParaMensaje.email}
            </p>
            
            <div className="form-group">
              <label>Asunto del Email:</label>
              <input
                type="text"
                value={nuevoMensaje.asunto}
                onChange={(e) => setNuevoMensaje({...nuevoMensaje, asunto: e.target.value})}
                placeholder="Ej: Solicitud de Documento Adicional"
                style={{width: '100%', padding: '10px', border: '1px solid #e5e7eb', borderRadius: '5px'}}
              />
            </div>

            <div className="form-group">
              <label>Tipo de Mensaje:</label>
              <select
                value={nuevoMensaje.tipo}
                onChange={(e) => setNuevoMensaje({...nuevoMensaje, tipo: e.target.value})}
                style={{width: '100%', padding: '10px', border: '1px solid #e5e7eb', borderRadius: '5px'}}
              >
                <option value="informacion">ℹ️ Información General</option>
                <option value="solicitud_documento">📄 Solicitud de Documento</option>
                <option value="recordatorio">⏰ Recordatorio</option>
                <option value="urgente">🚨 Urgente</option>
              </select>
            </div>

            {nuevoMensaje.tipo === 'solicitud_documento' && (
              <div className="form-group">
                <label>Documento Solicitado:</label>
                <input
                  type="text"
                  value={nuevoMensaje.documento_solicitado}
                  onChange={(e) => setNuevoMensaje({...nuevoMensaje, documento_solicitado: e.target.value})}
                  placeholder="Ej: Certificado de antecedentes penales"
                  style={{width: '100%', padding: '10px', border: '1px solid #e5e7eb', borderRadius: '5px'}}
                />
              </div>
            )}

            <div className="form-group">
              <label>Mensaje:</label>
              <textarea
                value={nuevoMensaje.mensaje}
                onChange={(e) => setNuevoMensaje({...nuevoMensaje, mensaje: e.target.value})}
                placeholder="Escribe tu mensaje aquí..."
                rows="8"
                style={{width: '100%', padding: '10px', border: '1px solid #e5e7eb', borderRadius: '5px', fontFamily: 'inherit'}}
              />
            </div>

            <div style={{backgroundColor: '#dbeafe', padding: '15px', borderRadius: '5px', marginBottom: '20px'}}>
              <p style={{margin: 0, fontSize: '14px', color: '#1e40af'}}>
                ℹ️ <strong>Nota:</strong> El estudiante recibirá este mensaje en su portal y también por email a {estudianteParaMensaje.email}
              </p>
            </div>

            <div className="modal-actions">
              <button 
                onClick={() => {
                  setShowMensajeModal(false)
                  setEstudianteParaMensaje(null)
                }} 
                className="btn-cancelar"
                disabled={enviandoMensaje}
              >
                Cancelar
              </button>
              <button 
                onClick={enviarMensaje} 
                className="btn-confirmar"
                disabled={enviandoMensaje || !nuevoMensaje.mensaje.trim()}
                style={{backgroundColor: '#3b82f6', opacity: enviandoMensaje ? 0.6 : 1}}
              >
                {enviandoMensaje ? '⏳ Enviando...' : '📤 Enviar Mensaje'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal Editar Estudiante */}
      {showEditarEstudianteModal && estudianteEditar && (
        <div className="modal-overlay">
          <div className="modal-content" style={{maxWidth: '700px', maxHeight: '90vh', overflowY: 'auto'}}>
            <h3 style={{marginTop: 0, color: '#1f2937', borderBottom: '2px solid #10b981', paddingBottom: '10px'}}>
              ✏️ Editar Datos del Estudiante
            </h3>

            {/* Información Básica */}
            <div style={{marginBottom: '25px'}}>
              <h4 style={{color: '#3b82f6', marginBottom: '15px', fontSize: '16px'}}>📋 Información Básica</h4>
              
              <div className="form-group" style={{marginBottom: '15px'}}>
                <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Nombre Completo:</label>
                <input
                  type="text"
                  value={estudianteEditar.nombre || ''}
                  onChange={(e) => setEstudianteEditar({...estudianteEditar, nombre: e.target.value})}
                  style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                  placeholder="Nombre completo del estudiante"
                />
              </div>

              <div className="form-group" style={{marginBottom: '15px'}}>
                <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Email:</label>
                <input
                  type="email"
                  value={estudianteEditar.email || ''}
                  onChange={(e) => setEstudianteEditar({...estudianteEditar, email: e.target.value})}
                  style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                  placeholder="correo@ejemplo.com"
                />
              </div>

              <div className="form-group" style={{marginBottom: '15px'}}>
                <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Teléfono:</label>
                <input
                  type="text"
                  value={estudianteEditar.telefono || ''}
                  onChange={(e) => setEstudianteEditar({...estudianteEditar, telefono: e.target.value})}
                  style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                  placeholder="+34 123 456 789"
                />
              </div>

              <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '15px'}}>
                <div className="form-group">
                  <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Pasaporte:</label>
                  <input
                    type="text"
                    value={estudianteEditar.pasaporte || ''}
                    onChange={(e) => setEstudianteEditar({...estudianteEditar, pasaporte: e.target.value})}
                    style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                    placeholder="ABC123456"
                  />
                </div>

                <div className="form-group">
                  <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Edad:</label>
                  <input
                    type="number"
                    value={estudianteEditar.edad || ''}
                    onChange={(e) => setEstudianteEditar({...estudianteEditar, edad: parseInt(e.target.value)})}
                    style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                    placeholder="25"
                  />
                </div>
              </div>

              <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '15px'}}>
                <div className="form-group">
                  <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Nacionalidad:</label>
                  <input
                    type="text"
                    value={estudianteEditar.nacionalidad || ''}
                    onChange={(e) => setEstudianteEditar({...estudianteEditar, nacionalidad: e.target.value})}
                    style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                    placeholder="Ej: Colombiana"
                  />
                </div>

                <div className="form-group">
                  <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Ciudad Origen:</label>
                  <input
                    type="text"
                    value={estudianteEditar.ciudad_origen || ''}
                    onChange={(e) => setEstudianteEditar({...estudianteEditar, ciudad_origen: e.target.value})}
                    style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                    placeholder="Ej: Bogotá"
                  />
                </div>
              </div>
            </div>

            {/* Información Académica */}
            <div style={{marginBottom: '25px'}}>
              <h4 style={{color: '#3b82f6', marginBottom: '15px', fontSize: '16px'}}>🎓 Información Académica</h4>
              
              <div className="form-group" style={{marginBottom: '15px'}}>
                <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Especialidad:</label>
                <input
                  type="text"
                  value={estudianteEditar.especialidad || ''}
                  onChange={(e) => setEstudianteEditar({...estudianteEditar, especialidad: e.target.value})}
                  style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                  placeholder="Ej: Ingeniería de Software"
                />
              </div>

              <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '15px'}}>
                <div className="form-group">
                  <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Nivel Español:</label>
                  <select
                    value={estudianteEditar.nivel_espanol || ''}
                    onChange={(e) => setEstudianteEditar({...estudianteEditar, nivel_espanol: e.target.value})}
                    style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                  >
                    <option value="">Seleccionar...</option>
                    <option value="A1">A1 - Principiante</option>
                    <option value="A2">A2 - Básico</option>
                    <option value="B1">B1 - Intermedio</option>
                    <option value="B2">B2 - Intermedio Alto</option>
                    <option value="C1">C1 - Avanzado</option>
                    <option value="C2">C2 - Nativo</option>
                  </select>
                </div>

                <div className="form-group">
                  <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Tipo Visa:</label>
                  <select
                    value={estudianteEditar.tipo_visa || ''}
                    onChange={(e) => setEstudianteEditar({...estudianteEditar, tipo_visa: e.target.value})}
                    style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                  >
                    <option value="">Seleccionar...</option>
                    <option value="estudios">Estudios</option>
                    <option value="trabajo">Trabajo</option>
                    <option value="residencia">Residencia</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Información Financiera */}
            <div style={{marginBottom: '25px', backgroundColor: '#f0fdf4', padding: '15px', borderRadius: '8px', border: '1px solid #bbf7d0'}}>
              <h4 style={{color: '#10b981', marginBottom: '15px', fontSize: '16px'}}>💰 Información Financiera</h4>
              
              <div className="form-group" style={{marginBottom: '15px'}}>
                <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer'}}>
                  <input
                    type="checkbox"
                    checked={estudianteEditar.fondos_suficientes || false}
                    onChange={(e) => setEstudianteEditar({...estudianteEditar, fondos_suficientes: e.target.checked})}
                    style={{marginRight: '10px', width: '18px', height: '18px', cursor: 'pointer'}}
                  />
                  <span style={{fontWeight: '500', color: '#374151'}}>¿Tiene fondos suficientes?</span>
                </label>
              </div>

              <div className="form-group" style={{marginBottom: '15px'}}>
                <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Monto de Fondos (€):</label>
                <input
                  type="number"
                  step="0.01"
                  value={estudianteEditar.monto_fondos || ''}
                  onChange={(e) => setEstudianteEditar({...estudianteEditar, monto_fondos: parseFloat(e.target.value)})}
                  style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                  placeholder="8000.00"
                />
                <small style={{color: '#6b7280', fontSize: '12px'}}>Mínimo recomendado: 8,000€ por año académico</small>
              </div>
            </div>

            {/* Información de Patrocinio */}
            <div style={{marginBottom: '25px', backgroundColor: '#fef3c7', padding: '15px', borderRadius: '8px', border: '1px solid #fde68a'}}>
              <h4 style={{color: '#f59e0b', marginBottom: '15px', fontSize: '16px'}}>🤝 Información de Patrocinio</h4>
              
              <div className="form-group" style={{marginBottom: '15px'}}>
                <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer'}}>
                  <input
                    type="checkbox"
                    checked={estudianteEditar.tiene_patrocinador || false}
                    onChange={(e) => setEstudianteEditar({...estudianteEditar, tiene_patrocinador: e.target.checked})}
                    style={{marginRight: '10px', width: '18px', height: '18px', cursor: 'pointer'}}
                  />
                  <span style={{fontWeight: '500', color: '#374151'}}>¿Tiene patrocinador?</span>
                </label>
              </div>

              {estudianteEditar.tiene_patrocinador && (
                <>
                  <div className="form-group" style={{marginBottom: '15px'}}>
                    <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Tipo de Patrocinador:</label>
                    <select
                      value={estudianteEditar.tipo_patrocinador || ''}
                      onChange={(e) => setEstudianteEditar({...estudianteEditar, tipo_patrocinador: e.target.value})}
                      style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                    >
                      <option value="">Seleccionar...</option>
                      <option value="familiar">Familiar</option>
                      <option value="empresa">Empresa</option>
                    </select>
                  </div>

                  <div className="form-group" style={{marginBottom: '15px'}}>
                    <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Nombre del Patrocinador:</label>
                    <input
                      type="text"
                      value={estudianteEditar.nombre_patrocinador || ''}
                      onChange={(e) => setEstudianteEditar({...estudianteEditar, nombre_patrocinador: e.target.value})}
                      style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                      placeholder="Nombre completo del patrocinador"
                    />
                  </div>

                  {estudianteEditar.tipo_patrocinador === 'familiar' && (
                    <div className="form-group" style={{marginBottom: '15px'}}>
                      <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>Relación con el Patrocinador:</label>
                      <select
                        value={estudianteEditar.relacion_patrocinador || ''}
                        onChange={(e) => setEstudianteEditar({...estudianteEditar, relacion_patrocinador: e.target.value})}
                        style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                      >
                        <option value="">Seleccionar...</option>
                        <option value="padre">Padre</option>
                        <option value="madre">Madre</option>
                        <option value="hermano">Hermano/a</option>
                        <option value="abuelo">Abuelo/a</option>
                        <option value="tio">Tío/a</option>
                        <option value="otro">Otro Familiar</option>
                      </select>
                    </div>
                  )}
                </>
              )}
            </div>

            {/* Documentos Subidos */}
            <div style={{marginBottom: '25px', backgroundColor: '#eff6ff', padding: '15px', borderRadius: '8px', border: '1px solid #bfdbfe'}}>
              <h4 style={{color: '#3b82f6', marginBottom: '15px', fontSize: '16px'}}>📄 Documentos del Estudiante</h4>
              
              <div style={{display: 'flex', flexDirection: 'column', gap: '12px'}}>
                {/* Pasaporte */}
                <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px', backgroundColor: 'white', borderRadius: '6px', border: '1px solid #e5e7eb'}}>
                  <div style={{display: 'flex', alignItems: 'center', gap: '10px', flex: 1}}>
                    {estudianteEditar.archivo_pasaporte ? (
                      <span style={{fontSize: '20px'}}>✅</span>
                    ) : (
                      <span style={{fontSize: '20px'}}>❌</span>
                    )}
                    <span style={{fontWeight: '500', color: '#374151', fontSize: '14px'}}>Pasaporte</span>
                  </div>
                  {estudianteEditar.archivo_pasaporte && (
                    <button
                      onClick={() => {
                        const url = `${import.meta.env.VITE_API_URL}/estudiantes/${estudianteEditar.id}/documentos/pasaporte`;
                        window.open(url, '_blank');
                      }}
                      style={{
                        padding: '6px 12px',
                        backgroundColor: '#3b82f6',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        fontSize: '13px',
                        fontWeight: '500',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px'
                      }}
                    >
                      📥 Descargar
                    </button>
                  )}
                </div>

                {/* Título Universitario */}
                <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px', backgroundColor: 'white', borderRadius: '6px', border: '1px solid #e5e7eb'}}>
                  <div style={{display: 'flex', alignItems: 'center', gap: '10px', flex: 1}}>
                    {estudianteEditar.archivo_titulo ? (
                      <span style={{fontSize: '20px'}}>✅</span>
                    ) : (
                      <span style={{fontSize: '20px'}}>❌</span>
                    )}
                    <span style={{fontWeight: '500', color: '#374151', fontSize: '14px'}}>Título Universitario</span>
                  </div>
                  {estudianteEditar.archivo_titulo && (
                    <button
                      onClick={() => {
                        const url = `${import.meta.env.VITE_API_URL}/estudiantes/${estudianteEditar.id}/documentos/titulo`;
                        window.open(url, '_blank');
                      }}
                      style={{
                        padding: '6px 12px',
                        backgroundColor: '#3b82f6',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        fontSize: '13px',
                        fontWeight: '500',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px'
                      }}
                    >
                      📥 Descargar
                    </button>
                  )}
                </div>

                {/* Notas Académicas */}
                <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px', backgroundColor: 'white', borderRadius: '6px', border: '1px solid #e5e7eb'}}>
                  <div style={{display: 'flex', alignItems: 'center', gap: '10px', flex: 1}}>
                    {estudianteEditar.archivo_notas ? (
                      <span style={{fontSize: '20px'}}>✅</span>
                    ) : (
                      <span style={{fontSize: '20px'}}>❌</span>
                    )}
                    <span style={{fontWeight: '500', color: '#374151', fontSize: '14px'}}>Notas Académicas</span>
                  </div>
                  {estudianteEditar.archivo_notas && (
                    <button
                      onClick={() => {
                        const url = `${import.meta.env.VITE_API_URL}/estudiantes/${estudianteEditar.id}/documentos/notas`;
                        window.open(url, '_blank');
                      }}
                      style={{
                        padding: '6px 12px',
                        backgroundColor: '#3b82f6',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        fontSize: '13px',
                        fontWeight: '500',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px'
                      }}
                    >
                      📥 Descargar
                    </button>
                  )}
                </div>

                {/* Certificado Médico */}
                <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px', backgroundColor: 'white', borderRadius: '6px', border: '1px solid #e5e7eb'}}>
                  <div style={{display: 'flex', alignItems: 'center', gap: '10px', flex: 1}}>
                    {estudianteEditar.archivo_certificado_medico ? (
                      <span style={{fontSize: '20px'}}>✅</span>
                    ) : (
                      <span style={{fontSize: '20px'}}>❌</span>
                    )}
                    <span style={{fontWeight: '500', color: '#374151', fontSize: '14px'}}>Certificado Médico</span>
                  </div>
                  {estudianteEditar.archivo_certificado_medico && (
                    <button
                      onClick={() => {
                        const url = `${import.meta.env.VITE_API_URL}/estudiantes/${estudianteEditar.id}/documentos/certificado_medico`;
                        window.open(url, '_blank');
                      }}
                      style={{
                        padding: '6px 12px',
                        backgroundColor: '#3b82f6',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        fontSize: '13px',
                        fontWeight: '500',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px'
                      }}
                    >
                      📥 Descargar
                    </button>
                  )}
                </div>

                <p style={{margin: '10px 0 0 0', fontSize: '12px', color: '#6b7280', fontStyle: 'italic'}}>
                  💡 Los estudiantes pueden subir sus documentos desde su panel.
                </p>
              </div>
            </div>

            <div className="modal-actions" style={{display: 'flex', justifyContent: 'flex-end', gap: '10px', paddingTop: '15px', borderTop: '1px solid #e5e7eb'}}>
              <button 
                onClick={() => {
                  setShowEditarEstudianteModal(false)
                  setEstudianteEditar(null)
                }} 
                className="btn-cancelar"
                style={{padding: '10px 20px', backgroundColor: '#6b7280', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontSize: '14px'}}
              >
                Cancelar
              </button>
              <button 
                onClick={guardarEstudiante} 
                className="btn-confirmar"
                style={{padding: '10px 20px', backgroundColor: '#10b981', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontSize: '14px', fontWeight: '500'}}
              >
                💾 Guardar Cambios
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal Contraoferta */}
      {showContraofertaModal && presupuestoSeleccionado && (
        <div className="modal-overlay">
          <div className="modal-content" style={{maxWidth: '600px'}}>
            <h3 style={{marginTop: 0, color: '#1f2937', borderBottom: '2px solid #10b981', paddingBottom: '10px'}}>
              💰 Ofertar Modalidades de Pago
            </h3>

            <div style={{backgroundColor: '#f9fafb', padding: '15px', borderRadius: '8px', marginBottom: '20px'}}>
              <p style={{margin: '0 0 5px 0', fontSize: '14px', color: '#6b7280'}}>
                <strong>Estudiante:</strong> {presupuestoSeleccionado.nombre_estudiante}
              </p>
              <p style={{margin: '0 0 5px 0', fontSize: '14px', color: '#6b7280'}}>
                <strong>Email:</strong> {presupuestoSeleccionado.email_estudiante}
              </p>
              <p style={{margin: '0 0 5px 0', fontSize: '14px', color: '#6b7280'}}>
                <strong>Servicios solicitados:</strong> {Array.isArray(presupuestoSeleccionado.servicios_solicitados) ? presupuestoSeleccionado.servicios_solicitados.join(', ') : 'N/A'}
              </p>
            </div>

            <div className="form-group" style={{marginBottom: '15px'}}>
              <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>
                💳 Precio al Empezar (€) *
              </label>
              <input
                type="number"
                step="0.01"
                value={contraoferta.precio_al_empezar}
                onChange={(e) => setContraoferta({...contraoferta, precio_al_empezar: e.target.value})}
                style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                placeholder="1200.00"
              />
            </div>

            <div className="form-group" style={{marginBottom: '15px'}}>
              <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>
                🎯 Precio con Visa (€) *
              </label>
              <input
                type="number"
                step="0.01"
                value={contraoferta.precio_con_visa}
                onChange={(e) => setContraoferta({...contraoferta, precio_con_visa: e.target.value})}
                style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                placeholder="1350.00"
              />
            </div>

            <div className="form-group" style={{marginBottom: '15px'}}>
              <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>
                📅 Precio Financiado - 12 cuotas (€) *
              </label>
              <input
                type="number"
                step="0.01"
                value={contraoferta.precio_financiado}
                onChange={(e) => setContraoferta({...contraoferta, precio_financiado: e.target.value})}
                style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px'}}
                placeholder="1500.00"
              />
              <small style={{color: '#6b7280'}}>Cuota mensual: €{contraoferta.precio_financiado ? (contraoferta.precio_financiado / 12).toFixed(2) : '0.00'}</small>
            </div>

            <div className="form-group" style={{marginBottom: '20px'}}>
              <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151'}}>
                💬 Comentarios Adicionales
              </label>
              <textarea
                value={contraoferta.comentarios_admin}
                onChange={(e) => setContraoferta({...contraoferta, comentarios_admin: e.target.value})}
                rows="4"
                style={{width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: '5px', fontSize: '14px', fontFamily: 'inherit'}}
                placeholder="Detalles adicionales sobre la oferta..."
              />
            </div>

            <div style={{marginBottom: '15px', padding: '12px', backgroundColor: '#e0f2fe', borderLeft: '4px solid #0288d1', borderRadius: '5px'}}>
              <p style={{margin: 0, fontSize: '12px', color: '#01579b'}}>
                📝 <strong>Nota:</strong> Se incluirá automáticamente un mensaje indicando que el estudiante puede rechazar esta oferta y solicitar un nuevo presupuesto.
              </p>
            </div>

            <div style={{display: 'flex', gap: '10px', justifyContent: 'flex-end'}}>
              <button
                onClick={() => {
                  setShowContraofertaModal(false)
                  setPresupuestoSeleccionado(null)
                  setContraoferta({
                    precio_al_empezar: '', 
                    precio_con_visa: '', 
                    precio_financiado: '', 
                    comentarios_admin: ''
                  })
                }}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#6b7280',
                  color: 'white',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}
              >
                Cancelar
              </button>
              <button
                onClick={async () => {
                  if (!contraoferta.precio_al_empezar || !contraoferta.precio_con_visa || !contraoferta.precio_financiado) {
                    alert('⚠️ Por favor completa todas las modalidades de pago');
                    return;
                  }

                  try {
                    await axios.put(`${apiUrl}/api/admin/presupuestos/${presupuestoSeleccionado.id}/ofertar-modalidades`, {
                      precio_al_empezar: parseFloat(contraoferta.precio_al_empezar),
                      precio_con_visa: parseFloat(contraoferta.precio_con_visa),
                      precio_financiado: parseFloat(contraoferta.precio_financiado),
                      comentarios_admin: contraoferta.comentarios_admin
                    });
                    alert('✅ Oferta con modalidades enviada exitosamente');
                    setShowContraofertaModal(false);
                    setPresupuestoSeleccionado(null);
                    setContraoferta({
                      precio_al_empezar: '', 
                      precio_con_visa: '', 
                      precio_financiado: '', 
                      comentarios_admin: ''
                    });
                    cargarDatos();
                  } catch (err) {
                    alert('❌ Error al enviar oferta: ' + (err.response?.data?.detail || err.message));
                  }
                }}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#10b981',
                  color: 'white',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '600'
                }}
              >
                📤 Enviar Oferta
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Ajustar Crédito de Referido */}
      {showAjustarCreditoModal && estudianteReferido && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            padding: '30px',
            maxWidth: '500px',
            width: '90%'
          }}>
            <h3 style={{margin: '0 0 20px 0', color: '#2d3748'}}>
              ⚙️ Ajustar Crédito: {estudianteReferido.nombre}
            </h3>

            <div style={{marginBottom: '20px'}}>
              <label style={{display: 'block', marginBottom: '8px', fontWeight: '600', color: '#4a5568'}}>
                Crédito Disponible (€)
              </label>
              <input
                type="number"
                step="0.01"
                value={ajusteCredito.credito}
                onChange={(e) => setAjusteCredito({...ajusteCredito, credito: parseFloat(e.target.value)})}
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '2px solid #e2e8f0',
                  borderRadius: '8px',
                  fontSize: '16px'
                }}
              />
            </div>

            <div style={{marginBottom: '25px'}}>
              <label style={{display: 'block', marginBottom: '8px', fontWeight: '600', color: '#4a5568'}}>
                Tipo de Recompensa
              </label>
              <select
                value={ajusteCredito.tipo_recompensa}
                onChange={(e) => setAjusteCredito({...ajusteCredito, tipo_recompensa: e.target.value})}
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '2px solid #e2e8f0',
                  borderRadius: '8px',
                  fontSize: '16px'
                }}
              >
                <option value="dinero">💰 Dinero</option>
                <option value="descuento">🎟️ Descuento</option>
              </select>
            </div>

            <div style={{
              background: '#fef3c7',
              padding: '15px',
              borderRadius: '8px',
              marginBottom: '20px',
              border: '1px solid #fde68a'
            }}>
              <p style={{margin: 0, fontSize: '14px', color: '#92400e'}}>
                ℹ️ <strong>Info:</strong> Los cambios se aplicarán inmediatamente y el estudiante podrá ver su nuevo crédito.
              </p>
            </div>

            <div style={{display: 'flex', gap: '10px', justifyContent: 'flex-end'}}>
              <button
                onClick={() => {
                  setShowAjustarCreditoModal(false);
                  setEstudianteReferido(null);
                }}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#e2e8f0',
                  color: '#2d3748',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '600'
                }}
              >
                Cancelar
              </button>
              <button
                onClick={async () => {
                  try {
                    await axios.put(`${apiUrl}/api/admin/referidos/${estudianteReferido.id}/credito`, {
                      credito: ajusteCredito.credito,
                      tipo_recompensa: ajusteCredito.tipo_recompensa
                    });
                    alert('✅ Crédito actualizado exitosamente');
                    setShowAjustarCreditoModal(false);
                    setEstudianteReferido(null);
                    cargarDatos();
                  } catch (err) {
                    alert('❌ Error al actualizar crédito: ' + (err.response?.data?.detail || err.message));
                  }
                }}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#10b981',
                  color: 'white',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '600'
                }}
              >
                💾 Guardar Cambios
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default DashboardAdminExpandido
