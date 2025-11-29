import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './AdminServicios.css'

function AdminServicios() {
  const [servicios, setServicios] = useState([])
  const [loading, setLoading] = useState(true)

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  const token = localStorage.getItem('token')

  useEffect(() => {
    cargarServicios()
  }, [])

  const cargarServicios = async () => {
    try {
      const res = await axios.get(`${apiUrl}/api/admin/servicios-solicitados`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setServicios(res.data.servicios || [])
    } catch (err) {
      console.error('Error cargando servicios:', err)
      alert('Error cargando servicios solicitados')
    } finally {
      setLoading(false)
    }
  }

  const limpiarTodosLosPresupuestos = async () => {
    if (!confirm('⚠️ ¿ELIMINAR TODOS los presupuestos aceptados del panel?\n\nEsto borrará TODO el seguimiento actual.\nÚsalo solo para empezar de cero con pruebas.\n\n¿Continuar?')) {
      return
    }

    try {
      const res = await axios.delete(`${apiUrl}/api/admin/presupuestos/limpiar-aceptados`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      alert(`✅ ${res.data.message}`)
      cargarServicios()
    } catch (err) {
      console.error('Error limpiando presupuestos:', err)
      alert('❌ Error al limpiar presupuestos: ' + (err.response?.data?.detail || err.message))
    }
  }

  const serviciosPorEstado = {
    pendiente: servicios.filter(s => s.estado === 'pendiente'),
    en_proceso: servicios.filter(s => s.estado === 'en_proceso'),
    completado: servicios.filter(s => s.estado === 'completado')
  }

  if (loading) {
    return <div className="admin-servicios-loading">Cargando solicitudes...</div>
  }

  return (
    <div className="admin-servicios">
      <div className="admin-servicios-header">
        <h2>💼 Servicios Solicitados por Estudiantes</h2>
        <button
          onClick={limpiarTodosLosPresupuestos}
          style={{
            padding: '10px 20px',
            backgroundColor: '#ef4444',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
          onMouseEnter={(e) => e.target.style.backgroundColor = '#dc2626'}
          onMouseLeave={(e) => e.target.style.backgroundColor = '#ef4444'}
        >
          🗑️ Limpiar Panel (Pruebas)
        </button>
      </div>
      
      <div className="servicios-stats">
        <div className="stat-card pendiente">
          <div className="stat-numero">{serviciosPorEstado.pendiente.length}</div>
          <div className="stat-label">Pendientes</div>
        </div>
        <div className="stat-card proceso">
          <div className="stat-numero">{serviciosPorEstado.en_proceso.length}</div>
          <div className="stat-label">En Proceso</div>
        </div>
        <div className="stat-card completado">
          <div className="stat-numero">{serviciosPorEstado.completado.length}</div>
          <div className="stat-label">Completados</div>
        </div>
      </div>
    </div>
  )
}

export default AdminServicios
