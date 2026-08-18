# Documento definitivo de diseño financiero para revisión final

> Este documento es solo de revisión y aprobación. No se ejecuta SQL, no se modifica PostgreSQL, Supabase, Render ni ninguna base de datos real.

## 1. Estado

APROBADO PARA IMPLEMENTACIÓN — PENDIENTE DE EJECUCIÓN

No quedan decisiones pendientes. Las siguientes decisiones están cerradas y forman la base del diseño definitivo:

- usuarios será la identidad principal del sistema financiero.
- Las monedas iniciales serán EUR, CUP y MLC, con estructura preparada para ampliarse en el futuro.
- cuentas_bancarias será una entidad separada para las cuentas utilizadas en retiros.
- Los administradores utilizarán el mismo sistema de usuarios, con rol admin diferenciado y validación estricta en backend.
- Los archivos se almacenarán y reutilizarán mediante documentos, y justificantes será la entidad financiera que los vincula con las aportaciones.
- La auditoría cubrirá tanto decisiones administrativas como cambios internos relevantes realizados por el backend.
- Comisiones complejas no se implementan en esta primera fase, pero la arquitectura debe permitir añadirlas posteriormente.
- Ajustes y devoluciones quedan contemplados para una futura extensión.
- Se mantiene operaciones_comerciales como entidad funcional y no se crea una segunda tabla central duplicada.

Este diseño incorpora dichas decisiones definitivas y no contempla más preguntas abiertas.

---

## 2. Objetivo

Diseñar la capa financiera para una plataforma de operaciones comerciales e inversión con:

- integridad transaccional
- trazabilidad completa
- seguridad por roles
- control de concurrencia
- idempotencia
- validación de saldo y movimientos
- clara separación entre usuario normal, administrador y backend

La lógica financiera queda bajo control del backend y no puede ser manipulada por el frontend.

---

## 3. Principios de diseño

1. El saldo no se modifica directamente desde cliente.
2. Los movimientos son append-only y no se editan.
3. Cada operación oficial queda registrada con auditoría.
4. Toda actualización crítica se hace dentro de una transacción PostgreSQL.
5. Si falla cualquier paso, se ejecuta ROLLBACK.
6. El backend valida permisos, estado, duplicados y saldo disponible.
7. Cada operación sensible usa idempotency_key o request_id.
8. El usuario crea peticiones; el backend ejecuta la operación real.

---

## 4. Esquema final propuesto

### 4.1 usuarios

```sql
usuarios (
  id uuid primary key,
  email text unique not null,
  nombre text not null,
  apellidos text,
  telefono text,
  rol text not null default 'user' check (rol in ('user','admin','service_role')),
  activo boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
)
```

### 4.2 cuentas_bancarias

```sql
cuentas_bancarias (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete cascade,
  banco text not null,
  iban text,
  swift text,
  alias text,
  moneda text not null default 'EUR' check (moneda in ('EUR','CUP','MLC')),
  es_principal boolean not null default false,
  activa boolean not null default true,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(usuario_id, alias)
)
```

### 4.3 aportaciones

```sql
aportaciones (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete restrict,
  moneda text not null check (moneda in ('EUR','CUP','MLC')),
  importe numeric(18,2) not null check (importe > 0),
  metodo text not null,
  estado text not null default 'pending' check (estado in ('pending','approved','rejected','cancelled')),
  idempotency_key text not null unique,
  cuenta_id uuid references cuentas_bancarias(id),
  creado_por uuid references usuarios(id),
  aprobado_por uuid references usuarios(id),
  aprobado_en timestamptz,
  motivo_rechazo text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
)
```

### 4.4 justificantes

```sql
justificantes (
  id uuid primary key,
  aportacion_id uuid not null references aportaciones(id) on delete cascade,
  documento_id uuid not null references documentos(id) on delete restrict,
  tipo text not null,
  estado text not null default 'pending' check (estado in ('pending','validated','rejected')),
  observado text,
  validado_por uuid references usuarios(id),
  validado_en timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(aportacion_id, documento_id)
)
```

### 4.5 retiros

```sql
retiros (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete restrict,
  moneda text not null check (moneda in ('EUR','CUP','MLC')),
  importe numeric(18,2) not null check (importe > 0),
  estado text not null default 'pending' check (estado in ('pending','approved','rejected','cancelled','processing')),
  idempotency_key text not null unique,
  cuenta_id uuid references cuentas_bancarias(id),
  solicitado_por uuid references usuarios(id),
  aprobado_por uuid references usuarios(id),
  aprobado_en timestamptz,
  motivo_rechazo text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
)
```

### 4.6 saldos_usuario_moneda

```sql
saldos_usuario_moneda (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete cascade,
  moneda text not null check (moneda in ('EUR','CUP','MLC')),
  saldo numeric(18,2) not null default 0 check (saldo >= 0),
  version integer not null default 0,
  updated_at timestamptz not null default now(),
  unique(usuario_id, moneda)
)
```

### 4.7 movimientos

```sql
movimientos (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete restrict,
  tipo text not null check (tipo in ('APORTACION','RETIRO','AJUSTE','DEVOLUCION','COMISION')),
  moneda text not null check (moneda in ('EUR','CUP','MLC')),
  importe numeric(18,2) not null check (importe > 0),
  saldo_post numeric(18,2) not null,
  referencia text not null,
  operacion_id uuid not null,
  estado text not null default 'confirmed' check (estado in ('confirmed','pending','reversed')),
  created_by uuid references usuarios(id),
  created_at timestamptz not null default now(),
  unique(operacion_id, tipo)
)
```

### 4.8 documentos

```sql
documentos (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete cascade,
  nombre_original text not null,
  tipo_documento text not null,
  mime_type text,
  storage_path text not null,
  hash_archivo text,
  tamano_bytes bigint,
  estado text not null default 'uploaded' check (estado in ('uploaded','validated','rejected')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
)
```

### 4.9 auditoria_admin

```sql
auditoria_admin (
  id uuid primary key,
  tipo text not null,
  entity_id uuid not null,
  usuario_id uuid references usuarios(id),
  admin_id uuid references usuarios(id),
  accion text not null,
  detalles jsonb not null default '{}'::jsonb,
  idempotency_key text not null,
  created_at timestamptz not null default now(),
  unique(tipo, entity_id, idempotency_key)
)
```

> `idempotency_key` es obligatorio y no puede ser nulo. Esto permite que la restricción `UNIQUE(tipo, entity_id, idempotency_key)` impida duplicados reales en la auditoría. En la práctica, una operación financiera crítica debe generar una clave idempotente siempre.

### 4.10 validaciones_admin

```sql
validaciones_admin (
  id uuid primary key,
  entidad text not null check (entidad in ('aportacion','retiro','documento','justificante')),
  entidad_id uuid not null,
  admin_id uuid not null references usuarios(id),
  resultado text not null check (resultado in ('approved','rejected')),
  motivo text,
  created_at timestamptz not null default now()
)
```

### 4.11 operaciones_comerciales

```sql
operaciones_comerciales (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete restrict,
  tipo text not null,
  estado text not null default 'draft' check (estado in ('draft','active','completed','cancelled')),
  moneda text not null check (moneda in ('EUR','CUP','MLC')),
  importe_total numeric(18,2) not null default 0,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
)
```

> Esta tabla es funcional para el negocio, pero no sustituye a aportaciones ni retiros ni movimientos.

---

## 5. Relaciones y claves foráneas

- usuarios 1:N aportaciones
- usuarios 1:N retiros
- usuarios 1:N cuentas_bancarias
- usuarios 1:N saldos_usuario_moneda
- usuarios 1:N movimientos
- usuarios 1:N documentos
- aportaciones 1:N justificantes
- documentos 1:N justificantes
- usuarios 1:N auditoria_admin
- usuarios 1:N validaciones_admin
- usuarios 1:N operaciones_comerciales

### Foráneas clave

- `aportaciones.usuario_id -> usuarios.id`
- `aportaciones.cuenta_id -> cuentas_bancarias.id`
- `aportaciones.aprobado_por -> usuarios.id`
- `justificantes.aportacion_id -> aportaciones.id`
- `justificantes.documento_id -> documentos.id`
- `justificantes.validado_por -> usuarios.id`
- `retiros.usuario_id -> usuarios.id`
- `retiros.cuenta_id -> cuentas_bancarias.id`
- `retiros.aprobado_por -> usuarios.id`
- `cuentas_bancarias.usuario_id -> usuarios.id`
- `saldos_usuario_moneda.usuario_id -> usuarios.id`
- `movimientos.usuario_id -> usuarios.id`
- `documentos.usuario_id -> usuarios.id`
- `auditoria_admin.usuario_id -> usuarios.id`
- `auditoria_admin.admin_id -> usuarios.id`
- `validaciones_admin.admin_id -> usuarios.id`
- `operaciones_comerciales.usuario_id -> usuarios.id`

---

## 6. Constraints de integridad

### 6.1 Monedas

```sql
check (moneda in ('EUR','CUP','MLC'))
```

### 6.2 Importe positivo

```sql
check (importe > 0)
```

### 6.3 Saldo no negativo

```sql
check (saldo >= 0)
```

### 6.4 Estados válidos

- aportaciones: `pending | approved | rejected | cancelled`
- justificantes: `pending | validated | rejected`
- retiros: `pending | approved | rejected | cancelled | processing`
- movimientos: `confirmed | pending | reversed`
- documentos: `uploaded | validated | rejected`
- operaciones_comerciales: `draft | active | completed | cancelled`

### 6.5 Unique

- `aportaciones.idempotency_key` único
- `retiros.idempotency_key` único
- `cuentas_bancarias(usuario_id, alias)` único
- `saldos_usuario_moneda(usuario_id, moneda)` único
- `movimientos(operacion_id, tipo)` único
- `justificantes(aportacion_id, documento_id)` único
- `auditoria_admin(tipo, entity_id, idempotency_key)` único

### 6.6 Reglas de negocio

- Un usuario solo puede tener un saldo por moneda.
- Un retiro no puede superar el saldo disponible al aprobar.
- Una aportación aprobada no puede repetirse.
- Un retiro aprobado no puede procesarse dos veces.
- Un movimiento confirmado no debe editarse.
- Una cuenta bancaria debe estar activa para usarse en una operación financiera.

---

## 7. Índices recomendados

```sql
create index idx_aportaciones_usuario_estado on aportaciones(usuario_id, estado);
create index idx_aportaciones_estado_created on aportaciones(estado, created_at desc);
create index idx_justificantes_aportacion on justificantes(aportacion_id, estado);
create index idx_justificantes_documento on justificantes(documento_id);
create index idx_retiros_usuario_estado on retiros(usuario_id, estado);
create index idx_retiros_estado_created on retiros(estado, created_at desc);
create index idx_saldos_usuario_moneda on saldos_usuario_moneda(usuario_id, moneda);
create index idx_movimientos_usuario_fecha on movimientos(usuario_id, created_at desc);
create index idx_movimientos_operacion on movimientos(operacion_id, tipo);
create index idx_documentos_usuario on documentos(usuario_id, created_at desc);
create index idx_cuentas_bancarias_usuario on cuentas_bancarias(usuario_id, activa, moneda);
create index idx_auditoria_admin_entity on auditoria_admin(entity_id, tipo, created_at desc);
create index idx_validaciones_admin_entidad on validaciones_admin(entidad, entidad_id);
create index idx_operaciones_comerciales_usuario on operaciones_comerciales(usuario_id, estado);
```

---

## 8. Políticas RLS definitivas para Supabase

### 8.1 Helpers

```sql
create or replace function app.current_user_id()
returns uuid
language sql
stable
as $$
  select auth.uid();
$$;

create or replace function app.is_admin()
returns boolean
language sql
stable
as $$
  select coalesce((auth.jwt() ->> 'role') = 'admin', false);
$$;
```

### 8.2 usuarios

```sql
alter table usuarios enable row level security;

create policy "usuarios_select_own"
on usuarios
for select
using (id = app.current_user_id());

create policy "usuarios_update_own"
on usuarios
for update
using (id = app.current_user_id())
with check (id = app.current_user_id());

create policy "usuarios_admin_select_all"
on usuarios
for select
using (app.is_admin());
```

### 8.3 cuentas_bancarias

```sql
alter table cuentas_bancarias enable row level security;

create policy "cuentas_select_own"
on cuentas_bancarias
for select
using (usuario_id = app.current_user_id());

create policy "cuentas_insert_own"
on cuentas_bancarias
for insert
with check (usuario_id = app.current_user_id());

create policy "cuentas_update_own"
on cuentas_bancarias
for update
using (usuario_id = app.current_user_id())
with check (usuario_id = app.current_user_id());

create policy "cuentas_admin_select_all"
on cuentas_bancarias
for select
using (app.is_admin());
```

### 8.4 aportaciones

```sql
alter table aportaciones enable row level security;

create policy "aportaciones_select_own"
on aportaciones
for select
using (usuario_id = app.current_user_id());

create policy "aportaciones_insert_own_pending"
on aportaciones
for insert
with check (
  usuario_id = app.current_user_id()
  and estado = 'pending'
);

create policy "aportaciones_update_own_pending_only"
on aportaciones
for update
using (usuario_id = app.current_user_id())
with check (
  usuario_id = app.current_user_id()
  and estado in ('pending', 'rejected', 'cancelled')
);

create policy "aportaciones_admin_select_all"
on aportaciones
for select
using (app.is_admin());

create policy "aportaciones_admin_update_all"
on aportaciones
for update
using (app.is_admin())
with check (app.is_admin());
```

### 8.5 justificantes

```sql
alter table justificantes enable row level security;

create policy "justificantes_select_own"
on justificantes
for select
using (
  exists (
    select 1 from aportaciones a
    where a.id = aportacion_id and a.usuario_id = app.current_user_id()
  )
);

create policy "justificantes_insert_own"
on justificantes
for insert
with check (
  exists (
    select 1 from aportaciones a
    where a.id = aportacion_id and a.usuario_id = app.current_user_id()
  )
);

create policy "justificantes_admin_select_all"
on justificantes
for select
using (app.is_admin());
```

### 8.6 retiros

```sql
alter table retiros enable row level security;

create policy "retiros_select_own"
on retiros
for select
using (usuario_id = app.current_user_id());

create policy "retiros_insert_own_pending"
on retiros
for insert
with check (
  usuario_id = app.current_user_id()
  and estado = 'pending'
);

create policy "retiros_update_own_pending_only"
on retiros
for update
using (usuario_id = app.current_user_id())
with check (
  usuario_id = app.current_user_id()
  and estado in ('pending', 'rejected', 'cancelled')
);

create policy "retiros_admin_select_all"
on retiros
for select
using (app.is_admin());

create policy "retiros_admin_update_all"
on retiros
for update
using (app.is_admin())
with check (app.is_admin());
```

### 8.7 saldos_usuario_moneda

```sql
alter table saldos_usuario_moneda enable row level security;

create policy "saldo_select_own"
on saldos_usuario_moneda
for select
using (usuario_id = app.current_user_id());

create policy "saldo_admin_select_all"
on saldos_usuario_moneda
for select
using (app.is_admin());

create policy "saldo_no_client_write"
on saldos_usuario_moneda
for all
using (false)
with check (false);
```

### 8.8 movimientos

```sql
alter table movimientos enable row level security;

create policy "movimientos_select_own"
on movimientos
for select
using (usuario_id = app.current_user_id());

create policy "movimientos_admin_select_all"
on movimientos
for select
using (app.is_admin());

create policy "movimientos_no_client_write"
on movimientos
for all
using (false)
with check (false);
```

### 8.9 documentos

```sql
alter table documentos enable row level security;

create policy "documentos_select_own"
on documentos
for select
using (usuario_id = app.current_user_id());

create policy "documentos_insert_own"
on documentos
for insert
with check (usuario_id = app.current_user_id());

create policy "documentos_update_own"
on documentos
for update
using (usuario_id = app.current_user_id())
with check (usuario_id = app.current_user_id());

create policy "documentos_admin_select_all"
on documentos
for select
using (app.is_admin());
```

### 8.10 auditoria_admin

```sql
alter table auditoria_admin enable row level security;

create policy "auditoria_admin_select_all"
on auditoria_admin
for select
using (app.is_admin());

create policy "auditoria_no_client_write"
on auditoria_admin
for all
using (false)
with check (false);
```

### 8.11 validaciones_admin

```sql
alter table validaciones_admin enable row level security;

create policy "validaciones_admin_select_all"
on validaciones_admin
for select
using (app.is_admin());

create policy "validaciones_no_client_write"
on validaciones_admin
for all
using (false)
with check (false);
```

### 8.12 operaciones_comerciales

```sql
alter table operaciones_comerciales enable row level security;

create policy "operaciones_select_own"
on operaciones_comerciales
for select
using (usuario_id = app.current_user_id());

create policy "operaciones_insert_own"
on operaciones_comerciales
for insert
with check (usuario_id = app.current_user_id());

create policy "operaciones_admin_select_all"
on operaciones_comerciales
for select
using (app.is_admin());
```

---

## 9. Permisos por rol y tabla

### 9.1 Usuario autenticado

| Tabla | SELECT | INSERT | UPDATE | DELETE |
|---|---|---|---|---|
| usuarios | propio | no | propio | no |
| cuentas_bancarias | propio | propio | propio | no |
| aportaciones | propio | propio, solo pending | propio, solo pending/rejected/cancelled | no |
| justificantes | propio | propio | propio solo si pertenece a su aportación | no |
| retiros | propio | propio, solo pending | propio, solo pending/rejected/cancelled | no |
| saldos_usuario_moneda | propio | no | no | no |
| movimientos | propio | no | no | no |
| documentos | propio | propio | propio | no |
| auditoria_admin | no | no | no | no |
| validaciones_admin | no | no | no | no |
| operaciones_comerciales | propio | propio | propio solo para estados locales | no |

### 9.2 Administrador

| Tabla | SELECT | INSERT | UPDATE | DELETE |
|---|---|---|---|---|
| usuarios | todo | no | no | no |
| cuentas_bancarias | todo | no | no | no |
| aportaciones | todo | no | aprobar/rechazar | no |
| justificantes | todo | no | aprobar/rechazar | no |
| retiros | todo | no | aprobar/rechazar | no |
| saldos_usuario_moneda | todo | no | no | no |
| movimientos | todo | no | no | no |
| documentos | todo | no | no | no |
| auditoria_admin | todo | no | no | no |
| validaciones_admin | todo | no | no | no |
| operaciones_comerciales | todo | no | no | no |

### 9.3 Backend / service role

| Tabla | SELECT | INSERT | UPDATE | DELETE |
|---|---|---|---|---|
| usuarios | sí | sí | sí | limitado |
| cuentas_bancarias | sí | sí | sí | limitado |
| aportaciones | sí | sí | sí | no |
| justificantes | sí | sí | sí | no |
| retiros | sí | sí | sí | no |
| saldos_usuario_moneda | sí | sí | sí | no |
| movimientos | sí | sí | sí | no |
| documentos | sí | sí | sí | no |
| auditoria_admin | sí | sí | sí | no |
| validaciones_admin | sí | sí | sí | no |
| operaciones_comerciales | sí | sí | sí | no |

---

## 10. Seguridad para impedir que un usuario modifique su saldo o movimientos directamente

### Reglas obligatorias

1. `saldos_usuario_moneda` debe tener RLS deny all para cliente.
2. `movimientos` debe tener la misma restricción.
3. `auditoria_admin` debe ser de lectura para admin y sin escritura directa desde cliente.
4. La lógica de saldo se escribe estrictamente desde backend.
5. El frontend solo puede enviar solicitudes o intenciones.
6. La validación de disponibilidad se hace en backend.
7. La actualización del saldo y la creación del movimiento se hacen en la misma transacción.
8. La auditoría se genera desde backend con contexto real.

### SQL de bloqueo directo

```sql
create policy "saldo_no_client_write" on saldos_usuario_moneda for all using (false) with check (false);
create policy "movimientos_no_client_write" on movimientos for all using (false) with check (false);
create policy "auditoria_no_client_write" on auditoria_admin for all using (false) with check (false);
```

---

## 11. Flujo transaccional del backend

### 11.1 Creación de aportación

1. El usuario crea una aportación con `idempotency_key`.
2. Backend valida usuario activo, importe positivo, moneda válida y duplicados.
3. Se inserta la fila en `aportaciones` con `pending`.
4. Si hay justificante, se guarda en `documentos` y luego en `justificantes`.
5. Se registra la acción de creación en `auditoria_admin`.

### 11.2 Aprobación de aportación

1. Administrador revisa la operación.
2. Backend comprueba permisos y estado.
3. Bloquea la fila del saldo con `SELECT ... FOR UPDATE`.
4. Calcula el nuevo saldo.
5. Actualiza `saldos_usuario_moneda`.
6. Inserta movimiento de crédito.
7. Actualiza la aportación a `approved`.
8. Registra auditoría y commit final.

### 11.3 Solicitud de retiro

1. Usuario solicita retiro con `idempotency_key`.
2. Backend valida usuario, saldo disponible y moneda.
3. Inserta fila en `retiros` con `pending`.
4. Registra una auditoría de solicitud.

### 11.4 Aprobación de retiro

1. Administrador valida el retiro.
2. Backend valida permisos y estado.
3. Bloquea fila de saldo con `FOR UPDATE`.
4. Compara importe con saldo disponible.
5. Si es válido, descuenta el saldo.
6. Inserta movimiento de débito.
7. Actualiza retiro a `approved`.
8. Registra auditoría y commit final.

---

## 12. Idempotencia y concurrencia

### 12.1 Idempotencia

Cada operación crítica usa un `idempotency_key`:

- creación de aportación
- aprobación de aportación
- creación de retiro
- aprobación de retiro
- creación de movimiento
- auditoría

Reglas:

- misma clave repetida = mismo resultado o `already_processed`
- no se duplican movimientos
- no se duplica auditoría
- no se acepta doble aprobación de la misma operación

### 12.2 Control de concurrencia

```sql
select * from saldos_usuario_moneda
where usuario_id = $1 and moneda = $2
for update;
```

Esto bloquea la fila del saldo para evitar que dos procesos descuenten o acrediten simultáneamente sin control.

### 12.3 Regla crítica

Un retiro nunca puede dejar el saldo negativo. La comprobación y actualización deben hacerse dentro de la misma transacción.

---

## 13. Auditoría de decisiones y ajustes del backend

```sql
auditoria_admin (
  id uuid primary key,
  tipo text not null,
  entity_id uuid not null,
  usuario_id uuid references usuarios(id),
  admin_id uuid references usuarios(id),
  accion text not null,
  detalles jsonb not null default '{}'::jsonb,
  idempotency_key text,
  created_at timestamptz not null default now()
)
```

### Se audita

- aprobación/rechazo de aportaciones
- aprobación/rechazo de retiros
- validación de documentos y justificantes
- ajustes internos del backend
- cambios de saldo y movimientos
- referencia de operación
- saldo anterior y nuevo
- motivo del rechazo
- responsable y fecha

### Eventos sugeridos

- `APORTACION_CREADA`
- `APORTACION_APROBADA`
- `APORTACION_RECHAZADA`
- `JUSTIFICANTE_VALIDADO`
- `RETIRO_SOLICITADO`
- `RETIRO_APROBADO`
- `RETIRO_RECHAZADO`
- `SALDO_AJUSTADO`
- `MOVIMIENTO_GENERADO`

---

## 14. Pseudocódigo del backend

### 14.1 Aprobar una aportación

```python
async def aprobar_aportacion(aportacion_id: str, admin_id: str, idempotency_key: str):
    with db.transaction() as tx:
        ya = tx.query_one("""
            select id from auditoria_admin
            where tipo = 'APORTACION_APROBADA'
              and entity_id = %s
              and idempotency_key = %s
        """, [aportacion_id, idempotency_key])

        if ya:
            return {"status": "already_processed"}

        aportacion = tx.query_one("""
            select * from aportaciones where id = %s for update
        """, [aportacion_id])

        if not aportacion:
            raise ValueError('aportacion_no_existe')

        if aportacion.estado != 'pending':
            raise ValueError('aportacion_no_pendiente')

        admin = tx.query_one("select id, rol from usuarios where id = %s", [admin_id])
        if admin.rol != 'admin':
            raise PermissionError('no_autorizado')

        saldo = tx.query_one("""
            select * from saldos_usuario_moneda
            where usuario_id = %s and moneda = %s for update
        """, [aportacion.usuario_id, aportacion.moneda])

        if not saldo:
            tx.execute("""
                insert into saldos_usuario_moneda (id, usuario_id, moneda, saldo)
                values (gen_random_uuid(), %s, %s, 0)
            """, [aportacion.usuario_id, aportacion.moneda])
            saldo = tx.query_one("""
                select * from saldos_usuario_moneda
                where usuario_id = %s and moneda = %s for update
            """, [aportacion.usuario_id, aportacion.moneda])

        nuevo_saldo = saldo.saldo + aportacion.importe

        tx.execute("""
            update saldos_usuario_moneda
            set saldo = %s, updated_at = now(), version = version + 1
            where id = %s
        """, [nuevo_saldo, saldo.id])

        tx.execute("""
            insert into movimientos (id, usuario_id, tipo, moneda, importe, saldo_post, referencia, operacion_id, estado, created_by)
            values (gen_random_uuid(), %s, 'APORTACION', %s, %s, %s, %s, %s, 'confirmed', %s)
        """, [aportacion.usuario_id, aportacion.moneda, aportacion.importe, nuevo_saldo, aportacion.id, aportacion.id, admin_id])

        tx.execute("""
            update aportaciones
            set estado = 'approved', aprobado_por = %s, aprobado_en = now(), updated_at = now()
            where id = %s
        """, [admin_id, aportacion_id])

        tx.execute("""
            insert into auditoria_admin (id, tipo, entity_id, usuario_id, admin_id, accion, detalles, idempotency_key)
            values (gen_random_uuid(), 'APORTACION_APROBADA', %s, %s, %s, 'approve', %s, %s)
        """, [
            aportacion_id,
            aportacion.usuario_id,
            admin_id,
            {"importe": str(aportacion.importe), "moneda": aportacion.moneda, "saldo_anterior": str(saldo.saldo), "saldo_nuevo": str(nuevo_saldo)},
            idempotency_key
        ])

    return {"status": "approved"}
```

### 14.2 Aprobar un retiro

```python
async def aprobar_retiro(retiro_id: str, admin_id: str, idempotency_key: str):
    with db.transaction() as tx:
        ya = tx.query_one("""
            select id from auditoria_admin
            where tipo = 'RETIRO_APROBADO'
              and entity_id = %s
              and idempotency_key = %s
        """, [retiro_id, idempotency_key])

        if ya:
            return {"status": "already_processed"}

        retiro = tx.query_one("""
            select * from retiros where id = %s for update
        """, [retiro_id])

        if not retiro:
            raise ValueError('retiro_no_existe')

        if retiro.estado != 'pending':
            raise ValueError('retiro_no_pendiente')

        admin = tx.query_one("select id, rol from usuarios where id = %s", [admin_id])
        if admin.rol != 'admin':
            raise PermissionError('no_autorizado')

        saldo = tx.query_one("""
            select * from saldos_usuario_moneda
            where usuario_id = %s and moneda = %s for update
        """, [retiro.usuario_id, retiro.moneda])

        if not saldo:
            raise ValueError('saldo_no_existe')

        if saldo.saldo < retiro.importe:
            raise ValueError('saldo_insuficiente')

        nuevo_saldo = saldo.saldo - retiro.importe

        tx.execute("""
            update saldos_usuario_moneda
            set saldo = %s, updated_at = now(), version = version + 1
            where id = %s
        """, [nuevo_saldo, saldo.id])

        tx.execute("""
            insert into movimientos (id, usuario_id, tipo, moneda, importe, saldo_post, referencia, operacion_id, estado, created_by)
            values (gen_random_uuid(), %s, 'RETIRO', %s, %s, %s, %s, %s, 'confirmed', %s)
        """, [retiro.usuario_id, retiro.moneda, retiro.importe, nuevo_saldo, retiro.id, retiro.id, admin_id])

        tx.execute("""
            update retiros
            set estado = 'approved', aprobado_por = %s, aprobado_en = now(), updated_at = now()
            where id = %s
        """, [admin_id, retiro_id])

        tx.execute("""
            insert into auditoria_admin (id, tipo, entity_id, usuario_id, admin_id, accion, detalles, idempotency_key)
            values (gen_random_uuid(), 'RETIRO_APROBADO', %s, %s, %s, 'approve', %s, %s)
        """, [
            retiro_id,
            retiro.usuario_id,
            admin_id,
            {"importe": str(retiro.importe), "moneda": retiro.moneda, "saldo_anterior": str(saldo.saldo), "saldo_nuevo": str(nuevo_saldo)},
            idempotency_key
        ])

    return {"status": "approved"}
```

---

## 15. Implementación segura del backend

### Reglas obligatorias

1. Soportar autenticación con JWT o sesión válida.
2. El cliente no puede tocar directamente saldo ni movimientos.
3. El proxy de acceso debe estar respaldado por backend.
4. La validación se hace contra la base real.
5. Todo cambio financiero crítico usa transacción.
6. `SELECT ... FOR UPDATE` sobre la fila de saldo.
7. `ROLLBACK` si falla cualquiera de los pasos.
8. `COMMIT` solo al final.
9. Los movimientos y auditoría son inmutables desde cliente.
10. El backend debe ser la única capa que escribe saldos, movimientos y auditoría.

---

## 16. Orden recomendado de implementación futura

1. Revisar y aprobar este documento.
2. Confirmar compatibilidad entre usuarios actuales y autenticación del sistema.
3. Confirmar roles de admin y service role.
4. Revisar estructura de cuentas_bancarias y validación de cuentas autorizadas.
5. Revisar documentos y justificantes.
6. Preparar migración SQL de esquema final.
7. Preparar constraints, índices y RLS.
8. Preparar backend con transacciones y bloqueo de fila.
9. Preparar validación de idempotencia y concurrencia.
10. Preparar pruebas en entorno de prueba.
11. Ejecutar solo tras backup y verificación.
12. Desplegar en pruebas y luego en producción.

---

## 17. Checklist antes de producción

- [ ] Backup confirmado.
- [ ] Conexión PostgreSQL verificada.
- [ ] SSL verificado.
- [ ] Esquema actual revisado.
- [ ] RLS revisadas.
- [ ] Roles comprobados.
- [ ] Backend revisado.
- [ ] Pruebas realizadas en entorno de prueba.
- [ ] SQL revisado y aprobado.

---

## 18. Conclusión

Este documento define la base final para la capa financiera sin tocar ni ejecutar nada sobre la base real. Respeta las decisiones adoptadas:

- reutilización de usuarios y documentos
- cuentas_bancarias separadas
- auditoría financiera completa
- estructura granular sin duplicidad central
- seguridad por RLS y backend
- transacciones atómicas y control de saldo
- idempotencia y concurrencia
- preparación para futuras ampliaciones de comisiones, ajustes y devoluciones

No quedan preguntas pendientes. Este estado autoriza la preparación y revisión final de la implementación, pero no autoriza la ejecución sobre ninguna base real.

---

## 18. Checklist final antes de ejecución

- [ ] Esquema revisado.
- [ ] Relaciones revisadas.
- [ ] Constraints revisados.
- [ ] Índices revisados.
- [ ] RLS revisadas.
- [ ] Roles revisados.
- [ ] Backend y transacciones revisados.
- [ ] Idempotencia revisada.
- [ ] Concurrencia revisada.
- [ ] Auditoría revisada.
- [ ] Usuarios existentes protegidos.
- [ ] Tablas existentes que no deben modificarse claramente identificadas.
- [ ] Orden exacto de ejecución del SQL.
- [ ] Procedimiento de rollback.
- [ ] Backup obligatorio antes de ejecutar.
- [ ] Verificación de conexión SSL antes de ejecutar.
- [ ] Pruebas posteriores a la implementación.

---

## 19. Orden exacto de ejecución del SQL (solo cuando se autorice la ejecución)

1. Hacer backup completo y verificable de la base actual.
2. Verificar conexión SSL y endpoint PostgreSQL/Render/Supabase.
3. Revisar la estructura actual de usuarios, documentos, notificaciones, etc., para confirmar compatibilidad.
4. Ejecutar la creación de nuevas tablas financieras en orden de dependencia.
5. Crear índices y constraints.
6. Aplicar políticas RLS.
7. Validar permisos de roles.
8. Ejecutar pruebas de integración con datos de prueba y sin tocar producción real.
9. Solo entonces preparar despliegue final en entorno autorizado.

---

## 20. Procedimiento de rollback

1. Detener cualquier despliegue o proceso relacionado con la implementación financiera.
2. Revisar el histórico de migración y confirmar qué objetos se crearon en esta fase.
3. Eliminar únicamente los objetos financieros nuevos, si la operación no se ha validado aún.
4. Restablecer la base bajo backup si se detecta riesgo funcional o de integridad.
5. Invalidar cualquier cambio parcial que pudiera dejar tablas sin dependencias.

> Este procedimiento es de recuperación y no se ejecuta mientras el diseño no esté formalmente autorizado.

---

## 21. Recomendación final

El diseño financiero queda aprobado para pasar a la fase de implementación, pero no se autoriza la ejecución sobre la base real ni sobre PostgreSQL/Supabase/Render. La fase siguiente es la preparación técnica final de cada script SQL y la validación previa a la ejecución, con backup y SSL verificados antes de cualquier comando real.

---

Fin del documento de aprobación final.
