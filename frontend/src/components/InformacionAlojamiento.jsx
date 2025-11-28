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

  const apiUrl = process.env.REACT_APP_API_URL || 'https://bot-visas-api.onrender.com';

  useEffect(() => {
    // Cargar datos del estudiante
    const cargarEstudiante = async () => {
      if (estudianteId) {
        try {
          const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}`);
          setEstudiante(response.data);
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
      
      // Refrescar datos del estudiante
      window.location.reload();
      
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
            marginRight: '15px',
            color: '#6b7280'
          }}
        >
          ←
        </button>
        <div>
          <h2 style={{ margin: 0, color: '#1f2937', fontSize: '24px', fontWeight: '700' }}>
            🏠 Información de Alojamiento
          </h2>
          <p style={{ margin: '5px 0 0 0', color: '#6b7280', fontSize: '16px' }}>
            Gestiona tu situación de alojamiento para la estadía en España
          </p>
        </div>
      </div>

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
            🏠 Situación de Alojamiento
          </h3>
          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
            <label style={{
              display: 'flex',
              alignItems: 'center',
              padding: '15px',
              backgroundColor: formData.tiene_alojamiento === true ? '#dbeafe' : '#fff',
              border: `2px solid ${formData.tiene_alojamiento === true ? '#2563eb' : '#d1d5db'}`,
              borderRadius: '8px',
              cursor: editing ? 'pointer' : 'default',
              fontSize: '16px',
              fontWeight: '500',
              minWidth: '200px'
            }}>
              <input
                type="radio"
                name="tiene_alojamiento"
                value="true"
                checked={formData.tiene_alojamiento === true}
                onChange={() => setFormData(prev => ({...prev, tiene_alojamiento: true, gestion_solicitada: false}))}
                disabled={!editing}
                style={{ marginRight: '10px' }}
              />
              🏡 Ya tengo alojamiento
            </label>
            <label style={{
              display: 'flex',
              alignItems: 'center',
              padding: '15px',
              backgroundColor: formData.tiene_alojamiento === false ? '#fef2f2' : '#fff',
              border: `2px solid ${formData.tiene_alojamiento === false ? '#dc2626' : '#d1d5db'}`,
              borderRadius: '8px',
              cursor: editing ? 'pointer' : 'default',
              fontSize: '16px',
              fontWeight: '500',
              minWidth: '200px'
            }}>
              <input
                type="radio"
                name="tiene_alojamiento"
                value="false"
                checked={formData.tiene_alojamiento === false}
                onChange={() => setFormData(prev => ({...prev, tiene_alojamiento: false, gestion_solicitada: true}))}
                disabled={!editing}
                style={{ marginRight: '10px' }}
              />
              🏢 Necesito que me gestionen
            </label>
          </div>
        </div>

        {/* Datos del alojamiento (si ya tiene) */}
        {formData.tiene_alojamiento === true && (
          <div style={{
            marginBottom: '30px',
            padding: '20px',
            backgroundColor: '#f0fdf4',
            borderRadius: '10px',
            border: '1px solid #bbf7d0'
          }}>
            <h3 style={{ color: '#065f46', fontSize: '18px', fontWeight: '600', marginBottom: '20px' }}>
              📋 Detalles del Alojamiento
            </h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
              <div>
                <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                  Tipo de Alojamiento *
                </label>
                <select
                  value={formData.tipo_alojamiento}
                  onChange={(e) => setFormData(prev => ({...prev, tipo_alojamiento: e.target.value}))}
                  disabled={!editing}
                  required
                  style={{
                    width: '100%',
                    padding: '12px',
                    border: '1px solid #d1d5db',
                    borderRadius: '6px',
                    fontSize: '16px',
                    backgroundColor: editing ? '#fff' : '#f9fafb'
                  }}
                >
                  <option value="">Seleccionar tipo</option>
                  <option value="piso_compartido">Piso Compartido</option>
                  <option value="habitacion_privada">Habitación Privada</option>
                  <option value="apartamento_completo">Apartamento Completo</option>
                  <option value="residencia_estudiantes">Residencia de Estudiantes</option>
                  <option value="familia_anfitriona">Familia Anfitriona</option>
                  <option value="hotel">Hotel/Hostal</option>
                </select>
              </div>
              
              <div style={{ display: 'flex', gap: '10px' }}>
                <div style={{ flex: 1 }}>
                  <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                    Precio Mensual
                  </label>
                  <input
                    type="number"
                    placeholder="800"
                    value={formData.precio_mensual}
                    onChange={(e) => setFormData(prev => ({...prev, precio_mensual: e.target.value}))}
                    disabled={!editing}
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '1px solid #d1d5db',
                      borderRadius: '6px',
                      fontSize: '16px',
                      backgroundColor: editing ? '#fff' : '#f9fafb'
                    }}
                  />
                </div>
                <div style={{ width: '80px' }}>
                  <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                    Moneda
                  </label>
                  <select
                    value={formData.moneda_alojamiento}
                    onChange={(e) => setFormData(prev => ({...prev, moneda_alojamiento: e.target.value}))}
                    disabled={!editing}
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '1px solid #d1d5db',
                      borderRadius: '6px',
                      fontSize: '16px',
                      backgroundColor: editing ? '#fff' : '#f9fafb'
                    }}
                  >
                    <option value="EUR">EUR</option>
                    <option value="USD">USD</option>
                  </select>
                </div>
              </div>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                Dirección Completa *
              </label>
              <input
                type="text"
                placeholder="Calle, número, código postal, ciudad"
                value={formData.direccion_alojamiento}
                onChange={(e) => setFormData(prev => ({...prev, direccion_alojamiento: e.target.value}))}
                disabled={!editing}
                required
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #d1d5db',
                  borderRadius: '6px',
                  fontSize: '16px',
                  backgroundColor: editing ? '#fff' : '#f9fafb'
                }}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div>
                <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                  Contacto del Alojamiento
                </label>
                <input
                  type="text"
                  placeholder="Nombre del propietario/agencia"
                  value={formData.contacto_alojamiento}
                  onChange={(e) => setFormData(prev => ({...prev, contacto_alojamiento: e.target.value}))}
                  disabled={!editing}
                  style={{
                    width: '100%',
                    padding: '12px',
                    border: '1px solid #d1d5db',
                    borderRadius: '6px',
                    fontSize: '16px',
                    backgroundColor: editing ? '#fff' : '#f9fafb'
                  }}
                />
              </div>
              
              <div>
                <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                  Teléfono de Contacto
                </label>
                <input
                  type="tel"
                  placeholder="+34 XXX XXX XXX"
                  value={formData.telefono_alojamiento}
                  onChange={(e) => setFormData(prev => ({...prev, telefono_alojamiento: e.target.value}))}
                  disabled={!editing}
                  style={{
                    width: '100%',
                    padding: '12px',
                    border: '1px solid #d1d5db',
                    borderRadius: '6px',
                    fontSize: '16px',
                    backgroundColor: editing ? '#fff' : '#f9fafb'
                  }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Solicitar gestión (si necesita gestión) */}
        {formData.tiene_alojamiento === false && (
          <div style={{
            marginBottom: '30px',
            padding: '20px',
            backgroundColor: '#fef2f2',
            borderRadius: '10px',
            border: '1px solid #fecaca'
          }}>
            <h3 style={{ color: '#dc2626', fontSize: '18px', fontWeight: '600', marginBottom: '15px' }}>
              🏢 Solicitar Gestión de Alojamiento
            </h3>
            
            <label style={{
              display: 'flex',
              alignItems: 'center',
              padding: '15px',
              backgroundColor: '#fff',
              border: '1px solid #d1d5db',
              borderRadius: '8px',
              marginBottom: '20px',
              cursor: editing ? 'pointer' : 'default'
            }}>
              <input
                type="checkbox"
                name="gestion_solicitada"
                checked={formData.gestion_solicitada}
                onChange={(e) => setFormData(prev => ({...prev, gestion_solicitada: e.target.checked}))}
                disabled={!editing}
                style={{ marginRight: '12px' }}
              />
              <span style={{ fontWeight: '500', color: '#374151' }}>
                Solicito que la empresa me gestione el alojamiento
              </span>
            </label>

            <div>
              <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                Comentarios adicionales o preferencias
              </label>
              <textarea
                placeholder="Describe tus preferencias: zona preferida, presupuesto máximo, tipo de alojamiento deseado..."
                value={formData.comentarios_alojamiento}
                onChange={(e) => setFormData(prev => ({...prev, comentarios_alojamiento: e.target.value}))}
                disabled={!editing}
                rows={4}
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #d1d5db',
                  borderRadius: '6px',
                  fontSize: '16px',
                  backgroundColor: editing ? '#fff' : '#f9fafb',
                  resize: 'vertical'
                }}
              />
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div style={{
          display: 'flex',
          gap: '15px',
          justifyContent: 'flex-end',
          paddingTop: '20px',
          borderTop: '1px solid #e5e7eb'
        }}>
          {!editing ? (
            <button
              type="button"
              onClick={() => setEditing(true)}
              style={{
                padding: '12px 24px',
                backgroundColor: '#2563eb',
                color: '#fff',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
            >
              ✏️ Editar Información
            </button>
          ) : (
            <>
              <button
                type="button"
                onClick={() => {
                  setEditing(false);
                  // Restaurar datos originales
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
                }}
                style={{
                  padding: '12px 24px',
                  backgroundColor: '#6b7280',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: 'pointer'
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
          )}
        </div>
      </form>
    </div>
  );
};

export default InformacionAlojamiento;