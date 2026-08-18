# Diseño del backend para validación y transacciones financieras

Este documento describe el flujo completo de negocio para la capa financiera, sin ejecutar nada en PostgreSQL ni hacer cambios reales en la base de datos.

## Objetivo

Garantizar que:
- las operaciones financieras sean atómicas;
- el saldo no pueda ser falseado;
- un usuario no pueda modificar su propio saldo;
- no se descuente dos veces una misma operación;
- la validación admin quede registrada;
- el historial de movimientos sea inmutable y trazable;
- cualquier fallo haga rollback completo.

---

## Principios arquitectónicos

1. El frontend solo envía intención de operación.
2. El backend valida permisos, identidad, moneda, importe y estado.
3. El saldo se calcula y actualiza solo en backend.
4. Los movimientos son la fuente de verdad del saldo.
5. Todo cambio financiero se guarda en auditoria_admin.
6. Todo cambio financiero se ejecuta dentro de una transacción PostgreSQL.
7. Si falla cualquier paso, se hace rollback completo.

---

## Reglas de negocio globales

### 1) Identidad y permisos
- El usuario autenticado debe venir en el JWT o en el contexto de sesión.
- El backend usa `usuario_id` del token y no confía en lo que manda el cliente.
- Solo el backend puede actualizar `saldos_usuario_moneda` y `movimientos`.
- Solo el admin puede validar/rechazar aportaciones y retiros.

### 2) Monedas separadas
- `EUR`, `CUP`, `MLC` son mutuamente excluyentes por saldo y movimiento.
- No se puede mezclar ninguna moneda en una operación.
- El backend debe fijar y validar la moneda antes de actualizar.

### 3) Idempotencia
Cada operación financiera debe tener una clave de idempotencia para evitar dobles envíos.

Ejemplo:
- `idempotency_key` por aportar/retiro
- si llega la misma operación dos veces, el backend devuelve el mismo resultado y no duplica movimientos o saldos

### 4) Concurrencia
- Se usan transacciones con `SELECT ... FOR UPDATE` sobre la fila de saldo del usuario + moneda.
- Esto bloquea la fila para que otra transacción no la modifique a la vez.

### 5) Sin dinero negativo
- Antes de procesar un retiro, se valida:
  - `saldo_disponible >= importe`
  - o, si se usa reserva, `saldo_disponible + saldo_retenido >= importe`
- Si no se cumple, la operación se rechaza.

---

## Entidades que participan

- usuarios
- aportaciones
- justificantes
- documentos
- movimientos
- saldos_usuario_moneda
- validaciones_admin
- auditoria_admin
- retiros

---

## Flujo 1: Creación de una aportación

### Casos de uso
- Un usuario normal quiere aportar capital.
- La operación debe quedar registrada con estado `pending`.
- El importe, moneda y cuenta deben validar.
- El usuario no debe poder modificar el saldo en el cliente.

### Reglas
- El backend toma `usuario_id` del token.
- El frontend envía datos de apoyo, pero no saldo.
- El backend crea la fila en `aportaciones` con estado `pending`.
- Se genera una `idempotency_key` para evitar duplicado.
- Se registra una validación inicial si se decide guardar el evento.

### Pseudocódigo

```python
async def crear_aportacion(payload, usuario_actual):
    # payload incluye: importe, moneda, operacion_id, cuenta_destino_id, comentarios
    # NO aceptar saldo ni campos de balance del cliente

    if usuario_actual is None:
        raise ForbiddenError('No autenticado')

    if payload['importe'] <= 0:
        raise ValidationError('Importe inválido')

    if payload['moneda'] not in {'EUR', 'CUP', 'MLC'}:
        raise ValidationError('Moneda inválida')

    if not existe_cuenta(payload['cuenta_destino_id'], payload['moneda']):
        raise ValidationError('Cuenta no válida para la moneda')

    idem = payload.get('idempotency_key')
    if idem and existe_aportacion_por_idempotencia(idem):
        return obtener_aportacion_existente(idem)

    with db.transaction() as tx:
        nueva = tx.execute(
            """
            INSERT INTO aportaciones (
                usuario_id,
                operacion_id,
                cuenta_destino_id,
                moneda,
                importe,
                estado,
                comentarios,
                fecha_solicitud,
                idempotency_key
            )
            VALUES (%s, %s, %s, %s, %s, 'pending', %s, NOW(), %s)
            RETURNING *
            """,
            (
                usuario_actual.id,
                payload.get('operacion_id'),
                payload['cuenta_destino_id'],
                payload['moneda'],
                payload['importe'],
                payload.get('comentarios'),
                idem,
            )
        )

        tx.execute(
            """
            INSERT INTO auditoria_admin (
                admin_id,
                accion,
                entidad,
                entidad_id,
                detalle,
                fecha,
                ip_address
            ) VALUES (%s, 'aportacion_creada', 'aportacion', %s, %s, NOW(), %s)
            """,
            (
                usuario_actual.id,
                nueva.id,
                {
                    'usuario_id': usuario_actual.id,
                    'importe': payload['importe'],
                    'moneda': payload['moneda'],
                    'operacion_id': payload.get('operacion_id')
                },
                obtener_ip_cliente()
            )
        )

        tx.commit()
        return nueva
```

### Qué se ejecuta dentro de una transacción PostgreSQL
- inserción de `aportaciones`
- registro de auditoria si se decide registrar la creación
- chequeo de idempotencia
- validación de permisos y existencia de cuentas

### No se hace aquí
- no se actualiza saldo todavía
- no se crea movimiento financiero todavía

---

## Flujo 2: Subida y vinculación del justificante

### Reglas
- El usuario sube la prueba de la transferencia o soporte documental.
- El archivo debe quedar asociado al `documentos` existente y a la `aportaciones` correspondiente.
- El backend debe vincular el documento con el usuario correcto.
- El documento no debe ser visible para otros usuarios.

### Pseudocódigo

```python
async def subir_justificante(aportacion_id, archivo, usuario_actual):
    if usuario_actual is None:
        raise ForbiddenError('No autenticado')

    aportacion = obtener_aportacion(aportacion_id)
    if aportacion['usuario_id'] != usuario_actual.id:
        raise ForbiddenError('No es tu aportación')

    # Guardar el documento en almacenamiento del sistema
    documento = guardar_documento(archivo, usuario_actual.id)

    with db.transaction() as tx:
        justificante = tx.execute(
            """
            INSERT INTO justificantes (
                usuario_id,
                aportacion_id,
                documento_id,
                nombre_archivo,
                mime_type,
                peso_bytes,
                estado_revision,
                fecha_subida,
                subido_por,
                comentario
            )
            VALUES (%s, %s, %s, %s, %s, %s, 'pending', NOW(), %s, %s)
            RETURNING *
            """,
            (
                usuario_actual.id,
                aportacion_id,
                documento.id,
                archivo.filename,
                archivo.content_type,
                archivo.size,
                usuario_actual.id,
                'Documento adjunto para validación'
            )
        )

        tx.execute(
            """
            INSERT INTO auditoria_admin (
                admin_id,
                accion,
                entidad,
                entidad_id,
                detalle,
                fecha,
                ip_address
            ) VALUES (%s, 'justificante_subido', 'justificante', %s, %s, NOW(), %s)
            """,
            (
                usuario_actual.id,
                justificante.id,
                {
                    'usuario_id': usuario_actual.id,
                    'aportacion_id': aportacion_id,
                    'documento_id': documento.id
                },
                obtener_ip_cliente()
            )
        )

        tx.commit()
        return justificante
```

### Qué se ejecuta dentro de transacción
- creación del documento
- inserción en `justificantes`
- auditoría del archivo subido

### No se hace aquí
- no se actualiza saldo
- no se aprueba la aportación

---

## Flujo 3: Validación / aprobación por administrador

### Reglas
- Solo un admin puede validar o rechazar una aportación.
- La validación debe ser trazable.
- Si la aportación está en `validated`, entonces se puede generar el movimiento y el saldo.
- Si la aportación se rechaza `rejected`, no debe actualizar saldo.

### Pseudocódigo

```python
async def validar_aportacion(aportacion_id, admin_id, accion, comentario=None):
    admin = obtener_usuario(admin_id)
    if admin.rol != 'admin':
        raise ForbiddenError('No es administrador')

    with db.transaction() as tx:
        aportacion = tx.execute(
            """
            SELECT * FROM aportaciones
            WHERE id = %s
            FOR UPDATE
            """,
            (aportacion_id,)
        ).fetchone()

        if aportacion is None:
            raise NotFoundError('Aportación no existe')

        if aportacion['estado'] in {'validated', 'rejected', 'cancelled'}:
            raise ValidationError('La aportación ya no puede cambiar de estado')

        if accion == 'approved':
            nuevo_estado = 'validated'
        elif accion == 'rejected':
            nuevo_estado = 'rejected'
        elif accion == 'request_information':
            nuevo_estado = 'information_requested'
        else:
            raise ValidationError('Acción no válida')

        tx.execute(
            """
            UPDATE aportaciones
            SET estado = %s,
                fecha_validacion = NOW(),
                validado_por = %s,
                comentarios = COALESCE(comentarios, '') || %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            (nuevo_estado, admin_id, (' | ' + comentario) if comentario else '', aportacion_id)
        )

        tx.execute(
            """
            INSERT INTO validaciones_admin (
                entidad,
                entidad_id,
                accion,
                admin_id,
                comentario,
                fecha,
                metadata
            )
            VALUES (%s, %s, %s, %s, %s, NOW(), %s)
            """,
            (
                'aportacion',
                aportacion_id,
                accion,
                admin_id,
                comentario,
                {
                    'usuario_id': aportacion['usuario_id'],
                    'importe': aportacion['importe'],
                    'moneda': aportacion['moneda']
                }
            )
        )

        tx.execute(
            """
            INSERT INTO auditoria_admin (
                admin_id,
                accion,
                entidad,
                entidad_id,
                detalle,
                ip_address,
                fecha
            ) VALUES (%s, 'aportacion_validada', 'aportacion', %s, %s, %s, NOW())
            """,
            (
                admin_id,
                aportacion_id,
                {
                    'usuario_id': aportacion['usuario_id'],
                    'accion': accion,
                    'importe': aportacion['importe'],
                    'moneda': aportacion['moneda'],
                    'comentario': comentario
                },
                obtener_ip_cliente()
            )
        )

        tx.commit()
        return {'estado': nuevo_estado}
```

### Qué se ejecuta dentro de transacción
- bloqueo de la fila de la aportación con `FOR UPDATE`
- update del estado de aportación
- inserción en `validaciones_admin`
- inserción en `auditoria_admin`

### Qué no se hace aquí
- no se actualiza saldo aún, si la acción es `approved` se hace en la siguiente lógica transaccional

---

## Flujo 4: Actualización del saldo del usuario

### Reglas
- El saldo no se recibe del navegador.
- El backend debe actualizar el saldo real por `usuario_id + moneda`.
- El saldo debe ser `>= 0` después de cada operación.
- Debe haber control de concurrencia para evitar doble descuento/ingreso.

### Pseudocódigo

```python
async def actualizar_saldo_usuario(tx, usuario_id, moneda, delta_importe, motivo, referencia, origen, origen_id):
    # delta_importe puede ser positivo o negativo
    # ejemplo: +500 EUR significa aporte validado
    # ejemplo: -200 EUR significa retiro procesado

    saldo = tx.execute(
        """
        SELECT * FROM saldos_usuario_moneda
        WHERE usuario_id = %s AND moneda = %s
        FOR UPDATE
        """,
        (usuario_id, moneda)
    ).fetchone()

    if saldo is None:
        saldo = tx.execute(
            """
            INSERT INTO saldos_usuario_moneda (
                usuario_id,
                moneda,
                saldo_disponible,
                saldo_retenido,
                actualizado_en
            )
            VALUES (%s, %s, 0, 0, NOW())
            RETURNING *
            """,
            (usuario_id, moneda)
        ).fetchone()

    nuevo_disponible = saldo['saldo_disponible'] + delta_importe
    if nuevo_disponible < 0:
        raise ValidationError('Saldo insuficiente para esta operación')

    tx.execute(
        """
        UPDATE saldos_usuario_moneda
        SET saldo_disponible = %s,
            actualizado_en = NOW(),
            updated_at = NOW()
        WHERE id = %s
        """,
        (nuevo_disponible, saldo['id'])
    )

    tx.execute(
        """
        INSERT INTO movimientos (
            usuario_id,
            tipo,
            importe,
            moneda,
            referencia,
            fecha,
            origen,
            origen_id,
            estado,
            descripcion,
            creado_por_admin
        )
        VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, 'applied', %s, %s)
        """,
        (
            usuario_id,
            motivo,
            delta_importe,
            moneda,
            referencia,
            origen,
            origen_id,
            f'Actualización por {origen}',
            None
        )
    )
```

### Regla importante
- El importe del movimiento debe reflejar el mismo delta que el salto del saldo.
- Si se usa `delta_importe` positivo, el saldo sube y el movimiento es positivo.
- Si es negativo, el saldo baja y el movimiento es negativo.

---

## Flujo 5: Creación del movimiento correspondiente

### Reglas
- El movimiento debe crear un historial de cada operación concreta.
- Debe guardar referencia, origen, usuario, importe, moneda y estado.
- Debe ser inmutable.

### Pseudocódigo

```python
async def registrar_movimiento(tx, usuario_id, tipo, importe, moneda, referencia, origen, origen_id, descripcion=None, admin_id=None):
    # Idempotencia: comprobar si ya existe la referencia
    existe = tx.execute(
        """
        SELECT id FROM movimientos
        WHERE referencia = %s AND origen = %s AND origen_id = %s
        LIMIT 1
        """,
        (referencia, origen, origen_id)
    ).fetchone()

    if existe:
        return existe['id']

    tx.execute(
        """
        INSERT INTO movimientos (
            usuario_id,
            tipo,
            importe,
            moneda,
            referencia,
            fecha,
            origen,
            origen_id,
            estado,
            descripcion,
            creado_por_admin
        )
        VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, 'applied', %s, %s)
        """,
        (
            usuario_id,
            tipo,
            importe,
            moneda,
            referencia,
            origen,
            origen_id,
            descripcion,
            admin_id
        )
    )
```

### Qué debe quedar en el movimiento
- usuario_id
- tipo: aporte o retiro
- importe: puede ser positivo o negativo
- moneda
- referencia: texto único, ejemplo `aportacion:42` o `retiro:12`
- fecha: NOW()
- origen: `aportacion` o `retiro`
- origen_id: id de la fila relacionada
- estado: `applied` o `reversed`

---

## Flujo 6: Solicitud de retiro

### Reglas
- El usuario crea una solicitud de retiro con `estado = 'pending'`.
- El backend jamás acepta un retiro sin comprobar si hay saldo suficiente.
- La validación y el descuento no se hacen en la misma fase del usuario.

### Pseudocódigo

```python
async def crear_retiro(payload, usuario_actual):
    if usuario_actual is None:
        raise ForbiddenError('No autenticado')

    if payload['importe'] <= 0:
        raise ValidationError('Importe inválido')

    if payload['moneda'] not in {'EUR', 'CUP', 'MLC'}:
        raise ValidationError('Moneda inválida')

    idem = payload.get('idempotency_key')
    if idem and existe_retiro_por_idempotencia(idem):
        return obtener_retiro_existente(idem)

    with db.transaction() as tx:
        saldo = tx.execute(
            """
            SELECT * FROM saldos_usuario_moneda
            WHERE usuario_id = %s AND moneda = %s
            FOR UPDATE
            """,
            (usuario_actual.id, payload['moneda'])
        ).fetchone()

        if saldo is None:
            raise ValidationError('No existe saldo para esa moneda')

        # No se descuenta todavía; solo se valida la disponibilidad
        if saldo['saldo_disponible'] < payload['importe']:
            raise ValidationError('Saldo insuficiente para retirar')

        retiro = tx.execute(
            """
            INSERT INTO retiros (
                usuario_id,
                moneda,
                importe,
                destino,
                estado,
                fecha_solicitud,
                comentarios,
                idempotency_key
            )
            VALUES (%s, %s, %s, %s, 'pending', NOW(), %s, %s)
            RETURNING *
            """,
            (
                usuario_actual.id,
                payload['moneda'],
                payload['importe'],
                payload['destino'],
                payload.get('comentarios'),
                idem,
            )
        ).fetchone()

        tx.execute(
            """
            INSERT INTO auditoria_admin (
                admin_id,
                accion,
                entidad,
                entidad_id,
                detalle,
                fecha,
                ip_address
            ) VALUES (%s, 'retiro_solicitado', 'retiro', %s, %s, NOW(), %s)
            """,
            (
                usuario_actual.id,
                retiro['id'],
                {
                    'usuario_id': usuario_actual.id,
                    'moneda': payload['moneda'],
                    'importe': payload['importe'],
                    'destino': payload['destino']
                },
                obtener_ip_cliente()
            )
        )

        tx.commit()
        return retiro
```

### Qué se hace dentro de transacción
- bloqueo del saldo del usuario + moneda
- comprobación de disponibilidad
- inserción del retiro
- auditoría de la solicitud

### Qué no se hace aquí
- no se descuenta saldo todavía
- la autoridad de aprobación está en admin

---

## Flujo 7: Validación del retiro por administrador

### Reglas
- Solo un admin puede aprobar/rechazar un retiro.
- El ingreso o descuento del saldo se hace en la capa transaccional.
- La validación debe quedar en `validaciones_admin` y `auditoria_admin`.

### Pseudocódigo

```python
async def validar_retiro(retiro_id, admin_id, accion, comentario=None):
    admin = obtener_usuario(admin_id)
    if admin.rol != 'admin':
        raise ForbiddenError('No es administrador')

    with db.transaction() as tx:
        retiro = tx.execute(
            """
            SELECT * FROM retiros
            WHERE id = %s
            FOR UPDATE
            """,
            (retiro_id,)
        ).fetchone()

        if retiro is None:
            raise NotFoundError('Retiro no existe')

        if retiro['estado'] in {'approved', 'rejected', 'processed', 'cancelled'}:
            raise ValidationError('El retiro ya no puede validarse')

        if accion == 'approved':
            nuevo_estado = 'approved'
            fecha_aprobacion = 'NOW()'
        elif accion == 'rejected':
            nuevo_estado = 'rejected'
            fecha_aprobacion = 'NOW()'
        else:
            raise ValidationError('Acción no válida para retiro')

        tx.execute(
            """
            UPDATE retiros
            SET estado = %s,
                fecha_aprobacion = NOW(),
                aprobado_por = %s,
                comentarios = COALESCE(comentarios, '') || %s,
                motivo_rechazo = %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            (
                nuevo_estado,
                admin_id,
                (' | ' + comentario) if comentario else '',
                comentario if accion == 'rejected' else None,
                retiro_id,
            )
        )

        tx.execute(
            """
            INSERT INTO validaciones_admin (
                entidad,
                entidad_id,
                accion,
                admin_id,
                comentario,
                motivo,
                fecha,
                metadata
            )
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
            """,
            (
                'retiro',
                retiro_id,
                accion,
                admin_id,
                comentario,
                comentario if accion == 'rejected' else None,
                {
                    'usuario_id': retiro['usuario_id'],
                    'importe': retiro['importe'],
                    'moneda': retiro['moneda']
                }
            )
        )

        tx.execute(
            """
            INSERT INTO auditoria_admin (
                admin_id,
                accion,
                entidad,
                entidad_id,
                detalle,
                fecha,
                ip_address
            ) VALUES (%s, 'retiro_validado', 'retiro', %s, %s, NOW(), %s)
            """,
            (
                admin_id,
                retiro_id,
                {
                    'usuario_id': retiro['usuario_id'],
                    'accion': accion,
                    'importe': retiro['importe'],
                    'moneda': retiro['moneda'],
                    'comentario': comentario
                },
                obtener_ip_cliente()
            )
        )

        tx.commit()
        return {'estado': nuevo_estado}
```

---

## Flujo 8: Descuento del saldo

### Reglas
- Debe hacerse solo tras aprobación del retiro.
- Debe verificarse saldo disponible.
- Debe ser atómico.
- Debe respetar la idempotencia: no descontar dos veces el mismo retiro.

### Pseudocódigo

```python
async def procesar_retiro(retiro_id, admin_id):
    admin = obtener_usuario(admin_id)
    if admin.rol != 'admin':
        raise ForbiddenError('No es administrador')

    with db.transaction() as tx:
        retiro = tx.execute(
            """
            SELECT * FROM retiros
            WHERE id = %s
            FOR UPDATE
            """,
            (retiro_id,)
        ).fetchone()

        if retiro is None:
            raise NotFoundError('Retiro no existe')

        if retiro['estado'] in {'processed', 'cancelled'}:
            raise ValidationError('Retiro ya procesado o cancelado')

        saldo = tx.execute(
            """
            SELECT * FROM saldos_usuario_moneda
            WHERE usuario_id = %s AND moneda = %s
            FOR UPDATE
            """,
            (retiro['usuario_id'], retiro['moneda'])
        ).fetchone()

        if saldo is None:
            raise ValidationError('No existe saldo para esa moneda')

        if saldo['saldo_disponible'] < retiro['importe']:
            raise ValidationError('Saldo insuficiente para procesar retiro')

        # Idempotencia: comprobar si el movimiento ya existe.
        movimiento_existente = tx.execute(
            """
            SELECT id FROM movimientos
            WHERE origen = 'retiro' AND origen_id = %s AND referencia = %s
            LIMIT 1
            """,
            ('retiro', f'retiro:{retiro_id}')
        ).fetchone()

        if movimiento_existente:
            raise ValidationError('El retiro ya tiene un movimiento asociado')

        nuevo_saldo = saldo['saldo_disponible'] - retiro['importe']

        tx.execute(
            """
            UPDATE saldos_usuario_moneda
            SET saldo_disponible = %s,
                actualizado_en = NOW(),
                updated_at = NOW()
            WHERE id = %s
            """,
            (nuevo_saldo, saldo['id'])
        )

        tx.execute(
            """
            INSERT INTO movimientos (
                usuario_id,
                tipo,
                importe,
                moneda,
                referencia,
                fecha,
                origen,
                origen_id,
                estado,
                descripcion,
                creado_por_admin
            )
            VALUES (%s, 'retiro', %s, %s, %s, NOW(), 'retiro', %s, 'applied', %s, %s)
            """,
            (
                retiro['usuario_id'],
                -retiro['importe'],
                retiro['moneda'],
                f'retiro:{retiro_id}',
                retiro_id,
                'Retiro procesado',
                admin_id
            )
        )

        tx.execute(
            """
            UPDATE retiros
            SET estado = 'processed',
                fecha_procesado = NOW(),
                updated_at = NOW()
            WHERE id = %s
            """,
            (retiro_id,)
        )

        tx.execute(
            """
            INSERT INTO auditoria_admin (
                admin_id,
                accion,
                entidad,
                entidad_id,
                detalle,
                fecha,
                ip_address
            ) VALUES (%s, 'retiro_procesado', 'retiro', %s, %s, NOW(), %s)
            """,
            (
                admin_id,
                retiro_id,
                {
                    'usuario_id': retiro['usuario_id'],
                    'importe': retiro['importe'],
                    'moneda': retiro['moneda']
                },
                obtener_ip_cliente()
            )
        )

        tx.commit()
        return {'status': 'processed'}
```

### Garantías de esta transacción
- No descuenta dos veces la misma operación porque la consulta `SELECT ... FOR UPDATE` bloquea la fila del saldo y la comprobación del movimiento existente evita duplicados.
- Si el saldo queda por debajo de cero, se aborta la transacción.
- Si falla cualquier paso, el rollback lo revierte todo.

---

## Flujo 9: Registro de auditoría para todo cambio financiero

### Qué debe registrarse en auditoria_admin
- creación de aportación
- subida de justificante
- aprobación/rechazo de aportación
- creación de retiro
- aprobación/rechazo/procesado del retiro
- cambio de saldo
- inserción de movimiento
- corrección manual de saldo
- cualquier acción administrativa que afecte a dinero

### Pseudocódigo genérico

```python
async def registrar_auditoria(tx, admin_id, accion, entidad, entidad_id, detalle, ip_address=None):
    tx.execute(
        """
        INSERT INTO auditoria_admin (
            admin_id,
            accion,
            entidad,
            entidad_id,
            detalle,
            ip_address,
            fecha
        )
        VALUES (%s, %s, %s, %s, %s::jsonb, %s, NOW())
        """,
        (
            admin_id,
            accion,
            entidad,
            entidad_id,
            json.dumps(detalle),
            ip_address,
        )
    )
```

### Requisitos
- auditoria_admin solo debe poder ser escrita por backend/admin
- usuarios normales no pueden ni leer ni modificar esta tabla
- auditoria_admin tiene trazabilidad completa y un historial inmutable

---

## Transparencia de transacciones PostgreSQL

Las siguientes operaciones deben ejecutarse dentro de una misma transacción PostgreSQL:

### A. Validación de aportación
- bloquear la fila `aportaciones`
- actualizar `aportaciones.estado`
- insertar `validaciones_admin`
- insertar `auditoria_admin`
- si la validación implica saldo, también bloquear `saldos_usuario_moneda` e insertar `movimientos`

### B. Procesado de aporte validado
- bloquear saldo del usuario + moneda
- comprobar saldo disponible
- insertar movimiento positivo
- actualizar saldo
- actualizar estado de aportación si se requiere
- registrar auditoria_admin

### C. Aprobación de retiro
- bloquear retiro
- bloquear saldo_usuario_moneda
- comprobar disponible
- actualizar saldo
- insertar movimiento negativo
- actualizar retiro a `processed`
- registrar auditoria_admin

### D. Rechazo de retiro o aportación
- actualizar estado de la operacion
- insertar validaciones_admin
- insertar auditoria_admin
- no alterar saldo si la operación fue rechazada

### E. Cualquier corrección manual crítica
- bloquear fila del saldo
- insertar movimiento de ajuste
- actualizar saldo
- registrar auditoria_admin

---

## Cómo se evita doble descuento o duplicado

Se deben aplicar estas tres capas:

1. Idempotency key
   - cada operación financiera lleva un `idempotency_key`
   - si llega la misma operación dos veces, no se inserta dos veces

2. Verificación de movimiento previo
   - antes de crear un movimiento, comprobar si ya existe:
     - mismo origen
     - mismo origen_id
     - misma referencia

3. Bloqueo de saldo con `FOR UPDATE`
   - si dos procesos intentan modificar el mismo saldo al mismo tiempo, uno esperará hasta que el otro termine

Ejemplo:

```sql
SELECT * FROM saldos_usuario_moneda
WHERE usuario_id = $1 AND moneda = $2
FOR UPDATE;
```

Esto es esencial para evitar race conditions.

---

## Cómo se asegura que el saldo no quede negativo

Se debe exigir esta regla en el backend antes de cada actualización:

```python
if nuevo_saldo < 0:
    raise ValidationError('Saldo insuficiente')
```

Y además se aplica en la base:

```sql
CHECK (saldo_disponible >= 0)
```

Esto aporta validación de capa de negocio y capa de base de datos.

---

## Cómo se evita que el usuario cambie su saldo

Debe cumplirse esta regla estricta:

- no permitir que el cliente mande `saldo_disponible`
- no permitir `UPDATE` directo a `saldos_usuario_moneda` desde el frontend
- no permitir que un usuario haga `INSERT` a `movimientos`
- no permitir que un usuario haga `UPDATE` a `aportaciones` para cambiar a `validated`
- no permitir que un usuario haga `UPDATE` a `retiros` para cambiar a `processed`

Todo eso debe quedar solo en backend/admin.

---

## Qué debe quedar fuera del frontend

El frontend no debe hacer nunca esto:
- enviar un valor de saldo fijo
- sumar o restar saldo en el navegador
- crear movimientos manualmente
- marcar una aportación como validada
- aprobar un retiro directamente
- manipular auditoría

El frontend solo debe enviar:
- intención de operación
- importe
- moneda
- cuenta elegida
- comentarios
- idempotency key
- datos de soporte para justificante

---

## Tabla de responsabilidades

| Acción | Usuario | Admin | Backend/service role |
|---|---|---|---|
| Crear aportación | Sí, propia | No | Sí |
| Subir justificante | Sí, propio | Sí | Sí |
| Validar aportación | No | Sí | Sí |
| Actualizar saldo | No | No (sin backend) | Sí |
| Crear movimiento | No | No | Sí |
| Solicitar retiro | Sí, propio | No | Sí |
| Validar retiro | No | Sí | Sí |
| Descontar saldo | No | No | Sí |
| Registrar auditoría | No | No | Sí |

---

## Conclusión del diseño backend

Este diseño garantiza:
- atómico negocio y transaccionalidad;
- control de permisos por usuario/admin/backend;
- trazabilidad completa;
- cálculo del saldo desde movimientos validados;
- bloqueo de doble consumo y doble inserción;
- rollback total si falla cualquier paso;
- consistencia financiera y control de concurrencia.

La clave es que el saldo y los movimientos no son un dato “de entrada” del frontend, sino un estado derivado del backend y validado por transacciones reales en PostgreSQL.

---

## Recomendación antes de implementación

Antes de ejecutar este diseño en la base real, conviene revisar y confirmar:
1. que la conexión a PostgreSQL esté restaurada;
2. que exista backup verificado;
3. que la base tenga usuarios y documentos bien configurados;
4. que las RLS y roles quedarán definidos después de esta capa transaccional;
5. que el backend tenga los permisos de escritura a saldo, movimientos y auditoría.

Esto queda listo para revisión antes de implementar la capa real en la base de datos.
