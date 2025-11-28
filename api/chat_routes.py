from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from database.models import MensajeChat, Estudiante, get_db
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json

router = APIRouter()

# Manager de conexiones WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}  # {estudiante_id: websocket}
        self.admin_connections: dict = {}   # {admin_id: websocket}
    
    async def connect(self, websocket: WebSocket, user_id: int, user_type: str):
        await websocket.accept()
        if user_type == "estudiante":
            self.active_connections[user_id] = websocket
        elif user_type == "admin":
            self.admin_connections[user_id] = websocket
        print(f"✅ {user_type} {user_id} conectado al chat")
    
    def disconnect(self, user_id: int, user_type: str):
        if user_type == "estudiante" and user_id in self.active_connections:
            del self.active_connections[user_id]
        elif user_type == "admin" and user_id in self.admin_connections:
            del self.admin_connections[user_id]
        print(f"❌ {user_type} {user_id} desconectado del chat")
    
    async def send_personal_message(self, message: dict, user_id: int, user_type: str):
        websocket = None
        if user_type == "estudiante":
            websocket = self.active_connections.get(user_id)
        elif user_type == "admin":
            websocket = self.admin_connections.get(user_id)
        
        if websocket:
            await websocket.send_json(message)
    
    async def notify_admin(self, estudiante_id: int, message: dict):
        # Notificar a todos los admins conectados
        for admin_id, websocket in self.admin_connections.items():
            try:
                await websocket.send_json({
                    "type": "nuevo_mensaje_estudiante",
                    "estudiante_id": estudiante_id,
                    "message": message
                })
            except:
                pass

manager = ConnectionManager()

# Schemas
class MensajeChatCreate(BaseModel):
    estudiante_id: int
    mensaje: str
    remitente: str  # 'estudiante' o 'admin'
    admin_id: Optional[int] = None

class MensajeChatResponse(BaseModel):
    id: int
    estudiante_id: int
    admin_id: Optional[int]
    remitente: str
    mensaje: str
    leido: bool
    tipo: str
    created_at: datetime

    class Config:
        from_attributes = True

# ============================================
# ENDPOINTS REST (para historial y envío)
# ============================================

@router.get("/chat/{estudiante_id}/mensajes")
def obtener_historial_chat(
    estudiante_id: int,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener historial de mensajes de un estudiante"""
    try:
        mensajes = db.query(MensajeChat).filter(
            MensajeChat.estudiante_id == estudiante_id
        ).order_by(
            MensajeChat.created_at.asc()
        ).limit(limit).all()
        
        return {
            "success": True,
            "mensajes": [
                {
                    "id": m.id,
                    "estudiante_id": m.estudiante_id,
                    "admin_id": m.admin_id,
                    "remitente": m.remitente,
                    "mensaje": m.mensaje,
                    "leido": m.leido,
                    "tipo": m.tipo,
                    "created_at": m.created_at.isoformat()
                }
                for m in mensajes
            ],
            "total": len(mensajes)
        }
    except Exception as e:
        print(f"❌ Error obteniendo historial: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/enviar")
def enviar_mensaje_chat(
    data: MensajeChatCreate,
    db: Session = Depends(get_db)
):
    """Enviar mensaje de chat (REST endpoint de respaldo)"""
    try:
        mensaje = MensajeChat(
            estudiante_id=data.estudiante_id,
            admin_id=data.admin_id,
            remitente=data.remitente,
            mensaje=data.mensaje,
            leido=False,
            tipo='texto'
        )
        db.add(mensaje)
        db.commit()
        db.refresh(mensaje)
        
        return {
            "success": True,
            "mensaje": {
                "id": mensaje.id,
                "estudiante_id": mensaje.estudiante_id,
                "remitente": mensaje.remitente,
                "mensaje": mensaje.mensaje,
                "created_at": mensaje.created_at.isoformat()
            }
        }
    except Exception as e:
        db.rollback()
        print(f"❌ Error enviando mensaje: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/{mensaje_id}/marcar-leido")
def marcar_mensaje_leido(
    mensaje_id: int,
    db: Session = Depends(get_db)
):
    """Marcar mensaje como leído"""
    try:
        mensaje = db.query(MensajeChat).filter(MensajeChat.id == mensaje_id).first()
        if not mensaje:
            raise HTTPException(status_code=404, detail="Mensaje no encontrado")
        
        mensaje.leido = True
        db.commit()
        
        return {"success": True, "message": "Mensaje marcado como leído"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/{estudiante_id}/marcar-todos-leidos")
def marcar_todos_mensajes_leidos(
    estudiante_id: int,
    remitente: str,  # 'admin' o 'estudiante'
    db: Session = Depends(get_db)
):
    """Marcar TODOS los mensajes de una conversación como leídos"""
    try:
        # Marcar todos los mensajes del remitente especificado como leídos
        mensajes_actualizados = db.query(MensajeChat).filter(
            MensajeChat.estudiante_id == estudiante_id,
            MensajeChat.remitente == remitente,
            MensajeChat.leido == False
        ).update({MensajeChat.leido: True})
        
        db.commit()
        
        return {
            "success": True, 
            "message": f"Marcados {mensajes_actualizados} mensajes como leídos",
            "mensajes_actualizados": mensajes_actualizados
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/chat/{estudiante_id}/marcar-leidos")
def admin_marcar_mensajes_leidos(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    """Admin marca como leídos todos los mensajes del estudiante"""
    try:
        # El admin marca como leídos todos los mensajes que el estudiante le envió
        mensajes_actualizados = db.query(MensajeChat).filter(
            MensajeChat.estudiante_id == estudiante_id,
            MensajeChat.remitente == "estudiante",  # Mensajes que el estudiante envió al admin
            MensajeChat.leido == False
        ).update({MensajeChat.leido: True})
        
        db.commit()
        
        return {
            "success": True, 
            "message": f"Admin marcó {mensajes_actualizados} mensajes como leídos",
            "mensajes_actualizados": mensajes_actualizados
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/estudiante/chat/{estudiante_id}/marcar-leidos")
def estudiante_marcar_mensajes_leidos(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    """Estudiante marca como leídos todos los mensajes del admin"""
    try:
        # El estudiante marca como leídos todos los mensajes que el admin le envió
        mensajes_actualizados = db.query(MensajeChat).filter(
            MensajeChat.estudiante_id == estudiante_id,
            MensajeChat.remitente == "admin",  # Mensajes que el admin envió al estudiante
            MensajeChat.leido == False
        ).update({MensajeChat.leido: True})
        
        db.commit()
        
        return {
            "success": True, 
            "message": f"Estudiante marcó {mensajes_actualizados} mensajes como leídos",
            "mensajes_actualizados": mensajes_actualizados
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/{estudiante_id}/no-leidos")
def contar_mensajes_no_leidos(
    estudiante_id: int,
    remitente: str,  # 'admin' para contar mensajes del admin no leídos por estudiante
    db: Session = Depends(get_db)
):
    """Contar mensajes no leídos"""
    try:
        count = db.query(MensajeChat).filter(
            MensajeChat.estudiante_id == estudiante_id,
            MensajeChat.remitente == remitente,
            MensajeChat.leido == False
        ).count()
        
        return {"success": True, "no_leidos": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# WEBSOCKET (tiempo real)
# ============================================

@router.websocket("/ws/chat/{estudiante_id}/{user_type}")
async def websocket_chat(
    websocket: WebSocket,
    estudiante_id: int,
    user_type: str,  # 'estudiante' o 'admin'
    db: Session = Depends(get_db)
):
    """
    WebSocket para chat en tiempo real
    user_type: 'estudiante' o 'admin'
    """
    await manager.connect(websocket, estudiante_id, user_type)
    
    try:
        while True:
            # Recibir mensaje
            data = await websocket.receive_json()
            
            # Guardar en base de datos
            mensaje = MensajeChat(
                estudiante_id=estudiante_id,
                admin_id=data.get('admin_id'),
                remitente=data.get('remitente', user_type),
                mensaje=data.get('mensaje'),
                leido=False,
                tipo=data.get('tipo', 'texto')
            )
            db.add(mensaje)
            db.commit()
            db.refresh(mensaje)
            
            mensaje_data = {
                "id": mensaje.id,
                "estudiante_id": mensaje.estudiante_id,
                "admin_id": mensaje.admin_id,
                "remitente": mensaje.remitente,
                "mensaje": mensaje.mensaje,
                "tipo": mensaje.tipo,
                "created_at": mensaje.created_at.isoformat()
            }
            
            # Enviar a destinatario según remitente
            if mensaje.remitente == 'estudiante':
                # Notificar a admins
                await manager.notify_admin(estudiante_id, mensaje_data)
            else:
                # Enviar a estudiante
                await manager.send_personal_message(
                    mensaje_data,
                    estudiante_id,
                    'estudiante'
                )
                
                # Crear notificación
                from api.notificaciones_routes import crear_notificacion
                crear_notificacion(
                    db=db,
                    estudiante_id=estudiante_id,
                    tipo='mensaje',
                    titulo='💬 Nuevo mensaje del equipo',
                    mensaje=mensaje.mensaje[:100] + ('...' if len(mensaje.mensaje) > 100 else ''),
                    url_accion='/estudiante/dashboard',
                    icono='💬',
                    prioridad='normal'
                )
            
    except WebSocketDisconnect:
        manager.disconnect(estudiante_id, user_type)
    except Exception as e:
        print(f"❌ Error en WebSocket: {e}")
        manager.disconnect(estudiante_id, user_type)

# ============================================
# ADMIN ENDPOINTS
# ============================================

@router.get("/admin/chat/conversaciones")
def listar_conversaciones_activas(
    db: Session = Depends(get_db)
):
    """Listar estudiantes con conversaciones activas"""
    try:
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT mc.estudiante_id, e.nombre, e.email,
                   COUNT(CASE WHEN mc.remitente = 'estudiante' AND mc.leido = false THEN 1 END) as no_leidos,
                   MAX(mc.created_at) as ultimo_mensaje
            FROM mensajes_chat mc
            LEFT JOIN estudiantes e ON e.id = mc.estudiante_id
            GROUP BY mc.estudiante_id, e.nombre, e.email
            ORDER BY ultimo_mensaje DESC
        """)
        
        conversaciones = []
        for row in cursor.fetchall():
            conversaciones.append({
                "estudiante_id": row[0],
                "nombre": row[1] or "N/A",
                "email": row[2] or "N/A",
                "no_leidos": row[3],
                "ultimo_mensaje": row[4].isoformat() if row[4] else None
            })
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "conversaciones": conversaciones,
            "total": len(conversaciones)
        }
    except Exception as e:
        print(f"❌ Error listando conversaciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/chat/total-no-leidos")
def obtener_total_mensajes_no_leidos(
    db: Session = Depends(get_db)
):
    """Obtener el total de mensajes no leídos de todos los estudiantes"""
    try:
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) as total_no_leidos
            FROM mensajes_chat 
            WHERE remitente = 'estudiante' AND leido = false
        """)
        
        result = cursor.fetchone()
        total_no_leidos = result[0] if result else 0
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "total_no_leidos": total_no_leidos
        }
    except Exception as e:
        print(f"❌ Error obteniendo total de mensajes no leídos: {e}")
        raise HTTPException(status_code=500, detail=str(e))
