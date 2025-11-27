import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, PointElement, LineElement } from 'chart.js';
import { Bar, Pie, Line, Doughnut } from 'react-chartjs-2';
import './DashboardAnalytics.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, PointElement, LineElement);

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://botvisa-production.up.railway.app';

const DashboardAnalytics = () => {
  const [metricas, setMetricas] = useState(null);
  const [porPais, setPorPais] = useState([]);
  const [porEspecialidad, setPorEspecialidad] = useState([]);
  const [crecimiento, setCrecimiento] = useState([]);
  const [estados, setEstados] = useState([]);
  const [universidades, setUniversidades] = useState([]);
  const [engagement, setEngagement] = useState(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    cargarAnalytics();
  }, []);

  const cargarAnalytics = async () => {
    try {
      setCargando(true);
      const token = localStorage.getItem('token');
      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };

      // Cargar todas las métricas en paralelo
      const [resGeneral, resPais, resEsp, resCrecimiento, resEstados, resUni, resEngagement] = await Promise.all([
        fetch(`${API_BASE_URL}/api/admin/analytics/general`, { headers }),
        fetch(`${API_BASE_URL}/api/admin/analytics/por-pais`, { headers }),
        fetch(`${API_BASE_URL}/api/admin/analytics/por-especialidad`, { headers }),
        fetch(`${API_BASE_URL}/api/admin/analytics/crecimiento-mensual`, { headers }),
        fetch(`${API_BASE_URL}/api/admin/analytics/estados-visa`, { headers }),
        fetch(`${API_BASE_URL}/api/admin/analytics/universidades-populares`, { headers }),
        fetch(`${API_BASE_URL}/api/admin/analytics/engagement`, { headers })
      ]);

      const dataGeneral = await resGeneral.json();
      const dataPais = await resPais.json();
      const dataEsp = await resEsp.json();
      const dataCrecimiento = await resCrecimiento.json();
      const dataEstados = await resEstados.json();
      const dataUni = await resUni.json();
      const dataEngagement = await resEngagement.json();

      setMetricas(dataGeneral.metricas);
      setPorPais(dataPais.paises || []);
      setPorEspecialidad(dataEsp.especialidades || []);
      setCrecimiento(dataCrecimiento.crecimiento || []);
      setEstados(dataEstados.estados || []);
      setUniversidades(dataUni.universidades || []);
      setEngagement(dataEngagement.engagement);

      setCargando(false);
    } catch (error) {
      console.error('❌ Error cargando analytics:', error);
      setCargando(false);
    }
  };

  const exportarCSV = async () => {
    try {
      const token = localStorage.getItem('token');
      window.open(`${API_BASE_URL}/api/admin/analytics/exportar-csv?token=${token}`, '_blank');
    } catch (error) {
      console.error('❌ Error exportando CSV:', error);
    }
  };

  if (cargando) {
    return (
      <div className="analytics-container">
        <div className="cargando">
          <div className="spinner"></div>
          <p>Cargando analytics...</p>
        </div>
      </div>
    );
  }

  // Chart configs
  const chartOptionsPais = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      title: { display: true, text: 'Estudiantes por País', font: { size: 16 } }
    },
    scales: {
      y: { beginAtZero: true, ticks: { stepSize: 1 } }
    }
  };

  const dataPaisChart = {
    labels: porPais.map(p => p.pais),
    datasets: [{
      label: 'Estudiantes',
      data: porPais.map(p => p.total),
      backgroundColor: [
        '#8b5cf6', '#6366f1', '#3b82f6', '#0ea5e9', '#06b6d4',
        '#14b8a6', '#10b981', '#84cc16', '#eab308', '#f59e0b'
      ]
    }]
  };

  const dataEspecialidadChart = {
    labels: porEspecialidad.map(e => e.especialidad),
    datasets: [{
      label: 'Estudiantes',
      data: porEspecialidad.map(e => e.total),
      backgroundColor: [
        '#8b5cf6', '#ec4899', '#f43f5e', '#f97316', '#eab308',
        '#84cc16', '#10b981', '#06b6d4', '#3b82f6', '#6366f1'
      ]
    }]
  };

  const dataCrecimientoChart = {
    labels: crecimiento.map(c => c.mes),
    datasets: [{
      label: 'Nuevos Estudiantes',
      data: crecimiento.map(c => c.total),
      borderColor: '#8b5cf6',
      backgroundColor: 'rgba(139, 92, 246, 0.1)',
      tension: 0.4,
      fill: true
    }]
  };

  const dataEstadosChart = {
    labels: estados.map(e => e.estado),
    datasets: [{
      label: 'Estudiantes',
      data: estados.map(e => e.total),
      backgroundColor: [
        '#10b981', '#eab308', '#f59e0b', '#ef4444', '#8b5cf6',
        '#06b6d4', '#3b82f6', '#ec4899'
      ]
    }]
  };

  const chartOptionsLine = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true, position: 'top' },
      title: { display: true, text: 'Crecimiento Mensual', font: { size: 16 } }
    },
    scales: {
      y: { beginAtZero: true, ticks: { stepSize: 1 } }
    }
  };

  const chartOptionsPie = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'right' },
      title: { display: true, text: 'Especialidades', font: { size: 16 } }
    }
  };

  const chartOptionsDoughnut = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'bottom' },
      title: { display: true, text: 'Estados de Visa', font: { size: 16 } }
    }
  };

  return (
    <div className="analytics-container">
      <div className="analytics-header">
        <h1>📊 Dashboard Analytics</h1>
        <div className="analytics-actions">
          <button className="btn-exportar" onClick={exportarCSV}>
            📥 Exportar CSV
          </button>
          <button className="btn-refrescar" onClick={cargarAnalytics}>
            🔄 Refrescar
          </button>
        </div>
      </div>

      {/* Métricas principales */}
      <div className="metricas-grid">
        <div className="metrica-card">
          <div className="metrica-icono">👥</div>
          <div className="metrica-info">
            <p className="metrica-label">Total Estudiantes</p>
            <h2 className="metrica-valor">{metricas?.total_estudiantes || 0}</h2>
          </div>
        </div>

        <div className="metrica-card green">
          <div className="metrica-icono">✅</div>
          <div className="metrica-info">
            <p className="metrica-label">Aprobados</p>
            <h2 className="metrica-valor">{metricas?.aprobados || 0}</h2>
          </div>
        </div>

        <div className="metrica-card blue">
          <div className="metrica-icono">📈</div>
          <div className="metrica-info">
            <p className="metrica-label">Tasa Aprobación</p>
            <h2 className="metrica-valor">{metricas?.tasa_aprobacion || 0}%</h2>
          </div>
        </div>

        <div className="metrica-card orange">
          <div className="metrica-icono">⏳</div>
          <div className="metrica-info">
            <p className="metrica-label">Pendientes</p>
            <h2 className="metrica-valor">{metricas?.pendientes || 0}</h2>
          </div>
        </div>

        <div className="metrica-card red">
          <div className="metrica-icono">❌</div>
          <div className="metrica-info">
            <p className="metrica-label">Rechazados</p>
            <h2 className="metrica-valor">{metricas?.rechazados || 0}</h2>
          </div>
        </div>

        <div className="metrica-card purple">
          <div className="metrica-icono">🆕</div>
          <div className="metrica-info">
            <p className="metrica-label">Nuevos (30 días)</p>
            <h2 className="metrica-valor">{metricas?.nuevos_30_dias || 0}</h2>
          </div>
        </div>

        <div className="metrica-card cyan">
          <div className="metrica-icono">💬</div>
          <div className="metrica-info">
            <p className="metrica-label">Mensajes (mes)</p>
            <h2 className="metrica-valor">{metricas?.mensajes_mes || 0}</h2>
          </div>
        </div>

        <div className="metrica-card pink">
          <div className="metrica-icono">🎯</div>
          <div className="metrica-info">
            <p className="metrica-label">Engagement Rate</p>
            <h2 className="metrica-valor">{metricas?.engagement_rate || 0}%</h2>
          </div>
        </div>
      </div>

      {/* Gráficos */}
      <div className="charts-grid">
        <div className="chart-card chart-large">
          <div className="chart-container">
            <Bar data={dataPaisChart} options={chartOptionsPais} />
          </div>
        </div>

        <div className="chart-card">
          <div className="chart-container">
            <Pie data={dataEspecialidadChart} options={chartOptionsPie} />
          </div>
        </div>

        <div className="chart-card chart-large">
          <div className="chart-container">
            <Line data={dataCrecimientoChart} options={chartOptionsLine} />
          </div>
        </div>

        <div className="chart-card">
          <div className="chart-container">
            <Doughnut data={dataEstadosChart} options={chartOptionsDoughnut} />
          </div>
        </div>
      </div>

      {/* Universidades top */}
      {universidades.length > 0 && (
        <div className="universidades-card">
          <h3>🏆 Universidades Más Populares</h3>
          <div className="universidades-list">
            {universidades.map((uni, index) => (
              <div key={index} className="universidad-item">
                <span className="ranking">#{index + 1}</span>
                <span className="nombre">{uni.nombre}</span>
                <span className="visitas">{uni.visitas} visitas</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Engagement metrics */}
      {engagement && (
        <div className="engagement-card">
          <h3>🎯 Métricas de Engagement</h3>
          <div className="engagement-grid">
            <div className="engagement-item">
              <div className="engagement-label">Simulador Completado</div>
              <div className="engagement-bar">
                <div 
                  className="engagement-progress" 
                  style={{ width: `${engagement.porcentajes.simulador}%`, backgroundColor: '#8b5cf6' }}
                ></div>
              </div>
              <div className="engagement-value">{engagement.simulador_completado} ({engagement.porcentajes.simulador}%)</div>
            </div>

            <div className="engagement-item">
              <div className="engagement-label">Alertas Configuradas</div>
              <div className="engagement-bar">
                <div 
                  className="engagement-progress" 
                  style={{ width: `${engagement.porcentajes.alertas}%`, backgroundColor: '#06b6d4' }}
                ></div>
              </div>
              <div className="engagement-value">{engagement.alertas_configuradas} ({engagement.porcentajes.alertas}%)</div>
            </div>

            <div className="engagement-item">
              <div className="engagement-label">Chat Activo</div>
              <div className="engagement-bar">
                <div 
                  className="engagement-progress" 
                  style={{ width: `${engagement.porcentajes.chat}%`, backgroundColor: '#10b981' }}
                ></div>
              </div>
              <div className="engagement-value">{engagement.chat_activo} ({engagement.porcentajes.chat}%)</div>
            </div>

            <div className="engagement-item">
              <div className="engagement-label">Documentos Subidos</div>
              <div className="engagement-bar">
                <div 
                  className="engagement-progress" 
                  style={{ width: `${engagement.porcentajes.documentos}%`, backgroundColor: '#f59e0b' }}
                ></div>
              </div>
              <div className="engagement-value">{engagement.documentos_subidos} ({engagement.porcentajes.documentos}%)</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardAnalytics;
