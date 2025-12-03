import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const InformacionAlojamiento = ({ estudianteId }) => {
  const navigate = useNavigate();
  const [estudiante, setEstudiante] = useState(null);
  const [formData, setFormData] = useState({
    tiene_alojamiento: null, // true = ya tiene, false = necesita gestión
    tipo_alojamiento: '',
    direccion_alojamiento: '',
    contacto_alojamiento: '',
    telefono_alojamiento: '',
    precio_mensual: '',
    moneda_alojamiento: 'EUR',
    gestion_solicitada: false,
    comentarios_alojamiento: ''
  });

  const [loading, setLoading] = useState(false);
  const [editing, setEditing] = useState(false);
  const [estadoAlojamiento, setEstadoAlojamiento] = useState(null); // pendiente/aprobado/rechazado
  const [comentariosAdmin, setComentariosAdmin] = useState('');
  const [modoEdicion, setModoEdicion] = useState(false);

  const apiUrl = import.meta.env.VITE_API_URL || 'https://bot-visas-api.onrender.com';

  useEffect(() => {
    // Cargar datos del estudiante
    const cargarEstudiante = async () => {
      if (!estudianteId) {
        navigate('/estudiante/login');
        return;
      }
      if (estudianteId) {
        try {
          const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}`);
          setEstudiante(response.data);
          
          // Cargar estado de la gestión por el admin
          setEstadoAlojamiento(response.data.estado_alojamiento || 'pendiente');
          setComentariosAdmin(response.data.comentarios_alojamiento || '');
          
          // Si ya fue procesado por el admin, no mostrar en modo edición por defecto
          if (response.data.estado_alojamiento && response.data.estado_alojamiento !== 'pendiente') {
            setModoEdicion(false);
          } else {
            setModoEdicion(true);
          }
        } catch (error) {
          console.error('Error cargando estudiante:', error);
        }
      }
    };
    
    cargarEstudiante();
  }, [estudianteId, apiUrl]);

  useEffect(() => {
    // Cargar datos existentes del estudiante
    if (estudiante) {
      setFormData({
        tiene_alojamiento: estudiante.tiene_alojamiento,
        tipo_alojamiento: estudiante.tipo_alojamiento || '',
        direccion_alojamiento: estudiante.direccion_alojamiento || '',
        contacto_alojamiento: estudiante.contacto_alojamiento || '',
        telefono_alojamiento: estudiante.telefono_alojamiento || '',
        precio_mensual: estudiante.precio_mensual || '',
        moneda_alojamiento: estudiante.moneda_alojamiento || 'EUR',
        gestion_solicitada: estudiante.gestion_solicitada || false,
        comentarios_alojamiento: estudiante.comentarios_alojamiento || ''
      });
    }
  }, [estudiante]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const dataToSend = {
        estudiante_id: estudiante.id,
        ...formData
      };

      await axios.post(`${apiUrl}/api/estudiantes/informacion-alojamiento`, dataToSend);
      
      alert('✅ Información de alojamiento guardada correctamente');
      setEditing(false);
      setModoEdicion(false); // Salir del modo edición después de guardar
      
      // Redirigir al dashboard
      setTimeout(() => {
        window.location.href = '/estudiante/dashboard';
      }, 500);
      
    } catch (error) {
      console.error('Error guardando información de alojamiento:', error);
      alert('❌ Error: ' + (error.response?.data?.detail || 'No se pudo guardar la información'));
    } finally {
      setLoading(false);
    }
  };

  const tieneAlojamientoCompleto = formData.tiene_alojamiento !== null && 
    (formData.tiene_alojamiento === true ? 
      (formData.direccion_alojamiento && formData.tipo_alojamiento) : 
      formData.gestion_solicitada
    );

  if (!estudiante && !estudianteId) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <p style={{ color: '#dc2626', marginBottom: '20px' }}>No se pudo identificar el estudiante</p>
        <button
          onClick={() => window.location.href = '/estudiante/dashboard'}
          style={{
            padding: '10px 20px',
            background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontWeight: '600',
            cursor: 'pointer'
          }}
        >
          ← Volver al Dashboard
        </button>
      </div>
    );
  }

  if (!estudiante) {
    return <div style={{ textAlign: 'center', padding: '50px' }}>Cargando información del estudiante...</div>;
  }

  return (
    <div style={{
      maxWidth: '800px',
      margin: '0 auto',
      padding: '20px',
      backgroundColor: '#fff',
      borderRadius: '12px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        marginBottom: '30px',
        paddingBottom: '20px',
        borderBottom: '2px solid #e5e7eb'
      }}>
        <button
          onClick={() => navigate('/estudiante/dashboard')}
          style={{
            background: 'none',
            border: 'none',
            fontSize: '24px',
            cursor: 'pointer',
            marginRight: '15px'
          }}
        >
          ← 
        </button>
        <div>
          <h1 style={{
            color: '#1f2937',
            fontSize: '28px',
            fontWeight: 'bold',
            margin: '0 0 8px 0'
          }}>
            🏠 Información de Alojamiento
          </h1>
          <p style={{
            color: '#6b7280',
            margin: 0,
            fontSize: '16px'
          }}>
            Gestiona tu situación de alojamiento para la estadía en España
          </p>
        </div>
      </div>

      {/* Vista de estado procesado */}
      {estadoAlojamiento && estadoAlojamiento !== 'pendiente' && !modoEdicion ? (
        <div>
          {/* Estado de la solicitud */}
          <div style={{
            padding: '30px',
            backgroundColor: estadoAlojamiento === 'aprobado' ? '#d1fae5' : '#fee2e2',
            border: `3px solid ${estadoAlojamiento === 'aprobado' ? '#10b981' : '#ef4444'}`,
            borderRadius: '15px',
            textAlign: 'center',
            marginBottom: '25px'
          }}>
            <div style={{
              fontSize: '48px',
              marginBottom: '15px'
            }}>
              {estadoAlojamiento === 'aprobado' ? '✅' : '❌'}
            </div>
            <h2 style={{
              color: estadoAlojamiento === 'aprobado' ? '#065f46' : '#991b1b',
              fontSize: '24px',
              fontWeight: '700',
              marginBottom: '10px'
            }}>
              Solicitud de Gestión de Alojamiento {estadoAlojamiento === 'aprobado' ? 'APROBADA' : 'RECHAZADA'}
            </h2>
            <p style={{
              color: estadoAlojamiento === 'aprobado' ? '#047857' : '#dc2626',
              fontSize: '16px',
              margin: 0
            }}>
              {estadoAlojamiento === 'aprobado' 
                ? 'Tu solicitud ha sido aprobada por nuestro equipo' 
                : 'Tu solicitud ha sido rechazada por nuestro equipo'
              }
            </p>
          </div>

          {/* Comentarios del admin */}
          {comentariosAdmin && (
            <div style={{
              padding: '20px',
              backgroundColor: '#f8fafc',
              border: '2px solid #e2e8f0',
              borderRadius: '10px',
              marginBottom: '25px'
            }}>
              <h3 style={{
                color: '#374151',
                fontSize: '16px',
                fontWeight: '600',
                marginBottom: '10px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                💬 Comentarios del equipo
              </h3>
              <p style={{
                color: '#6b7280',
                fontSize: '14px',
                lineHeight: '1.6',
                margin: 0
              }}>
                {comentariosAdmin}
              </p>
            </div>
          )}

          {/* Botón editar */}
          <div style={{ textAlign: 'center' }}>
            <button
              onClick={() => setModoEdicion(true)}
              style={{
                backgroundColor: '#3b82f6',
                color: 'white',
                border: 'none',
                padding: '12px 30px',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s',
                boxShadow: '0 4px 12px rgba(59, 130, 246, 0.2)'
              }}
            >
              ✏️ Editar Información
            </button>
          </div>
        </div>
      ) : (
        /* Formulario de edición */
        <div>
          {/* Si ya fue procesado, mostrar botón cancelar */}
          {estadoAlojamiento && estadoAlojamiento !== 'pendiente' && (
            <div style={{
              marginBottom: '20px',
              padding: '15px',
              backgroundColor: '#fef3c7',
              border: '2px solid #f59e0b',
              borderRadius: '8px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <span style={{ color: '#92400e', fontWeight: '500' }}>
                ⚠️ Editando solicitud ya procesada
              </span>
              <button
                type="button"
                onClick={() => setModoEdicion(false)}
                style={{
                  backgroundColor: '#6b7280',
                  color: 'white',
                  border: 'none',
                  padding: '8px 16px',
                  borderRadius: '6px',
                  fontSize: '14px',
                  cursor: 'pointer'
                }}
              >
                Cancelar
              </button>
            </div>
          )}

          {/* Status Card */}
          <div style={{
            backgroundColor: tieneAlojamientoCompleto ? '#f0fdf4' : '#fef3c7',
            border: `2px solid ${tieneAlojamientoCompleto ? '#10b981' : '#f59e0b'}`,
            borderRadius: '12px',
            padding: '20px',
            marginBottom: '30px',
            textAlign: 'center'
          }}>
            <div style={{
              fontSize: '48px',
              marginBottom: '10px'
            }}>
              {tieneAlojamientoCompleto ? '✅' : '⚠️'}
            </div>
            <h3 style={{
              color: tieneAlojamientoCompleto ? '#065f46' : '#92400e',
              margin: '0 0 8px 0',
              fontSize: '20px',
              fontWeight: '600'
            }}>
              {tieneAlojamientoCompleto ? 'Alojamiento Completado' : 'Información Pendiente'}
            </h3>
            <p style={{
              color: tieneAlojamientoCompleto ? '#047857' : '#d97706',
              margin: 0,
              fontSize: '16px'
            }}>
              {tieneAlojamientoCompleto 
                ? 'Tu información de alojamiento está completa'
                : 'Completa tu información de alojamiento para continuar'
              }
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit}>
            {/* ¿Tienes alojamiento? */}
            <div style={{
              marginBottom: '30px',
              padding: '20px',
              backgroundColor: '#f8fafc',
              borderRadius: '10px',
              border: '1px solid #e2e8f0'
            }}>
              <h3 style={{ color: '#374151', fontSize: '18px', fontWeight: '600', marginBottom: '15px' }}>
                🏠 ¿Tienes alojamiento en España?
              </h3>
              
              <div style={{ display: 'flex', gap: '20px' }}>
                <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                  <input
                    type="radio"
                    name="tiene_alojamiento"
                    value="true"
                    checked={formData.tiene_alojamiento === true}
                    onChange={() => setFormData({...formData, tiene_alojamiento: true, gestion_solicitada: false})}
                    style={{ marginRight: '8px' }}
                  />
                  ✅ Sí, ya tengo alojamiento
                </label>
                <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                  <input
                    type="radio"
                    name="tiene_alojamiento"
                    value="false"
                    checked={formData.tiene_alojamiento === false}
                    onChange={() => setFormData({...formData, tiene_alojamiento: false, gestion_solicitada: true})}
                    style={{ marginRight: '8px' }}
                  />
                  ❌ No, necesito ayuda para conseguir uno
                </label>
              </div>
            </div>

            {/* Si tiene alojamiento - mostrar detalles */}
            {formData.tiene_alojamiento === true && (
              <div style={{
                marginBottom: '30px',
                padding: '20px',
                backgroundColor: '#f0fdf4',
                borderRadius: '10px',
                border: '1px solid #bbf7d0'
              }}>
                <h4 style={{ color: '#065f46', fontSize: '16px', fontWeight: '600', marginBottom: '15px' }}>
                  Detalles de tu alojamiento actual
                </h4>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '15px' }}>
                  <div>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151' }}>
                      Tipo de alojamiento:
                    </label>
                    <select
                      value={formData.tipo_alojamiento}
                      onChange={(e) => setFormData({...formData, tipo_alojamiento: e.target.value})}
                      style={{
                        width: '100%',
                        padding: '10px',
                        border: '1px solid #d1d5db',
                        borderRadius: '6px',
                        fontSize: '14px'
                      }}
                    >
                      <option value="">Selecciona...</option>
                      <option value="piso_compartido">Piso compartido</option>
                      <option value="residencia">Residencia universitaria</option>
                      <option value="familia_anfitriona">Familia anfitriona</option>
                      <option value="apartamento_privado">Apartamento privado</option>
                      <option value="otros">Otros</option>
                    </select>
                  </div>
                  
                  <div>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151' }}>
                      Precio mensual:
                    </label>
                    <div style={{ display: 'flex', gap: '10px' }}>
                      <input
                        type="number"
                        value={formData.precio_mensual}
                        onChange={(e) => setFormData({...formData, precio_mensual: e.target.value})}
                        placeholder="400"
                        style={{
                          flex: 1,
                          padding: '10px',
                          border: '1px solid #d1d5db',
                          borderRadius: '6px',
                          fontSize: '14px'
                        }}
                      />
                      <select
                        value={formData.moneda_alojamiento}
                        onChange={(e) => setFormData({...formData, moneda_alojamiento: e.target.value})}
                        style={{
                          padding: '10px',
                          border: '1px solid #d1d5db',
                          borderRadius: '6px',
                          fontSize: '14px',
                          width: '80px'
                        }}
                      >
                        <option value="EUR">EUR</option>
                        <option value="USD">USD</option>
                        <option value="CUP">CUP</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div style={{ marginBottom: '15px' }}>
                  <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151' }}>
                    Dirección completa:
                  </label>
                  <input
                    type="text"
                    value={formData.direccion_alojamiento}
                    onChange={(e) => setFormData({...formData, direccion_alojamiento: e.target.value})}
                    placeholder="Calle, número, ciudad, código postal"
                    style={{
                      width: '100%',
                      padding: '10px',
                      border: '1px solid #d1d5db',
                      borderRadius: '6px',
                      fontSize: '14px'
                    }}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                  <div>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151' }}>
                      Contacto del alojamiento:
                    </label>
                    <input
                      type="text"
                      value={formData.contacto_alojamiento}
                      onChange={(e) => setFormData({...formData, contacto_alojamiento: e.target.value})}
                      placeholder="Nombre del propietario o responsable"
                      style={{
                        width: '100%',
                        padding: '10px',
                        border: '1px solid #d1d5db',
                        borderRadius: '6px',
                        fontSize: '14px'
                      }}
                    />
                  </div>
                  
                  <div>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500', color: '#374151' }}>
                      Teléfono del alojamiento:
                    </label>
                    <input
                      type="tel"
                      value={formData.telefono_alojamiento}
                      onChange={(e) => setFormData({...formData, telefono_alojamiento: e.target.value})}
                      placeholder="+34 XXX XXX XXX"
                      style={{
                        width: '100%',
                        padding: '10px',
                        border: '1px solid #d1d5db',
                        borderRadius: '6px',
                        fontSize: '14px'
                      }}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Si NO tiene alojamiento - mostrar mensaje de gestión */}
            {formData.tiene_alojamiento === false && (
              <div style={{
                marginBottom: '30px',
                padding: '20px',
                backgroundColor: '#fffbeb',
                borderRadius: '10px',
                border: '1px solid #fbbf24'
              }}>
                <h4 style={{ color: '#92400e', fontSize: '16px', fontWeight: '600', marginBottom: '10px' }}>
                  🏠 Gestión de Alojamiento
                </h4>
                <p style={{ color: '#78350f', fontSize: '14px', marginBottom: '15px' }}>
                  Nuestro equipo te ayudará a encontrar el alojamiento más adecuado para tu estancia en España. 
                  Te contactaremos con opciones que se ajusten a tu presupuesto y preferencias.
                </p>
                <div style={{ backgroundColor: '#f59e0b', color: 'white', padding: '10px', borderRadius: '6px', textAlign: 'center', fontWeight: '600' }}>
                  ✅ Gestión de alojamiento solicitada
                </div>
              </div>
            )}

            {/* Comentarios adicionales */}
            <div style={{
              marginBottom: '30px',
              padding: '20px',
              backgroundColor: '#f8fafc',
              borderRadius: '10px',
              border: '1px solid #e2e8f0'
            }}>
              <label style={{ display: 'block', marginBottom: '10px', fontWeight: '500', color: '#374151' }}>
                📝 Comentarios adicionales (opcional):
              </label>
              <textarea
                value={formData.comentarios_alojamiento}
                onChange={(e) => setFormData({...formData, comentarios_alojamiento: e.target.value})}
                placeholder="Preferencias de ubicación, necesidades especiales, mascotas, etc."
                rows="3"
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '1px solid #d1d5db',
                  borderRadius: '6px',
                  fontSize: '14px',
                  resize: 'vertical'
                }}
              />
            </div>

            {/* Botones */}
            {editing ? (
              <>
                <button
                  type="button"
                  onClick={() => setEditing(false)}
                  style={{
                    padding: '12px 24px',
                    backgroundColor: '#6b7280',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    marginRight: '10px'
                  }}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  style={{
                    padding: '12px 24px',
                    backgroundColor: loading ? '#9ca3af' : '#10b981',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: '600',
                    cursor: loading ? 'not-allowed' : 'pointer'
                  }}
                >
                  {loading ? 'Guardando...' : '💾 Guardar Información'}
                </button>
              </>
            ) : (
              <button
                type="button"
                onClick={() => setEditing(true)}
                style={{
                  padding: '12px 24px',
                  backgroundColor: '#3b82f6',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: 'pointer'
                }}
              >
                ✏️ Editar Información
              </button>
            )}
          </form>
        </div>
      )}
    </div>
  );
};

export default InformacionAlojamiento;