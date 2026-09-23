import React from 'react'
import { useNavigate } from 'react-router-dom'
import './Domino.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const fichaKey = ficha => ficha.join('-')

const puntosPorValor = { 0: [], 1: ['centro'], 2: ['arriba-izquierda', 'abajo-derecha'], 3: ['arriba-izquierda', 'centro', 'abajo-derecha'], 4: ['arriba-izquierda', 'arriba-derecha', 'abajo-izquierda', 'abajo-derecha'], 5: ['arriba-izquierda', 'arriba-derecha', 'centro', 'abajo-izquierda', 'abajo-derecha'], 6: ['arriba-izquierda', 'arriba-derecha', 'medio-izquierda', 'medio-derecha', 'abajo-izquierda', 'abajo-derecha'] }

function Cara({ valor }) {
  return <span className="domino-cara">{puntosPorValor[valor].map(posicion => <i key={posicion} className={posicion} />)}</span>
}

function Ficha({ ficha, activa, onClick, compacta = false, mesaClase = '', style }) {
  return <button className={`domino-ficha ${activa ? 'activa' : ''} ${compacta ? 'compacta' : ''} ${compacta && ficha[0] === ficha[1] ? 'doble' : ''} ${mesaClase}`} onClick={onClick} style={style} type="button" aria-label={`${ficha[0]} con ${ficha[1]}`}>
    <Cara valor={ficha[0]} /><b /><Cara valor={ficha[1]} />
  </button>
}

function claseMesa(indice) {
  if (indice < 8) return `mesa-tramo uno posicion-${indice}`
  if (indice < 13) return `mesa-tramo giro-derecha posicion-${indice - 8}`
  if (indice < 21) return `mesa-tramo dos posicion-${indice - 13}`
  return `mesa-tramo giro-izquierda posicion-${indice - 21}`
}

function asientoMesa(posicion, miPosicion) {
  return ['abajo', 'derecha', 'arriba', 'izquierda'][(posicion - miPosicion + 4) % 4]
}

function Domino() {
  const navigate = useNavigate()
  const token = localStorage.getItem('token')
  const [codigo, setCodigo] = React.useState(() => new URLSearchParams(window.location.search).get('mesa') || '')
  const [partida, setPartida] = React.useState(null)
  const [seleccionada, setSeleccionada] = React.useState(null)
  const [accionando, setAccionando] = React.useState(false)
  const [error, setError] = React.useState('')

  const headers = { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }

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
    if (!codigo) navigate('/domino/torneos', { replace: true })
  }, [])

  React.useEffect(() => {
    if (!codigo) return undefined
    cargarPartida(codigo)
    const intervalo = setInterval(() => cargarPartida(codigo), 4000)
    return () => clearInterval(intervalo)
  }, [codigo])

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
    navigate('/domino/torneos')
  }

  if (!codigo) return null

  const miTurno = partida?.turno === partida?.mi_posicion && partida?.estado === 'jugando'
  const jugadorActual = partida?.jugadores?.find(jugador => jugador.posicion === partida?.turno)
  const ganador = partida?.ganador === undefined || partida?.ganador === null ? null : `Pareja ${Number(partida.ganador) + 1}`

  return <main className="domino-page domino-partida">
    <header className="domino-game-header"><button onClick={volverASalas} className="domino-link">Torneo</button><div><p className="domino-eyebrow">Mesa {codigo}</p><h1>Dominó suizo</h1></div><span className={miTurno ? 'domino-turno es-mi-turno' : 'domino-turno'}>{ganador ? `${ganador} ganó` : partida?.estado === 'esperando' ? `Esperando ${4 - (partida?.jugadores?.length || 0)} jugadores` : miTurno ? 'Tu turno' : `Turno de ${jugadorActual?.nombre || '...'}`}</span></header>
    {error && <p className="domino-error">{error}</p>}
    <section className="domino-score">{[0, 1].map(pareja => <div key={pareja} className={partida?.mi_posicion % 2 === pareja ? 'mi-pareja' : ''}><span>Pareja {pareja + 1}</span><strong>{partida?.puntuacion?.[pareja] || 0}</strong><small>/ {partida?.limite_puntos || 200}</small></div>)}</section>
    {partida?.estado === 'jugando' && <section className={`domino-ubicacion ${partida.ubicacion_pareja_lista ? 'verificada' : ''}`}><span>{partida.ubicacion_pareja_lista ? 'Ubicación de la pareja verificada' : 'La pareja debe validar una distancia mínima de 1 km'}</span>{!partida.ubicacion_pareja_lista && <button className="domino-secondary" onClick={activarUbicacion} disabled={accionando}>Activar ubicación</button>}</section>}
    <section className="domino-tablero"><div className="domino-mesa">{partida?.jugadores?.map(jugador => <div className={`domino-asiento ${asientoMesa(jugador.posicion, partida.mi_posicion)} ${jugador.posicion === partida.mi_posicion ? 'soy-yo ' : ''}${jugador.posicion === partida.turno ? 'turno-activo' : ''}`} key={jugador.id}><div className="domino-avatar">{jugador.nombre.slice(0, 1).toUpperCase()}</div><div><strong>{jugador.nombre}{jugador.posicion === partida.mi_posicion ? ' (tú)' : ''}</strong><span>{jugador.fichas} fichas</span></div></div>)}<div className="domino-cadena">{partida?.mesa?.length ? partida.mesa.map((ficha, indice) => <Ficha key={`${fichaKey(ficha)}-${indice}`} ficha={ficha} compacta mesaClase={claseMesa(indice)} />) : <span>La mesa espera la salida.</span>}</div></div>{miTurno && partida?.estado === 'jugando' && <div className="domino-controles"><button className="domino-secondary" disabled={!seleccionada || accionando} onClick={() => enviarJugada('izquierda')}>Jugar izquierda</button><button className="domino-primary" disabled={!seleccionada || accionando} onClick={() => enviarJugada('derecha')}>Jugar derecha</button><button className="domino-pass" disabled={accionando} onClick={pasar}>Pasar</button></div>}</section>
      <section className="domino-tablero"><div className="domino-mesa">{partida?.jugadores?.map(jugador => <div className={`domino-asiento ${asientoMesa(jugador.posicion, partida.mi_posicion)} ${jugador.posicion === partida.mi_posicion ? 'soy-yo ' : ''}${jugador.posicion === partida.turno ? 'turno-activo' : ''}`} key={jugador.id}><div className="domino-avatar">{jugador.nombre.slice(0, 1).toUpperCase()}</div><div><strong>{jugador.nombre}{jugador.posicion === partida.mi_posicion ? ' (tú)' : ''}</strong><span>{jugador.fichas} fichas</span></div></div>)}<div className="domino-cadena">{partida?.mesa?.length ? partida.mesa.map((ficha, indice) => <Ficha key={`${fichaKey(ficha)}-${indice}`} ficha={ficha} compacta mesaClase={claseMesa(indice)} style={{ '--pos': indice < 8 ? indice : indice < 13 ? indice - 8 : indice < 21 ? indice - 13 : indice - 21 }} />) : <span>La mesa espera la salida.</span>}</div></div>{miTurno && partida?.estado === 'jugando' && <div className="domino-controles"><button className="domino-secondary" disabled={!seleccionada || accionando} onClick={() => enviarJugada('izquierda')}>Jugar izquierda</button><button className="domino-primary" disabled={!seleccionada || accionando} onClick={() => enviarJugada('derecha')}>Jugar derecha</button><button className="domino-pass" disabled={accionando} onClick={pasar}>Pasar</button></div>}</section>
    <section className="domino-mano"><div><h2>Tus fichas</h2><span>{miTurno ? 'Selecciona una ficha' : 'Esperando turno'}</span></div><div className="domino-fichas">{partida?.mis_fichas?.map((ficha, indice) => <Ficha key={`${fichaKey(ficha)}-${indice}`} ficha={ficha} activa={seleccionada && fichaKey(seleccionada) === fichaKey(ficha)} onClick={() => miTurno && setSeleccionada(ficha)} />)}</div></section>
    <section className="domino-eventos"><h2>Últimas jugadas</h2>{partida?.eventos?.map((evento, indice) => <p key={`${evento}-${indice}`}>{evento}</p>)}</section>
  </main>
}

export default Domino