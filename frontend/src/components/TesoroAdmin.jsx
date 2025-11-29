import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function TesoroAdmin({ embedded = false }) {
  const [pagos, setPagos] = useState([])
  const [estadisticas, setEstadisticas] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    cargarPagos()
  }, [])

  const cargarPagos = async () => {
    setLoading(true)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await axios.get(`${apiUrl}/api/admin/tesoro`)
      console.log('[TESORO] Respuesta del API:', response.data)
      
      // El backend devuelve un objeto con pagos y estadisticas
      if (response.data && response.data.pagos) {
        setPagos(Array.isArray(response.data.pagos) ? response.data.pagos : [])
        setEstadisticas(response.data.estadisticas || null)
      } else if (Array.isArray(response.data)) {
        // Por si acaso devuelve un array directo (backward compatibility)
        setPagos(response.data)
      } else {
        console.error('[TESORO] Formato inesperado:', response.data)
        setPagos([])
        setError('Error: Los datos recibidos no tienen el formato correcto')
      }
      setError('')
    } catch (err) {
      console.error('[TESORO] Error:', err)
      setPagos([])
      setError('Error al cargar pagos: ' + (err.response?.data?.detail || err.message))
    } finally {
      setLoading(false)
    }
  }

  const marcarComoPagado = async (presupuestoId) => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      await axios.put(`${apiUrl}/api/admin/tesoro/${presupuestoId}/marcar-pagado`)
      setSuccess('✅ Pago marcado como recibido')
      cargarPagos()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Error al marcar pago: ' + (err.response?.data?.detail || err.message))
    }
  }

  const marcarPagoIndividual = async (presupuestoId, modalidad, pagado) => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      await axios.put(`${apiUrl}/api/admin/tesoro/${presupuestoId}/marcar-pago-individual`, {
        modalidad,
        pagado
      })
      setSuccess(`✅ Pago ${modalidad} ${pagado ? 'marcado' : 'desmarcado'}`)
      cargarPagos()
      setTimeout(() => setSuccess(''), 2000)
    } catch (err) {
      setError('Error al actualizar pago: ' + (err.response?.data?.detail || err.message))
      setTimeout(() => setError(''), 3000)
    }
  }

  const formatearFecha = (fecha) => {
    if (!fecha) return 'No registrada'
    return new Date(fecha).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const formatearModalidad = (modalidad) => {
    if (!modalidad || modalidad === 'sin_seleccionar') {
      return '⚠️ Sin seleccionar';
    }
    const modalidades = {
      'precio_al_empezar': '💳 Pago al Empezar',
      'al_empezar': '💳 Pago al Empezar',
      'precio_con_visa': '🎯 Pago con Visa',
      'con_visa': '🎯 Pago con Visa',
      'precio_financiado': '📅 Pago Financiado',
      'financiado': '📅 Pago Financiado'
    };
    return modalidades[modalidad] || modalidad;
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Cargando tesoro de pagos...</div>
      </div>
    )
  }

  return (
    <div className="container">
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '30px'
      }}>
        <div>
          <h1 style={{ color: 'white', marginBottom: '5px' }}>
            💰 Tesoro de Pagos
          </h1>
          <p style={{ color: 'rgba(255,255,255,0.9)' }}>
            Gestión de todos los pagos pendientes y realizados
          </p>
        </div>
        {!embedded && (
          <button
            onClick={() => navigate('/admin')}
            className="btn"
            style={{ background: 'white', color: '#667eea' }}
          >
            ← Volver al Dashboard
          </button>
        )}
      </div>

      {/* Alertas */}
      {error && (
        <div className="alert alert-danger" style={{ marginBottom: '20px' }}>
          {error}
        </div>
      )}

      {success && (
        <div className="alert alert-success" style={{ marginBottom: '20px' }}>
          {success}
        </div>
      )}

      {/* Estadísticas */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '20px',
        marginBottom: '30px'
      }}>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#10b981' }}>
            {pagos.filter(p => !p.pagado).length}
          </div>
          <div style={{ color: '#718096', marginTop: '5px' }}>
            Pagos Pendientes
          </div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#059669' }}>
            {pagos.filter(p => p.pagado).length}
          </div>
          <div style={{ color: '#718096', marginTop: '5px' }}>
            Pagos Realizados
          </div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#3b82f6' }}>
            €{pagos.filter(p => !p.pagado).reduce((sum, p) => sum + (p.monto_a_pagar || p.monto_total || 0), 0).toFixed(2)}
          </div>
          <div style={{ color: '#718096', marginTop: '5px' }}>
            Total Pendiente
          </div>
        </div>
      </div>

      {/* Lista de Pagos */}
      <div className="card">
        <div style={{ 
          borderBottom: '1px solid #e2e8f0',
          paddingBottom: '15px',
          marginBottom: '20px'
        }}>
          <h3 style={{ margin: 0, color: '#2d3748' }}>
            📊 Todos los Pagos
          </h3>
        </div>

        {pagos.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#718096' }}>
            No hay pagos registrados
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#667eea', color: 'white' }}>
                  <th style={{ padding: '14px', textAlign: 'left', fontWeight: '600', fontSize: '13px' }}>
                    👤 CLIENTE
                  </th>
                  <th style={{ padding: '14px', textAlign: 'left', fontWeight: '600', fontSize: '13px' }}>
                    📋 SERVICIOS
                  </th>
                  <th style={{ padding: '14px', textAlign: 'left', fontWeight: '600', fontSize: '13px', minWidth: '300px' }}>
                    💳 DESGLOSE DE PAGOS
                  </th>
                  <th style={{ padding: '14px', textAlign: 'center', fontWeight: '600', fontSize: '13px' }}>
                    💰 MONTO TOTAL
                  </th>
                  <th style={{ padding: '14px', textAlign: 'center', fontWeight: '600', fontSize: '13px' }}>
                    📅 FECHA
                  </th>
                  <th style={{ padding: '14px', textAlign: 'center', fontWeight: '600', fontSize: '13px' }}>
                    ⚡ ESTADO
                  </th>
                </tr>
              </thead>
              <tbody>
                {pagos.map((pago, index) => (
                  <tr 
                    key={pago.presupuesto_id} 
                    style={{ 
                      borderBottom: '1px solid #e2e8f0',
                      backgroundColor: index % 2 === 0 ? '#ffffff' : '#f8fafc',
                      transition: 'all 0.2s'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f1f5f9'}
                    onMouseLeave={(e) => e.currentTarget.style.backgroundColor = index % 2 === 0 ? '#ffffff' : '#f8fafc'}
                  >
                    {/* Cliente */}
                    <td style={{ padding: '16px', verticalAlign: 'top' }}>
                      <div>
                        <div style={{ fontWeight: '600', color: '#1e293b', fontSize: '14px', marginBottom: '4px' }}>
                          {pago.nombre_estudiante || pago.estudiante_nombre}
                        </div>
                        <div style={{ fontSize: '11px', color: '#94a3b8', fontFamily: 'monospace' }}>
                          #{pago.presupuesto_id}
                        </div>
                      </div>
                    </td>

                    {/* Servicios */}
                    <td style={{ padding: '16px', verticalAlign: 'top' }}>
                      <div style={{ fontSize: '12px', color: '#475569', lineHeight: '1.6' }}>
                        {pago.servicios_solicitados && pago.servicios_solicitados.length > 0 ? (
                          <>
                            {pago.servicios_solicitados.slice(0, 2).map((servicio, idx) => (
                              <div key={idx} style={{ marginBottom: '3px' }}>
                                • {servicio}
                              </div>
                            ))}
                            {pago.servicios_solicitados.length > 2 && (
                              <div style={{ 
                                fontSize: '11px', 
                                color: '#667eea', 
                                fontWeight: '600',
                                marginTop: '5px'
                              }}>
                                +{pago.servicios_solicitados.length - 2} más
                              </div>
                            )}
                          </>
                        ) : (
                          <span style={{ color: '#94a3b8', fontStyle: 'italic' }}>Sin servicios</span>
                        )}
                      </div>
                    </td>

                    {/* Desglose de Pagos */}
                    <td style={{ padding: '16px', verticalAlign: 'top' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {/* Pago Inicial */}
                        {pago.precio_al_empezar > 0 && (
                          <label style={{ 
                            display: 'flex', 
                            alignItems: 'center', 
                            gap: '10px',
                            padding: '10px 14px',
                            backgroundColor: pago.pagado_al_empezar ? '#ecfdf5' : '#fffbeb',
                            borderRadius: '8px',
                            border: `2px solid ${pago.pagado_al_empezar ? '#10b981' : '#fbbf24'}`,
                            cursor: pago.pagado ? 'not-allowed' : 'pointer',
                            transition: 'all 0.2s',
                            opacity: pago.pagado ? 0.6 : 1
                          }}>
                            <input
                              type="checkbox"
                              checked={pago.pagado_al_empezar || false}
                              onChange={(e) => marcarPagoIndividual(pago.presupuesto_id, 'al_empezar', e.target.checked)}
                              style={{ 
                                cursor: pago.pagado ? 'not-allowed' : 'pointer',
                                width: '18px',
                                height: '18px',
                                accentColor: '#10b981'
                              }}
                              disabled={pago.pagado}
                            />
                            <div style={{ flex: 1 }}>
                              <div style={{ 
                                fontWeight: '600',
                                color: pago.pagado_al_empezar ? '#065f46' : '#92400e',
                                fontSize: '13px'
                              }}>
                                🚀 Pago Inicial
                              </div>
                              <div style={{ fontSize: '15px', fontWeight: '700', color: pago.pagado_al_empezar ? '#047857' : '#b45309', marginTop: '2px' }}>
                                €{pago.precio_al_empezar.toFixed(2)}
                              </div>
                              {pago.fecha_pago_al_empezar && (
                                <div style={{ fontSize: '10px', color: '#64748b', marginTop: '4px' }}>
                                  ✓ {new Date(pago.fecha_pago_al_empezar).toLocaleDateString('es-ES')}
                                </div>
                              )}
                            </div>
                          </label>
                        )}
                        
                        {/* Pago con Visa */}
                        {pago.precio_con_visa > 0 && (
                          <label style={{ 
                            display: 'flex', 
                            alignItems: 'center', 
                            gap: '10px',
                            padding: '10px 14px',
                            backgroundColor: pago.pagado_con_visa ? '#ecfdf5' : '#eff6ff',
                            borderRadius: '8px',
                            border: `2px solid ${pago.pagado_con_visa ? '#10b981' : '#60a5fa'}`,
                            cursor: pago.pagado ? 'not-allowed' : 'pointer',
                            transition: 'all 0.2s',
                            opacity: pago.pagado ? 0.6 : 1
                          }}>
                            <input
                              type="checkbox"
                              checked={pago.pagado_con_visa || false}
                              onChange={(e) => marcarPagoIndividual(pago.presupuesto_id, 'con_visa', e.target.checked)}
                              style={{ 
                                cursor: pago.pagado ? 'not-allowed' : 'pointer',
                                width: '18px',
                                height: '18px',
                                accentColor: '#10b981'
                              }}
                              disabled={pago.pagado}
                            />
                            <div style={{ flex: 1 }}>
                              <div style={{ 
                                fontWeight: '600',
                                color: pago.pagado_con_visa ? '#065f46' : '#1e40af',
                                fontSize: '13px'
                              }}>
                                🎯 Con Visa
                              </div>
                              <div style={{ fontSize: '15px', fontWeight: '700', color: pago.pagado_con_visa ? '#047857' : '#2563eb', marginTop: '2px' }}>
                                €{pago.precio_con_visa.toFixed(2)}
                              </div>
                              {pago.fecha_pago_con_visa && (
                                <div style={{ fontSize: '10px', color: '#64748b', marginTop: '4px' }}>
                                  ✓ {new Date(pago.fecha_pago_con_visa).toLocaleDateString('es-ES')}
                                </div>
                              )}
                            </div>
                          </label>
                        )}
                        
                        {/* Pago Financiado */}
                        {pago.precio_financiado > 0 && (
                          <label style={{ 
                            display: 'flex', 
                            alignItems: 'center', 
                            gap: '10px',
                            padding: '10px 14px',
                            backgroundColor: pago.pagado_financiado ? '#ecfdf5' : '#f5f3ff',
                            borderRadius: '8px',
                            border: `2px solid ${pago.pagado_financiado ? '#10b981' : '#a78bfa'}`,
                            cursor: pago.pagado ? 'not-allowed' : 'pointer',
                            transition: 'all 0.2s',
                            opacity: pago.pagado ? 0.6 : 1
                          }}>
                            <input
                              type="checkbox"
                              checked={pago.pagado_financiado || false}
                              onChange={(e) => marcarPagoIndividual(pago.presupuesto_id, 'financiado', e.target.checked)}
                              style={{ 
                                cursor: pago.pagado ? 'not-allowed' : 'pointer',
                                width: '18px',
                                height: '18px',
                                accentColor: '#10b981'
                              }}
                              disabled={pago.pagado}
                            />
                            <div style={{ flex: 1 }}>
                              <div style={{ 
                                fontWeight: '600',
                                color: pago.pagado_financiado ? '#065f46' : '#5b21b6',
                                fontSize: '13px'
                              }}>
                                📅 Financiado
                              </div>
                              <div style={{ fontSize: '15px', fontWeight: '700', color: pago.pagado_financiado ? '#047857' : '#7c3aed', marginTop: '2px' }}>
                                €{pago.precio_financiado.toFixed(2)}
                              </div>
                              {pago.fecha_pago_financiado && (
                                <div style={{ fontSize: '10px', color: '#64748b', marginTop: '4px' }}>
                                  ✓ {new Date(pago.fecha_pago_financiado).toLocaleDateString('es-ES')}
                                </div>
                              )}
                            </div>
                          </label>
                        )}
                      </div>
                    </td>

                    {/* Monto Total */}
                    <td style={{ padding: '16px', textAlign: 'center', verticalAlign: 'top' }}>
                      <div style={{ 
                        fontWeight: '700', 
                        color: '#059669', 
                        fontSize: '18px',
                        marginBottom: '4px'
                      }}>
                        €{(pago.monto_a_pagar || pago.monto_total || 0).toFixed(2)}
                      </div>
                      <div style={{ fontSize: '10px', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                        Total
                      </div>
                    </td>

                    {/* Fecha */}
                    <td style={{ padding: '16px', textAlign: 'center', verticalAlign: 'top' }}>
                      <div style={{ fontSize: '12px', color: '#475569' }}>
                        {pago.fecha_aceptacion ? (
                          <>
                            <div style={{ fontWeight: '600' }}>
                              {new Date(pago.fecha_aceptacion).toLocaleDateString('es-ES')}
                            </div>
                            <div style={{ fontSize: '10px', color: '#94a3b8', marginTop: '2px' }}>
                              {new Date(pago.fecha_aceptacion).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}
                            </div>
                          </>
                        ) : (
                          <span style={{ color: '#cbd5e1' }}>—</span>
                        )}
                      </div>
                    </td>

                    {/* Estado */}
                    <td style={{ padding: '16px', textAlign: 'center', verticalAlign: 'top' }}>
                      {pago.pagado ? (
                        <div>
                          <div style={{
                            display: 'inline-block',
                            padding: '8px 16px',
                            borderRadius: '20px',
                            backgroundColor: '#d1fae5',
                            color: '#065f46',
                            fontSize: '13px',
                            fontWeight: '700',
                            border: '2px solid #10b981'
                          }}>
                            ✅ COMPLETADO
                          </div>
                          {pago.fecha_pago && (
                            <div style={{ fontSize: '10px', color: '#64748b', marginTop: '6px' }}>
                              {new Date(pago.fecha_pago).toLocaleDateString('es-ES')}
                            </div>
                          )}
                        </div>
                      ) : (
                        <div>
                          <div style={{
                            display: 'inline-block',
                            padding: '8px 16px',
                            borderRadius: '20px',
                            backgroundColor: '#fef3c7',
                            color: '#92400e',
                            fontSize: '13px',
                            fontWeight: '700',
                            border: '2px solid #fbbf24'
                          }}>
                            ⏳ PENDIENTE
                          </div>
                          <div style={{ fontSize: '10px', color: '#94a3b8', marginTop: '6px', fontStyle: 'italic' }}>
                            Marcar arriba ↑
                          </div>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default TesoroAdmin