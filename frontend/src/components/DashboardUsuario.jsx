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
  const [showPresupuestoModal, setShowPresupuestoModal] = useState(false);
  const [serviciosSeleccionados, setServiciosSeleccionados] = useState({});
  const [presupuestoActual, setPresupuestoActual] = useState(null);
  const [estadisticasReferidos, setEstadisticasReferidos] = useState(null);
  const [showReferidosModal, setShowReferidosModal] = useState(false);
  const [showOfertaModal, setShowOfertaModal] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    console.log('[DEBUG] DashboardUsuario montado con ID:', estudianteId);
    if (estudianteId) {
      // Guardar ID en localStorage para persistencia entre navegaciones
      localStorage.setItem('estudiante_id', estudianteId);
      console.log('[DEBUG] Iniciando carga de datos...');
      cargarDatos();
      cargarPresupuestos();
      console.log('[DEBUG] Llamando a cargarEstadisticasReferidos...');
      cargarEstadisticasReferidos();
      console.log('[DEBUG] Todas las funciones de carga iniciadas');
    }
  }, [estudianteId]);

  const cargarEstadisticasReferidos = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      console.log('[REFERIDOS] Cargando estadísticas para estudiante:', estudianteId);
      const response = await axios.get(`${apiUrl}/api/referidos/estadisticas/${estudianteId}`);
      console.log('[REFERIDOS] Datos recibidos:', response.data);
      setEstadisticasReferidos(response.data);
    } catch (err) {
      console.error('[REFERIDOS] Error cargando estadísticas:', err);
      console.error('[REFERIDOS] Error detalles:', err.response?.data);
    }
  };

  const cargarPresupuestos = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${apiUrl}/api/presupuestos/estudiante/${estudianteId}`);
      console.log('[DEBUG] Presupuestos recibidos:', response.data);
      if (response.data && response.data.length > 0) {
        // Obtener el presupuesto más reciente con oferta (incluye aceptados)
        const ultimoConOferta = response.data.find(p => 
          p.estado === 'oferta_enviada' || 
          p.estado === 'ofertado' || 
          p.estado === 'aceptado'
        );
        if (ultimoConOferta) {
          console.log('[DEBUG] Presupuesto con oferta encontrado:', ultimoConOferta);
          console.log('[DEBUG] Precios disponibles:', {
            precio_al_empezar: ultimoConOferta.precio_al_empezar,
            precio_con_visa: ultimoConOferta.precio_con_visa,
            precio_financiado: ultimoConOferta.precio_financiado
          });
          console.log('[DEBUG] Estado del presupuesto:', ultimoConOferta.estado);
          console.log('[DEBUG] ¿Tiene al menos un precio?', 
            !!(ultimoConOferta.precio_al_empezar || ultimoConOferta.precio_con_visa || ultimoConOferta.precio_financiado)
          );
          setPresupuestoActual(ultimoConOferta);
        } else {
          console.log('[DEBUG] No hay presupuestos con oferta. Estados encontrados:', response.data.map(p => p.estado));
          setPresupuestoActual(null);
        }
      } else {
        console.log('[DEBUG] No hay presupuestos');
        setPresupuestoActual(null);
      }
    } catch (err) {
      console.error('Error cargando presupuestos:', err);
      setPresupuestoActual(null);
    }
  };

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

      {/* Sección de Acciones Principales */}
      <div style={{
        background: 'white',
        borderRadius: '15px',
        padding: '25px',
        marginBottom: '30px',
        boxShadow: '0 4px 15px rgba(0,0,0,0.1)'
      }}>
        <h3 style={{
          margin: '0 0 20px 0',
          color: '#2d3748',
          fontSize: '18px',
          fontWeight: '600'
        }}>
          🎯 Acciones Rápidas
        </h3>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '15px',
          marginBottom: '20px'
        }}>
          <button
            onClick={() => setShowPresupuestoModal(true)}
            className="btn"
            style={{
              background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              color: 'white',
              border: 'none',
              fontWeight: '600',
              padding: '15px 20px',
              borderRadius: '10px',
              fontSize: '16px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px'
            }}
          >
            💰 Solicitar Presupuesto
          </button>
          
          {estadisticasReferidos && estadisticasReferidos.codigo_referido && (
            <button
              onClick={() => setShowReferidosModal(true)}
              className="btn"
              style={{
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                color: 'white',
                border: 'none',
                fontWeight: '600',
                padding: '15px 20px',
                borderRadius: '10px',
                fontSize: '16px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              💎 Referidos ({estadisticasReferidos.total_referidos})
            </button>
          )}
          
          {/* Botón Ver Oferta - Si existe presupuesto */}
          {presupuestoActual && 
           ['ofertado', 'oferta_enviada', 'aceptado'].includes(presupuestoActual.estado) && 
           (presupuestoActual.precio_al_empezar || presupuestoActual.precio_con_visa || presupuestoActual.precio_financiado) && (
            <button
              onClick={() => setShowOfertaModal(true)}
              className="btn"
              style={{
                background: presupuestoActual.estado === 'aceptado' 
                  ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' 
                  : 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
                color: 'white',
                border: 'none',
                fontWeight: '600',
                padding: '15px 20px',
                borderRadius: '10px',
                fontSize: '16px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              {presupuestoActual.estado === 'aceptado' ? '✅ Ver Presupuesto Aceptado' : '💰 Ver Oferta Recibida'}
            </button>
          )}
        </div>
        
        <h4 style={{
          margin: '25px 0 15px 0',
          color: '#4a5568',
          fontSize: '16px',
          fontWeight: '600'
        }}>
          📋 Gestionar Mi Información
        </h4>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '15px'
        }}>
          <button
            onClick={() => navigate('/estudiante/informacion-financiera')}
            className="btn"
            style={{
              background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
              color: 'white',
              border: 'none',
              fontWeight: '600',
              padding: '15px 20px',
              borderRadius: '10px',
              fontSize: '15px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px'
            }}
          >
            💸 Información Financiera
          </button>
          
          <button
            onClick={() => navigate('/estudiante/informacion-alojamiento')}
            className="btn"
            style={{
              background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
              color: 'white',
              border: 'none',
              fontWeight: '600',
              padding: '15px 20px',
              borderRadius: '10px',
              fontSize: '15px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px'
            }}
          >
            🏠 Información de Alojamiento
          </button>
          
          <button
            onClick={() => navigate('/estudiante/informacion-seguro-medico')}
            className="btn"
            style={{
              background: 'linear-gradient(135deg, #dc2626 0%, #991b1b 100%)',
              color: 'white',
              border: 'none',
              fontWeight: '600',
              padding: '15px 20px',
              borderRadius: '10px',
              fontSize: '15px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px'
            }}
          >
            🏥 Seguro Médico
          </button>
        </div>
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

      {/* Modal Solicitar Presupuesto */}
      {showPresupuestoModal && (
        <div className="modal-overlay">
          <div className="modal-content" style={{maxWidth: '800px', maxHeight: '90vh', overflowY: 'auto'}}>
            <h3 style={{marginTop: 0, color: '#1f2937', borderBottom: '2px solid #10b981', paddingBottom: '10px'}}>
              💰 Solicitar Presupuesto de Servicios
            </h3>

            <p style={{color: '#6b7280', marginBottom: '25px'}}>
              Selecciona los servicios que necesitas y verás el precio total calculado automáticamente.
            </p>

            <div style={{marginBottom: '30px'}}>
              {[
                {
                  id: 'gestion_basica_documentos', 
                  nombre: 'Gestión Básica de Documentos',
                  descripcion: 'Organización, revisión y preparación de todos tus documentos académicos y personales necesarios para el proceso de visa. Incluye verificación de completitud y formato requerido.'
                },
                {
                  id: 'solicitud_universitaria', 
                  nombre: 'Solicitud Universitaria',
                  descripcion: 'Búsqueda personalizada de universidades según tu perfil académico, aplicación completa a múltiples instituciones, seguimiento del proceso y obtención de carta de aceptación.'
                },
                {
                  id: 'legalizacion_apostillamiento', 
                  nombre: 'Legalización y Apostillamiento',
                  descripcion: 'Legalización de tu título y documentos académicos en órganos rectores de tu país, apostillado en cancillería y preparación para validación internacional.'
                },
                {
                  id: 'antecedentes_penales', 
                  nombre: 'Antecedentes Penales',
                  descripcion: 'Obtención de certificado de antecedentes penales, legalización en instancias correspondientes, apostillado y preparación del documento para presentación consular.'
                },
                {
                  id: 'cita_preparacion_consular', 
                  nombre: 'Cita y Preparación Consular',
                  descripcion: 'Agendamiento de cita en consulado, preparación completa para entrevista, simulacros, revisión de documentación requerida y acompañamiento en el proceso.'
                },
                {
                  id: 'seguimiento_visa_otorgada', 
                  nombre: 'Seguimiento Hasta Visa Otorgada',
                  descripcion: 'Monitoreo constante del estado de tu solicitud, comunicación con consulado, resolución de requerimientos adicionales y acompañamiento hasta obtención de visa.'
                },
                {
                  id: 'alojamiento_cita', 
                  nombre: 'Gestión de Alojamiento',
                  descripcion: 'Esto es solo para llevar a la cita consular como comprobante de alojamiento planificado. Búsqueda y reserva temporal de accommodation.',
                  esParaCita: true,
                  navegarA: '/informacion-alojamiento'
                },
                {
                  id: 'seguro_medico_real', 
                  nombre: 'Seguro Médico Internacional',
                  descripcion: 'Este seguro sí te va a servir allí. Contratación de seguro médico internacional válido para estudios, con cobertura completa y reconocimiento oficial.',
                  navegarA: '/informacion-seguro-medico'
                },
                {
                  id: 'financiacion_cita', 
                  nombre: 'Demostración Financiera',
                  descripcion: 'Esto es solo para llevar a la cita consular. Preparación de documentos bancarios, certificaciones de solvencia y comprobantes financieros requeridos.',
                  esParaCita: true,
                  navegarA: '/informacion-financiera'
                }
              ].map(servicio => (
                <div key={servicio.id} style={{
                  backgroundColor: serviciosSeleccionados[servicio.id] ? '#d1fae5' : '#f9fafb',
                  padding: '20px',
                  borderRadius: '12px',
                  marginBottom: '15px',
                  border: serviciosSeleccionados[servicio.id] ? '2px solid #10b981' : '1px solid #e5e7eb',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  boxShadow: serviciosSeleccionados[servicio.id] ? '0 4px 12px rgba(16, 185, 129, 0.2)' : '0 2px 4px rgba(0,0,0,0.1)'
                }}
                onClick={() => {
                  // Si es un servicio que navega a otro componente
                  if (servicio.navegarA) {
                    if (confirm(`Este servicio requiere completar información adicional. ¿Quieres ir a rellenar la solicitud ahora?`)) {
                      navigate(`${servicio.navegarA}/${estudianteId}`);
                      return;
                    }
                  }
                  
                  setServiciosSeleccionados(prev => ({
                    ...prev,
                    [servicio.id]: !prev[servicio.id]
                  }))
                }}
                >
                  <div style={{display: 'flex', alignItems: 'flex-start', gap: '15px'}}>
                    <input
                      type="checkbox"
                      checked={serviciosSeleccionados[servicio.id] || false}
                      onChange={() => {}}
                      style={{width: '20px', height: '20px', cursor: 'pointer', marginTop: '2px'}}
                    />
                    <div style={{flex: 1}}>
                      <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px'}}>
                        <strong style={{color: '#1f2937', fontSize: '16px'}}>{servicio.nombre}</strong>
                        {servicio.esParaCita && (
                          <span style={{
                            backgroundColor: '#fbbf24',
                            color: '#92400e',
                            fontSize: '11px',
                            padding: '2px 6px',
                            borderRadius: '4px',
                            fontWeight: '600'
                          }}>SOLO PARA CITA</span>
                        )}
                        {servicio.navegarA && (
                          <span style={{
                            backgroundColor: '#3b82f6',
                            color: 'white',
                            fontSize: '11px',
                            padding: '2px 6px',
                            borderRadius: '4px',
                            fontWeight: '600'
                          }}>REQUIERE FORMULARIO</span>
                        )}
                      </div>
                      <p style={{color: '#6b7280', fontSize: '14px', margin: 0, lineHeight: '1.4'}}>
                        {servicio.descripcion}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Resumen de Servicios Seleccionados */}
            <div style={{
              backgroundColor: '#f0fdf4',
              padding: '20px',
              borderRadius: '10px',
              border: '2px solid #10b981',
              marginBottom: '20px'
            }}>
              <div>
                <h4 style={{margin: '0 0 15px 0', color: '#065f46', fontSize: '18px'}}>📋 Servicios Seleccionados</h4>
                <p style={{margin: '0 0 10px 0', fontSize: '16px', color: '#059669', fontWeight: '600'}}>
                  {Object.values(serviciosSeleccionados).filter(Boolean).length} servicios solicitados
                </p>
                {Object.values(serviciosSeleccionados).filter(Boolean).length > 0 && (
                  <p style={{margin: 0, fontSize: '14px', color: '#065f46'}}>
                    ✅ Tu solicitud será revisada y recibirás una oferta personalizada
                  </p>
                )}
              </div>
            </div>

            <div style={{
              backgroundColor: '#e0f2fe',
              padding: '20px',
              borderRadius: '12px',
              marginBottom: '20px',
              border: '1px solid #81d4fa'
            }}>
              <div style={{marginBottom: '15px'}}>
                <h4 style={{margin: '0 0 10px 0', color: '#01579b', fontSize: '16px'}}>💰 Proceso de Presupuesto:</h4>
                <ol style={{margin: 0, paddingLeft: '20px', color: '#0277bd', fontSize: '14px'}}>
                  <li>Seleccionas los servicios que necesitas</li>
                  <li>Nuestro equipo revisa tu solicitud personalizada</li>
                  <li>Te enviamos una oferta con modalidades de pago</li>
                  <li>Puedes aceptar, rechazar o consultar dudas por chat</li>
                </ol>
              </div>
              <div style={{
                backgroundColor: '#b3e5fc',
                padding: '12px',
                borderRadius: '8px',
                marginTop: '15px'
              }}>
                <p style={{margin: 0, fontSize: '14px', color: '#01579b', fontWeight: '600'}}>
                  💬 Para cualquier duda, contacta por chat al administrador
                </p>
              </div>
            </div>

            <div style={{display: 'flex', gap: '10px', justifyContent: 'flex-end'}}>
              <button
                onClick={() => {
                  setShowPresupuestoModal(false)
                  setServiciosSeleccionados({})
                }}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#6b7280',
                  color: 'white',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}
              >
                Cancelar
              </button>
              <button
                onClick={async () => {
                  const serviciosArray = Object.entries(serviciosSeleccionados)
                    .filter(([_, selected]) => selected)
                    .map(([id]) => id);
                  
                  if (serviciosArray.length === 0) {
                    alert('⚠️ Por favor selecciona al menos un servicio para solicitar presupuesto');
                    return;
                  }

                  try {
                    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                    await axios.post(`${apiUrl}/api/presupuestos`, {
                      estudiante_id: estudianteId,
                      servicios_solicitados: serviciosArray,
                      estado: 'pendiente',
                      comentarios_estudiante: 'Solicitud de presupuesto personalizado'
                    });
                    alert('✅ Solicitud enviada exitosamente!\n\nNuestro equipo revisará tu solicitud y te enviará una oferta personalizada con diferentes modalidades de pago.\n\nPuedes consultar dudas por chat.');
                    setShowPresupuestoModal(false);
                    setServiciosSeleccionados({});
                  } catch (err) {
                    console.error('Error enviando solicitud:', err);
                    alert('❌ Error al enviar solicitud: ' + (err.response?.data?.detail || err.message));
                  }
                }}
                disabled={Object.values(serviciosSeleccionados).filter(Boolean).length === 0}
                style={{
                  padding: '12px 30px',
                  backgroundColor: Object.values(serviciosSeleccionados).filter(Boolean).length > 0 ? '#10b981' : '#d1d5db',
                  color: 'white',
                  fontSize: '16px',
                  fontWeight: '600',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: Object.values(serviciosSeleccionados).filter(Boolean).length > 0 ? 'pointer' : 'not-allowed',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                  transition: 'all 0.2s'
                }}
              >
                💰 Solicitar Presupuesto Personalizado
              </button>
            </div>

            {/* Nota sobre presupuestos rechazados */}
            <div style={{
              marginTop: '20px',
              padding: '15px',
              backgroundColor: '#e6f3ff',
              borderLeft: '4px solid #2563eb',
              borderRadius: '8px'
            }}>
              <p style={{margin: 0, fontSize: '13px', color: '#1e40af', lineHeight: '1.5'}}>
                💡 <strong>¿Rechazaste alguna oferta anterior?</strong> No te preocupes, puedes solicitar un nuevo presupuesto las veces que necesites hasta encontrar la opción perfecta para ti. Nuestro equipo está aquí para ayudarte.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Lista de Referidos */}
      {showReferidosModal && estadisticasReferidos && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '20px'
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '15px',
            padding: '30px',
            maxWidth: '700px',
            width: '100%',
            maxHeight: '80vh',
            overflow: 'auto'
          }}>
            <h2 style={{margin: '0 0 20px 0', color: '#2d3748'}}>
              💎 Mis Referidos
            </h2>

            {/* Enlace de Referido para Compartir */}
            <div style={{
              background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
              color: 'white',
              padding: '20px',
              borderRadius: '10px',
              marginBottom: '25px'
            }}>
              <h3 style={{fontSize: '18px', marginBottom: '15px', margin: '0 0 15px 0'}}>
                🔗 Tu Enlace de Referido
              </h3>
              <div style={{
                background: 'rgba(255,255,255,0.2)',
                padding: '12px',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                marginBottom: '15px'
              }}>
                <input
                  type="text"
                  value={`${window.location.origin}/estudiante/registro?ref=${estadisticasReferidos.codigo_referido}`}
                  readOnly
                  style={{
                    flex: 1,
                    padding: '10px',
                    border: 'none',
                    borderRadius: '6px',
                    backgroundColor: 'white',
                    color: '#2d3748',
                    fontSize: '14px'
                  }}
                />
                <button
                  onClick={() => {
                    const enlace = `${window.location.origin}/estudiante/registro?ref=${estadisticasReferidos.codigo_referido}`;
                    navigator.clipboard.writeText(enlace).then(() => {
                      alert('✅ Enlace copiado al portapapeles');
                    });
                  }}
                  style={{
                    padding: '10px 15px',
                    background: 'white',
                    color: '#3b82f6',
                    border: 'none',
                    borderRadius: '6px',
                    fontSize: '14px',
                    fontWeight: '600',
                    cursor: 'pointer'
                  }}
                >
                  📋 Copiar
                </button>
              </div>
              <p style={{fontSize: '13px', opacity: 0.9, margin: '0 0 15px 0'}}>
                Comparte este enlace y recibe el <strong>10% del valor del trámite</strong> por cada persona que empiece proceso usando tu código: <strong>{estadisticasReferidos.codigo_referido}</strong>
              </p>
              
              {/* Botones de compartir rápido */}
              <div style={{display: 'flex', gap: '10px', flexWrap: 'wrap'}}>
                <button
                  onClick={() => {
                    const enlace = `${window.location.origin}/estudiante/registro?ref=${estadisticasReferidos.codigo_referido}`;
                    const mensaje = `¡Hola! 👋 Te invito a registrarte en Bot Visas de Estudio usando mi código de referido ${estadisticasReferidos.codigo_referido}. ¡Recibo el 10% cuando empiezas tu trámite y tú obtienes ayuda profesional! ${enlace}`;
                    window.open(`https://wa.me/?text=${encodeURIComponent(mensaje)}`);
                  }}
                  style={{
                    flex: 1,
                    padding: '8px 12px',
                    background: '#25d366',
                    color: 'white',
                    border: 'none',
                    borderRadius: '6px',
                    fontSize: '12px',
                    fontWeight: '600',
                    cursor: 'pointer'
                  }}
                >
                  📱 WhatsApp
                </button>
                <button
                  onClick={() => {
                    const enlace = `${window.location.origin}/estudiante/registro?ref=${estadisticasReferidos.codigo_referido}`;
                    const mensaje = `¡Regístrate en Bot Visas de Estudio con mi código ${estadisticasReferidos.codigo_referido} y recibe ayuda profesional para tu visa! Yo recibo el 10% cuando empiezas tu trámite. Win-win 🎯 ${enlace}`;
                    navigator.clipboard.writeText(mensaje).then(() => {
                      alert('✅ Mensaje copiado. Pégalo en cualquier red social');
                    });
                  }}
                  style={{
                    flex: 1,
                    padding: '8px 12px',
                    background: 'rgba(255,255,255,0.2)',
                    color: 'white',
                    border: '2px solid white',
                    borderRadius: '6px',
                    fontSize: '12px',
                    fontWeight: '600',
                    cursor: 'pointer'
                  }}
                >
                  📄 Copiar Mensaje
                </button>
              </div>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '15px',
              marginBottom: '25px'
            }}>
              <div style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                padding: '20px',
                borderRadius: '10px',
                textAlign: 'center'
              }}>
                <div style={{fontSize: '36px', fontWeight: '700'}}>
                  {estadisticasReferidos.total_referidos}
                </div>
                <div style={{fontSize: '14px', opacity: 0.9}}>Total Referidos</div>
              </div>
              <div style={{
                background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                color: 'white',
                padding: '20px',
                borderRadius: '10px',
                textAlign: 'center'
              }}>
                <div style={{fontSize: '36px', fontWeight: '700'}}>
                  {estadisticasReferidos.credito_disponible.toFixed(2)}€
                </div>
                <div style={{fontSize: '14px', opacity: 0.9}}>Crédito Disponible</div>
              </div>
              <div style={{
                background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                color: 'white',
                padding: '20px',
                borderRadius: '10px',
                textAlign: 'center'
              }}>
                <div style={{fontSize: '36px', fontWeight: '700'}}>
                  {estadisticasReferidos.total_ganado.toFixed(2)}€
                </div>
                <div style={{fontSize: '14px', opacity: 0.9}}>Total Ganado</div>
              </div>
            </div>

            {estadisticasReferidos.referidos.length > 0 ? (
              <div>
                <h3 style={{fontSize: '18px', color: '#2d3748', marginBottom: '15px'}}>
                  Lista de Personas Referidas:
                </h3>
                <div style={{display: 'flex', flexDirection: 'column', gap: '10px'}}>
                  {estadisticasReferidos.referidos.map((referido, index) => (
                    <div key={index} style={{
                      backgroundColor: '#f7fafc',
                      padding: '15px',
                      borderRadius: '8px',
                      border: '1px solid #e2e8f0'
                    }}>
                      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                        <div>
                          <div style={{fontWeight: '600', color: '#2d3748', marginBottom: '5px'}}>
                            {referido.nombre}
                          </div>
                          <div style={{fontSize: '13px', color: '#718096'}}>
                            {referido.email}
                          </div>
                        </div>
                        <div style={{
                          fontSize: '12px',
                          color: '#718096',
                          textAlign: 'right'
                        }}>
                          {new Date(referido.fecha_registro).toLocaleDateString('es-ES')}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div style={{
                textAlign: 'center',
                padding: '40px',
                color: '#a0aec0'
              }}>
                <div style={{fontSize: '48px', marginBottom: '10px'}}>👥</div>
                <p>Aún no tienes referidos</p>
                <p style={{fontSize: '14px'}}>Comparte tu código para empezar a ganar crédito</p>
              </div>
            )}

            {/* Opciones para usar el crédito */}
            {estadisticasReferidos.credito_disponible > 0 && (
              <div style={{
                marginTop: '25px',
                padding: '20px',
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                borderRadius: '10px',
                color: 'white'
              }}>
                <h3 style={{fontSize: '18px', marginBottom: '15px', margin: 0}}>
                  💰 Usa tu Crédito Disponible
                </h3>
                <p style={{fontSize: '14px', opacity: 0.9, marginBottom: '15px'}}>
                  Tienes {estadisticasReferidos.credito_disponible.toFixed(2)}€ disponibles
                </p>
                <div style={{display: 'flex', gap: '10px', flexWrap: 'wrap'}}>
                  <button
                    onClick={async () => {
                      if (confirm(`¿Solicitar retiro de ${estadisticasReferidos.credito_disponible.toFixed(2)}€?\n\nEl administrador procesará tu solicitud y te contactará.`)) {
                        try {
                          const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                          await axios.post(`${apiUrl}/api/referidos/solicitar-uso`, {
                            estudiante_id: estudianteId,
                            tipo: 'retiro',
                            monto: estadisticasReferidos.credito_disponible
                          });
                          alert('✅ Solicitud de retiro enviada. El administrador te contactará pronto.');
                          setShowReferidosModal(false);
                        } catch (err) {
                          alert('❌ Error al enviar solicitud: ' + (err.response?.data?.detail || err.message));
                        }
                      }
                    }}
                    style={{
                      flex: 1,
                      padding: '12px 20px',
                      background: 'white',
                      color: '#f5576c',
                      border: 'none',
                      borderRadius: '8px',
                      fontSize: '15px',
                      fontWeight: '600',
                      cursor: 'pointer'
                    }}
                  >
                    💸 Retirar Dinero
                  </button>
                  <button
                    onClick={async () => {
                      if (confirm(`¿Usar ${estadisticasReferidos.credito_disponible.toFixed(2)}€ como descuento en tu presupuesto aceptado?\n\nSe descontará del precio total.`)) {
                        try {
                          const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                          await axios.post(`${apiUrl}/api/referidos/solicitar-uso`, {
                            estudiante_id: estudianteId,
                            tipo: 'descuento',
                            monto: estadisticasReferidos.credito_disponible
                          });
                          alert('✅ Solicitud de descuento enviada. El administrador la aprobará.');
                          setShowReferidosModal(false);
                        } catch (err) {
                          alert('❌ Error al enviar solicitud: ' + (err.response?.data?.detail || err.message));
                        }
                      }
                    }}
                    style={{
                      flex: 1,
                      padding: '12px 20px',
                      background: 'rgba(255,255,255,0.2)',
                      color: 'white',
                      border: '2px solid white',
                      borderRadius: '8px',
                      fontSize: '15px',
                      fontWeight: '600',
                      cursor: 'pointer'
                    }}
                  >
                    🎫 Descontar de Trámite
                  </button>
                </div>
              </div>
            )}

            <button
              onClick={() => setShowReferidosModal(false)}
              style={{
                marginTop: '20px',
                width: '100%',
                padding: '12px',
                backgroundColor: '#e2e8f0',
                color: '#2d3748',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              Cerrar
            </button>
          </div>
        </div>
      )}

      {/* Modal de Oferta Recibida */}
      {showOfertaModal && presupuestoActual && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '20px'
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '15px',
            padding: '30px',
            maxWidth: '600px',
            width: '100%',
            maxHeight: '80vh',
            overflow: 'auto'
          }}>
            {/* Encabezado */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '15px',
              marginBottom: '20px',
              padding: '15px',
              background: 'linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)',
              borderRadius: '12px'
            }}>
              <div style={{
                width: '50px',
                height: '50px',
                background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '24px'
              }}>
                💰
              </div>
              <div>
                <h2 style={{ margin: 0, color: '#065f46', fontSize: '20px', fontWeight: '700' }}>
                  {presupuestoActual.estado === 'aceptado' ? 
                    '✅ Presupuesto Aceptado' : 
                    'Oferta Personalizada Recibida'}
                </h2>
                <p style={{ margin: '5px 0 0 0', color: '#059669', fontSize: '14px' }}>
                  {presupuestoActual.estado === 'aceptado' ? 
                    'Trabajo en proceso' :
                    'Revisa las modalidades de pago disponibles'}
                </p>
              </div>
            </div>
            
            {/* Modalidades de Pago */}
            <div style={{ display: 'grid', gap: '15px', marginBottom: '20px' }}>
              {presupuestoActual.precio_al_empezar && (
                <div style={{
                  background: 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
                  padding: '20px',
                  borderRadius: '12px',
                  border: '2px solid #fbbf24'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <div>
                      <div style={{ fontWeight: '700', color: '#92400e', fontSize: '16px', marginBottom: '4px' }}>
                        🚀 Pago Inicial
                      </div>
                      <div style={{ fontSize: '13px', color: '#78350f' }}>
                        Pago completo al iniciar el proceso
                      </div>
                    </div>
                    <div style={{ fontSize: '28px', fontWeight: '700', color: '#92400e' }}>
                      €{presupuestoActual.precio_al_empezar}
                    </div>
                  </div>
                </div>
              )}
              
              {presupuestoActual.precio_con_visa && (
                <div style={{
                  background: 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)',
                  padding: '20px',
                  borderRadius: '12px',
                  border: '2px solid #3b82f6'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <div>
                      <div style={{ fontWeight: '700', color: '#1e40af', fontSize: '16px', marginBottom: '4px' }}>
                        🎯 Pago Después de Cita
                      </div>
                      <div style={{ fontSize: '13px', color: '#1e40af' }}>
                        Pago al recibir visa aprobada
                      </div>
                    </div>
                    <div style={{ fontSize: '28px', fontWeight: '700', color: '#1e40af' }}>
                      €{presupuestoActual.precio_con_visa}
                    </div>
                  </div>
                </div>
              )}
              
              {presupuestoActual.precio_financiado && (
                <div style={{
                  background: 'linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%)',
                  padding: '20px',
                  borderRadius: '12px',
                  border: '2px solid #6366f1'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <div>
                      <div style={{ fontWeight: '700', color: '#4338ca', fontSize: '16px', marginBottom: '4px' }}>
                        📅 Pago Financiado
                      </div>
                      <div style={{ fontSize: '13px', color: '#4338ca' }}>
                        €{(presupuestoActual.precio_financiado / 12).toFixed(2)}/mes x 12 meses
                      </div>
                    </div>
                    <div style={{ fontSize: '28px', fontWeight: '700', color: '#4338ca' }}>
                      €{presupuestoActual.precio_financiado}
                    </div>
                  </div>
                </div>
              )}
              
              {/* Precio Total */}
              <div style={{
                background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                padding: '20px',
                borderRadius: '12px',
                border: '3px solid #065f46',
                boxShadow: '0 4px 12px rgba(16, 185, 129, 0.3)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <div style={{ fontWeight: '700', color: 'white', fontSize: '18px', marginBottom: '4px' }}>
                      💰 PRECIO TOTAL
                    </div>
                    <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.9)' }}>
                      Suma de todos los pagos
                    </div>
                  </div>
                  <div style={{ fontSize: '32px', fontWeight: '700', color: 'white' }}>
                    €{(
                      (parseFloat(presupuestoActual.precio_al_empezar) || 0) + 
                      (parseFloat(presupuestoActual.precio_con_visa) || 0) + 
                      (parseFloat(presupuestoActual.precio_financiado) || 0)
                    ).toFixed(2)}
                  </div>
                </div>
              </div>
            </div>

            {presupuestoActual.mensaje_admin && (
              <div style={{
                background: '#f0fdf4',
                padding: '16px',
                borderRadius: '10px',
                marginBottom: '20px',
                border: '1px solid #86efac'
              }}>
                <strong style={{ color: '#065f46', fontSize: '14px' }}>💬 Mensaje del equipo:</strong>
                <p style={{ margin: '8px 0 0 0', color: '#047857', fontSize: '14px', lineHeight: '1.6' }}>
                  {presupuestoActual.mensaje_admin}
                </p>
              </div>
            )}

            {/* Nota informativa */}
            <div style={{
              background: '#fef3c7',
              padding: '16px',
              borderRadius: '10px',
              marginBottom: '20px',
              border: '1px solid #fbbf24'
            }}>
              <p style={{ 
                margin: 0, 
                color: '#92400e', 
                fontSize: '13px', 
                lineHeight: '1.6',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '8px'
              }}>
                <span style={{ fontSize: '16px', marginTop: '-2px' }}>💡</span>
                <span>
                  <strong>Nota:</strong> El precio total incluye 3 pagos: inicial, después de la cita, y financiado. Si esta oferta no se ajusta a tu presupuesto, puedes rechazarla y solicitar un nuevo presupuesto ajustando los servicios. Estamos aquí para encontrar la mejor solución para ti.
                </span>
              </p>
            </div>

            {/* Botones de acción */}
            {presupuestoActual.estado === 'ofertado' ? (
              <div style={{ display: 'flex', gap: '12px' }}>
                <button
                  onClick={async () => {
                    const precioTotal = (
                      (parseFloat(presupuestoActual.precio_al_empezar) || 0) + 
                      (parseFloat(presupuestoActual.precio_con_visa) || 0) + 
                      (parseFloat(presupuestoActual.precio_financiado) || 0)
                    ).toFixed(2);
                    if (!confirm(`¿Estás seguro de aceptar esta oferta por un total de €${precioTotal}?`)) return;
                    try {
                      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                      await axios.put(`${apiUrl}/api/presupuestos/${presupuestoActual.id}/respuesta`, {
                        aceptar: true
                      });
                      alert('✅ ¡Perfecto! Oferta aceptada.');
                      setShowOfertaModal(false);
                      setPresupuestoActual(null);
                      cargarPresupuestos();
                    } catch (err) {
                      alert('❌ Error: ' + (err.response?.data?.detail || err.message));
                    }
                  }}
                  style={{
                    flex: 1,
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    color: 'white',
                    padding: '14px 24px',
                    border: 'none',
                    borderRadius: '10px',
                    fontSize: '16px',
                    fontWeight: '600',
                    cursor: 'pointer'
                  }}
                >
                  ✅ Aceptar Oferta
                </button>
                <button
                  onClick={async () => {
                    if (!confirm('¿Seguro que quieres rechazar esta oferta?')) return;
                    try {
                      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                      await axios.put(`${apiUrl}/api/presupuestos/${presupuestoActual.id}/respuesta`, {
                        aceptar: false
                      });
                      alert('Oferta rechazada. Puedes solicitar un nuevo presupuesto.');
                      setShowOfertaModal(false);
                      setPresupuestoActual(null);
                      cargarPresupuestos();
                    } catch (err) {
                      alert('❌ Error: ' + (err.response?.data?.detail || err.message));
                    }
                  }}
                  style={{
                    flex: 1,
                    background: 'white',
                    color: '#ef4444',
                    padding: '14px 24px',
                    border: '2px solid #ef4444',
                    borderRadius: '10px',
                    fontSize: '16px',
                    fontWeight: '600',
                    cursor: 'pointer'
                  }}
                >
                  ❌ Rechazar
                </button>
              </div>
            ) : (
              <button
                onClick={() => setShowOfertaModal(false)}
                style={{
                  width: '100%',
                  padding: '14px',
                  backgroundColor: '#e2e8f0',
                  color: '#2d3748',
                  border: 'none',
                  borderRadius: '10px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: 'pointer'
                }}
              >
                Cerrar
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default DashboardUsuario;
