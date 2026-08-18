# DEPLOYMENT AUTOMÁTICO - VERCEL + RENDER

Tu código está en GitHub: https://github.com/u3969595173-spec/bot-visas-web-Marca-como-Private

## PASO 1: DEPLOY VERCEL (Frontend)

1. Ve a: https://vercel.com
2. Click "Sign Up" → Elige "GitHub"
3. Autoriza y selecciona tu repo: `bot-visas-web-Marca-como-Private`
4. Vercel detectará automáticamente que es Vite
5. Configuración:
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Environment Variable**:
     - Key: `VITE_API_URL`
     - Value: `https://capital-trade-api.onrender.com` (luego actualizarás)
6. Click **"Deploy"** ✅
7. En 2-3 minutos verás URL: `https://tu-app.vercel.app`

## PASO 2: DEPLOY RENDER (Backend)

1. Ve a: https://render.com
2. Click "Sign Up" → Elige "GitHub"
3. Autoriza y selecciona tu repo
4. Click "New +" → "Web Service"
5. Selecciona: `bot-visas-web-Marca-como-Private`
6. Configuración:
   - **Name**: `capital-trade-api`
   - **Runtime**: `Python 3.12`
   - **Build Command**: 
     ```
     pip install -q fastapi uvicorn psycopg2-binary bcrypt python-jose pydantic-settings python-dotenv requests
     ```
   - **Start Command**: 
     ```
     python api_simple.py
     ```
7. **Environment Variables**:
   - `DATABASE_URL` = Tu PostgreSQL URL (ya existe en Render)
   - `ADMIN_USUARIO` = `admin`
   - `ADMIN_PASSWORD` = Tu contraseña
   - `SECRET_KEY` = Tu clave secreta
8. Plan: Elige **"Free"**
9. Click **"Create Web Service"** ✅
10. En 3-5 minutos verás URL: `https://capital-trade-api.onrender.com`

## PASO 3: ACTUALIZAR VERCEL CON URL DE RENDER

1. Ve a Vercel
2. Tu proyecto → **Settings**
3. **Environment Variables**
4. Edita `VITE_API_URL` y cambia a: `https://capital-trade-api.onrender.com`
5. Redeploy automático ✅

## RESULTADO FINAL

- **Frontend**: https://tu-app.vercel.app ✅
- **Backend**: https://capital-trade-api.onrender.com ✅
- **Funcionan 24/7 automáticamente** ✅

## AHORA:

1. Crea cuenta en Vercel (5 minutos)
2. Crea cuenta en Render (5 minutos)
3. Sigue los pasos arriba
4. Me avisas cuando estén ONLINE

¿Empezamos?
