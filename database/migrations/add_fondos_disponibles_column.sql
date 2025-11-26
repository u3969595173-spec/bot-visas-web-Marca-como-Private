-- Migration: Agregar columna fondos_disponibles a tabla estudiantes
-- Fecha: 2025-11-26
-- Descripción: Añade campo para almacenar fondos disponibles del estudiante

ALTER TABLE estudiantes 
ADD COLUMN IF NOT EXISTS fondos_disponibles INTEGER;

COMMENT ON COLUMN estudiantes.fondos_disponibles IS 'Fondos disponibles del estudiante en euros';
