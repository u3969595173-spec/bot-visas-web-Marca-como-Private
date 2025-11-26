import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PartnersAdmin.css';

function PartnersAdmin() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [universidades, setUniversidades] = useState([]);
  const [comisiones, setComisiones] = useState([]);
  const [dashboardStats, setDashboardStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editingUniversidad, setEditingUniversidad] = useState(null);
  const [formData, setFormData] = useState({
    nombre: '',
    codigo_referido: '',
    email_contacto: '',
    persona_contacto: '',
    telefono: '',
    tipo_comision: 'porcentaje',
    porcentaje_comision: 15,
    monto_fijo_comision: 0,
    logo_url: '',
    notas: '',
    activo: true
  });

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    cargarDatos();
  }, [activeTab]);

  const cargarDatos = async () => {
    setLoading(true);
    try {
      if (activeTab === 'dashboard') {
        const res = await axios.get(`${apiUrl}/api/admin/partners/dashboard`);
        setDashboardStats(res.data);
      } else if (activeTab === 'universidades') {
        const res = await axios.get(`${apiUrl}/api/admin/partners/universidades`);
        setUniversidades(res.data.universidades);
      } else if (activeTab === 'comisiones') {
        const res = await axios.get(`${apiUrl}/api/admin/partners/comisiones`);
        setComisiones(res.data.comisiones);
      }
    } catch (err) {
      console.error('Error cargando datos:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingUniversidad) {
        await axios.put(
          `${apiUrl}/api/admin/partners/universidades/${editingUniversidad.id}`,
          formData
        );
      } else {
        await axios.post(`${apiUrl}/api/admin/partners/universidades`, formData);
      }
      setShowModal(false);
      setEditingUniversidad(null);
      resetForm();
      cargarDatos();
    } catch (err) {
      alert('Error al guardar: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleEdit = (universidad) => {
    setEditingUniversidad(universidad);
    setFormData({
      nombre: universidad.nombre,
      codigo_referido: universidad.codigo_referido,
      email_contacto: universidad.email_contacto || '',
      persona_contacto: universidad.persona_contacto || '',
      telefono: universidad.telefono || '',
      tipo_comision: universidad.tipo_comision,
      porcentaje_comision: universidad.porcentaje_comision,
      monto_fijo_comision: universidad.monto_fijo_comision,
      logo_url: universidad.logo_url || '',
      notas: universidad.notas || '',
      activo: universidad.activo
    });
    setShowModal(true);
  };

  const resetForm = () => {
    setFormData({
      nombre: '',
      codigo_referido: '',
      email_contacto: '',
      persona_contacto: '',
      telefono: '',
      tipo_comision: 'porcentaje',
      porcentaje_comision: 15,
      monto_fijo_comision: 0,
      logo_url: '',
      notas: '',
      activo: true
    });
  };

  const marcarComoPagada = async (comisionId) => {
    if (!confirm('¿Marcar comisión como pagada?')) return;
    try {
      await axios.put(`${apiUrl}/api/admin/partners/comisiones/${comisionId}/marcar-pagado`);
      cargarDatos();
    } catch (err) {
      alert('Error: ' + (err.response?.data?.detail || err.message));
    }
  };

  const copiarLink = (codigo) => {
    const link = `${window.location.origin}/registro?ref=${codigo}`;
    navigator.clipboard.writeText(link);
    alert('Link copiado: ' + link);
  };

  return (
    <div className="partners-admin">
      <div className="partners-header">
        <h1>🤝 Partnerships Universitarios</h1>
        <p>Gestión de alianzas con universidades y escuelas</p>
      </div>

      {/* Tabs */}
      <div className="partners-tabs">
        <button
          className={activeTab === 'dashboard' ? 'active' : ''}
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Dashboard
        </button>
        <button
          className={activeTab === 'universidades' ? 'active' : ''}
          onClick={() => setActiveTab('universidades')}
        >
          🏫 Universidades
        </button>
        <button
          className={activeTab === 'comisiones' ? 'active' : ''}
          onClick={() => setActiveTab('comisiones')}
        >
          💰 Comisiones
        </button>
      </div>

      {/* Dashboard Tab */}
      {activeTab === 'dashboard' && dashboardStats && (
        <div className="dashboard-content">
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">🏫</div>
              <div className="stat-value">{dashboardStats.stats.total_universidades}</div>
              <div className="stat-label">Universidades Partner</div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">👥</div>
              <div className="stat-value">{dashboardStats.stats.total_referidos}</div>
              <div className="stat-label">Estudiantes Referidos</div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">✅</div>
              <div className="stat-value">{dashboardStats.stats.total_matriculados}</div>
              <div className="stat-label">Matriculados</div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">📈</div>
              <div className="stat-value">{dashboardStats.stats.tasa_conversion}%</div>
              <div className="stat-label">Tasa Conversión</div>
            </div>
            <div className="stat-card highlight">
              <div className="stat-icon">⏳</div>
              <div className="stat-value">€{dashboardStats.stats.comisiones_pendientes.toLocaleString()}</div>
              <div className="stat-label">Comisiones Pendientes</div>
            </div>
            <div className="stat-card success">
              <div className="stat-icon">💵</div>
              <div className="stat-value">€{dashboardStats.stats.comisiones_pagadas.toLocaleString()}</div>
              <div className="stat-label">Comisiones Pagadas</div>
            </div>
          </div>

          <div className="top-partners">
            <h3>🏆 Top 5 Universidades</h3>
            <table className="partners-table">
              <thead>
                <tr>
                  <th>Universidad</th>
                  <th>Referidos</th>
                  <th>Comisiones</th>
                </tr>
              </thead>
              <tbody>
                {dashboardStats.top_universidades.map((uni, idx) => (
                  <tr key={idx}>
                    <td>{uni.nombre}</td>
                    <td>{uni.total_referidos}</td>
                    <td>€{uni.total_comisiones.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Universidades Tab */}
      {activeTab === 'universidades' && (
        <div className="universidades-content">
          <div className="content-header">
            <h2>Universidades Partner ({universidades.length})</h2>
            <button
              className="btn-primary"
              onClick={() => {
                setEditingUniversidad(null);
                resetForm();
                setShowModal(true);
              }}
            >
              ➕ Nueva Universidad
            </button>
          </div>

          <div className="universidades-grid">
            {universidades.map((uni) => (
              <div key={uni.id} className="universidad-card">
                <div className="universidad-header">
                  <h3>{uni.nombre}</h3>
                  <span className={`badge ${uni.activo ? 'badge-success' : 'badge-danger'}`}>
                    {uni.activo ? 'Activo' : 'Inactivo'}
                  </span>
                </div>

                <div className="universidad-info">
                  <div className="info-row">
                    <strong>Código:</strong> {uni.codigo_referido}
                    <button
                      className="btn-copy"
                      onClick={() => copiarLink(uni.codigo_referido)}
                      title="Copiar link de referido"
                    >
                      📋
                    </button>
                  </div>
                  <div className="info-row">
                    <strong>Contacto:</strong> {uni.persona_contacto || 'N/A'}
                  </div>
                  <div className="info-row">
                    <strong>Email:</strong> {uni.email_contacto || 'N/A'}
                  </div>
                  <div className="info-row">
                    <strong>Comisión:</strong>{' '}
                    {uni.tipo_comision === 'porcentaje'
                      ? `${uni.porcentaje_comision}%`
                      : `€${uni.monto_fijo_comision}`}
                  </div>
                </div>

                <div className="universidad-stats">
                  <div className="stat-item">
                    <span className="stat-number">{uni.stats.total_referidos}</span>
                    <span className="stat-text">Referidos</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-number">{uni.stats.matriculados}</span>
                    <span className="stat-text">Matriculados</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-number">{uni.stats.tasa_conversion}%</span>
                    <span className="stat-text">Conversión</span>
                  </div>
                </div>

                <div className="universidad-footer">
                  <button className="btn-secondary" onClick={() => handleEdit(uni)}>
                    ✏️ Editar
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Comisiones Tab */}
      {activeTab === 'comisiones' && (
        <div className="comisiones-content">
          <div className="content-header">
            <h2>Comisiones ({comisiones.length})</h2>
          </div>

          <table className="comisiones-table">
            <thead>
              <tr>
                <th>Universidad</th>
                <th>Estudiante</th>
                <th>Monto Curso</th>
                <th>Comisión</th>
                <th>Estado</th>
                <th>Fecha Matrícula</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {comisiones.map((com) => (
                <tr key={com.id}>
                  <td>{com.universidad}</td>
                  <td>{com.estudiante}</td>
                  <td>€{com.monto_curso.toLocaleString()}</td>
                  <td>
                    <strong>€{com.monto_comision.toLocaleString()}</strong>
                  </td>
                  <td>
                    <span
                      className={`badge ${
                        com.estado === 'pagado' ? 'badge-success' : 'badge-warning'
                      }`}
                    >
                      {com.estado === 'pagado' ? 'Pagado' : 'Pendiente'}
                    </span>
                  </td>
                  <td>
                    {com.fecha_matricula
                      ? new Date(com.fecha_matricula).toLocaleDateString()
                      : 'N/A'}
                  </td>
                  <td>
                    {com.estado === 'pendiente' && (
                      <button
                        className="btn-success-small"
                        onClick={() => marcarComoPagada(com.id)}
                      >
                        ✓ Marcar Pagado
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal Crear/Editar Universidad */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingUniversidad ? 'Editar Universidad' : 'Nueva Universidad'}</h2>
              <button className="modal-close" onClick={() => setShowModal(false)}>
                ✕
              </button>
            </div>

            <form onSubmit={handleSubmit} className="universidad-form">
              <div className="form-group">
                <label>Nombre de la Universidad *</label>
                <input
                  type="text"
                  value={formData.nombre}
                  onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Código de Referido * (sin espacios, minúsculas)</label>
                <input
                  type="text"
                  value={formData.codigo_referido}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      codigo_referido: e.target.value.toLowerCase().replace(/\s/g, ''),
                    })
                  }
                  placeholder="ej: nebrija2024"
                  required
                  disabled={!!editingUniversidad}
                />
                {formData.codigo_referido && (
                  <small>
                    Link: {window.location.origin}/registro?ref={formData.codigo_referido}
                  </small>
                )}
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Persona de Contacto</label>
                  <input
                    type="text"
                    value={formData.persona_contacto}
                    onChange={(e) =>
                      setFormData({ ...formData, persona_contacto: e.target.value })
                    }
                  />
                </div>

                <div className="form-group">
                  <label>Email Contacto</label>
                  <input
                    type="email"
                    value={formData.email_contacto}
                    onChange={(e) =>
                      setFormData({ ...formData, email_contacto: e.target.value })
                    }
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Teléfono</label>
                <input
                  type="tel"
                  value={formData.telefono}
                  onChange={(e) => setFormData({ ...formData, telefono: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label>Tipo de Comisión</label>
                <select
                  value={formData.tipo_comision}
                  onChange={(e) => setFormData({ ...formData, tipo_comision: e.target.value })}
                >
                  <option value="porcentaje">Porcentaje del Curso</option>
                  <option value="fijo">Monto Fijo</option>
                </select>
              </div>

              {formData.tipo_comision === 'porcentaje' ? (
                <div className="form-group">
                  <label>Porcentaje de Comisión (%)</label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    step="0.5"
                    value={formData.porcentaje_comision}
                    onChange={(e) =>
                      setFormData({ ...formData, porcentaje_comision: parseFloat(e.target.value) })
                    }
                  />
                </div>
              ) : (
                <div className="form-group">
                  <label>Monto Fijo (€)</label>
                  <input
                    type="number"
                    min="0"
                    step="0.01"
                    value={formData.monto_fijo_comision}
                    onChange={(e) =>
                      setFormData({ ...formData, monto_fijo_comision: parseFloat(e.target.value) })
                    }
                  />
                </div>
              )}

              <div className="form-group">
                <label>URL del Logo</label>
                <input
                  type="url"
                  value={formData.logo_url}
                  onChange={(e) => setFormData({ ...formData, logo_url: e.target.value })}
                  placeholder="https://ejemplo.com/logo.png"
                />
              </div>

              <div className="form-group">
                <label>Notas</label>
                <textarea
                  value={formData.notas}
                  onChange={(e) => setFormData({ ...formData, notas: e.target.value })}
                  rows="3"
                />
              </div>

              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={formData.activo}
                    onChange={(e) => setFormData({ ...formData, activo: e.target.checked })}
                  />
                  Universidad Activa
                </label>
              </div>

              <div className="form-actions">
                <button type="button" className="btn-secondary" onClick={() => setShowModal(false)}>
                  Cancelar
                </button>
                <button type="submit" className="btn-primary">
                  {editingUniversidad ? 'Actualizar' : 'Crear'} Universidad
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default PartnersAdmin;
