from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

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
    usuario_id = Column(Integer)
    fecha_cita = Column(DateTime)
    tipo_visa = Column(String(100))
    estado = Column(String(50), default='pendiente')
    documentos_estado = Column(String(50), default='pendiente')
    notas = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database initialization
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
