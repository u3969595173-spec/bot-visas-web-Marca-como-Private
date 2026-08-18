import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Platform.css';

function ComoFunciona() {
  const navigate = useNavigate();

  const pasos = [
    {
      numero: 1,
      titulo: 'Elige la operación',
      descripcion: 'Revisa el catálogo de operaciones activas con sus condiciones, capital requerido, plazo estimado y nivel de riesgo. Selecciona la que se ajuste a tu perfil.',
      icono: '🎯'
    },
    {
      numero: 2,
      titulo: 'Solicita tu participación',
      descripcion: 'Envía tu solicitud de participación. El equipo la revisará y te contactará con la documentación, condiciones definitivas y el proceso de formalización.',
      icono: '✍️'
    },
    {
      numero: 3,
      titulo: 'Seguimiento en tiempo real',
      descripcion: 'Una vez formalizada la participación, desde tu panel puedes consultar el estado de la operación, los movimientos de capital y los hitos completados.',
      icono: '📈'
    },
    {
      numero: 4,
      titulo: 'Liquidación y resultado',
      descripcion: 'Al cierre de la operación, se comparte el resultado, la liquidación y la documentación justificativa. El capital y el resultado se distribuyen según las condiciones acordadas.',
      icono: '📊'
    }
  ];

  return (
    <div className="detail-shell" style={{ background: 'linear-gradient(180deg, #07111f 0%, #0e1b2d 100%)', minHeight: '100vh' }}>
      {/* Header */}
      <div className="detail-card" style={{ background: 'linear-gradient(135deg, #0e1b2d 0%, #1a2538 100%)', marginBottom: '2rem', borderBottom: '2px solid #f6c453' }}>
        <div className="detail-header">
          <p className="section-label" style={{ color: '#f6c453', fontSize: '14px', fontWeight: '700', textTransform: 'uppercase' }}>Sistema de inversión</p>
          <h1 style={{ color: '#ffffff', fontSize: '48px', fontWeight: '800', margin: '0.5rem 0' }}>Cómo funciona</h1>
          <p style={{ color: '#cbd5e1', fontSize: '18px', margin: '1rem 0 0 0' }}>
            Descubre el proceso completo desde tu aportación inicial hasta la generación de beneficios
          </p>
        </div>
      </div>

      {/* Pasos */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '2rem', marginBottom: '3rem' }}>
        {pasos.map((paso) => (
          <div
            key={paso.numero}
            className="detail-card"
            style={{
              background: 'linear-gradient(135deg, rgba(14, 27, 45, 0.8), rgba(7, 17, 31, 0.8))',
              border: '2px solid rgba(246, 196, 83, 0.2)',
              borderLeft: `4px solid #f6c453`,
              position: 'relative',
              padding: '2rem',
              transition: 'all 0.3s ease'
            }}
          >
            {/* Número del paso */}
            <div
              style={{
                position: 'absolute',
                top: '-15px',
                left: '30px',
                width: '50px',
                height: '50px',
                background: 'linear-gradient(135deg, #f6c453, #dba93a)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#0f172a',
                fontSize: '24px',
                fontWeight: '800',
                boxShadow: '0 8px 20px rgba(246, 196, 83, 0.3)'
              }}
            >
              {paso.numero}
            </div>

            {/* Icono */}
            <div style={{ fontSize: '48px', marginTop: '1rem', marginBottom: '1rem' }}>
              {paso.icono}
            </div>

            {/* Título */}
            <h3 style={{
              color: '#ffffff',
              fontSize: '20px',
              fontWeight: '700',
              margin: '0 0 1rem 0'
            }}>
              {paso.titulo}
            </h3>

            {/* Descripción */}
            <p style={{
              color: '#cbd5e1',
              fontSize: '14px',
              lineHeight: '1.6',
              margin: 0
            }}>
              {paso.descripcion}
            </p>
          </div>
        ))}
      </div>

      {/* Sección de Transparencia */}
      <div
        className="detail-card"
        style={{
          background: 'linear-gradient(135deg, rgba(246, 196, 83, 0.06), rgba(219, 169, 58, 0.06))',
          border: '2px solid rgba(246, 196, 83, 0.2)',
          marginBottom: '2rem'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1.5rem' }}>
          <div style={{ fontSize: '40px' }}>🔒</div>
          <div>
            <h3 style={{ color: '#f6c453', fontSize: '20px', fontWeight: '700', margin: '0 0 0.5rem 0' }}>
              Transparencia ante todo
            </h3>
            <p style={{ color: '#cbd5e1', fontSize: '15px', lineHeight: '1.6', margin: 0 }}>
              Todas las aportaciones, movimientos y beneficios quedan registrados y pueden estar sujetos a validación antes de ser acreditados. Tienes acceso total a tu información en cualquier momento desde tu panel personal.
            </p>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="detail-cta" style={{ justifyContent: 'center', gap: '1rem' }}>
        <button
          className="primary-btn"
          onClick={() => navigate('/login')}
          style={{
            background: 'linear-gradient(135deg, #f6c453, #dba93a)',
            padding: '14px 32px',
            fontSize: '16px',
            fontWeight: '700',
            borderRadius: '8px',
            border: 'none',
            color: '#0f172a',
            cursor: 'pointer',
            boxShadow: '0 8px 20px rgba(246, 196, 83, 0.3)'
          }}
        >
          Comenzar ahora
        </button>
        <button
          className="secondary-btn"
          onClick={() => navigate('/')}
          style={{
            background: 'rgba(14, 27, 45, 0.5)',
            padding: '14px 32px',
            fontSize: '16px',
            fontWeight: '700',
            borderRadius: '8px',
            border: '1px solid rgba(148, 163, 184, 0.3)',
            color: '#cbd5e1',
            cursor: 'pointer',
            transition: 'all 0.3s ease'
          }}
        >
          Volver al inicio
        </button>
      </div>
    </div>
  );
}

export default ComoFunciona;
