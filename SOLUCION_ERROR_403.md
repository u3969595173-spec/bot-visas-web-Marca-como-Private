# 🔐 SOLUCIÓN ERROR 403 FORBIDDEN

## ❌ Problema
El admin recibe error **403 Forbidden** al intentar aprobar/rechazar solicitudes de crédito.

## 🔍 Causa
La función `verificar_admin()` buscaba el campo `is_admin` en el token JWT, pero el token solo incluye:
- `usuario`: email
- `rol`: 'admin' 
- `exp`: expiración

**No existe** `is_admin` en el token.

## ✅ Corrección Aplicada

### Antes:
```python
def verificar_admin(usuario = Depends(obtener_usuario_actual)):
    if not usuario.get('is_admin'):  # ❌ Campo inexistente
        raise HTTPException(status_code=403)
    return usuario
```

### Después:
```python
def verificar_admin(usuario = Depends(obtener_usuario_actual)):
    if usuario.get('rol') != 'admin':  # ✅ Campo correcto
        raise HTTPException(status_code=403)
    return usuario
```

## 🚀 Solución Inmediata

**El admin debe hacer LOGOUT y LOGIN nuevamente** para obtener un token nuevo con el formato correcto.

### Pasos:
1. ✅ Código corregido y desplegado (commit `85c595f`)
2. ⏳ Render auto-deploy (2-3 minutos)
3. 🔄 Admin hace **LOGOUT**
4. 🔑 Admin hace **LOGIN** nuevamente
5. ✅ Token nuevo funcionará correctamente

## 📊 Verificación

```bash
python verificar_roles_admin.py
```

Resultado:
- ✅ 2 usuarios con `rol='admin'` en BD
- ✅ Login genera token con campo `rol`
- ✅ `verificar_admin()` ahora valida `rol=='admin'`

## 🎯 Endpoints Afectados

Todos los endpoints que usan `verificar_admin`:
- `/api/admin/solicitudes-credito/{id}/responder` ✅
- `/api/admin/*` (todos los endpoints de admin)

## 📝 Nota Técnica

Los tokens JWT son **stateless** y no se pueden invalidar del lado del servidor. Por eso el admin debe obtener un token nuevo haciendo login nuevamente.

---

**Commit:** `85c595f`  
**Estado:** Desplegado en Render  
**Acción requerida:** Admin debe hacer logout/login
