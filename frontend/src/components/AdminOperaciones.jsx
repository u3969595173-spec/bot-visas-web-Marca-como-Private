import React from 'react';
import './Platform.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const emptyForm = {
  nombre: '',
  tipo: '',
  categoria: '',
  estado: 'Activa',
  capital: '',
  comprometido: '',
  disponible: '',
  plazo: '',
  riesgo: 'Medio',
  rendimiento: '',
  descripcion: ''
};

function AdminOperaciones() {
  const [ops, setOps] = React.useState([]);
  const [form, setForm] = React.useState(emptyForm);
  const [editingId, setEditingId] = React.useState(null);
  const [solicitudes, setSolicitudes] = React.useState([]);
  const [mensaje, setMensaje] = React.useState('');

  const cargarOperaciones = async () => {
    try {
      const response = await fetch(`${API}/api/operaciones`);
      if (response.ok) {
        const data = await response.json();
        setOps(data.operaciones || []);
      }
    } catch (error) {
      console.log('Error cargando operaciones:', error);
    }
  };

  const cargarSolicitudes = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API}/api/solicitudes-participacion`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setSolicitudes(data.solicitudes || []);
      }
    } catch (error) {
      console.log('Error cargando solicitudes:', error);
    }
  };

  React.useEffect(() => {
    cargarOperaciones();
    cargarSolicitudes();
    const intervalo = setInterval(() => {
      cargarOperaciones();
      cargarSolicitudes();
    }, 10000);
    return () => clearInterval(intervalo);
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const resetForm = () => {
    setForm(emptyForm);
    setEditingId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.nombre.trim() || !form.capital.trim()) {
      alert('Completa al menos nombre y capital de la operación');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      if (editingId !== null) {
        const response = await fetch(`${API}/api/operaciones/${editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify(form)
        });
        if (!response.ok) throw new Error('Error al guardar cambios');
        setMensaje('✅ Operación actualizada');
      } else {
        const response = await fetch(`${API}/api/operaciones`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify(form)
        });
        if (!response.ok) throw new Error('Error al crear la operación');
        setMensaje('✅ Operación creada');
      }
      await cargarOperaciones();
      resetForm();
    } catch (error) {
      alert(error.message);
    }
    setTimeout(() => setMensaje(''), 2000);
  };

  const handleEdit = (op) => {
    setEditingId(op.id);
    setForm({
      nombre: op.nombre,
      tipo: op.tipo,
      categoria: op.categoria,
      estado: op.estado,
      capital: op.capital,
      comprometido: op.comprometido,
      disponible: op.disponible,
      plazo: op.plazo,
      riesgo: op.riesgo,
      rendimiento: op.rendimiento,
      descripcion: op.descripcion
    });
  };

  const toggleEstado = async (op) => {
    const next = op.estado === 'Activa' ? 'Pendiente' : op.estado === 'Pendiente' ? 'Cerrada' : 'Activa';
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API}/api/operaciones/${op.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ estado: next })
      });
      if (response.ok) {
        setOps((current) => current.map((item) => item.id === op.id ? { ...item, estado: next } : item));
      }
    } catch (error) {
      console.log('Error actualizando estado:', error);
    }
  };

  const totalCapital = ops.reduce((sum, op) => sum + Number((op.capital || '0').replace(/[^0-9]/g, '')), 0);
  const totalComprometido = ops.reduce((sum, op) => sum + Number((op.comprometido || '0').replace(/[^0-9]/g, '')), 0);
  const activos = ops.filter((op) => op.estado === 'Activa').length;

  const actualizarEstadoSolicitud = async (id, nuevoEstado) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API}/api/solicitudes-participacion/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ estado: nuevoEstado })
      });
      if (response.ok) {
        setSolicitudes((current) => current.map((s) => s.id === id ? { ...s, estado: nuevoEstado } : s));
      }
    } catch (error) {
      console.log('Error actualizando solicitud:', error);
    }
  };

  return (
    <div className="platform-page">
      <div className="platform-card">
        <div className="platform-header">
          <div>
            <p className="section-label">Administración</p>
            <h1>Operaciones</h1>
          </div>
          <div className="platform-actions">
            {mensaje && <span style={{ marginRight: '1rem', color: '#10b981', fontWeight: 600 }}>{mensaje}</span>}
            <button className="ghost-btn" onClick={resetForm}>Nueva operación</button>
          </div>
        </div>

        <div className="summary-grid">
          <div className="stat-box">
            <span>Operaciones activas</span>
            <strong>{activos}</strong>
          </div>
          <div className="stat-box">
            <span>Capital total</span>
            <strong>€{totalCapital.toLocaleString('es-ES')}</strong>
          </div>
          <div className="stat-box">
            <span>Comprometido</span>
            <strong>€{totalComprometido.toLocaleString('es-ES')}</strong>
          </div>
          <div className="stat-box">
            <span>Estado del portafolio</span>
            <strong>{Math.min(100, Math.round((activos / Math.max(ops.length, 1)) * 100))}%</strong>
          </div>
        </div>

        <div className="admin-grid">
          <form className="admin-form" onSubmit={handleSubmit}>
            <h3>{editingId ? 'Editar operación' : 'Ficha de operación'}</h3>
            <div className="form-grid">
              <div><label>Nombre</label><input name="nombre" value={form.nombre} onChange={handleChange} placeholder="Ej. Compra de cementos" /></div>
              <div><label>Tipo</label><input name="tipo" value={form.tipo} onChange={handleChange} placeholder="Ej. Material de construcción" /></div>
              <div><label>Categoría</label><input name="categoria" value={form.categoria} onChange={handleChange} placeholder="Ej. Infraestructura" /></div>
              <div><label>Estado</label>
                <select name="estado" value={form.estado} onChange={handleChange}>
                  <option>Activa</option>
                  <option>Pendiente</option>
                  <option>Cerrada</option>
                </select>
              </div>
              <div><label>Capital</label><input name="capital" value={form.capital} onChange={handleChange} placeholder="€80.000" /></div>
              <div><label>Comprometido</label><input name="comprometido" value={form.comprometido} onChange={handleChange} placeholder="€48.000" /></div>
              <div><label>Disponible</label><input name="disponible" value={form.disponible} onChange={handleChange} placeholder="€32.000" /></div>
              <div><label>Plazo</label><input name="plazo" value={form.plazo} onChange={handleChange} placeholder="6-10 meses" /></div>
              <div><label>Riesgo</label>
                <select name="riesgo" value={form.riesgo} onChange={handleChange}>
                  <option>Medio</option>
                  <option>Medio-alto</option>
                  <option>Variable</option>
                </select>
              </div>
              <div className="full-width"><label>Rendimiento</label><input name="rendimiento" value={form.rendimiento} onChange={handleChange} placeholder="Resultado según cierre comercial" /></div>
              <div className="full-width"><label>Descripción</label><textarea name="descripcion" value={form.descripcion} onChange={handleChange} rows="4" placeholder="Describe la operación y su estructura comercial" /></div>
            </div>
            <div className="form-actions">
              <button type="submit" className="primary-btn">{editingId ? 'Guardar cambios' : 'Crear operación'}</button>
              {editingId && <button type="button" className="secondary-btn" onClick={resetForm}>Cancelar</button>}
            </div>
          </form>

          <div className="table-wrapper">
            <h3>Listado</h3>
            <table>
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Estado</th>
                  <th>Capital</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {ops.map((op) => (
                  <tr key={op.id}>
                    <td>{op.nombre}</td>
                    <td><span className={`status-badge ${op.estado === 'Activa' ? 'active' : op.estado === 'Pendiente' ? 'pending' : 'closed'}`}>{op.estado}</span></td>
                    <td>{op.capital}</td>
                    <td className="tab-actions">
                      <button className="inline-btn" onClick={() => handleEdit(op)}>Editar</button>
                      <button className="inline-btn" onClick={() => toggleEstado(op)}>Estado</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="table-wrapper" style={{ marginTop: '1.5rem' }}>
          <h3>Solicitudes de participación</h3>
          {solicitudes.length === 0 ? (
            <p>No hay solicitudes de participación pendientes.</p>
          ) : (
            <div className="admin-requests-list">
              {solicitudes.map((solicitud) => (
                <div className="admin-request-item" key={solicitud.id}>
                  <div className="admin-request-item-head">
                    <strong>{solicitud.nombre || 'Usuario'}</strong>
                    <span className={`status-badge ${solicitud.estado === 'Pendiente' ? 'pending' : solicitud.estado === 'Aprobada' ? 'active' : 'closed'}`}>
                      {solicitud.estado || 'Pendiente'}
                    </span>
                  </div>
                  <p><strong>Contacto:</strong> {solicitud.email} · {solicitud.telefono} · {solicitud.pais}</p>
                  <p><strong>Importe:</strong> {Number(solicitud.importe || 0).toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} {solicitud.moneda}</p>
                  <div style={{ marginTop: '0.75rem' }}>
                    <label>Estado</label>
                    <select
                      value={solicitud.estado || 'Pendiente'}
                      onChange={(e) => actualizarEstadoSolicitud(solicitud.id, e.target.value)}
                    >
                      <option>Pendiente</option>
                      <option>Revisada</option>
                      <option>Aprobada</option>
                      <option>Rechazada</option>
                    </select>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminOperaciones;
