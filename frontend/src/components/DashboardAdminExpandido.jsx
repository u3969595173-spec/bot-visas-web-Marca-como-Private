import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import './DashboardAdminExpandido.css'
// Complete dark mode applied
import RetirosCreditoPanel from './RetirosCreditoPanel'

const API = import.meta.env.VITE_API_URL || '${API}'

const METODOS_DEFAULT = [
  { moneda: 'MLC', tipo: 'tarjeta', numero: '', instrucciones: '', minimo: 100 },
  { moneda: 'CUP', tipo: 'tarjeta', numero: '', instrucciones: '', minimo: 500 },
  { moneda: 'EUR', tipo: 'iban', titular: '', iban: '', concepto: '', minimo: 500 },
  { moneda: 'USDT BEP-20', tipo: 'wallet', wallet: '', red: 'BEP-20 (BSC)', instrucciones: '', minimo: 50 },
]

const defaultMinimos = { MLC: 100, CUP: 500, 'USDT BEP-20': 50, EUR: 500 }

const readStorage = (key, fallback) => {
  try {
    const raw = localStorage.getItem(key)
    return raw ? JSON.parse(raw) : fallback
  } catch {
    return fallback
  }
}

const writeStorage = (key, value) => localStorage.setItem(key, JSON.stringify(value))

const formatCurrency = (value, moneda) => {
  if (!Number.isFinite(value)) return '—'
  if (moneda === 'CUP') return `${Number(value).toLocaleString('es-ES')} CUP`
  if (moneda === 'MLC') return `${Number(value).toLocaleString('es-ES')} MLC`
  return `€${Number(value).toLocaleString('es-ES')}`
}

const formatDate = (value) => {
  if (!value) return '—'
  try {
    return new Date(value).toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' })
  } catch {
    return value
  }
}

const normalizeAportacion = (item) => {
  const importe = Number(item.importe || 0)
  const gananciasDisponibles = item.gananciasDisponibles !== undefined ? Number(item.gananciasDisponibles) : importe * 3
  return {
    id: item.id,
    usuario: item.usuario || item.usuarioNombre || 'Usuario DEMO',
    usuarioNombre: item.usuarioNombre || item.usuario || 'Usuario DEMO',
    importe: importe,
    moneda: item.moneda || 'EUR',
    fecha: formatDate(item.createdAt || item.fecha),
    fechaOriginal: item.createdAt || item.fecha || new Date().toISOString(),
    fechaUltimoPago: item.fechaUltimoPago || null,
    gananciasDisponibles: gananciasDisponibles,
    email: item.email || item.usuarioEmail || '',
    cuenta: item.cuentaDestino || item.cuenta || 'Sin cuenta',
    metodo: item.metodoPago || item.metodo || 'Transferencia',
    estado: item.estado || 'Pendiente de validación',
    comentarios: item.comentarios || item.comentario || 'Sin comentarios',
    justificante: item.justificante?.nombre || item.justificante || 'Sin justificante',
    justificanteData: item.justificante || null,
    comentario: item.comentario || item.comentarios || 'Sin comentarios',
  }
}

function DashboardAdminExpandido({ onLogout }) {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('resumen')
  const [aportaciones, setAportaciones] = useState([])
  const [retiros, setRetiros] = useState([])
  const [cuentas, setCuentas] = useState(METODOS_DEFAULT)
  const [minimos, setMinimos] = useState({ MLC: 100, CUP: 500, 'USDT BEP-20': 50 })
  const [porcentajeSemanal, setPorcentajeSemanal] = useState('')
  const [usuariosRegistrados, setUsuariosRegistrados] = useState([])
  const [solicitudes, setSolicitudes] = useState([])
  const [mensaje, setMensaje] = useState('')
  const [expandedCard, setExpandedCard] = useState(null)
  const [referidos, setReferidos] = useState([])
  const [mensajes, setMensajes] = useState([])
  const [respuesta, setRespuesta] = useState('')
  const [seleccionadoChat, setSeleccionadoChat] = useState(null)
  const [solicitudesInversion, setSolicitudesInversion] = useState([])

  React.useEffect(() => {
    // Cargar config del admin (minimos)
    const cargarConfig = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`${API}/api/admin/config`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (response.ok) {
          const data = await response.json()
          setMinimos(data.minimos && Object.keys(data.minimos).length > 0 ? data.minimos : defaultMinimos)
        }
      } catch (error) {
        console.log('Error cargando config:', error)
      }
    }

    // Cargar cuentas bancarias
    const cargarCuentas = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`${API}/api/admin/cuentas`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (response.ok) {
          const data = await response.json()
          if (data.cuentas && data.cuentas.length > 0) {
            const merged = METODOS_DEFAULT.map(defaultM => {
              const fromAPI = data.cuentas.find(c => c.moneda === defaultM.moneda)
              return fromAPI ? { ...defaultM, ...fromAPI } : defaultM
            })
            setCuentas(merged)
            localStorage.setItem('capital_trade_cuentas', JSON.stringify(merged))
          } else {
            setCuentas(METODOS_DEFAULT)
            localStorage.setItem('capital_trade_cuentas', JSON.stringify(METODOS_DEFAULT))
          }
        }
      } catch (error) {
        console.log('Error cargando cuentas:', error)
      }
    }

    cargarConfig()
    cargarCuentas()

    const intervaloConfig = setInterval(cargarConfig, 30000) // cada 30s
    const intervaloCuentas = setInterval(cargarCuentas, 30000)

    return () => {
      clearInterval(intervaloConfig)
      clearInterval(intervaloCuentas)
    }
  }, [])

  // Cargar aportaciones desde API
  React.useEffect(() => {
    const cargarAportaciones = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return

        const response = await fetch('${API}/api/aportaciones', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.ok) {
          const data = await response.json()
          setAportaciones(data.aportaciones || [])
        }
      } catch (error) {
        console.log('Error cargando aportaciones:', error)
      }
    }

    cargarAportaciones()
    const intervalo = setInterval(cargarAportaciones, 5000)

    return () => clearInterval(intervalo)
  }, [])

  // Cargar retiros desde API
  React.useEffect(() => {
    const cargarRetiros = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return

        const response = await fetch('${API}/api/retiros', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.ok) {
          const data = await response.json()
          setRetiros(data.retiros || [])
        }
      } catch (error) {
        console.log('Error cargando retiros:', error)
      }
    }

    cargarRetiros()
    const intervalo = setInterval(cargarRetiros, 5000)

    return () => clearInterval(intervalo)
  }, [])

  React.useEffect(() => {
    const cargarMensajes = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('${API}/api/comunidad/mensajes', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (response.ok) {
          const data = await response.json()
          setMensajes(data.mensajes || [])
        }
      } catch (error) {
        console.log('Error cargando mensajes:', error)
      }
    }

    cargarMensajes()
    const intervalo = setInterval(cargarMensajes, 5000)

    return () => clearInterval(intervalo)
  }, [])

  // Cargar inversores pendientes desde la API
  React.useEffect(() => {
    const cargarInversoresPendientes = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return

        const response = await fetch('${API}/api/inversores/pendientes', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.ok) {
          const data = await response.json()
          setSolicitudes(data.inversores || [])
        }
      } catch (error) {
        console.log('Error cargando inversores pendientes:', error)
      }
    }

    cargarInversoresPendientes()
    const intervalo = setInterval(cargarInversoresPendientes, 5000) // Actualizar cada 5s

    return () => clearInterval(intervalo)
  }, [])

  // Cargar inversores validados desde la API
  React.useEffect(() => {
    const cargarInversoresValidados = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return

        const response = await fetch('${API}/api/inversores/validados', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.ok) {
          const data = await response.json()
          setUsuariosRegistrados(data.inversores || [])
        }
      } catch (error) {
        console.log('Error cargando inversores validados:', error)
      }
    }

    cargarInversoresValidados()
    const intervalo = setInterval(cargarInversoresValidados, 5000) // Actualizar cada 5s

    return () => clearInterval(intervalo)
  }, [])

  // Cargar solicitudes de inversión pendientes desde la API
  React.useEffect(() => {
    const cargarSolicitudesInversion = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return

        const response = await fetch('${API}/api/solicitudes-inversion/pendientes', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.ok) {
          const data = await response.json()
          setSolicitudesInversion(data.solicitudes || [])
        }
      } catch (error) {
        console.log('Error cargando solicitudes de inversión:', error)
      }
    }

    cargarSolicitudesInversion()
    const intervalo = setInterval(cargarSolicitudesInversion, 5000) // Actualizar cada 5s

    return () => clearInterval(intervalo)
  }, [])

  React.useEffect(() => {
    // Cambio de cuentas o minimos - puede sincronizar en background pero no es necesario
  }, [cuentas, minimos])

  const tabs = [
    { key: 'resumen', label: 'Resumen' },
    { key: 'aportaciones', label: 'Aportaciones' },
    { key: 'retiros', label: 'Retiros' },
    { key: 'usuarios', label: 'Usuarios' },
    { key: 'operaciones', label: 'Operaciones' },
    { key: 'solicitudes', label: 'Solicitudes' },
    { key: 'depositos', label: `💳 Depósitos (${solicitudesInversion.length})` },
    { key: 'capital', label: 'Capital y movimientos' },
    { key: 'referidos', label: 'Referidos' },
    { key: 'rangos', label: '🏆 Rangos' },
    { key: 'configuracion', label: 'Configuración' },
    { key: 'chat', label: `💬 Chat ${mensajes.filter(m => m.tipo === 'inversor' && !m.leido).length > 0 ? `(${mensajes.filter(m => m.tipo === 'inversor' && !m.leido).length})` : ''}` },
  ]

  const solicitudesPendientes = solicitudes.length > 0
    ? solicitudes
    : usuariosRegistrados.map((usuario) => ({
      id: usuario.id,
      nombre: usuario.name || 'Sin nombre',
      usuarioNombre: usuario.name || 'Sin nombre',
      email: usuario.email || '—',
      telefono: usuario.telefono || '—',
      pais: usuario.pais || '—',
      fecha: usuario.fecha || new Date().toLocaleDateString('es-ES'),
      estado: 'Pendiente de validación'
    }))

  const aportacionesNormalizadas = aportaciones.map(normalizeAportacion)

  const totalAportacionesPendientes = aportacionesNormalizadas.filter((item) => item.estado === 'Pendiente de validación').length || solicitudesPendientes.filter((item) => item.estado === 'Pendiente de validación').length
  const totalRetirosRevision = retiros.filter((item) => item.estado === 'Pendiente' || item.estado === 'En revisión').length
  const totalCapitalActivo = aportacionesNormalizadas.filter((item) => item.estado === 'Activa' || item.estado === 'Validada').reduce((sum, item) => sum + Number(item.importe || 0), 0) || usuariosRegistrados.length * 1000
  const totalAportacionesRechazadas = aportacionesNormalizadas.filter((item) => item.estado === 'Rechazada').length

  const getStatClass = (label) => {
    if (label === 'Aportaciones pendientes') return 'stat-pendientes'
    if (label === 'Retiros en revisión') return 'stat-aprobados'
    if (label === 'Capital activo') return 'stat-total'
    if (label === 'Aportaciones rechazadas') return 'stat-rechazados'
    return ''
  }

  const summaryCards = [
    { label: 'Aportaciones pendientes', value: String(totalAportacionesPendientes), icon: '👥' },
    { label: 'Retiros en revisión', value: String(totalRetirosRevision), icon: '✅' },
    { label: 'Capital activo', value: formatCurrency(totalCapitalActivo, 'EUR'), icon: '💰' },
    { label: 'Aportaciones rechazadas', value: String(totalAportacionesRechazadas), icon: '📈' },
  ]

  const table = (headers, rows) => (
    <table className="tabla-estudiantes">
      <thead>
        <tr>
          {headers.map((header) => <th key={header}>{header}</th>)}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, index) => (
          <tr key={index}>
            {row.map((cell, cellIndex) => (
              <td key={`${index}-${cellIndex}`}>{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('usuario')
    localStorage.removeItem('capital_trade_user')
    localStorage.removeItem('admin_fallback')
    if (typeof onLogout === 'function') onLogout()
    navigate('/admin/login')
  }

  const updateAportacionStatus = async (id, estado, comentario = '') => {
    try {
      const token = localStorage.getItem('token')

      const response = await fetch(`${API}/api/aportaciones/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ estado })
      })

      if (response.ok) {
        const updated = aportaciones.map((item) => {
          if (item.id === id) {
            const gananciasDisponibles = item.gananciasDisponibles !== undefined ? item.gananciasDisponibles : Number(item.importe || 0) * 3
            return { ...item, estado, comentarios: comentario || item.comentarios, gananciasDisponibles, fechaValidacion: new Date().toISOString().slice(0, 10) }
          }
          return item
        })
        setAportaciones(updated)
        setMensaje(`✅ Aportación actualizada a: ${estado}`)
        setTimeout(() => setMensaje(''), 2000)
      } else {
        setMensaje('❌ Error al actualizar')
        setTimeout(() => setMensaje(''), 2000)
      }
    } catch (error) {
      console.error('Error:', error)
      setMensaje('❌ Error al actualizar')
      setTimeout(() => setMensaje(''), 2000)
    }
  }

  const updateRetiroStatus = async (id, estado, comentario = '') => {
    try {
      const token = localStorage.getItem('token')

      const response = await fetch(`${API}/api/retiros/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ estado })
      })

      if (response.ok) {
        const updated = retiros.map((item) =>
          item.id === id
            ? { ...item, estado, comentarios: comentario || item.comentarios, fechaValidacion: new Date().toISOString().slice(0, 10) }
            : item
        )
        setRetiros(updated)
        setMensaje(`✅ Retiro actualizado a: ${estado}`)
        setTimeout(() => setMensaje(''), 2000)
      } else {
        setMensaje('❌ Error al actualizar')
        setTimeout(() => setMensaje(''), 2000)
      }
    } catch (error) {
      console.error('Error:', error)
      setMensaje('❌ Error al actualizar')
      setTimeout(() => setMensaje(''), 2000)
    }
  }

  const updateBankAccount = (index, field, value) => {
    setCuentas((prev) => prev.map((account, i) => (i === index ? { ...account, [field]: value } : account)))
  }

  const updateMinimo = (moneda, value) => setMinimos((prev) => ({ ...prev, [moneda]: Number(value) || 0 }))

  // Generar código único de referido para el admin
  const generarCodigoReferido = () => {
    return 'REF' + Math.random().toString(36).substring(2, 11).toUpperCase()
  }

  // Obtener o crear código de referido del admin
  const getCodigoReferidoAdmin = () => {
    let referidoAdmin = referidos.find(r => r.esAdmin === true)
    if (!referidoAdmin) {
      referidoAdmin = {
        id: 'admin-referido-' + Date.now(),
        codigo: generarCodigoReferido(),
        esAdmin: true,
        referidosCount: 0,
        gananciaTotal: 0,
        historial: []
      }
      setReferidos([...referidos, referidoAdmin])
    }
    return referidoAdmin
  }

  // Obtener referidos activos del admin
  const getReferidosDelAdmin = () => {
    const referidoAdmin = referidos.find(r => r.esAdmin === true)
    if (!referidoAdmin) return []
    return referidos.filter(r => r.referidoPor === referidoAdmin.codigo && r.esAdmin !== true)
  }

  // Niveles del Programa de Aceleración
  const RANGOS = [
    { nombre: 'Agent', emoji: '🟠', minInversion: 5000, minReferidos: 20, beneficioMensual: 200, meses: 7 },
    { nombre: 'Senior Partner', emoji: '🟣', minInversion: 3500, minReferidos: 15, beneficioMensual: 150, meses: 5 },
    { nombre: 'Advisor', emoji: '🔵', minInversion: 2000, minReferidos: 10, beneficioMensual: 100, meses: 3 },
    { nombre: 'Partner', emoji: '🟢', minInversion: 1000, minReferidos: 5, beneficioMensual: 50, meses: 2 }
  ]

  // Calcula el rango, referidos activos e inversión propia de cada inversor con código de referido
  const getRangosInversores = () => {
    return referidos
      .filter(r => r.codigo && !r.esAdmin)
      .map(inversor => {
        const referidosActivos = referidos.filter(r =>
          r.referidoPor === inversor.codigo && r.codigo !== inversor.codigo && Number(r.inversionTotal || 0) >= 100
        ).length

        const inversionPropia = aportacionesNormalizadas
          .filter(a => (a.estado === 'Activa' || a.estado === 'Validada') && (
            a.usuarioId === inversor.usuarioId ||
            a.usuarioNombre === inversor.nombreInversor ||
            a.usuario === inversor.nombreInversor
          ))
          .reduce((sum, a) => sum + Number(a.importe || 0), 0)

        const rango = RANGOS.find(r => inversionPropia >= r.minInversion && referidosActivos >= r.minReferidos) || null

        return {
          nombreInversor: inversor.nombreInversor,
          inversionPropia,
          referidosActivos,
          rango
        }
      })
      .filter(item => item.rango)
  }

  // Calcular comisión de referido (10% del importe de inversión)
  const calcularGananciaAcelerada = (comisionBase) => {
    return Number(comisionBase) * 3
  }

  // Actualizar ganancias disponibles después de pago de comisión
  const restarDelPoolGanancias = (aportacionId, monto) => {
    const updated = aportaciones.map(a => {
      if (a.id === aportacionId) {
        const gananciasDisponibles = Math.max(0, Number(a.gananciasDisponibles || 0) - monto)
        const nuevoEstado = gananciasDisponibles <= 0 ? 'Completada' : a.estado
        return { ...a, gananciasDisponibles, estado: nuevoEstado }
      }
      return a
    })
    setAportaciones(updated)
    return updated
  }

  const updateSolicitud = async (id, estado) => {
    try {
      const token = localStorage.getItem('token')

      // Actualizar en la API
      const response = await fetch(`${API}/api/inversores/${id}/estado`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ estado: estado.toLowerCase() })
      })

      if (response.ok) {
        // Actualizar en el estado local
        const updated = solicitudes.map((item) =>
          item.id === id ? { ...item, estado, fechaValidacion: new Date().toISOString().slice(0, 10) } : item
        )
        setSolicitudes(updated)
        writeStorage('capital_trade_solicitudes', updated)
        window.dispatchEvent(new Event('capital-trade-sync'))

        // Mostrar mensaje de confirmación
        setMensaje(`✅ Solicitud actualizada a: ${estado}`)
        setTimeout(() => setMensaje(''), 2000)
      } else {
        setMensaje('❌ Error al actualizar solicitud')
        setTimeout(() => setMensaje(''), 2000)
      }
    } catch (error) {
      console.error('Error:', error)
      setMensaje('❌ Error al actualizar solicitud')
      setTimeout(() => setMensaje(''), 2000)
    }
  }

  // Procesar pagos de comisiones de referidos con descuento en cascada
  const pagarComisionesReferidos = () => {
    const referidosSinPagar = referidos.filter(r => r.referidoPor && !r.pagado && r.esAdmin !== true)

    if (referidosSinPagar.length === 0) {
      alert('No hay comisiones de referidos para procesar')
      return
    }

    let totalComisiones = 0
    let aportacionesActualizadas = [...aportaciones]

    referidosSinPagar.forEach(referido => {
      // Comisión = 10% de la inversión del referido (SIN aceleración ×3)
      const comision = (referido.inversionTotal || 0) * 0.1
      totalComisiones += comision

      // Buscar el usuario referidor
      const referidorData = referidos.find(r => r.codigo === referido.referidoPor)

      if (referidorData && referidorData.usuarioId) {
        // Buscar TODAS las aportaciones del referidor ordenadas
        const aportacionesReferidor = aportacionesActualizadas.filter(a =>
          a.usuarioId === referidorData.usuarioId ||
          a.usuarioNombre === referidorData.nombreInversor ||
          a.usuario === referidorData.nombreInversor
        )

        if (aportacionesReferidor.length > 0) {
          let montoRestante = comision

          // Descuento en CASCADA: restar de cada aportación hasta que no quede saldo
          for (let aportacion of aportacionesReferidor) {
            if (montoRestante <= 0) break

            const gananciasActuales = Number(aportacion.gananciasDisponibles || aportacion.importe * 3)
            const montoARestar = Math.min(montoRestante, gananciasActuales)
            const gananciasRestantes = Math.max(0, gananciasActuales - montoARestar)
            const nuevoEstado = gananciasRestantes <= 0 ? 'Completada' : aportacion.estado

            // Actualizar esta aportación
            aportacionesActualizadas = aportacionesActualizadas.map(a =>
              a.id === aportacion.id
                ? { ...a, gananciasDisponibles: gananciasRestantes, estado: nuevoEstado }
                : a
            )

            montoRestante -= montoARestar
          }
        }
      }
    })

    // Actualizar referidos como pagados
    const referidosActualizados = referidos.map(r =>
      referidosSinPagar.find(rsp => rsp.id === r.id)
        ? { ...r, pagado: true }
        : r
    )

    setAportaciones(aportacionesActualizadas)
    setReferidos(referidosActualizados)
    writeStorage('capital_trade_aportaciones', aportacionesActualizadas)
    writeStorage('capital_trade_referidos', referidosActualizados)
    window.dispatchEvent(new Event('capital-trade-sync'))

    setMensaje(`✅ Pagadas ${referidosSinPagar.length} comisiones de referidos por €${totalComisiones.toFixed(2)} (saldo disponible actualizado)`)
    setTimeout(() => setMensaje(''), 3000)
  }

  // Obtener día de la semana (0-6: domingo a sábado)
  const obtenerDiaSemanainversion = (fecha) => {
    return new Date(fecha).getDay()
  }

  // Calcular próxima fecha de pago (mismo día de la semana + 7 días)
  const calcularProximoPago = (fechaUltimoPago, fechaInicio) => {
    const fechaBase = fechaUltimoPago ? new Date(fechaUltimoPago) : new Date(fechaInicio)
    const proximaPago = new Date(fechaBase)
    proximaPago.setDate(proximaPago.getDate() + 7)
    return proximaPago
  }

  // Verificar si es el día de pago de la semana (mismo día que se invirtió)
  const esDialPagoSemanal = (fechaInicio) => {
    const diaInicio = obtenerDiaSemanainversion(fechaInicio)
    const diaHoy = new Date().getDay()
    return diaInicio === diaHoy
  }

  // Verificar si inversión es elegible para pago
  const esInversionElegible = (aportacion) => {
    if (aportacion.estado !== 'Activa' && aportacion.estado !== 'Validada') return false

    // Debe ser el mismo día de la semana que el inicial
    if (!esDialPagoSemanal(aportacion.fechaOriginal)) return false

    // Y deben haber pasado 7+ días desde el último pago
    const fechaBase = aportacion.fechaUltimoPago ? new Date(aportacion.fechaUltimoPago) : new Date(aportacion.fechaOriginal)
    const hoy = new Date()
    const diasDesdeBase = Math.floor((hoy.getTime() - fechaBase.getTime()) / (1000 * 60 * 60 * 24))

    return diasDesdeBase >= 7
  }

  // Obtener inversiones elegibles para pago
  const getInversionesElegibles = () => {
    return aportacionesNormalizadas.filter(a => esInversionElegible(a))
  }

  const pagarRentabilidadSemanal = () => {
    if (!porcentajeSemanal || isNaN(porcentajeSemanal) || Number(porcentajeSemanal) <= 0) {
      alert('Ingresa un porcentaje válido')
      return
    }

    const inversionesElegibles = getInversionesElegibles()
    if (inversionesElegibles.length === 0) {
      alert('No hay inversiones elegibles para pagar hoy')
      return
    }

    // Calcular pago semanal (10% simple, sin aceleración)
    const pagosDetallados = inversionesElegibles.map(a => {
      const pago = Number(a.importe) * Number(porcentajeSemanal) / 100
      return { id: a.id, pago }
    })

    const totalAPagar = pagosDetallados.reduce((sum, p) => sum + p.pago, 0)

    const confirmacion = confirm(
      `Confirmar pago de rentabilidad:\n\n` +
      `Inversores: ${inversionesElegibles.length}\n` +
      `Porcentaje: ${porcentajeSemanal}%\n` +
      `Total a pagar: €${totalAPagar.toFixed(2)}\n\n` +
      `¿Proceder con el pago?`
    )

    if (confirmacion) {
      let aportacionesActualizadas = aportaciones.map(aportacion => {
        const pagoPorAportacion = pagosDetallados.find(p => p.id === aportacion.id)
        if (pagoPorAportacion) {
          const gananciasDisp = Number(aportacion.gananciasDisponibles || aportacion.importe * 3)
          const gananciasRestantes = Math.max(0, gananciasDisp - pagoPorAportacion.pago)
          const nuevoEstado = gananciasRestantes <= 0 ? 'Completada' : aportacion.estado

          return {
            ...aportacion,
            fechaUltimoPago: new Date().toISOString(),
            gananciasDisponibles: gananciasRestantes,
            estado: nuevoEstado
          }
        }
        return aportacion
      })

      setAportaciones(aportacionesActualizadas)
      writeStorage('capital_trade_aportaciones', aportacionesActualizadas)
      window.dispatchEvent(new Event('capital-trade-sync'))

      setMensaje(`✅ Pagos procesados: €${totalAPagar.toFixed(2)} a ${inversionesElegibles.length} inversores (saldo disponible actualizado)`)
      setTimeout(() => setMensaje(''), 3000)
      setPorcentajeSemanal('')
    }
  }

  return (
    <div className="admin-futuristic-layout">
      {/* SIDEBAR NAVIGATION */}
      <aside className="admin-sidebar">
        <div className="sidebar-brand">
          <div className="brand-icon">✧</div>
          <div className="brand-text">
            <span className="glow-text">Capital Trade</span>
            <span className="badge-admin">Admin Center</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-group-title">MENÚ PRINCIPAL</div>
          {tabs.map((tab) => (
            <button
              key={tab.key}
              className={`sidebar-tab ${activeTab === tab.key ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.key)}
            >
              <div className="tab-indicator" />
              <span className="tab-label">{tab.label}</span>
            </button>
          ))}

          <div className="nav-divider"></div>
          <div className="nav-group-title">EXTRAS</div>

          <button onClick={() => navigate('/comunidad')} className="sidebar-tab highlight">
            <div className="tab-indicator" />
            <span className="tab-label">💬 Comunidad Interna</span>
          </button>
        </nav>

        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="avatar">{(localStorage.getItem('usuario') || 'A')[0].toUpperCase()}</div>
            <div className="user-info">
              <span className="user-name">{localStorage.getItem('usuario') || 'Administrador'}</span>
              <small className="user-role">Super Admin</small>
            </div>
          </div>
          <button onClick={handleLogout} className="btn-logout-sidebar">
            Cerrar Sesión
          </button>
        </div>
      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="admin-main-content">
        <header className="topbar">
          <div className="topbar-left">
            <h1>{tabs.find(t => t.key === activeTab)?.label || 'Panel'}</h1>
            <p className="subtitle">Gestión institucional y analítica avanzada</p>
          </div>
          <div className="topbar-actions">
            {mensaje && (
              <div className="status-message fade-in">
                {mensaje}
              </div>
            )}
            <div className="header-pill status-live">
              <span className="dot-live" />
              <span>Portafolio En Línea</span>
            </div>
          </div>
        </header>

        <div className="content-scroll">

          {activeTab === 'resumen' && (
            <>
              <div className="estadisticas-grid">
                {summaryCards.map((card) => {
                  const isExpanded = expandedCard === card.label
                  const statClass = getStatClass(card.label)

                  // Preparar datos para cada tarjeta
                  let details = []
                  if (card.label === 'Aportaciones pendientes') {
                    details = aportacionesNormalizadas.filter(a => a.estado === 'Pendiente de validación')
                  } else if (card.label === 'Retiros en revisión') {
                    details = retiros.filter(r => r.estado === 'Pendiente' || r.estado === 'En revisión')
                  } else if (card.label === 'Aportaciones rechazadas') {
                    details = aportacionesNormalizadas.filter(a => a.estado === 'Rechazada')
                  }

                  return (
                    <div key={card.label}>
                      <div
                        className={`stat-card ${statClass}`}
                        onClick={() => setExpandedCard(isExpanded ? null : card.label)}
                        style={{ cursor: 'pointer', position: 'relative' }}
                      >
                        <div className="stat-icon">{card.icon}</div>
                        <div className="stat-info">
                          <h3>{card.value}</h3>
                          <p>{card.label}</p>
                        </div>
                        {details.length > 0 && (
                          <div style={{ position: 'absolute', top: '8px', right: '8px', fontSize: '18px', cursor: 'pointer' }}>
                            {isExpanded ? '▼' : '▶'}
                          </div>
                        )}
                      </div>

                      {isExpanded && details.length > 0 && (
                        <div style={{
                          marginTop: '8px',
                          padding: '12px',
                          backgroundColor: '#f3f4f6',
                          borderRadius: '8px',
                          border: '1px solid #e5e7eb',
                          fontSize: '14px',
                          maxHeight: '300px',
                          overflowY: 'auto'
                        }}>
                          {details.map((item, idx) => (
                            <div key={idx} style={{
                              padding: '8px',
                              borderBottom: idx < details.length - 1 ? '1px solid #d1d5db' : 'none',
                              marginBottom: '4px'
                            }}>
                              <strong>{item.usuario || item.nombre || 'N/A'}</strong>
                              <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
                                {card.label.includes('Aportaciones') ? (
                                  <>
                                    <div>💵 {item.importe ? `${item.importe} ${item.moneda}` : 'N/A'}</div>
                                    <div>📅 {item.fecha || 'N/A'}</div>
                                    <div>📝 {item.estado || 'N/A'}</div>
                                  </>
                                ) : (
                                  <>
                                    <div>💰 Monto: {item.monto || 'N/A'}</div>
                                    <div>📅 {item.fecha_solicitud ? new Date(item.fecha_solicitud).toLocaleDateString('es-ES') : 'N/A'}</div>
                                    <div>📝 {item.estado || 'N/A'}</div>
                                  </>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>

              <div className="card panel-summary">
                <div className="section-header">
                  <h2>Resumen operativo</h2>
                  <span className="section-tag">Últimas 24h</span>
                </div>
                <div className="summary-mini-grid">
                  {[
                    ['Aportaciones pendientes', String(totalAportacionesPendientes)],
                    ['Aportaciones validadas', String(aportaciones.filter((item) => item.estado === 'Activa' || item.estado === 'Validada').length || usuariosRegistrados.length)],
                    ['Retiros pendientes', String(totalRetirosRevision)],
                    ['Retiros aprobados', String(retiros.filter((item) => item.estado === 'Aprobado' || item.estado === 'Procesado').length)],
                    ['Capital activo', formatCurrency(totalCapitalActivo, 'EUR')]
                  ].map(([label, value]) => (
                    <div key={label} className="summary-mini-card">
                      <div className="mini-label">{label}</div>
                      <div className="mini-value">{value}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="two-column-grid">
                <div className="card">
                  <div className="section-header">
                    <h2>Aportaciones recientes</h2>
                  </div>
                  {table(
                    ['Usuario', 'Importe', 'Moneda', 'Estado'],
                    aportacionesNormalizadas.slice(0, 4).map((item) => [item.usuario, formatCurrency(Number(item.importe || 0), item.moneda), item.moneda, item.estado])
                  )}
                </div>

                <div className="card">
                  <div className="section-header">
                    <h2>Actividad reciente</h2>
                  </div>
                  <div className="activity-list">
                    {aportacionesNormalizadas.length ? (
                      aportacionesNormalizadas.slice(0, 4).map((item) => (
                        <div key={item.id} className="activity-item">
                          {item.fecha} · {item.usuario} · {item.estado} · {item.moneda} {formatCurrency(Number(item.importe || 0), item.moneda)}
                        </div>
                      ))
                    ) : (
                      <div className="activity-item">No hay actividad registrada todavía.</div>
                    )}
                  </div>
                </div>
              </div>
            </>
          )}

          {activeTab === 'aportaciones' && (
            <div className="card">
              <div className="section-header"><h2>Aportaciones</h2></div>
              <table className="tabla-estudiantes">
                <thead>
                  <tr>
                    <th>Usuario</th>
                    <th>Importe</th>
                    <th>Moneda</th>
                    <th>Fecha</th>
                    <th>Cuenta</th>
                    <th>Justificante</th>
                    <th>Estado</th>
                    <th>Comentario</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {aportacionesNormalizadas.length ? aportacionesNormalizadas.map((item) => (
                    <tr key={item.id}>
                      <td>{item.usuario}</td>
                      <td>{formatCurrency(Number(item.importe || 0), item.moneda)}</td>
                      <td>{item.moneda}</td>
                      <td>{item.fecha}</td>
                      <td>{item.cuenta}</td>
                      <td>
                        {item.justificanteData ? (
                          <a href={item.justificanteData.dataUrl || '#'} target="_blank" rel="noreferrer" style={{ color: '#2563eb' }}>
                            {item.justificante}
                          </a>
                        ) : (
                          item.justificante
                        )}
                      </td>
                      <td>{item.estado}</td>
                      <td>{item.comentarios || 'Sin comentarios'}</td>
                      <td>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                          <button
                            className="btn-action"
                            onClick={() => updateAportacionStatus(item.id, 'Activa', 'Aportación validada manualmente por el administrador.')}
                            disabled={item.estado === 'Activa'}
                            style={{
                              opacity: item.estado === 'Activa' ? 0.6 : 1,
                              cursor: item.estado === 'Activa' ? 'default' : 'pointer',
                              backgroundColor: item.estado === 'Activa' ? '#10b981' : undefined,
                              color: item.estado === 'Activa' ? 'white' : undefined
                            }}
                          >
                            {item.estado === 'Activa' ? '✓ Validada' : 'Validar'}
                          </button>
                          <button
                            className="btn-action"
                            onClick={() => updateAportacionStatus(item.id, 'Rechazada', 'La aportación fue rechazada por documentación no válida.')}
                            disabled={item.estado === 'Rechazada'}
                            style={{
                              opacity: item.estado === 'Rechazada' ? 0.6 : 1,
                              cursor: item.estado === 'Rechazada' ? 'default' : 'pointer',
                              backgroundColor: item.estado === 'Rechazada' ? '#ef4444' : undefined,
                              color: item.estado === 'Rechazada' ? 'white' : undefined
                            }}
                          >
                            {item.estado === 'Rechazada' ? '✗ Rechazada' : 'Rechazar'}
                          </button>
                          <button
                            className="btn-action"
                            onClick={() => updateAportacionStatus(item.id, 'Información solicitada', 'Se solicita información adicional.')}
                            disabled={item.estado === 'Información solicitada'}
                            style={{
                              opacity: item.estado === 'Información solicitada' ? 0.6 : 1,
                              cursor: item.estado === 'Información solicitada' ? 'default' : 'pointer',
                              backgroundColor: item.estado === 'Información solicitada' ? '#f59e0b' : undefined,
                              color: item.estado === 'Información solicitada' ? 'white' : undefined
                            }}
                          >
                            {item.estado === 'Información solicitada' ? '⏱ Información solicitada' : 'Solicitar información'}
                          </button>
                        </div>
                      </td>
                    </tr>
                  )) : (
                    <tr><td colSpan="9">No hay aportaciones registradas.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === 'retiros' && (
            <RetirosCreditoPanel />
          )}

          {activeTab === 'solicitudes' && (
            <div className="card">
              <div className="section-header"><h2>Solicitudes de inversores</h2></div>
              {table(
                ['Nombre', 'Email', 'Teléfono', 'País', 'Fecha', 'Estado', 'Acción'],
                solicitudesPendientes.length
                  ? solicitudesPendientes.map((solicitud) => [
                    solicitud.nombre || 'Sin nombre',
                    solicitud.email || '—',
                    solicitud.telefono || '—',
                    solicitud.pais || '—',
                    solicitud.fecha || '—',
                    solicitud.estado || 'Pendiente de validación',
                    <div key={solicitud.id} style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                      <button
                        className="btn-action"
                        onClick={() => updateSolicitud(solicitud.id, 'Validada')}
                        disabled={solicitud.estado === 'Validada'}
                        style={{
                          opacity: solicitud.estado === 'Validada' ? 0.6 : 1,
                          cursor: solicitud.estado === 'Validada' ? 'default' : 'pointer',
                          backgroundColor: solicitud.estado === 'Validada' ? '#10b981' : undefined,
                          color: solicitud.estado === 'Validada' ? 'white' : undefined
                        }}
                      >
                        {solicitud.estado === 'Validada' ? '✓ Validada' : 'Validar'}
                      </button>
                      <button
                        className="btn-action"
                        onClick={() => updateSolicitud(solicitud.id, 'Rechazada')}
                        disabled={solicitud.estado === 'Rechazada'}
                        style={{
                          opacity: solicitud.estado === 'Rechazada' ? 0.6 : 1,
                          cursor: solicitud.estado === 'Rechazada' ? 'default' : 'pointer',
                          backgroundColor: solicitud.estado === 'Rechazada' ? '#ef4444' : undefined,
                          color: solicitud.estado === 'Rechazada' ? 'white' : undefined
                        }}
                      >
                        {solicitud.estado === 'Rechazada' ? '✗ Rechazada' : 'Rechazar'}
                      </button>
                    </div>
                  ])
                  : [['Sin solicitudes', '—', '—', '—', '—', 'Sin datos', '—']]
              )}
            </div>
          )}

          {activeTab === 'usuarios' && (
            <div className="card">
              <div className="section-header"><h2>Usuarios</h2></div>
              {table(
                ['Nombre', 'Email', 'Teléfono', 'País', 'Fecha', 'Rol', 'Estado', 'Acción'],
                usuariosRegistrados.length
                  ? usuariosRegistrados.map((usuario) => [
                    usuario.name || 'Sin nombre',
                    usuario.email || '—',
                    usuario.telefono || '—',
                    usuario.pais || '—',
                    usuario.fecha || '—',
                    usuario.role || 'inversor',
                    'Activo',
                    <button
                      key={`chat-${usuario.id}`}
                      className="btn-action"
                      onClick={() => { setSeleccionadoChat(usuario.name || 'Sin nombre'); setActiveTab('chat') }}
                      style={{ backgroundColor: '#0284c7', color: 'white' }}
                    >
                      💬 Chat
                    </button>
                  ])
                  : [['Sin registros', '—', '—', '—', '—', '—', 'Sin datos', '—']]
              )}
            </div>
          )}
          {activeTab === 'operaciones' && (
            <div className="card">
              <div className="section-header"><h2>💰 Pagos de Rentabilidad Semanal</h2></div>
              <div style={{ marginTop: '1.5rem', padding: '1.5rem', backgroundColor: '#f0fdf4', borderRadius: '8px', border: '1px solid #86efac' }}>
                <h4 style={{ marginTop: 0, color: '#374151' }}>📊 Inversiones elegibles para pagar hoy:</h4>
                {getInversionesElegibles().length > 0 ? (
                  <div style={{ display: 'grid', gap: '0.75rem' }}>
                    {getInversionesElegibles().map(aportacion => {
                      const proximoPago = calcularProximoPago(aportacion.fechaUltimoPago, aportacion.fechaOriginal)
                      const proximoPagoFormato = proximoPago.toLocaleDateString('es-ES')
                      return (
                        <div key={aportacion.id} style={{ padding: '12px', backgroundColor: 'white', borderRadius: '6px', border: '1px solid #e5e7eb', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '14px' }}>
                          <div>
                            <strong>{aportacion.usuario}</strong>
                            <div style={{ color: '#6b7280', fontSize: '12px', marginTop: '4px' }}>📅 Inicio: {new Date(aportacion.fechaOriginal).toLocaleDateString('es-ES')}{aportacion.fechaUltimoPago && ` · Últm pago: ${new Date(aportacion.fechaUltimoPago).toLocaleDateString('es-ES')}`}</div>
                            <div style={{ color: '#6b7280', fontSize: '12px' }}>💰 Capital: €{aportacion.importe} {aportacion.moneda} · Próx pago: {proximoPagoFormato}</div>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                ) : (
                  <div style={{ color: '#6b7280', fontStyle: 'italic' }}>No hay inversores activos</div>
                )}
                <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid #d1d5db' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600', color: '#374151' }}>Porcentaje semanal (%):</label>
                  <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                    <input type="number" value={porcentajeSemanal} onChange={(e) => setPorcentajeSemanal(e.target.value)} placeholder="Ej: 0.5" min="0" step="0.01" style={{ padding: '8px 12px', border: '1px solid #d1d5db', borderRadius: '6px', flex: 1, maxWidth: '150px' }} />
                    <button onClick={pagarRentabilidadSemanal} style={{ padding: '8px 16px', backgroundColor: '#3b82f6', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: '600', fontSize: '14px', whiteSpace: 'nowrap' }}>
                      💳 Pagar rentabilidad
                    </button>
                  </div>
                  <div style={{ marginTop: '1rem', fontSize: '12px', color: '#6b7280' }}>
                    Inversiones elegibles: {getInversionesElegibles().length}
                  </div>
                  {porcentajeSemanal && getInversionesElegibles().length > 0 && (
                    <div style={{ marginTop: '1rem', padding: '12px', backgroundColor: '#ecfdf5', borderRadius: '6px', border: '2px solid #10b981', display: 'flex', justifyContent: 'space-between' }}>
                      <strong style={{ color: '#065f46' }}>Total a pagar:</strong>
                      <strong style={{ color: '#10b981', fontSize: '16px' }}>
                        €{(getInversionesElegibles().reduce((sum, a) => sum + (Number(a.importe) * Number(porcentajeSemanal) / 100), 0).toFixed(2))}
                      </strong>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
          {activeTab === 'capital' && (
            <div className="card">
              <div className="section-header"><h2>Capital y movimientos</h2></div>

              {/* Tabla de Capital por Usuario */}
              {table(
                ['Usuario', 'Capital Total', 'Pool Activo (300%)', 'Total Retiros'],
                (() => {
                  const usuariosMap = new Map()

                  // Agrupar aportaciones por usuario
                  aportacionesNormalizadas.forEach(aport => {
                    if (!usuariosMap.has(aport.usuario)) {
                      usuariosMap.set(aport.usuario, {
                        capital: 0,
                        ganancias: 0,
                        retiros: 0,
                        aportaciones: []
                      })
                    }
                    const user = usuariosMap.get(aport.usuario)
                    const importe = Number(aport.importe || 0)
                    user.capital += importe
                    user.aportaciones.push(aport)
                    // Pool Activo = capital × 3 (si es activa)
                    if (aport.estado === 'Activa' || aport.estado === 'Validada') {
                      user.ganancias += importe * 3 // pool total es importe × 3
                    }
                  })

                  // Agrupar retiros por usuario
                  retiros.forEach(retiro => {
                    if (usuariosMap.has(retiro.usuario)) {
                      const user = usuariosMap.get(retiro.usuario)
                      if (retiro.estado === 'Aprobado' || retiro.estado === 'Procesado') {
                        user.retiros += Number(retiro.monto || 0)
                      }
                    }
                  })

                  // Convertir a array y mapear a filas de tabla
                  return Array.from(usuariosMap.entries()).map(([usuario, data]) => {
                    return [
                      usuario,
                      formatCurrency(data.capital, 'EUR'),
                      formatCurrency(data.ganancias, 'EUR'),
                      formatCurrency(data.retiros, 'EUR')
                    ]
                  })
                })()
              )}
            </div>
          )}
          {activeTab === 'referidos' && (
            <div className="card">
              <div className="section-header"><h2>🎯 Sistema de Referidos</h2></div>

              {/* Tu código de referido */}
              <div style={{ marginTop: '1.5rem', padding: '1.5rem', backgroundColor: '#fef3c7', borderRadius: '8px', border: '2px solid #f59e0b' }}>
                <h3 style={{ marginTop: 0, color: '#92400e' }}>📌 Tu Enlace de Referido</h3>
                <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', marginBottom: '1rem' }}>
                  <input
                    type="text"
                    value={`https://capitaltradeiberia.com?ref=${getCodigoReferidoAdmin().codigo}`}
                    readOnly
                    style={{ flex: 1, padding: '10px 12px', border: '1px solid #d1d5db', borderRadius: '6px', fontFamily: 'monospace', fontSize: '14px' }}
                  />
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(`https://capitaltradeiberia.com?ref=${getCodigoReferidoAdmin().codigo}`)
                      setMensaje('✅ Enlace copiado al portapapeles')
                      setTimeout(() => setMensaje(''), 2000)
                    }}
                    style={{ padding: '10px 16px', backgroundColor: '#f59e0b', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: '600' }}
                  >
                    📋 Copiar
                  </button>
                </div>
                <p style={{ color: '#78350f', fontSize: '14px', margin: 0 }}>Comparte este enlace. Cada usuario que se registre con él, tú ganas 10% de su inversión.</p>
              </div>

              {/* Estadísticas de referidos */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1.5rem' }}>
                <div style={{ padding: '1rem', backgroundColor: '#ecfdf5', borderRadius: '8px', border: '1px solid #86efac' }}>
                  <h4 style={{ marginTop: 0, color: '#065f46' }}>👥 Referidos activos</h4>
                  <p style={{ fontSize: '24px', fontWeight: 'bold', margin: '0.5rem 0 0 0', color: '#10b981' }}>{getReferidosDelAdmin().length}</p>
                </div>
                <div style={{ padding: '1rem', backgroundColor: '#f0fdf4', borderRadius: '8px', border: '1px solid #86efac' }}>
                  <h4 style={{ marginTop: 0, color: '#065f46' }}>💰 Comisiones Ganadas (10%)</h4>
                  <p style={{ fontSize: '24px', fontWeight: 'bold', margin: '0.5rem 0 0 0', color: '#10b981' }}>
                    €{getReferidosDelAdmin().reduce((sum, ref) => sum + ((ref.inversionTotal || 0) * 0.1), 0).toFixed(2)}
                  </p>
                </div>
                <div style={{ padding: '1rem', backgroundColor: '#f0fdf4', borderRadius: '8px', border: '1px solid #86efac' }}>
                  <h4 style={{ marginTop: 0, color: '#065f46' }}>📊 Inversión total de referidos</h4>
                  <p style={{ fontSize: '24px', fontWeight: 'bold', margin: '0.5rem 0 0 0', color: '#10b981' }}>
                    €{getReferidosDelAdmin().reduce((sum, ref) => sum + (ref.inversionTotal || 0), 0).toFixed(2)}
                  </p>
                </div>
              </div>

              {/* Tabla de inversiones activas con ganancias disponibles */}
              <div style={{ marginTop: '2rem' }}>
                <h3 style={{ color: '#374151', marginBottom: '1rem' }}>📋 Inversiones Activas (Pool de Ganancias)</h3>
                {aportacionesNormalizadas.filter(a => a.estado === 'Activa' || a.estado === 'Validada').length > 0 ? (
                  <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
                      <thead>
                        <tr style={{ backgroundColor: '#f3f4f6', borderBottom: '2px solid #e5e7eb' }}>
                          <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>👤 Usuario</th>
                          <th style={{ padding: '12px', textAlign: 'right', fontWeight: '600' }}>💵 Inversión</th>
                          <th style={{ padding: '12px', textAlign: 'right', fontWeight: '600' }}>📊 Ganancias Disponibles</th>
                          <th style={{ padding: '12px', textAlign: 'right', fontWeight: '600' }}>⚡ % Restante</th>
                          <th style={{ padding: '12px', textAlign: 'center', fontWeight: '600' }}>📅 Estado</th>
                        </tr>
                      </thead>
                      <tbody>
                        {aportacionesNormalizadas.filter(a => a.estado === 'Activa' || a.estado === 'Validada').map((aportacion, idx) => {
                          const gananciasDisp = Number(aportacion.gananciasDisponibles || aportacion.importe * 3)
                          const totalGanancias = aportacion.importe * 3
                          const porcentajeRestante = ((gananciasDisp / totalGanancias) * 100).toFixed(1)
                          const colorBarra = porcentajeRestante > 66 ? '#10b981' : porcentajeRestante > 33 ? '#f59e0b' : '#ef4444'
                          return (
                            <tr key={idx} style={{ borderBottom: '1px solid #e5e7eb', backgroundColor: idx % 2 === 0 ? '#f9fafb' : 'white' }}>
                              <td style={{ padding: '12px' }}><strong>{aportacion.usuario}</strong></td>
                              <td style={{ padding: '12px', textAlign: 'right' }}>€{Number(aportacion.importe).toLocaleString('es-ES')}</td>
                              <td style={{ padding: '12px', textAlign: 'right' }}>
                                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '8px' }}>
                                  <div style={{ width: '100px', height: '20px', backgroundColor: '#e5e7eb', borderRadius: '10px', overflow: 'hidden' }}>
                                    <div style={{ width: `${porcentajeRestante}%`, height: '100%', backgroundColor: colorBarra, transition: 'width 0.3s ease' }}></div>
                                  </div>
                                  <span style={{ fontWeight: '600', minWidth: '80px' }}>€{gananciasDisp.toFixed(2)}</span>
                                </div>
                              </td>
                              <td style={{ padding: '12px', textAlign: 'right', fontWeight: '600', color: colorBarra }}>{porcentajeRestante}%</td>
                              <td style={{ padding: '12px', textAlign: 'center' }}>
                                <span style={{ display: 'inline-block', padding: '4px 12px', backgroundColor: '#dbeafe', color: '#1e40af', borderRadius: '20px', fontSize: '12px', fontWeight: '600' }}>
                                  {aportacion.estado}
                                </span>
                              </td>
                            </tr>
                          )
                        })}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p style={{ color: '#6b7280', textAlign: 'center', padding: '2rem' }}>No hay inversiones activas</p>
                )}
              </div>

              {/* Tabla de referidos */}
              <div style={{ marginTop: '2rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                  <h3 style={{ color: '#374151', margin: 0 }}>🌐 Historial de Referidos</h3>
                  <button
                    onClick={pagarComisionesReferidos}
                    style={{ padding: '8px 16px', backgroundColor: '#10b981', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: '600', fontSize: '14px' }}
                  >
                    💳 Pagar Comisiones
                  </button>
                </div>
                {getReferidosDelAdmin().length > 0 ? (
                  <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
                      <thead>
                        <tr style={{ backgroundColor: '#f3f4f6', borderBottom: '2px solid #e5e7eb' }}>
                          <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>👤 Referido</th>
                          <th style={{ padding: '12px', textAlign: 'right', fontWeight: '600' }}>💵 Inversión</th>
                          <th style={{ padding: '12px', textAlign: 'right', fontWeight: '600' }}>🎁 Comisión (10%)</th>
                          <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>📅 Fecha</th>
                        </tr>
                      </thead>
                      <tbody>
                        {getReferidosDelAdmin().map((referido, idx) => {
                          const comision = referido.inversionTotal * 0.1
                          return (
                            <tr key={idx} style={{ borderBottom: '1px solid #e5e7eb', backgroundColor: idx % 2 === 0 ? '#f9fafb' : 'white' }}>
                              <td style={{ padding: '12px' }}><strong>{referido.nombreReferido || 'Usuario'}</strong></td>
                              <td style={{ padding: '12px', textAlign: 'right' }}>€{Number(referido.inversionTotal || 0).toLocaleString('es-ES')}</td>
                              <td style={{ padding: '12px', textAlign: 'right', fontWeight: '600', color: '#10b981' }}>€{comision.toFixed(2)}</td>
                              <td style={{ padding: '12px', color: '#6b7280', fontSize: '12px' }}>{new Date(referido.fecha || Date.now()).toLocaleDateString('es-ES')}</td>
                            </tr>
                          )
                        })}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p style={{ color: '#6b7280', textAlign: 'center', padding: '2rem' }}>Aún no tienes referidos. Comparte tu enlace para empezar a ganar.</p>
                )}
              </div>

              {/* Gráfico de distribución de ganancias */}
              <div style={{ marginTop: '2rem', padding: '1.5rem', backgroundColor: '#f9fafb', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
                <h3 style={{ marginTop: 0, color: '#374151' }}>📈 Análisis de Ganancias</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '1rem' }}>
                  {/* Pie chart simple */}
                  <div style={{ textAlign: 'center' }}>
                    <h4 style={{ color: '#6b7280' }}>Distribución de Ganancias</h4>
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap: '12px', height: '200px', marginTop: '1rem' }}>
                      <div style={{ width: '60px', backgroundColor: '#10b981', borderRadius: '8px 8px 0 0', height: `${(getReferidosDelAdmin().length / (aportacionesNormalizadas.filter(a => a.estado === 'Activa' || a.estado === 'Validada').length || 1)) * 100 || 10}%`, display: 'flex', alignItems: 'flex-end', justifyContent: 'center', color: 'white', fontSize: '12px', fontWeight: '600', paddingBottom: '8px' }}>
                        Referidos
                      </div>
                      <div style={{ width: '60px', backgroundColor: '#3b82f6', borderRadius: '8px 8px 0 0', height: '70%', display: 'flex', alignItems: 'flex-end', justifyContent: 'center', color: 'white', fontSize: '12px', fontWeight: '600', paddingBottom: '8px' }}>
                        Activos
                      </div>
                    </div>
                  </div>

                  {/* Resumen de pagos */}
                  <div style={{ textAlign: 'center' }}>
                    <h4 style={{ color: '#6b7280' }}>Resumen</h4>
                    <div style={{ marginTop: '1rem', textAlign: 'left', backgroundColor: 'white', padding: '1rem', borderRadius: '6px', border: '1px solid #e5e7eb' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', paddingBottom: '8px', borderBottom: '1px solid #e5e7eb' }}>
                        <span style={{ color: '#6b7280' }}>Total Referidos:</span>
                        <strong style={{ color: '#10b981' }}>{getReferidosDelAdmin().length}</strong>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', paddingBottom: '8px', borderBottom: '1px solid #e5e7eb' }}>
                        <span style={{ color: '#6b7280' }}>Inv. Total Referidos:</span>
                        <strong style={{ color: '#3b82f6' }}>€{getReferidosDelAdmin().reduce((sum, ref) => sum + (ref.inversionTotal || 0), 0).toFixed(2)}</strong>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span style={{ color: '#6b7280' }}>Comisiones Totales (10%):</span>
                        <strong style={{ color: '#f59e0b' }}>€{getReferidosDelAdmin().reduce((sum, ref) => sum + ((ref.inversionTotal || 0) * 0.1), 0).toFixed(2)}</strong>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
          {activeTab === 'rangos' && (
            <div className="card">
              <div className="section-header"><h2>🏆 Programa de Aceleración - Rangos</h2></div>
              <p style={{ color: '#6b7280', marginBottom: '1.5rem' }}>
                Inversores que alcanzaron un rango según su inversión propia y sus referidos activos (mínimo 100 $ de inversión cada uno). Aquí ves cuánto hay que pagarles mensualmente.
              </p>

              {getRangosInversores().length > 0 ? (
                <>
                  <div className="table-container">
                    <table className="tabla-estudiantes">
                      <thead>
                        <tr>
                          <th>Inversor</th>
                          <th>Rango</th>
                          <th>Inversión propia</th>
                          <th>Referidos activos</th>
                          <th>Beneficio mensual</th>
                          <th>Duración</th>
                        </tr>
                      </thead>
                      <tbody>
                        {getRangosInversores().map((item, idx) => (
                          <tr key={idx}>
                            <td>{item.nombreInversor}</td>
                            <td>{item.rango.emoji} {item.rango.nombre}</td>
                            <td>€{item.inversionPropia.toFixed(2)}</td>
                            <td>{item.referidosActivos}</td>
                            <td style={{ fontWeight: '700', color: '#10b981' }}>€{item.rango.beneficioMensual} / mes</td>
                            <td>{item.rango.meses} meses</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: '#f0fdf4', border: '1px solid #22c55e', borderRadius: '10px' }}>
                    <strong style={{ color: '#15803d' }}>💰 Total a pagar este mes a todos los rangos: </strong>
                    <span style={{ fontWeight: '700', color: '#15803d' }}>
                      €{getRangosInversores().reduce((sum, item) => sum + item.rango.beneficioMensual, 0).toFixed(2)}
                    </span>
                  </div>
                </>
              ) : (
                <p style={{ color: '#6b7280', textAlign: 'center', padding: '2rem' }}>Aún ningún inversor ha alcanzado un rango del programa de aceleración.</p>
              )}
            </div>
          )}
          {activeTab === 'configuracion' && (
            <div className="card">
              <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h2>Métodos de pago para inversores</h2>
                <button onClick={async () => {
                  try {
                    const token = localStorage.getItem('token')
                    const res = await fetch(`${API}/api/admin/cuentas`, {
                      method: 'PUT',
                      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                      body: JSON.stringify({ cuentas })
                    })
                    setMensaje(res.ok ? '✅ Guardado correctamente' : '❌ Error guardando')
                  } catch { setMensaje('❌ Error guardando') }
                  setTimeout(() => setMensaje(''), 3000)
                }} style={{ padding: '8px 20px', background: 'linear-gradient(135deg,#f6c453,#dba93a)', color: '#0a0f1a', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '700', fontSize: '14px' }}>
                  💾 Guardar cambios
                </button>
              </div>
              <p style={{ color: '#94a3b8', fontSize: 14, margin: '0.5rem 0 1.5rem' }}>
                Esta información se mostrará a los inversores cuando vayan a realizar una aportación.
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {cuentas.map((m, i) => (
                  <div key={m.moneda} style={{ background: 'rgba(15,23,42,0.6)', border: '1px solid rgba(246,196,83,0.2)', borderRadius: 14, padding: '1.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.7rem', marginBottom: '1.2rem' }}>
                      <span style={{ fontSize: 20 }}>{m.tipo === 'wallet' ? '💎' : m.moneda === 'MLC' ? '🏦' : '💵'}</span>
                      <h3 style={{ margin: 0, color: '#f6c453', fontSize: '1.1rem' }}>{m.moneda}</h3>
                      <span style={{ fontSize: 12, color: '#94a3b8', background: 'rgba(255,255,255,0.05)', padding: '2px 10px', borderRadius: 999 }}>{m.tipo === 'wallet' ? 'Crypto wallet' : 'Tarjeta bancaria'}</span>
                    </div>
                    {m.tipo === 'wallet' ? (
                      <div style={{ display: 'grid', gap: '0.8rem' }}>
                        <div>
                          <label style={{ fontSize: 12, color: '#94a3b8', display: 'block', marginBottom: 4 }}>Dirección de wallet</label>
                          <input value={m.wallet} onChange={e => updateBankAccount(i, 'wallet', e.target.value)}
                            placeholder="0x..." style={{ width: '100%', background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(148,163,184,0.2)', borderRadius: 8, padding: '10px 12px', color: '#f1f5f9', fontFamily: 'monospace', fontSize: 14, boxSizing: 'border-box' }} />
                        </div>
                        <div>
                          <label style={{ fontSize: 12, color: '#94a3b8', display: 'block', marginBottom: 4 }}>Red</label>
                          <input value={m.red} onChange={e => updateBankAccount(i, 'red', e.target.value)}
                            placeholder="BEP-20 (BSC)" style={{ width: '100%', background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(148,163,184,0.2)', borderRadius: 8, padding: '10px 12px', color: '#f1f5f9', fontSize: 14, boxSizing: 'border-box' }} />
                        </div>
                        <div>
                          <label style={{ fontSize: 12, color: '#94a3b8', display: 'block', marginBottom: 4 }}>Instrucciones adicionales / Referencia</label>
                          <input value={m.instrucciones} onChange={e => updateBankAccount(i, 'instrucciones', e.target.value)}
                            placeholder="Ej: Indicar tu email como referencia" style={{ width: '100%', background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(148,163,184,0.2)', borderRadius: 8, padding: '10px 12px', color: '#f1f5f9', fontSize: 14, boxSizing: 'border-box' }} />
                        </div>
                        <div>
                          <label style={{ fontSize: 12, color: '#94a3b8', display: 'block', marginBottom: 4 }}>Monto mínimo requerido (en {m.moneda})</label>
                          <input type="number" value={m.minimo || ''} onChange={e => updateBankAccount(i, 'minimo', e.target.value)}
                            placeholder="Ej: 50" style={{ width: '100%', background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(148,163,184,0.2)', borderRadius: 8, padding: '10px 12px', color: '#f1f5f9', fontSize: 14, boxSizing: 'border-box' }} />
                        </div>
                      </div>
                    ) : m.tipo === 'tarjeta' ? (
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.8rem' }}>
                        {[['Número de tarjeta', 'numero', '0000 0000 0000 0000'], ['Monto mínimo (opcional)', 'minimo', 'Ej: 100'], ['Instrucciones', 'instrucciones', 'Ej: Indicar tu email como referencia']].map(([label, field, ph]) => (
                          <div key={field} style={{ gridColumn: field === 'instrucciones' ? 'span 2' : 'auto' }}>
                            <label style={{ fontSize: 12, color: '#94a3b8', display: 'block', marginBottom: 4 }}>{label}</label>
                            <input value={m[field] || ''} onChange={e => updateBankAccount(i, field, e.target.value)} type={field === 'minimo' ? 'number' : 'text'}
                              placeholder={ph}
                              style={{ width: '100%', padding: '0.6rem', borderRadius: 8, background: '#07111f', border: '1px solid #1e293b', color: '#f8fafc' }} />
                          </div>
                        ))}
                      </div>
                    ) : m.tipo === 'iban' ? (
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.8rem' }}>
                        {[['Titular', 'titular', 'Nombre completo'], ['IBAN', 'iban', 'ES00...'], ['Concepto', 'concepto', 'Ej: Nombre y Apellido'], ['Monto mínimo (opcional)', 'minimo', 'Ej: 500']].map(([label, field, ph]) => (
                          <div key={field} style={{ gridColumn: 'auto' }}>
                            <label style={{ fontSize: 12, color: '#94a3b8', display: 'block', marginBottom: 4 }}>{label}</label>
                            <input value={m[field] || ''} onChange={e => updateBankAccount(i, field, e.target.value)} type={field === 'minimo' ? 'number' : 'text'}
                              placeholder={ph}
                              style={{ width: '100%', padding: '0.6rem', borderRadius: 8, background: '#07111f', border: '1px solid #1e293b', color: '#f8fafc' }} />
                          </div>
                        ))}
                      </div>
                    ) : null}
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'depositos' && (
            <div className="card">
              <div className="section-header"><h2>Solicitudes de Depósito Pendientes</h2></div>
              {table(
                ['ID', 'Nombre', 'Email', 'Importe', 'Moneda', 'Fecha', 'Estado', 'Acción'],
                solicitudesInversion.length
                  ? solicitudesInversion.map((solicitud) => [
                    solicitud.id,
                    solicitud.nombre || '—',
                    solicitud.email || '—',
                    formatCurrency(solicitud.importe, solicitud.moneda),
                    solicitud.moneda,
                    new Date(solicitud.fecha).toLocaleDateString('es-ES'),
                    solicitud.estado || 'Pendiente',
                    <button
                      className="btn-action"
                      style={{ backgroundColor: '#10b981', color: 'white' }}
                    >
                      ✓ Validar depósito
                    </button>
                  ])
                  : [['Sin solicitudes', '—', '—', '—', '—', '—', '—', '—']]
              )}
            </div>
          )}

          {activeTab === 'chat' && (
            <div className="card">
              <div className="section-header">
                <h2>💬 Sistema de chat con inversores</h2>
                <div style={{ fontSize: '12px', color: '#6b7280' }}>
                  Total de mensajes sin leer: <strong>{mensajes.filter(m => m.tipo === 'inversor' && !m.leido).length}</strong>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: seleccionadoChat ? '250px 1fr' : '1fr', gap: '1rem', minHeight: '600px' }}>
                {/* Panel de inversores */}
                <div style={{
                  border: '1px solid #dfe3ea',
                  borderRadius: '12px',
                  overflow: 'hidden',
                  display: 'flex',
                  flexDirection: 'column'
                }}>
                  <div style={{
                    backgroundColor: '#f3f4f6',
                    padding: '1rem',
                    borderBottom: '1px solid #dfe3ea',
                    fontWeight: '600',
                    color: '#374151'
                  }}>
                    📧 Conversaciones
                  </div>

                  <div style={{ overflowY: 'auto', flex: 1 }}>
                    {(() => {
                      const inversoresUnicos = {}
                      mensajes.forEach(msg => {
                        if (msg.tipo === 'inversor') {
                          if (!inversoresUnicos[msg.usuarioNombre]) {
                            inversoresUnicos[msg.usuarioNombre] = []
                          }
                          inversoresUnicos[msg.usuarioNombre].push(msg)
                        }
                      })

                      return Object.entries(inversoresUnicos).length === 0 ? (
                        <div style={{ padding: '1rem', color: '#6b7280', textAlign: 'center', marginTop: '2rem' }}>
                          Sin mensajes aún
                        </div>
                      ) : (
                        Object.entries(inversoresUnicos).map(([nombre, msgs]) => {
                          const noLeidos = msgs.filter(m => !m.leido).length
                          const ultimoMsg = msgs[msgs.length - 1]
                          return (
                            <div
                              key={nombre}
                              onClick={() => setSeleccionadoChat(nombre)}
                              style={{
                                padding: '1rem',
                                borderBottom: '1px solid #e5e7eb',
                                cursor: 'pointer',
                                backgroundColor: seleccionadoChat === nombre ? '#eff6ff' : 'white',
                                borderLeft: seleccionadoChat === nombre ? '4px solid #0284c7' : 'none'
                              }}
                            >
                              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                                <div style={{ fontWeight: '600', color: '#1f2937' }}>{nombre}</div>
                                {noLeidos > 0 && (
                                  <span style={{
                                    backgroundColor: '#ef4444',
                                    color: 'white',
                                    borderRadius: '50%',
                                    width: '20px',
                                    height: '20px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontSize: '12px',
                                    fontWeight: 'bold'
                                  }}>
                                    {noLeidos}
                                  </span>
                                )}
                              </div>
                              <div style={{ fontSize: '12px', color: '#6b7280', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                {ultimoMsg.mensaje.substring(0, 40)}...
                              </div>
                              <div style={{ fontSize: '11px', color: '#9ca3af', marginTop: '0.25rem' }}>
                                {ultimoMsg.fecha}
                              </div>
                            </div>
                          )
                        })
                      )
                    })()}
                  </div>
                </div>

                {/* Panel de mensajes */}
                {seleccionadoChat ? (
                  <div style={{
                    border: '1px solid #dfe3ea',
                    borderRadius: '12px',
                    overflow: 'hidden',
                    display: 'flex',
                    flexDirection: 'column'
                  }}>
                    <div style={{
                      backgroundColor: '#f3f4f6',
                      padding: '1rem',
                      borderBottom: '1px solid #dfe3ea',
                      fontWeight: '600',
                      color: '#374151'
                    }}>
                      {seleccionadoChat}
                    </div>

                    <div style={{ overflowY: 'auto', flex: 1, padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      {(() => {
                        const msgsDelInversor = mensajes.filter(m => m.usuarioNombre === seleccionadoChat)
                        return msgsDelInversor.length === 0 ? (
                          <div style={{ color: '#6b7280', textAlign: 'center', marginTop: '2rem' }}>
                            Sin mensajes
                          </div>
                        ) : (
                          msgsDelInversor.map(msg => (
                            <div
                              key={msg.id}
                              style={{
                                backgroundColor: msg.tipo === 'inversor' ? '#e5e7eb' : '#dbeafe',
                                padding: '0.75rem 1rem',
                                borderRadius: '8px',
                                maxWidth: '80%',
                                alignSelf: msg.tipo === 'inversor' ? 'flex-start' : 'flex-end',
                                wordWrap: 'break-word'
                              }}
                            >
                              <div style={{ fontSize: '12px', fontWeight: '600', color: '#374151', marginBottom: '0.25rem' }}>
                                {msg.tipo === 'inversor' ? msg.usuarioNombre : 'Tú (Admin)'}
                              </div>
                              <div style={{ fontSize: '14px', color: '#1f2937' }}>
                                {msg.mensaje}
                              </div>
                              <div style={{ fontSize: '11px', color: '#6b7280', marginTop: '0.5rem' }}>
                                {msg.fecha}
                              </div>
                            </div>
                          ))
                        )
                      })()}
                    </div>

                    <div style={{
                      borderTop: '1px solid #dfe3ea',
                      padding: '1rem',
                      display: 'flex',
                      gap: '0.5rem'
                    }}>
                      <textarea
                        value={respuesta}
                        onChange={(e) => setRespuesta(e.target.value)}
                        placeholder="Escribe tu respuesta..."
                        style={{
                          flex: 1,
                          padding: '0.75rem',
                          border: '1px solid #d1d5db',
                          borderRadius: '6px',
                          fontSize: '14px',
                          fontFamily: 'inherit',
                          minHeight: '80px',
                          resize: 'vertical'
                        }}
                      />
                      <button
                        onClick={async () => {
                          if (!respuesta.trim()) {
                            alert('Escribe un mensaje')
                            return
                          }
                          try {
                            const token = localStorage.getItem('token')
                            const response = await fetch('${API}/api/comunidad/mensajes', {
                              method: 'POST',
                              headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${token}`
                              },
                              body: JSON.stringify({
                                mensaje: respuesta.trim(),
                                destinatario: seleccionadoChat
                              })
                            })
                            if (response.ok) {
                              setRespuesta('')
                              setMensaje('✅ Respuesta enviada')
                            } else {
                              setMensaje('❌ Error enviando respuesta')
                            }
                          } catch (error) {
                            console.error('Error:', error)
                            setMensaje('❌ Error enviando respuesta')
                          }
                          setTimeout(() => setMensaje(''), 2000)
                        }}
                        style={{
                          padding: '0.75rem 1.5rem',
                          backgroundColor: '#3b82f6',
                          color: 'white',
                          border: 'none',
                          borderRadius: '6px',
                          cursor: 'pointer',
                          fontWeight: '600',
                          alignSelf: 'flex-end'
                        }}
                      >
                        Enviar
                      </button>
                    </div>
                  </div>
                ) : (
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#6b7280',
                    fontSize: '16px'
                  }}>
                    Selecciona una conversación para ver los mensajes
                  </div>
                )}
              </div>
            </div>
          )}


        </div>
      </main>
    </div>
  )
}

export default DashboardAdminExpandido

