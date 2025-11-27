import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import PerfilEstudiante from './PerfilEstudiante';
import CalculadoraVisa from './CalculadoraVisa';
import GestorDocumentos from './GestorDocumentos';
import ChatMensajes from './ChatMensajes';
import ChecklistDocumentos from './ChecklistDocumentos';
import ProcesoVisa from './ProcesoVisa';

function DashboardUsuario({ estudianteId: propEstudianteId }) {
  const { id: paramId } = useParams();
  const estudianteId = propEstudianteId || paramId;
  const [estudiante, setEstudiante] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('perfil');
  const navigate = useNavigate();

  useEffect(() => {
    console.log('[DEBUG] DashboardUsuario montado con ID:', estudianteId);
    if (estudianteId) {
      // Guardar ID en localStorage para persistencia entre navegaciones
      localStorage.setItem('estudiante_id', estudianteId);
    }
    cargarDatos();
  }, [estudianteId]);

  const cargarDatos = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const url = `${apiUrl}/api/estudiantes/${estudianteId}`;
      console.log('[DEBUG] Cargando datos desde:', url);
      
      const estRes = await axios.get(url);
      console.log('[DEBUG] Datos recibidos:', estRes.data);
      setEstudiante(estRes.data);
      setError(null);
    } catch (err) {
      console.error('[ERROR] Error cargando datos:', err);
      console.error('[ERROR] Detalles:', err.response?.data);
      setError(err.response?.data?.detail || err.message || 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <p>Cargando...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div style={{ 
          textAlign: 'center', 
          padding: '50px',
          background: '#fff3cd',
          borderRadius: '10px',
          margin: '20px'
        }}>
          <h2 style={{ color: '#856404' }}>⚠️ Error al cargar datos</h2>
          <p style={{ color: '#856404' }}>{error}</p>
          <button 
            className="btn btn-primary" 
            onClick={() => {
              setLoading(true);
              setError(null);
              cargarDatos();
            }}
          >
            🔄 Reintentar
          </button>
          <button 
            className="btn" 
            style={{ marginLeft: '10px' }}
            onClick={() => navigate('/')}
          >
            ← Volver al inicio
          </button>
        </div>
      </div>
    );
  }

  if (!estudiante) {
    return (
      <div className="container">
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <h2>⚠️ No se encontraron datos del estudiante</h2>
          <button className="btn btn-primary" onClick={() => navigate('/')}>
            ← Volver al inicio
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      {/* Alerta de Perfil Incompleto */}
      {!estudiante.perfil_completo && (
        <div style={{
          background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
          color: 'white',
          padding: '25px',
          borderRadius: '10px',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '15px',
          boxShadow: '0 4px 15px rgba(240, 147, 251, 0.3)'
        }}>
          <div>
            <h3 style={{ margin: '0 0 10px 0', fontSize: '20px' }}>
              ⚠️ Completa tu Perfil
            </h3>
            <p style={{ margin: 0, fontSize: '15px', opacity: 0.95 }}>
              Necesitamos información adicional para procesar tu solicitud de visa
            </p>
          </div>
          <button
            onClick={() => navigate(`/completar-perfil/${estudianteId}`)}
            style={{
              background: 'white',
              color: '#f5576c',
              padding: '12px 25px',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: 'pointer',
              boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
              transition: 'transform 0.2s'
            }}
            onMouseEnter={(e) => e.target.style.transform = 'scale(1.05)'}
            onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
          >
            📝 Completar Ahora
          </button>
        </div>
      )}

      {/* Header */}
      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        padding: '40px',
        borderRadius: '10px',
        marginBottom: '30px'
      }}>
        <h1 style={{ marginBottom: '10px' }}>
          Hola, {estudiante?.nombre || 'Estudiante'}! 👋
        </h1>
        <p style={{ fontSize: '18px', opacity: 0.9 }}>
          Bienvenido a tu portal de estudiante
        </p>
      </div>

      {/* Tabs de navegación */}
      <div style={{
        background: 'white',
        borderRadius: '10px',
        padding: '10px',
        marginBottom: '30px',
        display: 'flex',
        gap: '10px',
        flexWrap: 'wrap'
      }}>
        {['perfil', 'proceso', 'probabilidad', 'estado', 'checklist', 'documentos', 'mensajes'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className="btn"
            style={{
              background: activeTab === tab ? '#667eea' : 'transparent',
              color: activeTab === tab ? 'white' : '#2d3748',
              border: activeTab === tab ? 'none' : '2px solid #e2e8f0'
            }}
          >
            {tab === 'proceso' && '📊 Mi Proceso'}
            {tab === 'checklist' && '📋 Checklist'}
            {tab === 'perfil' && '👤 Perfil'}
            {tab === 'probabilidad' && '🎯 Probabilidad'}
            {tab === 'estado' && '📈 Estado'}
            {tab === 'documentos' && '📄 Documentos'}
            {tab === 'mensajes' && '💬 Mensajes'}
          </button>
        ))}
      </div>

      {/* TAB: Perfil */}
      {activeTab === 'perfil' && (
        <PerfilEstudiante estudianteId={estudianteId} />
      )}

      {/* TAB: Proceso de Visa Completo */}
      {activeTab === 'proceso' && (
        <ProcesoVisa estudianteId={estudianteId} />
      )}

      {/* TAB: Probabilidad */}
      {activeTab === 'probabilidad' && (
        <CalculadoraVisa estudianteId={estudianteId} />
      )}
      
      {/* TAB: Checklist Documentos */}
      {activeTab === 'checklist' && (
        <ChecklistDocumentos estudianteId={estudianteId} />
      )}

      {/* TAB: Estado */}
      {activeTab === 'estado' && (
        <div>
          <div className="card">
            <h2 style={{ marginBottom: '20px' }}>📊 Estado de tu Solicitud</h2>
            <div style={{
              background: '#f7fafc',
              padding: '30px',
              borderRadius: '10px',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '48px', marginBottom: '20px' }}>
                {estudiante?.estado === 'aprobado' ? '✅' : 
                 estudiante?.estado === 'rechazado' ? '❌' : '⏳'}
              </div>
              <h3 style={{ color: '#2d3748', marginBottom: '10px' }}>
                {estudiante?.estado?.toUpperCase() || 'PENDIENTE'}
              </h3>
              <p style={{ color: '#718096' }}>
                {estudiante?.estado === 'aprobado' ? '¡Felicidades! Tu solicitud ha sido aprobada.' :
                 estudiante?.estado === 'rechazado' ? 'Tu solicitud requiere más información.' :
                 'Tu solicitud está siendo revisada por nuestro equipo.'}
              </p>
              {estudiante?.notas && (
                <div style={{
                  background: 'white',
                  padding: '20px',
                  borderRadius: '8px',
                  marginTop: '20px',
                  textAlign: 'left',
                  borderLeft: '4px solid #667eea'
                }}>
                  <strong>Notas del administrador:</strong>
                  <p style={{ marginTop: '10px' }}>{estudiante.notas}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* TAB: Documentos */}
      {activeTab === 'documentos' && (
        <GestorDocumentos estudianteId={estudianteId} />
      )}

      {/* TAB: Mensajes */}
      {activeTab === 'mensajes' && (
        <ChatMensajes estudianteId={estudianteId} remitente="estudiante" />
      )}
    </div>
  );
}

export default DashboardUsuario;
