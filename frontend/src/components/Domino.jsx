import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './Domino.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const fichaKey = ficha => ficha.join('-')

function Ficha({ ficha, activa, onClick, compacta = false }) {
  return <button className={`domino-ficha ${activa ? 'activa' : ''} ${compacta ? 'compacta' : ''}`} onClick={onClick} type="button">
    <span>{ficha[0]}</span><i /><span>{ficha[1]}</span>
  </button>
}

function Domino() {
  const navigate = useNavigate()
  const token = localStorage.getItem('token')
  const [salas, setSalas] = React.useState([])
  const [codigoEntrada, setCodigoEntrada] = React.useState('')
  const [codigo, setCodigo] = React.useState('')
  const [partida, setPartida] = React.useState(null)
  const [seleccionada, setSeleccionada] = React.useState(null)
  const [cargando, setCargando] = React.useState(true)
  const [accionando, setAccionando] = React.useState(false)
  const [error, setError] = React.useState('')

  const headers = { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }

  const cargarSalas = async () => {
    try {
      const respuesta = await fetch(`${API}/api/domino/partidas`, { headers })
      const datos = await respuesta.json()
      if (!respuesta.ok) throw new Error(datos.detail || 'No se pudieron cargar las salas.')
      setSalas(datos.salas || [])
    } catch (requestError) {
      setError(requestError.message || 'No se pudieron cargar las salas.')
    } finally {
      setCargando(false)
    }
  }

  const cargarPartida = async codigoPartida => {
    try {
      const respuesta = await fetch(`${API}/api/domino/partidas/${codigoPartida}`, { headers })
      const datos = await respuesta.json()
      if (!respuesta.ok) throw new Error(datos.detail || 'No se pudo recuperar la partida.')
      setPartida(datos)
      setError('')
    } catch (requestError) {
      setError(requestError.message || 'No se pudo recuperar la partida.')
    }
  }

  React.useEffect(() => {
    if (!token) { navigate('/login'); return }
    cargarSalas()
  }, [])

  React.useEffect(() => {
    if (!codigo) return undefined
    cargarPartida(codigo)
    const intervalo = setInterval(() => cargarPartida(codigo), 4000)
    return () => clearInterval(intervalo)
  }, [codigo])

  const crearSala = async () => {
    setAccionando(true); setError('')
    try {
      const respuesta = await fetch(`${API}/api/domino/partidas`, { method: 'POST', headers, body: JSON.stringify({}) })
      const datos = await respuesta.json()
      if (!respuesta.ok) throw new Error(datos.detail || 'No se pudo crear la sala.')
      setCodigo(datos.codigo)
    } catch (requestError) {
      setError(requestError.message || 'No se pudo crear la sala.')
    } finally {
      setAccionando(false)
    }
  }

  const unirse = async codigoSala => {
    const sala = codigoSala.trim().toUpperCase()
    if (!sala) return
    setAccionando(true); setError('')
    try {
      const respuesta = await fetch(`${API}/api/domino/partidas/${sala}/unirse`, { method: 'POST', headers })
      const datos = await respuesta.json()
      if (!respuesta.ok) throw new Error(datos.detail || 'No se pudo entrar a la sala.')
      setCodigo(datos.codigo)
      setCodigoEntrada('')
    } catch (requestError) {
      setError(requestError.message || 'No se pudo entrar a la sala.')
    } finally {
      setAccionando(false)
    }
  }

  const enviarJugada = async lado => {
    if (!seleccionada || !codigo || accionando) return
    setAccionando(true); setError('')
    try {
      const respuesta = await fetch(`${API}/api/domino/partidas/${codigo}/jugar`, { method: 'POST', headers, body: JSON.stringify({ ficha: seleccionada, lado }) })
      const datos = await respuesta.json()
      if (!respuesta.ok) throw new Error(datos.detail || 'No se pudo jugar la ficha.')
      setPartida(datos); setSeleccionada(null)
    } catch (requestError) {
      setError(requestError.message || 'No se pudo jugar la ficha.')
    } finally {
      setAccionando(false)
    }
  }

  const pasar = async () => {
    if (!codigo || accionando) return
    setAccionando(true); setError('')
    try {
      const respuesta = await fetch(`${API}/api/domino/partidas/${codigo}/pasar`, { method: 'POST', headers })
      const datos = await respuesta.json()
      if (!respuesta.ok) throw new Error(datos.detail || 'No puedes pasar ahora.')
      setPartida(datos); setSeleccionada(null)
    } catch (requestError) {
      setError(requestError.message || 'No puedes pasar ahora.')
    } finally {
      setAccionando(false)
    }
  }

  const activarUbicacion = () => {
    if (!navigator.geolocation) {
      setError('Este dispositivo no permite usar ubicación.')
      return
    }
    setAccionando(true); setError('')
    navigator.geolocation.getCurrentPosition(async posicion => {
      try {
        const respuesta = await fetch(`${API}/api/domino/partidas/${codigo}/ubicacion`, {
          method: 'POST', headers,
          body: JSON.stringify({ latitud: posicion.coords.latitude, longitud: posicion.coords.longitude })
        })
        const datos = await respuesta.json()
        if (!respuesta.ok) throw new Error(datos.detail || 'No se pudo validar la ubicación.')
        setPartida(datos)
      } catch (requestError) {
        setError(requestError.message || 'No se pudo validar la ubicación.')
      } finally {
        setAccionando(false)
      }
    }, () => {
      setError('Debes permitir la ubicación para jugar con tu pareja.')
      setAccionando(false)
    }, { enableHighAccuracy: true, timeout: 15000, maximumAge: 300000 })
  }

  const volverASalas = () => {
    setCodigo(''); setPartida(null); setSeleccionada(null); setCargando(true); cargarSalas()
  }

  if (!codigo) return <main className="domino-page">
    <header className="domino-header"><div><p className="domino-eyebrow">Comunidad</p><h1>Dominó suizo</h1><span>Partidas por parejas a 200 puntos</span></div><Link to="/comunidad" className="domino-link">Comunidad</Link></header>
    {error && <p className="domino-error">{error}</p>}
    <section className="domino-lobby">
      <div className="domino-lobby-action"><h2>Nueva mesa</h2><button className="domino-primary" onClick={crearSala} disabled={accionando}>{accionando ? 'Creando...' : 'Crear sala'}</button></div>
      <form className="domino-lobby-action" onSubmit={evento => { evento.preventDefault(); unirse(codigoEntrada) }}><h2>Entrar con código</h2><div className="domino-code-row"><input value={codigoEntrada} onChange={evento => setCodigoEntrada(evento.target.value)} maxLength="6" placeholder="Código" /><button className="domino-secondary" disabled={accionando}>Entrar</button></div></form>
    </section>
    <section className="domino-salas"><div className="domino-section-title"><h2>Salas activas</h2><button onClick={cargarSalas} title="Actualizar salas">Actualizar</button></div>{cargando ? <p>Cargando salas...</p> : salas.length ? <div className="domino-salas-grid">{salas.map(sala => <article key={sala.codigo}><strong>{sala.creador}</strong><span>{sala.jugadores}/4 jugadores</span><small>{sala.estado === 'esperando' ? 'Esperando jugadores' : 'En juego'}</small><button onClick={() => unirse(sala.codigo)} disabled={accionando || (sala.estado === 'jugando' && !sala.es_mia)}>{sala.es_mia ? 'Volver a la mesa' : sala.estado === 'esperando' ? 'Unirse' : 'Completa'}</button></article>)}</div> : <p className="domino-empty">No hay mesas abiertas.</p>}</section>
  </main>

  const miTurno = partida?.turno === partida?.mi_posicion && partida?.estado === 'jugando'
  const jugadorActual = partida?.jugadores?.find(jugador => jugador.posicion === partida?.turno)
  const ganador = partida?.ganador === undefined || partida?.ganador === null ? null : `Pareja ${Number(partida.ganador) + 1}`

  return <main className="domino-page domino-partida">
    <header className="domino-game-header"><button onClick={volverASalas} className="domino-link">Salas</button><div><p className="domino-eyebrow">Mesa {codigo}</p><h1>Dominó suizo</h1></div><span className={miTurno ? 'domino-turno es-mi-turno' : 'domino-turno'}>{ganador ? `${ganador} ganó` : partida?.estado === 'esperando' ? `Esperando ${4 - (partida?.jugadores?.length || 0)} jugadores` : miTurno ? 'Tu turno' : `Turno de ${jugadorActual?.nombre || '...'}`}</span></header>
    {error && <p className="domino-error">{error}</p>}
    <section className="domino-score">{[0, 1].map(pareja => <div key={pareja} className={partida?.mi_posicion % 2 === pareja ? 'mi-pareja' : ''}><span>Pareja {pareja + 1}</span><strong>{partida?.puntuacion?.[pareja] || 0}</strong><small>/ {partida?.limite_puntos || 200}</small></div>)}</section>
    {partida?.estado === 'jugando' && <section className={`domino-ubicacion ${partida.ubicacion_pareja_lista ? 'verificada' : ''}`}><span>{partida.ubicacion_pareja_lista ? 'Ubicación de la pareja verificada' : 'La pareja debe validar una distancia mínima de 1 km'}</span>{!partida.ubicacion_pareja_lista && <button className="domino-secondary" onClick={activarUbicacion} disabled={accionando}>Activar ubicación</button>}</section>}
    <section className="domino-jugadores">{partida?.jugadores?.map(jugador => <div className={`${jugador.posicion === partida.mi_posicion ? 'soy-yo ' : ''}${jugador.posicion === partida.turno ? 'turno-activo' : ''}`} key={jugador.id}><strong>{jugador.nombre}{jugador.posicion === partida.mi_posicion ? ' (tú)' : ''}</strong><span>{jugador.fichas} fichas</span></div>)}</section>
    <section className="domino-tablero"><div className="domino-mesa">{partida?.mesa?.length ? partida.mesa.map((ficha, indice) => <Ficha key={`${fichaKey(ficha)}-${indice}`} ficha={ficha} compacta />) : <span>La mesa espera la salida.</span>}</div>{miTurno && partida?.estado === 'jugando' && <div className="domino-controles"><button className="domino-secondary" disabled={!seleccionada || accionando} onClick={() => enviarJugada('izquierda')}>Jugar izquierda</button><button className="domino-primary" disabled={!seleccionada || accionando} onClick={() => enviarJugada('derecha')}>Jugar derecha</button><button className="domino-pass" disabled={accionando} onClick={pasar}>Pasar</button></div>}</section>
    <section className="domino-mano"><div><h2>Tus fichas</h2><span>{miTurno ? 'Selecciona una ficha' : 'Esperando turno'}</span></div><div className="domino-fichas">{partida?.mis_fichas?.map((ficha, indice) => <Ficha key={`${fichaKey(ficha)}-${indice}`} ficha={ficha} activa={seleccionada && fichaKey(seleccionada) === fichaKey(ficha)} onClick={() => miTurno && setSeleccionada(ficha)} />)}</div></section>
    <section className="domino-eventos"><h2>Últimas jugadas</h2>{partida?.eventos?.map((evento, indice) => <p key={`${evento}-${indice}`}>{evento}</p>)}</section>
  </main>
}

export default Domino