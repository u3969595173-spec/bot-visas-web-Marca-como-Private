from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import Notificacion, Estudiante, get_db
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()

# Schemas
class NotificacionCreate(BaseModel):
    estudiante_id: int
    tipo: str
    titulo: str
    mensaje: str
    url_accion: Optional[str] = None
    icono: Optional[str] = '🔔'
    prioridad: Optional[str] = 'normal'

class NotificacionResponse(BaseModel):
    id: int
    tipo: str
    titulo: str
    mensaje: str
    leida: bool
    url_accion: Optional[str]
    icono: str
    prioridad: str
    created_at: datetime

    class Config:
        from_attributes = True

# ============================================
# ENDPOINTS PÚBLICOS (requieren estudiante_id)
# ============================================

@router.get("/notificaciones/{estudiante_id}")
def listar_notificaciones(
    estudiante_id: int,
    limit: int = 50,
    solo_no_leidas: bool = False,
    db: Session = Depends(get_db)
):
    """Listar notificaciones de un estudiante"""
    try:
        query = db.query(Notificacion).filter(
            Notificacion.estudiante_id == estudiante_id
        )
        
        if solo_no_leidas:
            query = query.filter(Notificacion.leida == False)
        
        notificaciones = query.order_by(
            Notificacion.created_at.desc()
        ).limit(limit).all()
        
        return {
            "success": True,
            "notificaciones": [
                {
                    "id": n.id,
                    "tipo": n.tipo,
                    "titulo": n.titulo,
                    "mensaje": n.mensaje,
                    "leida": n.leida,
                    "url_accion": n.url_accion,
                    "icono": n.icono,
                    "prioridad": n.prioridad,
                    "created_at": n.created_at.isoformat()
                }
                for n in notificaciones
            ],
            "total": len(notificaciones)
        }
    except Exception as e:
        print(f"❌ Error listando notificaciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/notificaciones/{estudiante_id}/contar")
def contar_no_leidas(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    """Contar notificaciones no leídas"""
    try:
        count = db.query(Notificacion).filter(
            Notificacion.estudiante_id == estudiante_id,
            Notificacion.leida == False
        ).count()
        
        return {
            "success": True,
            "no_leidas": count
        }
    except Exception as e:
        print(f"❌ Error contando no leídas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notificaciones/{notificacion_id}/marcar-leida")
def marcar_leida(
    notificacion_id: int,
    db: Session = Depends(get_db)
):
    """Marcar una notificación como leída"""
    try:
        notificacion = db.query(Notificacion).filter(
            Notificacion.id == notificacion_id
        ).first()
        
        if not notificacion:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        notificacion.leida = True
        db.commit()
        
        return {
            "success": True,
            "message": "Notificación marcada como leída"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error marcando leída: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notificaciones/{estudiante_id}/marcar-todas-leidas")
def marcar_todas_leidas(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    """Marcar todas las notificaciones de un estudiante como leídas"""
    try:
        db.query(Notificacion).filter(
            Notificacion.estudiante_id == estudiante_id,
            Notificacion.leida == False
        ).update({"leida": True})
        
        db.commit()
        
        return {
            "success": True,
            "message": "Todas las notificaciones marcadas como leídas"
        }
    except Exception as e:
        db.rollback()
        print(f"❌ Error marcando todas leídas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# FUNCIONES INTERNAS (crear notificaciones)
# ============================================

def crear_notificacion(
    db: Session,
    estudiante_id: int,
    tipo: str,
    titulo: str,
    mensaje: str,
    url_accion: Optional[str] = None,
    icono: Optional[str] = '🔔',
    prioridad: Optional[str] = 'normal'
):
    """Función helper para crear notificaciones desde otros módulos"""
    try:
        notificacion = Notificacion(
            estudiante_id=estudiante_id,
            tipo=tipo,
            titulo=titulo,
            mensaje=mensaje,
            url_accion=url_accion,
            icono=icono,
            prioridad=prioridad,
            leida=False
        )
        db.add(notificacion)
        db.commit()
        db.refresh(notificacion)
        
        print(f"✅ Notificación creada: {titulo} para estudiante {estudiante_id}")
        return notificacion
    except Exception as e:
        db.rollback()
        print(f"❌ Error creando notificación: {e}")
        return None

# ============================================
# ENDPOINTS ADMIN
# ============================================

@router.post("/admin/notificaciones/enviar")
def enviar_notificacion_admin(
    data: NotificacionCreate,
    db: Session = Depends(get_db)
):
    """Admin envía notificación manual a un estudiante"""
    try:
        # Verificar que el estudiante existe
        estudiante = db.query(Estudiante).filter(Estudiante.id == data.estudiante_id).first()
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        notificacion = crear_notificacion(
            db=db,
            estudiante_id=data.estudiante_id,
            tipo=data.tipo,
            titulo=data.titulo,
            mensaje=data.mensaje,
            url_accion=data.url_accion,
            icono=data.icono,
            prioridad=data.prioridad
        )
        
        if not notificacion:
            raise HTTPException(status_code=500, detail="Error creando notificación")
        
        return {
            "success": True,
            "message": "Notificación enviada",
            "notificacion_id": notificacion.id
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error enviando notificación admin: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/admin/notificaciones/{notificacion_id}")
def eliminar_notificacion(
    notificacion_id: int,
    db: Session = Depends(get_db)
):
    """Admin elimina una notificación"""
    try:
        notificacion = db.query(Notificacion).filter(
            Notificacion.id == notificacion_id
        ).first()
        
        if not notificacion:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        db.delete(notificacion)
        db.commit()
        
        return {
            "success": True,
            "message": "Notificación eliminada"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error eliminando notificación: {e}")
        raise HTTPException(status_code=500, detail=str(e))
