import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const RANGOS = [
  { nivel: 1, nombre: 'Community',        emoji: '🌱', color: '#4ade80', min: 5,   max: 24,  cupo: '2%',  beneficio: '25 USDT/mes' },
  { nivel: 2, nombre: 'Leader',           emoji: '⭐', color: '#facc15', min: 25,  max: 49,  cupo: '5%',  beneficio: '50 USDT/mes' },
  { nivel: 3, nombre: 'Senior Leader',    emoji: '🔥', color: '#fb923c', min: 50,  max: 99,  cupo: '10%', beneficio: '100 USDT/mes' },
  { nivel: 4, nombre: 'Elite Leader',     emoji: '💎', color: '#60a5fa', min: 100, max: 199, cupo: '15%', beneficio: '150 USDT/mes' },
  { nivel: 5, nombre: 'Executive Leader', emoji: '👑', color: '#c084fc', min: 200, max: 499, cupo: '25%', beneficio: '250 USDT/mes' },
  { nivel: 6, nombre: 'Founding Leader',  emoji: '🏆', color: '#f6c453', min: 500, max: null, cupo: '43%', beneficio: '400 USDT/mes' },
];

function getRango(miembros = 0) {
  return [...RANGOS].reverse().find(r => miembros >= r.min) || null;
}

const getApiUrl = () => {
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  return window.location.hostname === 'localhost' ? 'http://localhost:8000' : `http://${window.location.hostname}:8000`;
};

function PerfilInversor() {
  const navigate = useNavigate();
  const userSession = React.useMemo(() => {
    try { return JSON.parse(localStorage.getItem('capital_trade_user') || 'null'); } catch { return null; }
  }, []);

  const [perfil, setPerfil] = useState(null);
  const [fotoPerfil, setFotoPerfil] = useState(null);
  const [fotoPortada, setFotoPortada] = useState(null);
  const [guardando, setGuardando] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({ nombre: '', telefono: '', pais: '' });

  const fotoRef = useRef();
  const portadaRef = useRef();
  const token = localStorage.getItem('token');

  useEffect(() => {
    const defaultForm = {
      nombre: userSession?.name || userSession?.nombre || 'Inversor',
      telefono: userSession?.telefono || '',
      pais: userSession?.pais || 'España'
    };
    setEditForm(defaultForm);

    if (!token) return;
    axios.get(`${getApiUrl()}/api/inversores/perfil`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => {
        setPerfil(r.data);
        if (r.data.foto_perfil) setFotoPerfil(r.data.foto_perfil);
        if (r.data.foto_portada) setFotoPortada(r.data.foto_portada);
        setEditForm({
          nombre: r.data.nombre || defaultForm.nombre,
          telefono: r.data.telefono || defaultForm.telefono,
          pais: r.data.pais || defaultForm.pais
        });
      })
      .catch((error) => {
        if (error.response?.status === 401 || error.response?.status === 403 || error.response?.status === 404) {
          localStorage.removeItem('token');
          localStorage.removeItem('usuario');
          localStorage.removeItem('capital_trade_user');
          window.dispatchEvent(new Event('capital-trade-sync'));
          navigate('/login');
        }
      });
  }, [token]);

  const handleSaveProfile = () => {
    setPerfil(prev => ({ ...prev, ...editForm }));
    if (userSession) {
      localStorage.setItem('capital_trade_user', JSON.stringify({ ...userSession, ...editForm, name: editForm.nombre }));
      window.dispatchEvent(new Event('capital-trade-sync'));
    }
    setIsEditing(false);
    if (token) {
      axios.put(`${getApiUrl()}/api/inversores/perfil/actualizar`, editForm, { headers: { Authorization: `Bearer ${token}` } }).catch(() => { });
    }
  };

  const nombre = perfil?.nombre || userSession?.name || userSession?.nombre || 'Inversor';
  const email = perfil?.email || userSession?.email || '—';
  const telefono = perfil?.telefono || userSession?.telefono || '—';
  const pais = perfil?.pais || userSession?.pais || 'España';
  const rango = getRango(perfil?.miembros || 0);

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
      <div style={{ maxWidth: 700, margin: '0 auto', padding: '0 1.5rem', position: 'relative', zIndex: 10 }}>
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
            <h1 style={{ margin: 0, fontSize: '1.6rem', fontWeight: 800, color: '#f8fafc', lineHeight: 1.2, wordBreak: 'break-word', paddingBottom: '2px' }}>
              {isEditing ? <input value={editForm.nombre} onChange={e => setEditForm({ ...editForm, nombre: e.target.value })} style={{ background: 'transparent', border: '1px solid #f6c453', color: '#fff', fontSize: '1.6rem', fontWeight: 800, width: '100%', borderRadius: 4, padding: '4px 8px', outline: 'none' }} /> : nombre}
            </h1>
            {rango ? (
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, marginTop: 6, background: 'rgba(255,255,255,0.05)', border: `1px solid ${rango.color}`, borderRadius: 999, padding: '4px 14px' }}>
                <span>{rango.emoji}</span>
                <span style={{ fontSize: 13, fontWeight: 700, color: rango.color }}>{rango.nombre}</span>
              </div>
            ) : (
              <div style={{ display: 'inline-flex', marginTop: 6, background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(148,163,184,0.2)', borderRadius: 999, padding: '4px 14px' }}>
                <span style={{ fontSize: 13, color: '#94a3b8' }}>Sin nivel asignado</span>
              </div>
            )}
          </div>
        </div>

        <hr style={{ border: 'none', borderTop: '1px solid rgba(148,163,184,0.1)', margin: '0 0 1.5rem' }} />

        {/* Info */}
        <div style={{ background: 'rgba(15,23,42,0.7)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 16, padding: '1.5rem', marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem' }}>
            <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: 700, color: '#f6c453' }}>Información</h3>
            {isEditing ? (
              <button onClick={handleSaveProfile} style={{ background: '#f6c453', color: '#000', border: 'none', padding: '4px 12px', borderRadius: 4, cursor: 'pointer', fontWeight: 700 }}>Guardar</button>
            ) : (
              <button onClick={() => setIsEditing(true)} style={{ background: 'transparent', color: '#f6c453', border: '1px solid #f6c453', padding: '4px 12px', borderRadius: 4, cursor: 'pointer', fontWeight: 600 }}>Editar info</button>
            )}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {[
              { icon: '✉️', label: 'Email', value: email, editable: false },
              { icon: '📞', label: 'Teléfono', value: telefono, editable: true, field: 'telefono' },
              { icon: '🌍', label: 'País', value: pais, editable: true, field: 'pais' },
              { icon: '🏅', label: 'Nivel', value: rango ? `${rango.emoji} ${rango.nombre}` : 'Sin nivel', editable: false },
            ].map(item => (
              <div key={item.label} style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
                <span style={{ fontSize: 18, width: 28, textAlign: 'center' }}>{item.icon}</span>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 11, color: 'rgba(148,163,184,0.6)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{item.label}</div>
                  {isEditing && item.editable ? (
                    <input value={editForm[item.field]} onChange={e => setEditForm({ ...editForm, [item.field]: e.target.value })} style={{ background: 'rgba(0,0,0,0.2)', border: '1px solid #334155', color: '#f1f5f9', width: '100%', maxWidth: 300, padding: '4px 8px', borderRadius: 4, marginTop: 4, fontSize: 14, outline: 'none' }} />
                  ) : (
                    <div style={{ fontSize: 15, fontWeight: 600, color: '#f1f5f9' }}>{item.value}</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Rango actual + botón programa */}
        <div style={{ background: 'rgba(15,23,42,0.7)', border: '1px solid rgba(148,163,184,0.1)', borderRadius: 16, padding: '1.5rem', marginBottom: '2rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <span style={{ fontSize: 36 }}>{rango ? rango.emoji : '🔒'}</span>
            <div>
              <div style={{ fontSize: 11, color: 'rgba(148,163,184,0.6)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 4 }}>Tu nivel actual</div>
              {rango ? (
                <>
                  <div style={{ fontSize: '1.2rem', fontWeight: 800, color: rango.color }}>{rango.nombre}</div>
                  <div style={{ fontSize: 13, color: '#94a3b8', marginTop: 2 }}>Cupo {rango.cupo} · {rango.beneficio}</div>
                </>
              ) : (
                <>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#94a3b8' }}>Sin nivel asignado</div>
                  <div style={{ fontSize: 13, color: 'rgba(148,163,184,0.5)', marginTop: 2 }}>Necesitas mínimo 5 miembros activos</div>
                </>
              )}
            </div>
          </div>
          <button onClick={() => navigate('/programa')} style={{ background: 'linear-gradient(135deg, #f6c453, #dba93a)', color: '#0a0f1a', border: 'none', padding: '0.7rem 1.4rem', borderRadius: 10, fontWeight: 700, fontSize: 14, cursor: 'pointer', whiteSpace: 'nowrap' }}>
            Ver programa →
          </button>
        </div>
      </div>
    </div>
  );
}

export default PerfilInversor;

