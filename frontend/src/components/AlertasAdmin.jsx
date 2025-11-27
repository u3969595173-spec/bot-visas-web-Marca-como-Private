import React, { useState, useEffect } from 'react'
import axios from 'axios'

const AlertasAdmin = ({ apiUrl }) => {
  const [fechasProximas, setFechasProximas] = useState([])
  const [loading, setLoading] = useState(true)
  const [diasFiltro, setDiasFiltro] = useState(30)
  const [tipoFiltro, setTipoFiltro] = useState('todos')

  const tiposFecha = {
    entrevista_consular: { nombre: 'Entrevista Consular', emoji: '🎤', color: '#dc3545' },
    vencimiento_pasaporte: { nombre: 'Vencimiento de Pasaporte', emoji: '📘', color: '#ffc107' },
    vencimiento_documento: { nombre: 'Vencimiento de Documento', emoji: '📄', color: '#ffc107' },
    deadline_aplicacion: { nombre: 'Fecha Límite de Aplicación', emoji: '⏰', color: '#fd7e14' },
    cita_visa: { nombre: 'Cita para Visa', emoji: '📅', color: '#dc3545' },
    inicio_clases: { nombre: 'Inicio de Clases', emoji: '🎓', color: '#28a745' },
    pago_matricula: { nombre: 'Pago de Matrícula', emoji: '💵', color: '#17a2b8' },
    renovacion_visa: { nombre: 'Renovación de Visa', emoji: '🔄', color: '#6c757d' },
    entrega_documentos: { nombre: 'Entrega de Documentos', emoji: '📋', color: '#007bff' },
    otro: { nombre: 'Otro', emoji: '📌', color: '#6c757d' }
  }

  useEffect(() => {
    cargarFechasProximas()
  }, [diasFiltro])

  const cargarFechasProximas = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${apiUrl}/api/alertas/proximas?dias=${diasFiltro}`)
      if (response.data.success) {
        setFechasProximas(response.data.fechas_proximas)
      }
    } catch (error) {
      console.error('Error cargando fechas próximas:', error)
    } finally {
      setLoading(false)
    }
  }

  const getUrgencia = (diasRestantes) => {
    if (diasRestantes <= 1) return { nivel: 'critico', color: '#dc3545', texto: '¡URGENTE!' }
    if (diasRestantes <= 7) return { nivel: 'alto', color: '#ffc107', texto: 'Próxima' }
    if (diasRestantes <= 15) return { nivel: 'medio', color: '#17a2b8', texto: 'Pronto' }
    return { nivel: 'bajo', color: '#28a745', texto: 'Planificada' }
  }

  const formatearFecha = (fechaISO) => {
    const fecha = new Date(fechaISO)
    return fecha.toLocaleDateString('es-ES', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const fechasFiltradas = tipoFiltro === 'todos' 
    ? fechasProximas 
    : fechasProximas.filter(f => f.tipo_fecha === tipoFiltro)

  if (loading) {
    return <div style={{padding: '40px', textAlign: 'center'}}><p>Cargando alertas...</p></div>
  }

  return (
    <div style={{padding: '20px'}}>
      <div style={{marginBottom: '30px'}}>
        <h2 style={{fontSize: '28px', marginBottom: '10px'}}>📅 Alertas de Fechas Importantes</h2>
        <p style={{color: '#718096', marginBottom: '20px'}}>
          Monitorea todas las fechas críticas de tus estudiantes
        </p>

        {/* Filtros */}
        <div style={{display: 'flex', gap: '16px', marginBottom: '24px', flexWrap: 'wrap'}}>
          <div>
            <label style={{fontSize: '14px', fontWeight: '600', marginBottom: '8px', display: 'block'}}>
              Período:
            </label>
            <select 
              value={diasFiltro} 
              onChange={(e) => setDiasFiltro(parseInt(e.target.value))}
              style={{padding: '10px', borderRadius: '6px', border: '2px solid #e2e8f0'}}
            >
              <option value={7}>Próximos 7 días</option>
              <option value={15}>Próximos 15 días</option>
              <option value={30}>Próximos 30 días</option>
              <option value={60}>Próximos 60 días</option>
            </select>
          </div>
          
          <div>
            <label style={{fontSize: '14px', fontWeight: '600', marginBottom: '8px', display: 'block'}}>
              Tipo:
            </label>
            <select 
              value={tipoFiltro} 
              onChange={(e) => setTipoFiltro(e.target.value)}
              style={{padding: '10px', borderRadius: '6px', border: '2px solid #e2e8f0'}}
            >
              <option value="todos">Todos los tipos</option>
              {Object.entries(tiposFecha).map(([key, val]) => (
                <option key={key} value={key}>{val.emoji} {val.nombre}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Estadísticas rápidas */}
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '30px'}}>
          <div style={{background: '#fff5f5', padding: '20px', borderRadius: '10px', borderLeft: '4px solid #dc3545'}}>
            <div style={{fontSize: '32px', fontWeight: 'bold', color: '#dc3545'}}>
              {fechasProximas.filter(f => f.dias_restantes <= 1).length}
            </div>
            <div style={{color: '#dc3545', fontWeight: '600'}}>Urgentes (1 día)</div>
          </div>
          
          <div style={{background: '#fffbeb', padding: '20px', borderRadius: '10px', borderLeft: '4px solid #ffc107'}}>
            <div style={{fontSize: '32px', fontWeight: 'bold', color: '#ffc107'}}>
              {fechasProximas.filter(f => f.dias_restantes > 1 && f.dias_restantes <= 7).length}
            </div>
            <div style={{color: '#d97706', fontWeight: '600'}}>Esta semana</div>
          </div>
          
          <div style={{background: '#f0f9ff', padding: '20px', borderRadius: '10px', borderLeft: '4px solid #17a2b8'}}>
            <div style={{fontSize: '32px', fontWeight: 'bold', color: '#17a2b8'}}>
              {fechasProximas.filter(f => f.dias_restantes > 7 && f.dias_restantes <= 30).length}
            </div>
            <div style={{color: '#17a2b8', fontWeight: '600'}}>Este mes</div>
          </div>
          
          <div style={{background: '#f8f9fa', padding: '20px', borderRadius: '10px', borderLeft: '4px solid #6c757d'}}>
            <div style={{fontSize: '32px', fontWeight: 'bold', color: '#2d3748'}}>
              {fechasProximas.length}
            </div>
            <div style={{color: '#6c757d', fontWeight: '600'}}>Total</div>
          </div>
        </div>
      </div>

      {/* Lista de fechas */}
      {fechasFiltradas.length === 0 ? (
        <div style={{background: 'white', padding: '60px', textAlign: 'center', borderRadius: '12px'}}>
          <div style={{fontSize: '64px', marginBottom: '16px'}}>📭</div>
          <h3>No hay fechas próximas</h3>
          <p style={{color: '#718096'}}>No se encontraron fechas importantes en este período</p>
        </div>
      ) : (
        <div style={{display: 'grid', gap: '16px'}}>
          {fechasFiltradas.map(fecha => {
            const tipoInfo = tiposFecha[fecha.tipo_fecha] || tiposFecha.otro
            const urgencia = getUrgencia(fecha.dias_restantes)
            
            return (
              <div 
                key={fecha.id}
                style={{
                  background: 'white',
                  padding: '20px',
                  borderRadius: '10px',
                  borderLeft: `4px solid ${tipoInfo.color}`,
                  boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
                  display: 'grid',
                  gridTemplateColumns: '60px 1fr 120px 150px',
                  gap: '20px',
                  alignItems: 'center'
                }}
              >
                {/* Emoji */}
                <div style={{
                  width: '50px',
                  height: '50px',
                  borderRadius: '50%',
                  background: tipoInfo.color,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '24px'
                }}>
                  {tipoInfo.emoji}
                </div>

                {/* Información */}
                <div>
                  <h4 style={{margin: '0 0 4px 0', fontSize: '18px', color: '#2d3748'}}>
                    {tipoInfo.nombre}
                  </h4>
                  <p style={{margin: '0 0 4px 0', color: '#718096', fontSize: '14px'}}>
                    <strong>{fecha.estudiante?.nombre}</strong> ({fecha.estudiante?.email})
                  </p>
                  {fecha.descripcion && (
                    <p style={{margin: '4px 0 0 0', color: '#4a5568', fontSize: '13px'}}>
                      {fecha.descripcion}
                    </p>
                  )}
                </div>

                {/* Días restantes */}
                <div style={{textAlign: 'center'}}>
                  <div style={{fontSize: '36px', fontWeight: 'bold', color: urgencia.color}}>
                    {fecha.dias_restantes}
                  </div>
                  <div style={{fontSize: '13px', color: '#718096'}}>
                    día{fecha.dias_restantes !== 1 ? 's' : ''}
                  </div>
                </div>

                {/* Fecha y urgencia */}
                <div style={{textAlign: 'right'}}>
                  <div style={{
                    display: 'inline-block',
                    padding: '6px 12px',
                    borderRadius: '20px',
                    background: urgencia.color,
                    color: 'white',
                    fontSize: '12px',
                    fontWeight: '600',
                    marginBottom: '8px'
                  }}>
                    {urgencia.texto}
                  </div>
                  <div style={{fontSize: '13px', color: '#4a5568'}}>
                    {formatearFecha(fecha.fecha)}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default AlertasAdmin
