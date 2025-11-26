"""
Schemas Pydantic para validación de datos API
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ============================================================================
# ESTUDIANTE
# ============================================================================

class EstudianteCreate(BaseModel):
    """Datos para registro de nuevo estudiante"""
    nombre_completo: str = Field(..., min_length=3, max_length=100)
    numero_pasaporte: str = Field(..., min_length=5, max_length=20)
    edad: int = Field(..., ge=18, le=65)
    nacionalidad: str = Field(..., min_length=2, max_length=50)
    ciudad_origen: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: str = Field(..., min_length=8, max_length=20)
    especialidad_interes: str = Field(..., min_length=3, max_length=100)
    nivel_espanol: str = Field(..., pattern="^(A1|A2|B1|B2|C1|C2|Nativo)$")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre_completo": "Carlos Pérez García",
                "numero_pasaporte": "ABC123456",
                "edad": 24,
                "nacionalidad": "Cubana",
                "ciudad_origen": "La Habana",
                "email": "carlos@email.com",
                "telefono": "+5355123456",
                "especialidad_interes": "Ingeniería de Software",
                "nivel_espanol": "B2"
            }
        }


class EstudianteUpdate(BaseModel):
    """Datos para actualizar estudiante"""
    nombre_completo: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    especialidad_interes: Optional[str] = None
    nivel_espanol: Optional[str] = None
    estado_procesamiento: Optional[str] = None
    estado_visa: Optional[str] = None
    notas_admin: Optional[str] = None


class EstudianteResponse(BaseModel):
    """Respuesta con datos de estudiante"""
    id: int
    nombre_completo: str
    numero_pasaporte: str
    edad: int
    nacionalidad: str
    ciudad_origen: str
    email: str
    telefono: str
    especialidad_interes: str
    nivel_espanol: str
    estado_procesamiento: str
    estado_visa: str
    created_at: datetime
    fecha_procesamiento_automatico: Optional[datetime]
    admin_revisor_id: Optional[int]
    curso_seleccionado_id: Optional[int]
    
    class Config:
        from_attributes = True


# ============================================================================
# AUTENTICACIÓN
# ============================================================================

class LoginRequest(BaseModel):
    """Datos de login"""
    usuario: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    
    class Config:
        json_schema_extra = {
            "example": {
                "usuario": "leandroeloytamayoreyes@gmail.com",
                "password": "Eloy1940"
            }
        }


class LoginResponse(BaseModel):
    """Respuesta de login exitoso"""
    token: str
    tipo: str = "Bearer"
    usuario: str
    rol: str


# ============================================================================
# ESTADÍSTICAS
# ============================================================================

class EstadisticasResponse(BaseModel):
    """Estadísticas del dashboard"""
    total_estudiantes: int
    pendientes_revision: int
    aprobados: int
    enviados: int
    por_especialidad: dict[str, int]


class EstadoEstudiante(BaseModel):
    """Estado público de estudiante"""
    nombre: str
    estado_procesamiento: str
    estado_visa: str
    fecha_registro: datetime
    mensaje: str
