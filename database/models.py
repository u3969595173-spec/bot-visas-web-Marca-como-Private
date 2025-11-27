from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    language = Column(String(10), default='es')
    subscription_tier = Column(String(50), default='free')  # free, basic, premium, success_fee
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class VisaApplication(Base):
    __tablename__ = 'visa_applications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    
    # Personal Information
    country_origin = Column(String(100))
    study_type = Column(String(100))
    university = Column(String(255))
    university_type = Column(String(100))
    course_name = Column(String(255))
    course_duration_months = Column(Integer)
    course_cost = Column(Float)
    
    # Economic Situation
    total_funds = Column(Float)
    funds_sources = Column(JSON)  # List of sources: own, parents, scholarship, loan
    
    # Documents Status
    documents_uploaded = Column(JSON)  # Dict of document: status
    documents_validated = Column(JSON)  # Dict of document: validation result
    
    # Prediction
    success_probability = Column(Float)
    score_breakdown = Column(JSON)
    risk_factors = Column(JSON)
    
    # Interview
    interview_date = Column(DateTime, nullable=True)
    interview_practice_count = Column(Integer, default=0)
    interview_practice_score = Column(Float, nullable=True)
    
    # Status Tracking
    application_status = Column(String(50), default='in_progress')  # in_progress, submitted, approved, rejected
    submission_date = Column(DateTime, nullable=True)
    decision_date = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    tier = Column(String(50))  # basic, premium, success_fee
    amount = Column(Float)
    stripe_payment_id = Column(String(255))
    status = Column(String(50))  # pending, completed, refunded
    created_at = Column(DateTime, default=datetime.utcnow)

class InterviewPractice(Base):
    __tablename__ = 'interview_practices'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    question = Column(Text)
    user_answer = Column(Text)
    ai_evaluation = Column(JSON)  # score, problems, improved_answer
    created_at = Column(DateTime, default=datetime.utcnow)

class Reminder(Base):
    __tablename__ = 'reminders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    reminder_type = Column(String(100))  # document_expiry, interview, submission
    reminder_date = Column(DateTime)
    message = Column(Text)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Web platform models
class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    telefono = Column(String(50))
    rol = Column(String(50), default='estudiante')
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)

class Estudiante(Base):
    __tablename__ = 'estudiantes'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    email = Column(String(255))
    telefono = Column(String(50))
    pasaporte = Column(String(100))
    edad = Column(Integer)
    nacionalidad = Column(String(100))
    ciudad_origen = Column(String(100))
    especialidad = Column(String(255))
    nivel_espanol = Column(String(50))
    fondos_disponibles = Column(Integer)
    usuario_id = Column(Integer)
    fecha_cita = Column(DateTime)
    tipo_visa = Column(String(100))
    estado = Column(String(50), default='pendiente')
    documentos_estado = Column(String(50), default='pendiente')
    curso_asignado_id = Column(Integer)
    alojamiento_asignado_id = Column(Integer)
    universidad_referidora_id = Column(Integer)
    codigo_referido = Column(String(50))
    notas = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FechaImportante(Base):
    __tablename__ = 'fechas_importantes'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, nullable=False)
    tipo_fecha = Column(String(100), nullable=False)  # entrevista, vencimiento_documento, deadline_aplicacion, cita_visa, etc.
    fecha = Column(DateTime, nullable=False)
    descripcion = Column(Text)
    alertado_30d = Column(Boolean, default=False)
    alertado_15d = Column(Boolean, default=False)
    alertado_7d = Column(Boolean, default=False)
    alertado_1d = Column(Boolean, default=False)
    completada = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UniversidadEspana(Base):
    __tablename__ = 'universidades_espana'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    siglas = Column(String(50))
    ciudad = Column(String(100), nullable=False)
    comunidad_autonoma = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)  # publica, privada
    url_oficial = Column(String(500))
    email_contacto = Column(String(255))
    telefono = Column(String(50))
    tiene_api = Column(Boolean, default=False)
    endpoint_api = Column(String(500))
    metodo_scraping = Column(String(100))  # beautifulsoup, selenium, api_rest
    ultima_actualizacion = Column(DateTime)
    logo_url = Column(String(500))
    descripcion = Column(Text)
    ranking_nacional = Column(Integer)
    total_alumnos = Column(Integer)
    total_programas = Column(Integer)
    acepta_extranjeros = Column(Boolean, default=True)
    requisitos_extranjeros = Column(Text)
    activa = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProgramaUniversitario(Base):
    __tablename__ = 'programas_universitarios'
    
    id = Column(Integer, primary_key=True)
    universidad_id = Column(Integer, nullable=False)
    nombre = Column(String(500), nullable=False)
    tipo_programa = Column(String(100))  # grado, master, doctorado, curso
    area_estudio = Column(String(200))  # ingenieria, medicina, arte, etc.
    duracion_anos = Column(Float)
    creditos_ects = Column(Integer)
    idioma = Column(String(50))  # espanol, ingles, bilingue
    modalidad = Column(String(50))  # presencial, online, hibrido
    precio_anual_eur = Column(Float)
    plazas_disponibles = Column(Integer)
    nota_corte = Column(Float)
    url_info = Column(String(500))
    fecha_inicio_inscripcion = Column(DateTime)
    fecha_fin_inscripcion = Column(DateTime)
    requisitos = Column(Text)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BlogPost(Base):
    __tablename__ = 'blog_posts'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, nullable=False)
    contenido = Column(Text, nullable=False)
    extracto = Column(Text)
    categoria = Column(String(100))
    autor_nombre = Column(String(200), default='Equipo Editorial')
    imagen_portada = Column(String(500))
    meta_description = Column(String(300))
    meta_keywords = Column(String(500))
    visitas = Column(Integer, default=0)
    publicado = Column(Boolean, default=False)
    destacado = Column(Boolean, default=False)
    fecha_publicacion = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Testimonio(Base):
    __tablename__ = 'testimonios'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer)
    nombre_completo = Column(String(200), nullable=False)
    pais_origen = Column(String(100), nullable=False)
    programa_estudio = Column(String(300))
    universidad = Column(String(300))
    ciudad_espana = Column(String(100))
    rating = Column(Integer)
    titulo = Column(String(300))
    testimonio = Column(Text, nullable=False)
    foto_url = Column(String(500))
    video_url = Column(String(500))
    email_contacto = Column(String(200))
    aprobado = Column(Boolean, default=False)
    destacado = Column(Boolean, default=False)
    visible = Column(Boolean, default=True)
    fecha_experiencia = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Notificacion(Base):
    __tablename__ = 'notificaciones'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, nullable=False)  # Relación con Student
    tipo = Column(String(50), nullable=False)  # 'mensaje', 'estado', 'documento', 'alerta', 'sistema'
    titulo = Column(String(200), nullable=False)
    mensaje = Column(Text, nullable=False)
    leida = Column(Boolean, default=False)
    url_accion = Column(String(500))  # URL donde redirigir al hacer clic
    icono = Column(String(20), default='🔔')  # Emoji del icono
    prioridad = Column(String(20), default='normal')  # 'baja', 'normal', 'alta', 'urgente'
    created_at = Column(DateTime, default=datetime.utcnow)

class MensajeChat(Base):
    __tablename__ = 'mensajes_chat'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, nullable=False)
    admin_id = Column(Integer)  # NULL si mensaje es del estudiante
    remitente = Column(String(20), nullable=False)  # 'estudiante' o 'admin'
    mensaje = Column(Text, nullable=False)
    leido = Column(Boolean, default=False)
    tipo = Column(String(20), default='texto')  # 'texto', 'sistema', 'archivo'
    created_at = Column(DateTime, default=datetime.utcnow)

# Database initialization
from dotenv import load_dotenv
load_dotenv()  # Cargar .env ANTES de crear engine

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL no encontrada en .env")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
