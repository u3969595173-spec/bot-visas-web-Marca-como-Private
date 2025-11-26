"""
Sistema de Plantillas de Mensaje Personalizables
Admin puede crear, editar y usar plantillas según tipo de estudiante
"""

from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from database.models import get_db

Base = declarative_base()


class PlantillaMensaje(Base):
    __tablename__ = 'plantillas_mensaje'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    
    # Tipo de plantilla
    tipo = Column(String(50))  # 'general', 'especialidad', 'pais', 'fondos'
    
    # Filtros para auto-selección
    especialidad = Column(String(255))  # Para qué especialidad aplica
    pais = Column(String(100))  # Para qué país aplica
    nivel_fondos = Column(String(50))  # 'suficientes', 'insuficientes', 'parciales'
    
    # Contenido de la plantilla
    asunto = Column(String(500))
    contenido = Column(Text, nullable=False)
    
    # Variables disponibles en la plantilla
    variables_disponibles = Column(JSON)  # {nombre}, {especialidad}, {curso}, etc.
    
    # Metadata
    creado_por_admin_id = Column(Integer)
    activa = Column(Boolean, default=True)
    predeterminada = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GestorPlantillas:
    """Gestor de plantillas de mensaje"""
    
    @staticmethod
    def crear_plantilla(
        nombre: str,
        contenido: str,
        admin_id: int,
        asunto: str = None,
        descripcion: str = None,
        tipo: str = 'general',
        especialidad: str = None,
        pais: str = None,
        nivel_fondos: str = None,
        predeterminada: bool = False
    ) -> PlantillaMensaje:
        """
        Crear nueva plantilla de mensaje
        
        Args:
            nombre: Nombre identificador de la plantilla
            contenido: Contenido del mensaje con variables {nombre}, {curso}, etc.
            admin_id: ID del admin que crea la plantilla
            asunto: Asunto del mensaje (opcional)
            descripcion: Descripción de cuándo usar esta plantilla
            tipo: Tipo de plantilla (general, especialidad, pais, fondos)
            especialidad: Especialidad específica (opcional)
            pais: País específico (opcional)
            nivel_fondos: Nivel de fondos (suficientes, insuficientes, parciales)
            predeterminada: Si es la plantilla por defecto
            
        Returns:
            PlantillaMensaje creada
        """
        db = get_db()
        
        try:
            # Variables disponibles para reemplazo
            variables = [
                '{nombre}', '{nombre_completo}', '{especialidad}', '{curso}', 
                '{escuela}', '{ciudad}', '{precio}', '{duracion}', '{fecha_inicio}',
                '{fondos_disponibles}', '{fondos_requeridos}', '{porcentaje_fondos}',
                '{documentos_completos}', '{documentos_pendientes}', '{alojamiento}',
                '{fecha_cita}', '{probabilidad_exito}', '{nivel_espanol}'
            ]
            
            plantilla = PlantillaMensaje(
                nombre=nombre,
                descripcion=descripcion,
                tipo=tipo,
                especialidad=especialidad,
                pais=pais,
                nivel_fondos=nivel_fondos,
                asunto=asunto or f"Tu plan de estudios en España - {nombre}",
                contenido=contenido,
                variables_disponibles=variables,
                creado_por_admin_id=admin_id,
                predeterminada=predeterminada,
                activa=True
            )
            
            # Si es predeterminada, desactivar otras predeterminadas del mismo tipo
            if predeterminada:
                db.query(PlantillaMensaje).filter(
                    PlantillaMensaje.tipo == tipo,
                    PlantillaMensaje.predeterminada == True
                ).update({'predeterminada': False})
            
            db.add(plantilla)
            db.commit()
            db.refresh(plantilla)
            
            print(f"✅ Plantilla '{nombre}' creada exitosamente")
            return plantilla
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def obtener_plantilla_sugerida(
        especialidad: str = None,
        pais: str = None,
        fondos_suficientes: bool = True
    ) -> Optional[PlantillaMensaje]:
        """
        Obtiene la plantilla más adecuada según el perfil del estudiante
        
        Args:
            especialidad: Especialidad del estudiante
            pais: País de origen
            fondos_suficientes: Si tiene fondos suficientes
            
        Returns:
            PlantillaMensaje más adecuada o None
        """
        db = get_db()
        
        try:
            nivel_fondos = 'suficientes' if fondos_suficientes else 'insuficientes'
            
            # Buscar plantilla específica por especialidad
            if especialidad:
                plantilla = db.query(PlantillaMensaje).filter(
                    PlantillaMensaje.especialidad.ilike(f"%{especialidad}%"),
                    PlantillaMensaje.activa == True
                ).first()
                
                if plantilla:
                    return plantilla
            
            # Buscar por país
            if pais:
                plantilla = db.query(PlantillaMensaje).filter(
                    PlantillaMensaje.pais.ilike(f"%{pais}%"),
                    PlantillaMensaje.activa == True
                ).first()
                
                if plantilla:
                    return plantilla
            
            # Buscar por nivel de fondos
            plantilla = db.query(PlantillaMensaje).filter(
                PlantillaMensaje.nivel_fondos == nivel_fondos,
                PlantillaMensaje.activa == True
            ).first()
            
            if plantilla:
                return plantilla
            
            # Plantilla predeterminada general
            plantilla = db.query(PlantillaMensaje).filter(
                PlantillaMensaje.tipo == 'general',
                PlantillaMensaje.predeterminada == True,
                PlantillaMensaje.activa == True
            ).first()
            
            return plantilla
            
        except Exception as e:
            print(f"Error obteniendo plantilla sugerida: {e}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def renderizar_plantilla(
        plantilla_id: int,
        datos_estudiante: Dict
    ) -> Dict[str, str]:
        """
        Renderiza una plantilla reemplazando variables con datos reales
        
        Args:
            plantilla_id: ID de la plantilla
            datos_estudiante: Diccionario con datos del estudiante
            
        Returns:
            Dict con 'asunto' y 'contenido' renderizados
        """
        db = get_db()
        
        try:
            plantilla = db.query(PlantillaMensaje).filter(
                PlantillaMensaje.id == plantilla_id
            ).first()
            
            if not plantilla:
                raise ValueError("Plantilla no encontrada")
            
            # Reemplazar variables en asunto y contenido
            asunto = plantilla.asunto
            contenido = plantilla.contenido
            
            # Mapeo de variables a datos
            reemplazos = {
                '{nombre}': datos_estudiante.get('nombre', ''),
                '{nombre_completo}': datos_estudiante.get('nombre_completo', ''),
                '{especialidad}': datos_estudiante.get('especialidad_interes', ''),
                '{curso}': datos_estudiante.get('curso_nombre', ''),
                '{escuela}': datos_estudiante.get('escuela', ''),
                '{ciudad}': datos_estudiante.get('ciudad', ''),
                '{precio}': str(datos_estudiante.get('precio', 0)),
                '{duracion}': str(datos_estudiante.get('duracion_meses', 0)),
                '{fecha_inicio}': datos_estudiante.get('fecha_inicio', ''),
                '{fondos_disponibles}': f"{datos_estudiante.get('fondos_disponibles', 0):,.2f}",
                '{fondos_requeridos}': f"{datos_estudiante.get('fondos_requeridos', 0):,.2f}",
                '{porcentaje_fondos}': f"{datos_estudiante.get('porcentaje_fondos', 0):.0f}",
                '{documentos_completos}': str(datos_estudiante.get('documentos_completos', 0)),
                '{documentos_pendientes}': str(datos_estudiante.get('documentos_pendientes', 0)),
                '{alojamiento}': datos_estudiante.get('alojamiento', ''),
                '{fecha_cita}': datos_estudiante.get('fecha_cita', ''),
                '{probabilidad_exito}': f"{datos_estudiante.get('probabilidad_exito', 0):.0f}",
                '{nivel_espanol}': datos_estudiante.get('nivel_espanol', '')
            }
            
            # Realizar reemplazos
            for variable, valor in reemplazos.items():
                asunto = asunto.replace(variable, str(valor))
                contenido = contenido.replace(variable, str(valor))
            
            return {
                'asunto': asunto,
                'contenido': contenido,
                'plantilla_usada': plantilla.nombre
            }
            
        except Exception as e:
            raise e
        finally:
            db.close()
    
    @staticmethod
    def listar_plantillas(
        tipo: str = None,
        activas_solo: bool = True
    ) -> List[PlantillaMensaje]:
        """
        Lista todas las plantillas disponibles
        
        Args:
            tipo: Filtrar por tipo (opcional)
            activas_solo: Solo mostrar plantillas activas
            
        Returns:
            Lista de plantillas
        """
        db = get_db()
        
        try:
            query = db.query(PlantillaMensaje)
            
            if tipo:
                query = query.filter(PlantillaMensaje.tipo == tipo)
            
            if activas_solo:
                query = query.filter(PlantillaMensaje.activa == True)
            
            plantillas = query.order_by(PlantillaMensaje.predeterminada.desc(), PlantillaMensaje.nombre).all()
            
            return plantillas
            
        finally:
            db.close()
    
    @staticmethod
    def editar_plantilla(
        plantilla_id: int,
        nombre: str = None,
        contenido: str = None,
        asunto: str = None,
        descripcion: str = None,
        activa: bool = None,
        predeterminada: bool = None
    ) -> PlantillaMensaje:
        """
        Edita una plantilla existente
        
        Args:
            plantilla_id: ID de la plantilla a editar
            nombre, contenido, asunto, etc.: Campos a actualizar
            
        Returns:
            PlantillaMensaje actualizada
        """
        db = get_db()
        
        try:
            plantilla = db.query(PlantillaMensaje).filter(
                PlantillaMensaje.id == plantilla_id
            ).first()
            
            if not plantilla:
                raise ValueError("Plantilla no encontrada")
            
            # Actualizar campos proporcionados
            if nombre is not None:
                plantilla.nombre = nombre
            if contenido is not None:
                plantilla.contenido = contenido
            if asunto is not None:
                plantilla.asunto = asunto
            if descripcion is not None:
                plantilla.descripcion = descripcion
            if activa is not None:
                plantilla.activa = activa
            if predeterminada is not None:
                if predeterminada:
                    # Desactivar otras predeterminadas del mismo tipo
                    db.query(PlantillaMensaje).filter(
                        PlantillaMensaje.tipo == plantilla.tipo,
                        PlantillaMensaje.id != plantilla_id,
                        PlantillaMensaje.predeterminada == True
                    ).update({'predeterminada': False})
                
                plantilla.predeterminada = predeterminada
            
            plantilla.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(plantilla)
            
            print(f"✅ Plantilla '{plantilla.nombre}' actualizada")
            return plantilla
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def eliminar_plantilla(plantilla_id: int) -> bool:
        """
        Elimina (desactiva) una plantilla
        
        Args:
            plantilla_id: ID de la plantilla
            
        Returns:
            True si se eliminó correctamente
        """
        db = get_db()
        
        try:
            plantilla = db.query(PlantillaMensaje).filter(
                PlantillaMensaje.id == plantilla_id
            ).first()
            
            if not plantilla:
                return False
            
            plantilla.activa = False
            db.commit()
            
            print(f"✅ Plantilla '{plantilla.nombre}' desactivada")
            return True
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()


def inicializar_plantillas_predeterminadas():
    """Crea plantillas predeterminadas al iniciar el sistema"""
    
    # Plantilla general
    GestorPlantillas.crear_plantilla(
        nombre="General - Estudiante Cubano",
        contenido="""¡Hola {nombre_completo}! 👋

Hemos procesado tu solicitud y tenemos excelentes noticias para ti.

📚 **CURSO SELECCIONADO:**
• Nombre: {curso}
• Escuela: {escuela}
• Ciudad: {ciudad}
• Duración: {duracion} meses
• Precio: {precio}€
• Inicio: {fecha_inicio}

💰 **SITUACIÓN ECONÓMICA:**
• Fondos disponibles: {fondos_disponibles}€
• Fondos requeridos: {fondos_requeridos}€
• Cobertura: {porcentaje_fondos}%

📄 **DOCUMENTOS:**
• Completados: {documentos_completos}
• Pendientes: {documentos_pendientes}

🏠 **ALOJAMIENTO:**
{alojamiento}

📊 **Probabilidad de aprobación:** {probabilidad_exito}%

📞 **PRÓXIMOS PASOS:**
1. Revisa toda la información
2. Confirma tu interés en el curso
3. Prepara los documentos pendientes
4. Nuestro equipo te guiará en el proceso

¿Tienes preguntas? ¡Estamos aquí para ayudarte! 🇪🇸

Saludos,
Equipo Agencia Educativa""",
        admin_id=0,
        tipo='general',
        pais='Cuba',
        predeterminada=True,
        descripcion="Plantilla general para estudiantes cubanos"
    )
    
    # Plantilla para fondos insuficientes
    GestorPlantillas.crear_plantilla(
        nombre="Fondos Insuficientes",
        contenido="""Hola {nombre_completo},

Hemos revisado tu solicitud para {curso} en {ciudad}.

💰 **SITUACIÓN ECONÓMICA:**
Fondos actuales: {fondos_disponibles}€
Fondos necesarios: {fondos_requeridos}€
⚠️ Déficit: Requieres fondos adicionales

**OPCIONES DISPONIBLES:**

1️⃣ **Patrocinador:**
   Podemos ayudarte a gestionar un patrocinador (familiar en España o Cuba)
   Generamos la carta de patrocinio automáticamente

2️⃣ **Plan de Pago:**
   Algunos cursos aceptan pagos mensuales
   Te ayudamos a negociar con la escuela

3️⃣ **Becas Disponibles:**
   Tenemos {especialidad} con becas parciales
   Hasta 30% de descuento

4️⃣ **Préstamo Estudiantil:**
   Te conectamos con instituciones financieras

📞 **Nuestro equipo te contactará en 24 horas** para discutir la mejor opción.

No te preocupes, ¡encontraremos la solución! 💪

Saludos,
Equipo Agencia Educativa""",
        admin_id=0,
        tipo='fondos',
        nivel_fondos='insuficientes',
        predeterminada=True,
        descripcion="Para estudiantes con fondos insuficientes"
    )
    
    print("✅ Plantillas predeterminadas inicializadas")
