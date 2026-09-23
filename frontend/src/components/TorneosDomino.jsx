import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './Domino.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function TorneosDomino({ admin = false }) {
  const navigate = useNavigate()
  const token = localStorage.getItem('token')
  const [torneos, setTorneos] = React.useState([])
  const [seleccionado, setSeleccionado] = React.useState(null)
  const [codigoPareja, setCodigoPareja] = React.useState('')
  const [formulario, setFormulario] = React.useState({ nombre: '', max_parejas: 30, premio_primero: 0, premio_segundo: 0, premio_tercero: 0 })
  const [error, setError] = React.useState('')
  const [ocupado, setOcupado] = React.useState(false)
  const headers = { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }

  const request = async (url, options = {}) => {
    const respuesta = await fetch(`${API}${url}`, { ...options, headers: { ...headers, ...(options.headers || {}) } })
    const datos = await respuesta.json()
    if (!respuesta.ok) throw new Error(datos.detail || 'No se pudo completar la acción.')
    return datos
  }

  const cargar = async () => {
    try {
      const datos = await request('/api/domino/torneos')
      setTorneos(datos.torneos || [])
    } catch (requestError) { setError(requestError.message) }
  }

  const cargarDetalle = async torneoId => {
    try {
      const datos = await request(`/api/domino/torneos/${torneoId}`)
      setSeleccionado(datos); setError('')
    } catch (requestError) { setError(requestError.message) }
  }

  React.useEffect(() => {
    if (!token) { navigate('/login'); return }
    cargar()
  }, [])

  React.useEffect(() => {
    if (!seleccionado) return undefined
    const intervalo = setInterval(() => cargarDetalle(seleccionado.id), 6000)
    return () => clearInterval(intervalo)
  }, [seleccionado?.id])

  const crearTorneo = async evento => {
    evento.preventDefault(); setOcupado(true); setError('')
    try {
      const datos = await request('/api/admin/domino/torneos', { method: 'POST', body: JSON.stringify({ ...formulario, max_parejas: Number(formulario.max_parejas), premio_primero: Number(formulario.premio_primero), premio_segundo: Number(formulario.premio_segundo), premio_tercero: Number(formulario.premio_tercero) }) })
      await cargar(); await cargarDetalle(datos.id)
    } catch (requestError) { setError(requestError.message) } finally { setOcupado(false) }
  }

  const crearPareja = async () => {
    setOcupado(true); setError('')
    try { const datos = await request(`/api/domino/torneos/${seleccionado.id}/parejas`, { method: 'POST', body: '{}' }); setCodigoPareja(datos.codigo); await cargarDetalle(seleccionado.id) } catch (requestError) { setError(requestError.message) } finally { setOcupado(false) }
  }

  const unirsePareja = async evento => {
    evento.preventDefault(); setOcupado(true); setError('')
    try { await request(`/api/domino/torneos/${seleccionado.id}/parejas/unirse`, { method: 'POST', body: JSON.stringify({ codigo: codigoPareja }) }); setCodigoPareja(''); await cargarDetalle(seleccionado.id) } catch (requestError) { setError(requestError.message) } finally { setOcupado(false) }
  }

  const aprobar = async parejaId => {
    setOcupado(true); setError('')
    try { await request(`/api/admin/domino/torneos/${seleccionado.id}/parejas/${parejaId}/aprobar`, { method: 'POST', body: '{}' }); await cargarDetalle(seleccionado.id); await cargar() } catch (requestError) { setError(requestError.message) } finally { setOcupado(false) }
  }

  const siguienteRonda = async () => {
    setOcupado(true); setError('')
    try { await request(`/api/admin/domino/torneos/${seleccionado.id}/siguiente-ronda`, { method: 'POST', body: '{}' }); await cargarDetalle(seleccionado.id); await cargar() } catch (requestError) { setError(requestError.message) } finally { setOcupado(false) }
  }

  if (!seleccionado) return <main className="domino-page">
    <header className="domino-header"><div><p className="domino-eyebrow">Dominó suizo</p><h1>{admin ? 'Administrar torneos' : 'Torneos'}</h1><span>10 rondas suizas, top 8 y fase final.</span></div><Link to={admin ? '/admin' : '/dashboard'} className="domino-link">Volver</Link></header>
    {error && <p className="domino-error">{error}</p>}
    {admin && <form className="domino-lobby-action domino-torneo-form" onSubmit={crearTorneo}><h2>Crear torneo</h2><div className="domino-torneo-fields"><input required placeholder="Nombre del torneo" value={formulario.nombre} onChange={evento => setFormulario({ ...formulario, nombre: evento.target.value })} /><input type="number" min="4" max="30" step="2" value={formulario.max_parejas} onChange={evento => setFormulario({ ...formulario, max_parejas: evento.target.value })} /><input type="number" min="0" placeholder="Premio 1.º" value={formulario.premio_primero} onChange={evento => setFormulario({ ...formulario, premio_primero: evento.target.value })} /><input type="number" min="0" placeholder="Premio 2.º" value={formulario.premio_segundo} onChange={evento => setFormulario({ ...formulario, premio_segundo: evento.target.value })} /><input type="number" min="0" placeholder="Premio 3.º" value={formulario.premio_tercero} onChange={evento => setFormulario({ ...formulario, premio_tercero: evento.target.value })} /></div><button className="domino-primary" disabled={ocupado}>Crear torneo</button></form>}
    <section className="domino-salas"><div className="domino-section-title"><h2>Torneos</h2><button onClick={cargar}>Actualizar</button></div>{torneos.length ? <div className="domino-salas-grid">{torneos.map(torneo => <article key={torneo.id}><strong>{torneo.nombre}</strong><span>{torneo.parejas_aprobadas}/{torneo.max_parejas} parejas</span><small>{torneo.estado}</small><button onClick={() => cargarDetalle(torneo.id)}>Ver torneo</button></article>)}</div> : <p className="domino-empty">No hay torneos creados.</p>}</section>
  </main>

  const mesaPropia = seleccionado.mesas.find(mesa => mesa.estado === 'jugando' && seleccionado.mi_pareja && (mesa.pareja_a.includes(seleccionado.ranking.find(pareja => pareja.id === seleccionado.mi_pareja.id)?.jugador_uno || '') || mesa.pareja_b.includes(seleccionado.ranking.find(pareja => pareja.id === seleccionado.mi_pareja.id)?.jugador_uno || '')))
  return <main className="domino-page">
    <header className="domino-header"><div><p className="domino-eyebrow">Torneo</p><h1>{seleccionado.nombre}</h1><span>{seleccionado.estado} · {seleccionado.rondas_suizas} rondas suizas</span></div><button className="domino-link" onClick={() => { setSeleccionado(null); cargar() }}>Torneos</button></header>
    {error && <p className="domino-error">{error}</p>}
    {!admin && seleccionado.estado === 'inscripcion' && <section className="domino-lobby"><div className="domino-lobby-action"><h2>Inscribir pareja</h2>{seleccionado.mi_pareja ? <p>Tu código de pareja: <strong>{seleccionado.mi_pareja.codigo}</strong></p> : <button className="domino-primary" onClick={crearPareja} disabled={ocupado}>Crear código de pareja</button>}</div><form className="domino-lobby-action" onSubmit={unirsePareja}><h2>Unirse a una pareja</h2><div className="domino-code-row"><input value={codigoPareja} maxLength="8" placeholder="Código de pareja" onChange={evento => setCodigoPareja(evento.target.value)} /><button className="domino-secondary" disabled={ocupado}>Unirse</button></div></form></section>}
    {admin && <section className="domino-ubicacion"><span>Aprueba las parejas completas y genera la siguiente ronda cuando todas las mesas finalicen.</span><button className="domino-primary" onClick={siguienteRonda} disabled={ocupado}>Generar siguiente ronda</button></section>}
    {mesaPropia && <section className="domino-ubicacion verificada"><span>Tu mesa está lista.</span><Link className="domino-secondary" to={`/domino?mesa=${mesaPropia.codigo}`}>Abrir mesa</Link></section>}
    {admin && <section className="domino-salas"><h2>Parejas inscritas</h2><div className="domino-ranking">{seleccionado.parejas.map(pareja => <div key={pareja.id}><strong>#{pareja.id}</strong><span>{pareja.jugador_uno} y {pareja.jugador_dos || 'esperando compañero'}</span><small>{pareja.estado}</small>{pareja.estado !== 'aprobada' && pareja.jugador_dos && <button onClick={() => aprobar(pareja.id)} disabled={ocupado}>Aprobar</button>}</div>)}</div></section>}
    <section className="domino-salas"><h2>Ranking</h2><div className="domino-ranking">{seleccionado.ranking.map(pareja => <div key={pareja.id}><strong>{pareja.posicion}</strong><span>{pareja.jugador_uno} y {pareja.jugador_dos || 'pendiente'}</span><small>{pareja.victorias}V · {pareja.derrotas}D · {pareja.diferencia >= 0 ? '+' : ''}{pareja.diferencia}</small></div>)}</div></section>
    <section className="domino-salas"><h2>Mesas</h2>{seleccionado.mesas.length ? <div className="domino-ranking">{seleccionado.mesas.map(mesa => <div key={mesa.id}><strong>{mesa.fase} {mesa.ronda}</strong><span>{mesa.pareja_a} vs {mesa.pareja_b}</span><small>{mesa.estado}</small></div>)}</div> : <p className="domino-empty">Las mesas aparecerán al iniciar la primera ronda.</p>}</section>
  </main>
}

export default TorneosDomino