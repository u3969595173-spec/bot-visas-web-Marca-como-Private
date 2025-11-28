import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function PresupuestosAdmin() {
  const [presupuestos, setPresupuestos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [presupuestoSeleccionado, setPresupuestoSeleccionado] = useState(null)
  const [mostrarModal, setMostrarModal] = useState(false)
  const [modalidades, setModalidades] = useState({
    precio_al_empezar: '',
    precio_con_visa: '',
    precio_financiado: '',
    comentarios_admin: ''
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
      comentarios_admin: ''
    })
    setMostrarModal(true)
  }

  const enviarOferta = async () => {
    if (!presupuestoSeleccionado) return

    // Validación
    if (!modalidades.precio_al_empezar || !modalidades.precio_con_visa || !modalidades.precio_financiado) {
      setError('Por favor completa todos los precios')
      return
    }

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      await axios.put(`${apiUrl}/api/admin/presupuestos/${presupuestoSeleccionado.id}/ofertar-modalidades`, modalidades)
      setSuccess('✅ Oferta enviada exitosamente')
      setMostrarModal(false)
      cargarPresupuestos()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Error al enviar oferta: ' + (err.response?.data?.detail || err.message))
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
        <button
          onClick={() => navigate('/admin')}
          className="btn"
          style={{ background: 'white', color: '#667eea' }}
        >
          ← Volver al Dashboard
        </button>
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
            {presupuestos.filter(p => p.estado === 'oferta_enviada').length}
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
                          {presupuesto.estudiante_nombre}
                        </div>
                        <div style={{ fontSize: '12px', color: '#718096' }}>
                          ID: {presupuesto.id}
                        </div>
                      </div>
                    </td>
                    <td style={{ padding: '12px' }}>
                      <div style={{ fontSize: '12px', color: '#4a5568' }}>
                        {presupuesto.servicios_solicitados?.slice(0, 2).join(', ')}
                        {presupuesto.servicios_solicitados?.length > 2 && '...'}
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
                      {presupuesto.estado === 'aceptado' && (
                        <span style={{ fontSize: '12px', color: '#059669' }}>
                          €{presupuesto.monto_total?.toFixed(2)}
                        </span>
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
          zIndex: 1000
        }}>
          <div style={{
            backgroundColor: 'white',
            padding: '30px',
            borderRadius: '15px',
            maxWidth: '600px',
            width: '90%',
            maxHeight: '90%',
            overflowY: 'auto'
          }}>
            <h3 style={{ marginTop: 0, marginBottom: '20px', color: '#2d3748' }}>
              💰 Crear Oferta para {presupuestoSeleccionado.estudiante_nombre}
            </h3>

            <div style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f8fafc', borderRadius: '8px' }}>
              <h4 style={{ margin: '0 0 10px 0', color: '#4a5568' }}>Servicios Solicitados:</h4>
              <ul style={{ margin: 0, paddingLeft: '20px' }}>
                {presupuestoSeleccionado.servicios_solicitados?.map((servicio, index) => (
                  <li key={index} style={{ color: '#2d3748' }}>{servicio}</li>
                ))}
              </ul>
            </div>

            <div style={{ display: 'grid', gap: '15px' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: '600' }}>
                  💳 Precio al Empezar (€)
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={modalidades.precio_al_empezar}
                  onChange={(e) => setModalidades({...modalidades, precio_al_empezar: parseFloat(e.target.value) || ''})}
                  style={{
                    width: '100%',
                    padding: '10px',
                    border: '1px solid #d1d5db',
                    borderRadius: '5px'
                  }}
                  placeholder="Ej: 1200.00"
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: '600' }}>
                  🎯 Precio con Visa (€)
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={modalidades.precio_con_visa}
                  onChange={(e) => setModalidades({...modalidades, precio_con_visa: parseFloat(e.target.value) || ''})}
                  style={{
                    width: '100%',
                    padding: '10px',
                    border: '1px solid #d1d5db',
                    borderRadius: '5px'
                  }}
                  placeholder="Ej: 1350.00"
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: '600' }}>
                  📅 Precio Financiado (€)
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={modalidades.precio_financiado}
                  onChange={(e) => setModalidades({...modalidades, precio_financiado: parseFloat(e.target.value) || ''})}
                  style={{
                    width: '100%',
                    padding: '10px',
                    border: '1px solid #d1d5db',
                    borderRadius: '5px'
                  }}
                  placeholder="Ej: 1500.00"
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: '600' }}>
                  💬 Comentarios Adicionales
                </label>
                <textarea
                  value={modalidades.comentarios_admin}
                  onChange={(e) => setModalidades({...modalidades, comentarios_admin: e.target.value})}
                  style={{
                    width: '100%',
                    padding: '10px',
                    border: '1px solid #d1d5db',
                    borderRadius: '5px',
                    minHeight: '80px',
                    resize: 'vertical'
                  }}
                  placeholder="Detalles adicionales sobre la oferta..."
                />
              </div>
            </div>

            <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '25px' }}>
              <button
                onClick={() => setMostrarModal(false)}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#6b7280',
                  color: 'white',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer'
                }}
              >
                Cancelar
              </button>
              <button
                onClick={enviarOferta}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#10b981',
                  color: 'white',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  fontWeight: '600'
                }}
              >
                📤 Enviar Oferta
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default PresupuestosAdmin