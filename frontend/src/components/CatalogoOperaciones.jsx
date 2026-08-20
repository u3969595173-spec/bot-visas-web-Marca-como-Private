import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Platform.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function CatalogoOperaciones() {
  const navigate = useNavigate();
  const [operaciones, setOperaciones] = React.useState([]);
  const [cargando, setCargando] = React.useState(true);

  React.useEffect(() => {
    fetch(`${API}/api/operaciones`)
      .then((res) => res.json())
      .then((data) => setOperaciones(data.operaciones || []))
      .catch(() => setOperaciones([]))
      .finally(() => setCargando(false));
  }, []);

  return (
    <div className="platform-page">
      <div className="platform-card">
        <div className="platform-header">
          <div>
            <p className="section-label">Oportunidades</p>
            <h1>Operaciones disponibles</h1>
          </div>
          <div className="platform-actions">
            <Link to="/registro" className="primary-btn" style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center' }}>Solicitar información</Link>
          </div>
        </div>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Operación</th>
                <th>Categoría</th>
                <th>Capital</th>
              </tr>
            </thead>
            <tbody>
              {cargando ? (
                <tr><td colSpan="3">Cargando operaciones…</td></tr>
              ) : operaciones.length === 0 ? (
                <tr><td colSpan="3">No hay operaciones disponibles.</td></tr>
              ) : (
                operaciones.map((op) => (
                  <tr key={op.id} onClick={() => navigate(`/operacion/${op.id}`)} style={{ cursor: 'pointer' }}>
                    <td>{op.icono} {op.nombre}</td>
                    <td>{op.categoria}</td>
                    <td>{op.capital}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default CatalogoOperaciones;
