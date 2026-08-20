import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const NIVELES = [
  { emoji: '🌱', nombre: 'Community', min: 5, max: 24, cupo: '2%', beneficio: '25 USDT/mes', duracion: '2 meses', color: '#4ade80', ejemplo: { usdt: 200, benef: 60 } },
  { emoji: '⭐', nombre: 'Leader', min: 25, max: 49, cupo: '5%', beneficio: '50 USDT/mes', duracion: '3 meses', color: '#facc15', ejemplo: { usdt: 500, benef: 150 } },
  { emoji: '🔥', nombre: 'Senior Leader', min: 50, max: 99, cupo: '10%', beneficio: '100 USDT/mes', duracion: '4 meses', color: '#fb923c', ejemplo: { usdt: 1000, benef: 300 } },
  { emoji: '💎', nombre: 'Elite Leader', min: 100, max: 199, cupo: '15%', beneficio: '150 USDT/mes', duracion: '6 meses', color: '#60a5fa', ejemplo: { usdt: 1500, benef: 450 } },
  { emoji: '👑', nombre: 'Executive Leader', min: 200, max: 499, cupo: '25%', beneficio: '250 USDT/mes', duracion: '12 meses', color: '#c084fc', ejemplo: { usdt: 2500, benef: 750 } },
  { emoji: '🏆', nombre: 'Founding Leader', min: 500, max: null, cupo: '43%', beneficio: '400 USDT/mes', duracion: '12 meses', color: '#f6c453', ejemplo: { usdt: 4300, benef: 1290 } },
];

const BENEFICIOS = [
  'Comunidad propia dentro de la plataforma',
  'Promociones exclusivas',
  'Descuentos especiales',
  'Ofertas especiales para tu comunidad',
  'Acceso anticipado a determinadas campañas',
  'Campañas exclusivas',
  'Eventos y experiencias',
  'Apoyo promocional',
  'Patrocinios',
  'Colaboraciones con Soporte Capital',
  'Condiciones especiales para niveles superiores',
];

export default function Programa() {
  const navigate = useNavigate();
  const [tab, setTab] = useState('niveles');

  return (
    <div style={{ background: '#050d18', minHeight: '100vh', fontFamily: 'Inter, sans-serif', color: '#f1f5f9' }}>

      {/* Header */}
      <div style={{ background: 'linear-gradient(135deg, #0e1b2d, #1a2538)', borderBottom: '2px solid #f6c453', padding: '3rem 1.5rem 2rem' }}>
        <div style={{ maxWidth: 800, margin: '0 auto' }}>
          <p style={{ color: '#f6c453', fontSize: 13, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', margin: '0 0 0.5rem' }}>Soporte Capital</p>
          <h1 style={{ margin: '0 0 0.8rem', fontSize: 'clamp(1.8rem,4vw,2.8rem)', fontWeight: 900, color: '#fff' }}>👑 Programa de Comunidad y Líderes</h1>
          <p style={{ margin: 0, color: '#94a3b8', fontSize: '1.05rem', maxWidth: 600 }}>
            Construye tu comunidad, hazla crecer y desbloquea nuevas oportunidades de participación.
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ background: '#07111f', borderBottom: '1px solid rgba(148,163,184,0.1)', padding: '0 1.5rem' }}>
        <div style={{ maxWidth: 800, margin: '0 auto', display: 'flex', gap: '0.5rem' }}>
          {[['niveles', '🏆 Niveles'], ['ejemplo', '🧱 Ejemplo'], ['calculo', '📊 Cálculo'], ['beneficios', '🎁 Beneficios']].map(([id, label]) => (
            <button key={id} onClick={() => setTab(id)} style={{ padding: '1rem 1.2rem', background: 'transparent', border: 'none', borderBottom: tab === id ? '2px solid #f6c453' : '2px solid transparent', color: tab === id ? '#f6c453' : '#94a3b8', fontWeight: 600, fontSize: 14, cursor: 'pointer', transition: 'color 0.2s' }}>
              {label}
            </button>
          ))}
        </div>
      </div>

      <div style={{ maxWidth: 800, margin: '0 auto', padding: '2rem 1.5rem' }}>

        {/* TAB: NIVELES */}
        {tab === 'niveles' && (
          <div>
            <p style={{ color: '#94a3b8', marginBottom: '1.5rem' }}>En Soporte Capital creemos que una comunidad fuerte genera más oportunidades. Cada líder puede construir su propia comunidad y desbloquear progresivamente beneficios, promociones y mayor capacidad de participación.</p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {NIVELES.map((n, i) => (
                <div key={n.nombre} style={{ background: 'rgba(15,23,42,0.8)', border: `1px solid ${n.color}33`, borderLeft: `4px solid ${n.color}`, borderRadius: 14, padding: '1.4rem 1.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem' }}>
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.3rem' }}>
                        <span style={{ fontSize: 22 }}>{n.emoji}</span>
                        <span style={{ fontSize: '1.1rem', fontWeight: 800, color: n.color }}>{n.nombre}</span>
                      </div>
                      <div style={{ fontSize: 13, color: '#94a3b8' }}>{n.min}{n.max ? `–${n.max}` : '+'} miembros activos</div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '1rem', fontWeight: 700, color: n.color }}>Cupo máximo: {n.cupo}</div>
                      <div style={{ fontSize: 13, color: '#94a3b8', marginTop: 2 }}>{n.beneficio} (x {n.duracion})</div>
                    </div>
                  </div>
                  {i > 0 && <div style={{ fontSize: 12, color: 'rgba(148,163,184,0.5)', marginTop: '0.8rem' }}>✓ Incluye todo lo del nivel anterior</div>}
                </div>
              ))}
            </div>
            <p style={{ fontSize: 12, color: 'rgba(148,163,184,0.4)', marginTop: '1.5rem' }}>* Los cupos son máximos y están sujetos a las condiciones y disponibilidad de cada operación. Los beneficios mensuales de comunidad están sujetos a las condiciones del programa.</p>
          </div>
        )}

        {/* TAB: EJEMPLO */}
        {tab === 'ejemplo' && (
          <div>
            <div style={{ background: 'rgba(246,196,83,0.06)', border: '1px solid rgba(246,196,83,0.2)', borderRadius: 14, padding: '1.5rem', marginBottom: '1.5rem' }}>
              <h2 style={{ margin: '0 0 1rem', color: '#f6c453' }}>🧱 Operación de ejemplo: Contenedor de cemento</h2>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '1rem', textAlign: 'center' }}>
                {[['Capital necesario', '10.000 USDT'], ['Venta mercancía', '13.000 USDT'], ['Beneficio neto', '3.000 USDT']].map(([l, v]) => (
                  <div key={l} style={{ background: 'rgba(0,0,0,0.2)', borderRadius: 10, padding: '1rem' }}>
                    <div style={{ fontSize: 11, color: '#94a3b8', textTransform: 'uppercase', marginBottom: 4 }}>{l}</div>
                    <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#f6c453' }}>{v}</div>
                  </div>
                ))}
              </div>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
              {NIVELES.map(n => (
                <div key={n.nombre} style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '1rem 1.2rem', background: 'rgba(15,23,42,0.7)', border: `1px solid rgba(148,163,184,0.08)`, borderRadius: 10 }}>
                  <span style={{ fontSize: 20, width: 30 }}>{n.emoji}</span>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 700, color: n.color }}>{n.nombre}</div>
                    <div style={{ fontSize: 13, color: '#94a3b8' }}>Cupo {n.cupo} × 10.000 USDT = <strong style={{ color: '#f1f5f9' }}>{n.ejemplo.usdt.toLocaleString()} USDT</strong></div>
                  </div>
                  <div style={{ textAlign: 'right', fontWeight: 700, color: '#4ade80', fontSize: '1rem' }}>+{n.ejemplo.benef.toLocaleString()} USDT</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB: CÁLCULO */}
        {tab === 'calculo' && (
          <div>
            <div style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 14, padding: '1.5rem', marginBottom: '1.5rem' }}>
              <h2 style={{ margin: '0 0 1rem', color: '#f6c453' }}>📊 ¿Cómo se calcula?</h2>
              <p style={{ color: '#94a3b8' }}>En este ejemplo la operación genera un <strong style={{ color: '#f1f5f9' }}>30% de beneficio</strong> sobre el capital utilizado (3.000 / 10.000).</p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1.5rem' }}>
                {[
                  { titulo: 'Executive Leader (25%) — usando todo el cupo', lineas: ['10.000 × 25% = 2.500 USDT participados', '2.500 × 30% = 750 USDT de beneficio'] },
                  { titulo: 'Executive Leader (25%) — usando solo 1.000 USDT', lineas: ['1.000 USDT participados', '1.000 × 30% = 300 USDT de beneficio'] },
                ].map(item => (
                  <div key={item.titulo} style={{ background: 'rgba(246,196,83,0.04)', border: '1px solid rgba(246,196,83,0.15)', borderRadius: 10, padding: '1.2rem' }}>
                    <div style={{ fontWeight: 700, color: '#f6c453', marginBottom: '0.6rem' }}>{item.titulo}</div>
                    {item.lineas.map(l => <div key={l} style={{ color: '#cbd5e1', fontSize: 14, marginBottom: 4 }}>→ {l}</div>)}
                  </div>
                ))}
              </div>
              <p style={{ color: '#94a3b8', fontSize: 14, marginTop: '1.2rem' }}>El beneficio depende de la cantidad que realmente participe la comunidad y del resultado de la operación.</p>
            </div>
            <div style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 14, padding: '1.5rem' }}>
              <h3 style={{ color: '#f6c453', margin: '0 0 1rem' }}>📈 Hoja de ruta</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {NIVELES.map(n => (
                  <div key={n.nombre} style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', fontSize: 14 }}>
                    <span>{n.emoji}</span>
                    <span style={{ color: '#94a3b8' }}>{n.min} miembros →</span>
                    <span style={{ fontWeight: 700, color: n.color }}>{n.nombre}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TAB: BENEFICIOS */}
        {tab === 'beneficios' && (
          <div>
            <div style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 14, padding: '1.5rem', marginBottom: '1.5rem' }}>
              <h2 style={{ margin: '0 0 1.2rem', color: '#f6c453' }}>🎁 Beneficios del programa</h2>
              <p style={{ color: '#94a3b8', marginBottom: '1.2rem' }}>A medida que la comunidad crece, el líder puede desbloquear:</p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                {BENEFICIOS.map((b, i) => (
                  <div key={i} style={{ display: 'flex', gap: '0.8rem', alignItems: 'flex-start' }}>
                    <span style={{ color: '#f6c453', fontWeight: 700, flexShrink: 0 }}>•</span>
                    <span style={{ color: '#cbd5e1', fontSize: 15 }}>{b}</span>
                  </div>
                ))}
              </div>
            </div>
            <div style={{ background: 'linear-gradient(135deg, rgba(246,196,83,0.08), rgba(246,196,83,0.03))', border: '1px solid rgba(246,196,83,0.2)', borderRadius: 14, padding: '2rem', textAlign: 'center' }}>
              <div style={{ fontSize: '1.5rem', fontWeight: 900, color: '#f8fafc', marginBottom: '0.5rem' }}>CONSTRUYE TU COMUNIDAD.</div>
              <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f6c453', marginBottom: '0.5rem' }}>HAZLA CRECER.</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#94a3b8', marginBottom: '1.5rem' }}>DESBLOQUEA NUEVAS OPORTUNIDADES.</div>
              <button onClick={() => navigate('/registro')} style={{ background: 'linear-gradient(135deg, #f6c453, #dba93a)', color: '#0a0f1a', border: 'none', padding: '0.9rem 2.5rem', borderRadius: 12, fontWeight: 800, fontSize: '1rem', cursor: 'pointer' }}>
                Empezar ahora
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Sección contacto — siempre visible */}
      <div style={{ maxWidth: 800, margin: '0 auto', padding: '0 1.5rem 3rem' }}>
        <div style={{ background: 'rgba(15,23,42,0.9)', border: '2px solid rgba(246,196,83,0.3)', borderRadius: 16, padding: '2rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1.5rem' }}>
          <div>
            <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#f8fafc', marginBottom: '0.4rem' }}>¿Quieres crear tu comunidad?</div>
            <p style={{ margin: 0, color: '#94a3b8', fontSize: 14, maxWidth: 440 }}>
              Contacta con Soporte Capital y te habilitamos tu propio panel de control de comunidad con acceso a todas las herramientas de gestión.
            </p>
          </div>
          <a href="mailto:contacto@capitaltradeiberia.com" style={{ background: 'linear-gradient(135deg, #f6c453, #dba93a)', color: '#0a0f1a', textDecoration: 'none', padding: '0.9rem 2rem', borderRadius: 12, fontWeight: 800, fontSize: 15, whiteSpace: 'nowrap', display: 'inline-block' }}>
            ✉️ Contactar con Soporte
          </a>
        </div>
      </div>
    </div>
  );
}
