import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const NIVELES_CAPITAL = [
    { emoji: '💠', nombre: 'Partner', min: 500, max: 999, beneficio: '25 USDT/mes', meses: 2, color: '#4ade80' },
    { emoji: '🔷', nombre: 'Premium Partner', min: 1000, max: 2499, beneficio: '50 USDT/mes', meses: 3, color: '#60a5fa' },
    { emoji: '💎', nombre: 'VIP Partner', min: 2500, max: 4999, beneficio: '100 USDT/mes', meses: 4, color: '#c084fc' },
    { emoji: '👑', nombre: 'Strategic Partner', min: 5000, max: 9999, beneficio: '150 USDT/mes', meses: 6, color: '#fb923c' },
    { emoji: '🏆', nombre: 'Founding Partner', min: 10000, max: null, beneficio: '250 USDT/mes', meses: 12, color: '#f6c453' },
];

const NIVELES_COMUNIDAD = [
    { emoji: '🌱', nombre: 'Community', min: 5, max: 24, bonus: '25 USDT/mes', duracion: '2 meses', color: '#4ade80' },
    { emoji: '⭐', nombre: 'Leader', min: 25, max: 49, bonus: '50 USDT/mes', duracion: '3 meses', color: '#60a5fa' },
    { emoji: '🔥', nombre: 'Senior Leader', min: 50, max: 99, bonus: '100 USDT/mes', duracion: '4 meses', color: '#ef4444' },
    { emoji: '💎', nombre: 'Elite Leader', min: 100, max: 199, bonus: '150 USDT/mes', duracion: '6 meses', color: '#c084fc' },
    { emoji: '👑', nombre: 'Executive Leader', min: 200, max: 499, bonus: '250 USDT/mes', duracion: '12 meses', color: '#fb923c' },
    { emoji: '🏆', nombre: 'Founding Leader', min: 500, max: null, bonus: '400 USDT/mes', duracion: '12 meses', color: '#f6c453' },
];

const BENEFICIOS_EXTRA = [
    '🎁 Promociones exclusivas.',
    '🏷️ Descuentos especiales.',
    '🔥 Ofertas especiales.',
    '🚀 Acceso anticipado a campañas.',
    '🎉 Eventos y experiencias.',
    '📢 Apoyo promocional.',
    '🤝 Colaboraciones especiales.',
    '🏆 Patrocinios para determinadas actividades.',
    '⭐ Condiciones especiales para los niveles superiores.'
];

export default function ProgramaCombinado() {
    const navigate = useNavigate();
    const [tab, setTab] = useState('resumen');

    return (
        <div style={{ background: '#050d18', minHeight: '100vh', fontFamily: 'Inter, sans-serif', color: '#f1f5f9' }}>

            {/* Header */}
            <div style={{ background: 'linear-gradient(135deg, #2a0845, #6441A5)', borderBottom: '2px solid #ef4444', padding: '3rem 1.5rem 2rem' }}>
                <div style={{ maxWidth: 900, margin: '0 auto' }}>
                    <p style={{ color: '#fca5a5', fontSize: 13, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', margin: '0 0 0.5rem' }}>Capital Trade Iberia</p>
                    <h1 style={{ margin: '0 0 0.8rem', fontSize: 'clamp(1.8rem,4vw,2.8rem)', fontWeight: 900, color: '#fff' }}>🔥 Programa Combinado</h1>
                    <h2 style={{ margin: '0 0 1rem', fontSize: '1.2rem', color: '#fca5a5', fontWeight: 600 }}>Capital + Comunidad</h2>
                    <p style={{ margin: 0, color: '#cbd5e1', fontSize: '1.05rem', maxWidth: 700, lineHeight: 1.6 }}>
                        En Soporte Capital puedes crecer de dos formas: mediante tu propia participación de capital o mediante el desarrollo de una comunidad.
                        <strong> Ambas modalidades pueden combinarse.</strong> El beneficio mensual correspondiente al capital se mantiene y, al desarrollar una comunidad, puedes desbloquear bonificaciones mensuales adicionales.
                    </p>
                </div>
            </div>

            {/* Tabs */}
            <div style={{ background: '#07111f', borderBottom: '1px solid rgba(148,163,184,0.1)', padding: '0 1.5rem', overflowX: 'auto' }}>
                <div style={{ maxWidth: 900, margin: '0 auto', display: 'flex', gap: '0.5rem' }}>
                    {[['resumen', '🔥 Resumen'], ['capital', '💎 Programa de Capital'], ['comunidad', '👥 Bonus Comunidad'], ['info', '❓ Cómo Funciona']].map(([id, label]) => (
                        <button key={id} onClick={() => setTab(id)} style={{ padding: '1rem 1.2rem', background: 'transparent', border: 'none', borderBottom: tab === id ? '2px solid #ef4444' : '2px solid transparent', color: tab === id ? '#ef4444' : '#94a3b8', fontWeight: 600, fontSize: 14, cursor: 'pointer', transition: 'color 0.2s', whiteSpace: 'nowrap' }}>
                            {label}
                        </button>
                    ))}
                </div>
            </div>

            <div style={{ maxWidth: 900, margin: '0 auto', padding: '2rem 1.5rem' }}>

                {/* TAB: RESUMEN */}
                {tab === 'resumen' && (
                    <div style={{ display: 'grid', gap: '2rem' }}>
                        <div style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 14, padding: '2rem' }}>
                            <h2 style={{ margin: '0 0 1.5rem', color: '#fff', fontSize: '1.5rem' }}>🚀 Dos formas de crecer</h2>

                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
                                <div style={{ background: 'rgba(56, 189, 248, 0.05)', border: '1px solid rgba(56, 189, 248, 0.2)', padding: '1.5rem', borderRadius: 12 }}>
                                    <h3 style={{ margin: '0 0 0.8rem', color: '#38bdf8', fontSize: '1.2rem' }}>💎 Crece con tu Capital</h3>
                                    <p style={{ margin: 0, color: '#94a3b8', fontSize: '0.95rem', lineHeight: 1.6 }}>Aumenta tu nivel mediante tu propia participación de capital. Recibirás un beneficio mensual directo a tu billetera durante un tiempo limitado.</p>
                                </div>
                                <div style={{ background: 'rgba(167, 139, 250, 0.05)', border: '1px solid rgba(167, 139, 250, 0.2)', padding: '1.5rem', borderRadius: 12 }}>
                                    <h3 style={{ margin: '0 0 0.8rem', color: '#a78bfa', fontSize: '1.2rem' }}>👥 Crece con tu Comunidad</h3>
                                    <p style={{ margin: 0, color: '#94a3b8', fontSize: '0.95rem', lineHeight: 1.6 }}>Construye una red de inversores y recibe un Bonus mensual durante un tiempo preestablecido cada vez que desbloquees un nuevo hito de miembros activos.</p>
                                </div>
                            </div>

                            <div style={{ marginTop: '1.5rem', background: 'rgba(239, 68, 68, 0.05)', border: '1px solid rgba(239, 68, 68, 0.3)', padding: '1.5rem', borderRadius: 12 }}>
                                <h3 style={{ margin: '0 0 0.5rem', color: '#ef4444', fontSize: '1.2rem', textAlign: 'center' }}>🔥 HAZ AMBAS COSAS</h3>
                                <p style={{ margin: 0, color: '#e2e8f0', textAlign: 'center', lineHeight: 1.6 }}>
                                    Puedes mantener tu nivel de capital y, al mismo tiempo, desarrollar una comunidad. El beneficio mensual del capital se mantiene y los bonus de comunidad se reciben como recompensas temporales por cada nivel alcanzado.
                                </p>
                            </div>
                        </div>

                        <div style={{ textAlign: 'center', margin: '1rem 0' }}>
                            <h3 style={{ margin: 0, fontSize: '1.4rem', color: '#f8fafc', fontStyle: 'italic', fontWeight: 600 }}>
                                «Tu capital te permite avanzar. Tu comunidad te permite desbloquear nuevas recompensas. <span style={{ color: '#ef4444' }}>Tú decides hasta dónde quieres llegar.</span>»
                            </h3>
                        </div>
                    </div>
                )}

                {/* TAB: CAPITAL */}
                {tab === 'capital' && (
                    <div>
                        <h2 style={{ color: '#fff', marginBottom: '1.5rem', fontSize: '1.4rem' }}>💎 NIVELES DE CAPITAL</h2>
                        <p style={{ color: '#94a3b8', marginBottom: '2rem' }}>Tu nivel de capital genera retornos mensuales recurrentes durante la duración de tu programa. No necesitas referidos.</p>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            {NIVELES_CAPITAL.map((n, i) => (
                                <div key={n.nombre} style={{ background: 'rgba(15,23,42,0.8)', border: `1px solid ${n.color}33`, borderLeft: `6px solid ${n.color}`, borderRadius: 10, padding: '1.2rem 1.5rem' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.8rem' }}>
                                        <div>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.3rem' }}>
                                                <span style={{ fontSize: 24 }}>{n.emoji}</span>
                                                <span style={{ fontSize: '1.2rem', fontWeight: 800, color: n.color }}>{n.nombre}</span>
                                            </div>
                                            <div style={{ fontSize: 13, color: '#94a3b8', fontWeight: 600 }}>
                                                {n.max ? `${n.min.toLocaleString()}–${n.max.toLocaleString()} USDT` : `${n.min.toLocaleString()}+ USDT`}
                                            </div>
                                        </div>
                                        <div style={{ textAlign: 'right' }}>
                                            <div style={{ fontSize: '1.2rem', fontWeight: 800, color: n.color }}>{n.beneficio}</div>
                                            <div style={{ fontSize: 13, color: '#94a3b8', marginTop: 4 }}>Duración: {n.meses} meses</div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* TAB: COMUNIDAD */}
                {tab === 'comunidad' && (
                    <div>
                        <h2 style={{ color: '#fff', marginBottom: '1.5rem', fontSize: '1.4rem' }}>👥 BONUS DE COMUNIDAD</h2>
                        <p style={{ color: '#94a3b8', marginBottom: '2rem' }}>Si además decides crear una comunidad, puedes desbloquear bonificaciones mensuales al alcanzar cada nuevo nivel de red activa.</p>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            {NIVELES_COMUNIDAD.map((n, i) => (
                                <div key={n.nombre} style={{ background: 'rgba(15,23,42,0.8)', border: `1px solid ${n.color}33`, borderLeft: `6px solid ${n.color}`, borderRadius: 10, padding: '1.2rem 1.5rem' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.8rem' }}>
                                        <div>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.3rem' }}>
                                                <span style={{ fontSize: 24 }}>{n.emoji}</span>
                                                <span style={{ fontSize: '1.1rem', fontWeight: 700, color: n.color }}>{n.nombre}</span>
                                            </div>
                                            <div style={{ fontSize: 13, color: '#94a3b8' }}>
                                                {n.max ? `${n.min} a ${n.max} Miembros Activos` : `${n.min}+ Miembros Activos`}
                                            </div>
                                        </div>
                                        <div style={{ textAlign: 'right', display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '4px' }}>
                                            <span style={{ fontSize: 10, color: '#f8fafc', background: 'rgba(255,255,255,0.1)', padding: '2px 6px', borderRadius: 4, letterSpacing: '0.05em' }}>BONUS RECURRENTE</span>
                                            <div style={{ fontSize: '1.3rem', fontWeight: 900, color: n.color }}>{n.bonus}</div>
                                            <div style={{ fontSize: 13, color: '#94a3b8', marginTop: 0 }}>Duración: {n.duracion}</div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* TAB: CÓMO FUNCIONA */}
                {tab === 'info' && (
                    <div>
                        <div style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 14, padding: '2rem', marginBottom: '2rem' }}>
                            <h2 style={{ margin: '0 0 1.2rem', color: '#fff', fontSize: '1.4rem' }}>🔥 ¿Cómo funciona la combinación?</h2>
                            <p style={{ color: '#cbd5e1', marginBottom: '1.5rem', fontSize: '0.95rem', lineHeight: 1.6 }}>
                                Los beneficios de ambos programas (Capital y Comunidad) <strong>funcionan de forma independiente</strong>. Los bonus de comunidad NO sustituyen ni duplican el beneficio mensual del programa de capital.
                            </p>

                            <div style={{ background: 'rgba(0,0,0,0.4)', padding: '1.5rem', borderRadius: 8, borderLeft: '4px solid #ef4444' }}>
                                <h4 style={{ margin: '0 0 1rem', color: '#fca5a5' }}>Ejemplo Práctico:</h4>
                                <ul style={{ margin: 0, padding: '0 0 0 1.2rem', color: '#94a3b8', display: 'flex', flexDirection: 'column', gap: '0.8rem', fontSize: '0.95rem' }}>
                                    <li>Un usuario mantiene <strong>10.000 USDT</strong> de capital propio y alcanza el nivel <strong style={{ color: '#f6c453' }}>Founding Partner</strong>.</li>
                                    <li style={{ listStyle: 'none', color: '#f8fafc', paddingLeft: '1rem', borderLeft: '2px solid #334155' }}>
                                        → Recibe el beneficio mensual correspondiente a su nivel de capital (250 USDT/mes).
                                    </li>
                                    <li>Posteriormente desarrolla una comunidad y alcanza <strong>5 miembros activos</strong> (Nivel <strong style={{ color: '#4ade80' }}>Community</strong>).</li>
                                    <li style={{ listStyle: 'none', color: '#f8fafc', paddingLeft: '1rem', borderLeft: '2px solid #334155' }}>
                                        → Recibe 25 USDT/mes adicionales durante 2 meses.
                                    </li>
                                    <li>Si posteriormente alcanza <strong>25 miembros activos</strong> (Nivel <strong style={{ color: '#60a5fa' }}>Leader</strong>).</li>
                                    <li style={{ listStyle: 'none', color: '#f8fafc', paddingLeft: '1rem', borderLeft: '2px solid #334155' }}>
                                        → Recibe 50 USDT/mes adicionales durante 3 meses, y así sucesivamente...
                                    </li>
                                </ul>
                            </div>
                        </div>

                        <div style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 14, padding: '2rem' }}>
                            <h2 style={{ margin: '0 0 1.2rem', color: '#fff', fontSize: '1.4rem' }}>🎁 Beneficios adicionales</h2>
                            <p style={{ color: '#cbd5e1', marginBottom: '1.5rem', fontSize: '0.95rem', lineHeight: 1.6 }}>
                                Además de los beneficios económicos, el crecimiento dentro de cualquiera de los programas puede desbloquear ventajas exclusivas:
                            </p>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                                {BENEFICIOS_EXTRA.map((b, idx) => (
                                    <div key={idx} style={{ background: 'rgba(255,255,255,0.03)', padding: '0.8rem', borderRadius: 8, fontSize: '0.9rem', color: '#e2e8f0', display: 'flex', alignItems: 'center' }}>
                                        {b}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {/* Footer notes */}
                <div style={{ background: 'transparent', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '1.5rem', marginTop: '2rem' }}>
                    <ul style={{ margin: 0, padding: 0, color: '#64748b', fontSize: '0.8rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', listStyle: 'none' }}>
                        <li>* Los beneficios mensuales son temporales y están sujetos a las condiciones del programa.</li>
                        <li>* Los bonus de comunidad se emiten mensualmente según la duración de cada nivel.</li>
                        <li>* Los beneficios y promociones pueden variar según el nivel y las condiciones de cada campaña.</li>
                        <li>* Cualquier participación económica o recompensa vinculada estará sujeta a las condiciones específicas del programa y a la normativa aplicable.</li>
                    </ul>
                </div>

            </div>
        </div>
    );
}
