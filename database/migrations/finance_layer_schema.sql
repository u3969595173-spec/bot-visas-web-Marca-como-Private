-- ============================================================
-- CAPA FINANCIERA: ESQUEMA SQL FINAL PREPARADO PARA EJECUCIÓN
-- Proyecto: BotVisasEstudio / Capital Trade Iberia
-- Objetivo: crear la capa financiera sin tocar tablas existentes
-- Autor: Copilot
-- Fecha: 2026-08-16
--
-- REQUISITOS CUMPLIDOS:
-- - Reutiliza usuarios y documentos existentes
-- - No modifica users legacy ni estudiantes antigua
-- - Mantiene EUR, CUP y MLC totalmente separados
-- - Saldo derivado del backend desde movimientos validados
-- - Validaciones administrativas registradas
-- - Justificantes vinculados a aportaciones
-- - Referidos de un solo nivel
-- - Sin ejecutar SQL en este momento
-- ============================================================

BEGIN;

-- ============================================================
-- 1) OPERACIONES COMERCIALES
-- ============================================================
CREATE TABLE IF NOT EXISTS operaciones_comerciales (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    slug VARCHAR(120) NOT NULL UNIQUE,
    descripcion TEXT,
    categoria VARCHAR(40) NOT NULL DEFAULT 'comercial'
        CHECK (categoria IN ('comercial', 'exportacion', 'financiacion', 'otro')),
    estado VARCHAR(30) NOT NULL DEFAULT 'draft'
        CHECK (estado IN ('draft', 'published', 'active', 'closed', 'cancelled')),
    objetivo_capital NUMERIC(18,2) NOT NULL DEFAULT 0,
    capital_recaudado NUMERIC(18,2) NOT NULL DEFAULT 0,
    riesgo VARCHAR(20) NOT NULL DEFAULT 'medio'
        CHECK (riesgo IN ('bajo', 'medio', 'alto')),
    plazo_dias INTEGER,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_publicacion TIMESTAMPTZ,
    created_by BIGINT NOT NULL REFERENCES usuarios(id),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 2) CUENTAS BANCARIAS
-- ============================================================
CREATE TABLE IF NOT EXISTS cuentas_bancarias (
    id BIGSERIAL PRIMARY KEY,
    moneda CHAR(3) NOT NULL
        CHECK (moneda IN ('EUR', 'CUP', 'MLC')),
    banco VARCHAR(120) NOT NULL,
    titular VARCHAR(180) NOT NULL,
    iban VARCHAR(80),
    numero_cuenta VARCHAR(80),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creada_por_admin BIGINT NOT NULL REFERENCES usuarios(id),
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 3) APORTACIONES
-- ============================================================
CREATE TABLE IF NOT EXISTS aportaciones (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL REFERENCES usuarios(id),
    operacion_id BIGINT REFERENCES operaciones_comerciales(id),
    cuenta_destino_id BIGINT REFERENCES cuentas_bancarias(id),
    moneda CHAR(3) NOT NULL
        CHECK (moneda IN ('EUR', 'CUP', 'MLC')),
    importe NUMERIC(18,2) NOT NULL CHECK (importe > 0),
    estado VARCHAR(30) NOT NULL DEFAULT 'pending'
        CHECK (estado IN ('pending', 'validated', 'rejected', 'information_requested', 'cancelled')),
    fecha_solicitud TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_validacion TIMESTAMPTZ,
    validado_por BIGINT REFERENCES usuarios(id),
    comentarios TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_aportacion_validacion
        CHECK (
            (estado IN ('validated', 'rejected', 'information_requested', 'cancelled'))
            OR (fecha_validacion IS NULL AND validado_por IS NULL)
        )
);

-- ============================================================
-- 4) RETIROS
-- ============================================================
CREATE TABLE IF NOT EXISTS retiros (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL REFERENCES usuarios(id),
    moneda CHAR(3) NOT NULL
        CHECK (moneda IN ('EUR', 'CUP', 'MLC')),
    importe NUMERIC(18,2) NOT NULL CHECK (importe > 0),
    destino VARCHAR(255) NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'pending'
        CHECK (estado IN ('pending', 'approved', 'rejected', 'processing', 'processed', 'cancelled')),
    fecha_solicitud TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_aprobacion TIMESTAMPTZ,
    fecha_procesado TIMESTAMPTZ,
    aprobado_por BIGINT REFERENCES usuarios(id),
    comentarios TEXT,
    motivo_rechazo TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 5) SALDOS POR USUARIO Y MONEDA
-- ============================================================
CREATE TABLE IF NOT EXISTS saldos_usuario_moneda (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL REFERENCES usuarios(id),
    moneda CHAR(3) NOT NULL
        CHECK (moneda IN ('EUR', 'CUP', 'MLC')),
    saldo_disponible NUMERIC(18,2) NOT NULL DEFAULT 0,
    saldo_retenido NUMERIC(18,2) NOT NULL DEFAULT 0,
    saldo_total NUMERIC(18,2) NOT NULL GENERATED ALWAYS AS (saldo_disponible + saldo_retenido) STORED,
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (usuario_id, moneda)
);

-- ============================================================
-- 6) MOVIMIENTOS
-- El saldo no se escribe directamente desde frontend.
-- Los movimientos validados son la fuente de verdad del saldo.
-- ============================================================
CREATE TABLE IF NOT EXISTS movimientos (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL REFERENCES usuarios(id),
    tipo VARCHAR(40) NOT NULL
        CHECK (tipo IN ('aporte', 'retiro', 'ajuste', 'comision', 'rendimiento', 'reversion')),
    importe NUMERIC(18,2) NOT NULL,
    moneda CHAR(3) NOT NULL
        CHECK (moneda IN ('EUR', 'CUP', 'MLC')),
    referencia VARCHAR(255) NOT NULL,
    fecha TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    origen VARCHAR(40) NOT NULL
        CHECK (origen IN ('aportacion', 'retiro', 'ajuste', 'comision', 'rendimiento', 'reversion')),
    origen_id BIGINT,
    estado VARCHAR(30) NOT NULL DEFAULT 'applied'
        CHECK (estado IN ('pending', 'applied', 'reversed', 'rejected')),
    descripcion TEXT,
    creado_por_admin BIGINT REFERENCES usuarios(id),
    reversado_por BIGINT REFERENCES movimientos(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 7) VALIDACIONES ADMINISTRATIVAS
-- ============================================================
CREATE TABLE IF NOT EXISTS validaciones_admin (
    id BIGSERIAL PRIMARY KEY,
    entidad VARCHAR(40) NOT NULL
        CHECK (entidad IN ('aportacion', 'retiro', 'operacion', 'justificante', 'cuenta_bancaria')),
    entidad_id BIGINT NOT NULL,
    accion VARCHAR(40) NOT NULL
        CHECK (accion IN ('approved', 'rejected', 'request_information', 'processed', 'cancelled', 'updated')),
    admin_id BIGINT NOT NULL REFERENCES usuarios(id),
    comentario TEXT,
    motivo TEXT,
    fecha TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

-- ============================================================
-- 8) JUSTIFICANTES
-- Enlaza comprobantes/documentos a una aportación.
-- ============================================================
CREATE TABLE IF NOT EXISTS justificantes (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL REFERENCES usuarios(id),
    aportacion_id BIGINT REFERENCES aportaciones(id),
    documento_id BIGINT REFERENCES documentos(id),
    nombre_archivo VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100),
    peso_bytes BIGINT,
    estado_revision VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (estado_revision IN ('pending', 'approved', 'rejected')),
    fecha_subida TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    subido_por BIGINT NOT NULL REFERENCES usuarios(id),
    comentario TEXT
);

-- ============================================================
-- 9) AUDITORÍA ADMINISTRATIVA
-- ============================================================
CREATE TABLE IF NOT EXISTS auditoria_admin (
    id BIGSERIAL PRIMARY KEY,
    admin_id BIGINT NOT NULL REFERENCES usuarios(id),
    accion VARCHAR(80) NOT NULL,
    entidad VARCHAR(50) NOT NULL,
    entidad_id BIGINT NOT NULL,
    detalle JSONB NOT NULL DEFAULT '{}'::jsonb,
    ip_address INET,
    fecha TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 10) REFERIDOS (UN SOLO NIVEL)
-- ============================================================
CREATE TABLE IF NOT EXISTS referidos (
    id BIGSERIAL PRIMARY KEY,
    usuario_refiere_id BIGINT NOT NULL REFERENCES usuarios(id),
    usuario_referido_id BIGINT NOT NULL UNIQUE REFERENCES usuarios(id),
    estado VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (estado IN ('pending', 'active', 'cancelled', 'paid', 'rejected')),
    comision NUMERIC(18,2) NOT NULL DEFAULT 0,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_referido_distinto
        CHECK (usuario_refiere_id <> usuario_referido_id)
);

-- ============================================================
-- ÍNDICES IMPORTANTES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_aportaciones_usuario
    ON aportaciones(usuario_id);

CREATE INDEX IF NOT EXISTS idx_aportaciones_estado
    ON aportaciones(estado);

CREATE INDEX IF NOT EXISTS idx_aportaciones_moneda
    ON aportaciones(moneda);

CREATE INDEX IF NOT EXISTS idx_aportaciones_operacion
    ON aportaciones(operacion_id);

CREATE INDEX IF NOT EXISTS idx_aportaciones_fecha
    ON aportaciones(fecha_solicitud);

CREATE INDEX IF NOT EXISTS idx_retiros_usuario
    ON retiros(usuario_id);

CREATE INDEX IF NOT EXISTS idx_retiros_estado
    ON retiros(estado);

CREATE INDEX IF NOT EXISTS idx_retiros_moneda
    ON retiros(moneda);

CREATE INDEX IF NOT EXISTS idx_retiros_fecha
    ON retiros(fecha_solicitud);

CREATE UNIQUE INDEX IF NOT EXISTS idx_saldos_usuario_moneda_unique
    ON saldos_usuario_moneda(usuario_id, moneda);

CREATE INDEX IF NOT EXISTS idx_saldos_usuario
    ON saldos_usuario_moneda(usuario_id);

CREATE INDEX IF NOT EXISTS idx_movimientos_usuario
    ON movimientos(usuario_id);

CREATE INDEX IF NOT EXISTS idx_movimientos_tipo
    ON movimientos(tipo);

CREATE INDEX IF NOT EXISTS idx_movimientos_fecha
    ON movimientos(fecha);

CREATE INDEX IF NOT EXISTS idx_movimientos_origen
    ON movimientos(origen, origen_id);

CREATE INDEX IF NOT EXISTS idx_movimientos_estado
    ON movimientos(estado);

CREATE INDEX IF NOT EXISTS idx_validaciones_entidad
    ON validaciones_admin(entidad, entidad_id);

CREATE INDEX IF NOT EXISTS idx_validaciones_admin
    ON validaciones_admin(admin_id);

CREATE INDEX IF NOT EXISTS idx_validaciones_fecha
    ON validaciones_admin(fecha);

CREATE INDEX IF NOT EXISTS idx_justificantes_aportacion
    ON justificantes(aportacion_id);

CREATE INDEX IF NOT EXISTS idx_justificantes_usuario
    ON justificantes(usuario_id);

CREATE INDEX IF NOT EXISTS idx_justificantes_estado
    ON justificantes(estado_revision);

CREATE INDEX IF NOT EXISTS idx_auditoria_admin
    ON auditoria_admin(admin_id);

CREATE INDEX IF NOT EXISTS idx_auditoria_entidad
    ON auditoria_admin(entidad, entidad_id);

CREATE INDEX IF NOT EXISTS idx_auditoria_fecha
    ON auditoria_admin(fecha);

CREATE INDEX IF NOT EXISTS idx_referidos_refiere
    ON referidos(usuario_refiere_id);

CREATE INDEX IF NOT EXISTS idx_referidos_referido
    ON referidos(usuario_referido_id);

CREATE INDEX IF NOT EXISTS idx_referidos_estado
    ON referidos(estado);

COMMIT;
