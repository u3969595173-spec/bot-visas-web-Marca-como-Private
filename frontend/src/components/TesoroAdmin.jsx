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
                <tr style={{ backgroundColor: '#f8fafc' }}>
                  <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                    Cliente
                  </th>
                  <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                    Servicios
                  </th>
                  <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                    Desglose de Pagos
                  </th>
                  <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                    Monto Total
                  </th>
                  <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                    Fecha Aceptación
                  </th>
                  <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                    Estado
                  </th>
                  <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody>
                {pagos.map((pago) => (
                  <tr key={pago.presupuesto_id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '12px' }}>
                      <div>
                        <div style={{ fontWeight: '600', color: '#2d3748' }}>
                          {pago.nombre_estudiante || pago.estudiante_nombre}
                        </div>
                        <div style={{ fontSize: '12px', color: '#718096' }}>
                          ID: {pago.presupuesto_id}
                        </div>
                      </div>
                    </td>
                    <td style={{ padding: '12px' }}>
                      <div style={{ fontSize: '12px', color: '#4a5568' }}>
                        {pago.servicios_solicitados?.slice(0, 2).join(', ')}
                        {pago.servicios_solicitados?.length > 2 && '...'}
                      </div>
                    </td>
                    <td style={{ padding: '12px' }}>
                      <div style={{ fontSize: '12px', lineHeight: '1.8' }}>
                        {/* Pago Inicial */}
                        {pago.precio_al_empezar > 0 && (
                          <div style={{ 
                            display: 'flex', 
                            alignItems: 'center', 
                            gap: '8px',
                            marginBottom: '6px',
                            padding: '6px 10px',
                            backgroundColor: pago.pagado_al_empezar ? '#d1fae5' : '#fef3c7',
                            borderRadius: '6px',
                            border: `2px solid ${pago.pagado_al_empezar ? '#10b981' : '#f59e0b'}`
                          }}>
                            <input
                              type="checkbox"
                              checked={pago.pagado_al_empezar || false}
                              onChange={(e) => marcarPagoIndividual(pago.presupuesto_id, 'al_empezar', e.target.checked)}
                              style={{ 
                                cursor: 'pointer',
                                width: '16px',
                                height: '16px'
                              }}
                              disabled={pago.pagado}
                            />
                            <span style={{ 
                              fontWeight: '500',
                              color: pago.pagado_al_empezar ? '#065f46' : '#92400e'
                            }}>
                              🚀 Inicial: €{pago.precio_al_empezar.toFixed(2)}
                            </span>
                            {pago.fecha_pago_al_empezar && (
                              <span style={{ fontSize: '10px', color: '#6b7280' }}>
                                ({new Date(pago.fecha_pago_al_empezar).toLocaleDateString('es-ES')})
                              </span>
                            )}
                          </div>
                        )}
                        
                        {/* Pago con Visa */}
                        {pago.precio_con_visa > 0 && (
                          <div style={{ 
                            display: 'flex', 
                            alignItems: 'center', 
                            gap: '8px',
                            marginBottom: '6px',
                            padding: '6px 10px',
                            backgroundColor: pago.pagado_con_visa ? '#d1fae5' : '#dbeafe',
                            borderRadius: '6px',
                            border: `2px solid ${pago.pagado_con_visa ? '#10b981' : '#3b82f6'}`
                          }}>
                            <input
                              type="checkbox"
                              checked={pago.pagado_con_visa || false}
                              onChange={(e) => marcarPagoIndividual(pago.presupuesto_id, 'con_visa', e.target.checked)}
                              style={{ 
                                cursor: 'pointer',
                                width: '16px',
                                height: '16px'
                              }}
                              disabled={pago.pagado}
                            />
                            <span style={{ 
                              fontWeight: '500',
                              color: pago.pagado_con_visa ? '#065f46' : '#1e40af'
                            }}>
                              🎯 Con Visa: €{pago.precio_con_visa.toFixed(2)}
                            </span>
                            {pago.fecha_pago_con_visa && (
                              <span style={{ fontSize: '10px', color: '#6b7280' }}>
                                ({new Date(pago.fecha_pago_con_visa).toLocaleDateString('es-ES')})
                              </span>
                            )}
                          </div>
                        )}
                        
                        {/* Pago Financiado */}
                        {pago.precio_financiado > 0 && (
                          <div style={{ 
                            display: 'flex', 
                            alignItems: 'center', 
                            gap: '8px',
                            padding: '6px 10px',
                            backgroundColor: pago.pagado_financiado ? '#d1fae5' : '#e0e7ff',
                            borderRadius: '6px',
                            border: `2px solid ${pago.pagado_financiado ? '#10b981' : '#6366f1'}`
                          }}>
                            <input
                              type="checkbox"
                              checked={pago.pagado_financiado || false}
                              onChange={(e) => marcarPagoIndividual(pago.presupuesto_id, 'financiado', e.target.checked)}
                              style={{ 
                                cursor: 'pointer',
                                width: '16px',
                                height: '16px'
                              }}
                              disabled={pago.pagado}
                            />
                            <span style={{ 
                              fontWeight: '500',
                              color: pago.pagado_financiado ? '#065f46' : '#4338ca'
                            }}>
                              📅 Financiado: €{pago.precio_financiado.toFixed(2)}
                            </span>
                            {pago.fecha_pago_financiado && (
                              <span style={{ fontSize: '10px', color: '#6b7280' }}>
                                ({new Date(pago.fecha_pago_financiado).toLocaleDateString('es-ES')})
                              </span>
                            )}
                          </div>
                        )}
                        
                        {/* Mensaje si todo está pagado */}
                        {pago.pagado && (
                          <div style={{
                            marginTop: '8px',
                            padding: '4px 8px',
                            backgroundColor: '#d1fae5',
                            borderRadius: '4px',
                            fontSize: '11px',
                            color: '#065f46',
                            fontWeight: '600',
                            textAlign: 'center'
                          }}>
                            ✅ Completamente Pagado
                          </div>
                        )}
                      </div>
                    </td>
                    <td style={{ padding: '12px' }}>
                      <div style={{ fontWeight: '600', color: '#059669', fontSize: '15px' }}>
                        €{(pago.monto_a_pagar || pago.monto_total || 0).toFixed(2)}
                      </div>
                      <div style={{ fontSize: '10px', color: '#718096' }}>
                        Total
                      </div>
                    </td>
                    <td style={{ padding: '12px', fontSize: '12px', color: '#4a5568' }}>
                      {formatearFecha(pago.fecha_aceptacion)}
                    </td>
                    <td style={{ padding: '12px' }}>
                      {pago.pagado ? (
                        <span style={{
                          padding: '6px 12px',
                          borderRadius: '20px',
                          backgroundColor: '#d1fae5',
                          color: '#065f46',
                          fontSize: '12px',
                          fontWeight: '600'
                        }}>
                          ✅ Pagado
                        </span>
                      ) : (
                        <span style={{
                          padding: '6px 12px',
                          borderRadius: '20px',
                          backgroundColor: '#fef3c7',
                          color: '#92400e',
                          fontSize: '12px',
                          fontWeight: '600'
                        }}>
                          ⏳ Pendiente
                        </span>
                      )}
                    </td>
                    <td style={{ padding: '12px' }}>
                      {pago.pagado ? (
                        <div style={{
                          padding: '8px 12px',
                          backgroundColor: '#d1fae5',
                          color: '#065f46',
                          borderRadius: '6px',
                          fontSize: '13px',
                          fontWeight: '600',
                          textAlign: 'center'
                        }}>
                          ✅ Todo Pagado
                          {pago.fecha_pago && (
                            <div style={{ fontSize: '10px', marginTop: '4px', fontWeight: 'normal' }}>
                              {formatearFecha(pago.fecha_pago)}
                            </div>
                          )}
                        </div>
                      ) : (
                        <div style={{ fontSize: '11px', color: '#6b7280', textAlign: 'center' }}>
                          Marcar pagos ← con checkboxes
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