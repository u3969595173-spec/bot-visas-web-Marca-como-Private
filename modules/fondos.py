"""
Módulo de gestión de fondos económicos y patrocinadores
Verificación de fondos, cartas de patrocinio, transferencias
"""

from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database.models import get_db
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

Base = declarative_base()


class Patrocinador(Base):
    __tablename__ = 'patrocinadores'
    
    id = Column(Integer, primary_key=True)
    
    # Datos personales
    nombre_completo = Column(String(300), nullable=False)
    numero_identificacion = Column(String(100), unique=True)
    nacionalidad = Column(String(100))
    fecha_nacimiento = Column(DateTime)
    
    # Relación con estudiante
    relacion_estudiante = Column(String(100))  # padre, madre, familiar, amigo, empresa, etc.
    pais_residencia = Column(String(100))
    ciudad_residencia = Column(String(100))
    
    # Datos de contacto
    email = Column(String(255))
    telefono = Column(String(50))
    direccion_completa = Column(Text)
    
    # Datos económicos
    ocupacion = Column(String(255))
    empresa = Column(String(255))
    ingresos_mensuales = Column(Float)
    capacidad_patrocinio = Column(Float)  # Monto total que puede patrocinar
    
    # Verificación
    verificado = Column(Boolean, default=False)
    fecha_verificacion = Column(DateTime)
    documentos_verificados = Column(JSON, default=[])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TransferenciaFondos(Base):
    __tablename__ = 'transferencias_fondos'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    patrocinador_id = Column(Integer, ForeignKey('patrocinadores.id'))
    
    tipo_transferencia = Column(String(100))  # bancaria, remesa, efectivo, etc.
    monto = Column(Float, nullable=False)
    moneda = Column(String(10), default='EUR')
    fecha_transferencia = Column(DateTime)
    
    # Detalles
    banco_origen = Column(String(255))
    banco_destino = Column(String(255))
    numero_referencia = Column(String(255))
    concepto = Column(Text)
    
    # Estado
    estado = Column(String(50), default='pendiente')  # pendiente, procesando, completada, fallida
    comprobante_ruta = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class GestorFondos:
    """Gestor principal de fondos económicos"""
    
    @staticmethod
    def verificar_fondos(estudiante_id: int) -> Dict:
        """
        Verifica medios económicos del estudiante
        Evalúa si tiene fondos propios, patrocinador o ambos
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Diccionario con evaluación detallada de fondos
        """
        from modules.estudiantes import GestorEstudiantes
        from modules.cursos import GestorCursos
        
        db = get_db()
        estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=estudiante_id)
        
        if not estudiante:
            return {'error': 'Estudiante no encontrado'}
        
        # Obtener curso asignado para calcular necesidades
        curso = None
        if estudiante.curso_asignado_id:
            curso = GestorCursos.obtener_curso_por_id(estudiante.curso_asignado_id)
        
        # Calcular fondos necesarios
        if curso:
            duracion_meses = curso.duracion_meses or 12
            costo_matricula = curso.precio or 5000
        else:
            duracion_meses = 12
            costo_matricula = 5000
        
        # Cálculo de fondos mínimos requeridos
        MANUTENCIÓN_MENSUAL = 600  # € mínimo por mes
        ALOJAMIENTO_MENSUAL = 500  # € promedio
        SEGURO_ANUAL = 400  # €
        
        fondos_minimos = costo_matricula + (MANUTENCIÓN_MENSUAL * duracion_meses) + \
                        (ALOJAMIENTO_MENSUAL * duracion_meses) + SEGURO_ANUAL
        
        # Evaluar fuentes de fondos
        fondos_disponibles = 0
        fuentes = []
        
        # 1. Fondos propios
        if estudiante.tiene_fondos_propios and estudiante.monto_fondos_disponibles:
            fondos_disponibles += estudiante.monto_fondos_disponibles
            fuentes.append({
                'tipo': 'fondos_propios',
                'monto': estudiante.monto_fondos_disponibles,
                'porcentaje': (estudiante.monto_fondos_disponibles / fondos_minimos * 100)
            })
        
        # 2. Patrocinador
        if estudiante.tiene_patrocinador and estudiante.patrocinador_id:
            patrocinador = db.query(Patrocinador).filter(
                Patrocinador.id == estudiante.patrocinador_id
            ).first()
            
            if patrocinador:
                monto_patrocinio = patrocinador.capacidad_patrocinio or 0
                fondos_disponibles += monto_patrocinio
                fuentes.append({
                    'tipo': 'patrocinador',
                    'nombre': patrocinador.nombre_completo,
                    'relacion': patrocinador.relacion_estudiante,
                    'monto': monto_patrocinio,
                    'verificado': patrocinador.verificado,
                    'porcentaje': (monto_patrocinio / fondos_minimos * 100)
                })
        
        # 3. Transferencias recibidas
        transferencias = db.query(TransferenciaFondos).filter(
            TransferenciaFondos.estudiante_id == estudiante_id,
            TransferenciaFondos.estado == 'completada'
        ).all()
        
        total_transferencias = sum([t.monto for t in transferencias])
        if total_transferencias > 0:
            fuentes.append({
                'tipo': 'transferencias',
                'monto': total_transferencias,
                'numero_transferencias': len(transferencias),
                'porcentaje': (total_transferencias / fondos_minimos * 100)
            })
            fondos_disponibles += total_transferencias
        
        # Evaluación final
        porcentaje_cobertura = (fondos_disponibles / fondos_minimos * 100) if fondos_minimos > 0 else 0
        deficit = max(0, fondos_minimos - fondos_disponibles)
        
        if porcentaje_cobertura >= 120:
            estado = '✅ EXCELENTE'
            color = 'verde'
            mensaje = f'Tienes {fondos_disponibles - fondos_minimos:,.2f}€ extra'
        elif porcentaje_cobertura >= 100:
            estado = '✅ SUFICIENTE'
            color = 'verde'
            mensaje = 'Cumples con los fondos mínimos requeridos'
        elif porcentaje_cobertura >= 80:
            estado = '⚠️ CASI SUFICIENTE'
            color = 'amarillo'
            mensaje = f'Te faltan {deficit:,.2f}€ para el mínimo'
        else:
            estado = '❌ INSUFICIENTE'
            color = 'rojo'
            mensaje = f'Te faltan {deficit:,.2f}€ para el mínimo'
        
        return {
            'fondos_minimos_requeridos': fondos_minimos,
            'fondos_disponibles': fondos_disponibles,
            'porcentaje_cobertura': porcentaje_cobertura,
            'deficit': deficit,
            'estado': estado,
            'color': color,
            'mensaje': mensaje,
            'fuentes': fuentes,
            'desglose': {
                'matricula': costo_matricula,
                'manutencion': MANUTENCIÓN_MENSUAL * duracion_meses,
                'alojamiento': ALOJAMIENTO_MENSUAL * duracion_meses,
                'seguro': SEGURO_ANUAL,
                'duracion_meses': duracion_meses
            },
            'recomendaciones': GestorFondos._generar_recomendaciones_fondos(
                porcentaje_cobertura, deficit, fuentes
            )
        }
    
    @staticmethod
    def _generar_recomendaciones_fondos(porcentaje: float, deficit: float, fuentes: List[Dict]) -> List[str]:
        """Genera recomendaciones para mejorar situación financiera"""
        recomendaciones = []
        
        if porcentaje < 100:
            if not any(f['tipo'] == 'patrocinador' for f in fuentes):
                recomendaciones.append('💡 Considera buscar un patrocinador (familiar en España o Cuba)')
            
            recomendaciones.append(f'💡 Necesitas demostrar {deficit:,.2f}€ adicionales')
            recomendaciones.append('💡 Opciones: Ahorros, préstamo estudiantil, beca parcial')
        
        if any(f['tipo'] == 'patrocinador' and not f.get('verificado') for f in fuentes):
            recomendaciones.append('⚠️ Completa verificación de documentos del patrocinador')
        
        if porcentaje >= 100 and porcentaje < 110:
            recomendaciones.append('💡 Tener 10-20% extra aumenta probabilidad de aprobación')
        
        return recomendaciones
    
    @staticmethod
    def registrar_patrocinador(datos_patrocinador: Dict, estudiante_id: int = None) -> Patrocinador:
        """
        Registra un nuevo patrocinador
        
        Args:
            datos_patrocinador: Diccionario con información del patrocinador
            estudiante_id: ID del estudiante que será patrocinado
            
        Returns:
            Objeto Patrocinador creado
        """
        db = get_db()
        
        patrocinador = Patrocinador(**datos_patrocinador)
        db.add(patrocinador)
        db.commit()
        db.refresh(patrocinador)
        
        # Asociar con estudiante si se proporciona
        if estudiante_id:
            from modules.estudiantes import GestorEstudiantes
            estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=estudiante_id)
            if estudiante:
                estudiante.patrocinador_id = patrocinador.id
                estudiante.tiene_patrocinador = True
                db.commit()
        
        return patrocinador
    
    @staticmethod
    def generar_carta_patrocinio(patrocinador_id: int, estudiante_id: int, idioma: str = 'es') -> bytes:
        """
        Genera carta de patrocinio en PDF lista para presentar en consulado
        
        Args:
            patrocinador_id: ID del patrocinador
            estudiante_id: ID del estudiante
            idioma: 'es' para español, 'en' para inglés
            
        Returns:
            Bytes del PDF generado
        """
        from modules.estudiantes import GestorEstudiantes
        from modules.cursos import GestorCursos
        
        db = get_db()
        patrocinador = db.query(Patrocinador).filter(Patrocinador.id == patrocinador_id).first()
        estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=estudiante_id)
        
        if not patrocinador or not estudiante:
            raise ValueError("Patrocinador o estudiante no encontrado")
        
        # Obtener curso
        curso = None
        if estudiante.curso_asignado_id:
            curso = GestorCursos.obtener_curso_por_id(estudiante.curso_asignado_id)
        
        # Crear PDF
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Configuración
        fecha_actual = datetime.now().strftime('%d de %B de %Y')
        
        # Título
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height - 80, "CARTA DE PATROCINIO / SPONSORSHIP LETTER")
        
        # Fecha y lugar
        c.setFont("Helvetica", 11)
        y_position = height - 120
        c.drawString(70, y_position, f"Fecha: {fecha_actual}")
        c.drawString(70, y_position - 20, f"Lugar: {patrocinador.ciudad_residencia}, {patrocinador.pais_residencia}")
        
        # Destinatario
        y_position -= 60
        c.setFont("Helvetica-Bold", 11)
        c.drawString(70, y_position, "A QUIEN CORRESPONDA:")
        c.drawString(70, y_position - 15, "Consulado de España")
        
        # Cuerpo de la carta
        y_position -= 50
        c.setFont("Helvetica", 11)
        
        texto_lineas = [
            f"Por medio de la presente, yo, {patrocinador.nombre_completo}, con documento de identidad",
            f"número {patrocinador.numero_identificacion}, nacionalidad {patrocinador.nacionalidad}, y residente en",
            f"{patrocinador.direccion_completa}, declaro bajo juramento que:",
            "",
            f"1. Asumo la responsabilidad financiera COMPLETA de {estudiante.nombre_completo},",
            f"   con pasaporte número {estudiante.numero_pasaporte}, para cubrir todos los gastos",
            f"   relacionados con sus estudios en España.",
            "",
            f"2. Mi relación con el estudiante es: {patrocinador.relacion_estudiante}.",
            "",
            f"3. Me comprometo a cubrir los siguientes gastos:",
        ]
        
        if curso:
            texto_lineas.extend([
                f"   - Matrícula del curso: {curso.precio:,.2f}€",
                f"   - Manutención mensual: 600€ x {curso.duracion_meses} meses = {600 * curso.duracion_meses:,.2f}€",
                f"   - Alojamiento mensual: 500€ x {curso.duracion_meses} meses = {500 * curso.duracion_meses:,.2f}€",
                f"   - Seguro médico: 400€",
                f"   - Otros gastos: 1,000€",
            ])
        else:
            texto_lineas.extend([
                f"   - Matrícula, manutención, alojamiento, seguro médico y otros gastos necesarios",
                f"   - Monto total estimado: {patrocinador.capacidad_patrocinio:,.2f}€",
            ])
        
        texto_lineas.extend([
            "",
            f"4. Mis ingresos mensuales son de {patrocinador.ingresos_mensuales:,.2f}€ y trabajo como",
            f"   {patrocinador.ocupacion} en {patrocinador.empresa or 'cuenta propia'}.",
            "",
            "5. Adjunto los siguientes documentos como respaldo:",
            "   - Extractos bancarios de los últimos 6 meses",
            "   - Certificado de ingresos",
            "   - Documento de identidad",
            "   - Prueba de relación con el estudiante",
            "",
            "Firmo la presente carta asumiendo plena responsabilidad legal y financiera.",
            "",
            "Atentamente,",
        ])
        
        # Escribir líneas
        line_height = 15
        for linea in texto_lineas:
            if y_position < 100:  # Nueva página si es necesario
                c.showPage()
                y_position = height - 80
                c.setFont("Helvetica", 11)
            
            c.drawString(70, y_position, linea)
            y_position -= line_height
        
        # Firma
        y_position -= 40
        c.drawString(70, y_position, "_" * 40)
        c.drawString(70, y_position - 20, patrocinador.nombre_completo)
        c.drawString(70, y_position - 35, f"ID: {patrocinador.numero_identificacion}")
        c.drawString(70, y_position - 50, f"Email: {patrocinador.email}")
        c.drawString(70, y_position - 65, f"Teléfono: {patrocinador.telefono}")
        
        # Nota al pie
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(70, 50, "NOTA: Esta carta debe ser acompañada de documentación financiera de respaldo.")
        c.drawString(70, 35, "Generado automáticamente por Sistema de Gestión de Visas Estudiantiles")
        
        c.save()
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    @staticmethod
    def registrar_transferencia(
        estudiante_id: int,
        monto: float,
        patrocinador_id: int = None,
        tipo: str = 'bancaria',
        detalles: Dict = None
    ) -> TransferenciaFondos:
        """
        Registra una transferencia de fondos
        
        Args:
            estudiante_id: ID del estudiante receptor
            monto: Cantidad transferida
            patrocinador_id: ID del patrocinador que envía (opcional)
            tipo: Tipo de transferencia (bancaria, remesa, efectivo)
            detalles: Diccionario con detalles adicionales
            
        Returns:
            Objeto TransferenciaFondos creado
        """
        db = get_db()
        
        transferencia = TransferenciaFondos(
            estudiante_id=estudiante_id,
            patrocinador_id=patrocinador_id,
            tipo_transferencia=tipo,
            monto=monto,
            fecha_transferencia=datetime.utcnow()
        )
        
        if detalles:
            for key, value in detalles.items():
                if hasattr(transferencia, key):
                    setattr(transferencia, key, value)
        
        db.add(transferencia)
        db.commit()
        db.refresh(transferencia)
        
        return transferencia
    
    @staticmethod
    def actualizar_estado_transferencia(transferencia_id: int, nuevo_estado: str) -> bool:
        """Actualiza el estado de una transferencia"""
        db = get_db()
        transferencia = db.query(TransferenciaFondos).filter(
            TransferenciaFondos.id == transferencia_id
        ).first()
        
        if transferencia:
            transferencia.estado = nuevo_estado
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def obtener_historial_transferencias(estudiante_id: int) -> List[TransferenciaFondos]:
        """Obtiene historial de transferencias de un estudiante"""
        db = get_db()
        return db.query(TransferenciaFondos).filter(
            TransferenciaFondos.estudiante_id == estudiante_id
        ).order_by(TransferenciaFondos.fecha_transferencia.desc()).all()
    
    @staticmethod
    def verificar_patrocinador(patrocinador_id: int, documentos_verificados: List[str]) -> bool:
        """
        Marca un patrocinador como verificado
        
        Args:
            patrocinador_id: ID del patrocinador
            documentos_verificados: Lista de documentos que se verificaron
            
        Returns:
            True si se verificó exitosamente
        """
        db = get_db()
        patrocinador = db.query(Patrocinador).filter(Patrocinador.id == patrocinador_id).first()
        
        if patrocinador:
            patrocinador.verificado = True
            patrocinador.fecha_verificacion = datetime.utcnow()
            patrocinador.documentos_verificados = documentos_verificados
            db.commit()
            return True
        
        return False
