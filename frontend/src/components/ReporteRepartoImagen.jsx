import React from 'react'

const formatDate = value => new Date(`${value}T12:00:00`).toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' })
const formatPercent = value => Number(value || 0).toLocaleString('es-ES', { minimumFractionDigits: 0, maximumFractionDigits: 4 })

function ReporteRepartoImagen({ reporte, onClose }) {
  const canvasRef = React.useRef(null)

  React.useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas || !reporte) return
    const context = canvas.getContext('2d')
    const width = canvas.width
    const height = canvas.height
    const gradient = context.createLinearGradient(0, 0, width, height)
    gradient.addColorStop(0, '#07111f')
    gradient.addColorStop(1, '#17233a')
    context.fillStyle = gradient
    context.fillRect(0, 0, width, height)
    context.fillStyle = '#f6c453'
    context.fillRect(60, 76, 12, 165)
    context.fillStyle = '#f8fafc'
    context.font = '700 42px Arial'
    context.fillText('CAPITAL IBERIA', 96, 115)
    context.fillStyle = '#f6c453'
    context.font = '700 24px Arial'
    context.fillText('RENDIMIENTO ACREDITADO', 96, 153)
    context.fillStyle = '#cbd5e1'
    context.font = '400 24px Arial'
    context.fillText(formatDate(reporte.fecha), 96, 202)
    context.strokeStyle = 'rgba(246,196,83,0.45)'
    context.lineWidth = 2
    context.strokeRect(60, 290, width - 120, 300)
    context.fillStyle = '#94a3b8'
    context.font = '600 25px Arial'
    context.textAlign = 'center'
    context.fillText('PAGO DEL DÍA', width / 2, 358)
    context.fillStyle = '#f6c453'
    context.font = '700 112px Arial'
    context.fillText(`${formatPercent(reporte.porcentaje)}%`, width / 2, 485)
    context.fillStyle = '#f8fafc'
    context.font = '600 27px Arial'
    context.fillText(`ACUMULADO MENSUAL: ${formatPercent(reporte.acumulado_mensual)}%`, width / 2, 682)
    context.textAlign = 'left'
    context.fillStyle = '#f6c453'
    context.fillRect(60, 850, width - 120, 2)
    context.fillStyle = '#cbd5e1'
    context.font = '400 21px Arial'
    context.fillText('Información de rendimiento emitida por Capital Iberia.', 60, 910)
  }, [reporte])

  const descargar = () => {
    const enlace = document.createElement('a')
    enlace.download = `capital-iberia-rendimiento-${reporte.fecha}.png`
    enlace.href = canvasRef.current.toDataURL('image/png')
    enlace.click()
  }

  return <section className="payment-report-card">
    <div><h3>Imagen para WhatsApp</h3><p>Generada con el reparto confirmado y el acumulado del mes.</p></div>
    <canvas ref={canvasRef} width="900" height="1000" className="payment-report-canvas" />
    <div className="payment-report-actions"><button type="button" className="btn-action" onClick={descargar}>Descargar imagen PNG</button><button type="button" className="btn-action" onClick={onClose}>Cerrar</button></div>
  </section>
}

export default ReporteRepartoImagen