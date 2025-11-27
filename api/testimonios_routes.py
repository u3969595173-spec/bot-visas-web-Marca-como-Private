"""
Endpoints API para Testimonios
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database.models import get_db, Testimonio
from datetime import datetime

router = APIRouter()

@router.get("/testimonios", tags=["Testimonios - Público"])
def listar_testimonios_publicos(
    destacados: bool = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Obtener testimonios aprobados (público)"""
    query = db.query(Testimonio).filter(
        Testimonio.aprobado == True,
        Testimonio.visible == True
    )
    
    if destacados:
        query = query.filter(Testimonio.destacado == True)
    
    total = query.count()
    testimonios = query.order_by(desc(Testimonio.created_at)).offset(offset).limit(limit).all()
    
    return {
        "success": True,
        "total": total,
        "testimonios": [
            {
                "id": t.id,
                "nombre_completo": t.nombre_completo,
                "pais_origen": t.pais_origen,
                "programa_estudio": t.programa_estudio,
                "universidad": t.universidad,
                "ciudad_espana": t.ciudad_espana,
                "rating": t.rating,
                "titulo": t.titulo,
                "testimonio": t.testimonio,
                "foto_url": t.foto_url,
                "video_url": t.video_url,
                "destacado": t.destacado,
                "fecha_experiencia": t.fecha_experiencia.isoformat() if t.fecha_experiencia else None,
                "created_at": t.created_at.isoformat()
            }
            for t in testimonios
        ]
    }

@router.post("/testimonios", tags=["Testimonios - Público"])
def enviar_testimonio(datos: dict, db: Session = Depends(get_db)):
    """Enviar nuevo testimonio (requiere aprobación admin)"""
    try:
        nuevo_testimonio = Testimonio(
            estudiante_id=datos.get('estudiante_id'),
            nombre_completo=datos.get('nombre_completo'),
            pais_origen=datos.get('pais_origen'),
            programa_estudio=datos.get('programa_estudio', ''),
            universidad=datos.get('universidad', ''),
            ciudad_espana=datos.get('ciudad_espana', ''),
            rating=datos.get('rating', 5),
            titulo=datos.get('titulo', ''),
            testimonio=datos.get('testimonio'),
            foto_url=datos.get('foto_url', ''),
            video_url=datos.get('video_url', ''),
            email_contacto=datos.get('email_contacto', ''),
            aprobado=False,  # Requiere aprobación
            destacado=False,
            visible=True,
            fecha_experiencia=datetime.now()
        )
        
        db.add(nuevo_testimonio)
        db.commit()
        db.refresh(nuevo_testimonio)
        
        return {
            "success": True,
            "message": "¡Gracias por tu testimonio! Será revisado por nuestro equipo.",
            "testimonio_id": nuevo_testimonio.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/testimonios/pendientes", tags=["Admin - Testimonios"])
def listar_testimonios_pendientes(db: Session = Depends(get_db)):
    """Listar testimonios pendientes de aprobación"""
    testimonios = db.query(Testimonio).filter(
        Testimonio.aprobado == False
    ).order_by(desc(Testimonio.created_at)).all()
    
    return {
        "success": True,
        "total": len(testimonios),
        "testimonios": [
            {
                "id": t.id,
                "nombre_completo": t.nombre_completo,
                "pais_origen": t.pais_origen,
                "programa_estudio": t.programa_estudio,
                "universidad": t.universidad,
                "rating": t.rating,
                "titulo": t.titulo,
                "testimonio": t.testimonio,
                "foto_url": t.foto_url,
                "video_url": t.video_url,
                "email_contacto": t.email_contacto,
                "created_at": t.created_at.isoformat()
            }
            for t in testimonios
        ]
    }

@router.get("/admin/testimonios", tags=["Admin - Testimonios"])
def listar_todos_testimonios(
    aprobado: bool = None,
    destacado: bool = None,
    db: Session = Depends(get_db)
):
    """Listar todos los testimonios (admin)"""
    query = db.query(Testimonio)
    
    if aprobado is not None:
        query = query.filter(Testimonio.aprobado == aprobado)
    if destacado is not None:
        query = query.filter(Testimonio.destacado == destacado)
    
    testimonios = query.order_by(desc(Testimonio.created_at)).all()
    
    return {
        "success": True,
        "total": len(testimonios),
        "testimonios": [
            {
                "id": t.id,
                "nombre_completo": t.nombre_completo,
                "pais_origen": t.pais_origen,
                "universidad": t.universidad,
                "rating": t.rating,
                "titulo": t.titulo,
                "aprobado": t.aprobado,
                "destacado": t.destacado,
                "visible": t.visible,
                "created_at": t.created_at.isoformat()
            }
            for t in testimonios
        ]
    }

@router.post("/admin/testimonios/{testimonio_id}/aprobar", tags=["Admin - Testimonios"])
def aprobar_testimonio(
    testimonio_id: int,
    destacar: bool = False,
    db: Session = Depends(get_db)
):
    """Aprobar testimonio"""
    testimonio = db.query(Testimonio).filter(Testimonio.id == testimonio_id).first()
    
    if not testimonio:
        raise HTTPException(status_code=404, detail="Testimonio no encontrado")
    
    try:
        testimonio.aprobado = True
        testimonio.destacado = destacar
        testimonio.updated_at = datetime.now()
        db.commit()
        
        return {
            "success": True,
            "message": "Testimonio aprobado exitosamente"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/testimonios/{testimonio_id}/rechazar", tags=["Admin - Testimonios"])
def rechazar_testimonio(testimonio_id: int, db: Session = Depends(get_db)):
    """Rechazar/ocultar testimonio"""
    testimonio = db.query(Testimonio).filter(Testimonio.id == testimonio_id).first()
    
    if not testimonio:
        raise HTTPException(status_code=404, detail="Testimonio no encontrado")
    
    try:
        testimonio.visible = False
        testimonio.updated_at = datetime.now()
        db.commit()
        
        return {
            "success": True,
            "message": "Testimonio rechazado"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/admin/testimonios/{testimonio_id}/destacar", tags=["Admin - Testimonios"])
def marcar_destacado(
    testimonio_id: int,
    destacar: bool,
    db: Session = Depends(get_db)
):
    """Marcar/desmarcar testimonio como destacado"""
    testimonio = db.query(Testimonio).filter(Testimonio.id == testimonio_id).first()
    
    if not testimonio:
        raise HTTPException(status_code=404, detail="Testimonio no encontrado")
    
    try:
        testimonio.destacado = destacar
        testimonio.updated_at = datetime.now()
        db.commit()
        
        return {
            "success": True,
            "message": f"Testimonio {'destacado' if destacar else 'desmarcado'} exitosamente"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/admin/testimonios/{testimonio_id}", tags=["Admin - Testimonios"])
def eliminar_testimonio(testimonio_id: int, db: Session = Depends(get_db)):
    """Eliminar testimonio permanentemente"""
    testimonio = db.query(Testimonio).filter(Testimonio.id == testimonio_id).first()
    
    if not testimonio:
        raise HTTPException(status_code=404, detail="Testimonio no encontrado")
    
    try:
        nombre = testimonio.nombre_completo
        db.delete(testimonio)
        db.commit()
        
        return {
            "success": True,
            "message": f"Testimonio de {nombre} eliminado exitosamente"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
