"""
Sistema de Comentarios Internos entre Admins
Notas compartidas sobre estudiantes para coordinación del equipo
"""

from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database.models import get_db

Base = declarative_base()


class ComentarioInterno(Base):
    __tablename__ = 'comentarios_internos'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'), nullable=False)
    
    # Admin que crea el comentario
    admin_id = Column(Integer, nullable=False)
    admin_nombre = Column(String(255))
    
    # Contenido
    comentario = Column(Text, nullable=False)
    tipo = Column(String(50))  # 'nota', 'pregunta', 'alerta', 'recomendacion'
    prioridad = Column(String(20), default='normal')  # 'baja', 'normal', 'alta', 'urgente'
    
    # Respuestas
    respuesta_a_comentario_id = Column(Integer, ForeignKey('comentarios_internos.id'))  # Para hilos de conversación
    
    # Estado
    resuelto = Column(Boolean, default=False)
    resuelto_por_admin_id = Column(Integer)
    fecha_resolucion = Column(DateTime)
    
    # Visibilidad
    privado = Column(Boolean, default=False)  # Si es privado, solo lo ve el admin que lo creó
    mencionados = Column(String(500))  # IDs de admins mencionados: "1,5,8"
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SistemaComentarios:
    """Sistema de comunicación interna entre admins"""
    
    @staticmethod
    def crear_comentario(
        estudiante_id: int,
        admin_id: int,
        admin_nombre: str,
        comentario: str,
        tipo: str = 'nota',
        prioridad: str = 'normal',
        respuesta_a: int = None,
        privado: bool = False,
        mencionar_admins: List[int] = None
    ) -> ComentarioInterno:
        """
        Crea un nuevo comentario interno sobre un estudiante
        
        Args:
            estudiante_id: ID del estudiante
            admin_id: ID del admin que comenta
            admin_nombre: Nombre del admin
            comentario: Contenido del comentario
            tipo: Tipo (nota, pregunta, alerta, recomendacion)
            prioridad: Prioridad (baja, normal, alta, urgente)
            respuesta_a: ID del comentario al que responde (opcional)
            privado: Si es visible solo para el creador
            mencionar_admins: Lista de IDs de admins a mencionar
            
        Returns:
            ComentarioInterno creado
        """
        db = get_db()
        
        try:
            # Convertir lista de admins mencionados a string
            mencionados_str = ','.join(map(str, mencionar_admins)) if mencionar_admins else None
            
            comentario_obj = ComentarioInterno(
                estudiante_id=estudiante_id,
                admin_id=admin_id,
                admin_nombre=admin_nombre,
                comentario=comentario,
                tipo=tipo,
                prioridad=prioridad,
                respuesta_a_comentario_id=respuesta_a,
                privado=privado,
                mencionados=mencionados_str,
                resuelto=False
            )
            
            db.add(comentario_obj)
            db.commit()
            db.refresh(comentario_obj)
            
            # Si menciona admins, crear notificaciones
            if mencionar_admins:
                SistemaComentarios._notificar_admins_mencionados(
                    estudiante_id, 
                    admin_nombre, 
                    comentario, 
                    mencionar_admins
                )
            
            print(f"✅ Comentario creado por {admin_nombre}")
            return comentario_obj
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def responder_comentario(
        comentario_id: int,
        admin_id: int,
        admin_nombre: str,
        respuesta: str
    ) -> ComentarioInterno:
        """
        Responde a un comentario existente
        
        Args:
            comentario_id: ID del comentario original
            admin_id: ID del admin que responde
            admin_nombre: Nombre del admin
            respuesta: Contenido de la respuesta
            
        Returns:
            ComentarioInterno (respuesta) creado
        """
        db = get_db()
        
        try:
            # Obtener comentario original
            comentario_original = db.query(ComentarioInterno).filter(
                ComentarioInterno.id == comentario_id
            ).first()
            
            if not comentario_original:
                raise ValueError("Comentario original no encontrado")
            
            # Crear respuesta
            respuesta_obj = SistemaComentarios.crear_comentario(
                estudiante_id=comentario_original.estudiante_id,
                admin_id=admin_id,
                admin_nombre=admin_nombre,
                comentario=respuesta,
                tipo='nota',
                respuesta_a=comentario_id,
                mencionar_admins=[comentario_original.admin_id]  # Mencionar al autor original
            )
            
            return respuesta_obj
            
        finally:
            db.close()
    
    @staticmethod
    def marcar_resuelto(
        comentario_id: int,
        admin_id: int
    ) -> bool:
        """
        Marca un comentario como resuelto
        
        Args:
            comentario_id: ID del comentario
            admin_id: ID del admin que resuelve
            
        Returns:
            True si se marcó exitosamente
        """
        db = get_db()
        
        try:
            comentario = db.query(ComentarioInterno).filter(
                ComentarioInterno.id == comentario_id
            ).first()
            
            if not comentario:
                return False
            
            comentario.resuelto = True
            comentario.resuelto_por_admin_id = admin_id
            comentario.fecha_resolucion = datetime.utcnow()
            
            db.commit()
            
            print(f"✅ Comentario #{comentario_id} marcado como resuelto")
            return True
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def obtener_comentarios_estudiante(
        estudiante_id: int,
        admin_id: int = None,
        incluir_resueltos: bool = True
    ) -> List[ComentarioInterno]:
        """
        Obtiene todos los comentarios de un estudiante
        
        Args:
            estudiante_id: ID del estudiante
            admin_id: ID del admin (para filtrar privados)
            incluir_resueltos: Si incluir comentarios resueltos
            
        Returns:
            Lista de comentarios
        """
        db = get_db()
        
        try:
            query = db.query(ComentarioInterno).filter(
                ComentarioInterno.estudiante_id == estudiante_id
            )
            
            # Filtrar privados
            if admin_id:
                query = query.filter(
                    (ComentarioInterno.privado == False) |
                    (ComentarioInterno.admin_id == admin_id)
                )
            else:
                query = query.filter(ComentarioInterno.privado == False)
            
            # Filtrar resueltos
            if not incluir_resueltos:
                query = query.filter(ComentarioInterno.resuelto == False)
            
            comentarios = query.order_by(ComentarioInterno.created_at.desc()).all()
            
            return comentarios
            
        finally:
            db.close()
    
    @staticmethod
    def obtener_mis_menciones(
        admin_id: int,
        solo_no_resueltos: bool = True
    ) -> List[ComentarioInterno]:
        """
        Obtiene comentarios donde el admin fue mencionado
        
        Args:
            admin_id: ID del admin
            solo_no_resueltos: Solo comentarios no resueltos
            
        Returns:
            Lista de comentarios
        """
        db = get_db()
        
        try:
            query = db.query(ComentarioInterno).filter(
                ComentarioInterno.mencionados.like(f'%{admin_id}%')
            )
            
            if solo_no_resueltos:
                query = query.filter(ComentarioInterno.resuelto == False)
            
            menciones = query.order_by(ComentarioInterno.prioridad.desc(), ComentarioInterno.created_at.desc()).all()
            
            return menciones
            
        finally:
            db.close()
    
    @staticmethod
    def obtener_preguntas_sin_responder() -> List[ComentarioInterno]:
        """
        Obtiene todas las preguntas que no han sido respondidas
        
        Returns:
            Lista de preguntas sin responder
        """
        db = get_db()
        
        try:
            # Preguntas que no están resueltas y no tienen respuestas
            preguntas = db.query(ComentarioInterno).filter(
                ComentarioInterno.tipo == 'pregunta',
                ComentarioInterno.resuelto == False
            ).order_by(ComentarioInterno.prioridad.desc(), ComentarioInterno.created_at).all()
            
            # Filtrar las que no tienen respuestas
            sin_responder = []
            for pregunta in preguntas:
                respuestas = db.query(ComentarioInterno).filter(
                    ComentarioInterno.respuesta_a_comentario_id == pregunta.id
                ).count()
                
                if respuestas == 0:
                    sin_responder.append(pregunta)
            
            return sin_responder
            
        finally:
            db.close()
    
    @staticmethod
    def _notificar_admins_mencionados(
        estudiante_id: int,
        autor: str,
        comentario: str,
        admins_ids: List[int]
    ):
        """Notifica a admins mencionados (implementar con sistema de notificaciones)"""
        from modules.notificaciones import SistemaNotificaciones
        
        mensaje = f"""
💬 **MENCIÓN EN COMENTARIO**

{autor} te mencionó en un comentario sobre estudiante #{estudiante_id}:

"{comentario[:200]}{'...' if len(comentario) > 200 else ''}"

Revisa el panel para ver el comentario completo.
"""
        
        # Enviar notificación a cada admin mencionado
        for admin_id in admins_ids:
            try:
                SistemaNotificaciones._enviar_telegram(admin_id, "💬 Nueva mención", mensaje)
            except:
                pass
    
    @staticmethod
    def generar_hilo_conversacion(comentario_id: int) -> str:
        """
        Genera una vista de hilo de conversación
        
        Args:
            comentario_id: ID del comentario raíz
            
        Returns:
            String con el hilo formateado
        """
        db = get_db()
        
        try:
            # Obtener comentario raíz
            raiz = db.query(ComentarioInterno).filter(
                ComentarioInterno.id == comentario_id
            ).first()
            
            if not raiz:
                return "Comentario no encontrado"
            
            # Obtener todas las respuestas
            respuestas = db.query(ComentarioInterno).filter(
                ComentarioInterno.respuesta_a_comentario_id == comentario_id
            ).order_by(ComentarioInterno.created_at).all()
            
            # Formatear hilo
            hilo = f"""
╔══════════════════════════════════════════════════════════════╗
║                    HILO DE CONVERSACIÓN                      ║
╚══════════════════════════════════════════════════════════════╝

📌 {raiz.admin_nombre} - {raiz.created_at.strftime('%d/%m/%Y %H:%M')}
   [{raiz.tipo.upper()}] [Prioridad: {raiz.prioridad.upper()}]
   
   {raiz.comentario}
   
   {'✅ RESUELTO' if raiz.resuelto else '⏳ PENDIENTE'}

"""
            
            if respuestas:
                hilo += "RESPUESTAS:\n" + "="*60 + "\n\n"
                
                for i, resp in enumerate(respuestas, 1):
                    hilo += f"""
  {i}. {resp.admin_nombre} - {resp.created_at.strftime('%d/%m/%Y %H:%M')}
     
     {resp.comentario}
     
"""
            else:
                hilo += "Sin respuestas aún.\n"
            
            return hilo
            
        finally:
            db.close()
    
    @staticmethod
    def estadisticas_comentarios() -> Dict:
        """
        Genera estadísticas de comentarios internos
        
        Returns:
            Dict con estadísticas
        """
        db = get_db()
        
        try:
            total = db.query(ComentarioInterno).count()
            resueltos = db.query(ComentarioInterno).filter(ComentarioInterno.resuelto == True).count()
            pendientes = total - resueltos
            
            preguntas = db.query(ComentarioInterno).filter(ComentarioInterno.tipo == 'pregunta').count()
            alertas = db.query(ComentarioInterno).filter(ComentarioInterno.tipo == 'alerta').count()
            notas = db.query(ComentarioInterno).filter(ComentarioInterno.tipo == 'nota').count()
            
            urgentes = db.query(ComentarioInterno).filter(
                ComentarioInterno.prioridad == 'urgente',
                ComentarioInterno.resuelto == False
            ).count()
            
            return {
                'total_comentarios': total,
                'resueltos': resueltos,
                'pendientes': pendientes,
                'preguntas': preguntas,
                'alertas': alertas,
                'notas': notas,
                'urgentes_sin_resolver': urgentes
            }
            
        finally:
            db.close()
