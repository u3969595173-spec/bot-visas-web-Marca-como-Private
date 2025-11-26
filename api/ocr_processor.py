"""
OCR Inteligente para Validación de Documentos
Extrae y valida información de pasaportes, certificados y extractos bancarios
"""

import re
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from io import BytesIO
from PIL import Image
import pytesseract

# Configurar ruta de Tesseract (Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class OCRProcessor:
    """Procesador OCR para validación automática de documentos"""
    
    # Patrones de validación
    PASSPORT_MRZ_PATTERN = r'^P<[A-Z]{3}[A-Z<]+<<[A-Z<]+$'
    PASSPORT_NUMBER_PATTERN = r'^[A-Z0-9]{6,9}$'
    DATE_PATTERN = r'\d{2}[/-]\d{2}[/-]\d{4}'
    AMOUNT_PATTERN = r'[\$€£]?\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?'
    
    # Palabras clave para detección de tipo de documento
    PASSPORT_KEYWORDS = ['passport', 'pasaporte', 'passeport', 'reisepass', 'nationality', 'nacionalidad']
    CERTIFICATE_KEYWORDS = ['certificate', 'certificado', 'university', 'universidad', 'degree', 'título']
    BANK_KEYWORDS = ['bank', 'banco', 'balance', 'saldo', 'account', 'cuenta', 'statement']
    
    def __init__(self):
        self.tesseract_available = self._check_tesseract()
    
    def _check_tesseract(self) -> bool:
        """Verifica si Tesseract está instalado"""
        try:
            pytesseract.get_tesseract_version()
            return True
        except Exception as e:
            print(f"⚠️ Tesseract no disponible: {e}")
            return False
    
    def extraer_texto_imagen(self, imagen_base64: str, idioma: str = 'spa+eng') -> str:
        """
        Extrae texto de una imagen usando OCR
        
        Args:
            imagen_base64: Imagen codificada en base64
            idioma: Idiomas para OCR (por defecto español + inglés)
        
        Returns:
            Texto extraído de la imagen
        """
        if not self.tesseract_available:
            raise Exception("Tesseract OCR no está instalado. Instale con: apt-get install tesseract-ocr")
        
        try:
            # Decodificar imagen
            imagen_bytes = base64.b64decode(imagen_base64)
            imagen = Image.open(BytesIO(imagen_bytes))
            
            # Preprocesar imagen para mejorar OCR
            imagen = imagen.convert('L')  # Convertir a escala de grises
            
            # Extraer texto con Tesseract
            texto = pytesseract.image_to_string(imagen, lang=idioma)
            
            return texto.strip()
            
        except Exception as e:
            raise Exception(f"Error extrayendo texto: {str(e)}")
    
    def detectar_tipo_documento(self, texto: str) -> str:
        """
        Detecta el tipo de documento basándose en palabras clave
        
        Returns:
            'pasaporte', 'certificado', 'extracto_bancario', 'otro'
        """
        texto_lower = texto.lower()
        
        # Contar coincidencias de palabras clave
        passport_matches = sum(1 for kw in self.PASSPORT_KEYWORDS if kw in texto_lower)
        certificate_matches = sum(1 for kw in self.CERTIFICATE_KEYWORDS if kw in texto_lower)
        bank_matches = sum(1 for kw in self.BANK_KEYWORDS if kw in texto_lower)
        
        # Determinar tipo basado en mayor cantidad de coincidencias
        max_matches = max(passport_matches, certificate_matches, bank_matches)
        
        if max_matches == 0:
            return 'otro'
        elif passport_matches == max_matches:
            return 'pasaporte'
        elif certificate_matches == max_matches:
            return 'certificado'
        else:
            return 'extracto_bancario'
    
    def validar_pasaporte(self, texto: str) -> Dict:
        """
        Valida pasaporte y extrae información clave
        
        Returns:
            Dict con: numero_pasaporte, nombre, nacionalidad, fecha_emision, 
                     fecha_expiracion, vigente, errores
        """
        resultado = {
            'tipo': 'pasaporte',
            'valido': False,
            'datos_extraidos': {},
            'advertencias': [],
            'errores': []
        }
        
        # Extraer número de pasaporte
        numeros = re.findall(r'[A-Z]{1,2}\d{6,9}|\d{6,9}[A-Z]{1,2}', texto)
        if numeros:
            resultado['datos_extraidos']['numero_pasaporte'] = numeros[0]
        else:
            resultado['errores'].append('No se encontró número de pasaporte válido')
        
        # Extraer fechas
        fechas = re.findall(self.DATE_PATTERN, texto)
        if len(fechas) >= 2:
            try:
                fecha_emision = self._parse_fecha(fechas[0])
                fecha_expiracion = self._parse_fecha(fechas[1])
                
                resultado['datos_extraidos']['fecha_emision'] = fecha_emision.strftime('%Y-%m-%d')
                resultado['datos_extraidos']['fecha_expiracion'] = fecha_expiracion.strftime('%Y-%m-%d')
                
                # Validar vigencia (mínimo 6 meses)
                dias_hasta_expiracion = (fecha_expiracion - datetime.now()).days
                resultado['datos_extraidos']['dias_vigencia'] = dias_hasta_expiracion
                
                if dias_hasta_expiracion < 0:
                    resultado['errores'].append('❌ Pasaporte VENCIDO')
                elif dias_hasta_expiracion < 180:  # 6 meses
                    resultado['advertencias'].append(f'⚠️ Pasaporte expira en {dias_hasta_expiracion} días (se requieren 6 meses de vigencia)')
                else:
                    resultado['datos_extraidos']['vigente'] = True
                    
            except Exception as e:
                resultado['errores'].append(f'Error procesando fechas: {str(e)}')
        else:
            resultado['errores'].append('No se encontraron fechas de emisión/expiración')
        
        # Extraer nombre (líneas en mayúsculas)
        lineas_mayusculas = [l for l in texto.split('\n') if l.isupper() and len(l) > 5]
        if lineas_mayusculas:
            resultado['datos_extraidos']['nombre_extraido'] = lineas_mayusculas[0]
        
        # Validar MRZ (Machine Readable Zone)
        lineas_mrz = [l for l in texto.split('\n') if re.match(r'^[A-Z0-9<]{30,}$', l)]
        if lineas_mrz:
            resultado['datos_extraidos']['mrz_detectado'] = True
        else:
            resultado['advertencias'].append('⚠️ No se detectó MRZ (puede dificultar lectura automática)')
        
        # Marcar como válido si no hay errores críticos
        resultado['valido'] = len(resultado['errores']) == 0
        
        return resultado
    
    def validar_certificado_academico(self, texto: str) -> Dict:
        """
        Valida certificado académico y extrae información
        
        Returns:
            Dict con: universidad, titulo, fecha_emision, sellos_detectados, valido
        """
        resultado = {
            'tipo': 'certificado_academico',
            'valido': False,
            'datos_extraidos': {},
            'advertencias': [],
            'errores': []
        }
        
        # Buscar nombre de universidad
        universidades_españa = [
            'Universidad Complutense', 'UCM', 'Universidad de Barcelona', 'UB',
            'Universidad Autónoma', 'UAM', 'Universidad Politécnica', 'UPM',
            'Universidad de Valencia', 'Universidad de Sevilla'
        ]
        
        texto_lower = texto.lower()
        universidad_encontrada = None
        for uni in universidades_españa:
            if uni.lower() in texto_lower:
                universidad_encontrada = uni
                break
        
        if universidad_encontrada:
            resultado['datos_extraidos']['universidad'] = universidad_encontrada
        else:
            resultado['advertencias'].append('⚠️ Universidad no identificada (verificar manualmente)')
        
        # Extraer fechas
        fechas = re.findall(self.DATE_PATTERN, texto)
        if fechas:
            resultado['datos_extraidos']['fecha_emision'] = fechas[0]
        else:
            resultado['errores'].append('No se encontró fecha de emisión')
        
        # Buscar palabras clave de títulos
        titulos_keywords = ['bachelor', 'master', 'licenciatura', 'grado', 'máster', 'doctorado']
        titulo_encontrado = None
        for keyword in titulos_keywords:
            if keyword in texto_lower:
                titulo_encontrado = keyword.title()
                break
        
        if titulo_encontrado:
            resultado['datos_extraidos']['nivel_academico'] = titulo_encontrado
        
        # Detectar sellos/firmas (buscar palabras clave)
        sellos_keywords = ['sello', 'firma', 'seal', 'signature', 'rector', 'decano']
        sellos_encontrados = sum(1 for kw in sellos_keywords if kw in texto_lower)
        resultado['datos_extraidos']['indicadores_autenticidad'] = sellos_encontrados
        
        if sellos_encontrados == 0:
            resultado['advertencias'].append('⚠️ No se detectaron sellos o firmas (verificar autenticidad)')
        
        # Validar antigüedad (certificados muy antiguos pueden requerir apostilla)
        if fechas:
            try:
                fecha_cert = self._parse_fecha(fechas[0])
                años_antiguedad = (datetime.now() - fecha_cert).days / 365
                resultado['datos_extraidos']['años_antiguedad'] = round(años_antiguedad, 1)
                
                if años_antiguedad > 5:
                    resultado['advertencias'].append(f'⚠️ Certificado de hace {round(años_antiguedad)} años (puede requerir apostilla reciente)')
            except:
                pass
        
        # Marcar como válido si no hay errores críticos
        resultado['valido'] = len(resultado['errores']) == 0
        
        return resultado
    
    def validar_extracto_bancario(self, texto: str) -> Dict:
        """
        Valida extracto bancario y extrae montos
        
        Returns:
            Dict con: banco, saldo, fecha, montos_suficientes, valido
        """
        resultado = {
            'tipo': 'extracto_bancario',
            'valido': False,
            'datos_extraidos': {},
            'advertencias': [],
            'errores': []
        }
        
        # Buscar nombre de banco
        bancos_comunes = [
            'BBVA', 'Santander', 'CaixaBank', 'Bankia', 'Sabadell',
            'ING', 'Banco Popular', 'Bankinter', 'Unicaja'
        ]
        
        banco_encontrado = None
        for banco in bancos_comunes:
            if banco.lower() in texto.lower():
                banco_encontrado = banco
                break
        
        if banco_encontrado:
            resultado['datos_extraidos']['banco'] = banco_encontrado
        else:
            resultado['advertencias'].append('⚠️ Banco no identificado')
        
        # Extraer montos (buscar números con símbolos de moneda)
        montos = re.findall(self.AMOUNT_PATTERN, texto)
        if montos:
            # Limpiar y convertir montos
            montos_numericos = []
            for monto in montos:
                try:
                    # Eliminar símbolos y convertir
                    monto_limpio = re.sub(r'[^\d.,]', '', monto)
                    monto_limpio = monto_limpio.replace(',', '.')
                    valor = float(monto_limpio)
                    if valor > 100:  # Filtrar centavos
                        montos_numericos.append(valor)
                except:
                    pass
            
            if montos_numericos:
                saldo_maximo = max(montos_numericos)
                resultado['datos_extraidos']['saldo_detectado'] = f"€{saldo_maximo:,.2f}"
                resultado['datos_extraidos']['saldo_numerico'] = saldo_maximo
                
                # Validar fondos suficientes (15,000€ mínimo recomendado)
                FONDOS_MINIMOS = 15000
                if saldo_maximo >= FONDOS_MINIMOS:
                    resultado['datos_extraidos']['fondos_suficientes'] = True
                elif saldo_maximo >= FONDOS_MINIMOS * 0.8:  # 80% del mínimo
                    resultado['advertencias'].append(f'⚠️ Fondos ligeramente por debajo del recomendado (€{FONDOS_MINIMOS:,})')
                    resultado['datos_extraidos']['fondos_suficientes'] = True
                else:
                    resultado['errores'].append(f'❌ Fondos insuficientes. Detectado: €{saldo_maximo:,.2f}, Requerido: €{FONDOS_MINIMOS:,}')
                    resultado['datos_extraidos']['fondos_suficientes'] = False
        else:
            resultado['errores'].append('No se detectaron montos en el extracto')
        
        # Extraer fecha del extracto
        fechas = re.findall(self.DATE_PATTERN, texto)
        if fechas:
            resultado['datos_extraidos']['fecha_extracto'] = fechas[0]
            
            # Validar que sea reciente (últimos 3 meses)
            try:
                fecha_extracto = self._parse_fecha(fechas[0])
                dias_antiguedad = (datetime.now() - fecha_extracto).days
                resultado['datos_extraidos']['dias_antiguedad'] = dias_antiguedad
                
                if dias_antiguedad > 90:
                    resultado['advertencias'].append(f'⚠️ Extracto antiguo ({dias_antiguedad} días). Se recomienda extracto reciente (<3 meses)')
                    
            except Exception as e:
                resultado['advertencias'].append(f'Error al validar fecha: {str(e)}')
        else:
            resultado['errores'].append('No se encontró fecha del extracto')
        
        # Marcar como válido si no hay errores críticos
        resultado['valido'] = len(resultado['errores']) == 0
        
        return resultado
    
    def procesar_documento(self, imagen_base64: str, tipo_esperado: Optional[str] = None) -> Dict:
        """
        Procesa documento completo: OCR + validación automática
        
        Args:
            imagen_base64: Imagen del documento en base64
            tipo_esperado: Tipo esperado ('pasaporte', 'certificado', 'extracto_bancario')
        
        Returns:
            Dict con resultado completo del procesamiento
        """
        resultado = {
            'exito': False,
            'texto_extraido': '',
            'tipo_detectado': '',
            'validacion': {},
            'tiempo_procesamiento': 0
        }
        
        inicio = datetime.now()
        
        try:
            # Paso 1: Extraer texto
            texto = self.extraer_texto_imagen(imagen_base64)
            resultado['texto_extraido'] = texto
            
            if not texto or len(texto) < 20:
                resultado['error'] = 'No se pudo extraer texto suficiente de la imagen. Verifique la calidad.'
                return resultado
            
            # Paso 2: Detectar tipo de documento
            tipo_detectado = tipo_esperado or self.detectar_tipo_documento(texto)
            resultado['tipo_detectado'] = tipo_detectado
            
            # Paso 3: Validar según tipo
            if tipo_detectado == 'pasaporte':
                validacion = self.validar_pasaporte(texto)
            elif tipo_detectado == 'certificado' or tipo_detectado == 'certificado_academico':
                validacion = self.validar_certificado_academico(texto)
            elif tipo_detectado == 'extracto_bancario':
                validacion = self.validar_extracto_bancario(texto)
            else:
                validacion = {
                    'tipo': 'otro',
                    'valido': False,
                    'datos_extraidos': {},
                    'advertencias': ['Tipo de documento no reconocido'],
                    'errores': []
                }
            
            resultado['validacion'] = validacion
            resultado['exito'] = True
            
            # Calcular tiempo de procesamiento
            resultado['tiempo_procesamiento'] = (datetime.now() - inicio).total_seconds()
            
            return resultado
            
        except Exception as e:
            resultado['error'] = str(e)
            resultado['tiempo_procesamiento'] = (datetime.now() - inicio).total_seconds()
            return resultado
    
    def _parse_fecha(self, fecha_str: str) -> datetime:
        """Intenta parsear fecha en múltiples formatos"""
        formatos = [
            '%d/%m/%Y',
            '%d-%m-%Y',
            '%m/%d/%Y',
            '%Y-%m-%d',
            '%d.%m.%Y'
        ]
        
        for formato in formatos:
            try:
                return datetime.strptime(fecha_str.strip(), formato)
            except:
                continue
        
        raise ValueError(f"No se pudo parsear fecha: {fecha_str}")
    
    def generar_reporte_validacion(self, resultado: Dict) -> str:
        """
        Genera reporte legible de validación
        
        Returns:
            String con reporte formateado
        """
        if not resultado.get('exito'):
            return f"❌ ERROR: {resultado.get('error', 'Error desconocido')}"
        
        validacion = resultado.get('validacion', {})
        tipo = validacion.get('tipo', 'desconocido')
        valido = validacion.get('valido', False)
        
        reporte = f"📄 DOCUMENTO: {tipo.upper()}\n"
        reporte += f"{'✅ VÁLIDO' if valido else '❌ INVÁLIDO'}\n\n"
        
        # Datos extraídos
        datos = validacion.get('datos_extraidos', {})
        if datos:
            reporte += "📊 DATOS EXTRAÍDOS:\n"
            for clave, valor in datos.items():
                reporte += f"  • {clave.replace('_', ' ').title()}: {valor}\n"
            reporte += "\n"
        
        # Advertencias
        advertencias = validacion.get('advertencias', [])
        if advertencias:
            reporte += "⚠️ ADVERTENCIAS:\n"
            for adv in advertencias:
                reporte += f"  {adv}\n"
            reporte += "\n"
        
        # Errores
        errores = validacion.get('errores', [])
        if errores:
            reporte += "❌ ERRORES:\n"
            for err in errores:
                reporte += f"  {err}\n"
            reporte += "\n"
        
        reporte += f"⏱️ Tiempo: {resultado.get('tiempo_procesamiento', 0):.2f}s"
        
        return reporte
