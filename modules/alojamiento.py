"""
Módulo de gestión de alojamiento
Registro de pisos, asignación de habitaciones, alertas de alquiler
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database.models import get_db

Base = declarative_base()


class Alojamiento(Base):
    __tablename__ = 'alojamientos'
    
    id = Column(Integer, primary_key=True)
    
    # Información del inmueble
    tipo = Column(String(100))  # piso_completo, habitacion_individual, habitacion_compartida, residencia
    direccion = Column(Text, nullable=False)
    ciudad = Column(String(100), nullable=False)
    codigo_postal = Column(String(20))
    barrio = Column(String(100))
    
    # Características
    num_habitaciones = Column(Integer)
    num_banos = Column(Integer)
    metros_cuadrados = Column(Float)
    amueblado = Column(Boolean, default=True)
    wifi = Column(Boolean, default=True)
    cocina = Column(Boolean, default=True)
    lavadora = Column(Boolean, default=False)
    calefaccion = Column(Boolean, default=True)
    aire_acondicionado = Column(Boolean, default=False)
    
    # Ubicación y transporte
    distancia_universidad_km = Column(Float)
    metro_cercano = Column(String(100))
    distancia_metro_minutos = Column(Integer)
    
    # Económico
    precio_mensual = Column(Float, nullable=False)
    gastos_incluidos = Column(Boolean, default=False)
    gastos_adicionales = Column(Float, default=0)
    deposito_requerido = Column(Float)  # Fianza
    
    # Disponibilidad
    disponible = Column(Boolean, default=True)
    fecha_disponible_desde = Column(DateTime)
    fecha_disponible_hasta = Column(DateTime)
    capacidad_maxima = Column(Integer, default=1)
    ocupados_actual = Column(Integer, default=0)
    
    # Información del propietario
    propietario_nombre = Column(String(255))
    propietario_telefono = Column(String(50))
    propietario_email = Column(String(255))
    
    # Adicional
    descripcion = Column(Text)
    reglas = Column(Text)
    fotos_urls = Column(JSON, default=[])
    
    # Estado
    verificado = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AsignacionAlojamiento(Base):
    __tablename__ = 'asignaciones_alojamiento'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'), nullable=False)
    alojamiento_id = Column(Integer, ForeignKey('alojamientos.id'), nullable=False)
    
    # Fechas del contrato
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime)
    duracion_meses = Column(Integer)
    
    # Económico
    precio_acordado = Column(Float)
    deposito_pagado = Column(Float)
    gastos_mensuales = Column(Float)
    
    # Estado
    estado = Column(String(50), default='pendiente')  # pendiente, activo, finalizado, cancelado
    contrato_firmado = Column(Boolean, default=False)
    fecha_firma_contrato = Column(DateTime)
    ruta_contrato = Column(Text)
    
    # Pagos
    dia_pago_mensual = Column(Integer, default=1)  # Día del mes para pagar
    ultimo_pago_fecha = Column(DateTime)
    proximo_pago_fecha = Column(DateTime)
    
    # Notas
    notas = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PagoAlquiler(Base):
    __tablename__ = 'pagos_alquiler'
    
    id = Column(Integer, primary_key=True)
    asignacion_id = Column(Integer, ForeignKey('asignaciones_alojamiento.id'))
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    alojamiento_id = Column(Integer, ForeignKey('alojamientos.id'))
    
    mes = Column(Integer)  # 1-12
    ano = Column(Integer)
    monto = Column(Float, nullable=False)
    concepto = Column(String(255))  # alquiler, gastos, deposito, etc.
    
    estado = Column(String(50), default='pendiente')  # pendiente, pagado, atrasado, dispensado
    fecha_vencimiento = Column(DateTime)
    fecha_pago = Column(DateTime)
    
    metodo_pago = Column(String(100))
    referencia_pago = Column(String(255))
    comprobante_ruta = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class GestorAlojamiento:
    """Gestor principal de alojamientos"""
    
    @staticmethod
    def registrar_alojamiento(datos_alojamiento: Dict) -> Alojamiento:
        """
        Registra un nuevo alojamiento disponible
        
        Args:
            datos_alojamiento: Diccionario con información del alojamiento
            
        Returns:
            Objeto Alojamiento creado
        """
        db = get_db()
        
        alojamiento = Alojamiento(**datos_alojamiento)
        db.add(alojamiento)
        db.commit()
        db.refresh(alojamiento)
        
        return alojamiento
    
    @staticmethod
    def buscar_alojamientos(
        ciudad: str = None,
        precio_max: float = None,
        tipo: str = None,
        disponible: bool = True,
        fecha_desde: datetime = None
    ) -> List[Alojamiento]:
        """
        Busca alojamientos disponibles según criterios
        
        Args:
            ciudad: Ciudad deseada
            precio_max: Precio máximo mensual
            tipo: Tipo de alojamiento
            disponible: Solo mostrar disponibles
            fecha_desde: Fecha desde la que se necesita
            
        Returns:
            Lista de alojamientos que cumplen criterios
        """
        db = get_db()
        query = db.query(Alojamiento).filter(Alojamiento.activo == True)
        
        if disponible:
            query = query.filter(Alojamiento.disponible == True)
            query = query.filter(Alojamiento.ocupados_actual < Alojamiento.capacidad_maxima)
        
        if ciudad:
            query = query.filter(Alojamiento.ciudad.ilike(f'%{ciudad}%'))
        
        if precio_max:
            query = query.filter(Alojamiento.precio_mensual <= precio_max)
        
        if tipo:
            query = query.filter(Alojamiento.tipo == tipo)
        
        if fecha_desde:
            query = query.filter(
                (Alojamiento.fecha_disponible_desde <= fecha_desde) |
                (Alojamiento.fecha_disponible_desde == None)
            )
        
        return query.order_by(Alojamiento.precio_mensual).all()
    
    @staticmethod
    def asignar_alojamiento(
        estudiante_id: int,
        alojamiento_id: int,
        fecha_inicio: datetime,
        duracion_meses: int,
        precio_acordado: float = None
    ) -> AsignacionAlojamiento:
        """
        Asigna un alojamiento a un estudiante
        
        Args:
            estudiante_id: ID del estudiante
            alojamiento_id: ID del alojamiento
            fecha_inicio: Fecha de inicio del contrato
            duracion_meses: Duración en meses
            precio_acordado: Precio acordado (si es diferente al publicado)
            
        Returns:
            Objeto AsignacionAlojamiento creado
        """
        from modules.estudiantes import GestorEstudiantes
        
        db = get_db()
        
        # Verificar disponibilidad
        alojamiento = db.query(Alojamiento).filter(Alojamiento.id == alojamiento_id).first()
        if not alojamiento:
            raise ValueError("Alojamiento no encontrado")
        
        if alojamiento.ocupados_actual >= alojamiento.capacidad_maxima:
            raise ValueError("Alojamiento sin capacidad disponible")
        
        # Crear asignación
        fecha_fin = fecha_inicio + timedelta(days=30 * duracion_meses)
        proximo_pago = fecha_inicio.replace(day=1) + timedelta(days=32)
        proximo_pago = proximo_pago.replace(day=1)
        
        asignacion = AsignacionAlojamiento(
            estudiante_id=estudiante_id,
            alojamiento_id=alojamiento_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            duracion_meses=duracion_meses,
            precio_acordado=precio_acordado or alojamiento.precio_mensual,
            deposito_pagado=alojamiento.deposito_requerido or 0,
            gastos_mensuales=alojamiento.gastos_adicionales,
            estado='activo',
            proximo_pago_fecha=proximo_pago
        )
        
        db.add(asignacion)
        
        # Actualizar ocupación del alojamiento
        alojamiento.ocupados_actual += 1
        if alojamiento.ocupados_actual >= alojamiento.capacidad_maxima:
            alojamiento.disponible = False
        
        # Actualizar estudiante
        estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=estudiante_id)
        if estudiante:
            estudiante.alojamiento_asignado_id = alojamiento_id
            estudiante.necesita_alojamiento = False
        
        db.commit()
        db.refresh(asignacion)
        
        # Crear pagos mensuales programados
        GestorAlojamiento._crear_pagos_mensuales(asignacion.id, fecha_inicio, duracion_meses, precio_acordado or alojamiento.precio_mensual)
        
        # Crear evento de inicio de alquiler
        GestorEstudiantes.crear_evento(
            estudiante_id=estudiante_id,
            tipo_evento='inicio_alquiler',
            titulo='Inicio de alquiler',
            fecha_evento=fecha_inicio,
            descripcion=f'Inicio del contrato de alquiler en {alojamiento.direccion}',
            dias_recordatorio=3
        )
        
        return asignacion
    
    @staticmethod
    def _crear_pagos_mensuales(asignacion_id: int, fecha_inicio: datetime, duracion_meses: int, monto_mensual: float):
        """Crea los pagos mensuales programados para una asignación"""
        db = get_db()
        asignacion = db.query(AsignacionAlojamiento).filter(AsignacionAlojamiento.id == asignacion_id).first()
        
        if not asignacion:
            return
        
        fecha_pago = fecha_inicio.replace(day=asignacion.dia_pago_mensual)
        
        for mes_num in range(duracion_meses):
            pago = PagoAlquiler(
                asignacion_id=asignacion_id,
                estudiante_id=asignacion.estudiante_id,
                alojamiento_id=asignacion.alojamiento_id,
                mes=(fecha_pago.month),
                ano=fecha_pago.year,
                monto=monto_mensual,
                concepto='Alquiler mensual',
                estado='pendiente',
                fecha_vencimiento=fecha_pago
            )
            db.add(pago)
            
            # Siguiente mes
            fecha_pago = fecha_pago + timedelta(days=32)
            fecha_pago = fecha_pago.replace(day=asignacion.dia_pago_mensual)
        
        db.commit()
    
    @staticmethod
    def alertas_alquiler(dias_anticipacion: int = 7) -> List[Dict]:
        """
        Genera alertas de pagos de alquiler próximos o vencidos
        
        Args:
            dias_anticipacion: Días de anticipación para alertar
            
        Returns:
            Lista de alertas generadas
        """
        from modules.estudiantes import GestorEstudiantes
        
        db = get_db()
        alertas = []
        
        # Pagos próximos
        fecha_limite = datetime.utcnow() + timedelta(days=dias_anticipacion)
        
        pagos_proximos = db.query(PagoAlquiler).filter(
            PagoAlquiler.estado == 'pendiente',
            PagoAlquiler.fecha_vencimiento <= fecha_limite,
            PagoAlquiler.fecha_vencimiento >= datetime.utcnow()
        ).all()
        
        for pago in pagos_proximos:
            dias_restantes = (pago.fecha_vencimiento - datetime.utcnow()).days
            estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=pago.estudiante_id)
            alojamiento = db.query(Alojamiento).filter(Alojamiento.id == pago.alojamiento_id).first()
            
            alerta = {
                'tipo': 'pago_proximo',
                'estudiante_id': pago.estudiante_id,
                'pago_id': pago.id,
                'titulo': f'💰 Pago de alquiler en {dias_restantes} días',
                'mensaje': f"""
Recordatorio de pago de alquiler:

📅 Vencimiento: {pago.fecha_vencimiento.strftime('%d/%m/%Y')}
💰 Monto: {pago.monto:,.2f}€
🏠 Dirección: {alojamiento.direccion if alojamiento else 'N/A'}

Por favor, realiza el pago antes de la fecha de vencimiento.
""",
                'prioridad': 'alta' if dias_restantes <= 3 else 'normal',
                'dias_restantes': dias_restantes
            }
            alertas.append(alerta)
        
        # Pagos vencidos
        pagos_vencidos = db.query(PagoAlquiler).filter(
            PagoAlquiler.estado == 'pendiente',
            PagoAlquiler.fecha_vencimiento < datetime.utcnow()
        ).all()
        
        for pago in pagos_vencidos:
            dias_vencido = (datetime.utcnow() - pago.fecha_vencimiento).days
            estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=pago.estudiante_id)
            alojamiento = db.query(Alojamiento).filter(Alojamiento.id == pago.alojamiento_id).first()
            
            # Actualizar estado a atrasado
            pago.estado = 'atrasado'
            db.commit()
            
            alerta = {
                'tipo': 'pago_vencido',
                'estudiante_id': pago.estudiante_id,
                'pago_id': pago.id,
                'titulo': f'🚨 PAGO VENCIDO - {dias_vencido} días de retraso',
                'mensaje': f"""
⚠️ PAGO DE ALQUILER VENCIDO

📅 Fecha vencimiento: {pago.fecha_vencimiento.strftime('%d/%m/%Y')}
⏰ Días de retraso: {dias_vencido}
💰 Monto: {pago.monto:,.2f}€
🏠 Dirección: {alojamiento.direccion if alojamiento else 'N/A'}

Por favor, contacta al propietario y regulariza el pago urgentemente.
""",
                'prioridad': 'urgente',
                'dias_vencido': dias_vencido
            }
            alertas.append(alerta)
        
        return alertas
    
    @staticmethod
    def registrar_pago_alquiler(pago_id: int, fecha_pago: datetime, metodo_pago: str, referencia: str = None) -> bool:
        """
        Registra un pago de alquiler como completado
        
        Args:
            pago_id: ID del pago
            fecha_pago: Fecha en que se realizó el pago
            metodo_pago: Método utilizado (transferencia, efectivo, etc.)
            referencia: Número de referencia del pago
            
        Returns:
            True si se registró exitosamente
        """
        db = get_db()
        pago = db.query(PagoAlquiler).filter(PagoAlquiler.id == pago_id).first()
        
        if not pago:
            return False
        
        pago.estado = 'pagado'
        pago.fecha_pago = fecha_pago
        pago.metodo_pago = metodo_pago
        pago.referencia_pago = referencia
        
        # Actualizar último pago en asignación
        asignacion = db.query(AsignacionAlojamiento).filter(
            AsignacionAlojamiento.id == pago.asignacion_id
        ).first()
        
        if asignacion:
            asignacion.ultimo_pago_fecha = fecha_pago
            # Calcular próximo pago
            proximo = fecha_pago + timedelta(days=32)
            proximo = proximo.replace(day=asignacion.dia_pago_mensual)
            asignacion.proximo_pago_fecha = proximo
        
        db.commit()
        return True
    
    @staticmethod
    def finalizar_alojamiento(asignacion_id: int, fecha_fin: datetime = None) -> bool:
        """
        Finaliza una asignación de alojamiento
        
        Args:
            asignacion_id: ID de la asignación
            fecha_fin: Fecha de finalización (por defecto, hoy)
            
        Returns:
            True si se finalizó exitosamente
        """
        db = get_db()
        asignacion = db.query(AsignacionAlojamiento).filter(
            AsignacionAlojamiento.id == asignacion_id
        ).first()
        
        if not asignacion:
            return False
        
        asignacion.estado = 'finalizado'
        asignacion.fecha_fin = fecha_fin or datetime.utcnow()
        
        # Liberar espacio en alojamiento
        alojamiento = db.query(Alojamiento).filter(
            Alojamiento.id == asignacion.alojamiento_id
        ).first()
        
        if alojamiento:
            alojamiento.ocupados_actual = max(0, alojamiento.ocupados_actual - 1)
            if alojamiento.ocupados_actual < alojamiento.capacidad_maxima:
                alojamiento.disponible = True
        
        # Actualizar estudiante
        from modules.estudiantes import GestorEstudiantes
        estudiante = GestorEstudiantes.obtener_estudiante(estudiante_id=asignacion.estudiante_id)
        if estudiante:
            estudiante.alojamiento_asignado_id = None
            estudiante.necesita_alojamiento = True
        
        db.commit()
        return True
    
    @staticmethod
    def obtener_alojamiento_estudiante(estudiante_id: int) -> Optional[Dict]:
        """
        Obtiene información del alojamiento actual de un estudiante
        
        Args:
            estudiante_id: ID del estudiante
            
        Returns:
            Diccionario con información del alojamiento o None
        """
        db = get_db()
        
        asignacion = db.query(AsignacionAlojamiento).filter(
            AsignacionAlojamiento.estudiante_id == estudiante_id,
            AsignacionAlojamiento.estado == 'activo'
        ).first()
        
        if not asignacion:
            return None
        
        alojamiento = db.query(Alojamiento).filter(
            Alojamiento.id == asignacion.alojamiento_id
        ).first()
        
        if not alojamiento:
            return None
        
        # Obtener pagos pendientes
        pagos_pendientes = db.query(PagoAlquiler).filter(
            PagoAlquiler.asignacion_id == asignacion.id,
            PagoAlquiler.estado.in_(['pendiente', 'atrasado'])
        ).count()
        
        return {
            'asignacion': asignacion,
            'alojamiento': alojamiento,
            'direccion': alojamiento.direccion,
            'precio_mensual': asignacion.precio_acordado,
            'fecha_inicio': asignacion.fecha_inicio,
            'fecha_fin': asignacion.fecha_fin,
            'proximo_pago': asignacion.proximo_pago_fecha,
            'pagos_pendientes': pagos_pendientes,
            'propietario': {
                'nombre': alojamiento.propietario_nombre,
                'telefono': alojamiento.propietario_telefono,
                'email': alojamiento.propietario_email
            }
        }
    
    @staticmethod
    def listar_alojamientos_admin(filtros: Dict = None) -> List[Alojamiento]:
        """
        Lista todos los alojamientos (para administradores)
        
        Args:
            filtros: Diccionario con filtros opcionales
            
        Returns:
            Lista de alojamientos
        """
        db = get_db()
        query = db.query(Alojamiento)
        
        if filtros:
            if 'ciudad' in filtros:
                query = query.filter(Alojamiento.ciudad.ilike(f'%{filtros["ciudad"]}%'))
            if 'disponible' in filtros:
                query = query.filter(Alojamiento.disponible == filtros['disponible'])
            if 'tipo' in filtros:
                query = query.filter(Alojamiento.tipo == filtros['tipo'])
        
        return query.all()
