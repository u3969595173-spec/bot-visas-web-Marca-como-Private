import React, { useEffect, useState } from 'react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const money = (value, currency = 'USDT') => `${Number(value || 0).toLocaleString('es-ES', { maximumFractionDigits: 2 })} ${currency}`
const formatDate = (value) => value ? new Date(value).toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' }) : 'Sin fecha'

export default function FondoSolidarioPanel({ admin = false }) {
  const [data, setData] = useState(null)
  const [notice, setNotice] = useState('')
  const [loading, setLoading] = useState(true)
  const [movement, setMovement] = useState({ tipo: 'aporte_fee', importe: '', moneda: 'USDT', descripcion: '' })
  const [caseDraft, setCaseDraft] = useState({ alias_familia: '', categoria: 'Alimentos', descripcion: '', fuente: 'comunidad', importe_solicitado: '' })
  const [delivery, setDelivery] = useState({})

  const headers = () => ({ 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token') || ''}` })

  const load = async () => {
    try {
      const response = await fetch(`${API}/api/fondo-solidario`, { headers: headers() })
      if (!response.ok) throw new Error('No se pudo cargar el fondo')
      const payload = await response.json()
      setData(payload)
    } catch (error) {
      setNotice(error.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const request = async (url, method, body) => {
    const response = await fetch(`${API}${url}`, { method, headers: headers(), body: JSON.stringify(body) })
    const payload = await response.json().catch(() => ({}))
    if (!response.ok) throw new Error(payload.detail || 'No se pudo completar la operación')
    setData(payload)
    return payload
  }

  const addMovement = async (event) => {
    event.preventDefault()
    try {
      await request('/api/admin/fondo-solidario/movimientos', 'POST', { ...movement, importe: Number(movement.importe) })
      setMovement({ tipo: 'aporte_fee', importe: '', moneda: 'USDT', descripcion: '' })
      setNotice('Aporte registrado en el fondo.')
    } catch (error) { setNotice(error.message) }
  }

  const addCase = async (event) => {
    event.preventDefault()
    try {
      await request('/api/admin/fondo-solidario/casos', 'POST', { ...caseDraft, importe_solicitado: caseDraft.importe_solicitado ? Number(caseDraft.importe_solicitado) : null })
      setCaseDraft({ alias_familia: '', categoria: 'Alimentos', descripcion: '', fuente: 'comunidad', importe_solicitado: '' })
      setNotice('Caso registrado para verificación.')
    } catch (error) { setNotice(error.message) }
  }

  const updateCase = async (caseItem, state) => {
    try {
      await request(`/api/admin/fondo-solidario/casos/${caseItem.id}`, 'PUT', { estado: state, visible: state !== 'recibido' && state !== 'descartado' })
      setNotice('Estado del caso actualizado.')
    } catch (error) { setNotice(error.message) }
  }

  const loadEvidence = (caseId, file) => {
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => setDelivery(previous => ({ ...previous, [caseId]: { ...(previous[caseId] || {}), evidencia: reader.result } }))
    reader.readAsDataURL(file)
  }

  const completeDelivery = async (event, caseItem) => {
    event.preventDefault()
    const draft = delivery[caseItem.id] || {}
    try {
      await request(`/api/admin/fondo-solidario/casos/${caseItem.id}/entrega`, 'POST', {
        importe: Number(draft.importe), moneda: draft.moneda || 'USDT', responsable_entrega: draft.responsable_entrega,
        resumen_entrega: draft.resumen_entrega, evidencia: draft.evidencia || null,
      })
      setDelivery(previous => ({ ...previous, [caseItem.id]: {} }))
      setNotice('Entrega registrada y publicada en la vista de transparencia.')
    } catch (error) { setNotice(error.message) }
  }

  if (loading) return <p style={{ color: '#94a3b8' }}>Cargando Fondo Solidario...</p>
  if (!data) return <p style={{ color: '#fca5a5' }}>{notice || 'No se pudo cargar el Fondo Solidario.'}</p>

  const card = { background: 'rgba(15,23,42,0.72)', border: '1px solid rgba(148,163,184,0.2)', borderRadius: 8, padding: '1.25rem' }
  const input = { width: '100%', boxSizing: 'border-box', padding: '9px 10px', borderRadius: 6, border: '1px solid #334155', background: '#07111f', color: '#f8fafc' }
  const button = { padding: '9px 12px', border: 'none', borderRadius: 6, background: '#0891b2', color: 'white', fontWeight: 700, cursor: 'pointer' }

  return <section style={{ display: 'grid', gap: '1.25rem' }}>
    <div style={{ ...card, borderLeft: '4px solid #22c55e' }}>
      <h2 style={{ margin: 0, color: '#f8fafc' }}>Fondo Solidario Cuba</h2>
      <p style={{ margin: '0.55rem 0 0', color: '#cbd5e1', lineHeight: 1.55 }}>
        Una hucha separada del capital de inversión. De cada fee de retiro del 5%, el 2% se destina al Fondo Solidario y el 3% restante cubre el procesamiento operativo. La empresa realiza aportes obligatorios adicionales; estos se reflejan por separado para que la comunidad vea su contribución real.
      </p>
    </div>

    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
      {[['Saldo disponible', money(data.saldo), '#22c55e'], ['Del 2% de fees', money(data.aportado_fees), '#38bdf8'], ['Aporte obligatorio empresa', money(data.aportado_empresa), '#c084fc'], ['Ayuda entregada', money(data.entregado), '#f6c453'], ['Regla del fee', '2% del retiro', '#94a3b8']].map(([label, value, color]) => <div key={label} style={card}>
        <div style={{ color: '#94a3b8', fontSize: 12 }}>{label}</div><strong style={{ display: 'block', color, fontSize: 22, marginTop: 6 }}>{value}</strong>
      </div>)}
    </div>

    {!admin && <div style={card}>
      <h3 style={{ marginTop: 0, color: '#f8fafc' }}>Que es este Fondo</h3>
      <p style={{ color: '#cbd5e1', lineHeight: 1.55, margin: 0 }}>El Fondo Solidario reúne el 2% del fee de cada retiro y los aportes obligatorios adicionales de la empresa. El panel muestra ambas cifras por separado para que la comunidad pueda comprobar cuánto llega desde cada origen. Ese dinero no procede de las inversiones ni reduce los saldos de los usuarios: se reserva exclusivamente para ayudas verificadas a familias vulnerables en Cuba.</p>
      <p style={{ color: '#cbd5e1', lineHeight: 1.55, margin: '0.8rem 0 0' }}>Los casos se proponen mediante el chat de Comunidad o por soporte. La administración comprueba la información antes de seleccionar y publicar un caso. La entrega puede realizarla un equipo o representante de la propia comunidad; después se registra el importe usado, qué se entregó y evidencia autorizada. La web conserva ese registro para comprobar que el dinero del fondo se destinó a la ayuda anunciada, sin publicar datos sensibles de las familias.</p>
    </div>}

    {admin && <>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
        <div style={card}><h3 style={{ marginTop: 0, color: '#f8fafc' }}>Regla fija de aportación</h3><p style={{ color: '#cbd5e1', lineHeight: 1.55, marginBottom: 0 }}>Cada retiro tiene un fee total del 5%. De ese cargo, el 2% va al Fondo Solidario y el 3% restante se utiliza para costes de procesamiento, comisiones bancarias y de red. Esta regla no se puede modificar desde el panel.</p></div>
        <form onSubmit={addMovement} style={card}><h3 style={{ marginTop: 0, color: '#f8fafc' }}>Registrar aporte</h3><div style={{ display: 'grid', gap: 8 }}><select value={movement.tipo} onChange={event => setMovement({ ...movement, tipo: event.target.value })} style={input}><option value="aporte_fee">2% acumulado de fees de retiro</option><option value="aporte_empresa">Aporte de la empresa</option></select><input required type="number" min="0.01" step="0.01" placeholder="Importe" value={movement.importe} onChange={event => setMovement({ ...movement, importe: event.target.value })} style={input} /><input required placeholder="Origen o referencia" value={movement.descripcion} onChange={event => setMovement({ ...movement, descripcion: event.target.value })} style={input} /><button style={button}>Registrar aporte</button></div></form>
      </div>
      <form onSubmit={addCase} style={card}><h3 style={{ marginTop: 0, color: '#f8fafc' }}>Registrar caso propuesto</h3><div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 8 }}><input required placeholder="Alias de la familia" value={caseDraft.alias_familia} onChange={event => setCaseDraft({ ...caseDraft, alias_familia: event.target.value })} style={input} /><input required placeholder="Categoría" value={caseDraft.categoria} onChange={event => setCaseDraft({ ...caseDraft, categoria: event.target.value })} style={input} /><input type="number" min="0" step="0.01" placeholder="Importe estimado" value={caseDraft.importe_solicitado} onChange={event => setCaseDraft({ ...caseDraft, importe_solicitado: event.target.value })} style={input} /><select value={caseDraft.fuente} onChange={event => setCaseDraft({ ...caseDraft, fuente: event.target.value })} style={input}><option value="comunidad">Comunidad</option><option value="soporte">Soporte</option></select></div><textarea required rows="3" placeholder="Necesidad verificada, sin datos personales sensibles" value={caseDraft.descripcion} onChange={event => setCaseDraft({ ...caseDraft, descripcion: event.target.value })} style={{ ...input, marginTop: 8, resize: 'vertical' }} /><button style={{ ...button, marginTop: 8 }}>Guardar para verificación</button></form>
    </>}

    {notice && <p style={{ margin: 0, color: '#f6c453' }}>{notice}</p>}
    <div style={{ display: 'grid', gap: '1rem' }}><h3 style={{ margin: 0, color: '#f8fafc' }}>{admin ? 'Casos y entregas' : 'Casos seleccionados y entregas verificadas'}</h3>
      {data.casos.length === 0 && <p style={{ color: '#94a3b8' }}>Todavía no hay casos publicados.</p>}
      {data.casos.map(caseItem => <article key={caseItem.id} style={card}><div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}><div><strong style={{ color: '#f8fafc' }}>{caseItem.alias_familia}</strong><span style={{ color: '#94a3b8', marginLeft: 8 }}>{caseItem.categoria}</span></div><span style={{ color: '#38bdf8', fontSize: 13 }}>{caseItem.estado}</span></div><p style={{ color: '#cbd5e1', marginBottom: 8 }}>{caseItem.descripcion}</p>{caseItem.importe_solicitado && <small style={{ color: '#94a3b8' }}>Necesidad estimada: {money(caseItem.importe_solicitado)}</small>}{caseItem.estado === 'entregado' && <div style={{ marginTop: 10, borderTop: '1px solid #334155', paddingTop: 10 }}><strong style={{ color: '#22c55e' }}>Entrega: {money(caseItem.importe_entregado)}</strong><p style={{ color: '#cbd5e1', margin: '6px 0' }}>{caseItem.resumen_entrega}</p><small style={{ color: '#94a3b8' }}>Realizada por: {caseItem.responsable_entrega} · {formatDate(caseItem.updated_at)}</small>{caseItem.evidencia && <img src={caseItem.evidencia} alt="Evidencia autorizada de entrega" style={{ display: 'block', maxWidth: 260, maxHeight: 180, objectFit: 'cover', marginTop: 10, borderRadius: 6 }} />}</div>}
        {admin && <><div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 12 }}><button type="button" style={button} onClick={() => updateCase(caseItem, 'verificado')}>Verificar</button><button type="button" style={{ ...button, background: '#7c3aed' }} onClick={() => updateCase(caseItem, 'seleccionado')}>Seleccionar</button><button type="button" style={{ ...button, background: '#b91c1c' }} onClick={() => updateCase(caseItem, 'descartado')}>Descartar</button></div>{caseItem.estado === 'seleccionado' && <form onSubmit={event => completeDelivery(event, caseItem)} style={{ display: 'grid', gap: 8, marginTop: 12, paddingTop: 12, borderTop: '1px solid #334155' }}><strong style={{ color: '#f8fafc' }}>Registrar entrega comunitaria</strong><input required type="number" min="0.01" step="0.01" placeholder="Importe entregado" value={delivery[caseItem.id]?.importe || ''} onChange={event => setDelivery({ ...delivery, [caseItem.id]: { ...(delivery[caseItem.id] || {}), importe: event.target.value } })} style={input} /><input required placeholder="Responsable o equipo de comunidad" value={delivery[caseItem.id]?.responsable_entrega || ''} onChange={event => setDelivery({ ...delivery, [caseItem.id]: { ...(delivery[caseItem.id] || {}), responsable_entrega: event.target.value } })} style={input} /><textarea required rows="2" placeholder="Qué se entregó y confirmación de la ayuda" value={delivery[caseItem.id]?.resumen_entrega || ''} onChange={event => setDelivery({ ...delivery, [caseItem.id]: { ...(delivery[caseItem.id] || {}), resumen_entrega: event.target.value } })} style={input} /><input type="file" accept="image/*" onChange={event => loadEvidence(caseItem.id, event.target.files?.[0])} style={{ color: '#cbd5e1' }} /><button style={{ ...button, background: '#16a34a' }}>Publicar entrega verificada</button></form>}</>}</article>)}
    </div>
  </section>
}