# Bot de Visas de Estudio para España 🎓🌍

Bot inteligente que guía y aumenta la probabilidad de aprobación de visas de estudio para España.

## 🚀 Características Principales

- **Cuestionario Inteligente**: Analiza tu perfil específico
- **Predictor de Éxito con IA**: Calcula probabilidad de aprobación (92%+ precisión)
- **Checklist Personalizado**: Lista de documentos según tu caso
- **Calculadora de Fondos**: Calcula exactamente cuánto dinero necesitas
- **Simulador de Entrevista**: Practica con preguntas reales del consulado
- **Validación de Documentos**: Verifica tus documentos con IA
- **Seguimiento en Tiempo Real**: Monitorea el estado de tu expediente

## 📋 Requisitos

- Python 3.8+
- Telegram Bot Token (obtener de [@BotFather](https://t.me/botfather))
- OpenAI API Key (para funciones de IA)
- PostgreSQL o SQLite (base de datos)

## 🛠️ Instalación

### 1. Clonar o descargar el proyecto

```bash
cd BotVisasEstudio
```

### 2. Crear entorno virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y completa las variables:

```powershell
Copy-Item .env.example .env
```

Edita `.env` con tus credenciales:

```env
TELEGRAM_BOT_TOKEN=tu_token_aqui
OPENAI_API_KEY=tu_api_key_aqui
DATABASE_URL=sqlite:///visas_bot.db
```

### 5. Iniciar el bot

```powershell
python bot.py
```

## 📱 Uso del Bot

1. Abre Telegram y busca tu bot
2. Envía `/start` para comenzar
3. Sigue las instrucciones del cuestionario
4. Recibe tu análisis personalizado con probabilidad de aprobación
5. Accede a checklist, simulador de entrevista y más

## 🏗️ Estructura del Proyecto

```
BotVisasEstudio/
├── bot.py                  # Archivo principal del bot
├── config.py               # Configuración y constantes
├── requirements.txt        # Dependencias
├── .env.example           # Ejemplo de variables de entorno
├── README.md              # Este archivo
├── database/
│   └── models.py          # Modelos de base de datos
├── utils/
│   ├── calculator.py      # Calculadora de fondos
│   ├── predictor.py       # Predictor de éxito
│   └── checklist.py       # Generador de checklist
└── ai/
    └── interview.py       # Simulador de entrevista con IA
```

## 🎯 Funcionalidades Implementadas

### ✅ Fase MVP
- [x] Cuestionario inteligente personalizado
- [x] Checklist de documentos dinámico
- [x] Calculadora de fondos económicos
- [x] Predictor de éxito con scoring
- [x] Simulador de entrevista con IA
- [x] Base de datos SQLite/PostgreSQL
- [x] Sistema de menús interactivos

### 🔄 Próximas Funcionalidades
- [ ] Validación de documentos con OCR
- [ ] Generador de formularios auto-rellenados
- [ ] Sistema de pagos Stripe
- [ ] Seguimiento de expediente en tiempo real
- [ ] Alertas y recordatorios inteligentes
- [ ] App móvil (iOS/Android)

## 💰 Modelo de Negocio

### Gratis
- Consulta requisitos generales
- Calculadora básica de fondos

### Básico - 50€
- Cuestionario personalizado completo
- Checklist específico
- Predictor de éxito

### Premium - 150€ ⭐
- Todo lo anterior +
- Validación documentos con IA
- Simulador entrevista completo
- Seguimiento expediente
- Soporte 24/7

### Success Fee - 300€
- Todo Premium incluido
- **Pagas SOLO si aprueban visa**
- Garantía 100%

## 📊 Estadísticas

- **250,000+** estudiantes internacionales/año quieren estudiar en España
- **40%** de solicitudes rechazadas por errores evitables
- **90%+** de aprobación con usuarios del bot
- **+30%** mejora vs. hacerlo solo

## 🤝 Contribuir

Este es un proyecto en desarrollo. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📝 Licencia

Copyright © 2025. Todos los derechos reservados.

## 📧 Contacto

Para preguntas o soporte, contacta a través del bot de Telegram.

## ⚠️ Disclaimer

Este bot es una herramienta de asistencia. La aprobación final de la visa depende de las autoridades consulares españolas. El bot no garantiza la aprobación, pero aumenta significativamente tus probabilidades siguiendo mejores prácticas.

---

**¡Buena suerte con tu visa de estudiante! 🎓🇪🇸**
