import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './ChecklistDocumentos.css'

function ChecklistDocumentos({ estudianteId }) {
  const [documentos, setDocumentos] = useState([])
  const [documentosGenerados, setDocumentosGenerados] = useState([])
  const [serviciosSolicitados, setServiciosSolicitados] = useState([])
  const [loading, setLoading] = useState(true)

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const documentosRequeridos = [
    { id: 'titulo', nombre: 'Título Universitario', descripcion: 'Copia certificada de tu título', requerido: true },
    { id: 'pasaporte', nombre: 'Pasaporte', descripcion: 'Copia de tu pasaporte vigente', requerido: true },
    { id: 'extracto', nombre: 'Extracto Bancario', descripcion: 'Comprobante de fondos suficientes', requerido: true },
    { id: 'antecedentes', nombre: '📋 Antecedentes Penales', descripcion: 'Solicita este servicio - Listos y legalizados en 30 días hábiles', requerido: false, servicio: true },
    { id: 'cita_embajada', nombre: '🏛️ Cita en Embajada', descripcion: 'Solicita este servicio - Gestionamos tu cita consular', requerido: false, servicio: true },
    { id: 'foto', nombre: 'Fotografía', descripcion: 'Foto tamaño pasaporte', requerido: false },
    { id: 'seguro', nombre: 'Seguro Médico', descripcion: 'Seguro de salud internacional', requerido: false }
  ]

  const documentosOficialesEsperados = [
    { id: 'carta_aceptacion', nombre: 'Carta de Aceptación', descripcion: 'Generada por el sistema' },
    { id: 'carta_motivacion', nombre: 'Carta de Motivación', descripcion: 'Generada por el sistema' },
    { id: 'formulario_solicitud', nombre: 'Formulario de Solicitud', descripcion: 'Generado por el sistema' },
    { id: 'certificado_matricula', nombre: 'Certificado de Matrícula', descripcion: 'Generado por el sistema' }
  ]

  useEffect(() => {
    cargarDocumentos()
    cargarServiciosSolicitados()
  }, [])

  const cargarDocumentos = async () => {
    try {
      const [resSubidos, resGenerados] = await Promise.all([
        axios.get(`${apiUrl}/api/estudiantes/${estudianteId}/documentos`),
        axios.get(`${apiUrl}/api/estudiantes/${estudianteId}/documentos-generados`)
      ])
      setDocumentos(resSubidos.data.documentos || [])
      setDocumentosGenerados(resGenerados.data || [])
    } catch (err) {
      console.error('Error cargando documentos:', err)
    } finally {
      setLoading(false)
    }
  }

  const cargarServiciosSolicitados = async () => {
    try {
      const res = await axios.get(`${apiUrl}/api/estudiantes/${estudianteId}/servicios-solicitados`)
      setServiciosSolicitados(res.data.servicios || [])
    } catch (err) {
      console.error('Error cargando servicios:', err)
    }
  }

  const solicitarServicio = async (servicioId, servicioNombre) => {
    try {
      await axios.post(`${apiUrl}/api/estudiantes/${estudianteId}/solicitar-servicio`, {
        servicio_id: servicioId,
        servicio_nombre: servicioNombre
      })
      alert(`✅ Solicitud de "${servicioNombre}" enviada. El administrador te contactará con el precio.`)
      cargarServiciosSolicitados()
    } catch (err) {
      alert('Error al solicitar servicio')
    }
  }

  const calcularProgreso = () => {
    const totalRequeridos = documentosRequeridos.filter(d => d.requerido).length
    const subidos = documentos.length
    const generados = documentosGenerados.filter(d => d.estado === 'aprobado').length
    const total = subidos + generados
    const maxTotal = totalRequeridos + documentosOficialesEsperados.length
    return Math.round((total / maxTotal) * 100)
  }

  const tieneDocumento = (tipoId) => {
    return documentos.some(d => d.tipo_documento?.toLowerCase().includes(tipoId))
  }

  const tieneDocumentoGenerado = (tipoId) => {
    return documentosGenerados.some(d => 
      d.tipo_documento === tipoId && d.estado === 'aprobado'
    )
  }

  const servicioSolicitado = (servicioId) => {
    return serviciosSolicitados.some(s => s.servicio_id === servicioId)
  }

  const progreso = calcularProgreso()
  const docsSubidos = documentos.length
  const docsRequeridos = documentosRequeridos.filter(d => d.requerido).length
  const docsGeneradosAprobados = documentosGenerados.filter(d => d.estado === 'aprobado').length

  if (loading) {
    return <div className="checklist-loading">Cargando documentos...</div>
  }

  return (
    <div className="checklist-documentos">
      <div className="checklist-header">
        <h2>📋 Checklist de Documentos</h2>
        <div className="progreso-general">
          <div className="progreso-bar-container">
            <div 
              className="progreso-bar-fill" 
              style={{ width: `${progreso}%` }}
            />
          </div>
          <span className="progreso-porcentaje">{progreso}% Completado</span>
        </div>
      </div>

      <div className="resumen-cards">
        <div className="resumen-card">
          <div className="resumen-numero">{docsSubidos}</div>
          <div className="resumen-label">Documentos Subidos</div>
          <div className="resumen-detalle">de {docsRequeridos} requeridos</div>
        </div>
        <div className="resumen-card">
          <div className="resumen-numero">{docsGeneradosAprobados}</div>
          <div className="resumen-label">Documentos Aprobados</div>
          <div className="resumen-detalle">generados por el sistema</div>
        </div>
        <div className={`resumen-card ${progreso === 100 ? 'completo' : ''}`}>
          <div className="resumen-numero">{progreso}%</div>
          <div className="resumen-label">Progreso Total</div>
          <div className="resumen-detalle">
            {progreso === 100 ? '¡Completado!' : 'En proceso'}
          </div>
        </div>
      </div>

      <div className="checklist-seccion">
        <h3>Documentos que debes Subir</h3>
        <div className="checklist-lista">
          {documentosRequeridos.map(doc => {
            const subido = tieneDocumento(doc.id)
            const esServicio = doc.servicio === true
            const yasolicitado = servicioSolicitado(doc.id)
            return (
              <div key={doc.id} className={`checklist-item ${subido ? 'completado' : ''} ${esServicio ? 'item-servicio' : ''} ${yasolicitado ? 'servicio-solicitado' : ''}`}>
                <div className="checklist-icon">
                  {subido ? '✓' : yasolicitado ? '⏳' : doc.requerido ? '!' : '○'}
                </div>
                <div className="checklist-info">
                  <div className="checklist-nombre">
                    {doc.nombre}
                    {doc.requerido && <span className="badge-requerido">Requerido</span>}
                    {esServicio && <span className="badge-servicio">Servicio</span>}
                  </div>
                  <div className="checklist-descripcion">{doc.descripcion}</div>
                </div>
                <div className="checklist-estado">
                  {subido ? (
                    <span className="estado-badge estado-ok">✓ Subido</span>
                  ) : yasolicitado ? (
                    <span className="estado-badge estado-proceso">⏳ Solicitado</span>
                  ) : esServicio ? (
                    <button 
                      className="btn-solicitar-servicio"
                      onClick={() => solicitarServicio(doc.id, doc.nombre)}
                    >
                      💼 Solicitar
                    </button>
                  ) : (
                    <span className="estado-badge estado-pendiente">Pendiente</span>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      <div className="checklist-seccion">
        <h3>Documentos Oficiales (Generados por Administración)</h3>
        <div className="checklist-lista">
          {documentosOficialesEsperados.map(doc => {
            const generado = tieneDocumentoGenerado(doc.id)
            return (
              <div key={doc.id} className={`checklist-item ${generado ? 'completado' : 'pendiente-admin'}`}>
                <div className="checklist-icon">
                  {generado ? '✓' : '⏳'}
                </div>
                <div className="checklist-info">
                  <div className="checklist-nombre">{doc.nombre}</div>
                  <div className="checklist-descripcion">{doc.descripcion}</div>
                </div>
                <div className="checklist-estado">
                  {generado ? (
                    <span className="estado-badge estado-ok">✓ Aprobado</span>
                  ) : (
                    <span className="estado-badge estado-proceso">En revisión</span>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {progreso < 100 && (
        <div className="checklist-ayuda">
          <h4>💡 Próximos Pasos:</h4>
          <ul>
            {docsSubidos < docsRequeridos && (
              <li>Sube los documentos requeridos desde la sección "Mis Documentos"</li>
            )}
            {docsGeneradosAprobados === 0 && (
              <li>Espera a que el equipo revise tu solicitud y genere los documentos oficiales</li>
            )}
            {docsSubidos >= docsRequeridos && docsGeneradosAprobados < 4 && (
              <li>Tu expediente está en revisión. Te notificaremos cuando los documentos estén listos</li>
            )}
          </ul>
        </div>
      )}
    </div>
  )
}

export default ChecklistDocumentos
