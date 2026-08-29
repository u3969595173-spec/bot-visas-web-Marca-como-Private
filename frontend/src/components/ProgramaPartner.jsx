import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const NIVELES = [
    { emoji: '💠', nombre: 'Partner', min: 500, max: 999, beneficio: '25 USDT/mes', meses: 2, color: '#4ade80' },
    { emoji: '🔷', nombre: 'Premium Partner', min: 1000, max: 2499, beneficio: '50 USDT/mes', meses: 3, color: '#60a5fa' },
    { emoji: '💎', nombre: 'VIP Partner', min: 2500, max: 4999, beneficio: '100 USDT/mes', meses: 4, color: '#c084fc' },
    { emoji: '👑', nombre: 'Strategic Partner', min: 5000, max: 9999, beneficio: '150 USDT/mes', meses: 6, color: '#fb923c' },
    { emoji: '🏆', nombre: 'Founding Partner', min: 10000, max: null, beneficio: '250 USDT/mes', meses: 12, color: '#f6c453' },
];

const DETALLES_BENEFICIOS = [
    { nombre: 'Partner', min: 500, emoji: '💠', beneficios: ['Promociones.', 'Descuentos.', 'Ofertas especiales.', '25 USDT/mes durante 2 meses.'] },
    { nombre: 'Premium Partner', min: 1000, emoji: '🔷', beneficios: ['Todo lo anterior.', 'Ofertas exclusivas.', 'Acceso anticipado a determinadas campañas.', '50 USDT/mes durante 3 meses.'] },
    { nombre: 'VIP Partner', min: 2500, emoji: '💎', beneficios: ['Todo lo anterior.', 'Campañas especiales.', 'Eventos y experiencias.', '100 USDT/mes durante 4 meses.'] },
    { nombre: 'Strategic Partner', min: 5000, emoji: '👑', beneficios: ['Todo lo anterior.', 'Condiciones especiales.', 'Atención prioritaria.', '150 USDT/mes durante 6 meses.'] },
    { nombre: 'Founding Partner', min: 10000, emoji: '🏆', beneficios: ['Todo lo anterior.', 'Colaboraciones especiales.', 'Oportunidades y condiciones premium.', '250 USDT/mes durante 12 meses.'] },
];

export default function ProgramaPartner() {
    const navigate = useNavigate();
    const [tab, setTab] = useState('niveles');

    return (
        <div style={{ background: '#050d18', minHeight: '100vh', fontFamily: 'Inter, sans-serif', color: '#f1f5f9' }}>

            {/* Header */}
            <div style={{ background: 'linear-gradient(135deg, #0e1b2d, #1a2538)', borderBottom: '2px solid #f6c453', padding: '3rem 1.5rem 2rem' }}>
                <div style={{ maxWidth: 800, margin: '0 auto' }}>
                    <p style={{ color: '#f6c453', fontSize: 13, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', margin: '0 0 0.5rem' }}>Capital Iberia</p>
                    <h1 style={{ margin: '0 0 0.8rem', fontSize: 'clamp(1.8rem,4vw,2.8rem)', fontWeight: 900, color: '#fff' }}>💎 Programa Partner de Capital</h1>
                    <p style={{ margin: 0, color: '#94a3b8', fontSize: '1.05rem', maxWidth: 600 }}>
                        Un programa pensado para usuarios que prefieren crecer mediante su propia participación de capital, sin necesidad de crear una comunidad ni realizar referidos. Tu nivel depende del capital propio que mantengas dentro del programa.
                    </p>
                </div>
            </div>

            {/* Tabs */}
            <div style={{ background: '#07111f', borderBottom: '1px solid rgba(148,163,184,0.1)', padding: '0 1.5rem' }}>
                <div style={{ maxWidth: 800, margin: '0 auto', display: 'flex', gap: '0.5rem' }}>
                    {[['niveles', '🏆 Niveles'], ['beneficios', '🎁 Beneficios'], ['info', '📈 Crece a tu ritmo']].map(([id, label]) => (
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
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            {NIVELES.map((n, i) => (
                                <div key={n.nombre} style={{ background: 'rgba(15,23,42,0.8)', border: `1px solid ${n.color}33`, borderLeft: `4px solid ${n.color}`, borderRadius: 14, padding: '1.4rem 1.5rem' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem' }}>
                                        <div>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.3rem' }}>
                                                <span style={{ fontSize: 22 }}>{n.emoji}</span>
                                                <span style={{ fontSize: '1.1rem', fontWeight: 800, color: n.color }}>{n.nombre}</span>
                                            </div>
                                            <div style={{ fontSize: 13, color: '#94a3b8' }}>
                                                {n.max ? `${n.min.toLocaleString()}–${n.max.toLocaleString()} USDT` : `${n.min.toLocaleString()}+ USDT`}
                                            </div>
                                        </div>
                                        <div style={{ textAlign: 'right' }}>
                                            <div style={{ fontSize: '1rem', fontWeight: 700, color: n.color }}>{n.beneficio}</div>
                                            <div style={{ fontSize: 13, color: '#94a3b8', marginTop: 2 }}>Duración: {n.meses} meses</div>
                                        </div>
                                    </div>
                                    {i > 0 && <div style={{ fontSize: 12, color: 'rgba(148,163,184,0.5)', marginTop: '0.8rem' }}>✓ Incrementa capital para subir nivel</div>}
                                </div>
                            ))}
                        </div>

                        <div style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 10, padding: '1.5rem', marginTop: '2rem' }}>
                            <p style={{ color: '#94a3b8', fontSize: 13, margin: '0 0 0.5rem 0' }}>* Los beneficios mensuales son temporales y están sujetos a las condiciones del programa.</p>
                            <p style={{ color: '#94a3b8', fontSize: 13, margin: '0 0 0.5rem 0' }}>* Los beneficios, promociones y condiciones pueden variar según el nivel y las campañas disponibles.</p>
                            <p style={{ color: '#94a3b8', fontSize: 13, margin: '0 0 0.5rem 0' }}>* El acceso a los beneficios requiere mantener las condiciones establecidas para cada nivel.</p>
                            <p style={{ color: '#94a3b8', fontSize: 13, margin: '0' }}>* Cualquier participación económica o aportación de capital estará sujeta a las condiciones específicas del programa y a la normativa aplicable.</p>
                        </div>
                    </div>
                )}

                {/* TAB: BENEFICIOS */}
                {tab === 'beneficios' && (
                    <div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                            {DETALLES_BENEFICIOS.map((n, i) => (
                                <div key={n.nombre} style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 14, padding: '1.5rem' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                        <span style={{ fontSize: 24 }}>{n.emoji}</span>
                                        <h2 style={{ margin: 0, color: '#f6c453' }}>{n.nombre}</h2>
                                    </div>
                                    <p style={{ color: '#94a3b8', marginTop: 0, marginBottom: '1rem', fontSize: '0.95rem' }}>
                                        A partir de {n.min.toLocaleString()} USDT.
                                    </p>
                                    <div>
                                        <h4 style={{ color: '#f8fafc', marginBottom: '0.8rem', marginTop: 0 }}>Beneficios:</h4>
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                            {n.beneficios.map((b, idx) => (
                                                <div key={idx} style={{ display: 'flex', gap: '0.8rem', alignItems: 'flex-start' }}>
                                                    <span style={{ color: '#f6c453', fontWeight: 700, flexShrink: 0 }}>•</span>
                                                    <span style={{ color: '#cbd5e1', fontSize: 15 }}>{b}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* TAB: INFO (Crece a tu ritmo) */}
                {tab === 'info' && (
                    <div>
                        <div style={{ background: 'rgba(15,23,42,0.8)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 14, padding: '1.5rem', marginBottom: '1.5rem' }}>
                            <h2 style={{ margin: '0 0 1.2rem', color: '#f6c453', fontSize: '1.5rem' }}>📈 Crece a tu ritmo</h2>
                            <p style={{ color: '#cbd5e1', marginBottom: '1.5rem', fontSize: '1.05rem', lineHeight: 1.6 }}>
                                No todos los usuarios quieren desarrollar una comunidad. Por eso este programa permite avanzar únicamente mediante la participación de capital propio.
                            </p>

                            <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1.5rem', borderRadius: 10, marginBottom: '1.5rem' }}>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                                    {NIVELES.map(n => (
                                        <div key={n.nombre} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '0.8rem' }}>
                                            <span style={{ color: '#94a3b8' }}>{n.min.toLocaleString()}{n.max ? '' : '+'} USDT</span>
                                            <span style={{ color: n.color, fontWeight: 700 }}>→ {n.nombre}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <p style={{ color: '#cbd5e1', marginBottom: '2rem', fontSize: '1.05rem', lineHeight: 1.6 }}>
                                Cuanto mayor sea tu nivel, mayores serán las ventajas y el periodo durante el cual puedes disfrutar del beneficio mensual correspondiente.
                            </p>

                            <div style={{ textAlign: 'center', margin: '3rem 0 1rem' }}>
                                <h3 style={{ margin: 0, fontSize: '1.6rem', color: '#f6c453', fontStyle: 'italic', fontWeight: 900 }}>
                                    «Tu capital. Tu nivel. Tus beneficios.»
                                </h3>
                            </div>
                        </div>
                    </div>
                )}
            </div>

        </div>
    );
}
