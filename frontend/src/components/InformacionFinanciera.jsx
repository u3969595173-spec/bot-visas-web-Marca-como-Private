import React, { useState, useEffect } from 'react';
import axios from 'axios';

const InformacionFinanciera = ({ estudianteId }) => {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const [estudiante, setEstudiante] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    fondos_disponibles: '',
    moneda_fondos: 'EUR',
    patrocinador_nombre: '',
    patrocinador_relacion: '',
    patrocinio_solicitado: false
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [estadoPatrocinio, setEstadoPatrocinio] = useState(null); // pendiente/aprobado/rechazado
  const [comentariosAdmin, setComentariosAdmin] = useState('');

  useEffect(() => {
    if (estudianteId) {
      cargarDatos();
    } else {
      setLoading(false);
      setError('No se pudo identificar el estudiante. Por favor, inicia sesión nuevamente.');
    }
  }, [estudianteId]);

  const cargarDatos = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}`);
      setEstudiante(response.data);
      setFormData({
        fondos_disponibles: response.data.fondos_disponibles || '',
        moneda_fondos: response.data.moneda_fondos || 'EUR',
        patrocinador_nombre: response.data.patrocinador_nombre || '',
        patrocinador_relacion: response.data.patrocinador_relacion || '',
        patrocinio_solicitado: response.data.patrocinio_solicitado || false
      });
      
      // Cargar estado de la gestión por el admin
      setEstadoPatrocinio(response.data.estado_patrocinio || 'pendiente');
      setComentariosAdmin(response.data.comentarios_patrocinio || '');
      
      // Si ya fue procesado por el admin, no mostrar en modo edición por defecto
      if (response.data.estado_patrocinio && response.data.estado_patrocinio !== 'pendiente') {
        setEditing(false);
      }
      
      setLoading(false);
    } catch (err) {
      setError('Error al cargar información financiera');
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSave = async () => {
    try {
      setError('');
      setSuccess('');
      
      const dataToSend = {
        ...formData,
        estudiante_id: estudianteId
      };
      
      await axios.post(`${apiUrl}/api/estudiantes/informacion-financiera`, dataToSend);
      
      setSuccess('✅ Información financiera guardada correctamente');
      setEditing(false);
      cargarDatos();
      
      // Redirigir al dashboard después de 1 segundo
      setTimeout(() => {
        window.location.href = '/estudiante/dashboard';
      }, 1000);
    } catch (err) {
      setError('Error al guardar información financiera: ' + (err.response?.data?.detail || err.message));
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <p>Cargando información financiera...</p>
      </div>
    );
  }

  if (error && !estudiante) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <p style={{ color: '#dc2626', marginBottom: '20px' }}>{error}</p>
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

  return (
    <div style={{
      maxWidth: '800px',
      margin: '0 auto',
      padding: '30px',
      backgroundColor: 'white',
      borderRadius: '15px',
      boxShadow: '0 4px 15px rgba(0,0,0,0.1)'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '30px'
      }}>
        <button
          onClick={() => window.location.href = '/estudiante/dashboard'}
          style={{
            background: 'none',
            border: 'none',
            fontSize: '24px',
            cursor: 'pointer',
            color: '#2d3748'
          }}
          title="Volver al Dashboard"
        >
          ←
        </button>
        <h2 style={{ margin: 0, color: '#2d3748', flex: 1, marginLeft: '15px' }}>
          💸 Información Financiera
        </h2>
        {!editing ? (
          <button
            onClick={() => setEditing(true)}
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
            ✏️ Editar
          </button>
        ) : (
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              onClick={handleSave}
              style={{
                padding: '10px 20px',
                background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              ✅ Guardar
            </button>
            <button
              onClick={() => {
                setEditing(false);
                setError('');
                setSuccess('');
                cargarDatos();
              }}
              style={{
                padding: '10px 20px',
                background: '#6b7280',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              ❌ Cancelar
            </button>
          </div>
        )}
      </div>

      {error && (
        <div style={{
          backgroundColor: '#fee2e2',
          border: '1px solid #fecaca',
          color: '#dc2626',
          padding: '15px',
          borderRadius: '8px',
          marginBottom: '20px'
        }}>
          {error}
        </div>
      )}

      {success && (
        <div style={{
          backgroundColor: '#d1fae5',
          border: '1px solid #a7f3d0',
          color: '#059669',
          padding: '15px',
          borderRadius: '8px',
          marginBottom: '20px'
        }}>
          {success}
        </div>
      )}

      {/* Vista de estado procesado */}
      {estadoPatrocinio && estadoPatrocinio !== 'pendiente' && !editing ? (
        <div>
          {/* Estado de la solicitud */}
          <div style={{
            padding: '30px',
            backgroundColor: estadoPatrocinio === 'aprobado' ? '#d1fae5' : '#fee2e2',
            border: `3px solid ${estadoPatrocinio === 'aprobado' ? '#10b981' : '#ef4444'}`,
            borderRadius: '15px',
            textAlign: 'center',
            marginBottom: '25px'
          }}>
            <div style={{
              fontSize: '48px',
              marginBottom: '15px'
            }}>
              {estadoPatrocinio === 'aprobado' ? '✅' : '❌'}
            </div>
            <h2 style={{
              color: estadoPatrocinio === 'aprobado' ? '#065f46' : '#991b1b',
              fontSize: '24px',
              fontWeight: '700',
              marginBottom: '10px'
            }}>
              Solicitud de Patrocinio {estadoPatrocinio === 'aprobado' ? 'APROBADA' : 'RECHAZADA'}
            </h2>
            <p style={{
              color: estadoPatrocinio === 'aprobado' ? '#047857' : '#dc2626',
              fontSize: '16px',
              margin: 0
            }}>
              {estadoPatrocinio === 'aprobado' 
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
              onClick={() => setEditing(true)}
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
        /* Formulario de edición - contenido existente */

      <div style={{
        display: 'grid',
        gap: '25px'
      }}>
        {/* Fondos Disponibles */}
        <div style={{
          padding: '20px',
          border: '2px solid #e5e7eb',
          borderRadius: '10px',
          backgroundColor: '#f9fafb'
        }}>
          <h3 style={{ margin: '0 0 15px 0', color: '#374151' }}>
            💰 Presupuesto Disponible para la Cita
          </h3>
          
          <div style={{ marginBottom: '15px' }}>
            <label style={{
              display: 'block',
              marginBottom: '5px',
              fontWeight: '600',
              color: '#374151'
            }}>
              Cantidad disponible:
            </label>
            <div style={{ display: 'flex', gap: '10px' }}>
              {editing ? (
                <>
                  <input
                    type="number"
                    name="fondos_disponibles"
                    value={formData.fondos_disponibles}
                    onChange={handleInputChange}
                    placeholder="Ej: 15000"
                    style={{
                      flex: 2,
                      padding: '12px',
                      border: '2px solid #d1d5db',
                      borderRadius: '8px',
                      fontSize: '16px'
                    }}
                  />
                  <select
                    name="moneda_fondos"
                    value={formData.moneda_fondos}
                    onChange={handleInputChange}
                    style={{
                      flex: 1,
                      padding: '12px',
                      border: '2px solid #d1d5db',
                      borderRadius: '8px',
                      fontSize: '16px'
                    }}
                  >
                    <option value="EUR">EUR (Euro)</option>
                    <option value="USD">USD (Dólar)</option>
                    <option value="CUP">CUP (Peso Cubano)</option>
                    <option value="MLC">MLC (Moneda Libremente Convertible)</option>
                  </select>
                </>
              ) : (
                <div style={{
                  padding: '12px',
                  backgroundColor: 'white',
                  border: '2px solid #e5e7eb',
                  borderRadius: '8px',
                  fontSize: '16px',
                  fontWeight: '600',
                  width: '100%'
                }}>
                  {estudiante?.fondos_disponibles && estudiante?.moneda_fondos ? 
                    `${estudiante.fondos_disponibles} ${estudiante.moneda_fondos}` : 
                    'No especificado'}
                </div>
              )}
            </div>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              fontWeight: '600',
              color: '#374151'
            }}>
              {editing ? (
                <input
                  type="checkbox"
                  name="fondos_suficientes"
                  checked={formData.fondos_suficientes}
                  onChange={handleInputChange}
                />
              ) : (
                <span style={{
                  fontSize: '20px'
                }}>
                  {estudiante?.fondos_suficientes ? '✅' : '❌'}
                </span>
              )}
              ¿Este presupuesto es suficiente para cubrir todos los gastos del día de la cita?
            </label>
          </div>
        </div>

        {/* Información de Patrocinador */}
        <div style={{
          padding: '20px',
          border: '2px solid #e5e7eb',
          borderRadius: '10px',
          backgroundColor: '#f9fafb'
        }}>
          <h3 style={{ margin: '0 0 15px 0', color: '#374151' }}>
            👨‍👩‍👧‍👦 Información de Patrocinador
          </h3>

          <div style={{ marginBottom: '15px' }}>
            <label style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              fontWeight: '600',
              color: '#374151',
              marginBottom: '15px'
            }}>
              {editing ? (
                <input
                  type="checkbox"
                  name="tiene_patrocinador"
                  checked={formData.tiene_patrocinador}
                  onChange={handleInputChange}
                />
              ) : (
                <span style={{ fontSize: '20px' }}>
                  {estudiante?.tiene_patrocinador ? '✅' : '❌'}
                </span>
              )}
              ¿Tienes un patrocinador que cubra los gastos?
            </label>
          </div>

          {(editing && formData.tiene_patrocinador) || (!editing && estudiante?.tiene_patrocinador) ? (
            <>
              <div style={{ marginBottom: '15px' }}>
                <label style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: '600',
                  color: '#374151'
                }}>
                  Tipo de patrocinador:
                </label>
                {editing ? (
                  <select
                    name="tipo_patrocinador"
                    value={formData.tipo_patrocinador}
                    onChange={handleInputChange}
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '2px solid #d1d5db',
                      borderRadius: '8px',
                      fontSize: '16px'
                    }}
                  >
                    <option value="">Seleccionar...</option>
                    <option value="familiar">Familiar</option>
                    <option value="empresa">Empresa</option>
                  </select>
                ) : (
                  <div style={{
                    padding: '12px',
                    backgroundColor: 'white',
                    border: '2px solid #e5e7eb',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: '600'
                  }}>
                    {estudiante?.tipo_patrocinador || 'No especificado'}
                  </div>
                )}
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: '600',
                  color: '#374151'
                }}>
                  Nombre del patrocinador:
                </label>
                {editing ? (
                  <input
                    type="text"
                    name="patrocinador_nombre"
                    value={formData.patrocinador_nombre}
                    onChange={handleInputChange}
                    placeholder="Ej: María García"
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '2px solid #d1d5db',
                      borderRadius: '8px',
                      fontSize: '16px'
                    }}
                  />
                ) : (
                  <div style={{
                    padding: '12px',
                    backgroundColor: 'white',
                    border: '2px solid #e5e7eb',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: '600'
                  }}>
                    {estudiante?.patrocinador_nombre || 'No especificado'}
                  </div>
                )}
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: '600',
                  color: '#374151'
                }}>
                  Relación con el patrocinador:
                </label>
                {editing ? (
                  <select
                    name="relacion_patrocinador"
                    value={formData.relacion_patrocinador}
                    onChange={handleInputChange}
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '2px solid #d1d5db',
                      borderRadius: '8px',
                      fontSize: '16px'
                    }}
                  >
                    <option value="">Seleccionar...</option>
                    <option value="Padre">Padre</option>
                    <option value="Madre">Madre</option>
                    <option value="Padres">Padres (ambos)</option>
                    <option value="Abuelo/a">Abuelo/a</option>
                    <option value="Tío/a">Tío/a</option>
                    <option value="Hermano/a">Hermano/a</option>
                    <option value="Empresa">Empresa</option>
                    <option value="Otro">Otro familiar</option>
                  </select>
                ) : (
                  <div style={{
                    padding: '12px',
                    backgroundColor: 'white',
                    border: '2px solid #e5e7eb',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: '600'
                  }}>
                    {estudiante?.patrocinador_relacion || 'No especificado'}
                  </div>
                )}
              </div>

              {/* Información de contacto del patrocinador */}
              <div style={{ marginBottom: '15px' }}>
                <label style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: '600',
                  color: '#374151'
                }}>
                  Teléfono del patrocinador:
                </label>
                {editing ? (
                  <input
                    type="tel"
                    name="telefono_patrocinador"
                    value={formData.telefono_patrocinador}
                    onChange={handleInputChange}
                    placeholder="Ej: +34 612 345 678"
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '2px solid #d1d5db',
                      borderRadius: '8px',
                      fontSize: '16px'
                    }}
                  />
                ) : (
                  <div style={{
                    padding: '12px',
                    backgroundColor: 'white',
                    border: '2px solid #e5e7eb',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: '600'
                  }}>
                    {estudiante?.telefono_patrocinador || 'No especificado'}
                  </div>
                )}
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: '600',
                  color: '#374151'
                }}>
                  Email del patrocinador:
                </label>
                {editing ? (
                  <input
                    type="email"
                    name="email_patrocinador"
                    value={formData.email_patrocinador}
                    onChange={handleInputChange}
                    placeholder="Ej: patrocinador@email.com"
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '2px solid #d1d5db',
                      borderRadius: '8px',
                      fontSize: '16px'
                    }}
                  />
                ) : (
                  <div style={{
                    padding: '12px',
                    backgroundColor: 'white',
                    border: '2px solid #e5e7eb',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: '600'
                  }}>
                    {estudiante?.email_patrocinador || 'No especificado'}
                  </div>
                )}
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: '600',
                  color: '#374151'
                }}>
                  Dirección completa:
                </label>
                {editing ? (
                  <textarea
                    name="direccion_patrocinador"
                    value={formData.direccion_patrocinador}
                    onChange={handleInputChange}
                    placeholder="Dirección completa del patrocinador"
                    rows="3"
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '2px solid #d1d5db',
                      borderRadius: '8px',
                      fontSize: '16px',
                      resize: 'vertical'
                    }}
                  />
                ) : (
                  <div style={{
                    padding: '12px',
                    backgroundColor: 'white',
                    border: '2px solid #e5e7eb',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: '600'
                  }}>
                    {estudiante?.direccion_patrocinador || 'No especificado'}
                  </div>
                )}
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: '600',
                  color: '#374151'
                }}>
                  Ocupación/Trabajo:
                </label>
                {editing ? (
                  <input
                    type="text"
                    name="patrocinador_relacion"
                    value={formData.patrocinador_relacion}
                    onChange={handleInputChange}
                    placeholder="Ej: Ingeniero, Médico, Empresario"
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '2px solid #d1d5db',
                      borderRadius: '8px',
                      fontSize: '16px'
                    }}
                  />
                ) : (
                  <div style={{
                    padding: '12px',
                    backgroundColor: 'white',
                    border: '2px solid #e5e7eb',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: '600'
                  }}>
                    {estudiante?.ocupacion_patrocinador || 'No especificado'}
                  </div>
                )}
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: '600',
                  color: '#374151'
                }}>
                  Ingresos mensuales aproximados:
                </label>
                {editing ? (
                  <input
                    type="text"
                    name="ingresos_patrocinador"
                    value={formData.ingresos_patrocinador}
                    onChange={handleInputChange}
                    placeholder="Ej: 3000€, 50000 CUP, 2500 USD"
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '2px solid #d1d5db',
                      borderRadius: '8px',
                      fontSize: '16px'
                    }}
                  />
                ) : (
                  <div style={{
                    padding: '12px',
                    backgroundColor: 'white',
                    border: '2px solid #e5e7eb',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: '600'
                  }}>
                    {estudiante?.ingresos_patrocinador || 'No especificado'}
                  </div>
                )}
              </div>
            </>
          ) : (
            <div style={{
              textAlign: 'center',
              padding: '20px',
              color: '#6b7280',
              fontStyle: 'italic'
            }}>
              {editing ? 'Marca la casilla si tienes un patrocinador' : 'No tiene patrocinador registrado'}
            </div>
          )}
        </div>

        {/* Gestión de Patrocinio */}
        <div style={{
          padding: '20px',
          border: '2px solid #e5e7eb',
          borderRadius: '10px',
          backgroundColor: '#f9fafb'
        }}>
          <h3 style={{ margin: '0 0 15px 0', color: '#374151' }}>
            🤝 Gestión de Patrocinio
          </h3>

          <div style={{ marginBottom: '15px' }}>
            <label style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              fontWeight: '600',
              color: '#374151'
            }}>
              {editing ? (
                <input
                  type="checkbox"
                  name="patrocinio_solicitado"
                  checked={formData.patrocinio_solicitado}
                  onChange={handleInputChange}
                />
              ) : (
                <span style={{ fontSize: '20px' }}>
                  {estudiante?.patrocinio_solicitado ? '✅' : '❌'}
                </span>
              )}
              ¿Quiere que la empresa le gestione patrocinio?
            </label>
          </div>
        </div>

        {/* Aviso si está editando una solicitud procesada */}
        {estadoPatrocinio && estadoPatrocinio !== 'pendiente' && (
          <div style={{
            marginTop: '20px',
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
              onClick={() => setEditing(false)}
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
      </div>
      )}
    </div>
  );
};

export default InformacionFinanciera;