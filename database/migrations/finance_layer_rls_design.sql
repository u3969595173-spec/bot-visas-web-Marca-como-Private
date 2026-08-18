-- ============================================================
-- CAPA DE SEGURIDAD Y PERMISOS: RLS / POLÍTICAS DE ACCESO
-- Proyecto: BotVisasEstudio / Capital Trade Iberia
-- Objetivo: definir un diseño de permisos para la capa financiera
-- antes de ejecutar nada en PostgreSQL o Supabase.
--
-- REGLAS IMPORTANTES:
-- - NO ejecutar este SQL todavía.
-- - NO tocar PostgreSQL real.
-- - Solo es un archivo de diseño/revisión.
-- - Usuario no autenticado nunca tiene acceso.
-- - Usuario normal solo ve/modifica sus datos.
-- - Admin puede gestionar todas las filas relevantes.
-- - Backend/service role es la única capa para actualizar saldo y movimientos.
-- - auditoria_admin es de solo lectura para usuarios normales y de escritura solo para backend/admin.
-- ============================================================

-- ============================================================
-- 0) FUNCIONES AUXILIARES PARA POLÍTICAS
-- ============================================================
-- Estas funciones no se ejecutan aquí; son un diseño para revisar.
-- Deben implementarse en el backend o en la base si se usa Supabase.

-- Función auxiliar para obtener el id del usuario autenticado.
-- En Supabase suele resolverse con auth.uid() y una relación con usuarios.id.
-- Si el proyecto usa una columna auth_user_id, se recomienda usar esa referencia.
CREATE OR REPLACE FUNCTION public.current_app_user_id()
RETURNS BIGINT
LANGUAGE sql
STABLE
AS $$
    SELECT id
    FROM public.usuarios
    WHERE id = (SELECT current_setting('request.jwt.claims', true)::jsonb ->> 'sub')::bigint
    LIMIT 1;
$$;

-- Función para comprobar si el usuario actual es administrador.
CREATE OR REPLACE FUNCTION public.is_app_admin()
RETURNS BOOLEAN
LANGUAGE sql
STABLE
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM public.usuarios u
        WHERE u.id = (SELECT current_setting('request.jwt.claims', true)::jsonb ->> 'sub')::bigint
          AND u.rol = 'admin'
    );
$$;

-- Función para comprobar si el current user es el propietario de la fila.
CREATE OR REPLACE FUNCTION public.is_owner_of_row(p_usuario_id BIGINT)
RETURNS BOOLEAN
LANGUAGE sql
STABLE
AS $$
    SELECT p_usuario_id = (
        SELECT id
        FROM public.usuarios
        WHERE id = (SELECT current_setting('request.jwt.claims', true)::jsonb ->> 'sub')::bigint
    );
$$;

-- Función para bloquear cualquier escritura directa sobre saldo por usuario.
-- El saldo debe actualizarse vía backend/service role y no desde una política
-- de usuario normal, ni desde un UPDATE directo del frontend.
CREATE OR REPLACE FUNCTION public.can_modify_balance()
RETURNS BOOLEAN
LANGUAGE sql
STABLE
AS $$
    SELECT public.is_app_admin()
$$;

-- Función para comprobar que una operación financiera se hace con el usuario autenticado.
CREATE OR REPLACE FUNCTION public.same_user_or_admin(p_usuario_id BIGINT)
RETURNS BOOLEAN
LANGUAGE sql
STABLE
AS $$
    SELECT public.is_app_admin() OR public.is_owner_of_row(p_usuario_id);
$$;

-- ============================================================
-- 1) RLS PARA usuarios
-- ============================================================
-- Nota: esta es una tabla existente y no debe tocarse en esta fase.
-- Solo se define el patrón recomendado para que el sistema no exponga
-- otros perfiles ajenos.
--
-- Regla de seguridad:
-- - usuario normal solo puede ver su propia fila
-- - administrador puede ver todos
-- - el frontend nunca debe poder modificar el rol desde la app
--
-- POLÍTICAS RECOMENDADAS:
-- SELECT: usuario puede ver su propia fila; admin todos
-- INSERT: solo backend/admin en creación de usuarios
-- UPDATE: solo admin o propio perfil con campos limitados
-- DELETE: ninguno

-- ============================================================
-- 2) RLS PARA operaciones_comerciales
-- ============================================================
-- Seguridad:
-- - Operaciones públicas/activas pueden ser visibles para usuarios normales.
-- - La edición de negocio queda administrada.

ALTER TABLE public.operaciones_comerciales ENABLE ROW LEVEL SECURITY;

-- Usuario normal puede ver solo operaciones publicadas/activas.
CREATE POLICY operaciones_publicas_select
ON public.operaciones_comerciales
FOR SELECT
USING (
    estado IN ('published', 'active')
);

-- Usuario normal no puede crear ni editar operaciones.
CREATE POLICY operaciones_user_no_write
ON public.operaciones_comerciales
FOR INSERT
WITH CHECK (FALSE);

CREATE POLICY operaciones_user_no_update
ON public.operaciones_comerciales
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

CREATE POLICY operaciones_user_no_delete
ON public.operaciones_comerciales
FOR DELETE
USING (FALSE);

-- Administrador puede gestionar todas las operaciones.
CREATE POLICY operaciones_admin_full
ON public.operaciones_comerciales
FOR ALL
USING (public.is_app_admin())
WITH CHECK (public.is_app_admin());

-- ============================================================
-- 3) RLS PARA cuentas_bancarias
-- ============================================================
-- Seguridad:
-- - La información bancaria es sensible.
-- - Solo admin debe verla o administrar.
-- - Usuario normal no ve cuentas ni su información interna.

ALTER TABLE public.cuentas_bancarias ENABLE ROW LEVEL SECURITY;

CREATE POLICY cuentas_user_no_access
ON public.cuentas_bancarias
FOR SELECT
USING (FALSE);

CREATE POLICY cuentas_user_no_write
ON public.cuentas_bancarias
FOR INSERT
WITH CHECK (FALSE);

CREATE POLICY cuentas_user_no_update
ON public.cuentas_bancarias
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

CREATE POLICY cuentas_user_no_delete
ON public.cuentas_bancarias
FOR DELETE
USING (FALSE);

CREATE POLICY cuentas_admin_full
ON public.cuentas_bancarias
FOR ALL
USING (public.is_app_admin())
WITH CHECK (public.is_app_admin());

-- ============================================================
-- 4) RLS PARA aportaciones
-- ============================================================
-- Seguridad:
-- - Usuario normal solo ve sus propias aportaciones.
-- - No puede modificar el estado ni el importe una vez creada.
-- - El admin valida la aportación.

ALTER TABLE public.aportaciones ENABLE ROW LEVEL SECURITY;

-- Usuario normal: solo sus aportaciones.
CREATE POLICY aportaciones_user_select
ON public.aportaciones
FOR SELECT
USING (public.is_owner_of_row(usuario_id));

-- Usuario normal puede crear una aportación solo con su propio usuario_id.
CREATE POLICY aportaciones_user_insert
ON public.aportaciones
FOR INSERT
WITH CHECK (
    public.is_owner_of_row(usuario_id)
    AND estado IN ('pending', 'information_requested')
);

-- Usuario normal no puede editar el importe, moneda ni validación.
CREATE POLICY aportaciones_user_no_update
ON public.aportaciones
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

-- No se permite borrar aportaciones del usuario.
CREATE POLICY aportaciones_user_no_delete
ON public.aportaciones
FOR DELETE
USING (FALSE);

-- Administrador puede gestionar todas las aportaciones.
CREATE POLICY aportaciones_admin_full
ON public.aportaciones
FOR ALL
USING (public.is_app_admin())
WITH CHECK (public.is_app_admin());

-- ============================================================
-- 5) RLS PARA retiros
-- ============================================================
-- Seguridad:
-- - Usuario normal solo ve sus retiros.
-- - Solo puede crear el suyo y no puede aprobarse de forma directa.
-- - El admin valida y procesa.

ALTER TABLE public.retiros ENABLE ROW LEVEL SECURITY;

CREATE POLICY retiros_user_select
ON public.retiros
FOR SELECT
USING (public.is_owner_of_row(usuario_id));

CREATE POLICY retiros_user_insert
ON public.retiros
FOR INSERT
WITH CHECK (
    public.is_owner_of_row(usuario_id)
    AND estado = 'pending'
);

-- Usuario no puede aprobar ni procesar su retiro por sí mismo.
CREATE POLICY retiros_user_no_update
ON public.retiros
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

CREATE POLICY retiros_user_no_delete
ON public.retiros
FOR DELETE
USING (FALSE);

CREATE POLICY retiros_admin_full
ON public.retiros
FOR ALL
USING (public.is_app_admin())
WITH CHECK (public.is_app_admin());

-- ============================================================
-- 6) RLS PARA saldos_usuario_moneda
-- ============================================================
-- Seguridad:
-- - El saldo no debe poder escribirse desde el frontend.
-- - Usuario normal solo puede leer su propio saldo.
-- - Solo backend/service role o admin con control puede modificar.

ALTER TABLE public.saldos_usuario_moneda ENABLE ROW LEVEL SECURITY;

CREATE POLICY saldos_user_select
ON public.saldos_usuario_moneda
FOR SELECT
USING (public.is_owner_of_row(usuario_id));

CREATE POLICY saldos_user_no_insert
ON public.saldos_usuario_moneda
FOR INSERT
WITH CHECK (FALSE);

CREATE POLICY saldos_user_no_update
ON public.saldos_usuario_moneda
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

CREATE POLICY saldos_user_no_delete
ON public.saldos_usuario_moneda
FOR DELETE
USING (FALSE);

-- Admin puede leer y solo el backend/service role debería escribir.
CREATE POLICY saldos_admin_read
ON public.saldos_usuario_moneda
FOR SELECT
USING (public.is_app_admin());

CREATE POLICY saldos_admin_no_direct_write
ON public.saldos_usuario_moneda
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

-- Recomendación: la escritura real debe ser por backend/service role.
-- No permitir escritura directa desde admin en la app, salvo una operación
-- muy controlada de corrección y con auditoría.

-- ============================================================
-- 7) RLS PARA movimientos
-- ============================================================
-- Seguridad:
-- - El historial financiero es inmutable.
-- - Usuario normal solo puede leer los suyos.
-- - Backend/service role debe ser la única escritura posible.

ALTER TABLE public.movimientos ENABLE ROW LEVEL SECURITY;

CREATE POLICY movimientos_user_select
ON public.movimientos
FOR SELECT
USING (public.is_owner_of_row(usuario_id));

CREATE POLICY movimientos_user_no_insert
ON public.movimientos
FOR INSERT
WITH CHECK (FALSE);

CREATE POLICY movimientos_user_no_update
ON public.movimientos
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

CREATE POLICY movimientos_user_no_delete
ON public.movimientos
FOR DELETE
USING (FALSE);

CREATE POLICY movimientos_admin_read
ON public.movimientos
FOR SELECT
USING (public.is_app_admin());

CREATE POLICY movimientos_admin_no_direct_write
ON public.movimientos
FOR INSERT
WITH CHECK (FALSE);

CREATE POLICY movimientos_admin_no_direct_update
ON public.movimientos
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

-- ============================================================
-- 8) RLS PARA validaciones_admin
-- ============================================================
-- Seguridad:
-- - El usuario normal no ve validaciones ajenas.
-- - La validación es responsabilidad del admin.

ALTER TABLE public.validaciones_admin ENABLE ROW LEVEL SECURITY;

CREATE POLICY validaciones_user_no_access
ON public.validaciones_admin
FOR SELECT
USING (FALSE);

CREATE POLICY validaciones_user_no_write
ON public.validaciones_admin
FOR INSERT
WITH CHECK (FALSE);

CREATE POLICY validaciones_user_no_update
ON public.validaciones_admin
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

CREATE POLICY validaciones_user_no_delete
ON public.validaciones_admin
FOR DELETE
USING (FALSE);

CREATE POLICY validaciones_admin_full
ON public.validaciones_admin
FOR ALL
USING (public.is_app_admin())
WITH CHECK (public.is_app_admin());

-- ============================================================
-- 9) RLS PARA justificantes
-- ============================================================
-- Seguridad:
-- - Usuario normal solo ve sus justificantes.
-- - Admin revisa y aprueba.

ALTER TABLE public.justificantes ENABLE ROW LEVEL SECURITY;

CREATE POLICY justificantes_user_select
ON public.justificantes
FOR SELECT
USING (public.is_owner_of_row(usuario_id));

CREATE POLICY justificantes_user_insert
ON public.justificantes
FOR INSERT
WITH CHECK (
    public.is_owner_of_row(usuario_id)
    AND subido_por = current_setting('request.jwt.claims', true)::jsonb ->> 'sub'
);

CREATE POLICY justificantes_user_no_update
ON public.justificantes
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

CREATE POLICY justificantes_user_no_delete
ON public.justificantes
FOR DELETE
USING (FALSE);

CREATE POLICY justificantes_admin_full
ON public.justificantes
FOR ALL
USING (public.is_app_admin())
WITH CHECK (public.is_app_admin());

-- ============================================================
-- 10) RLS PARA auditoria_admin
-- ============================================================
-- Seguridad:
-- - Nunca debe ser modificable por usuario normal.
-- - Solo admin y backend deben tener acceso.

ALTER TABLE public.auditoria_admin ENABLE ROW LEVEL SECURITY;

CREATE POLICY auditoria_user_no_access
ON public.auditoria_admin
FOR SELECT
USING (FALSE);

CREATE POLICY auditoria_user_no_write
ON public.auditoria_admin
FOR INSERT
WITH CHECK (FALSE);

CREATE POLICY auditoria_user_no_update
ON public.auditoria_admin
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

CREATE POLICY auditoria_user_no_delete
ON public.auditoria_admin
FOR DELETE
USING (FALSE);

CREATE POLICY auditoria_admin_full
ON public.auditoria_admin
FOR ALL
USING (public.is_app_admin())
WITH CHECK (public.is_app_admin());

-- ============================================================
-- 11) RLS PARA referidos
-- ============================================================
-- Seguridad:
-- - Usuario normal solo ve las relaciones en las que participa.
-- - No puede alterarlas arbitrariamente.

ALTER TABLE public.referidos ENABLE ROW LEVEL SECURITY;

CREATE POLICY referidos_user_select
ON public.referidos
FOR SELECT
USING (
    usuario_refiere_id = (
        SELECT id
        FROM public.usuarios
        WHERE id = (SELECT current_setting('request.jwt.claims', true)::jsonb ->> 'sub')::bigint
    )
    OR usuario_referido_id = (
        SELECT id
        FROM public.usuarios
        WHERE id = (SELECT current_setting('request.jwt.claims', true)::jsonb ->> 'sub')::bigint
    )
);

CREATE POLICY referidos_user_insert
ON public.referidos
FOR INSERT
WITH CHECK (
    usuario_refiere_id = (
        SELECT id
        FROM public.usuarios
        WHERE id = (SELECT current_setting('request.jwt.claims', true)::jsonb ->> 'sub')::bigint
    )
);

CREATE POLICY referidos_user_no_update
ON public.referidos
FOR UPDATE
USING (FALSE)
WITH CHECK (FALSE);

CREATE POLICY referidos_user_no_delete
ON public.referidos
FOR DELETE
USING (FALSE);

CREATE POLICY referidos_admin_full
ON public.referidos
FOR ALL
USING (public.is_app_admin())
WITH CHECK (public.is_app_admin());

-- ============================================================
-- 12) REGLAS DE SEGURIDAD GLOBALES
-- ============================================================
-- IMPORTANTE:
-- - No se debe permitir que una sesión de usuario normal ejecute UPDATE/INSERT sobre saldos, movimientos o auditoria.
-- - El backend debe estar en un rol de servicio y debe ser la única capa que actualiza el saldo.
-- - La lógica del saldo debe ser derivada de movimientos validados.
-- - La validación administrativa debe quedar registrada en validaciones_admin y auditoria_admin.

-- ============================================================
-- 13) RESUMEN DE PERMISOS POR TABLA
-- ============================================================
-- Tabla                        | Usuario normal               | Administrador               | Backend/service role
-- -----------------------------+------------------------------+-----------------------------+----------------------------------------
-- operaciones_comerciales       | SELECT public/active         | ALL                        | ALL
-- cuentas_bancarias            | NONE                         | ALL                        | ALL
-- aportaciones                 | SELECT own / INSERT own      | ALL                        | ALL
-- retiros                      | SELECT own / INSERT own      | ALL                        | ALL
-- saldos_usuario_moneda        | SELECT own                  | SELECT / restricted        | FULL write
-- movimientos                  | SELECT own                  | SELECT                     | FULL write
-- validaciones_admin           | NONE                        | ALL                        | ALL
-- justificantes               | SELECT own / INSERT own      | ALL                        | ALL
-- auditoria_admin              | NONE                        | SELECT / controlled write  | FULL write
-- referidos                    | SELECT own / INSERT own      | ALL                        | ALL

-- ============================================================
-- 14) RECOMENDACIONES DE NEGOCIO / BACKEND
-- ============================================================
-- 1. El frontend nunca debe permitir editar saldo, movimientos, auditoria ni validaciones.
-- 2. Debe existir una capa backend que haga:
--    - validación de moneda
--    - validación de usuario
--    - comprobación de importe
--    - transacción
--    - inserción de movimiento
--    - actualización de saldo
--    - registro de validaciones_admin
--    - registro de auditoria_admin
-- 3. Si un usuario quiere cancelar una aportación válida, la solución es crear una validación o un movimiento de reversión, no editar los datos originales.
-- 4. Los movimientos deben ser inmutables por el usuario.
-- 5. Los justificantes deben ser privados y solo legibles por el propietario y admin.
-- 6. La capa admin debe manejar la revisión, aprobación y rechazo de aportaciones, retiros y justificantes.

-- ============================================================
-- FIN DEL ARCHIVO DE DISEÑO
-- ============================================================
