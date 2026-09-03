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
  const aportacionesPendientes = aportacionesInversor.filter(item => item.estado === 'Pendiente de validación')
  const aportacionesRechazadas = aportacionesInversor.filter(item => item.estado === 'Rechazada')
  const retirosEnRevision = retirosInversor.filter(item => !completedWithdrawalStates.has(item.estado) && item.estado !== 'Rechazado')

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
  const resumenPorMoneda = monedas.map(moneda => {
    const capitalTotal = aportacionesInversor
      .filter(item => item.moneda === moneda)
      .reduce((total, item) => total + Number(item.importe || 0), 0)
    const metaGanancia = aportacionesInversor
      .filter(item => item.moneda === moneda)
      .reduce((total, item) => total + Number(item.meta_ganancia || 0), 0)
    const gananciaTotal = aportacionesInversor
      .filter(item => item.moneda === moneda)
      .reduce((total, item) => total + Number(item.ganancia_total || 0), 0)
    return { moneda, capitalTotal, metaGanancia, gananciaTotal }
  })
  const comprobantes = aportacionesInversor.filter(item => item.tiene_justificante).length
  const actividad = [
    ...aportacionesInversor.map(item => ({ fecha: item.fecha, tipo: 'Aportación', detalle: `${formatCurrency(item.importe, item.moneda)} · ${item.estado}` })),
    ...retirosInversor.map(item => ({ fecha: item.fecha, tipo: 'Retiro', detalle: `${formatCurrency(item.importe, item.moneda)} · ${item.estado}` })),
    ...pagosInversor.map(item => ({ fecha: item.fecha || item.created_at, tipo: 'Rendimiento acreditado', detalle: formatCurrency(item.importe, item.moneda) })),
    ...mensajesInversor.map(item => ({ fecha: item.fecha, tipo: item.tipo === 'admin' ? 'Mensaje del administrador' : 'Mensaje del inversor', detalle: item.contenido || item.mensaje || 'Mensaje sin contenido' }))
  ].sort((left, right) => new Date(right.fecha || 0) - new Date(left.fecha || 0))

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

          <section className="investor-detail-section">
            <h3>Estado de cuenta</h3>
            <div className="investor-account-grid">
              <div><span>Aportaciones</span><strong>{aportacionesInversor.length}</strong></div>
              <div><span>Pendientes de validar</span><strong>{aportacionesPendientes.length}</strong></div>
              <div><span>Rechazadas</span><strong>{aportacionesRechazadas.length}</strong></div>
              <div><span>Retiros en revisión</span><strong>{retirosEnRevision.length}</strong></div>
              <div><span>Comprobantes cargados</span><strong>{comprobantes} de {aportacionesInversor.length}</strong></div>
              <div><span>Último movimiento</span><strong>{actividad.length ? formatDate(actividad[0].fecha) : 'Sin actividad'}</strong></div>
            </div>
          </section>

          {resumenPorMoneda.length > 0 && (
            <section className="investor-detail-section">
              <h3>Progreso de rendimientos</h3>
              <div className="investor-progress-grid">
                {resumenPorMoneda.map(resumen => {
                  const progreso = resumen.metaGanancia > 0 ? Math.min(100, (resumen.gananciaTotal / resumen.metaGanancia) * 100) : 0
                  return <div className="investor-progress-card" key={resumen.moneda}>
                    <div><strong>{resumen.moneda}</strong><span>{progreso.toFixed(1)}%</span></div>
                    <div className="investor-progress-track"><span style={{ width: `${progreso}%` }} /></div>
                    <p>Capital aportado: {formatCurrency(resumen.capitalTotal, resumen.moneda)}</p>
                    <p>Ganancia acumulada: {formatCurrency(resumen.gananciaTotal, resumen.moneda)}</p>
                    <p>Meta de ganancia: {formatCurrency(resumen.metaGanancia, resumen.moneda)}</p>
                  </div>
                })}
              </div>
            </section>
          )}

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
                <thead><tr><th>Fecha</th><th>Importe</th><th>Estado</th><th>Ganancia</th><th>Último pago</th><th>Documento</th></tr></thead>
                <tbody>{aportacionesInversor.length ? aportacionesInversor.map(item => (
                  <tr key={item.id}><td>{formatDate(item.fecha)}</td><td>{formatCurrency(item.importe, item.moneda)}</td><td>{item.estado}</td><td>{formatCurrency(item.ganancia_total, item.moneda)}</td><td>{formatDate(item.ultima_fecha_pago)}</td><td>{item.tiene_justificante ? 'Cargado' : 'Pendiente'}</td></tr>
                )) : <tr><td colSpan="6">No hay aportaciones registradas.</td></tr>}</tbody>
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
            <h3>Cronología completa</h3>
            <div className="investor-activity-list">
              {actividad.slice(0, 20).map((item, index) => <p key={`${item.tipo}-${item.fecha}-${index}`}><strong>{item.tipo}</strong> · {formatDate(item.fecha)} · {item.detalle}</p>)}
              {!actividad.length && <p className="investor-empty">No hay actividad registrada.</p>}
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