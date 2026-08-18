import React from 'react';
import { Link } from 'react-router-dom';
import './Platform.css';

const operaciones = [
  {
    id: 1,
    nombre: '🌾 Exportaciones de alimentos',
    categoria: 'Agricultura y exportación',
    capital: '€120.000'
  },
  {
    id: 2,
    nombre: '🏗️ Compra y venta de cemento en Cuba',
    categoria: 'Materiales de construcción',
    capital: '€95.000'
  },
  {
    id: 3,
    nombre: '💸 Remesas desde el exterior',
    categoria: 'Servicios financieros',
    capital: '€85.000'
  },
  {
    id: 4,
    nombre: '📊 Financiación a MYPIMEs y TCP',
    categoria: 'Financiamiento',
    capital: '€150.000'
  },
  {
    id: 5,
    nombre: '📈 Inversiones en MYPIMEs y TCP propias',
    categoria: 'Participación accionaria',
    capital: '€110.000'
  },
  {
    id: 6,
    nombre: '🌍 Inversiones en el extranjero',
    categoria: 'Mercados internacionales',
    capital: '€200.000'
  }
];

function CatalogoOperaciones() {
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
              {operaciones.map((op) => (
                <tr key={op.id}>
                  <td>{op.nombre}</td>
                  <td>{op.categoria}</td>
                  <td>{op.capital}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default CatalogoOperaciones;
