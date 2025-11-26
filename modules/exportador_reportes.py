"""
Sistema de Exportación de Reportes
Admin puede exportar datos en Excel, CSV y PDF
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict
from modules.estudiantes import Estudiante
from database.models import get_db
import io


class ExportadorReportes:
    """Exporta datos en múltiples formatos"""
    
    @staticmethod
    def exportar_excel(
        estudiantes: List[Estudiante] = None,
        incluir_todo: bool = False
    ) -> bytes:
        """
        Exporta estudiantes a Excel
        
        Args:
            estudiantes: Lista de estudiantes (opcional)
            incluir_todo: Si incluir todos los estudiantes
            
        Returns:
            Bytes del archivo Excel
        """
        db = get_db()
        
        try:
            if estudiantes is None:
                if incluir_todo:
                    estudiantes = db.query(Estudiante).all()
                else:
                    estudiantes = db.query(Estudiante).filter(
                        Estudiante.estado_procesamiento.in_([
                            'pendiente_revision_admin',
                            'aprobado_admin',
                            'enviado_estudiante'
                        ])
                    ).all()
            
            # Preparar datos
            datos = []
            for est in estudiantes:
                datos.append({
                    'ID': est.id,
                    'Nombre': est.nombre_completo,
                    'Pasaporte': est.numero_pasaporte,
                    'Edad': est.edad,
                    'Nacionalidad': est.nacionalidad,
                    'Ciudad': est.ciudad_origen,
                    'Especialidad': est.especialidad_interes,
                    'Nivel Español': est.nivel_espanol,
                    'Email': est.email,
                    'Teléfono': est.telefono,
                    'Estado Procesamiento': est.estado_procesamiento,
                    'Estado Visa': est.estado_visa,
                    'Fecha Registro': est.created_at.strftime('%d/%m/%Y %H:%M') if est.created_at else '',
                    'Fecha Procesamiento': est.fecha_procesamiento_automatico.strftime('%d/%m/%Y %H:%M') if est.fecha_procesamiento_automatico else '',
                    'Admin Revisor': est.admin_revisor_id or ''
                })
            
            # Crear DataFrame
            df = pd.DataFrame(datos)
            
            # Exportar a Excel en memoria
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Estudiantes', index=False)
                
                # Formatear
                workbook = writer.book
                worksheet = writer.sheets['Estudiantes']
                
                # Formato de encabezados
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#2C3E50',
                    'font_color': 'white',
                    'border': 1
                })
                
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                    worksheet.set_column(col_num, col_num, 15)
            
            buffer.seek(0)
            return buffer.getvalue()
            
        finally:
            db.close()
    
    @staticmethod
    def exportar_csv(estudiantes: List[Estudiante] = None) -> str:
        """
        Exporta estudiantes a CSV
        
        Args:
            estudiantes: Lista de estudiantes
            
        Returns:
            String con contenido CSV
        """
        db = get_db()
        
        try:
            if estudiantes is None:
                estudiantes = db.query(Estudiante).all()
            
            datos = []
            for est in estudiantes:
                datos.append({
                    'ID': est.id,
                    'Nombre': est.nombre_completo,
                    'Pasaporte': est.numero_pasaporte,
                    'Edad': est.edad,
                    'Nacionalidad': est.nacionalidad,
                    'Especialidad': est.especialidad_interes,
                    'Estado': est.estado_procesamiento,
                    'Email': est.email
                })
            
            df = pd.DataFrame(datos)
            return df.to_csv(index=False)
            
        finally:
            db.close()
    
    @staticmethod
    def exportar_reporte_completo(
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None
    ) -> bytes:
        """
        Genera reporte completo en Excel con múltiples hojas
        
        Args:
            fecha_desde: Fecha inicio
            fecha_hasta: Fecha fin
            
        Returns:
            Bytes del archivo Excel
        """
        from modules.admin_panel import PanelAdministrativo
        
        db = get_db()
        
        try:
            # Consultar estudiantes en el período
            query = db.query(Estudiante)
            
            if fecha_desde:
                query = query.filter(Estudiante.created_at >= fecha_desde)
            
            if fecha_hasta:
                query = query.filter(Estudiante.created_at <= fecha_hasta)
            
            estudiantes = query.all()
            
            # Preparar datos para múltiples hojas
            buffer = io.BytesIO()
            
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # HOJA 1: Resumen Ejecutivo
                resumen = PanelAdministrativo.dashboard()
                df_resumen = pd.DataFrame([resumen['resumen']])
                df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
                
                # HOJA 2: Estudiantes
                datos_estudiantes = []
                for est in estudiantes:
                    datos_estudiantes.append({
                        'ID': est.id,
                        'Nombre': est.nombre_completo,
                        'Especialidad': est.especialidad_interes,
                        'Estado': est.estado_procesamiento,
                        'Fecha Registro': est.created_at
                    })
                
                df_estudiantes = pd.DataFrame(datos_estudiantes)
                df_estudiantes.to_excel(writer, sheet_name='Estudiantes', index=False)
                
                # HOJA 3: Estadísticas por Especialidad
                especialidades = PanelAdministrativo.estadisticas_por_especialidad()
                df_especialidades = pd.DataFrame(especialidades)
                df_especialidades.to_excel(writer, sheet_name='Por Especialidad', index=False)
            
            buffer.seek(0)
            return buffer.getvalue()
            
        finally:
            db.close()
    
    @staticmethod
    def guardar_archivo(contenido: bytes, nombre: str, formato: str):
        """
        Guarda archivo en disco
        
        Args:
            contenido: Bytes del archivo
            nombre: Nombre base del archivo
            formato: Formato (excel, csv, pdf)
        """
        extension = {'excel': 'xlsx', 'csv': 'csv', 'pdf': 'pdf'}.get(formato, 'xlsx')
        filename = f"{nombre}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
        
        with open(filename, 'wb') as f:
            f.write(contenido)
        
        print(f"✅ Archivo guardado: {filename}")
        return filename
