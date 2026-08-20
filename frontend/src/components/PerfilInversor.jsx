import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const RANGOS = [
  { nivel: 1, nombre: 'Bronce', color: '#cd7f32', min: 0 },
  { nivel: 2, nombre: 'Plata', color: '#a8a9ad', min: 1000 },
  { nivel: 3, nombre: 'Oro', color: '#f6c453', min: 5000 },
  { nivel: 4, nombre: 'Platino', color: '#00d4ff', min: 15000 },
];

function getRango(aportacion = 0) {
  return [...RANGOS].reverse().find(r => aportacion >= r.min) || RANGOS[0];
}

const getApiUrl = () => {
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  return window.location.hostname === 'localhost' ? 'http://localhost:8000' : `http://${window.location.hostname}:8000`;
};

function PerfilInversor() {
  const userSession = React.useMemo(() => {
    try { return JSON.parse(localStorage.getItem('capital_trade_user') || 'null'); } catch { return null; }
  }, []);

  const [perfil, setPerfil] = useState(null);
  const [fotoPerfil, setFotoPerfil] = useState(null);
  const [fotoPortada, setFotoPortada] = useState(null);
  const [guardando, setGuardando] = useState('');
  const fotoRef = useRef();
  const portadaRef = useRef();
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) return;
    axios.get(`${getApiUrl()}/api/inversores/perfil`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => {
        setPerfil(r.data);
        if (r.data.foto_perfil) setFotoPerfil(r.data.foto_perfil);
        if (r.data.foto_portada) setFotoPortada(r.data.foto_portada);
      })
      .catch(() => {});
  }, [token]);

  const nombre = perfil?.nombre || userSession?.name || userSession?.nombre || 'Inversor';
  const email = perfil?.email || userSession?.email || '—';
  const telefono = perfil?.telefono || userSession?.telefono || '—';
  const pais = perfil?.pais || userSession?.pais || 'España';
  const rango = getRango(0);

  const handleFoto = (e, tipo) => {
    const file = e.target.files[0];
    if (!file) return;
    // Comprimir a max 800px antes de guardar
    const img = new Image();
    const url = URL.createObjectURL(file);
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const max = 800;
      const ratio = Math.min(max / img.width, max / img.height, 1);
      canvas.width = img.width * ratio;
      canvas.height = img.height * ratio;
      canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
      const data = canvas.toDataURL('image/jpeg', 0.8);
      URL.revokeObjectURL(url);

      if (tipo === 'perfil') setFotoPerfil(data);
      else setFotoPortada(data);

      setGuardando(tipo);
      const endpoint = tipo === 'perfil' ? '/api/inversores/perfil/foto' : '/api/inversores/perfil/portada';
      axios.put(`${getApiUrl()}${endpoint}`, { foto: data }, { headers: { Authorization: `Bearer ${token}` } })
        .finally(() => setGuardando(''));
    };
    img.src = url;
  };

  return (
    <div style={{ background: '#050d18', minHeight: '100vh', fontFamily: 'Inter, sans-serif', color: '#f1f5f9' }}>

      {/* Portada */}
      <div style={{ position: 'relative', height: '220px', background: fotoPortada ? `url(${fotoPortada}) center/cover` : 'linear-gradient(135deg, #0e1b2d, #1a2538)', cursor: 'pointer' }}
        onClick={() => portadaRef.current.click()}>
        <div style={{ position: 'absolute', bottom: 12, right: 16, background: 'rgba(0,0,0,0.5)', borderRadius: 8, padding: '6px 14px', fontSize: 13, color: '#cbd5e1' }}>
          {guardando === 'portada' ? 'Guardando...' : '📷 Cambiar portada'}
        </div>
        <input ref={portadaRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={e => handleFoto(e, 'portada')} />
      </div>

      {/* Zona foto + nombre */}
      <div style={{ maxWidth: 700, margin: '0 auto', padding: '0 1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: '1.5rem', marginTop: '-60px', marginBottom: '1rem' }}>
          <div style={{ position: 'relative', flexShrink: 0 }}>
            <div onClick={() => fotoRef.current.click()} style={{ width: 120, height: 120, borderRadius: '50%', border: '4px solid #050d18', background: fotoPerfil ? `url(${fotoPerfil}) center/cover` : 'linear-gradient(135deg, #f6c453, #dba93a)', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', fontSize: 40, fontWeight: 900, color: '#0a0f1a', overflow: 'hidden', backgroundSize: 'cover' }}>
              {!fotoPerfil && nombre.charAt(0).toUpperCase()}
            </div>
            <div onClick={() => fotoRef.current.click()} style={{ position: 'absolute', bottom: 4, right: 4, background: '#1e293b', border: '2px solid #050d18', borderRadius: '50%', width: 30, height: 30, display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', fontSize: 14 }}>
              {guardando === 'perfil' ? '⏳' : '📷'}
            </div>
            <input ref={fotoRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={e => handleFoto(e, 'perfil')} />
          </div>

          <div style={{ paddingBottom: '0.5rem' }}>
            <h1 style={{ margin: 0, fontSize: '1.6rem', fontWeight: 800, color: '#f8fafc' }}>{nombre}</h1>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, marginTop: 6, background: 'rgba(255,255,255,0.05)', border: `1px solid ${rango.color}`, borderRadius: 999, padding: '4px 14px' }}>
              <span style={{ width: 10, height: 10, borderRadius: '50%', background: rango.color, display: 'inline-block' }}></span>
              <span style={{ fontSize: 13, fontWeight: 700, color: rango.color }}>Rango {rango.nombre}</span>
            </div>
          </div>
        </div>

        <hr style={{ border: 'none', borderTop: '1px solid rgba(148,163,184,0.1)', margin: '0 0 1.5rem' }} />

        {/* Info */}
        <div style={{ background: 'rgba(15,23,42,0.7)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 16, padding: '1.5rem', marginBottom: '1.5rem' }}>
          <h3 style={{ margin: '0 0 1.2rem', fontSize: '1rem', fontWeight: 700, color: '#f6c453' }}>Información</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {[
              { icon: '✉️', label: 'Email', value: email },
              { icon: '📞', label: 'Teléfono', value: telefono },
              { icon: '🌍', label: 'País', value: pais },
              { icon: '🏅', label: 'Rango actual', value: rango.nombre },
            ].map(item => (
              <div key={item.label} style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
                <span style={{ fontSize: 18, width: 28, textAlign: 'center' }}>{item.icon}</span>
                <div>
                  <div style={{ fontSize: 11, color: 'rgba(148,163,184,0.6)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{item.label}</div>
                  <div style={{ fontSize: 15, fontWeight: 600, color: '#f1f5f9' }}>{item.value}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Rangos */}
        <div style={{ background: 'rgba(15,23,42,0.7)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 16, padding: '1.5rem', marginBottom: '2rem' }}>
          <h3 style={{ margin: '0 0 1.2rem', fontSize: '1rem', fontWeight: 700, color: '#f6c453' }}>Sistema de rangos</h3>
          <div style={{ display: 'flex', gap: '0.8rem', flexWrap: 'wrap' }}>
            {RANGOS.map(r => (
              <div key={r.nivel} style={{ flex: 1, minWidth: 100, background: rango.nivel === r.nivel ? 'rgba(246,196,83,0.08)' : 'rgba(255,255,255,0.03)', border: `1px solid ${rango.nivel === r.nivel ? r.color : 'rgba(148,163,184,0.1)'}`, borderRadius: 12, padding: '0.8rem', textAlign: 'center' }}>
                <div style={{ width: 14, height: 14, borderRadius: '50%', background: r.color, margin: '0 auto 6px' }}></div>
                <div style={{ fontSize: 13, fontWeight: 700, color: rango.nivel === r.nivel ? r.color : '#94a3b8' }}>{r.nombre}</div>
                <div style={{ fontSize: 11, color: 'rgba(148,163,184,0.5)', marginTop: 2 }}>+€{r.min.toLocaleString()}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PerfilInversor;

const RANGOS = [
  { nivel: 1, nombre: 'Bronce', color: '#cd7f32', min: 0 },
  { nivel: 2, nombre: 'Plata', color: '#a8a9ad', min: 1000 },
  { nivel: 3, nombre: 'Oro', color: '#f6c453', min: 5000 },
  { nivel: 4, nombre: 'Platino', color: '#00d4ff', min: 15000 },
];

function getRango(aportacion = 0) {
  return [...RANGOS].reverse().find(r => aportacion >= r.min) || RANGOS[0];
}

function PerfilInversor() {
  const userSession = React.useMemo(() => {
    try { return JSON.parse(localStorage.getItem('capital_trade_user') || 'null'); } catch { return null; }
  }, []);

  const nombre = userSession?.name || userSession?.nombre || localStorage.getItem('usuario') || 'Inversor';
  const email = userSession?.email || '—';
  const telefono = userSession?.telefono || '—';
  const pais = userSession?.pais || 'España';

  const [fotoPerfil, setFotoPerfil] = useState(() => localStorage.getItem('perfil_foto') || null);
  const [fotoPortada, setFotoPortada] = useState(() => localStorage.getItem('portada_foto') || null);
  const fotoRef = useRef();
  const portadaRef = useRef();

  const rango = getRango(0);

  const handleFoto = (e, tipo) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      const data = ev.target.result;
      if (tipo === 'perfil') { setFotoPerfil(data); localStorage.setItem('perfil_foto', data); }
      else { setFotoPortada(data); localStorage.setItem('portada_foto', data); }
    };
    reader.readAsDataURL(file);
  };

  return (
    <div style={{ background: '#050d18', minHeight: '100vh', fontFamily: 'Inter, sans-serif', color: '#f1f5f9' }}>

      {/* Portada */}
      <div style={{ position: 'relative', height: '220px', background: fotoPortada ? `url(${fotoPortada}) center/cover` : 'linear-gradient(135deg, #0e1b2d, #1a2538)', cursor: 'pointer' }}
        onClick={() => portadaRef.current.click()}>
        <div style={{ position: 'absolute', bottom: 12, right: 16, background: 'rgba(0,0,0,0.5)', borderRadius: 8, padding: '6px 14px', fontSize: 13, color: '#cbd5e1' }}>
          📷 Cambiar portada
        </div>
        <input ref={portadaRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={e => handleFoto(e, 'portada')} />
      </div>

      {/* Zona foto + nombre */}
      <div style={{ maxWidth: 700, margin: '0 auto', padding: '0 1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: '1.5rem', marginTop: '-60px', marginBottom: '1rem' }}>

          {/* Foto perfil */}
          <div style={{ position: 'relative', flexShrink: 0 }}>
            <div onClick={() => fotoRef.current.click()} style={{ width: 120, height: 120, borderRadius: '50%', border: '4px solid #050d18', background: fotoPerfil ? `url(${fotoPerfil}) center/cover` : 'linear-gradient(135deg, #f6c453, #dba93a)', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', fontSize: 40, fontWeight: 900, color: '#0a0f1a', overflow: 'hidden' }}>
              {!fotoPerfil && nombre.charAt(0).toUpperCase()}
            </div>
            <div onClick={() => fotoRef.current.click()} style={{ position: 'absolute', bottom: 4, right: 4, background: '#1e293b', border: '2px solid #050d18', borderRadius: '50%', width: 30, height: 30, display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', fontSize: 14 }}>📷</div>
            <input ref={fotoRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={e => handleFoto(e, 'perfil')} />
          </div>

          {/* Nombre y rango */}
          <div style={{ paddingBottom: '0.5rem' }}>
            <h1 style={{ margin: 0, fontSize: '1.6rem', fontWeight: 800, color: '#f8fafc' }}>{nombre}</h1>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, marginTop: 6, background: 'rgba(255,255,255,0.05)', border: `1px solid ${rango.color}`, borderRadius: 999, padding: '4px 14px' }}>
              <span style={{ width: 10, height: 10, borderRadius: '50%', background: rango.color, display: 'inline-block' }}></span>
              <span style={{ fontSize: 13, fontWeight: 700, color: rango.color }}>Rango {rango.nombre}</span>
            </div>
          </div>
        </div>

        <hr style={{ border: 'none', borderTop: '1px solid rgba(148,163,184,0.1)', margin: '0 0 1.5rem' }} />

        {/* Info */}
        <div style={{ background: 'rgba(15,23,42,0.7)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 16, padding: '1.5rem', marginBottom: '1.5rem' }}>
          <h3 style={{ margin: '0 0 1.2rem', fontSize: '1rem', fontWeight: 700, color: '#f6c453' }}>Información</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {[
              { icon: '✉️', label: 'Email', value: email },
              { icon: '📞', label: 'Teléfono', value: telefono },
              { icon: '🌍', label: 'País', value: pais },
              { icon: '🏅', label: 'Rango actual', value: rango.nombre },
            ].map(item => (
              <div key={item.label} style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
                <span style={{ fontSize: 18, width: 28, textAlign: 'center' }}>{item.icon}</span>
                <div>
                  <div style={{ fontSize: 11, color: 'rgba(148,163,184,0.6)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{item.label}</div>
                  <div style={{ fontSize: 15, fontWeight: 600, color: '#f1f5f9' }}>{item.value}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Rangos */}
        <div style={{ background: 'rgba(15,23,42,0.7)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 16, padding: '1.5rem', marginBottom: '2rem' }}>
          <h3 style={{ margin: '0 0 1.2rem', fontSize: '1rem', fontWeight: 700, color: '#f6c453' }}>Sistema de rangos</h3>
          <div style={{ display: 'flex', gap: '0.8rem', flexWrap: 'wrap' }}>
            {RANGOS.map(r => (
              <div key={r.nivel} style={{ flex: 1, minWidth: 100, background: rango.nivel === r.nivel ? `rgba(${r.color === '#f6c453' ? '246,196,83' : r.color === '#cd7f32' ? '205,127,50' : r.color === '#a8a9ad' ? '168,169,173' : '0,212,255'},0.1)` : 'rgba(255,255,255,0.03)', border: `1px solid ${rango.nivel === r.nivel ? r.color : 'rgba(148,163,184,0.1)'}`, borderRadius: 12, padding: '0.8rem', textAlign: 'center' }}>
                <div style={{ width: 14, height: 14, borderRadius: '50%', background: r.color, margin: '0 auto 6px' }}></div>
                <div style={{ fontSize: 13, fontWeight: 700, color: rango.nivel === r.nivel ? r.color : '#94a3b8' }}>{r.nombre}</div>
                <div style={{ fontSize: 11, color: 'rgba(148,163,184,0.5)', marginTop: 2 }}>+€{r.min.toLocaleString()}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PerfilInversor;


