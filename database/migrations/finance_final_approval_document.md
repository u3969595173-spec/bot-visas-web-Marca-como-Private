# Documento final de diseño financiero para revisión y aprobación

> Este documento es de carácter exclusivo de revisión. No se ejecuta SQL, no se modifica PostgreSQL, Supabase, Render ni ninguna base de datos real.

## 1. Objetivo

Diseñar la capa financiera para una plataforma de operaciones comerciales e inversión, manteniendo:

- integridad transaccional
- trazabilidad completa
- seguridad por roles
- control de concurrencia
- idempotencia
- reglas estrictas de saldo y movimientos
- separación clara entre usuario normal, administrador y backend

La capa financiera debe quedar bajo control del backend y no debe ser modificable directamente desde el frontend.

---

## 2. Principios de diseño

1. El saldo no se edita directamente desde un cliente.
2. Los movimientos son append-only y no se modifican.
3. Cada aprobación/rechazo queda registrada con auditoría.
4. Todo cambio financiero crítico se hace dentro de una transacción PostgreSQL.
5. Si falla cualquier paso, se ejecuta ROLLBACK.
6. El backend valida permisos, estado, duplicidades y saldo disponible.
7. Cada operación relevante usa idempotency key o request_id.
8. El usuario solo puede crear peticiones; el backend ejecuta la operación real.

---

## 3. Esquema final propuesto: 10 tablas financieras

### 3.1 Tabla 1: usuarios

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

### 3.2 Tabla 2: cuentas_usuario

```sql
cuentas_usuario (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete cascade,
  iban text,
  banco text,
  swift text,
  moneda text not null check (moneda in ('EUR','CUP','MLC')),
  es_principal boolean not null default false,
  activo boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(usuario_id, moneda, es_principal)
)
```

### 3.3 Tabla 3: aportaciones

```sql
aportaciones (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete restrict,
  moneda text not null check (moneda in ('EUR','CUP','MLC')),
  importe numeric(18,2) not null check (importe > 0),
  metodo text not null,
  estado text not null default 'pending' check (estado in ('pending','approved','rejected','cancelled')),
  idempotency_key text not null unique,
  justificante_id uuid,
  creado_por uuid references usuarios(id),
  aprobado_por uuid references usuarios(id),
  aprobado_en timestamptz,
  motivo_rechazo text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
)
```

### 3.4 Tabla 4: retiros

```sql
retiros (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete restrict,
  moneda text not null check (moneda in ('EUR','CUP','MLC')),
  importe numeric(18,2) not null check (importe > 0),
  estado text not null default 'pending' check (estado in ('pending','approved','rejected','cancelled','processing')),
  idempotency_key text not null unique,
  cuenta_id uuid references cuentas_usuario(id),
  solicitado_por uuid references usuarios(id),
  aprobado_por uuid references usuarios(id),
  aprobado_en timestamptz,
  motivo_rechazo text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
)
```

### 3.5 Tabla 5: saldos_usuario_moneda

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

### 3.6 Tabla 6: movimientos

```sql
movimientos (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete restrict,
  tipo text not null check (tipo in ('APORTACION','RETIRO','COMISION','AJUSTE','DEVOLUCION')),
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

### 3.7 Tabla 7: documentos

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
  status text not null default 'uploaded' check (status in ('uploaded','validated','rejected')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
)
```

### 3.8 Tabla 8: auditoria_admin

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
  created_at timestamptz not null default now(),
  unique(tipo, entity_id, idempotency_key)
)
```

### 3.9 Tabla 9: validaciones_admin

```sql
validaciones_admin (
  id uuid primary key,
  entidad text not null check (entidad in ('aportacion','retiro','documento')),
  entidad_id uuid not null,
  admin_id uuid not null references usuarios(id),
  resultado text not null check (resultado in ('approved','rejected')),
  motivo text,
  created_at timestamptz not null default now()
)
```

### 3.10 Tabla 10: operaciones_financieras

```sql
operaciones_financieras (
  id uuid primary key,
  usuario_id uuid not null references usuarios(id) on delete restrict,
  tipo text not null check (tipo in ('aportacion','retiro','comision','ajuste')),
  moneda text not null check (moneda in ('EUR','CUP','MLC')),
  importe numeric(18,2) not null,
  estado text not null default 'pending' check (estado in ('pending','approved','rejected','cancelled','processing')),
  idempotency_key text not null unique,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
)
```

---

## 4. Relaciones y claves foráneas

### Relaciones principales

- usuarios 1:N aportaciones
- usuarios 1:N retiros
- usuarios 1:N cuentas_usuario
- usuarios 1:N saldos_usuario_moneda
- usuarios 1:N movimientos
- usuarios 1:N documentos
- usuarios 1:N auditoria_admin
- usuarios 1:N validaciones_admin
- usuarios 1:N operaciones_financieras

### Claves foráneas relevantes

- `aportaciones.usuario_id -> usuarios.id`
- `aportaciones.aprobado_por -> usuarios.id`
- `retiros.usuario_id -> usuarios.id`
- `retiros.cuenta_id -> cuentas_usuario.id`
- `retiros.aprobado_por -> usuarios.id`
- `cuentas_usuario.usuario_id -> usuarios.id`
- `saldos_usuario_moneda.usuario_id -> usuarios.id`
- `movimientos.usuario_id -> usuarios.id`
- `documentos.usuario_id -> usuarios.id`
- `auditoria_admin.usuario_id -> usuarios.id`
- `auditoria_admin.admin_id -> usuarios.id`
- `validaciones_admin.admin_id -> usuarios.id`
- `operaciones_financieras.usuario_id -> usuarios.id`

---

## 5. Constraints necesarios para integridad

### 5.1 Constraints de moneda

```sql
check (moneda in ('EUR','CUP','MLC'))
```

### 5.2 Constraints de importe

```sql
check (importe > 0)
```

### 5.3 Constraints de saldo no negativo

```sql
check (saldo >= 0)
```

### 5.4 Constraints de estados

- aportaciones: `pending | approved | rejected | cancelled`
- retiros: `pending | approved | rejected | cancelled | processing`
- movimientos: `confirmed | pending | reversed`
- documentos: `uploaded | validated | rejected`

### 5.5 Unique constraints

- `idempotency_key` único en aportaciones
- `idempotency_key` único en retiros
- `idempotency_key` único en operaciones_financieras
- `unique(usuario_id, moneda)` en saldos_usuario_moneda
- `unique(operacion_id, tipo)` en movimientos
- `unique(tipo, entity_id, idempotency_key)` en auditoria_admin

### 5.6 Constraints de negocio extra recomendados

- Un usuario solo puede tener un saldo por moneda.
- Un retiro no puede tener importe mayor que el saldo disponible al aprobar.
- Una aportación aprobada no puede volver a aprobarse.
- Un retiro aprobado no puede procesarse dos veces.
- Un usuario no puede editar un movimiento ya confirmado.

---

## 6. Índices necesarios para rendimiento y consultas

### Índices básicos

```sql
create index idx_aportaciones_usuario_estado on aportaciones(usuario_id, estado);
create index idx_aportaciones_estado_created on aportaciones(estado, created_at desc);
create index idx_retiros_usuario_estado on retiros(usuario_id, estado);
create index idx_retiros_estado_created on retiros(estado, created_at desc);
create index idx_saldos_usuario_moneda on saldos_usuario_moneda(usuario_id, moneda);
create index idx_movimientos_usuario_fecha on movimientos(usuario_id, created_at desc);
create index idx_movimientos_operacion on movimientos(operacion_id, tipo);
create index idx_documentos_usuario on documentos(usuario_id, created_at desc);
create index idx_auditoria_admin_entity on auditoria_admin(entity_id, tipo, created_at desc);
create index idx_validaciones_admin_entidad on validaciones_admin(entidad, entidad_id);
create index idx_operaciones_financieras_usuario_estado on operaciones_financieras(usuario_id, estado);
```

### Índices recomendados para consultas admin

```sql
create index idx_aportaciones_admin_review on aportaciones(estado, created_at desc);
create index idx_retiros_admin_review on retiros(estado, created_at desc);
create index idx_auditoria_admin_admin_date on auditoria_admin(admin_id, created_at desc);
```

---

## 7. Políticas RLS definitivas para Supabase

> La intención es que el cliente nunca pueda escribir saldo ni movimientos, y que el backend sea la única capa escrita para la lógica financiera.

### 7.1 Helpers

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

### 7.2 usuarios

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

### 7.3 aportaciones

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

### 7.4 retiros

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

### 7.5 saldos_usuario_moneda

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

### 7.6 movimientos

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

### 7.7 documentos

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

### 7.8 auditoria_admin

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

### 7.9 validaciones_admin

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

### 7.10 operaciones_financieras

```sql
alter table operaciones_financieras enable row level security;

create policy "operaciones_select_own"
on operaciones_financieras
for select
using (usuario_id = app.current_user_id());

create policy "operaciones_insert_own_pending"
on operaciones_financieras
for insert
with check (
  usuario_id = app.current_user_id()
  and estado = 'pending'
);

create policy "operaciones_admin_select_all"
on operaciones_financieras
for select
using (app.is_admin());

create policy "operaciones_no_client_write"
on operaciones_financieras
for all
using (false)
with check (false);
```

---

## 8. Permisos de SELECT, INSERT, UPDATE y DELETE por tabla y por rol

### 8.1 Usuario autenticado

| Tabla | SELECT | INSERT | UPDATE | DELETE |
|---|---|---|---|---|
| usuarios | propio | no | propio | no |
| cuentas_usuario | propio | propio | propio | no |
| aportaciones | propio | propio, solo pending | propio, solo pending/rejected/cancelled | no |
| retiros | propio | propio, solo pending | propio, solo pending/rejected/cancelled | no |
| saldos_usuario_moneda | propio | no | no | no |
| movimientos | propio | no | no | no |
| documentos | propio | propio | propio | no |
| auditoria_admin | no | no | no | no |
| validaciones_admin | no | no | no | no |
| operaciones_financieras | propio | propio, solo pending | no | no |

### 8.2 Administrador

| Tabla | SELECT | INSERT | UPDATE | DELETE |
|---|---|---|---|---|
| usuarios | todo | no | no | no |
| cuentas_usuario | todo | no | no | no |
| aportaciones | todo | no | todo al aprobar/rechazar | no |
| retiros | todo | no | todo al aprobar/rechazar | no |
| saldos_usuario_moneda | todo | no | no | no |
| movimientos | todo | no | no | no |
| documentos | todo | no | no | no |
| auditoria_admin | todo | no | no | no |
| validaciones_admin | todo | no | no | no |
| operaciones_financieras | todo | no | no | no |

### 8.3 Backend / service role

| Tabla | SELECT | INSERT | UPDATE | DELETE |
|---|---|---|---|---|
| usuarios | sí | sí | sí | sí solo bajo control interno |
| cuentas_usuario | sí | sí | sí | sí solo bajo control interno |
| aportaciones | sí | sí | sí | no |
| retiros | sí | sí | sí | no |
| saldos_usuario_moneda | sí | sí | sí | no |
| movimientos | sí | sí | sí | no |
| documentos | sí | sí | sí | no |
| auditoria_admin | sí | sí | sí | no |
| validaciones_admin | sí | sí | sí | no |
| operaciones_financieras | sí | sí | sí | no |

> En la práctica, el backend debe ser el único responsable de la escritura financiera. El acceso del cliente se limita a peticiones y lectura propia.

---

## 9. Seguridad para impedir que un usuario modifique su saldo o los movimientos directamente

### Reglas de seguridad del diseño

1. `saldos_usuario_moneda` debe tener RLS con `for all using (false) with check (false)` para cliente.
2. `movimientos` debe tener la misma restricción.
3. `auditoria_admin` debe ser de solo lectura para admin y sin escritura desde cliente.
4. La lógica de saldo se escribe estrictamente desde backend.
5. El frontend solo puede enviar una solicitud o una intención de operación.
6. La validación de disponibilidad y diferencias se hace en backend.
7. Los `UPDATE` sobre saldo se ejecutan únicamente dentro de una transacción
   segura con bloqueo de fila.
8. Los movimientos deben ser insertados desde la misma transacción que la actualización del saldo.
9. La auditoría debe registrarse con un `admin_id` y/o `usuario_id` real, no con datos del cliente.
10. Ninguna fila de saldo debe ser actualizable por un usuario autenticado.

### Restricción de diseño recomendada

```sql
create policy "saldo_no_client_write" on saldos_usuario_moneda for all using (false) with check (false);
create policy "movimientos_no_client_write" on movimientos for all using (false) with check (false);
create policy "auditoria_no_client_write" on auditoria_admin for all using (false) with check (false);
```

---

## 10. Flujo transaccional del backend para aportaciones y retiros

### 10.1 Flujo de aportación

1. El usuario crea la aportación con estado `pending`.
2. El backend valida:
   - usuario activo
   - importe > 0
   - moneda válida
   - idempotency_key no repetida
   - no hay otra aportación pendiente duplicada
3. El usuario sube documento / justificante.
4. El backend vincula el documento a la aportación.
5. El admin revisa.
6. Si aprueba, backend ejecuta transacción:
   - bloquear fila de saldo con `SELECT ... FOR UPDATE`
   - actualizar saldo
   - insertar movimiento
   - actualizar estado de aportación
   - registrar auditoría
   - commit
7. Si falla cualquier paso, rollback.

### 10.2 Flujo de retiro

1. El usuario crea el retiro con estado `pending`.
2. El backend valida:
   - usuario activo
   - moneda válida
   - importe > 0
   - saldo suficiente para el importe
   - idempotency_key no repetida
3. El admin revisa.
4. Si aprueba, backend ejecuta transacción:
   - bloquear saldo de la moneda con `FOR UPDATE`
   - validar saldo disponible
   - descontar saldo
   - insertar movimiento de débito
   - poner retiro en `approved`
   - registrar auditoría
   - commit
5. Si el saldo es insuficiente o hay fallo, rollback.

---

## 11. Idempotencia y control de concurrencia

### 11.1 Idempotencia

Cada operación crítica debe incluir un `idempotency_key` o `request_id`:

- creación de aportación
- aprobación de aportación
- creación de retiro
- aprobación de retiro
- inserción de auditoría
- creación de movimiento

### Reglas

- si llega la misma operación con la misma clave dos veces, se responde la misma operación o se identifica como ya procesada
- no se crea un movimiento duplicado
- no se registra auditoría duplicada
- no se acepta doble aprobación de la misma aportación
- no se acepta doble aprobación del mismo retiro

### 11.2 Control de concurrencia

Para evitar carreras concurrentes:

- bloquear la fila `saldos_usuario_moneda` con `SELECT ... FOR UPDATE`
- ejecutar validación de saldo y actualización en la misma transacción
- no dejar la validación de saldo en una operación separada del UPDATE
- usar transacción única para cada aprobación de entrada/salida

### Regla crítica

```sql
SELECT * FROM saldos_usuario_moneda
WHERE usuario_id = $1 AND moneda = $2
FOR UPDATE;
```

Esto evita que dos procesos decidan simultáneamente que hay saldo suficiente y ambos lo descuenten.

---

## 12. Auditoría de las acciones administrativas

### Tabla propuesta

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

### Información que debe dejarse trazada

- qué se aprobó o rechazó
- quién lo hizo
- quién es el usuario afectado
- importe y moneda
- saldo anterior y saldo posterior
- motivo del rechazo
- hora exacta
- idempotency_key
- referencia de la operación

### Ejemplos de eventos a auditar

- `APORTACION_CREADA`
- `APORTACION_RECHAZADA`
- `APORTACION_APROBADA`
- `RETIRO_SOLICITADO`
- `RETIRO_APROBADO`
- `RETIRO_RECHAZADO`
- `DOCUMENTO_VALIDADO`
- `SALDO_AJUSTADO`

---

## 13. Pseudocódigo del backend para operaciones críticas

### 13.1 Aprobar una aportación

```python
async def aprobar_aportacion(aportacion_id: str, admin_id: str, idempotency_key: str):
    with db.transaction() as tx:
        # 1. idempotencia
        ya = tx.query_one("""
            select id from auditoria_admin
            where tipo = 'APORTACION_APROBADA'
              and entity_id = %s
              and idempotency_key = %s
        """, [aportacion_id, idempotency_key])

        if ya:
            return {"status": "already_processed"}

        # 2. cargar operación y bloquear la fila
        aportacion = tx.query_one("""
            select * from aportaciones
            where id = %s
            for update
        """, [aportacion_id])

        if not aportacion:
            raise ValueError('aportacion_no_existe')

        if aportacion.estado != 'pending':
            raise ValueError('aportacion_no_pendiente')

        # 3. validar permisos admin
        admin = tx.query_one("select id, rol from usuarios where id = %s", [admin_id])
        if admin.rol != 'admin':
            raise PermissionError('no_autorizado')

        # 4. bloquear saldo
        saldo = tx.query_one("""
            select * from saldos_usuario_moneda
            where usuario_id = %s and moneda = %s
            for update
        """, [aportacion.usuario_id, aportacion.moneda])

        if not saldo:
            tx.execute("""
                insert into saldos_usuario_moneda (id, usuario_id, moneda, saldo)
                values (gen_random_uuid(), %s, %s, 0)
            """, [aportacion.usuario_id, aportacion.moneda])
            saldo = tx.query_one("""
                select * from saldos_usuario_moneda
                where usuario_id = %s and moneda = %s
                for update
            """, [aportacion.usuario_id, aportacion.moneda])

        nuevo_saldo = saldo.saldo + aportacion.importe

        # 5. actualizar saldo
        tx.execute("""
            update saldos_usuario_moneda
            set saldo = %s, updated_at = now(), version = version + 1
            where id = %s
        """, [nuevo_saldo, saldo.id])

        # 6. insertar movimiento
        tx.execute("""
            insert into movimientos (id, usuario_id, tipo, moneda, importe, saldo_post, referencia, operacion_id, estado, created_by)
            values (gen_random_uuid(), %s, 'APORTACION', %s, %s, %s, %s, %s, 'confirmed', %s)
        """, [aportacion.usuario_id, aportacion.moneda, aportacion.importe, nuevo_saldo, aportacion.id, aportacion.id, admin_id])

        # 7. actualizar aportacion
        tx.execute("""
            update aportaciones
            set estado = 'approved', aprobado_por = %s, aprobado_en = now(), updated_at = now()
            where id = %s
        """, [admin_id, aportacion_id])

        # 8. auditoría
        tx.execute("""
            insert into auditoria_admin (id, tipo, entity_id, usuario_id, admin_id, accion, detalles, idempotency_key)
            values (gen_random_uuid(), 'APORTACION_APROBADA', %s, %s, %s, 'approve', %s, %s)
        """, [
            aportacion_id,
            aportacion.usuario_id,
            admin_id,
            {
                "importe": str(aportacion.importe),
                "moneda": aportacion.moneda,
                "saldo_anterior": str(saldo.saldo),
                "saldo_nuevo": str(nuevo_saldo)
            },
            idempotency_key
        ])

    return {"status": "approved"}
```

### 13.2 Aprobar un retiro

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
            select * from retiros
            where id = %s
            for update
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
            where usuario_id = %s and moneda = %s
            for update
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
            {
                "importe": str(retiro.importe),
                "moneda": retiro.moneda,
                "saldo_anterior": str(saldo.saldo),
                "saldo_nuevo": str(nuevo_saldo)
            },
            idempotency_key
        ])

    return {"status": "approved"}
```

---

## 14. Implementación segura del backend

### Nota técnica

La implementación real debe respetar estas reglas:

1. Usar backend con acceso privado y servidor a servidor.
2. Cargar la sesión del usuario desde JWT o sesión segura.
3. No recibir saldo o movimientos directamente desde la interfaz.
4. Validar todo en backend con la base de verdad.
5. Ejecutar `BEGIN` para cada transacción crítica.
6. Usar `SELECT ... FOR UPDATE` sobre la fila de saldo afectada.
7. Ejecutar `COMMIT` solo al final, con `ROLLBACK` si falla.
8. No permitir modificación desde API pública para acciones financieras internas.
9. Registrar todos los eventos importantes en `auditoria_admin`.
10. Guardar `idempotency_key` en la operación y en la auditoria.
11. Mantener `movimientos` inmutables.
12. Mantener `saldos_usuario_moneda` derivado exclusivamente de transacciones válidas.

### Capa de seguridad recomendada

- app backend
- validación de dominio
- permisos de rol
- bloqueo de filas
- transacciones atómicas
- auditoría
- RLS como defensa adicional

---

## 15. Orden exacto recomendado para implementar más adelante

1. Revisar y aprobar este documento
2. Confirmar que la relación entre `usuarios` y el sistema actual de autenticación es correcta
3. Validar el modelo de roles (`user`, `admin`, `service_role`)
4. Confirmar si se usa un `usuarios` existente o se crea una capa de perfiles financieramente separada
5. Revisar y aprobar RLS y permisos por tabla
6. Confirmar el tipo de documento y almacenamiento de justificantes
7. Confirmar el modelo de cuentas bancarias y moneda
8. Preparar migración SQL de esquema final
9. Preparar migración SQL de índices y constraints
10. Preparar migración SQL de RLS
11. Preparar backend con transacciones y bloqueo de fila
12. Preparar pruebas de idempotencia y concurrencia en entorno de prueba
13. Ejecutar la migración solo tras backup y verificación
14. Desplegar en entorno de pruebas
15. Ejecutar pruebas de negocio funcional
16. Preparar producción con revisión final

---

## 16. Checklist antes de producción

- [ ] Backup confirmado.
- [ ] Conexión PostgreSQL verificada.
- [ ] SSL verificado.
- [ ] Esquema actual comprobado.
- [ ] RLS revisadas.
- [ ] Roles comprobados.
- [ ] Backend revisado.
- [ ] Pruebas realizadas en entorno de prueba.
- [ ] SQL revisado y aprobado.

---

## 17. Puntos que requieren decisión antes de aprobar

Antes de dar el visto bueno final, todavía requiere una decisión sobre estos puntos:

1. ¿La tabla `usuarios` actual del proyecto ya cumple la necesidad de autenticación y rol, o se quiere una capa separada de perfiles financieros?
2. ¿La moneda y el saldo serán solo por `EUR`, `CUP`, `MLC` o se añadirá más adelante otra moneda?
3. ¿La cuenta bancaria para retiros se modela como `cuentas_usuario` o como una entidad separada con más detalle?
4. ¿El administrador tendrá un rol JWT específico o se usará la misma entidad `usuarios` con `rol = 'admin'`?
5. ¿El `documentos` financiero reutiliza la tabla actual de documentos del proyecto o se crea una tabla separada dedicada a justificantes?
6. ¿Se quiere auditar solo decisiones administrativas o también cada cambio financiero interno del backend?
7. ¿La operación financiera de comisión / ajuste / devolución debe implementarse desde el inicio o dejarse como extensión futura?
8. ¿Se va a mantener una tabla unificada `operaciones_financieras` o se va a diseñar una jerarquía más específica?

> Cuando estas decisiones queden cerradas, el documento puede pasar a la fase de implementación real, pero no antes.

---

## 18. Conclusión

Este documento define una base sólida para la capa financiera sin tocar ni ejecutar nada sobre la base real. Queda preparado para revisión y aprobación, con separación clara de responsabilidades, auditoría, transacciones, idempotencia y reglas seguras de saldo y retiros.

La implementación real no debe comenzar hasta que:

- el esquema sea aprobado,
- las RLS sean revisadas,
- los roles estén confirmados,
- el backend esté validado,
- el entorno de prueba confirme funcionamiento real.

---

Fin del documento de revisión.
