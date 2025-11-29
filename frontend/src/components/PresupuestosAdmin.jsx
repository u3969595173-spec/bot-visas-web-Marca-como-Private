import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function PresupuestosAdmin({ embedded = false }) {
  const [presupuestos, setPresupuestos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [presupuestoSeleccionado, setPresupuestoSeleccionado] = useState(null)
  const [mostrarModal, setMostrarModal] = useState(false)
  const [serviciosExpandidos, setServiciosExpandidos] = useState({}) // Para controlar qué presupuestos están expandidos
  const [modalidades, setModalidades] = useState({
    precio_al_empezar: '',
    precio_con_visa: '',
    precio_financiado: '',
    mensaje_admin: ''
  })
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    cargarPresupuestos()
  }, [])

  const cargarPresupuestos = async () => {
    setLoading(true)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await axios.get(`${apiUrl}/api/admin/presupuestos`)
      setPresupuestos(response.data)
      setError('')
    } catch (err) {
      setError('Error al cargar presupuestos: ' + (err.response?.data?.detail || err.message))
    } finally {
      setLoading(false)
    }
  }

  const abrirModalOferta = (presupuesto) => {
    setPresupuestoSeleccionado(presupuesto)
    setModalidades({
      precio_al_empezar: '',
      precio_con_visa: '',
      precio_financiado: '',
      mensaje_admin: ''
    })
    setMostrarModal(true)
  }

  const enviarOferta = async () => {
    if (!presupuestoSeleccionado) return

    // Validación - al menos una modalidad debe estar completa
    const tieneAlMenosUnaModalidad = modalidades.precio_al_empezar || 
                                     modalidades.precio_con_visa || 
                                     modalidades.precio_financiado

    if (!tieneAlMenosUnaModalidad) {
      setError('⚠️ Debes completar al menos una modalidad de pago')
      setTimeout(() => setError(''), 3000)
      return
    }

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      await axios.put(`${apiUrl}/api/admin/presupuestos/${presupuestoSeleccionado.id}/ofertar-modalidades`, modalidades)
      setSuccess('✅ Oferta enviada exitosamente al cliente')
      setMostrarModal(false)
      setModalidades({
        precio_al_empezar: '',
        precio_con_visa: '',
        precio_financiado: '',
        mensaje_admin: ''
      })
      cargarPresupuestos()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('❌ Error al enviar oferta: ' + (err.response?.data?.detail || err.message))
      setTimeout(() => setError(''), 5000)
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

  const getEstadoBadge = (estado) => {
    const estados = {
      'pendiente': { color: '#f59e0b', bg: '#fef3c7', text: '⏳ Pendiente' },
      'ofertado': { color: '#3b82f6', bg: '#dbeafe', text: '📤 Oferta Enviada' },
      'oferta_enviada': { color: '#3b82f6', bg: '#dbeafe', text: '📤 Oferta Enviada' },
      'aceptado': { color: '#10b981', bg: '#d1fae5', text: '✅ Aceptado' },
      'rechazado': { color: '#ef4444', bg: '#fee2e2', text: '❌ Rechazado' }
    }
    const estado_info = estados[estado] || { color: '#6b7280', bg: '#f3f4f6', text: estado }
    
    return (
      <span style={{
        padding: '6px 12px',
        borderRadius: '20px',
        backgroundColor: estado_info.bg,
        color: estado_info.color,
        fontSize: '12px',
        fontWeight: '600'
      }}>
        {estado_info.text}
      </span>
    )
  }

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Cargando presupuestos...</div>
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
            📋 Gestión de Presupuestos
          </h1>
          <p style={{ color: 'rgba(255,255,255,0.9)' }}>
            Administra todas las solicitudes de presupuesto
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
          <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#f59e0b' }}>
            {presupuestos.filter(p => p.estado === 'pendiente').length}
          </div>
          <div style={{ color: '#718096', marginTop: '5px' }}>
            Pendientes
          </div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#3b82f6' }}>
            {presupuestos.filter(p => p.estado === 'ofertado' || p.estado === 'oferta_enviada').length}
          </div>
          <div style={{ color: '#718096', marginTop: '5px' }}>
            Ofertas Enviadas
          </div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#10b981' }}>
            {presupuestos.filter(p => p.estado === 'aceptado').length}
          </div>
          <div style={{ color: '#718096', marginTop: '5px' }}>
            Aceptados
          </div>
        </div>
      </div>

      {/* Lista de Presupuestos */}
      <div className="card">
        <div style={{
          borderBottom: '1px solid #e2e8f0',
          paddingBottom: '15px',
          marginBottom: '20px'
        }}>
          <h3 style={{ margin: 0, color: '#2d3748' }}>
            📊 Todas las Solicitudes
          </h3>
        </div>

        {presupuestos.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#718096' }}>
            No hay presupuestos registrados
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
                    Estado
                  </th>
                  <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                    Fecha Solicitud
                  </th>
                  <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody>
                {presupuestos.map((presupuesto) => (
                  <tr key={presupuesto.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '12px' }}>
                      <div>
                        <div style={{ fontWeight: '600', color: '#2d3748' }}>
                          {presupuesto.nombre_estudiante || 'Sin nombre'}
                        </div>
                        <div style={{ fontSize: '12px', color: '#718096' }}>
                          ID: {presupuesto.id}
                        </div>
                      </div>
                    </td>
                    <td style={{ padding: '12px', maxWidth: '300px' }}>
                      <div style={{ fontSize: '12px', color: '#4a5568', lineHeight: '1.6' }}>
                        {presupuesto.servicios_solicitados && Array.isArray(presupuesto.servicios_solicitados) ? (
                          <div>
                            {/* Siempre mostrar solo el primer servicio */}
                            {presupuesto.servicios_solicitados.length > 0 && (
                              <div style={{ 
                                marginBottom: '5px',
                                padding: '6px 10px',
                                background: '#f0f9ff',
                                borderRadius: '6px',
                                border: '1px solid #bfdbfe',
                                fontSize: '11px'
                              }}>
                                • {presupuesto.servicios_solicitados[0]}
                              </div>
                            )}
                            
                            {/* Mostrar servicios expandidos si se hizo clic en "Ver más" */}
                            {serviciosExpandidos[presupuesto.id] && presupuesto.servicios_solicitados.slice(1).map((servicio, idx) => (
                              <div key={idx} style={{ 
                                marginBottom: '5px',
                                padding: '6px 10px',
                                background: '#f0f9ff',
                                borderRadius: '6px',
                                border: '1px solid #bfdbfe',
                                fontSize: '11px'
                              }}>
                                • {servicio}
                              </div>
                            ))}
                            
                            {/* Botón "Ver más" / "Ver menos" */}
                            {presupuesto.servicios_solicitados.length > 1 && (
                              <button
                                onClick={() => setServiciosExpandidos({
                                  ...serviciosExpandidos,
                                  [presupuesto.id]: !serviciosExpandidos[presupuesto.id]
                                })}
                                style={{ 
                                  marginTop: '6px',
                                  color: '#3b82f6',
                                  fontWeight: '600',
                                  fontSize: '11px',
                                  background: 'none',
                                  border: 'none',
                                  cursor: 'pointer',
                                  padding: '4px 8px',
                                  borderRadius: '4px',
                                  transition: 'background 0.2s'
                                }}
                                onMouseEnter={(e) => e.target.style.background = '#dbeafe'}
                                onMouseLeave={(e) => e.target.style.background = 'none'}
                              >
                                {serviciosExpandidos[presupuesto.id] 
                                  ? '▲ Ver menos' 
                                  : `▼ Ver ${presupuesto.servicios_solicitados.length - 1} más`
                                }
                              </button>
                            )}
                          </div>
                        ) : (
                          <div style={{ color: '#9ca3af' }}>
                            {presupuesto.servicios || 'Sin servicios'}
                          </div>
                        )}
                      </div>
                    </td>
                    <td style={{ padding: '12px' }}>
                      {getEstadoBadge(presupuesto.estado)}
                    </td>
                    <td style={{ padding: '12px', fontSize: '12px', color: '#4a5568' }}>
                      {formatearFecha(presupuesto.created_at)}
                    </td>
                    <td style={{ padding: '12px' }}>
                      {presupuesto.estado === 'pendiente' && (
                        <button
                          onClick={() => abrirModalOferta(presupuesto)}
                          style={{
                            padding: '6px 12px',
                            backgroundColor: '#3b82f6',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            fontSize: '12px',
                            cursor: 'pointer'
                          }}
                        >
                          💰 Crear Oferta
                        </button>
                      )}
                      {(presupuesto.estado === 'ofertado' || presupuesto.estado === 'oferta_enviada') && (
                        <div style={{ fontSize: '12px' }}>
                          <div style={{ fontWeight: '600', color: '#3b82f6', marginBottom: '4px' }}>
                            Oferta Enviada
                          </div>
                          <div style={{ fontSize: '11px', color: '#6b7280' }}>
                            {presupuesto.precio_al_empezar && `Inicial: €${parseFloat(presupuesto.precio_al_empezar).toFixed(2)}`}
                            {presupuesto.precio_con_visa && ` | Cita: €${parseFloat(presupuesto.precio_con_visa).toFixed(2)}`}
                            {presupuesto.precio_financiado && ` | Fin: €${parseFloat(presupuesto.precio_financiado).toFixed(2)}`}
                          </div>
                          <div style={{ fontWeight: '600', color: '#059669', marginTop: '4px' }}>
                            Total: €{(
                              (parseFloat(presupuesto.precio_al_empezar) || 0) +
                              (parseFloat(presupuesto.precio_con_visa) || 0) +
                              (parseFloat(presupuesto.precio_financiado) || 0)
                            ).toFixed(2)}
                          </div>
                        </div>
                      )}
                      {presupuesto.estado === 'aceptado' && (
                        <div style={{ fontSize: '12px' }}>
                          <div style={{ fontWeight: '600', color: '#10b981', marginBottom: '4px' }}>
                            ✅ Aceptado
                          </div>
                          <div style={{ fontWeight: '600', color: '#059669' }}>
                            €{(
                              (parseFloat(presupuesto.precio_al_empezar) || 0) +
                              (parseFloat(presupuesto.precio_con_visa) || 0) +
                              (parseFloat(presupuesto.precio_financiado) || 0)
                            ).toFixed(2)}
                          </div>
                          <div style={{ color: '#6b7280', fontSize: '10px' }}>Total</div>
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

      {/* Modal de Oferta */}
      {mostrarModal && presupuestoSeleccionado && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000,
          padding: '20px'
        }}>
          <div style={{
            backgroundColor: 'white',
            padding: '30px',
            borderRadius: '15px',
            maxWidth: '800px',
            width: '95%',
            maxHeight: '90vh',
            overflowY: 'auto'
          }}>
            <h3 style={{ 
              marginTop: 0, 
              marginBottom: '10px', 
              color: '#1f2937',
              borderBottom: '2px solid #10b981',
              paddingBottom: '10px'
            }}>
              💰 Crear Oferta de Presupuesto
            </h3>
            
            <p style={{ color: '#6b7280', marginBottom: '25px' }}>
              Cliente: <strong>{presupuestoSeleccionado.nombre_estudiante || 'Sin nombre'}</strong>
            </p>

            {/* Servicios Solicitados por el Cliente */}
            <div style={{ marginBottom: '30px' }}>
              <h4 style={{ 
                margin: '0 0 15px 0', 
                color: '#1f2937',
                fontSize: '18px'
              }}>
                📋 Servicios Solicitados por el Cliente
              </h4>
              
              {presupuestoSeleccionado.servicios_solicitados?.map((servicio, index) => (
                <div key={index} style={{
                  backgroundColor: '#f0fdf4',
                  padding: '15px 20px',
                  borderRadius: '12px',
                  marginBottom: '10px',
                  border: '2px solid #10b981',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px'
                }}>
                  <span style={{ fontSize: '20px' }}>✅</span>
                  <span style={{ 
                    color: '#065f46', 
                    fontSize: '15px',
                    fontWeight: '500'
                  }}>
                    {servicio}
                  </span>
                </div>
              ))}
              
              <div style={{
                backgroundColor: '#e0f2fe',
                padding: '15px',
                borderRadius: '10px',
                marginTop: '15px',
                border: '1px solid #7dd3fc'
              }}>
                <p style={{ 
                  margin: 0, 
                  fontSize: '14px', 
                  color: '#0369a1',
                  textAlign: 'center'
                }}>
                  💬 El cliente está esperando tu oferta personalizada
                </p>
              </div>
            </div>

            {/* Modalidades de Pago - Crear Oferta */}
            <div style={{ marginBottom: '25px' }}>
              <h4 style={{ 
                margin: '0 0 15px 0', 
                color: '#1f2937',
                fontSize: '18px',
                borderTop: '1px solid #e5e7eb',
                paddingTop: '20px'
              }}>
                💳 Modalidades de Pago - Crea tu Oferta
              </h4>
              
              <p style={{ color: '#6b7280', marginBottom: '20px', fontSize: '14px' }}>
                Ingresa los precios para cada modalidad de pago. Todas son opcionales pero debes completar al menos una.
              </p>

              {/* Modalidad 1: Pago Inicial */}
              <div style={{
                backgroundColor: '#fef3c7',
                padding: '20px',
                borderRadius: '12px',
                marginBottom: '15px',
                border: '2px solid #f59e0b',
                transition: 'all 0.2s'
              }}>
                <div style={{ marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <span style={{ fontSize: '24px' }}>🚀</span>
                    <strong style={{ color: '#92400e', fontSize: '16px' }}>
                      Pago Inicial (Al Empezar el Proceso)
                    </strong>
                  </div>
                  <p style={{ 
                    color: '#78350f', 
                    fontSize: '13px', 
                    margin: '0 0 0 34px',
                    lineHeight: '1.4'
                  }}>
                    El cliente paga el monto completo al iniciar el proceso. Ideal para descuentos por pago anticipado.
                  </p>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginLeft: '34px' }}>
                  <span style={{ color: '#92400e', fontWeight: '600' }}>€</span>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={modalidades.precio_al_empezar}
                    onChange={(e) => setModalidades({...modalidades, precio_al_empezar: parseFloat(e.target.value) || ''})}
                    style={{
                      flex: 1,
                      padding: '12px',
                      border: '2px solid #fbbf24',
                      borderRadius: '8px',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}
                    placeholder="Ej: 1200.00"
                  />
                </div>
              </div>

              {/* Modalidad 2: Pago con Visa */}
              <div style={{
                backgroundColor: '#dbeafe',
                padding: '20px',
                borderRadius: '12px',
                marginBottom: '15px',
                border: '2px solid #3b82f6',
                transition: 'all 0.2s'
              }}>
                <div style={{ marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <span style={{ fontSize: '24px' }}>🎯</span>
                    <strong style={{ color: '#1e40af', fontSize: '16px' }}>
                      Pago una vez Obtenida la Visa
                    </strong>
                  </div>
                  <p style={{ 
                    color: '#1e40af', 
                    fontSize: '13px', 
                    margin: '0 0 0 34px',
                    lineHeight: '1.4'
                  }}>
                    El cliente paga cuando recibe la visa aprobada. Mayor precio por el riesgo asumido.
                  </p>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginLeft: '34px' }}>
                  <span style={{ color: '#1e40af', fontWeight: '600' }}>€</span>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={modalidades.precio_con_visa}
                    onChange={(e) => setModalidades({...modalidades, precio_con_visa: parseFloat(e.target.value) || ''})}
                    style={{
                      flex: 1,
                      padding: '12px',
                      border: '2px solid #60a5fa',
                      borderRadius: '8px',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}
                    placeholder="Ej: 1500.00"
                  />
                </div>
              </div>

              {/* Modalidad 3: Pago Financiado */}
              <div style={{
                backgroundColor: '#e0e7ff',
                padding: '20px',
                borderRadius: '12px',
                marginBottom: '15px',
                border: '2px solid #6366f1',
                transition: 'all 0.2s'
              }}>
                <div style={{ marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <span style={{ fontSize: '24px' }}>📅</span>
                    <strong style={{ color: '#4338ca', fontSize: '16px' }}>
                      Pago Financiado a 12 Meses
                    </strong>
                  </div>
                  <p style={{ 
                    color: '#4338ca', 
                    fontSize: '13px', 
                    margin: '0 0 0 34px',
                    lineHeight: '1.4'
                  }}>
                    El cliente paga en cuotas mensuales durante un año. Precio más alto por facilidades de pago.
                  </p>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginLeft: '34px' }}>
                  <span style={{ color: '#4338ca', fontWeight: '600' }}>€</span>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={modalidades.precio_financiado}
                    onChange={(e) => setModalidades({...modalidades, precio_financiado: parseFloat(e.target.value) || ''})}
                    style={{
                      flex: 1,
                      padding: '12px',
                      border: '2px solid #818cf8',
                      borderRadius: '8px',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}
                    placeholder="Ej: 1800.00"
                  />
                </div>
                {modalidades.precio_financiado && modalidades.precio_financiado > 0 && (
                  <div style={{ 
                    marginTop: '10px', 
                    marginLeft: '34px',
                    padding: '8px 12px',
                    backgroundColor: '#c7d2fe',
                    borderRadius: '6px'
                  }}>
                    <span style={{ color: '#3730a3', fontSize: '13px', fontWeight: '500' }}>
                      💰 Cuota mensual: €{(modalidades.precio_financiado / 12).toFixed(2)} x 12 meses
                    </span>
                  </div>
                )}
              </div>
            </div>

            {/* Comentarios Opcionales */}
            <div style={{ marginBottom: '25px' }}>
              <label style={{ 
                display: 'block', 
                marginBottom: '8px', 
                fontWeight: '600',
                color: '#374151'
              }}>
                💬 Comentarios Adicionales (Opcional)
              </label>
              <textarea
                value={modalidades.mensaje_admin}
                onChange={(e) => setModalidades({...modalidades, mensaje_admin: e.target.value})}
                rows="3"
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '14px',
                  fontFamily: 'inherit',
                  resize: 'vertical'
                }}
                placeholder="Incluye cualquier nota o aclaración para el cliente..."
              />
            </div>

            {/* Botones de Acción */}
            <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '25px' }}>
              <button
                onClick={() => {
                  setMostrarModal(false)
                  setModalidades({
                    precio_al_empezar: '',
                    precio_con_visa: '',
                    precio_financiado: '',
                    mensaje_admin: ''
                  })
                }}
                style={{
                  padding: '12px 24px',
                  backgroundColor: '#6b7280',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500'
                }}
              >
                ✖️ Cancelar
              </button>
              <button
                onClick={enviarOferta}
                disabled={!modalidades.precio_al_empezar && !modalidades.precio_con_visa && !modalidades.precio_financiado}
                style={{
                  padding: '12px 30px',
                  backgroundColor: (modalidades.precio_al_empezar || modalidades.precio_con_visa || modalidades.precio_financiado) ? '#10b981' : '#d1d5db',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: (modalidades.precio_al_empezar || modalidades.precio_con_visa || modalidades.precio_financiado) ? 'pointer' : 'not-allowed',
                  fontWeight: '600',
                  fontSize: '15px',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}
              >
                📤 Enviar Oferta al Cliente
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default PresupuestosAdmin