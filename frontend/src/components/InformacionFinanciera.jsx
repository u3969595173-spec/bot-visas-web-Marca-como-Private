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

  useEffect(() => {
    cargarDatos();
  }, [estudianteId]);

  const cargarDatos = async () => {
    try {
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}`);
      setEstudiante(response.data);
      setFormData({
        fondos_disponibles: response.data.fondos_disponibles || '',
        moneda_fondos: response.data.moneda_fondos || 'EUR',
        patrocinador_nombre: response.data.patrocinador_nombre || '',
        patrocinador_relacion: response.data.patrocinador_relacion || '',
        patrocinio_solicitado: response.data.patrocinio_solicitado || false
      });
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
        <h2 style={{ margin: 0, color: '#2d3748' }}>
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


      </div>
    </div>
  );
};

export default InformacionFinanciera;