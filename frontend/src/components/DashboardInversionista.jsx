import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import './Platform.css';
import './DashboardAdminExpandido.css';
import FondoSolidarioPanel from './FondoSolidarioPanel';
import NotificacionesCampana from './NotificacionesCampana'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const documents = [
  { name: 'Contrato operación Cemento', type: 'PDF' },
  { name: 'Anexo de condiciones', type: 'PDF' },
  { name: 'Documento de participación', type: 'DOCX' }
];

const readStorage = (key, fallback) => {
  try {
    const raw = localStorage.getItem(key)
    return raw ? JSON.parse(raw) : fallback
  } catch {
    return fallback
  }
}

const METODOS_DEFAULT_INV = [
  { moneda: 'EUR', tipo: 'iban', titular: 'Capital Iberia', iban: 'ES00...', concepto: 'Referencia de inversión', minimo: 500 },
  { moneda: 'USDT BEP-20', wallet: '0x0000000', red: 'BEP-20 (BSC)', instrucciones: 'Transferencia USDT.', minimo: 50 }
]

const mergeCuentas = (cuentas) => {
  if (!cuentas || cuentas.length === 0) return METODOS_DEFAULT_INV
  return METODOS_DEFAULT_INV.map(defaultC => {
    const existe = cuentas.find(c => c.moneda === defaultC.moneda)
    return existe ? { ...defaultC, ...existe } : defaultC
  })
}

const formatCurrency = (value, moneda = 'EUR') => {
  if (!Number.isFinite(value)) return '€0'
  if (moneda === 'USDT BEP-20') return `${Number(value).toLocaleString('es-ES')} USDT`
  return `€${Number(value).toLocaleString('es-ES')}`
}

const safeFormatDate = (dateVal) => {
  try {
    if (!dateVal) return new Date().toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' })
    let parsed = typeof dateVal === 'string' ? new Date(dateVal.replace(' ', 'T').split('.')[0]) : new Date(dateVal)
    if (isNaN(parsed.getTime())) parsed = new Date()
    return parsed.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' })
  } catch {
    return 'N/A'
  }
}

const PROGRAMA_LIDERES = [
  { nombre: 'Founding Leader', minReferidos: 500, emoji: '🏆', bonus: 400, duracion: 12 },
  { nombre: 'Executive Leader', minReferidos: 200, emoji: '👑', bonus: 250, duracion: 12 },
  { nombre: 'Elite Leader', minReferidos: 100, emoji: '💎', bonus: 150, duracion: 6 },
  { nombre: 'Senior Leader', minReferidos: 50, emoji: '🔥', bonus: 100, duracion: 4 },
  { nombre: 'Leader', minReferidos: 25, emoji: '⭐', bonus: 50, duracion: 3 },
  { nombre: 'Community', minReferidos: 5, emoji: '🌱', bonus: 25, duracion: 2 },
]

const PROGRAMA_PARTNER = [
  { nombre: 'Founding Partner', minCapital: 50000, maxCapital: 100000, emoji: '🏦', beneficioMensual: 450 },
  { nombre: 'Strategic Partner', minCapital: 25000, maxCapital: 49999, emoji: '💎', beneficioMensual: 350 },
  { nombre: 'VIP Partner', minCapital: 10000, maxCapital: 24999, emoji: '💼', beneficioMensual: 250 },
  { nombre: 'Premium Partner', minCapital: 5000, maxCapital: 9999, emoji: '✨', beneficioMensual: 150 },
  { nombre: 'Partner', minCapital: 500, maxCapital: 4999, emoji: '🤝', beneficioMensual: 50 },
]

function DashboardInversionista() {
  const navigate = useNavigate();
  const esNavegadorMovil = typeof navigator !== 'undefined' && /Android|iPhone|iPad|iPod/i.test(navigator.userAgent)
  const [activeTab, setActiveTab] = React.useState('resumen');
  const [currentUser, setCurrentUser] = React.useState(() => {
    try {
      return JSON.parse(localStorage.getItem('capital_trade_user') || 'null')
    } catch {
      return null
    }
  })
  const [aportaciones, setAportaciones] = React.useState([])
  const [retiros, setRetiros] = React.useState([])
  const [pagosRentabilidad, setPagosRentabilidad] = React.useState([])
  const [referidos, setReferidos] = React.useState([])
  const [ofertasPrivadas, setOfertasPrivadas] = React.useState([])
  const [ofertasAportaciones, setOfertasAportaciones] = React.useState([])
  const [avisosOperaciones, setAvisosOperaciones] = React.useState([])
  const [cuentasPago, setCuentasPago] = React.useState(() => mergeCuentas(readStorage('capital_trade_cuentas', [])))
  const [sidebarOpen, setSidebarOpen] = React.useState(false)
  const [mostrarTodasRetenidas, setMostrarTodasRetenidas] = React.useState(false)
  const [mostrarTodosReferidos, setMostrarTodosReferidos] = React.useState(false)
  const [montoRetiro, setMontoRetiro] = React.useState('')
  const [monedaRetiro, setMonedaRetiro] = React.useState('USDT BEP-20')
  const [notasRetiro, setNotasRetiro] = React.useState('')
  const [errorRetiro, setErrorRetiro] = React.useState('')
  const [successRetiro, setSuccessRetiro] = React.useState('')
  const [tipoRetiro, setTipoRetiro] = React.useState('banco')
  const [emailP2P, setEmailP2P] = React.useState('')

  // Estados para modal de inversión
  const [showInversionModal, setShowInversionModal] = React.useState(false)
  const [showRangosModal, setShowRangosModal] = React.useState(false)
  const [monedaInversion, setMonedaInversion] = React.useState('USDT BEP-20')
  const [montoInversion, setMontoInversion] = React.useState('')
  const [errorInversion, setErrorInversion] = React.useState('')
  const [successInversion, setSuccessInversion] = React.useState('')
  const [datoCopiado, setDatoCopiado] = React.useState('')

  // Estados para justificante
  const [showJustificante, setShowJustificante] = React.useState(false)
  const [solicitudSeleccionada, setSolicitudSeleccionada] = React.useState(null)
  const [archivoJustificante, setArchivoJustificante] = React.useState(null)
  const [errorJustificante, setErrorJustificante] = React.useState('')
  const [solicitudes, setSolicitudes] = React.useState([])

  // Estados para minimos de inversión
  const [minimos, setMinimos] = React.useState({ EUR: 500, 'USDT BEP-20': 50 })

  // Estados para chat
  const [showChatModal, setShowChatModal] = React.useState(false)
  const [mensajeChat, setMensajeChat] = React.useState('')
  const [errorChat, setErrorChat] = React.useState('')
  const [mensajes, setMensajes] = React.useState([])

  // Codigo de referido permanente del inversor (viene de su perfil, nunca cambia)
  const [codigoReferidoPropio, setCodigoReferidoPropio] = React.useState(null)
  const [referidoPorPropio, setReferidoPorPropio] = React.useState(null)
  const [esLiderPropio, setEsLiderPropio] = React.useState(false)
  const [datosComunidadLider, setDatosComunidadLider] = React.useState(null)
  const [isCardFlipped, setIsCardFlipped] = React.useState(false)
  const [isSystemLoading, setIsSystemLoading] = React.useState(true)

  React.useEffect(() => {
    const syncData = () => {
      setCurrentUser(JSON.parse(localStorage.getItem('capital_trade_user') || 'null'))
    }

    syncData()
    setTimeout(() => {
      setIsSystemLoading(false)
    }, 1500)
    window.addEventListener('storage', syncData)
    window.addEventListener('capital-trade-sync', syncData)
    const interval = setInterval(syncData, 5000)

    return () => {
      window.removeEventListener('storage', syncData)
      window.removeEventListener('capital-trade-sync', syncData)
      clearInterval(interval)
    }
  }, [])

  React.useEffect(() => {
    const cargarAvisosOperaciones = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return
        const response = await fetch(`${API_URL}/api/avisos-operaciones`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (!response.ok) return
        const data = await response.json()
        setAvisosOperaciones(data.avisos || [])
      } catch (error) {
        console.log('Error cargando avisos de operaciones:', error)
      }
    }
    cargarAvisosOperaciones()
    const intervalo = setInterval(cargarAvisosOperaciones, 30000)
    return () => clearInterval(intervalo)
  }, [])

  React.useEffect(() => {
    const cargarCuentasPago = async () => {
      try {
        const response = await fetch(`${API_URL}/api/metodos-pago`)
        if (!response.ok) return
        const data = await response.json()
        const cuentas = mergeCuentas(data.metodos || [])
        setCuentasPago(cuentas)
        localStorage.setItem('capital_trade_cuentas', JSON.stringify(cuentas))
      } catch (error) {
        console.log('Error cargando métodos de pago:', error)
      }
    }

    cargarCuentasPago()
    const intervalo = setInterval(cargarCuentasPago, 30000)
    return () => clearInterval(intervalo)
  }, [])

  // Verificar que la cuenta siga existiendo; si fue borrada, cerrar sesión
  React.useEffect(() => {
    const verificarCuenta = async () => {
      const token = localStorage.getItem('token')
      if (!token) return
      try {
        const response = await fetch(`${API_URL}/api/inversores/perfil`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (response.status === 401 || response.status === 403 || response.status === 404) {
          localStorage.removeItem('token')
          localStorage.removeItem('usuario')
          localStorage.removeItem('capital_trade_user')
          window.dispatchEvent(new Event('capital-trade-sync'))
          navigate('/login')
        } else if (response.ok) {
          const data = await response.json()
          if (data.codigo_referido) setCodigoReferidoPropio(data.codigo_referido)
          setReferidoPorPropio(data.referido_por || null)
          setEsLiderPropio(data.es_lider || false)

          if (data.es_lider) {
            const resComunidad = await fetch(`${API_URL}/api/comunidad/${data.id}`, {
              headers: { 'Authorization': `Bearer ${token}` }
            })
            if (resComunidad.ok) {
              const comData = await resComunidad.json()
              setDatosComunidadLider(comData)
            }
          }
        }
      } catch (error) {
        console.log('Error verificando cuenta:', error)
      }
    }
    verificarCuenta()
  }, [])

  // Cargar minimos desde API
  React.useEffect(() => {
    const cargarMinimos = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`${API_URL}/api/admin/config`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (response.ok) {
          const data = await response.json()
          setMinimos(data.minimos || { EUR: 500, 'USDT BEP-20': 50 })
        }
      } catch (error) {
        console.log('Error cargando minimos:', error)
      }
    }
    cargarMinimos()
    const intervalo = setInterval(cargarMinimos, 30000)
    return () => clearInterval(intervalo)
  }, [])

  // Cargar mensajes desde API
  React.useEffect(() => {
    const cargarMensajes = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`${API_URL}/api/chat-admin/mensajes`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (response.ok) {
          const data = await response.json()
          setMensajes((data.mensajes || []).map((mensaje) => ({
            ...mensaje,
            usuarioId: mensaje.autor_id,
            usuarioNombre: mensaje.autor_nombre,
            tipo: mensaje.autor_rol === 'admin' ? 'admin' : 'inversor',
            fecha: mensaje.created_at
          })))
        }
      } catch (error) {
        console.log('Error cargando mensajes:', error)
      }
    }
    cargarMensajes()
    const intervalo = setInterval(cargarMensajes, 5000)
    return () => clearInterval(intervalo)
  }, [])

  // Cargar aportaciones desde API
  React.useEffect(() => {
    const cargarAportaciones = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return

        const response = await fetch(`${API_URL}/api/aportaciones`, {
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

    const cargarReferidos = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return

        const response = await fetch(`${API_URL}/api/referidos`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.ok) {
          const data = await response.json()
          // Normalizar data para el frontend
          const refFrontend = data.referidos.map(r => ({
            id: r.id,
            codigo: r.codigo,
            nombreInversor: r.nombreInversor,
            usuarioId: r.usuarioId,
            referidoPor: r.referidoPor,
            inversionTotal: r.inversionTotal,
            pagado: r.pagado,
            esAdmin: r.esAdmin
          }))
          setReferidos(refFrontend)
        }
      } catch (error) {
        console.log('Error cargando referidos:', error)
      }
    }

    cargarAportaciones()
    cargarReferidos()
    const intervalo = setInterval(() => {
      cargarAportaciones()
      cargarReferidos()
    }, 5000)

    return () => clearInterval(intervalo)
  }, [])

  const enviarMensajeChat = async () => {
    if (!mensajeChat.trim()) return
    setErrorChat('')
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${API_URL}/api/chat-admin/mensajes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ mensaje: mensajeChat.trim(), destinatario: 'admin' })
      })
      if (!response.ok) throw new Error('Error enviando mensaje')
      setMensajeChat('')
      setShowChatModal(false)
    } catch (error) {
      setErrorChat('Error enviando mensaje. Inténtalo de nuevo.')
    }
  }

  // Cargar retiros y ofertas desde API
  React.useEffect(() => {
    const cargarRetiros = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return

        const response = await fetch(`${API_URL}/api/retiros`, {
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

    const cargarOfertas = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return
        const [resOfertas, resAportaciones] = await Promise.all([
          fetch(`${API_URL}/api/ofertas`, { headers: { 'Authorization': `Bearer ${token}` } }),
          fetch(`${API_URL}/api/ofertas/aportaciones`, { headers: { 'Authorization': `Bearer ${token}` } })
        ])
        if (resOfertas.ok) {
          const dataOfertas = await resOfertas.json()
          setOfertasPrivadas(dataOfertas.ofertas || [])
        }
        if (resAportaciones.ok) {
          const dataAportaciones = await resAportaciones.json()
          setOfertasAportaciones(dataAportaciones.aportaciones || [])
        }
      } catch (error) {
        console.log('Error cargando ofertas API:', error)
      }
    }

    cargarRetiros()
    cargarOfertas()
    const intervalo = setInterval(() => {
      cargarRetiros()
      cargarOfertas()
    }, 5000)

    return () => clearInterval(intervalo)
  }, [])

  React.useEffect(() => {
    const cargarPagosRentabilidad = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) return
        const response = await fetch(`${API_URL}/api/pagos-rentabilidad`, { headers: { 'Authorization': `Bearer ${token}` } })
        if (response.ok) {
          const data = await response.json()
          setPagosRentabilidad(data.pagos || [])
        }
      } catch (error) {
        console.log('Error cargando historial de pagos:', error)
      }
    }
    cargarPagosRentabilidad()
    const intervalo = setInterval(cargarPagosRentabilidad, 10000)
    return () => clearInterval(intervalo)
  }, [])

  const userAportaciones = aportaciones.filter((item) => {
    const userId = currentUser?.id
    const userName = currentUser?.name || currentUser?.nombre
    return String(item.inversor_id ?? '') === String(userId ?? '') ||
      item.usuarioId === userId || item.usuarioNombre === userName || item.usuario === userName || item.nombre === userName
  })

  const userRetiros = retiros.filter((item) => {
    const userId = currentUser?.id
    const userName = currentUser?.name || currentUser?.nombre
    return String(item.inversor_id ?? '') === String(userId ?? '') ||
      item.usuarioId === userId || item.usuarioNombre === userName || item.usuario === userName || item.nombre === userName
  })

  const totalAportado = userAportaciones
    .filter((item) => item.estado === 'Activa' || item.estado === 'Validada')
    .reduce((sum, item) => sum + Number(item.importe || 0), 0)

  const totalRetirado = userRetiros
    .filter((item) => item.estado === 'Aprobado' || item.estado === 'Procesado')
    .reduce((sum, item) => sum + Number(item.importe || 0), 0)

  const totalGananciasPosibles = userAportaciones
    .filter((item) => item.estado === 'Activa' || item.estado === 'Validada')
    .reduce((sum, item) => {
      const gananciasDis = item.gananciasDisponibles !== undefined ? Number(item.gananciasDisponibles) : Number(item.importe || 0) * 3
      return sum + gananciasDis
    }, 0)

  // Dinero ganado realmente = Pool inicial - Pool actual
  const gananciasGeneradas = userAportaciones
    .filter((item) => item.estado === 'Activa' || item.estado === 'Validada')
    .reduce((sum, item) => {
      const inicial = Number(item.importe || 0) * 3
      const actual = Number(item.gananciasDisponibles !== undefined ? item.gananciasDisponibles : item.importe * 3)
      return sum + (inicial - actual)
    }, 0)

  // Saldo disponible para retirar = Lo que ha ganado - Lo que ya retiró
  const capitalDisponible = Math.max(gananciasGeneradas - totalRetirado, 0)

  const saldosPorMoneda = userAportaciones
    .filter((item) => item.estado === 'Activa' || item.estado === 'Validada')
    .reduce((saldos, item) => {
      const moneda = item.moneda || 'EUR'
      const inicial = Number(item.importe || 0) * 3
      const pendiente = Number(item.gananciasDisponibles !== undefined ? item.gananciasDisponibles : item.importe * 3)
      const saldo = saldos[moneda] || { aportado: 0, gananciasPosibles: 0, disponible: 0, retenido: 0, retirado: 0 }
      saldo.aportado += Number(item.importe || 0)
      saldo.gananciasPosibles += pendiente
      saldo.disponible += Math.max(0, inicial - pendiente)
      saldos[moneda] = saldo
      return saldos
    }, {})

  userRetiros
    .filter((item) => item.estado === 'Aprobado' || item.estado === 'Procesado')
    .forEach((item) => {
      const moneda = item.moneda || 'EUR'
      const saldo = saldosPorMoneda[moneda] || { aportado: 0, gananciasPosibles: 0, disponible: 0, retenido: 0, retirado: 0 }
      saldo.retirado += Number(item.importe || 0)
      saldosPorMoneda[moneda] = saldo
    })

  // Reloj en vivo para la cuenta regresiva de bloqueo de 72 horas
  const [ahora, setAhora] = React.useState(Date.now())
  React.useEffect(() => {
    const t = setInterval(() => setAhora(Date.now()), 1000)
    return () => clearInterval(t)
  }, [])

  const HORAS_BLOQUEO = 72
  const aportacionesRetenidas = userAportaciones.filter((item) => {
    if (item.estado !== 'Activa' && item.estado !== 'Validada') return false
    if (!item.fecha_aprobacion) return false
    return new Date(item.fecha_aprobacion + (item.fecha_aprobacion.includes('Z') ? '' : 'Z')).getTime() + HORAS_BLOQUEO * 3600000 > ahora
  })
  const capitalRetenido = aportacionesRetenidas.reduce((sum, item) => sum + Number(item.importe || 0), 0)
  const capitalActivo = totalAportado - capitalRetenido
  aportacionesRetenidas.forEach((item) => {
    const moneda = item.moneda || 'EUR'
    const saldo = saldosPorMoneda[moneda] || { aportado: 0, gananciasPosibles: 0, disponible: 0, retenido: 0, retirado: 0 }
    saldo.retenido += Number(item.importe || 0)
    saldosPorMoneda[moneda] = saldo
  })
  const monedasConSaldo = Object.keys(saldosPorMoneda).filter((moneda) => saldosPorMoneda[moneda].disponible - saldosPorMoneda[moneda].retirado > 0)
  const saldoRetirable = Math.max(0, (saldosPorMoneda[monedaRetiro]?.disponible || 0) - (saldosPorMoneda[monedaRetiro]?.retirado || 0))
  const mostrarSaldos = (campo) => {
    const resumen = Object.entries(saldosPorMoneda)
      .map(([moneda, saldo]) => ({ moneda, valor: campo === 'retirable' ? saldo.disponible - saldo.retirado : campo === 'activo' ? saldo.aportado - saldo.retenido : saldo[campo] }))
      .filter(({ valor }) => valor > 0)
      .map(({ moneda, valor }) => formatCurrency(valor, moneda))
    return resumen.length ? resumen.join(' · ') : '—'
  }

  React.useEffect(() => {
    if (monedasConSaldo.length && !monedasConSaldo.includes(monedaRetiro)) {
      setMonedaRetiro(monedasConSaldo[0])
    }
  }, [monedasConSaldo.join('|'), monedaRetiro])
  const obtenerTiempoRetenido = (item) => {
    const restanteMs = Math.max(0, new Date(item.fecha_aprobacion + (item.fecha_aprobacion.includes('Z') ? '' : 'Z')).getTime() + HORAS_BLOQUEO * 3600000 - ahora)
    return {
      horas: Math.floor(restanteMs / 3600000),
      minutos: Math.floor((restanteMs % 3600000) / 60000),
      segundos: Math.floor((restanteMs % 60000) / 1000)
    }
  }

  // CALCULO RANGOS y OFERTAS
  const referidosActivos = referidos.filter(r => r.referidoPor === currentUser?.codigo_referido && r.estado !== 'pendiente').length
  const nivelLideres = PROGRAMA_LIDERES.find(r => referidosActivos >= r.minReferidos) || null
  const nivelPartner = PROGRAMA_PARTNER.find(r => totalAportado >= r.minCapital && totalAportado <= r.maxCapital) || (totalAportado >= 100000 ? PROGRAMA_PARTNER[0] : null)

  const ofertasAsignadas = ofertasPrivadas.filter(of => {
    if (of.estado !== 'Activa') return false
    if (of.inversorIdEspecial && currentUser && (of.inversorIdEspecial.trim().toLowerCase() === (currentUser.email || '').trim().toLowerCase() || of.inversorIdEspecial === currentUser.id?.toString())) return true
    if (of.programa === 'Comunidad' && nivelLideres && of.nivel === nivelLideres.nombre) return true
    if (of.programa === 'Capital' && nivelPartner && of.nivel === nivelPartner.nombre) return true
    if (of.programa === 'Combinado' && nivelPartner && nivelLideres && of.nivel === 'Todos los Combinados') return true
    return false
  })


  const movimientos = [
    ...userAportaciones.map((item) => ({
      date: safeFormatDate(item.createdAt),
      description: `Aportación registrada en ${item.operacionNombre || 'operación'}`,
      amount: `+${formatCurrency(Number(item.importe || 0), item.moneda || 'EUR')}`,
      tipo: 'aportacion'
    })),
    ...userRetiros.map((item) => ({
      date: safeFormatDate(item.createdAt),
      description: `Solicitud de retiro ${item.estado}`,
      amount: `-${formatCurrency(Number(item.importe || 0), item.moneda || 'EUR')}`,
      tipo: 'retiro'
    }))
  ].slice(0, 6)

  const handleRetiroSubmit = async (e) => {
    e.preventDefault()
    setErrorRetiro('')
    setSuccessRetiro('')

    const importe = Number(montoRetiro)
    if (!montoRetiro || Number.isNaN(importe) || importe <= 0) {
      setErrorRetiro('Introduce un importe de retiro válido.')
      return
    }

    if (importe > saldoRetirable) {
      setErrorRetiro(`No puedes retirar más de ${formatCurrency(saldoRetirable, monedaRetiro)}.`)
      return
    }

    try {
      const token = localStorage.getItem('token')

      if (tipoRetiro === 'p2p') {
        if (!emailP2P.trim()) {
          setErrorRetiro('Debes escribir el correo electrónico oficial de tu recomendado.')
          return
        }

        const response = await fetch(`${API_URL}/api/retiros/transferir_p2p`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            email_receptor: emailP2P,
            moneda: monedaRetiro,
            importe: Number(importe)
          })
        })
        const result = await response.json()
        if (response.ok) {
          setMontoRetiro('')
          setEmailP2P('')
          setSuccessRetiro('Operación Cautiva Completa. Voucher activado y enviado al 0% de comisión corporativa.')
          // Recargar retiros y operaciones si es necesario para descontar saldo
        } else {
          setErrorRetiro(result.detail || 'Fallo de Transferencia Cautiva.')
        }
        return
      }

      const nombreUsuario = currentUser?.name || currentUser?.nombre || 'Usuario'
      const correoUsuario = currentUser?.email || '—'

      // Guardar retiro en BD
      const response = await fetch(`${API_URL}/api/retiros`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          inversor_id: currentUser?.id,
          nombre: nombreUsuario,
          email: correoUsuario,
          importe: Number(importe),
          moneda: monedaRetiro,
          estado: 'Pendiente de validación',
          detalles: notasRetiro
        })
      })

      if (response.ok) {
        setMontoRetiro('')
        setNotasRetiro('')
        setSuccessRetiro('Tu solicitud de retiro se ha registrado correctamente. El administrador la revisará.')
      } else {
        setErrorRetiro('Error al registrar el retiro')
      }
    } catch (error) {
      console.error('Error:', error)
      setErrorRetiro('Error al registrar el retiro')
    }
  }

  const copiarDatoPago = async (dato) => {
    if (!dato || dato === '—') return
    try {
      await navigator.clipboard.writeText(dato)
      setDatoCopiado('Copiado')
    } catch {
      const campoTemporal = document.createElement('textarea')
      campoTemporal.value = dato
      campoTemporal.style.position = 'fixed'
      campoTemporal.style.opacity = '0'
      document.body.appendChild(campoTemporal)
      campoTemporal.select()
      document.execCommand('copy')
      campoTemporal.remove()
      setDatoCopiado('Copiado')
    }
    setTimeout(() => setDatoCopiado(''), 1800)
  }

  const crearSolicitudInversion = async () => {
    setErrorInversion('')
    setSuccessInversion('')

    const importe = Number(montoInversion)
    if (!montoInversion || Number.isNaN(importe) || importe <= 0) {
      setErrorInversion('Introduce un importe válido.')
      return
    }

    const cuentasAdmin = cuentasPago
    const cuentaConfig = cuentasAdmin.find(c => c.moneda === monedaInversion)
    const minimoMoneda = cuentaConfig?.minimo ? Number(cuentaConfig.minimo) : 100

    if (importe < minimoMoneda) {
      setErrorInversion(`El mínimo para ${monedaInversion} es ${formatCurrency(minimoMoneda, monedaInversion)}`)
      return
    }

    const nombreUsuario = currentUser?.name || currentUser?.nombre || 'Usuario'
    const correoUsuario = currentUser?.email || '—'
    const telefonoUsuario = currentUser?.telefono || '—'
    const paisUsuario = currentUser?.pais || '—'

    try {
      const token = localStorage.getItem('token')

      // 1. Guardar aportación en la BD
      const response = await fetch(`${API_URL}/api/aportaciones`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          inversor_id: currentUser?.id,
          nombre: nombreUsuario,
          email: correoUsuario,
          importe: Number(importe),
          moneda: monedaInversion,
          estado: 'Pendiente de validación'
        })
      })

      if (!response.ok) throw new Error('Error guardando aportación')
      const data = await response.json()

      // Cerrar modal y abrir justificante
      const nuevaSolicitud = {
        id: data.id,
        usuarioId: currentUser?.id || 'anon',
        nombre: nombreUsuario,
        usuarioNombre: nombreUsuario,
        email: correoUsuario,
        telefono: telefonoUsuario,
        pais: paisUsuario,
        importe: Number(importe).toFixed(2),
        moneda: monedaInversion,
        estado: 'Pendiente de validación',
        tipo: 'inversion',
        createdAt: new Date().toISOString(),
        fecha: safeFormatDate(new Date())
      }

      setMontoInversion('')
      setMonedaInversion('USDT BEP-20')
      setShowInversionModal(false)
      setSolicitudSeleccionada(nuevaSolicitud)
      setShowJustificante(true)
      setArchivoJustificante(null)
      setErrorJustificante('')
    } catch (error) {
      console.error('Error:', error)
      setErrorInversion('Error al crear la solicitud')
    }
  }

  const subirJustificante = async () => {
    setErrorJustificante('')

    if (!archivoJustificante) {
      setErrorJustificante('Selecciona un archivo')
      return
    }

    // Guardar metadata del archivo
    const reader = new FileReader()
    reader.onload = async (e) => {
      try {
        const token = localStorage.getItem('token')
        const dataUrl = e.target.result

        // Llamada a la API para subir el justificante
        const response = await fetch(`${API_URL}/api/aportaciones/${solicitudSeleccionada.id}/justificante`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            justificante: dataUrl,
            nombreArchivo: archivoJustificante.name,
            tipoArchivo: archivoJustificante.type
          })
        })

        if (!response.ok) {
          throw new Error('Error al subir el justificante')
        }

        setShowJustificante(false)
        setSolicitudSeleccionada(null)
        setArchivoJustificante(null)
        alert('✅ Justificante subido correctamente. El administrador lo revisará.')

      } catch (error) {
        console.error('Error:', error)
        setErrorJustificante('Ocurrió un error al subir el justificante al servidor.')
      }
    }
    reader.readAsDataURL(archivoJustificante)
  }


  // Funciones de referidos
  const generarCodigoReferido = () => {
    return 'REF' + Math.random().toString(36).substring(2, 11).toUpperCase()
  }

  const correccionReferidoEnviada = React.useRef(false)

  // Crea o corrige (una sola vez) la entrada propia de referidos cuando cargan los datos del perfil.
  // Se hace en un efecto, nunca durante el render, para evitar actualizar estado mientras se pinta la pantalla.
  React.useEffect(() => {
    if (!codigoReferidoPropio || !currentUser?.id || correccionReferidoEnviada.current) return
    const userName = currentUser?.name || currentUser?.nombre || 'Usuario'
    const idPropio = 'inv-referido-' + currentUser.id
    const existente = referidos.find(r => r.id === idPropio) || referidos.find(r => r.codigo === codigoReferidoPropio)
    const desactualizado = !existente ||
      existente.codigo !== codigoReferidoPropio ||
      (referidoPorPropio || null) !== (existente.referidoPor || null)
    if (!desactualizado) return

    correccionReferidoEnviada.current = true
    const nuevoReferido = {
      id: idPropio,
      codigo: codigoReferidoPropio,
      nombreInversor: userName,
      usuarioId: currentUser.id,
      referidoPor: referidoPorPropio || null,
      referidosCount: 0,
      gananciaTotal: 0,
      historial: []
    }
    setReferidos(prev => {
      const existeOtro = prev.some(r => r.id === idPropio || r.codigo === codigoReferidoPropio)
      return existeOtro
        ? prev.map(r => (r.id === idPropio || r.codigo === codigoReferidoPropio) ? nuevoReferido : r)
        : [...prev, nuevoReferido]
    })

    const token = localStorage.getItem('token')
    fetch(`${API_URL}/api/referidos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({
        id: nuevoReferido.id,
        codigo: nuevoReferido.codigo,
        nombreInversor: nuevoReferido.nombreInversor,
        usuarioId: String(nuevoReferido.usuarioId),
        referidoPor: nuevoReferido.referidoPor,
        inversionTotal: 0,
        pagado: false,
        esAdmin: false
      })
    }).catch(console.error)
  }, [codigoReferidoPropio, referidoPorPropio, referidos, currentUser])

  const getCodigoReferidoInversor = () => {
    const userName = currentUser?.name || currentUser?.nombre || 'Usuario'
    const idPropio = 'inv-referido-' + currentUser?.id
    if (codigoReferidoPropio) {
      return referidos.find(r => r.id === idPropio) || referidos.find(r => r.codigo === codigoReferidoPropio) || {
        id: idPropio,
        codigo: codigoReferidoPropio,
        nombreInversor: userName,
        usuarioId: currentUser?.id,
        referidoPor: referidoPorPropio || null,
        referidosCount: 0,
        gananciaTotal: 0,
        historial: []
      }
    }
    return referidos.find(r => r.nombreInversor === userName) || {
      id: idPropio + '-temp',
      codigo: generarCodigoReferido(),
      nombreInversor: userName,
      usuarioId: currentUser?.id,
      referidosCount: 0,
      gananciaTotal: 0,
      historial: []
    }
  }

  const getReferidosDelInversor = () => {
    const codigoRef = getCodigoReferidoInversor().codigo
    return referidos.filter(r => r.referidoPor === codigoRef && r.codigo !== codigoRef)
  }

  // Referidos que cumplen el mínimo de inversión activa (100 $) para contar en el programa
  const getReferidosActivosCount = () => {
    return getReferidosDelInversor().filter(r => Number(r.inversionTotal || 0) >= 100).length
  }

  const NIVELES_CAPITAL = [
    { emoji: '🏆', nombre: 'Founding Partner', min: 10000, beneficio: '250 USDT/mes (x 12 meses)' },
    { emoji: '👑', nombre: 'Strategic Partner', min: 5000, beneficio: '150 USDT/mes (x 6 meses)' },
    { emoji: '💎', nombre: 'VIP Partner', min: 2500, beneficio: '100 USDT/mes (x 4 meses)' },
    { emoji: '🔷', nombre: 'Premium Partner', min: 1000, beneficio: '50 USDT/mes (x 3 meses)' },
    { emoji: '💠', nombre: 'Partner', min: 500, beneficio: '25 USDT/mes (x 2 meses)' },
  ];

  const NIVELES_COMUNIDAD = [
    { emoji: '🏆', nombre: 'Founding Leader', min: 500, bonus: '400 USDT/mes (x 12 meses)' },
    { emoji: '👑', nombre: 'Executive Leader', min: 200, bonus: '250 USDT/mes (x 12 meses)' },
    { emoji: '💎', nombre: 'Elite Leader', min: 100, bonus: '150 USDT/mes (x 6 meses)' },
    { emoji: '🔥', nombre: 'Senior Leader', min: 50, bonus: '100 USDT/mes (x 4 meses)' },
    { emoji: '⭐', nombre: 'Leader', min: 25, bonus: '50 USDT/mes (x 3 meses)' },
    { emoji: '🌱', nombre: 'Community', min: 5, bonus: '25 USDT/mes (x 2 meses)' },
  ];

  // Calcula el rango de Capital (solo inversión)
  const getRangoCapital = () => {
    return NIVELES_CAPITAL.find(r => totalAportado >= r.min) || null
  }

  // Calcula el próximo rango de Capital
  const getProximoRangoCapital = () => {
    return [...NIVELES_CAPITAL].reverse().find(r => totalAportado < r.min) || null
  }

  // Calcula el rango de Comunidad (solo referidos)
  const getRangoComunidad = () => {
    const refs = getReferidosActivosCount()
    return NIVELES_COMUNIDAD.find(r => refs >= r.min) || null
  }

  // Calcula el próximo rango de Comunidad
  const getProximoRangoComunidad = () => {
    const refs = getReferidosActivosCount()
    return [...NIVELES_COMUNIDAD].reverse().find(r => refs < r.min) || null
  }

  // Función para ir al chat de comunidad
  const irAlChat = () => {
    navigate('/comunidad')
  }

  return (
    <div className={`admin-futuristic-layout investor-dashboard${esNavegadorMovil ? ' mobile-browser-shell' : ''}`}>
      {/* Mobile hamburger button */}
      <button className="sidebar-mobile-toggle" onClick={() => setSidebarOpen(!sidebarOpen)}>
        {sidebarOpen ? '✕' : '☰'}
      </button>
      {/* Overlay */}
      <div className={`sidebar-overlay ${sidebarOpen ? 'open' : ''}`} onClick={() => setSidebarOpen(false)} />
      {/* SIDEBAR NAVIGATION */}
      <aside className={`admin-sidebar ${sidebarOpen ? 'open' : ''}`} style={{ borderRight: '1px solid rgba(0, 240, 255, 0.15)' }}>
        <div className="sidebar-brand">
          <div className="brand-icon" style={{ color: '#f6c453', textShadow: '0 0 15px rgba(246,196,83,0.5)' }}>✧</div>
          <div className="brand-text">
            <span className="glow-text" style={{ background: 'linear-gradient(to right, #fff, #f6c453)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', color: 'transparent' }}>Capital Iberia</span>
            <span className="badge-admin" style={{ color: '#00f0ff' }}>INVERSOR</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-group-title">PORTAFOLIO</div>
          <button className={`sidebar-tab ${activeTab === 'resumen' ? 'active' : ''}`} onClick={() => setActiveTab('resumen')}>
            <div className="tab-indicator" /> <span className="tab-label">📊 Mi Cartera</span>
          </button>
          <button className={`sidebar-tab ${activeTab === 'inversiones' ? 'active' : ''}`} onClick={() => setActiveTab('inversiones')}>
            <div className="tab-indicator" /> <span className="tab-label">💼 Mis Inversiones</span>
          </button>
          <button className={`sidebar-tab ${activeTab === 'pagos' ? 'active' : ''}`} onClick={() => setActiveTab('pagos')}>
            <div className="tab-indicator" /> <span className="tab-label">📅 Mis Pagos</span>
          </button>
          <button className={`sidebar-tab ${activeTab === 'ofertas' ? 'active' : ''}`} onClick={() => setActiveTab('ofertas')}>
            <div className="tab-indicator" /> <span className="tab-label">🎁 Mis Ofertas</span>
          </button>
          <button className={`sidebar-tab ${activeTab === 'retirar' ? 'active' : ''}`} onClick={() => setActiveTab('retirar')}>
            <div className="tab-indicator" /> <span className="tab-label">💳 Billetera / Retiros</span>
          </button>

          <div className="nav-divider"></div>
          <div className="nav-group-title">ACTIVIDAD</div>
          <button className={`sidebar-tab ${activeTab === 'operaciones' ? 'active' : ''}`} onClick={() => setActiveTab('operaciones')}>
            <div className="tab-indicator" /> <span className="tab-label">📢 Avisos</span>
          </button>
          <button className={`sidebar-tab ${activeTab === 'referidos' ? 'active' : ''}`} onClick={() => setActiveTab('referidos')}>
            <div className="tab-indicator" /> <span className="tab-label">👥 Mis Referidos</span>
          </button>
          <button className={`sidebar-tab ${activeTab === 'solicitudes' ? 'active' : ''}`} onClick={() => setActiveTab('solicitudes')}>
            <div className="tab-indicator" /> <span className="tab-label">📝 Mis Solicitudes</span>
          </button>
          <button className={`sidebar-tab ${activeTab === 'fondo-solidario' ? 'active' : ''}`} onClick={() => setActiveTab('fondo-solidario')}>
            <div className="tab-indicator" /> <span className="tab-label">🤝 Fondo Solidario</span>
          </button>

          <div className="nav-divider"></div>
          <div className="nav-group-title">EXTRAS</div>

          {esLiderPropio && (
            <button className={`sidebar-tab highlight ${activeTab === 'comunidad-lider' ? 'active' : ''}`} onClick={() => setActiveTab('comunidad-lider')} style={{ fontWeight: 'bold' }}>
              <div className="tab-indicator" /> <span className="tab-label">👑 Mi Comunidad (Red)</span>
            </button>
          )}

          <Link to="/comunidad" className="sidebar-tab highlight" style={{ textDecoration: 'none' }}>
            <div className="tab-indicator" />
            <span className="tab-label">🌐 Chat Global</span>
          </Link>
        </nav>

        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="avatar" style={{ background: 'linear-gradient(135deg, #f6c453, #00f0ff)' }}>{(currentUser?.name || currentUser?.nombre || 'U')[0].toUpperCase()}</div>
            <div className="user-info">
              <span className="user-name">{currentUser?.name || currentUser?.nombre || 'Inversor'}</span>
              <small className="user-role" style={{ color: '#00f0ff' }}>Online</small>
            </div>
          </div>
          {/* Action Buttons specific to investor */}
          <button className="btn-logout-sidebar" style={{ background: 'rgba(16, 185, 129, 0.12)', color: '#10b981', borderColor: 'rgba(16, 185, 129, 0.25)', marginBottom: '8px' }} onClick={() => setActiveTab('ofertas')}>
            🎁 Mis Ofertas
          </button>
          <button className="btn-logout-sidebar" style={{ background: 'rgba(246, 196, 83, 0.1)', color: '#f6c453', borderColor: 'rgba(246, 196, 83, 0.2)', marginBottom: '8px' }} onClick={() => setShowInversionModal(true)}>
            + Nueva Inversión
          </button>
          <button className="btn-logout-sidebar" style={{ background: 'rgba(168, 85, 247, 0.1)', color: '#a855f7', borderColor: 'rgba(168, 85, 247, 0.2)' }} onClick={() => setShowRangosModal(true)}>
            🏆 Mis Rangos
          </button>
        </div>
      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="admin-main-content">
        <header className="topbar investor-topbar">
          <div className="topbar-left">
            <h1>{activeTab === 'resumen' ? 'Mi Cartera' : activeTab === 'operaciones' ? 'Avisos de operaciones' : activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}</h1>
            <p className="subtitle">Gestión de capital y participación operativa</p>
          </div>
          <div className="topbar-actions investor-topbar-actions" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button onClick={() => {
              window.open('https://wa.me/34677412858', '_blank')
            }} className="investor-support-button">
              Soporte WhatsApp
            </button>
            <NotificacionesCampana />
          </div>
        </header>
        <div className="content-scroll">

          {activeTab === 'resumen' && (
            <>
              {/* Tarjeta VIP Negra 3D (Flip) */}
              <div className="vip-card-container" style={{
                perspective: '1000px',
                marginBottom: '2rem',
                display: 'flex',
                justifyContent: 'center',
                cursor: 'pointer'
              }} onClick={() => setIsCardFlipped(!isCardFlipped)}>
                <div className="vip-card-inner" style={{
                  position: 'relative',
                  width: '100%',
                  maxWidth: '450px',
                  height: '210px',
                  transition: 'transform 0.6s',
                  transformStyle: 'preserve-3d',
                  transform: isCardFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)'
                }}>
                  {/* FRENTE */}
                  <div className="vip-card-front" style={{
                    position: 'absolute',
                    width: '100%',
                    height: '100%',
                    backfaceVisibility: 'hidden',
                    background: 'linear-gradient(135deg, #111827 0%, #1f2937 50%, #000000 100%)',
                    borderRadius: '16px',
                    padding: '1.5rem',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    boxShadow: '0 20px 40px rgba(0,0,0,0.4), inset 0 1px 1px rgba(255,255,255,0.1)',
                    border: '1px solid rgba(246, 196, 83, 0.2)',
                    overflow: 'hidden'
                  }}
                    onMouseOver={(e) => { if (!isCardFlipped) e.currentTarget.parentElement.style.transform = 'rotateY(10deg) rotateX(5deg) scale(1.02)' }}
                    onMouseOut={(e) => { if (!isCardFlipped) e.currentTarget.parentElement.style.transform = 'rotateY(0deg) rotateX(0deg) scale(1)' }}
                  >
                    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, background: 'radial-gradient(circle at 80% 20%, rgba(246, 196, 83, 0.15) 0%, transparent 60%)', pointerEvents: 'none' }}></div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', zIndex: 1 }}>
                      <div>
                        <h2 style={{ color: '#f6c453', margin: 0, fontSize: '18px', fontFamily: 'serif', letterSpacing: '2px', textTransform: 'uppercase' }}>CAPITAL IBERIA</h2>
                        <p style={{ color: '#f8fafc', margin: '4px 0 0 0', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '1px', opacity: 0.8 }}>Asset Management</p>
                      </div>
                      <div style={{ background: 'rgba(255,255,255,0.1)', padding: '5px 10px', borderRadius: '4px', border: '1px solid rgba(255,255,255,0.2)' }}>
                        <span style={{ fontSize: '10px', color: '#f6c453', fontWeight: 'bold' }}>TAP TO FLIP ↺</span>
                      </div>
                    </div>

                    <div style={{ zIndex: 1 }}>
                      <p style={{ color: 'rgba(255,255,255,0.5)', margin: '0 0 5px 0', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '1px' }}>Inversor Acreditado</p>
                      <p style={{ color: 'white', margin: 0, fontSize: '20px', letterSpacing: '2px', fontWeight: 'bold', textShadow: '0 2px 4px rgba(0,0,0,0.5)' }}>
                        {currentUser?.name || currentUser?.nombre || 'Inversor VIP'}
                      </p>
                      <p style={{ color: '#f6c453', margin: '8px 0 0 0', fontSize: '13px', fontFamily: 'monospace', letterSpacing: '1px' }}>
                        ID MEMBRESÍA: {getCodigoReferidoInversor()?.codigo || 'N/A'}
                      </p>
                    </div>
                  </div>

                  {/* REVERSO */}
                  <div className="vip-card-back" style={{
                    position: 'absolute',
                    width: '100%',
                    height: '100%',
                    backfaceVisibility: 'hidden',
                    background: 'linear-gradient(135deg, #000000 0%, #111827 100%)',
                    borderRadius: '16px',
                    padding: '1.5rem',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    boxShadow: '0 20px 40px rgba(0,0,0,0.4)',
                    border: '1px solid rgba(246, 196, 83, 0.4)',
                    transform: 'rotateY(180deg)',
                    overflow: 'hidden'
                  }}>
                    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, background: 'repeating-linear-gradient(45deg, rgba(246,196,83,0.03) 0px, rgba(246,196,83,0.03) 2px, transparent 2px, transparent 4px)' }}></div>
                    <p style={{ color: '#f6c453', margin: '0 0 6px 0', fontSize: '9px', fontWeight: 'bold', letterSpacing: '1px' }}>CÓDIGO DE INVITACIÓN</p>
                    <div style={{ background: 'white', padding: '6px', borderRadius: '6px', zIndex: 1 }}>
                      <img src={`https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=${encodeURIComponent(window.location.origin + '?ref=' + (getCodigoReferidoInversor()?.codigo || ''))}`} alt="QR Gigante Referido" style={{ width: '70px', height: '70px', display: 'block' }} />
                    </div>
                  </div>
                </div>
              </div>

              <div className="stats-grid portfolio-summary-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
                {/* Inversión Activa - Gradiente Azul */}
                <div className="portfolio-stat-card portfolio-stat-primary" style={{
                  background: 'linear-gradient(135deg, #0284c7 0%, #0369a1 100%)',
                  borderRadius: '12px',
                  padding: '1.5rem',
                  color: 'white',
                  boxShadow: '0 8px 16px rgba(2, 132, 199, 0.3)',
                  border: '2px solid rgba(255,255,255,0.2)',
                  backdropFilter: 'blur(10px)'
                }}>
                  <p style={{ margin: 0, fontSize: '14px', opacity: 0.9, fontWeight: '600' }}>💰 Inversión Activa</p>
                  <p style={{ margin: '0.75rem 0 0 0', fontSize: '22px', fontWeight: 'bold' }}>
                    {isSystemLoading ? <div className="skeleton-shimmer" style={{ width: '120px' }}></div> : mostrarSaldos('activo')}
                  </p>
                  <p style={{ margin: '0.5rem 0 0 0', fontSize: '12px', opacity: 0.8 }}>Capital liberado por moneda</p>
                </div>

                {/* Ganancias Posibles - Gradiente Verde */}
                <div className="portfolio-stat-card portfolio-stat-positive" style={{
                  background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                  borderRadius: '12px',
                  padding: '1.5rem',
                  color: 'white',
                  boxShadow: '0 8px 16px rgba(16, 185, 129, 0.3)',
                  border: '2px solid rgba(255,255,255,0.2)',
                  backdropFilter: 'blur(10px)'
                }}>
                  <p style={{ margin: 0, fontSize: '14px', opacity: 0.9, fontWeight: '600' }}>📈 Ganancias Posibles</p>
                  <p style={{ margin: '0.75rem 0 0 0', fontSize: '22px', fontWeight: 'bold' }}>
                    {isSystemLoading ? <div className="skeleton-shimmer" style={{ width: '120px' }}></div> : mostrarSaldos('gananciasPosibles')}
                  </p>
                  <p style={{ margin: '0.5rem 0 0 0', fontSize: '12px', opacity: 0.8 }}>Pool por moneda</p>
                </div>

                {/* Saldo Disponible - Gradiente Púrpura */}
                <div className="portfolio-stat-card portfolio-stat-available" style={{
                  background: 'linear-gradient(135deg, #a855f7 0%, #9333ea 100%)',
                  borderRadius: '12px',
                  padding: '1.5rem',
                  color: 'white',
                  boxShadow: '0 8px 16px rgba(168, 85, 247, 0.3)',
                  border: '2px solid rgba(255,255,255,0.2)',
                  backdropFilter: 'blur(10px)'
                }}>
                  <p style={{ margin: 0, fontSize: '14px', opacity: 0.9, fontWeight: '600' }}>💵 Saldo Disponible</p>
                  <p style={{ margin: '0.75rem 0 0 0', fontSize: '22px', fontWeight: 'bold' }}>
                    {isSystemLoading ? <div className="skeleton-shimmer" style={{ width: '120px' }}></div> : mostrarSaldos('retirable')}
                  </p>
                  <p style={{ margin: '0.5rem 0 0 0', fontSize: '12px', opacity: 0.8 }}>Disponible para retirar</p>
                </div>

                {/* Total Retirado - Gradiente Naranja */}
                <div className="portfolio-stat-card portfolio-stat-withdrawn" style={{
                  background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                  borderRadius: '12px',
                  padding: '1.5rem',
                  color: 'white',
                  boxShadow: '0 8px 16px rgba(245, 158, 11, 0.3)',
                  border: '2px solid rgba(255,255,255,0.2)',
                  backdropFilter: 'blur(10px)'
                }}>
                  <p style={{ margin: 0, fontSize: '14px', opacity: 0.9, fontWeight: '600' }}>✅ Total Retirado</p>
                  <p style={{ margin: '0.75rem 0 0 0', fontSize: '22px', fontWeight: 'bold' }}>
                    {isSystemLoading ? <div className="skeleton-shimmer" style={{ width: '120px' }}></div> : mostrarSaldos('retirado')}
                  </p>
                  <p style={{ margin: '0.5rem 0 0 0', fontSize: '12px', opacity: 0.8 }}>Dinero recibido por moneda</p>
                </div>

                {/* Inversión Retenida - cuenta regresiva de bloqueo 72h */}
                {capitalRetenido > 0 && (
                  <div className="portfolio-stat-card portfolio-stat-locked" style={{
                    background: 'linear-gradient(135deg, #64748b 0%, #334155 100%)',
                    borderRadius: '12px',
                    padding: '1.5rem',
                    color: 'white',
                    boxShadow: '0 8px 16px rgba(51, 65, 85, 0.3)',
                    border: '2px solid rgba(255,255,255,0.2)',
                    backdropFilter: 'blur(10px)'
                  }}>
                    <p style={{ margin: 0, fontSize: '14px', opacity: 0.9, fontWeight: '600' }}>🔒 Inversión Retenida</p>
                    <p className="retained-investments-count" style={{ margin: '0.75rem 0 0 0', fontSize: '13px', fontWeight: '700' }}>
                      {aportacionesRetenidas.length} {aportacionesRetenidas.length === 1 ? 'inversión con bloqueo propio' : 'inversiones con bloqueos propios'}
                    </p>
                    <p style={{ margin: '0.25rem 0 0', fontSize: '10px', opacity: 0.8 }}>Cada inversión conserva su propia fecha de activación.</p>
                    <div style={{ display: 'grid', gap: '0.4rem', marginTop: '0.65rem' }}>
                      {(mostrarTodasRetenidas ? aportacionesRetenidas : aportacionesRetenidas.slice(0, 2)).map((item) => {
                        const tiempo = obtenerTiempoRetenido(item)
                        return (
                          <div key={item.id} style={{ fontSize: '11px', lineHeight: 1.35, opacity: 0.95 }}>
                            <strong>Inversión #{item.id}: {formatCurrency(Number(item.importe || 0), item.moneda || 'EUR')}</strong>
                            <span style={{ display: 'block', fontFamily: 'monospace', fontWeight: '700' }}>
                              ⏱️ {String(tiempo.horas).padStart(2, '0')}h {String(tiempo.minutos).padStart(2, '0')}m {String(tiempo.segundos).padStart(2, '0')}s para activarse
                            </span>
                          </div>
                        )
                      })}
                      {aportacionesRetenidas.length > 2 && (
                        <button
                          type="button"
                          className="retained-investments-toggle"
                          onClick={() => setMostrarTodasRetenidas((mostrar) => !mostrar)}
                        >
                          {mostrarTodasRetenidas ? 'Ver menos' : `Ver ${aportacionesRetenidas.length - 2} más`}
                        </button>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </>
          )}

          {activeTab === 'fondo-solidario' && (
            <FondoSolidarioPanel />
          )}

          {activeTab === 'inversiones' && (
            <div className="content-grid" style={{ display: 'grid', gap: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
                <h2 style={{ margin: 0, color: '#f8fafc', fontSize: '1.3rem', fontWeight: '700' }}>💼 Mis Inversiones</h2>
                <div style={{
                  background: 'rgba(239, 68, 68, 0.1)',
                  border: '1px solid rgba(239, 68, 68, 0.3)',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  maxWidth: '400px'
                }}>
                  <p style={{ margin: 0, fontSize: '12px', color: '#fca5a5', fontWeight: '600', lineHeight: '1.4' }}>
                    ⚠️ NORMATIVA: Todo saldo disponible en su billetera debe ser retirado obligatoriamente hacia sus métodos de pago externos. No se permite la reinversión directa desde su saldo interno.
                  </p>
                </div>
              </div>

              {/* El enlace de referido ha sido movido íntegramente a la pestaña 'referidos' */}

              {userAportaciones.length > 0 ? (
                userAportaciones.map((item, idx) => {
                  const capitalInvertido = Number(item.importe || 0)
                  const poolTotal = Number(item.meta_ganancia || (capitalInvertido * 3))
                  const ganado = Number(item.ganancia_total || 0)
                  const porcentaje = poolTotal > 0 ? Math.min((ganado / poolTotal) * 100, 100) : 0
                  const completado = porcentaje >= 100
                  const gananciasDis = poolTotal - ganado
                  const retenida = aportacionesRetenidas.some((aportacion) => aportacion.id === item.id)
                  const tiempoRetencion = retenida ? obtenerTiempoRetenido(item) : null

                  return (
                    <div key={item.id || idx} style={{
                      background: 'rgba(10, 17, 30, 0.7)',
                      backdropFilter: 'blur(16px)',
                      border: '1px solid rgba(148, 163, 184, 0.12)',
                      borderRadius: '20px',
                      padding: '1.5rem',
                      transition: 'all 0.3s ease',
                      boxShadow: '0 8px 24px rgba(0, 0, 0, 0.2)'
                    }}>
                      {/* Header de la inversión */}
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.2rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                        <div>
                          <p style={{ margin: 0, fontSize: '0.75rem', color: '#94a3b8', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                            Inversión #{idx + 1}
                          </p>
                          <p style={{ margin: '0.3rem 0 0', fontSize: '1.5rem', fontWeight: '800', color: '#f8fafc' }}>
                            {formatCurrency(capitalInvertido, item.moneda || 'EUR')}
                          </p>
                        </div>
                        <span style={{
                          padding: '0.35rem 0.9rem',
                          borderRadius: '999px',
                          fontSize: '0.72rem',
                          fontWeight: '700',
                          letterSpacing: '0.04em',
                          textTransform: 'uppercase',
                          background: completado
                            ? 'rgba(16, 185, 129, 0.15)'
                            : retenida
                              ? 'rgba(59, 130, 246, 0.15)'
                              : item.estado === 'Activa' || item.estado === 'Validada'
                                ? 'rgba(246, 196, 83, 0.12)'
                                : 'rgba(239, 68, 68, 0.12)',
                          color: completado
                            ? '#86efac'
                            : retenida
                              ? '#93c5fd'
                              : item.estado === 'Activa' || item.estado === 'Validada'
                                ? '#f6c453'
                                : '#fca5a5',
                          border: `1px solid ${completado ? 'rgba(16, 185, 129, 0.25)' : retenida ? 'rgba(59, 130, 246, 0.3)' : item.estado === 'Activa' || item.estado === 'Validada' ? 'rgba(246, 196, 83, 0.2)' : 'rgba(239, 68, 68, 0.2)'}`
                        }}>
                          {completado ? '✓ Completada' : retenida ? '🔒 Bloqueada' : item.estado}
                        </span>
                      </div>

                      {retenida && (
                        <p style={{ margin: '0 0 1rem', color: '#bfdbfe', fontSize: '0.75rem', fontFamily: 'monospace', fontWeight: '700' }}>
                          ⏱️ Bloqueo propio: {String(tiempoRetencion.horas).padStart(2, '0')}h {String(tiempoRetencion.minutos).padStart(2, '0')}m {String(tiempoRetencion.segundos).padStart(2, '0')}s
                        </p>
                      )}

                      {/* Barra de progreso */}
                      <div style={{ marginBottom: '1rem' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                          <span style={{ fontSize: '0.78rem', color: '#94a3b8', fontWeight: '600' }}>Progreso de ganancias</span>
                          <span style={{ fontSize: '0.85rem', color: completado ? '#86efac' : '#f6c453', fontWeight: '800' }}>{porcentaje.toFixed(1)}%</span>
                        </div>
                        <div style={{
                          width: '100%',
                          height: '12px',
                          backgroundColor: 'rgba(148, 163, 184, 0.08)',
                          borderRadius: '999px',
                          overflow: 'hidden',
                          border: '1px solid rgba(148, 163, 184, 0.08)'
                        }}>
                          <div style={{
                            width: `${porcentaje}%`,
                            height: '100%',
                            borderRadius: '999px',
                            background: completado
                              ? 'linear-gradient(90deg, #10b981, #34d399)'
                              : porcentaje > 50
                                ? 'linear-gradient(90deg, #f6c453, #dba93a, #10b981)'
                                : 'linear-gradient(90deg, #f6c453, #dba93a)',
                            transition: 'width 1.2s cubic-bezier(0.4, 0, 0.2, 1)',
                            boxShadow: completado
                              ? '0 0 12px rgba(16, 185, 129, 0.4)'
                              : '0 0 12px rgba(246, 196, 83, 0.3)'
                          }} />
                        </div>
                      </div>

                      {/* Detalles numéricos */}
                      <div className="investment-details-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: '1rem' }}>
                        <div style={{
                          background: 'rgba(246, 196, 83, 0.06)',
                          border: '1px solid rgba(246, 196, 83, 0.1)',
                          borderRadius: '12px',
                          padding: '0.8rem',
                          textAlign: 'center'
                        }}>
                          <p style={{ margin: 0, fontSize: '0.68rem', color: '#94a3b8', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Pool total</p>
                          <p style={{ margin: '0.3rem 0 0', fontSize: '1rem', fontWeight: '800', color: '#f6c453' }}>{formatCurrency(poolTotal, item.moneda || 'EUR')}</p>
                        </div>
                        <div style={{
                          background: 'rgba(16, 185, 129, 0.06)',
                          border: '1px solid rgba(16, 185, 129, 0.1)',
                          borderRadius: '12px',
                          padding: '0.8rem',
                          textAlign: 'center'
                        }}>
                          <p style={{ margin: 0, fontSize: '0.68rem', color: '#94a3b8', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Ganado</p>
                          <p style={{ margin: '0.3rem 0 0', fontSize: '1rem', fontWeight: '800', color: '#86efac' }}>{formatCurrency(ganado, item.moneda || 'EUR')}</p>
                        </div>
                        <div style={{
                          background: 'rgba(148, 163, 184, 0.04)',
                          border: '1px solid rgba(148, 163, 184, 0.08)',
                          borderRadius: '12px',
                          padding: '0.8rem',
                          textAlign: 'center'
                        }}>
                          <p style={{ margin: 0, fontSize: '0.68rem', color: '#94a3b8', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Por Completar</p>
                          <p style={{ margin: '0.3rem 0 0', fontSize: '1rem', fontWeight: '800', color: '#e2e8f0' }}>{formatCurrency(gananciasDis, item.moneda || 'EUR')}</p>
                        </div>
                      </div>

                      {/* Fecha */}
                      <p style={{ margin: '0.8rem 0 0', fontSize: '0.72rem', color: '#64748b', textAlign: 'right' }}>
                        📅 {item.fechaUltimoPago ? `Último pago: ${new Date(item.fechaUltimoPago).toLocaleDateString('es-ES')}` : `Registrada: ${new Date(item.createdAt || Date.now()).toLocaleDateString('es-ES')}`}
                      </p>
                    </div>
                  )
                })
              ) : (
                <div style={{
                  padding: '3rem 2rem',
                  background: 'rgba(10, 17, 30, 0.5)',
                  borderRadius: '20px',
                  textAlign: 'center',
                  border: '1px solid rgba(148, 163, 184, 0.08)'
                }}>
                  <p style={{ fontSize: '2.5rem', margin: '0 0 0.8rem' }}>💰</p>
                  <p style={{ color: '#94a3b8', fontSize: '0.95rem', margin: 0 }}>Aún no tienes inversiones registradas. ¡Comienza a invertir!</p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'resumen' && (
            <div className="content-grid" style={{ display: 'grid', gap: '1.5rem' }}>
              <div className="portfolio-overview">
                <div>
                  <p className="portfolio-eyebrow">CENTRO DE CONTROL</p>
                  <h2>Resumen de cartera</h2>
                  <p>Consulta cada posición en <strong>Mis Inversiones</strong>. El capital retenido se libera automáticamente al finalizar la cuenta atrás de 72 horas.</p>
                </div>
                <div className="portfolio-quick-actions">
                  <button className="portfolio-action action-invest" onClick={() => setShowInversionModal(true)}>
                    <span>+</span>Nueva inversión
                  </button>
                  <button className="portfolio-action action-withdraw" onClick={() => setActiveTab('retirar')}>
                    <span>€</span>Solicitar retiro
                  </button>
                  <button className="portfolio-action action-view" onClick={() => setActiveTab('inversiones')}>
                    <span>↗</span>Ver inversiones
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'pagos' && (
            <div className="content-grid" style={{ display: 'grid', gap: '1.5rem' }}>
              <section className="card" style={{ margin: 0 }}>
                <div className="section-header"><h2>Calendario semanal de pagos</h2></div>
                {(() => {
                  const inicioSemana = new Date()
                  inicioSemana.setHours(0, 0, 0, 0)
                  inicioSemana.setDate(inicioSemana.getDate() - ((inicioSemana.getDay() + 6) % 7))
                  const dias = Array.from({ length: 7 }, (_, index) => {
                    const fecha = new Date(inicioSemana)
                    fecha.setDate(inicioSemana.getDate() + index)
                    const pagos = pagosRentabilidad.filter(pago => pago.fecha?.slice(0, 10) === fecha.toISOString().slice(0, 10))
                    return { fecha, pagos }
                  })
                  return <>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(125px, 1fr))', gap: '0.75rem', margin: '1rem 0 1.5rem' }}>
                      {dias.map(({ fecha, pagos }) => {
                        const totales = pagos.reduce((result, pago) => ({ ...result, [pago.moneda]: (result[pago.moneda] || 0) + Number(pago.importe || 0) }), {})
                        return <div key={fecha.toISOString()} style={{ padding: '0.85rem', borderRadius: 8, border: '1px solid rgba(16,185,129,0.35)', background: pagos.length ? 'rgba(16,185,129,0.12)' : 'rgba(15,23,42,0.45)' }}>
                          <strong style={{ display: 'block', color: '#f8fafc', textTransform: 'capitalize' }}>{fecha.toLocaleDateString('es-ES', { weekday: 'short', day: '2-digit', month: '2-digit' })}</strong>
                          <span style={{ color: '#94a3b8', fontSize: 12 }}>{pagos.length} pago{pagos.length === 1 ? '' : 's'}</span>
                          <strong style={{ display: 'block', marginTop: 5, color: '#6ee7b7', fontSize: 13 }}>{Object.entries(totales).map(([moneda, importe]) => formatCurrency(importe, moneda)).join(' · ') || '—'}</strong>
                        </div>
                      })}
                    </div>
                    <div style={{ display: 'grid', gap: '0.6rem' }}>
                      {pagosRentabilidad.length ? pagosRentabilidad.map(pago => <div key={pago.id} style={{ display: 'flex', justifyContent: 'space-between', gap: '1rem', padding: '0.85rem', background: 'rgba(15,23,42,0.6)', borderRadius: 8, border: '1px solid rgba(148,163,184,0.14)' }}>
                        <span><strong>{safeFormatDate(pago.fecha)}</strong> · Contrato #{pago.aportacion_id} · {Number(pago.porcentaje).toLocaleString('es-ES')}%</span>
                        <strong style={{ color: '#6ee7b7', whiteSpace: 'nowrap' }}>+{formatCurrency(Number(pago.importe), pago.moneda)}</strong>
                      </div>) : <p style={{ color: '#94a3b8' }}>Todavía no hay pagos registrados.</p>}
                    </div>
                  </>
                })()}
              </section>
            </div>
          )}

          {activeTab === 'operaciones' && (
            <div className="content-grid" style={{ display: 'grid', gap: '1.5rem' }}>
              <section className="operaciones-journal-heading">
                <p>ACTUALIZACIÓN OPERATIVA</p>
                <h2>El diario de Capital Iberia</h2>
                <span>Información publicada por la administración sobre las operaciones en curso.</span>
              </section>
              {avisosOperaciones.length ? avisosOperaciones.map(aviso => (
                <article key={aviso.id} className="operacion-aviso-card">
                  <div className="operacion-aviso-meta">
                    <span>{aviso.operacionIcono} {aviso.operacionNombre}</span>
                    <time>{safeFormatDate(aviso.createdAt)}</time>
                  </div>
                  <h3>{aviso.titulo}</h3>
                  <p>{aviso.contenido}</p>
                  {aviso.imagenes?.length > 0 && (
                    <div className={`operacion-aviso-images images-${Math.min(aviso.imagenes.length, 3)}`}>
                      {aviso.imagenes.map((imagen, index) => <img key={`${aviso.id}-${index}`} src={imagen} alt={`Imagen de ${aviso.operacionNombre}: ${index + 1}`} />)}
                    </div>
                  )}
                  <footer>Publicado por administración</footer>
                </article>
              )) : (
                <div className="operacion-aviso-empty">
                  <strong>Aún no hay avisos publicados.</strong>
                  <span>Cuando la administración comunique una operación realizada, aparecerá aquí con sus detalles y fotografías.</span>
                </div>
              )}
            </div>
          )}

          {activeTab === 'retirar' && (
            <div className="content-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
              {/* Panel de Solicitud de Retiro */}
              <div style={{
                background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                borderRadius: '12px',
                padding: '2rem',
                color: 'white',
                boxShadow: '0 8px 16px rgba(245, 158, 11, 0.3)',
                border: '2px solid rgba(255,255,255,0.2)'
              }}>
                <h2 style={{ marginTop: 0 }}>🏦 Centro de Liquidez</h2>
                <p style={{ opacity: 0.9, margin: '0 0 0.5rem 0' }}>Saldo disponible en {monedaRetiro}: <strong style={{ fontSize: '20px' }}>{formatCurrency(saldoRetirable, monedaRetiro)}</strong></p>
                {tipoRetiro !== 'p2p' && saldoRetirable > 0 && (
                  <p style={{ margin: '0 0 1.5rem 0', fontSize: '13px', color: '#6ee7b7', fontWeight: '600' }}>
                    Monto máximo a recibir en banco tras descontar 5% de fee: {formatCurrency(saldoRetirable * 0.95, monedaRetiro)}
                  </p>
                )}
                {tipoRetiro === 'p2p' && saldoRetirable > 0 && (
                  <p style={{ margin: '0 0 1.5rem 0', fontSize: '13px', color: '#60a5fa', fontWeight: '600' }}>
                    Liquidez máxima a transferir (0% Fee): {formatCurrency(saldoRetirable, monedaRetiro)}
                  </p>
                )}
                {saldoRetirable <= 0 && <div style={{ marginBottom: '1.5rem' }}></div>}
                <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', width: '100%' }}>
                  <button type="button" onClick={() => { setTipoRetiro('banco'); setErrorRetiro('') }} style={{ flex: 1, padding: '1rem 0.5rem', background: tipoRetiro === 'banco' ? 'rgba(0,0,0,0.3)' : 'transparent', border: tipoRetiro === 'banco' ? '2px solid white' : '1px solid rgba(255,255,255,0.2)', color: 'white', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold', fontSize: '13px' }}>
                    🏦 Retiro a Banco (5% Fee)
                  </button>
                  <button type="button" onClick={() => { setTipoRetiro('p2p'); setErrorRetiro('') }} style={{ flex: 1, padding: '1rem 0.5rem', background: tipoRetiro === 'p2p' ? 'rgba(0,0,0,0.3)' : 'transparent', border: tipoRetiro === 'p2p' ? '2px solid #60a5fa' : '1px solid rgba(255,255,255,0.2)', color: 'white', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold', fontSize: '13px' }}>
                    🎫 Transferir a Nuevo Referido
                  </button>
                </div>

                <form onSubmit={handleRetiroSubmit} style={{ display: 'grid', gap: '1rem' }}>
                  <div>
                    <label htmlFor="moneda-retiro" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600', fontSize: '14px' }}>Moneda del retiro</label>
                    <select id="moneda-retiro" value={monedaRetiro} onChange={(e) => { setMonedaRetiro(e.target.value); setMontoRetiro('') }} style={{ width: '100%', padding: '0.75rem', border: '2px solid rgba(255,255,255,0.3)', borderRadius: '8px', backgroundColor: 'rgba(0,0,0,0.16)', color: 'white', fontSize: '14px' }}>
                      {(monedasConSaldo.length ? monedasConSaldo : Object.keys(saldosPorMoneda)).map((moneda) => <option key={moneda} value={moneda}>{moneda} - disponible: {formatCurrency(Math.max(0, saldosPorMoneda[moneda].disponible - saldosPorMoneda[moneda].retirado), moneda)}</option>)}
                    </select>
                    {!monedasConSaldo.length && <p style={{ margin: '0.5rem 0 0', fontSize: '12px', color: '#fef3c7' }}>No hay saldo de ganancias disponible para retirar todavía.</p>}
                  </div>
                  <div>
                    <label htmlFor="monto-retiro" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600', fontSize: '14px' }}>Importe a retirar</label>
                    <input
                      id="monto-retiro"
                      type="number"
                      min="0.01"
                      step="0.01"
                      value={montoRetiro}
                      onChange={(e) => setMontoRetiro(e.target.value)}
                      placeholder="Ej. 2500"
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: '2px solid rgba(255,255,255,0.3)',
                        borderRadius: '8px',
                        fontSize: '14px',
                        backgroundColor: 'transparent',
                        color: 'white',
                        outline: 'none',
                        boxSizing: 'border-box'
                      }}
                      required
                    />
                    {tipoRetiro === 'p2p' ? (
                      <div style={{ margin: '15px 0 0 0', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <label style={{ fontWeight: '600', fontSize: '14px' }}>Correo Electrónico (Receptor)</label>
                        <input
                          type="email"
                          placeholder="ejemplo@correo.com"
                          value={emailP2P}
                          onChange={(e) => setEmailP2P(e.target.value)}
                          style={{ width: '100%', padding: '0.75rem', border: '2px solid rgba(255,255,255,0.3)', borderRadius: '8px', fontSize: '14px', backgroundColor: 'transparent', color: 'white', outline: 'none' }}
                          required={tipoRetiro === 'p2p'}
                        />
                        <div style={{ marginTop: '10px', padding: '12px', backgroundColor: 'rgba(0, 0, 0, 0.25)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.2)' }}>
                          <p style={{ margin: 0, fontSize: '13px', color: '#10b981', fontWeight: 'bold' }}>
                            <span style={{ fontSize: '16px' }}>✔️</span> TRANSFERENCIA LIBRE DE FEES (0%)
                          </p>
                          <p style={{ margin: '8px 0 0 0', fontSize: '12px', color: '#fef3c7' }}>
                            Permitido estrictamente para pagar el abono inicial de prospectos <strong>registrados con tu código y sin historial de inversión</strong>.
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div style={{ margin: '15px 0 0 0', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                        {montoRetiro && Number(montoRetiro) > 0 && Number(montoRetiro) <= saldoRetirable && (
                          <div style={{ padding: '12px', backgroundColor: 'rgba(16, 185, 129, 0.15)', borderRadius: '8px', border: '1px solid rgba(16, 185, 129, 0.4)' }}>
                            <p style={{ margin: 0, fontSize: '14px', color: '#6ee7b7', fontWeight: 'bold' }}>
                              ✅ Recibirás en tu Banco: {formatCurrency(Number(montoRetiro) * 0.95, monedaRetiro)}
                            </p>
                          </div>
                        )}
                        <div style={{ padding: '12px', backgroundColor: 'rgba(0, 0, 0, 0.25)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.2)' }}>
                          <p style={{ margin: 0, fontSize: '13px', color: '#ffffff', fontWeight: 'bold', lineHeight: '1.4' }}>
                            ⚠️ ATENCIÓN: Todo saldo disponible debe ser retirado a su cuenta externa personal. No está permitida la reinversión de capital interno directo.
                          </p>
                          <p style={{ margin: '8px 0 0 0', fontSize: '12px', color: '#fef3c7' }}>
                            * Nota: Se aplicará una deducción del 5% del importe retirado destinado al corporativo y al Fondo Solidario.
                          </p>
                        </div>
                      </div>
                    )}
                  </div>

                  {tipoRetiro === 'banco' && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '10px' }}>
                      {monedaRetiro === 'USDT BEP-20' ? (
                        <div>
                          <label htmlFor="wallet-retiro" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600', fontSize: '14px' }}>Dirección de Billetera (Network: BEP-20)</label>
                          <input
                            id="wallet-retiro"
                            type="text"
                            value={notasRetiro}
                            onChange={(e) => setNotasRetiro(e.target.value)}
                            placeholder="0x..."
                            style={{ width: '100%', padding: '0.75rem', border: '2px solid rgba(255,255,255,0.3)', borderRadius: '8px', fontSize: '14px', backgroundColor: 'rgba(255,255,255,0.1)', color: 'white', boxSizing: 'border-box' }}
                            required
                          />
                        </div>
                      ) : (
                        <>
                          <div>
                            <label htmlFor="iban-retiro" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600', fontSize: '14px' }}>IBAN (Cuenta Bancaria)</label>
                            <input
                              id="iban-retiro"
                              type="text"
                              placeholder="ESXX XXXX XXXX XXXX"
                              onChange={(e) => setNotasRetiro(`IBAN: ${e.target.value} | Titular: ${document.getElementById('titular-retiro')?.value || ''}`)}
                              style={{ width: '100%', padding: '0.75rem', border: '2px solid rgba(255,255,255,0.3)', borderRadius: '8px', fontSize: '14px', backgroundColor: 'rgba(255,255,255,0.1)', color: 'white', boxSizing: 'border-box' }}
                              required
                            />
                          </div>
                          <div>
                            <label htmlFor="titular-retiro" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600', fontSize: '14px' }}>Nombre del Titular</label>
                            <input
                              id="titular-retiro"
                              type="text"
                              placeholder="Juan Pérez"
                              onChange={(e) => setNotasRetiro(`IBAN: ${document.getElementById('iban-retiro')?.value || ''} | Titular: ${e.target.value}`)}
                              style={{ width: '100%', padding: '0.75rem', border: '2px solid rgba(255,255,255,0.3)', borderRadius: '8px', fontSize: '14px', backgroundColor: 'rgba(255,255,255,0.1)', color: 'white', boxSizing: 'border-box' }}
                              required
                            />
                          </div>
                        </>
                      )}
                    </div>
                  )}

                  {errorRetiro && <div style={{ backgroundColor: 'rgba(0,0,0,0.2)', color: '#fef3c7', padding: '0.75rem', borderRadius: '6px', fontSize: '14px', fontWeight: '600' }}>⚠️ {errorRetiro}</div>}
                  {successRetiro && <div style={{ backgroundColor: 'rgba(34, 197, 94, 0.2)', color: '#dcfce7', padding: '0.75rem', borderRadius: '6px', fontSize: '14px', fontWeight: '600' }}>✅ {successRetiro}</div>}

                  <button type="submit" style={{
                    marginTop: '0.5rem', padding: '1rem',
                    backgroundColor: tipoRetiro === 'p2p' ? '#3b82f6' : 'rgba(255,255,255,0.2)',
                    color: 'white', border: tipoRetiro === 'p2p' ? 'none' : '2px solid rgba(255,255,255,0.4)',
                    borderRadius: '8px', cursor: 'pointer', fontWeight: '600', fontSize: '15px', transition: 'all 0.3s'
                  }}>
                    {tipoRetiro === 'p2p' ? '➡️ Ejecutar Transferencia' : '💰 Solicitar Retiro Externo'}
                  </button>
                </form>
              </div>

              {/* Panel de Historial de Retiros */}
              <div style={{
                backgroundColor: 'rgba(15, 23, 42, 0.8)',
                borderRadius: '12px',
                padding: '1.5rem',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
                border: '1px solid rgba(148, 163, 184, 0.12)'
              }}>
                <h2 style={{ marginTop: 0, color: '#f8fafc' }}>📋 Historial de Retiros</h2>
                {userRetiros.length ? (
                  <div style={{ display: 'grid', gap: '1rem' }}>
                    {userRetiros.map((item) => (
                      <div key={item.id} style={{
                        padding: '1rem',
                        backgroundColor: item.estado === 'Procesado' ? 'rgba(16, 185, 129, 0.1)' : item.estado === 'Pendiente' ? 'rgba(245, 158, 11, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                        borderRadius: '8px',
                        borderLeft: `4px solid ${item.estado === 'Procesado' ? '#10b981' : item.estado === 'Pendiente' ? '#f59e0b' : '#ef4444'}`,
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                      }}>
                        <div>
                          <p style={{ margin: 0, fontWeight: '600', color: '#e2e8f0' }}>Retiro #{String(item.id).substring(0, 8)}</p>
                          <p style={{ margin: '0.25rem 0 0 0', fontSize: '12px', color: '#94a3b8' }}>{item.fecha || 'Sin fecha'}</p>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                          <p style={{ margin: 0, fontWeight: '600', color: '#e2e8f0', fontSize: '16px' }}>
                            {formatCurrency(Number(item.importe || 0), item.moneda || 'EUR')}
                          </p>
                          <span style={{
                            display: 'inline-block',
                            marginTop: '0.25rem',
                            padding: '2px 8px',
                            borderRadius: '4px',
                            fontSize: '11px',
                            fontWeight: '600',
                            backgroundColor: item.estado === 'Procesado' ? '#10b981' : item.estado === 'Pendiente' ? '#f59e0b' : '#ef4444',
                            color: 'white'
                          }}>
                            {item.estado}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div style={{ padding: '2rem', backgroundColor: 'rgba(15, 23, 42, 0.5)', borderRadius: '8px', textAlign: 'center', color: '#94a3b8' }}>
                    <p>No tienes solicitudes de retiro aún.</p>
                  </div>
                )}
              </div>
            </div>
          )
          }

          {
            activeTab === 'solicitudes' && (
              <div className="content-grid" style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '2rem' }}>
                <div>
                  <h2 style={{ color: '#f8fafc', marginBottom: '1.5rem' }}>📋 Mis Solicitudes de Inversión</h2>
                  {(() => {
                    const AHORA = Date.now()
                    const HORAS_BLOQUEO = 72
                    const userSolicitudes = userAportaciones

                    const infoEstado = (item) => {
                      if (item.estado === 'Rechazada') {
                        return { label: '❌ Rechazada', color: '#fca5a5', bg: 'rgba(239, 68, 68, 0.15)', borderColor: 'rgba(239, 68, 68, 0.3)' }
                      }
                      if (item.estado === 'Activa' || item.estado === 'Validada') {
                        const aprobadaEn = item.fecha_aprobacion ? new Date(item.fecha_aprobacion + (item.fecha_aprobacion.includes('Z') ? '' : 'Z')).getTime() : null
                        const desbloqueaEn = aprobadaEn ? aprobadaEn + HORAS_BLOQUEO * 3600 * 1000 : null
                        if (desbloqueaEn && desbloqueaEn > AHORA) {
                          const restanteMs = desbloqueaEn - AHORA
                          const horas = Math.floor(restanteMs / 3600000)
                          const minutos = Math.floor((restanteMs % 3600000) / 60000)
                          return {
                            label: `🔒 Bloqueada ${horas}h ${minutos}m`,
                            color: '#93c5fd', bg: 'rgba(59, 130, 246, 0.15)', borderColor: 'rgba(59, 130, 246, 0.3)',
                            bloqueada: true, horas, minutos
                          }
                        }
                        return { label: '✅ Activa', color: '#86efac', bg: 'rgba(16, 185, 129, 0.15)', borderColor: 'rgba(16, 185, 129, 0.3)' }
                      }
                      return { label: `⏳ ${item.estado || 'Pendiente'}`, color: '#fcd34d', bg: 'rgba(245, 158, 11, 0.15)', borderColor: 'rgba(251, 191, 36, 0.3)' }
                    }

                    return userSolicitudes.length > 0 ? (
                      <div style={{ display: 'grid', gap: '1rem' }}>
                        {userSolicitudes.map((sol) => {
                          const info = infoEstado(sol)
                          return (
                            <div key={sol.id} style={{
                              backgroundColor: 'rgba(15, 23, 42, 0.8)',
                              borderRadius: '12px',
                              padding: '1.5rem',
                              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
                              border: `2px solid ${info.borderColor}`,
                              transition: 'all 0.3s'
                            }}>
                              <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: '1rem', marginBottom: '1rem' }}>
                                <div>
                                  <p style={{ margin: 0, fontSize: '12px', color: '#94a3b8', fontWeight: '600' }}>Solicitud #{sol.id}</p>
                                  <p style={{ margin: '0.5rem 0 0 0', fontSize: '20px', fontWeight: 'bold', color: '#f6c453' }}>
                                    {formatCurrency(Number(sol.importe), sol.moneda)}
                                  </p>
                                  <p style={{ margin: '0.25rem 0 0 0', fontSize: '12px', color: '#94a3b8' }}>
                                    📅 {safeFormatDate(sol.fecha)}
                                  </p>
                                </div>
                                <div style={{ textAlign: 'right', display: 'flex', flexDirection: 'column', alignItems: 'flex-end', justifyContent: 'center' }}>
                                  <span style={{
                                    display: 'inline-block',
                                    padding: '0.5rem 1rem',
                                    borderRadius: '20px',
                                    fontSize: '12px',
                                    fontWeight: '600',
                                    backgroundColor: info.bg,
                                    color: info.color
                                  }}>
                                    {info.label}
                                  </span>
                                </div>
                              </div>

                              {info.bloqueada && (
                                <div style={{
                                  backgroundColor: 'rgba(59, 130, 246, 0.08)',
                                  padding: '1rem',
                                  borderRadius: '8px',
                                  fontSize: '13px',
                                  borderLeft: '4px solid #3b82f6',
                                  marginBottom: '0.75rem'
                                }}>
                                  <p style={{ margin: 0, color: '#93c5fd', fontWeight: '600' }}>
                                    ⏱️ Tu inversión está validada. Las ganancias comienzan a generarse tras 72 horas de bloqueo de seguridad.
                                  </p>
                                  <p style={{ margin: '0.5rem 0 0 0', color: '#dbeafe', fontSize: '12px' }}>
                                    Faltan {info.horas}h {info.minutos}m para que quede totalmente activa.
                                  </p>
                                </div>
                              )}

                              {sol.estado === 'Pendiente de validación' && !sol.tiene_justificante && (
                                <button
                                  onClick={() => {
                                    setSolicitudSeleccionada(sol)
                                    setShowJustificante(true)
                                  }}
                                  style={{
                                    width: '100%',
                                    padding: '0.75rem',
                                    background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '8px',
                                    cursor: 'pointer',
                                    fontWeight: '600',
                                    fontSize: '14px',
                                    transition: 'all 0.3s'
                                  }}
                                >
                                  📎 Subir comprobante de transferencia
                                </button>
                              )}

                              {sol.tiene_justificante && sol.estado === 'Pendiente de validación' && (
                                <div style={{
                                  backgroundColor: '#fef3c7',
                                  padding: '1rem',
                                  borderRadius: '8px',
                                  fontSize: '13px',
                                  borderLeft: '4px solid #f59e0b'
                                }}>
                                  <p style={{ margin: 0, fontWeight: '600', color: '#374151' }}>📋 Comprobante en revisión por el administrador</p>
                                </div>
                              )}
                            </div>
                          )
                        })}
                      </div>
                    ) : (
                      <div style={{
                        padding: '3rem 2rem',
                        backgroundColor: 'linear-gradient(135deg, #f0f9ff 0%, #eff6ff 100%)',
                        borderRadius: '12px',
                        textAlign: 'center',
                        color: '#0369a1',
                        border: '2px dashed #0284c7'
                      }}>
                        <p style={{ fontSize: '18px', fontWeight: '600' }}>📭 No tienes solicitudes</p>
                        <p style={{ color: '#6b7280', marginTop: '0.5rem' }}>¡Comienza a invertir ahora mismo!</p>
                      </div>
                    )
                  })()}
                </div>
              </div>
            )
          }

          {
            activeTab === 'referidos' && (
              <div className="content-grid" style={{ display: 'grid', gap: '2rem' }}>
                {/* Panel Principal de Referidos */}
                <div style={{
                  background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                  borderRadius: '12px',
                  padding: '2rem',
                  color: 'white',
                  boxShadow: '0 8px 16px rgba(16, 185, 129, 0.3)',
                  border: '2px solid rgba(255,255,255,0.2)'
                }}>
                  <h2 style={{ marginTop: 0, fontSize: '24px' }}>🎯 Tu Programa de Referidos</h2>
                  <p style={{ opacity: 0.95, marginBottom: '1rem', fontSize: '15px' }}>Gana el <strong>10% de cada inversión</strong> que realicen tus referidos. Acelerado al 300%.</p>

                  <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
                    <input
                      type="text"
                      value={`${window.location.origin}?ref=${getCodigoReferidoInversor().codigo}`}
                      readOnly
                      style={{
                        flex: 1,
                        minWidth: '200px',
                        padding: '10px 12px',
                        border: '2px solid rgba(255,255,255,0.3)',
                        borderRadius: '8px',
                        fontFamily: 'monospace',
                        fontSize: '13px',
                        backgroundColor: 'rgba(255,255,255,0.1)',
                        color: 'white'
                      }}
                    />
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(`${window.location.origin}?ref=${getCodigoReferidoInversor().codigo}`)
                        setSuccessRetiro('✅ Enlace copiado')
                        setTimeout(() => setSuccessRetiro(''), 2000)
                      }}
                      style={{
                        padding: '10px 20px',
                        backgroundColor: 'rgba(255,255,255,0.2)',
                        color: 'white',
                        border: '2px solid rgba(255,255,255,0.3)',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontWeight: '600',
                        whiteSpace: 'nowrap',
                        transition: 'all 0.3s'
                      }}
                    >
                      📋 Copiar
                    </button>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
                    <div style={{ padding: '1rem', backgroundColor: 'rgba(255,255,255,0.15)', borderRadius: '8px', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.2)' }}>
                      <p style={{ margin: 0, fontSize: '12px', opacity: 0.9, fontWeight: '600' }}>👥 Referidos Activos</p>
                      <p style={{ fontSize: '24px', fontWeight: 'bold', margin: '0.5rem 0 0 0' }}>{getReferidosDelInversor().length}</p>
                    </div>
                    <div style={{ padding: '1rem', backgroundColor: 'rgba(255,255,255,0.15)', borderRadius: '8px', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.2)' }}>
                      <p style={{ margin: 0, fontSize: '12px', opacity: 0.9, fontWeight: '600' }}>💰 Comisiones Ganadas</p>
                      <p style={{ fontSize: '24px', fontWeight: 'bold', margin: '0.5rem 0 0 0' }}>€{getReferidosDelInversor().reduce((sum, ref) => sum + ((ref.inversionTotal || 0) * 0.1), 0).toFixed(2)}</p>
                    </div>
                    <div style={{ padding: '1rem', backgroundColor: 'rgba(255,255,255,0.15)', borderRadius: '8px', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.2)' }}>
                      <p style={{ margin: 0, fontSize: '12px', opacity: 0.9, fontWeight: '600' }}>📊 Inversión Total</p>
                      <p style={{ fontSize: '24px', fontWeight: 'bold', margin: '0.5rem 0 0 0' }}>€{getReferidosDelInversor().reduce((sum, ref) => sum + (ref.inversionTotal || 0), 0).toFixed(2)}</p>
                    </div>
                  </div>
                </div>

                {/* Tabla o Gráfica de Referidos */}
                {getReferidosDelInversor().length > 0 ? (
                  <div className="referrals-panel" style={{
                    backgroundColor: 'rgba(15, 23, 42, 0.88)',
                    borderRadius: '12px',
                    padding: '1.5rem',
                    boxShadow: '0 8px 20px rgba(0, 0, 0, 0.28)',
                    border: '1px solid rgba(148, 163, 184, 0.2)'
                  }}>
                    <h3 style={{ marginTop: 0, color: '#f8fafc' }}>📈 Mis Referidos</h3>

                    {/* Gráfica de inversiones */}
                    {getReferidosDelInversor().length > 0 && (
                      <ResponsiveContainer width="100%" height={250}>
                        <BarChart data={getReferidosDelInversor().map((ref, idx) => ({
                          nombre: `Ref ${idx + 1}`,
                          inversion: ref.inversionTotal || 0,
                          comision: (ref.inversionTotal || 0) * 0.1
                        }))}>
                          <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.22)" />
                          <XAxis dataKey="nombre" stroke="#cbd5e1" tick={{ fill: '#cbd5e1', fontSize: 12 }} />
                          <YAxis stroke="#cbd5e1" tick={{ fill: '#cbd5e1', fontSize: 12 }} />
                          <Tooltip formatter={(value) => `€${value.toFixed(2)}`} contentStyle={{ backgroundColor: '#0f172a', border: '1px solid rgba(148, 163, 184, 0.28)', borderRadius: '8px' }} labelStyle={{ color: '#f8fafc' }} itemStyle={{ color: '#e2e8f0' }} />
                          <Legend wrapperStyle={{ color: '#e2e8f0' }} />
                          <Bar dataKey="inversion" fill="#0284c7" name="Inversión" />
                          <Bar dataKey="comision" fill="#10b981" name="Comisión 10%" />
                        </BarChart>
                      </ResponsiveContainer>
                    )}

                    <div className="referrals-table-scroll" style={{ overflowX: 'auto', marginTop: '1.5rem' }}>
                      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', color: '#e2e8f0' }}>
                        <thead>
                          <tr style={{ backgroundColor: 'rgba(51, 65, 85, 0.82)', borderBottom: '1px solid rgba(148, 163, 184, 0.28)' }}>
                            <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>👤 Referido</th>
                            <th style={{ padding: '12px', textAlign: 'right', fontWeight: '600' }}>💵 Inversión</th>
                            <th style={{ padding: '12px', textAlign: 'right', fontWeight: '600' }}>🎁 Comisión</th>
                            <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>📅 Fecha</th>
                          </tr>
                        </thead>
                        <tbody>
                          {getReferidosDelInversor().slice(0, mostrarTodosReferidos ? undefined : 5).map((ref, idx) => {
                            const comision = (ref.inversionTotal || 0) * 0.1
                            return (
                              <tr key={idx} style={{ borderBottom: '1px solid rgba(148, 163, 184, 0.12)', backgroundColor: idx % 2 === 0 ? 'rgba(15, 23, 42, 0.56)' : 'rgba(30, 41, 59, 0.52)' }}>
                                <td style={{ padding: '12px', color: '#f8fafc' }}><strong>{ref.nombreReferido || ref.nombreInversor || 'Usuario'}</strong></td>
                                <td style={{ padding: '12px', textAlign: 'right', color: '#0284c7', fontWeight: '600' }}>€{Number(ref.inversionTotal || 0).toLocaleString('es-ES')}</td>
                                <td style={{ padding: '12px', textAlign: 'right', fontWeight: '600', color: '#10b981', fontSize: '15px' }}>€{comision.toFixed(2)}</td>
                                <td style={{ padding: '12px', color: '#cbd5e1', fontSize: '12px' }}>{new Date(ref.fecha || Date.now()).toLocaleDateString('es-ES')}</td>
                              </tr>
                            )
                          })}
                        </tbody>
                      </table>
                    </div>
                    {getReferidosDelInversor().length > 5 && (
                      <button
                        type="button"
                        onClick={() => setMostrarTodosReferidos(!mostrarTodosReferidos)}
                        style={{ marginTop: '1rem', padding: '9px 14px', backgroundColor: 'transparent', color: '#7dd3fc', border: '1px solid #0284c7', borderRadius: '6px', cursor: 'pointer', fontWeight: '600' }}
                      >
                        {mostrarTodosReferidos ? 'Ver menos' : `Ver más (${getReferidosDelInversor().length - 5})`}
                      </button>
                    )}
                  </div>
                ) : (
                  <div style={{
                    padding: '3rem 2rem',
                    background: 'rgba(6, 78, 59, 0.32)',
                    borderRadius: '12px',
                    textAlign: 'center',
                    color: '#d1fae5',
                    border: '1px dashed rgba(16, 185, 129, 0.7)'
                  }}>
                    <p style={{ fontSize: '18px', fontWeight: '600', margin: 0 }}>👥 Aún no tienes referidos</p>
                    <p style={{ color: '#a7f3d0', marginTop: '0.5rem' }}>¡Comparte tu enlace arriba para empezar a ganar comisiones!</p>
                  </div>
                )}
              </div>
            )
          }

          {/* Panel de Comunidad (Solo Líderes) */}
          {
            activeTab === 'comunidad-lider' && esLiderPropio && (
              <div className="content-grid" style={{ display: 'grid', gap: '1.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <h2 style={{ margin: 0, color: '#f8fafc', fontSize: '1.5rem', fontWeight: '800' }}>👑 Mi Comunidad (Niveles Infinitos)</h2>
                    <p style={{ margin: '0.4rem 0 0 0', color: '#94a3b8', fontSize: '14px' }}>Visualiza el crecimiento completo de todas tus ramas y sub-ramas de referidos al momento.</p>
                  </div>
                </div>

                {!datosComunidadLider ? (
                  <div style={{ padding: '3rem', textAlign: 'center', color: '#94a3b8', background: 'rgba(15, 23, 42, 0.7)', borderRadius: '12px' }}>
                    <p>Cargando datos de comunidad...</p>
                  </div>
                ) : (
                  <>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '1rem' }}>
                      <div style={{ padding: '1.5rem', backgroundColor: 'rgba(15, 23, 42, 0.88)', borderRadius: '12px', border: '1px solid rgba(148, 163, 184, 0.2)', boxShadow: '0 8px 20px rgba(0,0,0,0.2)' }}>
                        <p style={{ margin: 0, fontSize: '13px', opacity: 0.9, fontWeight: '600', color: '#cbd5e1' }}>👥 Personas en tu Red</p>
                        <p style={{ fontSize: '28px', fontWeight: 'bold', margin: '0.5rem 0 0 0', color: '#f8fafc' }}>{datosComunidadLider.total_miembros}</p>
                      </div>
                      <div style={{ padding: '1.5rem', backgroundColor: 'rgba(16, 185, 129, 0.1)', borderRadius: '12px', border: '1px solid rgba(16, 185, 129, 0.3)', boxShadow: '0 8px 20px rgba(0,0,0,0.2)' }}>
                        <p style={{ margin: 0, fontSize: '13px', opacity: 0.9, fontWeight: '600', color: '#86efac' }}>💰 Volumen Activo</p>
                        <p style={{ fontSize: '28px', fontWeight: 'bold', margin: '0.5rem 0 0 0', color: '#10b981' }}>€{(datosComunidadLider.total_capital || 0).toLocaleString('es-ES')}</p>
                      </div>
                      <div style={{ padding: '1.5rem', backgroundColor: 'rgba(239, 68, 68, 0.1)', borderRadius: '12px', border: '1px solid rgba(239, 68, 68, 0.3)', boxShadow: '0 8px 20px rgba(0,0,0,0.2)' }}>
                        <p style={{ margin: 0, fontSize: '13px', opacity: 0.9, fontWeight: '600', color: '#fca5a5' }}>⛔ Vencido (300%)</p>
                        <p style={{ fontSize: '28px', fontWeight: 'bold', margin: '0.5rem 0 0 0', color: '#ef4444' }}>€{(datosComunidadLider.total_vencido || 0).toLocaleString('es-ES')}</p>
                      </div>
                      <div style={{ padding: '1.5rem', backgroundColor: 'rgba(59, 130, 246, 0.1)', borderRadius: '12px', border: '1px solid rgba(59, 130, 246, 0.3)', boxShadow: '0 8px 20px rgba(0,0,0,0.2)' }}>
                        <p style={{ margin: 0, fontSize: '13px', opacity: 0.9, fontWeight: '600', color: '#93c5fd' }}>💎 Ganancias Totales</p>
                        <p style={{ fontSize: '28px', fontWeight: 'bold', margin: '0.5rem 0 0 0', color: '#3b82f6' }}>€{(datosComunidadLider.total_ganancias || 0).toLocaleString('es-ES')}</p>
                      </div>
                    </div>

                    <div className="referrals-panel" style={{
                      backgroundColor: 'rgba(15, 23, 42, 0.88)', borderRadius: '12px', padding: '1.5rem',
                      boxShadow: '0 8px 20px rgba(0, 0, 0, 0.28)', border: '1px solid rgba(148, 163, 184, 0.2)'
                    }}>
                      <h3 style={{ marginTop: 0, color: '#f8fafc', marginBottom: '1.5rem' }}>🌲 Estructura del Árbol</h3>

                      {datosComunidadLider.miembros && datosComunidadLider.miembros.length > 0 ? (
                        <div className="referrals-table-scroll" style={{ overflowX: 'auto' }}>
                          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', color: '#e2e8f0', textAlign: 'left' }}>
                            <thead>
                              <tr style={{ backgroundColor: 'rgba(51, 65, 85, 0.82)', borderBottom: '1px solid rgba(148, 163, 184, 0.28)' }}>
                                <th style={{ padding: '12px', fontWeight: '600' }}>Nivel</th>
                                <th style={{ padding: '12px', fontWeight: '600' }}>Inversor</th>
                                <th style={{ padding: '12px', fontWeight: '600' }}>País</th>
                                <th style={{ padding: '12px', fontWeight: '600' }}>Inversión Activa</th>
                                <th style={{ padding: '12px', fontWeight: '600' }}>Ganado</th>
                                <th style={{ padding: '12px', fontWeight: '600' }}>300% Alcanzado</th>
                              </tr>
                            </thead>
                            <tbody>
                              {datosComunidadLider.miembros.map((miembro) => (
                                <tr key={miembro.id} style={{ borderBottom: '1px solid rgba(148, 163, 184, 0.12)' }}>
                                  <td style={{ padding: '12px' }}>
                                    <span style={{
                                      backgroundColor: miembro.nivel === 1 ? 'rgba(59, 130, 246, 0.2)' : miembro.nivel === 2 ? 'rgba(245, 158, 11, 0.2)' : 'rgba(148, 163, 184, 0.1)',
                                      color: miembro.nivel === 1 ? '#93c5fd' : miembro.nivel === 2 ? '#fcd34d' : '#cbd5e1',
                                      padding: '4px 8px', borderRadius: '4px', fontWeight: '700', fontSize: '12px'
                                    }}>Nivel {miembro.nivel}</span>
                                  </td>
                                  <td style={{ padding: '12px', color: '#f8fafc', fontWeight: '600' }}>
                                    {miembro.nombre}
                                  </td>
                                  <td style={{ padding: '12px', color: '#cbd5e1' }}>{miembro.pais || '—'}</td>
                                  <td style={{ padding: '12px', color: '#10b981', fontWeight: 'bold' }}>
                                    €{Number(miembro.capital_activo || 0).toLocaleString('es-ES')}
                                  </td>
                                  <td style={{ padding: '12px', color: '#3b82f6', fontWeight: 'bold' }}>
                                    €{Number(miembro.capital_ganado || 0).toLocaleString('es-ES')}
                                  </td>
                                  <td style={{ padding: '12px', color: '#ef4444', fontWeight: 'bold' }}>
                                    €{Number(miembro.capital_vencido || 0).toLocaleString('es-ES')}
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      ) : (
                        <p style={{ color: '#94a3b8', textAlign: 'center', marginTop: '2rem' }}>Aún no hay inversores en tu red de comunidad.</p>
                      )}
                    </div>
                  </>
                )}
              </div>
            )
          }

          {/* Pestaña: Ofertas Privadas */}
          {
            activeTab === 'ofertas' && (
              <div className="card admin-futuristic-card">
                <div className="section-header">
                  <h2>🎁 Ofertas Restringidas</h2>
                </div>
                <p style={{ color: '#94a3b8', fontSize: 14, marginBottom: '2rem' }}>
                  Ofertas especiales exclusivas para tu nivel de socio y líderes destacables.
                </p>

                {ofertasAsignadas.length === 0 ? (
                  <div style={{
                    padding: '3rem 2rem',
                    background: 'rgba(15, 23, 42, 0.6)',
                    borderRadius: '12px',
                    textAlign: 'center',
                    color: '#94a3b8',
                    border: '1px solid rgba(255,255,255,0.05)'
                  }}>
                    <p style={{ fontSize: '18px', margin: 0 }}>No hay ofertas privadas disponibles para tu rango actualmente.</p>
                    <p style={{ marginTop: '0.5rem' }}>Sigue sumando referidos y aumentando tu capital para calificar pronto.</p>
                  </div>
                ) : (
                  <div style={{ display: 'grid', gap: '1.5rem', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
                    {ofertasAsignadas.map(of => (
                      <div key={of.id} style={{
                        background: 'linear-gradient(145deg, rgba(16,185,129,0.1), rgba(15,23,42,0.9))',
                        border: '1px solid rgba(16,185,129,0.3)',
                        borderRadius: 14,
                        padding: '1.5rem',
                        display: 'flex',
                        flexDirection: 'column',
                        position: 'relative'
                      }}>
                        <div style={{ position: 'absolute', top: 12, right: 12 }}>
                          <span style={{ background: 'rgba(16, 185, 129, 0.2)', color: '#10b981', padding: '4px 10px', borderRadius: 20, fontSize: 12 }}>
                            Activa
                          </span>
                        </div>
                        <h3 style={{ margin: '0 0 0.5rem 0', color: '#10b981' }}>{of.nombre}</h3>
                        <p style={{ fontSize: 13, color: '#f8fafc', marginBottom: '1rem', minHeight: 40 }}>{of.descripcion}</p>

                        <div style={{ marginBottom: '1rem', background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '8px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px', fontSize: 12 }}>
                            <span style={{ color: '#94a3b8' }}>Llenado:</span>
                            <span style={{ color: '#f1f5f9', fontWeight: 'bold' }}>{of.progresoActual} / {of.importeMaximo} USDT</span>
                          </div>
                          <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: 10, height: 8, width: '100%', overflow: 'hidden' }}>
                            <div style={{ background: '#10b981', height: '100%', width: `${Math.min(100, (Number(of.progresoActual) / Number(of.importeMaximo)) * 100)}%` }}></div>
                          </div>
                        </div>

                        <div style={{ fontSize: 12, color: '#94a3b8', marginBottom: '1.5rem' }}>
                          {of.condiciones && <p style={{ margin: 0, fontStyle: 'italic' }}>* {of.condiciones}</p>}
                        </div>

                        <button onClick={async () => {
                          const monto = prompt(`Ingresa el importe que deseas aportar a la oferta "${of.nombre}":`)
                          if (!monto || isNaN(monto) || Number(monto) <= 0) return alert('Importe inválido.')
                          if (Number(monto) + Number(of.progresoActual) > Number(of.importeMaximo)) return alert('Esta oferta no admite un importe tan alto porque supera el máximo autorizado.')

                          // Simulamos upload comprobante via prompt local para el inversor
                          const nuevaAportacion = {
                            id: Date.now().toString(),
                            ofertaId: of.id,
                            inversorNombre: currentUser?.name || currentUser?.nombre || 'Inversor',
                            inversorId: currentUser?.id,
                            importe: Number(monto),
                            comprobante: null,
                            estado: 'Pendiente de validación',
                            fecha: new Date().toISOString()
                          }

                          const fileInput = document.createElement('input')
                          fileInput.type = 'file'
                          fileInput.accept = 'image/*,application/pdf'
                          fileInput.onchange = (e) => {
                            const file = e.target.files[0]
                            if (file) {
                              const reader = new FileReader()
                              reader.onload = async (re) => {
                                nuevaAportacion.comprobante = re.target.result

                                try {
                                  const token = localStorage.getItem('token')
                                  const response = await fetch(`${API_URL}/api/ofertas/aportaciones`, {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                                    body: JSON.stringify(nuevaAportacion)
                                  })
                                  if (response.ok) {
                                    const updated = [...ofertasAportaciones, nuevaAportacion]
                                    setOfertasAportaciones(updated)
                                    alert('✅ Tu aportación ha sido enviada para validación con el comprobante de pago.')
                                  } else {
                                    alert('Error al enviar aportación')
                                  }
                                } catch (err) {
                                  console.log(err)
                                  alert('Hubo un error contactando el servidor')
                                }
                              }
                              reader.readAsDataURL(file)
                            }
                          }
                          alert('A continuación, selecciona el PDF o Imagen de tu comprobante de depósito.')
                          fileInput.click()

                        }} style={{ marginTop: 'auto', padding: '10px', background: 'linear-gradient(135deg, #10b981, #059669)', color: 'white', border: 'none', borderRadius: 8, cursor: 'pointer', fontWeight: 'bold' }}>
                          APORTAR AHORA
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )
          }

          {/* Modal de Justificante */}
          {
            showJustificante && solicitudSeleccionada && (
              <div style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 1000
              }}>
                <div style={{
                  backgroundColor: 'white',
                  borderRadius: '12px',
                  padding: '2rem',
                  maxWidth: '500px',
                  width: '90%',
                  boxShadow: '0 20px 25px rgba(0, 0, 0, 0.15)'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                    <h2 style={{ margin: 0 }}>📎 Subir Comprobante</h2>
                    <button onClick={() => {
                      setShowJustificante(false)
                      setSolicitudSeleccionada(null)
                      setArchivoJustificante(null)
                      setErrorJustificante('')
                    }} style={{
                      background: 'none',
                      border: 'none',
                      fontSize: '24px',
                      cursor: 'pointer',
                      color: '#6b7280'
                    }}>×</button>
                  </div>

                  <p style={{ color: '#6b7280', marginBottom: '1rem' }}>
                    Solicitud: {formatCurrency(Number(solicitudSeleccionada.importe), solicitudSeleccionada.moneda)}
                  </p>

                  {/* Mostrar cuenta bancaria de referencia */}
                  <div style={{ backgroundColor: '#f59e0b', border: '4px solid #f59e0b', borderRadius: '12px', padding: '2rem', marginBottom: '1.5rem', color: 'white' }}>
                    <p style={{ margin: '0 0 1.5rem 0', fontWeight: 'bold', fontSize: '18px' }}>📌 Referencia de transferencia</p>
                    {(() => {
                      const cuentasAdmin = cuentasPago
                      const cuentaSeleccionada = cuentasAdmin.find(c => c.moneda === solicitudSeleccionada.moneda)
                      return cuentaSeleccionada ? (
                        <div style={{ display: 'grid', gap: '1.2rem' }}>
                          {cuentaSeleccionada.titular && (
                            <div style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: '1rem', borderRadius: '8px' }}>
                              <p style={{ margin: '0', fontWeight: 'bold', fontSize: '14px', opacity: 0.9 }}>👤 TITULAR</p>
                              <p style={{ margin: '0.5rem 0 0 0', fontWeight: 'bold', fontSize: '18px' }}>{cuentaSeleccionada.titular}</p>
                            </div>
                          )}
                          <div style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: '1rem', borderRadius: '8px' }}>
                            <p style={{ margin: '0', fontWeight: 'bold', fontSize: '14px', opacity: 0.9 }}>{cuentaSeleccionada.wallet ? '🔗 DIRECCIÓN WALLET' : cuentaSeleccionada.iban ? '🏦 IBAN' : '💳 NÚMERO DE TARJETA'}</p>
                            {(() => {
                              const datoTransferencia = cuentaSeleccionada.iban || cuentaSeleccionada.numero || cuentaSeleccionada.wallet || cuentaSeleccionada.cuenta || '—'
                              return <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginTop: '0.5rem' }}>
                                <p style={{ margin: 0, flex: 1, fontWeight: 'bold', fontSize: '18px', fontFamily: 'monospace', letterSpacing: '1px', wordBreak: 'break-all' }}>{datoTransferencia}</p>
                                <button type="button" onClick={() => copiarDatoPago(datoTransferencia)} style={{ flexShrink: 0, padding: '8px 10px', background: 'rgba(15,23,42,0.28)', color: 'white', border: '1px solid rgba(255,255,255,0.45)', borderRadius: '6px', cursor: 'pointer', fontWeight: '700' }}>{datoCopiado === 'Copiado' ? 'Copiado' : 'Copiar'}</button>
                              </div>
                            })()}
                          </div>
                          {cuentaSeleccionada.concepto && (
                            <div style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: '1rem', borderRadius: '8px' }}>
                              <p style={{ margin: '0', fontWeight: 'bold', fontSize: '14px', opacity: 0.9 }}>📝 CONCEPTO / DESCRIPCIÓN</p>
                              <p style={{ margin: '0.5rem 0 0 0', fontWeight: 'bold', fontSize: '16px' }}>{cuentaSeleccionada.concepto}</p>
                            </div>
                          )}
                          {cuentaSeleccionada.red && (
                            <div style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: '1rem', borderRadius: '8px' }}>
                              <p style={{ margin: '0', fontWeight: 'bold', fontSize: '14px', opacity: 0.9 }}>🌐 RED / BANCO</p>
                              <p style={{ margin: '0.5rem 0 0 0', fontWeight: 'bold', fontSize: '18px' }}>{cuentaSeleccionada.red || cuentaSeleccionada.banco || '—'}</p>
                            </div>
                          )}
                        </div>
                      ) : <p style={{ margin: 0, color: '#ffffff', fontWeight: 'bold', fontSize: '16px', backgroundColor: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '8px' }}>❌ No hay cuenta configurada</p>
                    })()}
                  </div>

                  {errorJustificante && (
                    <div style={{
                      backgroundColor: '#fee2e2',
                      color: '#991b1b',
                      padding: '0.75rem',
                      borderRadius: '6px',
                      marginBottom: '1rem',
                      fontSize: '14px'
                    }}>
                      {errorJustificante}
                    </div>
                  )}

                  <div style={{
                    border: '2px dashed #d1d5db',
                    borderRadius: '8px',
                    padding: '2rem',
                    textAlign: 'center',
                    backgroundColor: '#f9fafb',
                    marginBottom: '1.5rem'
                  }}>
                    <input
                      type="file"
                      id="archivo-justificante"
                      onChange={(e) => setArchivoJustificante(e.target.files?.[0] || null)}
                      accept="image/*,.pdf"
                      style={{ display: 'none' }}
                    />
                    <label htmlFor="archivo-justificante" style={{ cursor: 'pointer', display: 'block' }}>
                      <p style={{ fontSize: '32px', margin: '0' }}>📁</p>
                      <p style={{ margin: '0.5rem 0', fontWeight: '600', color: '#374151' }}>
                        {archivoJustificante ? archivoJustificante.name : 'Haz clic para seleccionar archivo'}
                      </p>
                      <p style={{ margin: '0.5rem 0 0 0', fontSize: '12px', color: '#6b7280' }}>
                        o arrastra un archivo aquí
                      </p>
                      <p style={{ margin: '0.5rem 0 0 0', fontSize: '11px', color: '#9ca3af' }}>
                        JPG, PNG, PDF - Máximo 10MB
                      </p>
                    </label>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                    <button
                      onClick={() => {
                        setShowJustificante(false)
                        setSolicitudSeleccionada(null)
                        setArchivoJustificante(null)
                        setErrorJustificante('')
                      }}
                      style={{
                        padding: '0.75rem',
                        backgroundColor: '#e5e7eb',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontWeight: '600',
                        color: '#374151'
                      }}
                    >
                      Cancelar
                    </button>
                    <button
                      onClick={subirJustificante}
                      style={{
                        padding: '0.75rem',
                        backgroundColor: '#10b981',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontWeight: '600'
                      }}
                    >
                      Subir comprobante
                    </button>
                  </div>
                </div>
              </div>
            )
          }

          {/* Modal de Programa de Aceleración (Rangos) */}
          {
            showRangosModal && (
              <div style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 1000,
                padding: '1rem'
              }}>
                <div style={{
                  backgroundColor: '#07111f',
                  border: '1px solid rgba(168, 85, 247, 0.3)',
                  borderRadius: '16px',
                  padding: '2rem',
                  maxWidth: '650px',
                  width: '95%',
                  maxHeight: '90vh',
                  overflowY: 'auto',
                  boxShadow: '0 20px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(168, 85, 247, 0.15)'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                    <h2 style={{ margin: 0, color: '#f8fafc' }}>🏆 Programa Combinado</h2>
                    <button onClick={() => setShowRangosModal(false)} style={{
                      background: 'none',
                      border: 'none',
                      fontSize: '28px',
                      cursor: 'pointer',
                      color: '#94a3b8',
                      transition: 'color 0.2s'
                    }}>×</button>
                  </div>

                  <p style={{ color: '#94a3b8', fontSize: '14px', marginBottom: '1.5rem', fontWeight: '500', lineHeight: '1.5' }}>
                    En Capital Iberia puedes crecer de dos formas: mediante tu propia participación de capital o desarrollando una comunidad de red protegida.
                  </p>

                  {(() => {
                    const rCapital = getRangoCapital()
                    const rComunidad = getRangoComunidad()
                    const nextCapital = getProximoRangoCapital()
                    const nextComunidad = getProximoRangoComunidad()
                    const referidosActivos = getReferidosActivosCount()

                    return (
                      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
                        <div style={{ backgroundColor: rCapital ? 'rgba(168, 85, 247, 0.15)' : 'rgba(255, 255, 255, 0.03)', color: '#f8fafc', border: rCapital ? '1px solid rgba(168, 85, 247, 0.4)' : '1px solid rgba(255,255,255,0.1)', borderRadius: '12px', padding: '1rem', textAlign: 'center' }}>
                          <p style={{ margin: 0, fontSize: '12px', fontWeight: '700', color: rCapital ? '#c084fc' : '#94a3b8', letterSpacing: '0.05em' }}>💎 RANGO DE CAPITAL</p>
                          <p style={{ margin: '0.6rem 0', fontSize: '18px', fontWeight: '800' }}>
                            {rCapital ? `${rCapital.emoji} ${rCapital.nombre}` : '🔒 Sin rango'}
                          </p>
                          <p style={{ margin: 0, fontSize: '12px', fontWeight: '500', color: '#cbd5e1' }}>Tu Inversión: {formatCurrency(totalAportado, 'EUR')}</p>
                          {nextCapital && (
                            <div style={{ marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                              <p style={{ margin: '0 0 0.35rem 0', fontSize: '11px', fontWeight: '600', color: '#94a3b8' }}>Para {nextCapital.emoji} {nextCapital.nombre} te falta:</p>
                              <p style={{ margin: 0, fontSize: '12px', fontWeight: '700', color: '#60a5fa' }}>💰 {formatCurrency(Math.max(0, nextCapital.min - totalAportado), 'EUR')} más</p>
                            </div>
                          )}
                        </div>

                        <div style={{ backgroundColor: rComunidad ? 'rgba(56, 189, 248, 0.15)' : 'rgba(255, 255, 255, 0.03)', color: '#f8fafc', border: rComunidad ? '1px solid rgba(56, 189, 248, 0.4)' : '1px solid rgba(255,255,255,0.1)', borderRadius: '12px', padding: '1rem', textAlign: 'center' }}>
                          <p style={{ margin: 0, fontSize: '12px', fontWeight: '700', color: rComunidad ? '#38bdf8' : '#94a3b8', letterSpacing: '0.05em' }}>👥 RANGO COMUNIDAD</p>
                          <p style={{ margin: '0.6rem 0', fontSize: '18px', fontWeight: '800' }}>
                            {rComunidad ? `${rComunidad.emoji} ${rComunidad.nombre}` : '🔒 Sin rango'}
                          </p>
                          <p style={{ margin: 0, fontSize: '12px', fontWeight: '500', color: '#cbd5e1' }}>Miembros Activos: {referidosActivos}</p>
                          {nextComunidad && (
                            <div style={{ marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                              <p style={{ margin: '0 0 0.35rem 0', fontSize: '11px', fontWeight: '600', color: '#94a3b8' }}>Para {nextComunidad.emoji} {nextComunidad.nombre} te falta:</p>
                              <p style={{ margin: 0, fontSize: '12px', fontWeight: '700', color: '#60a5fa' }}>👤 {Math.max(0, nextComunidad.min - referidosActivos)} miembro{Math.max(0, nextComunidad.min - referidosActivos) === 1 ? '' : 's'}</p>
                            </div>
                          )}
                        </div>
                      </div>
                    )
                  })()}

                  <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                      <h3 style={{ margin: '0 0 0.75rem 0', color: '#e2e8f0', fontSize: '14px', fontWeight: '700' }}>💎 Niveles Capital</h3>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
                        {NIVELES_CAPITAL.map((nivel) => (
                          <div key={nivel.nombre} style={{ border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px', padding: '0.85rem', fontSize: '12px', backgroundColor: 'rgba(0,0,0,0.3)', color: '#cbd5e1' }}>
                            <strong style={{ display: 'block', fontSize: '13px', color: '#f8fafc', marginBottom: '4px' }}>{nivel.emoji} {nivel.nombre}</strong>
                            <span style={{ color: '#94a3b8' }}>Min: {formatCurrency(nivel.min, 'USD')}</span><br />
                            <span style={{ color: '#4ade80', fontWeight: '600' }}>{nivel.beneficio}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                      <h3 style={{ margin: '0 0 0.75rem 0', color: '#e2e8f0', fontSize: '14px', fontWeight: '700' }}>👥 Niveles Comunidad</h3>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
                        {NIVELES_COMUNIDAD.map((nivel) => (
                          <div key={nivel.nombre} style={{ border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px', padding: '0.85rem', fontSize: '12px', backgroundColor: 'rgba(0,0,0,0.3)', color: '#cbd5e1' }}>
                            <strong style={{ display: 'block', fontSize: '13px', color: '#f8fafc', marginBottom: '4px' }}>{nivel.emoji} {nivel.nombre}</strong>
                            <span style={{ color: '#94a3b8' }}>Min: {nivel.min} actvs.</span><br />
                            <span style={{ color: '#60a5fa', fontWeight: '600' }}>{nivel.bonus}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div style={{ backgroundColor: 'rgba(0,0,0,0.5)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '12px', padding: '1rem', marginBottom: '1rem' }}>
                    <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '14px', fontWeight: '700', color: '#e2e8f0' }}>¿Cómo funciona?</h3>
                    <p style={{ margin: '0.25rem 0', fontSize: '12.5px', color: '#94a3b8', lineHeight: '1.6' }}>
                      <strong style={{ color: '#cbd5e1' }}>Los programas son independientes.</strong> Tus retornos de Capital garantizan mensualidades basadas en tu inversión personal. Tu crecimiento en la Comunidad te recompensa con bonus únicos transferidos por logros de equipo. Un miembro afiliado se considera "Activo" a partir de $100.
                    </p>
                  </div>

                  <div style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.3)', borderRadius: '12px', padding: '1rem' }}>
                    <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '14px', color: '#fbbf24', fontWeight: '700' }}>⚠️ Bonificación aparte</h3>
                    <p style={{ margin: 0, fontSize: '12.5px', color: '#fcd34d', fontWeight: '500', lineHeight: '1.5' }}>
                      Esto no forma parte del programa de aceleración, es una bonificación aparte. Cuando el beneficio se venza y no subas de rango, tendrás otros beneficios adicionales.
                    </p>
                  </div>

                  <div style={{ marginTop: '1.5rem' }}>
                    <button
                      onClick={() => setShowRangosModal(false)}
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        backgroundColor: '#a855f7',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        fontWeight: '600',
                        cursor: 'pointer'
                      }}
                    >
                      Cerrar
                    </button>
                  </div>
                </div>
              </div>
            )
          }

          {/* Modal de Inversión */}
          {
            showInversionModal && (
              <div style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 1000
              }}>
                <div style={{
                  backgroundColor: 'white',
                  borderRadius: '12px',
                  padding: '2rem',
                  maxWidth: '500px',
                  width: '90%',
                  maxHeight: '90vh',
                  overflowY: 'auto',
                  boxShadow: '0 20px 25px rgba(0, 0, 0, 0.15)'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                    <h2 style={{ margin: 0, color: '#111827' }}>💰 Invertir</h2>
                    <button onClick={() => setShowInversionModal(false)} style={{
                      background: 'none',
                      border: 'none',
                      fontSize: '24px',
                      cursor: 'pointer',
                      color: '#6b7280'
                    }}>×</button>
                  </div>

                  {errorInversion && (
                    <div style={{
                      backgroundColor: '#fee2e2',
                      color: '#991b1b',
                      padding: '0.75rem',
                      borderRadius: '6px',
                      marginBottom: '1rem',
                      fontSize: '14px'
                    }}>
                      {errorInversion}
                    </div>
                  )}

                  <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600', color: '#374151' }}>Moneda de inversión</label>
                    <select
                      value={monedaInversion}
                      onChange={(e) => setMonedaInversion(e.target.value)}
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: '1px solid #d1d5db',
                        borderRadius: '6px',
                        fontSize: '14px'
                      }}
                    >
                      <option value="USDT BEP-20">USDT BEP-20 (Criptomoneda)</option>
                      <option value="EUR">EUR - Euro</option>
                    </select>
                  </div>

                  {/* Mostrar cuentas bancarias */}
                  <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '1rem', fontWeight: 'bold', color: '#374151', fontSize: '16px' }}>💳 Datos de transferencia</label>
                    {(() => {
                      const cuentasAdmin = cuentasPago
                      const cuentaSeleccionada = cuentasAdmin.find(c => c.moneda === monedaInversion)
                      return cuentaSeleccionada ? (
                        <div style={{ backgroundColor: '#0284c7', border: '4px solid #0284c7', padding: '1.5rem', borderRadius: '12px', fontSize: '16px', color: 'white' }}>
                          <div style={{ display: 'grid', gap: '1rem' }}>

                            {cuentaSeleccionada.titular && (
                              <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '8px' }}>
                                <p style={{ margin: '0', fontWeight: 'bold', fontSize: '14px', opacity: 0.9 }}>👤 TITULAR</p>
                                <p style={{ margin: '0.5rem 0 0 0', fontWeight: 'bold', fontSize: '18px' }}>{cuentaSeleccionada.titular}</p>
                              </div>
                            )}

                            <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '8px' }}>
                              <p style={{ margin: '0', fontWeight: 'bold', fontSize: '14px', opacity: 0.9 }}>{cuentaSeleccionada.wallet ? '🔗 DIRECCIÓN WALLET' : cuentaSeleccionada.iban ? '🏦 IBAN' : '💳 NÚMERO DE TARJETA'}</p>
                              {(() => {
                                const datoTransferencia = cuentaSeleccionada.iban || cuentaSeleccionada.numero || cuentaSeleccionada.wallet || cuentaSeleccionada.cuenta || '—'
                                return <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginTop: '0.5rem' }}>
                                  <p style={{ margin: 0, flex: 1, fontWeight: 'bold', fontSize: '18px', fontFamily: 'monospace', letterSpacing: '1px', wordBreak: 'break-all' }}>{datoTransferencia}</p>
                                  <button type="button" onClick={() => copiarDatoPago(datoTransferencia)} style={{ flexShrink: 0, padding: '8px 10px', background: 'rgba(255,255,255,0.16)', color: 'white', border: '1px solid rgba(255,255,255,0.45)', borderRadius: '6px', cursor: 'pointer', fontWeight: '700' }}>{datoCopiado === 'Copiado' ? 'Copiado' : 'Copiar'}</button>
                                </div>
                              })()}
                            </div>

                            {cuentaSeleccionada.concepto && (
                              <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '8px' }}>
                                <p style={{ margin: '0', fontWeight: 'bold', fontSize: '14px', opacity: 0.9 }}>📝 CONCEPTO / DESCRIPCIÓN</p>
                                <p style={{ margin: '0.5rem 0 0 0', fontWeight: 'bold', fontSize: '16px' }}>{cuentaSeleccionada.concepto}</p>
                              </div>
                            )}

                            {cuentaSeleccionada.red && (
                              <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '8px', backdropFilter: 'blur(10px)' }}>
                                <p style={{ margin: '0', fontWeight: 'bold', fontSize: '14px', opacity: 0.9 }}>🌐 RED / BANCO</p>
                                <p style={{ margin: '0.5rem 0 0 0', fontWeight: 'bold', fontSize: '18px' }}>{cuentaSeleccionada.red || cuentaSeleccionada.banco || '—'}</p>
                              </div>
                            )}

                            <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '8px' }}>
                              <p style={{ margin: '0', fontWeight: 'bold', fontSize: '14px', opacity: 0.9 }}>📋 INSTRUCCIONES DEL ADMIN</p>
                              <p style={{ margin: '0.5rem 0 0 0', fontWeight: 'bold', fontSize: '16px' }}>{cuentaSeleccionada.instrucciones || 'Sin instrucciones adicionales'}</p>
                            </div>
                          </div>
                        </div>
                      ) : <p style={{ color: '#ef4444', fontWeight: 'bold', fontSize: '16px', backgroundColor: '#fee2e2', padding: '1rem', borderRadius: '8px' }}>❌ No hay cuenta configurada o activa para esta moneda</p>
                    })()}
                  </div>

                  <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600', color: '#374151' }}>Monto a invertir</label>
                    <input
                      type="number"
                      value={montoInversion}
                      onChange={(e) => setMontoInversion(e.target.value)}
                      placeholder="Ej: 1000"
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: '1px solid #d1d5db',
                        borderRadius: '6px',
                        fontSize: '14px',
                        boxSizing: 'border-box'
                      }}
                    />
                    <p style={{ fontSize: '12px', color: '#6b7280', margin: '0.5rem 0 0 0' }}>
                      Mínimo: {(() => {
                        const cuentasAdmin = cuentasPago
                        const cuentaConfig = cuentasAdmin.find(c => c.moneda === monedaInversion)
                        const val = cuentaConfig?.minimo ? Number(cuentaConfig.minimo) : 100
                        return formatCurrency(val, monedaInversion)
                      })()}
                    </p>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                    <button
                      onClick={() => setShowInversionModal(false)}
                      style={{
                        padding: '0.75rem',
                        backgroundColor: '#e5e7eb',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontWeight: '600',
                        color: '#374151'
                      }}
                    >
                      Cancelar
                    </button>
                    <button
                      onClick={crearSolicitudInversion}
                      style={{
                        padding: '0.75rem',
                        backgroundColor: '#10b981',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontWeight: '600'
                      }}
                    >
                      Solicitar inversión
                    </button>
                  </div>
                </div>
              </div>
            )
          }

        </div >
      </main >
    </div >
  );
}

export default DashboardInversionista;
