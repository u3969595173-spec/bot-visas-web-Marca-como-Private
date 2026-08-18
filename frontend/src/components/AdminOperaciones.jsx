import React from 'react';
import './Platform.css';

const initialOperations = [
  {
    id: 1,
    nombre: 'Compra y exportación de cemento',
    tipo: 'Material de construcción',
    categoria: 'Infraestructura',
    estado: 'Activa',
    capital: '€80.000',
    comprometido: '€48.000',
    disponible: '€32.000',
    plazo: '6-10 meses',
    riesgo: 'Medio',
    rendimiento: 'Variable según cierre comercial y estructura',
    descripcion: 'Compra de cemento para distribución y exportación con estructura de participación por tramo.'
  },
  {
    id: 2,
    nombre: 'Paneles para construcción',
    tipo: 'Construcción',
    categoria: 'Materiales de edificación',
    estado: 'Pendiente',
    capital: '€95.000',
    comprometido: '€36.000',
    disponible: '€59.000',
    plazo: '7-12 meses',
    riesgo: 'Medio-alto',
    rendimiento: 'A definir según condiciones finales de la operación',
    descripcion: 'Operación en análisis para abastecer logística y distribución de paneles hacia destino final.'
  },
  {
    id: 3,
    nombre: 'Materiales de construcción',
    tipo: 'Insumos',
    categoria: 'Abastecimiento',
    estado: 'Cerrada',
    capital: '€60.000',
    comprometido: '€60.000',
    disponible: '€0',
    plazo: '4-9 meses',
    riesgo: 'Variable',
    rendimiento: 'Resultado final según cierre comercial',
    descripcion: 'Cierre de operación con seguimiento documental finalizado.'
  }
];

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
  const [ops, setOps] = React.useState(initialOperations);
  const [form, setForm] = React.useState(emptyForm);
  const [editingId, setEditingId] = React.useState(null);
  const [solicitudes, setSolicitudes] = React.useState([]);

  React.useEffect(() => {
    const stored = JSON.parse(localStorage.getItem('solicitudes_participacion') || '[]');
    setSolicitudes(stored);
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const resetForm = () => {
    setForm(emptyForm);
    setEditingId(null);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!form.nombre.trim() || !form.capital.trim()) {
      alert('Completa al menos nombre y capital de la operación');
      return;
    }

    if (editingId !== null) {
      setOps((current) => current.map((op) => op.id === editingId ? { ...op, ...form } : op));
    } else {
      const newOp = {
        id: Date.now(),
        ...form
      };
      setOps((current) => [newOp, ...current]);
    }

    resetForm();
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

  const toggleEstado = (id) => {
    setOps((current) => current.map((op) => {
      if (op.id !== id) return op;
      const next = op.estado === 'Activa' ? 'Pendiente' : op.estado === 'Pendiente' ? 'Cerrada' : 'Activa';
      return { ...op, estado: next };
    }));
  };

  const totalCapital = ops.reduce((sum, op) => sum + Number((op.capital || '0').replace(/[^0-9]/g, '')), 0);
  const totalComprometido = ops.reduce((sum, op) => sum + Number((op.comprometido || '0').replace(/[^0-9]/g, '')), 0);
  const activos = ops.filter((op) => op.estado === 'Activa').length;

  const actualizarEstadoSolicitud = (id, nuevoEstado) => {
    const updated = solicitudes.map((solicitud) =>
      solicitud.id === id ? { ...solicitud, estado: nuevoEstado } : solicitud
    );
    setSolicitudes(updated);
    localStorage.setItem('solicitudes_participacion', JSON.stringify(updated));
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
                      <button className="inline-btn" onClick={() => toggleEstado(op.id)}>Estado</button>
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
                    <strong>{solicitud.usuarioNombre || 'Usuario'}</strong>
                    <span className={`status-badge ${solicitud.estado === 'Pendiente' ? 'pending' : solicitud.estado === 'Aprobada' ? 'active' : 'closed'}`}>
                      {solicitud.estado || 'Pendiente'}
                    </span>
                  </div>
                  <p><strong>Operación:</strong> {solicitud.operacionNombre}</p>
                  <p><strong>Importe:</strong> €{Number(solicitud.importe || 0).toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                  {solicitud.comentario && <p><strong>Comentario:</strong> {solicitud.comentario}</p>}
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
