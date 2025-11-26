-- Migration: Agregar columnas OCR a tabla documentos
-- Fecha: 2025-11-26
-- Descripción: Añade campos para almacenar resultados de validación OCR

ALTER TABLE documentos 
ADD COLUMN IF NOT EXISTS ocr_procesado BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS ocr_texto_extraido TEXT,
ADD COLUMN IF NOT EXISTS ocr_datos_extraidos TEXT,
ADD COLUMN IF NOT EXISTS ocr_valido BOOLEAN DEFAULT NULL,
ADD COLUMN IF NOT EXISTS ocr_advertencias TEXT,
ADD COLUMN IF NOT EXISTS ocr_errores TEXT,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

-- Índice para búsqueda rápida de documentos sin procesar
CREATE INDEX IF NOT EXISTS idx_documentos_ocr_pendientes 
ON documentos(estudiante_id, ocr_procesado) 
WHERE ocr_procesado IS FALSE OR ocr_procesado IS NULL;

-- Índice para documentos con errores
CREATE INDEX IF NOT EXISTS idx_documentos_ocr_invalidos 
ON documentos(ocr_valido) 
WHERE ocr_valido IS FALSE;

COMMENT ON COLUMN documentos.ocr_procesado IS 'Indica si el documento fue procesado por OCR';
COMMENT ON COLUMN documentos.ocr_texto_extraido IS 'Texto completo extraído del documento';
COMMENT ON COLUMN documentos.ocr_datos_extraidos IS 'JSON con datos estructurados extraídos';
COMMENT ON COLUMN documentos.ocr_valido IS 'Resultado de validación automática';
COMMENT ON COLUMN documentos.ocr_advertencias IS 'Lista de advertencias detectadas';
COMMENT ON COLUMN documentos.ocr_errores IS 'Lista de errores críticos detectados';
