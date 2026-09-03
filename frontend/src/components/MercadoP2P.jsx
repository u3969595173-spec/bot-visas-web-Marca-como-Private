import React from 'react'
import { useNavigate } from 'react-router-dom'
import './MercadoP2P.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const initialForm = { tipo: 'Venta', titulo: '', categoria: 'Otros', cantidad: '', precio: '', moneda: '', descripcion: '', telefono: '' }

function MercadoP2P() {
  const navigate = useNavigate()
  const [anuncios, setAnuncios] = React.useState([])
  const [filtro, setFiltro] = React.useState('Todos')
  const [mostrarFormulario, setMostrarFormulario] = React.useState(false)
  const [formulario, setFormulario] = React.useState(initialForm)
  const [cargando, setCargando] = React.useState(true)
  const [error, setError] = React.useState('')
  const [publicando, setPublicando] = React.useState(false)
  const user = React.useMemo(() => { try { return JSON.parse(localStorage.getItem('capital_trade_user') || 'null') } catch { return null } }, [])
  const token = localStorage.getItem('token')

  const cargarAnuncios = React.useCallback(async () => {
    if (!token) { navigate('/login'); return }
    try {
      const response = await fetch(`${API}/api/mercado/anuncios`, { headers: { Authorization: `Bearer ${token}` } })
      if (response.status === 401) { navigate('/login'); return }
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'No se pudo cargar el mercado.')
      setAnuncios(data.anuncios || [])
    } catch (requestError) { setError(requestError.message || 'No se pudo cargar el mercado.') }
    finally { setCargando(false) }
  }, [navigate, token])

  React.useEffect(() => { cargarAnuncios() }, [cargarAnuncios])

  const publicar = async event => {
    event.preventDefault()
    setPublicando(true); setError('')
    try {
      const response = await fetch(`${API}/api/mercado/anuncios`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }, body: JSON.stringify(formulario) })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'No se pudo publicar el anuncio.')
      setFormulario(initialForm); setMostrarFormulario(false); await cargarAnuncios()
    } catch (requestError) { setError(requestError.message || 'No se pudo publicar el anuncio.') }
    finally { setPublicando(false) }
  }

  const cambiarEstado = async (id, estado) => {
    const response = await fetch(`${API}/api/mercado/anuncios/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }, body: JSON.stringify({ estado }) })
    if (response.ok) cargarAnuncios(); else setError('No se pudo actualizar el anuncio.')
  }

  const contactar = anuncio => {
    const telefono = String(anuncio.telefono || '').replace(/\D/g, '')
    const mensaje = `Hola ${anuncio.nombre}, vi tu anuncio en el Mercado Capital Iberia: ${anuncio.tipo} ${anuncio.titulo}. Precio fijo: ${anuncio.precio}${anuncio.moneda ? ` ${anuncio.moneda}` : ''}. Me interesa hablar contigo.`
    window.open(`https://wa.me/${telefono}?text=${encodeURIComponent(mensaje)}`, '_blank', 'noopener,noreferrer')
  }

  const visibles = anuncios.filter(anuncio => filtro === 'Todos' || anuncio.tipo === filtro)
  return <main className="market-page">
    <header className="market-header"><div><p>Mercado entre usuarios</p><h1>Compra y venta directa</h1><span>Publica lo que quieras vender o comprar a un precio fijo.</span></div><button className="market-primary" onClick={() => setMostrarFormulario(!mostrarFormulario)}>{mostrarFormulario ? 'Cerrar' : 'Publicar anuncio'}</button></header>
    <p className="market-notice">Capital Iberia facilita el contacto entre usuarios. La negociación, entrega y pago se acuerdan directamente entre las partes.</p>
    {error && <p className="market-error">{error}</p>}
    {mostrarFormulario && <form className="market-form" onSubmit={publicar}><h2>Nuevo anuncio</h2><div className="market-form-grid">
      <label>Quiero<select value={formulario.tipo} onChange={event => setFormulario({ ...formulario, tipo: event.target.value })}><option>Venta</option><option>Compra</option></select></label>
      <label>Producto o activo *<input value={formulario.titulo} onChange={event => setFormulario({ ...formulario, titulo: event.target.value })} placeholder="Ej.: Chaqueta, USDT, móvil..." maxLength="160" required /></label>
      <label>Categoría<select value={formulario.categoria} onChange={event => setFormulario({ ...formulario, categoria: event.target.value })}><option>Otros</option><option>Ropa y accesorios</option><option>Criptoactivos</option><option>Moneda</option><option>Electrónica</option><option>Hogar</option><option>Servicios</option></select></label>
      <label>Cantidad<input value={formulario.cantidad} onChange={event => setFormulario({ ...formulario, cantidad: event.target.value })} placeholder="Ej.: 2 unidades, 100 USDT" maxLength="100" /></label>
      <label>Precio fijo *<input value={formulario.precio} onChange={event => setFormulario({ ...formulario, precio: event.target.value })} placeholder="Ej.: 50" maxLength="100" required /></label>
      <label>Moneda de pago<input value={formulario.moneda} onChange={event => setFormulario({ ...formulario, moneda: event.target.value })} placeholder="Ej.: EUR, USD, CUP" maxLength="50" /></label>
      <label className="market-form-wide">Número de WhatsApp *<input type="tel" value={formulario.telefono} onChange={event => setFormulario({ ...formulario, telefono: event.target.value })} placeholder="Ej.: +34 600 000 000" maxLength="40" required /></label>
      <label className="market-form-wide">Descripción<textarea value={formulario.descripcion} onChange={event => setFormulario({ ...formulario, descripcion: event.target.value })} placeholder="Estado, detalles y condiciones del producto." maxLength="1000" rows="3" /></label>
    </div><button className="market-primary" disabled={publicando}>{publicando ? 'Publicando...' : 'Publicar anuncio'}</button></form>}
    <div className="market-filters">{['Todos', 'Venta', 'Compra'].map(item => <button key={item} onClick={() => setFiltro(item)} className={filtro === item ? 'active' : ''}>{item}</button>)}</div>
    {cargando ? <p className="market-empty">Cargando anuncios...</p> : <section className="market-grid">{visibles.map(anuncio => {
      const esMio = Number(anuncio.inversor_id) === Number(user?.id)
      return <article className={`market-card ${anuncio.tipo === 'Compra' ? 'market-buy' : 'market-sell'}`} key={anuncio.id}><div className="market-card-top"><span>{anuncio.tipo}</span><small>{anuncio.estado}</small></div><p className="market-category">{anuncio.categoria}</p><h2>{anuncio.titulo}</h2>{anuncio.cantidad && <p>Cantidad: <strong>{anuncio.cantidad}</strong></p>}<div className="market-price">{anuncio.precio} {anuncio.moneda}</div>{anuncio.descripcion && <p className="market-description">{anuncio.descripcion}</p>}<p className="market-owner">Publicado por {esMio ? 'ti' : anuncio.nombre}</p>{esMio ? <div className="market-owner-actions"><button onClick={() => cambiarEstado(anuncio.id, anuncio.estado === 'Activa' ? 'Pausada' : 'Activa')}>{anuncio.estado === 'Activa' ? 'Pausar' : 'Activar'}</button><button onClick={() => cambiarEstado(anuncio.id, 'Cerrada')}>Cerrar venta</button></div> : anuncio.estado === 'Activa' && <button className="market-whatsapp" onClick={() => contactar(anuncio)}>Hablar por WhatsApp</button>}</article>
    })}</section>}
    {!cargando && !visibles.length && <p className="market-empty">No hay anuncios para este filtro todavía.</p>}
  </main>
}

export default MercadoP2P