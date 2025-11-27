import React, { useState, useEffect } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import './AdminDocumentos.css';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://botvisa-production.up.railway.app';

const CATEGORIAS = {
  pasaporte: { nombre: 'Pasaporte', icono: '📘' },
  visa: { nombre: 'Visa', icono: '🛂' },
  academicos: { nombre: 'Académicos', icono: '🎓' },
  financieros: { nombre: 'Financieros', icono: '💰' },
  otros: { nombre: 'Otros', icono: '📄' }
};

const AdminDocumentos = () => {
  const [estudiantes, setEstudiantes] = useState([]);
  const [estudianteSeleccionado, setEstudianteSeleccionado] = useState(null);
  const [documentos, setDocumentos] = useState([]);
  const [previsualizando, setPrevisualizando] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [modalRevision, setModalRevision] = useState(null);
  const [comentario, setComentario] = useState('');
  const [procesando, setProcesando] = useState(false);
  const [busqueda, setBusqueda] = useState('');

  useEffect(() => {
    cargarEstudiantes();
  }, []);

  useEffect(() => {
    if (estudianteSeleccionado) {
      cargarDocumentos(estudianteSeleccionado.id);
    }
  }, [estudianteSeleccionado]);

  const cargarEstudiantes = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/admin/documentos/todos`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      
      if (data.success) {
        setEstudiantes(data.estudiantes);
      }
    } catch (error) {
      console.error('❌ Error cargando estudiantes:', error);
    }
  };

  const cargarDocumentos = async (estudianteId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/documentos/${estudianteId}/listar`);
      const data = await response.json();
      
      if (data.success) {
        setDocumentos(data.documentos);
      }
    } catch (error) {
      console.error('❌ Error cargando documentos:', error);
    }
  };

  const abrirModalRevision = (doc, estado) => {
    setModalRevision({ doc, estado });
    setComentario('');
  };

  const cerrarModalRevision = () => {
    setModalRevision(null);
    setComentario('');
  };

  const revisarDocumento = async () => {
    if (!modalRevision) return;
    
    setProcesando(true);
    
    try {
      const token = localStorage.getItem('token');
      const formData = new FormData();
      formData.append('estado', modalRevision.estado);
      formData.append('comentario', comentario);
      
      const response = await fetch(`${API_BASE_URL}/api/admin/documentos/${modalRevision.doc.id}/revisar`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });
      
      const data = await response.json();
      
      if (data.success) {
        alert(`✅ Documento ${modalRevision.estado} correctamente`);
        cargarDocumentos(estudianteSeleccionado.id);
        cargarEstudiantes();
        cerrarModalRevision();
      } else {
        alert('❌ Error revisando documento');
      }
    } catch (error) {
      console.error('❌ Error:', error);
      alert('❌ Error revisando documento');
    } finally {
      setProcesando(false);
    }
  };

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
    if (!estudianteSeleccionado) return;
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/documentos/${estudianteSeleccionado.id}/descargar-zip`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `estudiante_${estudianteSeleccionado.id}_documentos.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('❌ Error descargando ZIP:', error);
    }
  };

  const abrirPreview = (doc) => {
    setPrevisualizando(doc);
  };

  const cerrarPreview = () => {
    setPrevisualizando(null);
    setNumPages(null);
  };

  const estudiantesFiltrados = estudiantes.filter(est => 
    est.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
    est.email.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div className="admin-documentos">
      <h1>📂 Gestión de Documentos</h1>
      
      <div className="layout-documentos">
        {/* Panel izquierdo: Lista estudiantes */}
        <div className="panel-estudiantes">
          <div className="panel-header">
            <h3>Estudiantes ({estudiantes.length})</h3>
            <input
              type="text"
              placeholder="Buscar..."
              value={busqueda}
              onChange={(e) => setBusqueda(e.target.value)}
              className="input-busqueda"
            />
          </div>
          
          <div className="lista-estudiantes">
            {estudiantesFiltrados.map(est => (
              <div
                key={est.id}
                className={`estudiante-item ${estudianteSeleccionado?.id === est.id ? 'activo' : ''}`}
                onClick={() => setEstudianteSeleccionado(est)}
              >
                <div className="estudiante-info">
                  <h4>{est.nombre}</h4>
                  <p>{est.email}</p>
                </div>
                <div className="estudiante-badges">
                  <span className="badge total">{est.total_documentos} docs</span>
                  {est.pendientes > 0 && (
                    <span className="badge pendiente">{est.pendientes} ⏳</span>
                  )}
                  {est.aprobados > 0 && (
                    <span className="badge aprobado">{est.aprobados} ✅</span>
                  )}
                  {est.rechazados > 0 && (
                    <span className="badge rechazado">{est.rechazados} ❌</span>
                  )}
                </div>
              </div>
            ))}
            
            {estudiantesFiltrados.length === 0 && (
              <div className="empty-state-panel">
                <p>No se encontraron estudiantes</p>
              </div>
            )}
          </div>
        </div>

        {/* Panel derecho: Documentos del estudiante */}
        <div className="panel-documentos">
          {estudianteSeleccionado ? (
            <>
              <div className="panel-header">
                <div>
                  <h3>{estudianteSeleccionado.nombre}</h3>
                  <p>{estudianteSeleccionado.email}</p>
                </div>
                <button onClick={descargarTodoZIP} className="btn-descargar-zip">
                  📦 Descargar Todo
                </button>
              </div>
              
              {documentos.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-icono">📭</div>
                  <p>Este estudiante no ha subido documentos</p>
                </div>
              ) : (
                <div className="documentos-grid">
                  {documentos.map(doc => (
                    <div key={doc.id} className="documento-card-admin">
                      <div className="documento-header">
                        <div className="documento-icono">
                          {doc.mime_type.includes('pdf') ? '📄' : '🖼️'}
                        </div>
                        <div className="documento-info">
                          <h4>{doc.nombre}</h4>
                          <span className="documento-categoria">
                            {CATEGORIAS[doc.categoria]?.icono} {CATEGORIAS[doc.categoria]?.nombre}
                          </span>
                        </div>
                      </div>
                      
                      <div className={`documento-estado ${doc.estado_revision}`}>
                        {doc.estado_revision === 'aprobado' && '✅ Aprobado'}
                        {doc.estado_revision === 'rechazado' && '❌ Rechazado'}
                        {doc.estado_revision === 'pendiente' && '⏳ Pendiente Revisión'}
                      </div>
                      
                      {doc.comentario_admin && (
                        <div className="documento-comentario">
                          <strong>Tu comentario:</strong>
                          <p>{doc.comentario_admin}</p>
                        </div>
                      )}
                      
                      <div className="documento-meta">
                        <span>{(doc.tamano / 1024).toFixed(2)} KB</span>
                        <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                      </div>
                      
                      <div className="documento-acciones">
                        {doc.mime_type === 'application/pdf' && (
                          <button onClick={() => abrirPreview(doc)} className="btn-action preview">
                            👁️ Ver
                          </button>
                        )}
                        <button onClick={() => descargarDocumento(doc.id, doc.nombre)} className="btn-action download">
                          ⬇️
                        </button>
                        <button 
                          onClick={() => abrirModalRevision(doc, 'aprobado')} 
                          className="btn-action aprobar"
                          disabled={doc.estado_revision === 'aprobado'}
                        >
                          ✅ Aprobar
                        </button>
                        <button 
                          onClick={() => abrirModalRevision(doc, 'rechazado')} 
                          className="btn-action rechazar"
                          disabled={doc.estado_revision === 'rechazado'}
                        >
                          ❌ Rechazar
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          ) : (
            <div className="empty-state">
              <div className="empty-icono">👈</div>
              <p>Selecciona un estudiante para ver sus documentos</p>
            </div>
          )}
        </div>
      </div>

      {/* Modal Revisión */}
      {modalRevision && (
        <div className="modal-overlay" onClick={cerrarModalRevision}>
          <div className="modal-revision" onClick={(e) => e.stopPropagation()}>
            <h3>
              {modalRevision.estado === 'aprobado' ? '✅ Aprobar' : '❌ Rechazar'} Documento
            </h3>
            <p className="modal-doc-nombre">{modalRevision.doc.nombre}</p>
            
            <div className="form-group">
              <label>Comentario {modalRevision.estado === 'rechazado' && '(Requerido)'}:</label>
              <textarea
                value={comentario}
                onChange={(e) => setComentario(e.target.value)}
                placeholder={modalRevision.estado === 'aprobado' 
                  ? 'Agregar un comentario opcional...' 
                  : 'Especifica qué debe corregir el estudiante...'
                }
                rows={4}
                className="textarea-comentario"
              />
            </div>
            
            <div className="modal-acciones">
              <button onClick={cerrarModalRevision} className="btn-cancelar" disabled={procesando}>
                Cancelar
              </button>
              <button 
                onClick={revisarDocumento} 
                className={`btn-confirmar ${modalRevision.estado}`}
                disabled={procesando || (modalRevision.estado === 'rechazado' && !comentario.trim())}
              >
                {procesando ? 'Procesando...' : 'Confirmar'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal Preview PDF */}
      {previsualizando && previsualizando.mime_type === 'application/pdf' && (
        <div className="modal-preview" onClick={cerrarPreview}>
          <div className="modal-content-preview" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header-preview">
              <h3>{previsualizando.nombre}</h3>
              <button onClick={cerrarPreview} className="btn-cerrar">✖️</button>
            </div>
            <div className="modal-body-preview">
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

export default AdminDocumentos;
