import React from 'react';
import { useParams, Link } from 'react-router-dom';
import './Platform.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const OPERACION_VACIA = {
  nombre: 'Cargando…',
  tipo: '',
  capitalNecesario: '—',
  capitalDisponible: '—',
  capitalPendiente: '—',
  plazo: '—',
  inicio: 'Por definir',
  finEst: 'Por definir',
  estado: 'Activa',
  rendimiento: '—',
  riesgo: '—',
  descripcion: '',
  condiciones: []
};

function formatearEuros(valor) {
  return `€${Number(valor || 0).toLocaleString('es-ES')}`;
}

function adaptarOperacion(op) {
  const parseNumero = (str) => Number(String(str || '0').replace(/[^0-9]/g, '')) || 0;
  const pendiente = Math.max(0, parseNumero(op.capital) - parseNumero(op.disponible));
  return {
    id: op.id,
    nombre: op.nombre,
    tipo: op.tipo,
    capitalNecesario: op.capital,
    capitalDisponible: op.disponible,
    capitalPendiente: formatearEuros(pendiente),
    plazo: op.plazo,
    inicio: op.fechaInicio || 'Por definir',
    finEst: op.fechaFinEstimada || 'Por definir',
    estado: op.estado,
    rendimiento: op.rendimiento,
    riesgo: op.riesgo,
    descripcion: op.descripcion,
    condiciones: op.condiciones && op.condiciones.length ? op.condiciones : []
  };
}

function OperacionDetalle() {
  const { id } = useParams();
  const [op, setOp] = React.useState(OPERACION_VACIA);

  React.useEffect(() => {
    fetch(`${API}/api/operaciones`)
      .then((res) => res.json())
      .then((data) => {
        const encontrada = (data.operaciones || []).find((item) => String(item.id) === String(id));
        if (encontrada) setOp(adaptarOperacion(encontrada));
      })
      .catch(() => { });
  }, [id]);

  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [form, setForm] = React.useState({
    importe: '',
    moneda: 'EUR',
    metodoPago: 'transferencia',
    cuentaDestino: 'ES91 2100 0418 4502 0005 1332',
    comentario: '',
    justificante: null
  });
  const [error, setError] = React.useState('');
  const [success, setSuccess] = React.useState('');
  const [authPrompt, setAuthPrompt] = React.useState(false);
  const fileInputRef = React.useRef(null);

  const parseCapital = (value) => {
    if (!value) return 0;
    const normalized = String(value).replace(/€/g, '').replace(/\s/g, '').replace('.', '').replace(',', '.');
    const parsed = Number(normalized);
    return Number.isFinite(parsed) ? parsed : 0;
  };

  const capitalDisponible = parseCapital(op.capitalDisponible);

  const openRequestModal = () => {
    const storedUser = JSON.parse(localStorage.getItem('capital_trade_user') || 'null');
    const userId = storedUser?.id || localStorage.getItem('estudiante_id');
    if (!userId) {
      setAuthPrompt(true);
      setIsModalOpen(true);
      return;
    }

    setAuthPrompt(false);
    setSuccess('');
    setError('');
    setForm({ importe: '', comentario: '' });
    setIsModalOpen(true);
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) {
      setForm((prev) => ({ ...prev, justificante: null }));
      return;
    }

    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
    if (!allowedTypes.includes(file.type)) {
      setError('El justificante debe ser un PDF, JPG o PNG.');
      if (fileInputRef.current) fileInputRef.current.value = '';
      setForm((prev) => ({ ...prev, justificante: null }));
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError('El justificante no puede superar 5 MB.');
      if (fileInputRef.current) fileInputRef.current.value = '';
      setForm((prev) => ({ ...prev, justificante: null }));
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      setForm((prev) => ({
        ...prev, justificante: {
          nombre: file.name,
          tipo: file.type,
          tamaño: file.size,
          dataUrl: reader.result,
          cargadoEn: new Date().toISOString()
        }
      }));
    };
    reader.readAsDataURL(file);
    setError('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const importe = Number(String(form.importe).replace(/€/g, '').replace(/\s/g, '').replace('.', '').replace(',', '.'));

    if (!form.importe || Number.isNaN(importe) || importe <= 0) {
      setError('Introduce un importe válido para aportar.');
      return;
    }

    if (importe > capitalDisponible) {
      setError(`El importe no puede superar el capital disponible de la operación (${op.capitalDisponible}).`);
      return;
    }

    if (!form.justificante) {
      setError('Debes adjuntar el justificante de la aportación antes de enviar la solicitud.');
      return;
    }

    const storedUser = JSON.parse(localStorage.getItem('capital_trade_user') || 'null');
    const usuarioId = storedUser?.id || localStorage.getItem('estudiante_id') || 'anon';
    const usuarioNombre = storedUser?.name || localStorage.getItem('usuario') || 'Usuario';

    const nuevaAportacion = {
      id: `ap-${Date.now()}`,
      operacionId: op.id,
      operacionNombre: op.nombre,
      usuarioId,
      usuarioNombre,
      importe: Number(importe),
      moneda: form.moneda,
      metodoPago: form.metodoPago,
      cuentaDestino: form.cuentaDestino,
      comentario: form.comentario.trim(),
      estado: 'Pendiente de validación',
      justificante: form.justificante ? form.justificante.dataUrl : ''
    };

    fetch(import.meta.env.VITE_API_URL + '/api/operaciones/aportaciones', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(nuevaAportacion)
    })
      .then(res => {
        if (!res.ok) throw new Error('Error en el servidor');
        setSuccess(`Tu aportación para ${op.nombre} ha quedado registrada con justificante adjunto y está pendiente de validación por el administrador.`);
        setError('');
        setForm({
          importe: '',
          moneda: 'EUR',
          metodoPago: 'transferencia',
          cuentaDestino: 'ES91 2100 0418 4502 0005 1332',
          comentario: '',
          justificante: null
        });
        if (fileInputRef.current) fileInputRef.current.value = '';
      })
      .catch(err => {
        console.error(err);
        setError('Ocurrió un error la enviar tu solicitud. Verifica tu conexión.');
      });
  };

  return (
    <div className="detail-shell">
      <div className="detail-card">
        <div className="detail-hero">
          <div className="detail-header">
            <span className="operation-tag">{op.tipo}</span>
            <h1>{op.nombre}</h1>
            <p>{op.descripcion}</p>
            <div className="detail-cta">
              <button className="primary-btn" type="button" onClick={openRequestModal}>Solicitar participación</button>
              <Link to="/operaciones" className="secondary-btn" style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center' }}>Volver a operaciones</Link>
            </div>
          </div>

          <div className="compliance-box">
            <h3>Estado</h3>
            <span className={`status-badge ${op.estado === 'Activa' ? 'active' : op.estado === 'Pendiente' ? 'pending' : 'closed'}`}>{op.estado}</span>
            <p>Capital disponible: {op.capitalDisponible}</p>
            <p>Capital pendiente: {op.capitalPendiente}</p>
            <p>Rendimiento previsto: {op.rendimiento}</p>
          </div>
        </div>

        <div className="meta-grid">
          <div className="meta-box"><span>Capital necesario</span><strong>{op.capitalNecesario}</strong></div>
          <div className="meta-box"><span>Plazo estimado</span><strong>{op.plazo}</strong></div>
          <div className="meta-box"><span>Inicio</span><strong>{op.inicio}</strong></div>
          <div className="meta-box"><span>Fin estimado</span><strong>{op.finEst}</strong></div>
        </div>

        <div className="detail-sections">
          <div className="risk-box">
            <h3>Riesgos</h3>
            <p>{op.riesgo}</p>
          </div>

          <div className="risk-box">
            <h3>Condiciones</h3>
            <ul className="condition-list">
              {op.condiciones.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>

          <div className="document-box">
            <h3>Documentación</h3>
            <ul>
              <li>Resumen operativo</li>
              <li>Condiciones de participación</li>
              <li>Anexo de riesgo</li>
              <li>Contrato de aportación</li>
            </ul>
          </div>
        </div>
      </div>

      {isModalOpen && (
        <div className="participation-modal-backdrop" onClick={() => setIsModalOpen(false)}>
          <div className="participation-modal" onClick={(e) => e.stopPropagation()}>
            <div className="participation-modal-header">
              <h3>{authPrompt ? 'Inicia sesión para continuar' : 'Solicitar participación'}</h3>
              <button type="button" className="secondary-btn" onClick={() => setIsModalOpen(false)}>Cerrar</button>
            </div>

            {authPrompt ? (
              <div className="auth-prompt-box">
                <p>Debes iniciar sesión o registrarte antes de enviar una solicitud de participación.</p>
                <div className="participation-actions">
                  <button type="button" className="primary-btn" onClick={() => { setIsModalOpen(false); window.location.href = '/login'; }}>Iniciar sesión</button>
                  <button type="button" className="secondary-btn" onClick={() => { setIsModalOpen(false); window.location.href = '/registro'; }}>Registrarse</button>
                </div>
              </div>
            ) : success ? (
              <div className="request-success-box">
                <strong>Solicitud enviada correctamente</strong>
                <p>{success}</p>
                <div className="participation-actions">
                  <button type="button" className="primary-btn" onClick={() => setIsModalOpen(false)}>Aceptar</button>
                </div>
              </div>
            ) : (
              <form className="participation-form-box" onSubmit={handleSubmit}>
                <div className="participation-grid">
                  <div>
                    <label htmlFor="importe-solicitud">Importe que desea aportar *</label>
                    <input
                      id="importe-solicitud"
                      type="text"
                      value={form.importe}
                      onChange={(e) => setForm((prev) => ({ ...prev, importe: e.target.value }))}
                      placeholder={`Máximo ${op.capitalDisponible}`}
                    />
                  </div>

                  <div>
                    <label htmlFor="moneda-solicitud">Moneda *</label>
                    <select
                      id="moneda-solicitud"
                      value={form.moneda}
                      onChange={(e) => setForm((prev) => ({ ...prev, moneda: e.target.value }))}
                    >
                      <option value="EUR">EUR</option>
                      <option value="USDT BEP-20">USDT BEP-20</option>
                    </select>
                  </div>
                </div>

                <div className="participation-grid">
                  <div>
                    <label htmlFor="metodo-pago">Método de pago *</label>
                    <select
                      id="metodo-pago"
                      value={form.metodoPago}
                      onChange={(e) => setForm((prev) => ({ ...prev, metodoPago: e.target.value }))}
                    >
                      <option value="transferencia">Transferencia</option>
                      <option value="bizum">Bizum</option>
                      <option value="efectivo">Efectivo</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="cuenta-solicitud">Cuenta de destino *</label>
                    <input
                      id="cuenta-solicitud"
                      type="text"
                      value={form.cuentaDestino}
                      onChange={(e) => setForm((prev) => ({ ...prev, cuentaDestino: e.target.value }))}
                      placeholder="ES91 2100 0418 4502 0005 1332"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="comentario-solicitud">Comentario o mensaje (opcional)</label>
                  <textarea
                    id="comentario-solicitud"
                    value={form.comentario}
                    onChange={(e) => setForm((prev) => ({ ...prev, comentario: e.target.value }))}
                    placeholder="Añade cualquier detalle que quieras compartir con el administrador antes de evaluar la participación."
                  />
                </div>

                <div>
                  <label htmlFor="justificante-solicitud">Justificante de la aportación *</label>
                  <input
                    id="justificante-solicitud"
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.png,.jpg,.jpeg"
                    onChange={handleFileChange}
                  />
                  {form.justificante && (
                    <div className="file-preview">
                      <strong>Archivo adjunto:</strong> {form.justificante.nombre}
                    </div>
                  )}
                </div>

                {error && <div className="error-message">⚠️ {error}</div>}

                <div className="participation-actions">
                  <button type="button" className="secondary-btn" onClick={() => setIsModalOpen(false)}>Cancelar</button>
                  <button type="submit" className="primary-btn">Enviar aportación</button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default OperacionDetalle;
