import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './GestorDocumentos.css';

const GestorDocumentos = ({ estudianteId }) => {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const [documentos, setDocumentos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [tipoDocumento, setTipoDocumento] = useState('pasaporte');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [ocrStatus, setOcrStatus] = useState({});
  const [processingOcr, setProcessingOcr] = useState({});

  const tiposDocumento = [
    { value: 'pasaporte', label: 'Pasaporte' },
    { value: 'foto', label: 'Fotografía' },
    { value: 'certificado_estudios', label: 'Certificado de Estudios' },
    { value: 'carta_aceptacion', label: 'Carta de Aceptación' },
    { value: 'comprobante_fondos', label: 'Comprobante de Fondos' },
    { value: 'seguro_medico', label: 'Seguro Médico' },
    { value: 'antecedentes_penales', label: 'Antecedentes Penales' },
    { value: 'otro', label: 'Otro Documento' }
  ];

  useEffect(() => {
    cargarDocumentos();
    cargarOcrStatus();
  }, [estudianteId]);

  const cargarDocumentos = async () => {
    try {
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}/documentos`);
      setDocumentos(response.data.documentos);
      setLoading(false);
    } catch (err) {
      setError('Error al cargar documentos');
      setLoading(false);
    }
  };

  const cargarOcrStatus = async () => {
    try {
      const response = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}/documentos/ocr-status`);
      const statusMap = {};
      response.data.documentos.forEach(doc => {
        statusMap[doc.id] = {
          procesado: doc.ocr_procesado,
          confianza: doc.nivel_confianza,
          alertas: doc.alertas
        };
      });
      setOcrStatus(statusMap);
    } catch (err) {
      console.error('Error al cargar status OCR:', err);
    }
  };

  const validarConOcr = async (documentoId, tipoDoc) => {
    setProcessingOcr({ ...processingOcr, [documentoId]: true });
    
    try {
      const response = await axios.post(
        `${apiUrl}/api/documentos/${documentoId}/validar-ocr?tipo_documento=${tipoDoc}`
      );
      
      if (response.data.exito) {
        setSuccess(`✅ Documento validado con ${response.data.nivel_confianza}% confianza`);
        cargarOcrStatus();
        setTimeout(() => setSuccess(''), 5000);
      } else {
        setError('Error en validación OCR: ' + response.data.error);
      }
    } catch (err) {
      setError('Error al validar documento: ' + (err.response?.data?.detail || err.message));
    } finally {
      setProcessingOcr({ ...processingOcr, [documentoId]: false });
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validar tamaño
    if (file.size > 5 * 1024 * 1024) {
      setError('El archivo es muy grande. Máximo 5MB');
      return;
    }

    // Validar tipo
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
    if (!allowedTypes.includes(file.type)) {
      setError('Tipo de archivo no permitido. Use PDF, JPG o PNG');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const formData = new FormData();
      formData.append('archivo', file);

      await axios.post(
        `${apiUrl}/api/estudiantes/${estudianteId}/documentos?tipo_documento=${tipoDocumento}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      setSuccess('Documento subido correctamente');
      cargarDocumentos();
      e.target.value = ''; // Reset input
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al subir documento');
    } finally {
      setUploading(false);
    }
  };

  const getEstadoBadge = (estado) => {
    const badges = {
      'pendiente': { class: 'badge-pendiente', text: 'Pendiente' },
      'en_revision': { class: 'badge-revision', text: 'En Revisión' },
      'aprobado': { class: 'badge-aprobado', text: 'Aprobado' },
      'rechazado': { class: 'badge-rechazado', text: 'Rechazado' }
    };
    return badges[estado] || badges['pendiente'];
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const getTipoLabel = (tipo) => {
    const tipoObj = tiposDocumento.find(t => t.value === tipo);
    return tipoObj ? tipoObj.label : tipo;
  };

  if (loading) {
    return (
      <div className="documentos-loading">
        <div className="spinner"></div>
        <p>Cargando documentos...</p>
      </div>
    );
  }

  return (
    <div className="documentos-container">
      <div className="documentos-header">
        <h2>📄 Gestión de Documentos</h2>
        <p>Sube los documentos requeridos para tu solicitud de visa</p>
      </div>

      {success && (
        <div className="alert alert-success">
          ✓ {success}
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          ⚠ {error}
        </div>
      )}

      <div className="upload-section">
        <div className="upload-form">
          <div className="form-group">
            <label>Tipo de Documento</label>
            <select
              value={tipoDocumento}
              onChange={(e) => setTipoDocumento(e.target.value)}
              disabled={uploading}
            >
              {tiposDocumento.map(tipo => (
                <option key={tipo.value} value={tipo.value}>
                  {tipo.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="upload-label">
              {uploading ? (
                <span className="uploading">
                  <div className="upload-spinner"></div>
                  Subiendo...
                </span>
              ) : (
                <>
                  <span className="upload-icon">📤</span>
                  Seleccionar Archivo
                </>
              )}
              <input
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={handleFileUpload}
                disabled={uploading}
                style={{ display: 'none' }}
              />
            </label>
            <p className="upload-hint">
              Formatos permitidos: PDF, JPG, PNG (máx. 5MB)
            </p>
          </div>
        </div>
      </div>

      <div className="documentos-lista">
        <h3>Documentos Subidos ({documentos.length})</h3>

        {documentos.length === 0 ? (
          <div className="documentos-empty">
            <p style={{ fontSize: '48px', marginBottom: '15px' }}>📭</p>
            <p>Aún no has subido ningún documento</p>
            <p style={{ color: '#999', fontSize: '14px' }}>
              Comienza subiendo tu pasaporte y fotografía
            </p>
          </div>
        ) : (
          <div className="documentos-grid">
            {documentos.map((doc) => {
              const badge = getEstadoBadge(doc.estado);
              const ocr = ocrStatus[doc.id] || {};
              const isProcessing = processingOcr[doc.id];
              
              return (
                <div key={doc.id} className="documento-card">
                  <div className="documento-icon">
                    {doc.nombre_archivo.endsWith('.pdf') ? '📄' : '🖼️'}
                  </div>
                  <div className="documento-info">
                    <h4>{getTipoLabel(doc.tipo_documento)}</h4>
                    <p className="documento-nombre">{doc.nombre_archivo}</p>
                    <p className="documento-tamano">{formatFileSize(doc.tamano_bytes)}</p>
                    <span className={`documento-badge ${badge.class}`}>
                      {badge.text}
                    </span>
                    
                    {/* Estado OCR */}
                    {ocr.procesado && (
                      <div className="ocr-status">
                        <div className="ocr-confianza">
                          <strong>Confianza OCR:</strong>
                          <span className={`confianza-${ocr.confianza >= 80 ? 'alta' : ocr.confianza >= 60 ? 'media' : 'baja'}`}>
                            {ocr.confianza}%
                          </span>
                        </div>
                        {ocr.alertas && ocr.alertas.length > 0 && (
                          <div className="ocr-alertas">
                            {ocr.alertas.map((alerta, idx) => (
                              <div key={idx} className="alerta-item">⚠️ {alerta}</div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                    
                    {/* Botón Validar OCR */}
                    {!ocr.procesado && (
                      <button
                        className="btn-validar-ocr"
                        onClick={() => validarConOcr(doc.id, doc.tipo_documento)}
                        disabled={isProcessing}
                      >
                        {isProcessing ? '🔄 Validando...' : '🔍 Validar con OCR'}
                      </button>
                    )}
                    
                    {doc.notas && (
                      <div className="documento-notas">
                        <strong>Notas:</strong> {doc.notas}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <div className="documentos-info">
        <h4>📋 Documentos Requeridos</h4>
        <ul>
          <li>✓ Pasaporte vigente (copia completa)</li>
          <li>✓ Fotografía tamaño pasaporte reciente</li>
          <li>✓ Certificado de estudios previos</li>
          <li>✓ Carta de aceptación de la universidad</li>
          <li>✓ Comprobante de solvencia económica</li>
          <li>✓ Seguro médico internacional</li>
          <li>✓ Certificado de antecedentes penales</li>
        </ul>
      </div>
    </div>
  );
};

export default GestorDocumentos;
