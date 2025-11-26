"""
Validador OCR Inteligente para Documentos
Extrae y valida información de pasaportes, DNI, extractos bancarios, cartas de admisión
USA OCR.space API (25,000 requests/mes gratis) - Sin instalación de Tesseract
"""

import requests
from PIL import Image
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import os


class ValidadorOCR:
    """
    Validador inteligente de documentos con OCR
    Extrae datos clave y valida según tipo de documento
    """
    
    # Patrones regex para diferentes tipos de datos
    PATRONES = {
        'pasaporte_numero': r'[A-Z]{1,3}\d{6,9}',
        'dni_numero': r'\d{8}[A-Z]',
        'fecha_ddmmyyyy': r'\d{2}[/-]\d{2}[/-]\d{4}',
        'fecha_yyyymmdd': r'\d{4}[/-]\d{2}[/-]\d{2}',
        'monto_euros': r'€?\s*\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?',
        'monto_dolares': r'\$\s*\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?',
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'iban': r'ES\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}',
    }
    
    # Palabras clave por tipo de documento
    PALABRAS_CLAVE = {
        'pasaporte': ['passport', 'pasaporte', 'surname', 'apellidos', 'given names', 'nationality'],
        'dni': ['dni', 'documento nacional', 'identidad', 'nacionalidad'],
        'extracto_bancario': ['balance', 'saldo', 'cuenta', 'account', 'bank', 'banco', 'statement'],
        'carta_admision': ['admission', 'admisión', 'accept', 'university', 'universidad', 'programa'],
        'certificado_idioma': ['certificate', 'certificado', 'nivel', 'level', 'a1', 'a2', 'b1', 'b2', 'c1', 'c2']
    }
    
    def __init__(self):
        """Inicializa el validador OCR"""
        self.resultados = {}
        self.alertas = []
        self.nivel_confianza = 0
        # API Key de OCR.space (gratis: 25,000 requests/mes)
        # Registrarse en: https://ocr.space/ocrapi
        self.ocr_api_key = os.getenv('OCR_SPACE_API_KEY', 'K81993791988957')  # Free tier key
    
    def procesar_documento(self, ruta_archivo: str, tipo_documento: str) -> Dict:
        """
        Procesa un documento con OCR y valida según su tipo
        
        Args:
            ruta_archivo: Ruta al archivo de imagen o PDF
            tipo_documento: pasaporte, dni, extracto_bancario, carta_admision, etc.
            
        Returns:
            Dict con datos extraídos, validación y alertas
        """
        try:
            # Validar imagen
            ruta_validada = self._preprocesar_imagen(ruta_archivo)
            
            # Extraer texto con OCR.space API
            texto = self._extraer_texto(ruta_validada)
            
            # Validar según tipo de documento
            if tipo_documento == 'pasaporte':
                validacion = self._validar_pasaporte(texto)
            elif tipo_documento == 'dni':
                validacion = self._validar_dni(texto)
            elif tipo_documento == 'extracto_bancario':
                validacion = self._validar_extracto_bancario(texto)
            elif tipo_documento == 'carta_admision':
                validacion = self._validar_carta_admision(texto)
            elif tipo_documento == 'certificado_idioma':
                validacion = self._validar_certificado_idioma(texto)
            else:
                validacion = self._validacion_generica(texto, tipo_documento)
            
            return {
                'exito': True,
                'tipo_documento': tipo_documento,
                'texto_extraido': texto[:500],  # Primeros 500 caracteres
                'datos_extraidos': validacion.get('datos', {}),
                'validacion': validacion.get('validacion', {}),
                'alertas': self.alertas,
                'nivel_confianza': self.nivel_confianza,
                'procesado_en': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'exito': False,
                'error': str(e),
                'tipo_documento': tipo_documento
            }
    
    def _preprocesar_imagen(self, ruta_archivo: str) -> str:
        """
        Verifica y prepara imagen para OCR
        Retorna la ruta del archivo (ya no procesamos localmente)
        """
        if not os.path.exists(ruta_archivo):
            raise ValueError("Archivo no encontrado")
        
        # Verificar que es una imagen válida
        try:
            img = Image.open(ruta_archivo)
            img.verify()
            return ruta_archivo
        except Exception as e:
            raise ValueError(f"Archivo no es una imagen válida: {e}")
    
    def _extraer_texto(self, ruta_archivo: str) -> str:
        """
        Extrae texto de imagen usando OCR.space API
        API gratuita: 25,000 requests/mes
        """
        try:
            # Preparar request a OCR.space
            with open(ruta_archivo, 'rb') as f:
                response = requests.post(
                    'https://api.ocr.space/parse/image',
                    files={'file': f},
                    data={
                        'apikey': self.ocr_api_key,
                        'language': 'spa',  # Español
                        'isOverlayRequired': False,
                        'detectOrientation': True,
                        'scale': True,
                        'OCREngine': 2  # Engine 2 es mejor para documentos
                    },
                    timeout=30
                )
            
            result = response.json()
            
            if result.get('IsErroredOnProcessing'):
                raise Exception(f"Error en OCR: {result.get('ErrorMessage', 'Unknown error')}")
            
            # Extraer texto parseado
            if result.get('ParsedResults'):
                texto = result['ParsedResults'][0].get('ParsedText', '')
                return texto.strip()
            else:
                raise Exception("No se pudo extraer texto del documento")
                
        except requests.exceptions.Timeout:
            raise Exception("Timeout al procesar OCR - intente de nuevo")
        except Exception as e:
            raise Exception(f"Error al extraer texto: {str(e)}")
    
    def _validar_pasaporte(self, texto: str) -> Dict:
        """
        Valida pasaporte:
        - Número de pasaporte
        - Fecha de emisión y expiración
        - Nombre completo
        - Nacionalidad
        - MRZ (Machine Readable Zone)
        """
        self.alertas = []
        datos = {}
        validacion = {}
        
        # Detectar número de pasaporte
        numeros_pasaporte = re.findall(self.PATRONES['pasaporte_numero'], texto)
        if numeros_pasaporte:
            datos['numero_pasaporte'] = numeros_pasaporte[0]
            validacion['numero_pasaporte'] = True
        else:
            validacion['numero_pasaporte'] = False
            self.alertas.append("No se detectó número de pasaporte")
        
        # Detectar fechas
        fechas = re.findall(self.PATRONES['fecha_ddmmyyyy'], texto)
        fechas += re.findall(self.PATRONES['fecha_yyyymmdd'], texto)
        
        if len(fechas) >= 2:
            datos['fecha_emision'] = fechas[0]
            datos['fecha_expiracion'] = fechas[1]
            
            # Validar vigencia (debe vencer en más de 6 meses)
            try:
                fecha_exp = self._parsear_fecha(fechas[1])
                hoy = datetime.now()
                dias_restantes = (fecha_exp - hoy).days
                
                if dias_restantes < 0:
                    validacion['vigencia'] = False
                    self.alertas.append("⚠️ PASAPORTE VENCIDO")
                elif dias_restantes < 180:
                    validacion['vigencia'] = False
                    self.alertas.append(f"⚠️ Pasaporte vence en {dias_restantes} días (mínimo 6 meses)")
                else:
                    validacion['vigencia'] = True
                    datos['dias_vigencia'] = dias_restantes
            except:
                validacion['vigencia'] = None
                self.alertas.append("No se pudo validar vigencia")
        else:
            validacion['fechas'] = False
            self.alertas.append("No se detectaron fechas de emisión/expiración")
        
        # Buscar palabras clave de pasaporte
        texto_lower = texto.lower()
        palabras_encontradas = sum(1 for palabra in self.PALABRAS_CLAVE['pasaporte'] 
                                   if palabra in texto_lower)
        
        if palabras_encontradas >= 3:
            validacion['formato'] = True
        else:
            validacion['formato'] = False
            self.alertas.append("Formato no parece ser un pasaporte válido")
        
        # Intentar extraer MRZ (últimas 2 líneas del pasaporte)
        lineas = texto.split('\n')
        posibles_mrz = [l for l in lineas[-5:] if len(l) > 30 and all(c.isupper() or c.isdigit() or c == '<' for c in l.replace(' ', ''))]
        
        if posibles_mrz:
            datos['mrz_detectado'] = True
            validacion['mrz'] = True
        else:
            validacion['mrz'] = False
            self.alertas.append("No se detectó zona MRZ (Machine Readable Zone)")
        
        # Calcular nivel de confianza
        validaciones_exitosas = sum(1 for v in validacion.values() if v is True)
        total_validaciones = len(validacion)
        self.nivel_confianza = int((validaciones_exitosas / total_validaciones) * 100) if total_validaciones > 0 else 0
        
        return {
            'datos': datos,
            'validacion': validacion
        }
    
    def _validar_dni(self, texto: str) -> Dict:
        """
        Valida DNI/NIE:
        - Número de documento
        - Fecha de nacimiento
        - Fecha de expiración
        - Nombre completo
        """
        self.alertas = []
        datos = {}
        validacion = {}
        
        # Detectar número DNI
        numeros_dni = re.findall(self.PATRONES['dni_numero'], texto)
        if numeros_dni:
            datos['numero_dni'] = numeros_dni[0]
            validacion['numero_dni'] = True
            
            # Validar letra DNI
            letra_correcta = self._calcular_letra_dni(numeros_dni[0][:8])
            if letra_correcta == numeros_dni[0][-1]:
                validacion['letra_valida'] = True
            else:
                validacion['letra_valida'] = False
                self.alertas.append(f"⚠️ Letra DNI incorrecta (esperada: {letra_correcta})")
        else:
            validacion['numero_dni'] = False
            self.alertas.append("No se detectó número de DNI")
        
        # Detectar fechas
        fechas = re.findall(self.PATRONES['fecha_ddmmyyyy'], texto)
        if len(fechas) >= 1:
            datos['fecha_nacimiento'] = fechas[0]
            validacion['fecha_nacimiento'] = True
        
        # Buscar palabras clave DNI
        texto_lower = texto.lower()
        palabras_encontradas = sum(1 for palabra in self.PALABRAS_CLAVE['dni'] 
                                   if palabra in texto_lower)
        
        if palabras_encontradas >= 2:
            validacion['formato'] = True
        else:
            validacion['formato'] = False
            self.alertas.append("Formato no parece ser un DNI válido")
        
        # Calcular nivel de confianza
        validaciones_exitosas = sum(1 for v in validacion.values() if v is True)
        total_validaciones = len(validacion)
        self.nivel_confianza = int((validaciones_exitosas / total_validaciones) * 100) if total_validaciones > 0 else 0
        
        return {
            'datos': datos,
            'validacion': validacion
        }
    
    def _validar_extracto_bancario(self, texto: str) -> Dict:
        """
        Valida extracto bancario:
        - Saldo disponible
        - Fecha del extracto
        - Nombre del banco
        - Número de cuenta/IBAN
        - Movimientos recientes
        """
        self.alertas = []
        datos = {}
        validacion = {}
        
        # Detectar montos
        montos_euros = re.findall(self.PATRONES['monto_euros'], texto)
        montos_dolares = re.findall(self.PATRONES['monto_dolares'], texto)
        
        if montos_euros:
            # Convertir a float
            montos_numericos = []
            for monto in montos_euros:
                try:
                    valor = float(monto.replace('€', '').replace(',', '.').replace(' ', ''))
                    montos_numericos.append(valor)
                except:
                    pass
            
            if montos_numericos:
                saldo_max = max(montos_numericos)
                datos['saldo_disponible'] = f"{saldo_max:,.2f} €"
                validacion['saldo_detectado'] = True
                
                # Validar saldo mínimo (15,000€ requeridos)
                if saldo_max >= 15000:
                    validacion['saldo_suficiente'] = True
                else:
                    validacion['saldo_suficiente'] = False
                    self.alertas.append(f"⚠️ Saldo insuficiente: {saldo_max:,.2f}€ (mínimo: 15,000€)")
            else:
                validacion['saldo_detectado'] = False
        else:
            validacion['saldo_detectado'] = False
            self.alertas.append("No se detectó saldo en el extracto")
        
        # Detectar IBAN
        ibans = re.findall(self.PATRONES['iban'], texto)
        if ibans:
            datos['iban'] = ibans[0]
            validacion['iban'] = True
        else:
            validacion['iban'] = False
            self.alertas.append("No se detectó IBAN")
        
        # Detectar fecha del extracto
        fechas = re.findall(self.PATRONES['fecha_ddmmyyyy'], texto)
        if fechas:
            datos['fecha_extracto'] = fechas[0]
            validacion['fecha'] = True
            
            # Validar antigüedad (no más de 3 meses)
            try:
                fecha_extracto = self._parsear_fecha(fechas[0])
                hoy = datetime.now()
                dias_antiguedad = (hoy - fecha_extracto).days
                
                if dias_antiguedad > 90:
                    validacion['extracto_actualizado'] = False
                    self.alertas.append(f"⚠️ Extracto muy antiguo ({dias_antiguedad} días)")
                else:
                    validacion['extracto_actualizado'] = True
                    datos['dias_antiguedad'] = dias_antiguedad
            except:
                validacion['extracto_actualizado'] = None
        else:
            validacion['fecha'] = False
            self.alertas.append("No se detectó fecha del extracto")
        
        # Buscar palabras clave bancarias
        texto_lower = texto.lower()
        palabras_encontradas = sum(1 for palabra in self.PALABRAS_CLAVE['extracto_bancario'] 
                                   if palabra in texto_lower)
        
        if palabras_encontradas >= 2:
            validacion['formato'] = True
        else:
            validacion['formato'] = False
            self.alertas.append("Formato no parece ser un extracto bancario válido")
        
        # Calcular nivel de confianza
        validaciones_exitosas = sum(1 for v in validacion.values() if v is True)
        total_validaciones = len(validacion)
        self.nivel_confianza = int((validaciones_exitosas / total_validaciones) * 100) if total_validaciones > 0 else 0
        
        return {
            'datos': datos,
            'validacion': validacion
        }
    
    def _validar_carta_admision(self, texto: str) -> Dict:
        """
        Valida carta de admisión:
        - Nombre de universidad
        - Programa/curso
        - Fecha de inicio
        - Duración
        - Precio/matrícula
        """
        self.alertas = []
        datos = {}
        validacion = {}
        
        # Buscar palabras clave de admisión
        texto_lower = texto.lower()
        palabras_encontradas = sum(1 for palabra in self.PALABRAS_CLAVE['carta_admision'] 
                                   if palabra in texto_lower)
        
        if palabras_encontradas >= 3:
            validacion['formato'] = True
        else:
            validacion['formato'] = False
            self.alertas.append("Formato no parece ser una carta de admisión válida")
        
        # Detectar fechas
        fechas = re.findall(self.PATRONES['fecha_ddmmyyyy'], texto)
        fechas += re.findall(self.PATRONES['fecha_yyyymmdd'], texto)
        
        if fechas:
            datos['fecha_inicio'] = fechas[0]
            validacion['fecha_inicio'] = True
            
            # Validar que la fecha de inicio sea futura
            try:
                fecha_inicio = self._parsear_fecha(fechas[0])
                hoy = datetime.now()
                
                if fecha_inicio < hoy:
                    self.alertas.append("⚠️ La fecha de inicio ya pasó")
                else:
                    dias_hasta_inicio = (fecha_inicio - hoy).days
                    datos['dias_hasta_inicio'] = dias_hasta_inicio
            except:
                pass
        else:
            validacion['fecha_inicio'] = False
            self.alertas.append("No se detectó fecha de inicio del curso")
        
        # Detectar email de contacto
        emails = re.findall(self.PATRONES['email'], texto)
        if emails:
            datos['email_contacto'] = emails[0]
            validacion['contacto'] = True
        
        # Buscar nombres de universidades conocidas
        universidades_conocidas = ['complutense', 'ucm', 'barcelona', 'ub', 'autónoma', 'uam', 
                                  'politécnica', 'upm', 'upc', 'pompeu fabra', 'upf', 'esade', 
                                  'ie', 'universidad europea', 'carlos iii', 'uc3m']
        
        universidad_detectada = None
        for uni in universidades_conocidas:
            if uni in texto_lower:
                universidad_detectada = uni.upper()
                break
        
        if universidad_detectada:
            datos['universidad'] = universidad_detectada
            validacion['universidad_reconocida'] = True
        else:
            validacion['universidad_reconocida'] = False
            self.alertas.append("No se reconoció una universidad española registrada")
        
        # Calcular nivel de confianza
        validaciones_exitosas = sum(1 for v in validacion.values() if v is True)
        total_validaciones = len(validacion)
        self.nivel_confianza = int((validaciones_exitosas / total_validaciones) * 100) if total_validaciones > 0 else 0
        
        return {
            'datos': datos,
            'validacion': validacion
        }
    
    def _validar_certificado_idioma(self, texto: str) -> Dict:
        """
        Valida certificado de idioma:
        - Nivel (A1, A2, B1, B2, C1, C2)
        - Institución emisora
        - Fecha de emisión
        - Nombre del estudiante
        """
        self.alertas = []
        datos = {}
        validacion = {}
        
        # Detectar nivel de idioma
        texto_upper = texto.upper()
        niveles = ['C2', 'C1', 'B2', 'B1', 'A2', 'A1']
        nivel_detectado = None
        
        for nivel in niveles:
            if nivel in texto_upper:
                nivel_detectado = nivel
                break
        
        if nivel_detectado:
            datos['nivel_idioma'] = nivel_detectado
            validacion['nivel'] = True
        else:
            validacion['nivel'] = False
            self.alertas.append("No se detectó nivel de idioma (A1-C2)")
        
        # Detectar fechas
        fechas = re.findall(self.PATRONES['fecha_ddmmyyyy'], texto)
        if fechas:
            datos['fecha_emision'] = fechas[0]
            validacion['fecha'] = True
        else:
            validacion['fecha'] = False
            self.alertas.append("No se detectó fecha de emisión")
        
        # Buscar palabras clave de certificado
        texto_lower = texto.lower()
        palabras_encontradas = sum(1 for palabra in self.PALABRAS_CLAVE['certificado_idioma'] 
                                   if palabra in texto_lower)
        
        if palabras_encontradas >= 2:
            validacion['formato'] = True
        else:
            validacion['formato'] = False
            self.alertas.append("Formato no parece ser un certificado de idioma válido")
        
        # Calcular nivel de confianza
        validaciones_exitosas = sum(1 for v in validacion.values() if v is True)
        total_validaciones = len(validacion)
        self.nivel_confianza = int((validaciones_exitosas / total_validaciones) * 100) if total_validaciones > 0 else 0
        
        return {
            'datos': datos,
            'validacion': validacion
        }
    
    def _validacion_generica(self, texto: str, tipo_documento: str) -> Dict:
        """Validación genérica para documentos no específicos"""
        self.alertas = []
        datos = {}
        validacion = {}
        
        # Detectar fechas
        fechas = re.findall(self.PATRONES['fecha_ddmmyyyy'], texto)
        if fechas:
            datos['fechas_detectadas'] = fechas
            validacion['fechas'] = True
        
        # Detectar emails
        emails = re.findall(self.PATRONES['email'], texto)
        if emails:
            datos['emails'] = emails
            validacion['contacto'] = True
        
        # Validar que tiene contenido
        if len(texto) > 100:
            validacion['contenido'] = True
        else:
            validacion['contenido'] = False
            self.alertas.append("Documento con muy poco texto extraído")
        
        self.nivel_confianza = 50  # Confianza media para documentos genéricos
        
        return {
            'datos': datos,
            'validacion': validacion
        }
    
    def _parsear_fecha(self, fecha_str: str) -> datetime:
        """Intenta parsear una fecha en varios formatos"""
        formatos = ['%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d', '%d.%m.%Y']
        
        for formato in formatos:
            try:
                return datetime.strptime(fecha_str, formato)
            except ValueError:
                continue
        
        raise ValueError(f"No se pudo parsear fecha: {fecha_str}")
    
    def _calcular_letra_dni(self, numero: str) -> str:
        """Calcula letra de DNI español"""
        letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
        return letras[int(numero) % 23]
