import React from 'react'
import { createPortal } from 'react-dom'

const formatCurrency = (value, currency) => {
  const amount = Number(value || 0)
  return `${amount.toLocaleString('es-ES', { maximumFractionDigits: 2 })} ${currency || 'EUR'}`
}

const formatDate = (value) => {
  if (!value) return 'Sin fecha'
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString('es-ES', { dateStyle: 'medium', timeStyle: 'short' })
}

const activeStates = new Set(['Activa', 'Aprobada', 'Validada'])
const completedWithdrawalStates = new Set(['Aprobado', 'Completado', 'Procesado'])

function FichaInversorAdmin({ inversor, aportaciones, retiros, pagos, mensajes, referidos, onClose, onInjectBalance, onViewCommunity }) {
  const aportacionesInversor = aportaciones.filter(item => Number(item.inversor_id) === Number(inversor.id))
  const retirosInversor = retiros.filter(item => Number(item.inversor_id) === Number(inversor.id))
  const pagosInversor = pagos.filter(item => Number(item.inversor_id) === Number(inversor.id))
  const mensajesInversor = mensajes.filter(item => Number(item.usuarioId) === Number(inversor.id))
  const referidosDirectos = referidos.filter(item => item.referidoPor === inversor.codigo_referido)

  const cartera = aportacionesInversor.reduce((totales, item) => {
    if (!activeStates.has(item.estado)) return totales
    const moneda = item.moneda || 'EUR'
    totales[moneda] = (totales[moneda] || 0) + Number(item.importe || 0)
    return totales
  }, {})

  const retirado = retirosInversor.reduce((totales, item) => {
    if (!completedWithdrawalStates.has(item.estado)) return totales
    const moneda = item.moneda || 'EUR'
    totales[moneda] = (totales[moneda] || 0) + Number(item.importe || 0)
    return totales
  }, {})

  const acreditado = pagosInversor.reduce((totales, item) => {
    const moneda = item.moneda || 'EUR'
    totales[moneda] = (totales[moneda] || 0) + Number(item.importe || 0)
    return totales
  }, {})

  const monedas = [...new Set([...Object.keys(cartera), ...Object.keys(retirado), ...Object.keys(acreditado)])]

  return createPortal(
    <div className="investor-detail-backdrop" role="presentation" onMouseDown={onClose}>
      <section className="investor-detail-panel" role="dialog" aria-modal="true" aria-labelledby="investor-detail-title" onMouseDown={event => event.stopPropagation()}>
        <header className="investor-detail-header">
          <div>
            <p className="investor-detail-eyebrow">Vista administrativa 360</p>
            <h2 id="investor-detail-title">{inversor.nombre || 'Inversor'}</h2>
            <p>{inversor.email || 'Sin correo'} · {inversor.estado || 'Activa'}</p>
          </div>
          <button type="button" className="investor-detail-close" aria-label="Cerrar ficha del inversor" onClick={onClose}>Cerrar</button>
        </header>

        <div className="investor-detail-body">
          <section className="investor-detail-section">
            <h3>Cartera</h3>
            {monedas.length ? (
              <div className="investor-wallet-grid">
                {monedas.map(moneda => (
                  <div className="investor-wallet-card" key={moneda}>
                    <span>{moneda}</span>
                    <strong>{formatCurrency(cartera[moneda], moneda)}</strong>
                    <small>Capital activo</small>
                    <div>Retirado: {formatCurrency(retirado[moneda], moneda)}</div>
                    <div>Acreditado: {formatCurrency(acreditado[moneda], moneda)}</div>
                  </div>
                ))}
              </div>
            ) : <p className="investor-empty">No tiene movimientos financieros registrados.</p>}
          </section>

          <section className="investor-detail-section investor-detail-data-grid">
            <div><span>Teléfono</span><strong>{inversor.telefono || 'Sin registrar'}</strong></div>
            <div><span>País</span><strong>{inversor.pais || 'Sin registrar'}</strong></div>
            <div><span>Registro</span><strong>{formatDate(inversor.created_at)}</strong></div>
            <div><span>Código</span><strong>{inversor.codigo_referido || 'Sin código'}</strong></div>
            <div><span>Patrocinador</span><strong>{inversor.referido_por || 'Sin patrocinador'}</strong></div>
            <div><span>Comunidad</span><strong>{referidosDirectos.length} referidos directos</strong></div>
          </section>

          <section className="investor-detail-section">
            <h3>Aportaciones</h3>
            <div className="investor-detail-table-wrap">
              <table className="investor-detail-table">
                <thead><tr><th>Fecha</th><th>Importe</th><th>Estado</th><th>Ganancia</th></tr></thead>
                <tbody>{aportacionesInversor.length ? aportacionesInversor.map(item => (
                  <tr key={item.id}><td>{formatDate(item.fecha)}</td><td>{formatCurrency(item.importe, item.moneda)}</td><td>{item.estado}</td><td>{formatCurrency(item.ganancia_total, item.moneda)}</td></tr>
                )) : <tr><td colSpan="4">No hay aportaciones registradas.</td></tr>}</tbody>
              </table>
            </div>
          </section>

          <section className="investor-detail-section">
            <h3>Retiros</h3>
            <div className="investor-detail-table-wrap">
              <table className="investor-detail-table">
                <thead><tr><th>Fecha</th><th>Importe</th><th>Estado</th><th>Detalle</th></tr></thead>
                <tbody>{retirosInversor.length ? retirosInversor.map(item => (
                  <tr key={item.id}><td>{formatDate(item.fecha)}</td><td>{formatCurrency(item.importe, item.moneda)}</td><td>{item.estado}</td><td>{item.detalles || '—'}</td></tr>
                )) : <tr><td colSpan="4">No hay retiros registrados.</td></tr>}</tbody>
              </table>
            </div>
          </section>

          <section className="investor-detail-section">
            <h3>Actividad reciente</h3>
            <div className="investor-activity-list">
              {mensajesInversor.slice(0, 5).map(item => <p key={item.id}>{formatDate(item.fecha)} · {item.contenido || item.mensaje || 'Mensaje sin contenido'}</p>)}
              {!mensajesInversor.length && <p className="investor-empty">No hay mensajes registrados.</p>}
            </div>
          </section>
        </div>

        <footer className="investor-detail-actions">
          <button type="button" className="btn-action" onClick={() => onInjectBalance(inversor.id, inversor.nombre || 'Inversor')}>Inyectar saldo</button>
          {inversor.es_lider && <button type="button" className="btn-action" onClick={() => onViewCommunity(inversor.id, inversor.nombre || 'Inversor')}>Ver comunidad</button>}
        </footer>
      </section>
    </div>
  , document.body)
}

export default FichaInversorAdmin