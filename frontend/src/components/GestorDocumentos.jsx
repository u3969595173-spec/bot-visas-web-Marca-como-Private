import React, { useState, useEffect, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Document, Page, pdfjs } from 'react-pdf';
import './GestorDocumentos.css';

// Configurar worker de PDF.js
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://botvisa-production.up.railway.app';

const CATEGORIAS = [
  { id: 'pasaporte', nombre: 'Pasaporte', icono: '📘', descripcion: 'Copia del pasaporte vigente' },
  { id: 'visa', nombre: 'Visa', icono: '🛂', descripcion: 'Solicitud de visa y documentos relacionados' },
  { id: 'academicos', nombre: 'Académicos', icono: '🎓', descripcion: 'Títulos, certificados, transcripciones' },
  { id: 'financieros', nombre: 'Financieros', icono: '💰', descripcion: 'Extractos bancarios, cartas de solvencia' },
  { id: 'otros', nombre: 'Otros', icono: '📄', descripcion: 'Otros documentos relevantes' }
];

const GestorDocumentos = ({ estudianteId }) => {
  const [documentos, setDocumentos] = useState([]);
  const [progreso, setProgreso] = useState(0);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState('pasaporte');
  const [cargando, setCargando] = useState(false);
  const [previsualizando, setPrevisualizando] = useState(null);
  const [numPages, setNumPages] = useState(null);

  useEffect(() => {
    cargarDocumentos();
  }, [estudianteId]);

  const cargarDocumentos = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/documentos/${estudianteId}/listar`);
      const data = await response.json();
      
      if (data.success) {
        setDocumentos(data.documentos);
        setProgreso(data.progreso);
      }
    } catch (error) {
      console.error('❌ Error cargando documentos:', error);
    }
  };

  const onDrop = useCallback(async (acceptedFiles) => {
    if (!acceptedFiles.length) return;
    
    setCargando(true);
    
    try {
      const formData = new FormData();
      
      // Agregar cada archivo
      acceptedFiles.forEach(file => {
        formData.append('archivos', file);
      });
      
      // Todos los documentos van a categoría "otros" por defecto
      const categoriasStr = acceptedFiles.map(() => 'otros').join(',');
      formData.append('categorias', categoriasStr);
      
      const response = await fetch(`${API_BASE_URL}/api/documentos/${estudianteId}/subir`, {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Error response:', errorText);
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }
      
      const data = await response.json();
      
      if (data.success) {
        alert(`✅ ${data.documentos.length} documento(s) subido(s) correctamente`);
        cargarDocumentos();
      } else {
        alert('❌ Error subiendo documentos: ' + (data.detail || 'Error desconocido'));
      }
    } catch (error) {
      console.error('❌ Error completo:', error);
      alert('❌ Error subiendo documentos: ' + error.message);
    } finally {
      setCargando(false);
    }
  }, [estudianteId, categoriaSeleccionada]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxSize: 10485760, // 10MB
    multiple: true
  });

  const descargarDocumento = async (docId, nombre) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/documentos/${docId}/descargar`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = nombre;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('❌ Error descargando:', error);
    }
  };

  const descargarTodoZIP = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/documentos/${estudianteId}/descargar-zip`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `mis_documentos_${new Date().toISOString().split('T')[0]}.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('❌ Error descargando ZIP:', error);
      alert('❌ Error descargando archivos');
    }
  };

  const eliminarDocumento = async (docId) => {
    if (!confirm('¿Seguro que deseas eliminar este documento?')) return;
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/documentos/${docId}/eliminar`, {
        method: 'DELETE'
      });
      
      const data = await response.json();
      if (data.success) {
        alert('✅ Documento eliminado');
        cargarDocumentos();
      }
    } catch (error) {
      console.error('❌ Error eliminando:', error);
    }
  };

  const abrirPreview = (doc) => {
    setPrevisualizando(doc);
  };

  const cerrarPreview = () => {
    setPrevisualizando(null);
    setNumPages(null);
  };

  const obtenerEstadoClase = (estado) => {
    switch (estado) {
      case 'aprobado': return 'estado-aprobado';
      case 'rechazado': return 'estado-rechazado';
      default: return 'estado-pendiente';
    }
  };

  const obtenerEstadoTexto = (estado) => {
    switch (estado) {
      case 'aprobado': return '✅ Aprobado';
      case 'rechazado': return '❌ Rechazado';
      default: return '⏳ Pendiente';
    }
  };

  const documentosPorCategoria = (categoria) => {
    return documentos.filter(doc => doc.categoria === categoria);
  };

  return (
    <div className="gestor-documentos">
      <div className="header-documentos">
        <h1>📂 Mis Documentos</h1>
        <div className="acciones-header">
          <button className="btn-descargar-zip" onClick={descargarTodoZIP} disabled={documentos.length === 0}>
            📦 Descargar Todo (ZIP)
          </button>
        </div>
      </div>

      {/* Barra de progreso */}
      <div className="progreso-container">
        <div className="progreso-info">
          <span>Progreso de Documentos</span>
          <span className="progreso-porcentaje">{progreso}%</span>
        </div>
        <div className="progreso-barra">
          <div className="progreso-fill" style={{ width: `${progreso}%` }}></div>
        </div>
        <p className="progreso-texto">
          {documentos.length} documento(s) subido(s) • {documentos.filter(d => d.estado_revision === 'aprobado').length} aprobado(s)
        </p>
      </div>

      {/* Cartel informativo */}
      <div style={{
        backgroundColor: '#eff6ff',
        border: '2px solid #3b82f6',
        borderRadius: '12px',
        padding: '24px',
        margin: '20px 0',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '12px' }}>💬</div>
        <h3 style={{ color: '#1e40af', marginBottom: '12px', fontSize: '20px' }}>
          ¿No sabes qué documentos subir?
        </h3>
        <p style={{ color: '#1e3a8a', fontSize: '16px', marginBottom: '16px', lineHeight: '1.6' }}>
          <strong>Contacta con el administrador por chat</strong> para que te indique exactamente qué documentos necesitas subir según tu caso.
        </p>
        <button 
          onClick={() => window.location.href = '/estudiante#mensajes'}
          style={{
            backgroundColor: '#3b82f6',
            color: 'white',
            padding: '12px 32px',
            fontSize: '16px',
            fontWeight: '600',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'all 0.3s'
          }}
          onMouseEnter={(e) => e.target.style.backgroundColor = '#2563eb'}
          onMouseLeave={(e) => e.target.style.backgroundColor = '#3b82f6'}
        >
          💬 Ir al Chat
        </button>
      </div>

      {/* Zona de subida */}
      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'activa' : ''} ${cargando ? 'cargando' : ''}`}>
        <input {...getInputProps()} />
        {cargando ? (
          <div className="dropzone-content">
            <div className="spinner"></div>
            <p>Subiendo archivos...</p>
          </div>
        ) : isDragActive ? (
          <div className="dropzone-content">
            <div className="dropzone-icono">📥</div>
            <p>Suelta los archivos aquí</p>
          </div>
        ) : (
          <div className="dropzone-content">
            <div className="dropzone-icono">☁️</div>
            <p><strong>Arrastra tus documentos aquí</strong> o haz clic para seleccionar</p>
            <span className="dropzone-tipos">PDF, JPG, PNG, DOC, DOCX (máx. 10MB)</span>
          </div>
        )}
      </div>

      {/* Lista de documentos */}
      <div className="documentos-lista">
        <h3>📋 Documentos Subidos ({documentos.length})</h3>
        
        {documentos.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icono">📭</div>
            <p>No has subido documentos aún</p>
            <span>Usa el área de arriba para subir tus archivos</span>
          </div>
        ) : (
          <div className="documentos-grid">
            {documentos.map(doc => (
              <div key={doc.id} className="documento-card">
                <div className="documento-header">
                  <div className="documento-icono">
                    {doc.mime_type?.includes('pdf') ? '📄' : doc.origen === 'generado' ? '✨' : '🖼️'}
                  </div>
                  <div className="documento-info">
                    <h4>{doc.nombre}</h4>
                    {doc.origen === 'generado' && (
                      <span className="documento-categoria" style={{ color: '#10b981', fontWeight: 'bold' }}>
                        ✨ Generado por Admin
                      </span>
                    )}
                  </div>
                </div>
                
                <div className={`documento-estado ${obtenerEstadoClase(doc.estado_revision)}`}>
                  {obtenerEstadoTexto(doc.estado_revision)}
                </div>
                
                {doc.comentario_admin && (
                  <div className="documento-comentario">
                    <strong>Comentario Admin:</strong>
                    <p>{doc.comentario_admin}</p>
                  </div>
                )}
                
                <div className="documento-meta">
                  <span>{(doc.tamano / 1024).toFixed(2)} KB</span>
                  <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                </div>
                
                <div className="documento-acciones">
                  {doc.mime_type === 'application/pdf' && (
                    <button onClick={() => abrirPreview(doc)} className="btn-preview">
                      👁️ Preview
                    </button>
                  )}
                  <button onClick={() => descargarDocumento(doc.id, doc.nombre)} className="btn-descargar">
                    ⬇️ Descargar
                  </button>
                  <button onClick={() => eliminarDocumento(doc.id)} className="btn-eliminar">
                    🗑️
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal Preview PDF */}
      {previsualizando && previsualizando.mime_type === 'application/pdf' && (
        <div className="modal-preview" onClick={cerrarPreview}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{previsualizando.nombre}</h3>
              <button onClick={cerrarPreview} className="btn-cerrar">✖️</button>
            </div>
            <div className="modal-body">
              <Document
                file={`${API_BASE_URL}/api/documentos/${previsualizando.id}/descargar`}
                onLoadSuccess={({ numPages }) => setNumPages(numPages)}
                loading={<div className="spinner"></div>}
              >
                {Array.from(new Array(numPages), (el, index) => (
                  <Page key={`page_${index + 1}`} pageNumber={index + 1} width={800} />
                ))}
              </Document>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestorDocumentos;
