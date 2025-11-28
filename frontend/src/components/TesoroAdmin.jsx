import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function TesoroAdmin() {
  const [pagos, setPagos] = useState([])
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
      setPagos(response.data)
      setError('')
    } catch (err) {
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
    const modalidades = {
      'precio_al_empezar': '💳 Pago al Empezar',
      'precio_con_visa': '🎯 Pago con Visa',
      'precio_financiado': '📅 Pago Financiado'
    }
    return modalidades[modalidad] || modalidad
  }

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
            €{pagos.filter(p => !p.pagado).reduce((sum, p) => sum + p.monto_total, 0).toFixed(2)}
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
                    Modalidad
                  </th>
                  <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                    Monto
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
                          {pago.estudiante_nombre}
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
                      <span style={{
                        fontSize: '12px',
                        padding: '4px 8px',
                        borderRadius: '4px',
                        backgroundColor: '#e0f2fe',
                        color: '#0369a1'
                      }}>
                        {formatearModalidad(pago.modalidad_seleccionada)}
                      </span>
                    </td>
                    <td style={{ padding: '12px' }}>
                      <div style={{ fontWeight: '600', color: '#059669' }}>
                        €{pago.monto_total.toFixed(2)}
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
                      {!pago.pagado && (
                        <button
                          onClick={() => marcarComoPagado(pago.presupuesto_id)}
                          style={{
                            padding: '6px 12px',
                            backgroundColor: '#10b981',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            fontSize: '12px',
                            cursor: 'pointer'
                          }}
                        >
                          💳 Marcar Pagado
                        </button>
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