"""
API REST con FastAPI para Dashboard Web
Endpoints para estudiantes y panel de administración
"""

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional, Dict
from datetime import datetime

from database.models import get_db
from modules.estudiantes import Estudiante
from modules.admin_panel import PanelAdministrativo
from api.schemas import (
    EstudianteCreate, EstudianteResponse, EstudianteUpdate,
    LoginRequest, LoginResponse, EstadisticasResponse
)
from api.auth import crear_token, verificar_token

app = FastAPI(
    title="Bot Visas Estudio API",
    description="API para gestión de estudiantes y agencia educativa",
    version="1.0.0"
)

# CORS - Permitir requests desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://bot-visas-api.onrender.com",
        "https://bot-visas-web-marca-como-private-s785-g4twzsjhe.vercel.app",
        "https://*.vercel.app",  # Permitir todos los subdominios de Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Ejecutar migraciones al iniciar"""
    import os
    import psycopg2
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Crear tabla documentos_generados si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documentos_generados (
                id SERIAL PRIMARY KEY,
                estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
                tipo_documento VARCHAR(100) NOT NULL,
                nombre_archivo VARCHAR(255) NOT NULL,
                contenido_pdf TEXT NOT NULL,
                estado VARCHAR(50) DEFAULT 'generado',
                notas TEXT,
                generado_por VARCHAR(100),
                aprobado_por VARCHAR(100),
                fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_aprobacion TIMESTAMP,
                enviado_estudiante BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_documentos_generados_estudiante 
            ON documentos_generados(estudiante_id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_documentos_generados_estado 
            ON documentos_generados(estado);
        """)
        
        # Crear tabla cursos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cursos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                descripcion TEXT,
                duracion_meses INTEGER,
                precio_eur DECIMAL(10,2),
                ciudad VARCHAR(100),
                nivel_espanol_requerido VARCHAR(50),
                cupos_disponibles INTEGER DEFAULT 0,
                activo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla alojamientos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alojamientos (
                id SERIAL PRIMARY KEY,
                tipo VARCHAR(100) NOT NULL,
                direccion TEXT,
                ciudad VARCHAR(100),
                precio_mensual_eur DECIMAL(10,2),
                capacidad INTEGER DEFAULT 1,
                disponible BOOLEAN DEFAULT TRUE,
                descripcion TEXT,
                servicios TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Actualizar tabla documentos con campos OCR
        cursor.execute("""
            ALTER TABLE documentos 
            ADD COLUMN IF NOT EXISTS ocr_procesado BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS ocr_datos_extraidos JSONB,
            ADD COLUMN IF NOT EXISTS ocr_validacion JSONB,
            ADD COLUMN IF NOT EXISTS ocr_nivel_confianza INTEGER DEFAULT 0,
            ADD COLUMN IF NOT EXISTS ocr_alertas JSONB,
            ADD COLUMN IF NOT EXISTS ocr_fecha_procesamiento TIMESTAMP;
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_documentos_ocr_procesado 
            ON documentos(ocr_procesado);
        """)
        
        # Agregar columnas a estudiantes si no existen
        cursor.execute("""
            ALTER TABLE estudiantes 
            ADD COLUMN IF NOT EXISTS curso_asignado_id INTEGER REFERENCES cursos(id),
            ADD COLUMN IF NOT EXISTS alojamiento_asignado_id INTEGER REFERENCES alojamientos(id),
            ADD COLUMN IF NOT EXISTS universidad_referidora_id INTEGER,
            ADD COLUMN IF NOT EXISTS codigo_referido VARCHAR(50);
        """)
        
        # Crear tabla universidades_partner
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS universidades_partner (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                pais VARCHAR(100) DEFAULT 'España',
                codigo_referido VARCHAR(50) UNIQUE NOT NULL,
                email_contacto VARCHAR(255),
                persona_contacto VARCHAR(255),
                telefono VARCHAR(50),
                tipo_comision VARCHAR(50) DEFAULT 'porcentaje',
                valor_comision DECIMAL(10,2) DEFAULT 15.00,
                estado VARCHAR(50) DEFAULT 'activo',
                logo_url TEXT,
                sitio_web VARCHAR(255),
                notas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_universidades_codigo 
            ON universidades_partner(codigo_referido);
        """)
        
        # Crear tabla comisiones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comisiones (
                id SERIAL PRIMARY KEY,
                universidad_id INTEGER REFERENCES universidades_partner(id),
                estudiante_id INTEGER REFERENCES estudiantes(id),
                monto_curso DECIMAL(10,2),
                monto_comision DECIMAL(10,2),
                estado VARCHAR(50) DEFAULT 'pendiente',
                fecha_matricula TIMESTAMP,
                fecha_pago TIMESTAMP,
                notas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_comisiones_universidad 
            ON comisiones(universidad_id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_comisiones_estado 
            ON comisiones(estado);
        """)
        
        # Agregar foreign key a estudiantes
        cursor.execute("""
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.table_constraints 
                    WHERE constraint_name = 'fk_estudiantes_universidad'
                ) THEN
                    ALTER TABLE estudiantes 
                    ADD CONSTRAINT fk_estudiantes_universidad 
                    FOREIGN KEY (universidad_referidora_id) 
                    REFERENCES universidades_partner(id);
                END IF;
            END $$;
        """)
        
        conn.commit()
        
        # ===== SEED: Insertar universidades partner iniciales =====
        from api.seed_universidades import UNIVERSIDADES_DATA
        
        cursor.execute("SELECT COUNT(*) FROM universidades_partner")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("[INFO] Insertando 52 universidades partner iniciales...")
            inserted = 0
            for uni in UNIVERSIDADES_DATA:
                try:
                    cursor.execute("""
                        INSERT INTO universidades_partner (
                            nombre, pais, email_contacto, telefono, 
                            tipo_comision, valor_comision, codigo_referido, 
                            estado, logo_url, sitio_web, notas
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (codigo_referido) DO NOTHING
                    """, (
                        uni["nombre"], uni["pais"], uni["email_contacto"], 
                        uni["telefono"], uni["tipo_comision"], uni["valor_comision"],
                        uni["codigo_referido"], uni["estado"], 
                        uni.get("logo_url", ""), uni["sitio_web"], uni["notas"]
                    ))
                    inserted += 1
                except Exception as e:
                    print(f"[WARN] Error insertando {uni['nombre']}: {e}")
                    continue
            
            conn.commit()
            print(f"[OK] Insertadas {inserted} universidades partner")
        else:
            print(f"[INFO] Ya existen {count} universidades partner en la BD")
        
        cursor.close()
        conn.close()
        print("[OK] Tabla documentos_generados verificada/creada")
        print("[OK] Campos OCR agregados a documentos")
        print("[OK] Sistema de partnerships universitarios creado")
    except Exception as e:
        print(f"[ERROR] Error en startup: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: especificar dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


# ============================================================================
# AUTENTICACIÓN
# ============================================================================

@app.post("/api/login", response_model=LoginResponse, tags=["Auth"])
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    """
    Login para admins
    Email: leandroeloytamayoreyes@gmail.com / Contraseña: Eloy1940
    """
    import bcrypt
    import os
    import psycopg2
    
    try:
        # Conexión directa a la BD
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        # Buscar usuario por email
        cur.execute('SELECT email, password, nombre, rol FROM usuarios WHERE email = %s', (datos.usuario,))
        result = cur.fetchone()
        
        if not result:
            cur.close()
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
        
        email, password_hash, nombre, rol = result
        
        # Verificar contraseña con bcrypt
        if not bcrypt.checkpw(datos.password.encode('utf-8'), password_hash.encode('utf-8')):
            cur.close()
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
        
        cur.close()
        conn.close()
        
        # Crear token
        token = crear_token({"usuario": email, "rol": rol})
        return LoginResponse(
            token=token,
            tipo="Bearer",
            usuario=nombre,
            rol=rol
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en login: {str(e)}"
        )


def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Verifica token JWT y retorna usuario"""
    token = credentials.credentials
    payload = verificar_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    return payload


# ============================================================================
# ENDPOINTS PÚBLICOS (Estudiantes)
# ============================================================================

@app.post("/api/estudiantes", tags=["Estudiantes"])
def registrar_estudiante(datos: dict, db: Session = Depends(get_db)):
    """
    Registro público de estudiantes
    No requiere autenticación
    """
    try:
        from database.models import Estudiante as EstudianteModel
        
        # Verificar si ya existe
        existe = db.query(EstudianteModel).filter(
            EstudianteModel.email == datos.get('email')
        ).first()
        
        if existe:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un estudiante con este email"
            )
        
        # Crear nuevo estudiante
        nuevo = EstudianteModel(
            nombre=datos.get('nombre'),
            email=datos.get('email'),
            telefono=datos.get('telefono'),
            pasaporte=datos.get('pasaporte'),
            edad=datos.get('edad'),
            nacionalidad=datos.get('nacionalidad'),
            ciudad_origen=datos.get('ciudad_origen'),
            especialidad=datos.get('especialidad'),
            nivel_espanol=datos.get('nivel_espanol'),
            tipo_visa=datos.get('tipo_visa', 'estudiante'),
            estado='pendiente',
            documentos_estado='pendiente'
        )
        
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        
        # Enviar email de bienvenida
        try:
            from api.email_utils import email_bienvenida
            email_bienvenida(nuevo.nombre, nuevo.email, nuevo.id)
        except Exception as e:
            print(f"[WARN] Error enviando email: {e}")
        
        return {
            "id": nuevo.id,
            "estudiante_id": nuevo.id,
            "mensaje": "Registro exitoso. Revisa tu email para más información.",
            "estado": nuevo.estado
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/estudiantes/{estudiante_id}", tags=["Estudiantes"])
def obtener_estudiante_publico(estudiante_id: int, db: Session = Depends(get_db)):
    """
    Obtiene datos de un estudiante (sin auth para estudiante)
    """
    from database.models import Estudiante as EstudianteModel
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return {
        "id": estudiante.id,
        "nombre": estudiante.nombre,
        "email": estudiante.email,
        "telefono": estudiante.telefono,
        "pasaporte": estudiante.pasaporte,
        "edad": estudiante.edad,
        "nacionalidad": estudiante.nacionalidad,
        "ciudad_origen": estudiante.ciudad_origen,
        "especialidad": estudiante.especialidad,
        "nivel_espanol": estudiante.nivel_espanol,
        "tipo_visa": estudiante.tipo_visa,
        "estado": estudiante.estado,
        "documentos_estado": estudiante.documentos_estado,
        "notas": estudiante.notas,
        "created_at": estudiante.created_at.isoformat() if estudiante.created_at else None,
        "updated_at": estudiante.updated_at.isoformat() if estudiante.updated_at else None
    }


@app.put("/api/estudiantes/{estudiante_id}", tags=["Estudiantes"])
def actualizar_estudiante_publico(estudiante_id: int, datos: dict, db: Session = Depends(get_db)):
    """
    Actualiza datos de un estudiante (sin auth para estudiante)
    """
    from database.models import Estudiante as EstudianteModel
    from datetime import datetime
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Actualizar campos permitidos
    campos_permitidos = ['nombre', 'email', 'telefono', 'pasaporte', 'edad', 
                         'nacionalidad', 'ciudad_origen', 'especialidad', 
                         'nivel_espanol', 'tipo_visa']
    
    for campo in campos_permitidos:
        if campo in datos:
            setattr(estudiante, campo, datos[campo])
    
    estudiante.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(estudiante)
    
    return {
        "mensaje": "Datos actualizados correctamente",
        "estudiante": {
            "id": estudiante.id,
            "nombre": estudiante.nombre,
            "email": estudiante.email
        }
    }


@app.get("/api/estudiantes/{estudiante_id}/probabilidad-visa", tags=["Estudiantes"])
def calcular_probabilidad_visa(estudiante_id: int, db: Session = Depends(get_db)):
    """
    Calcula la probabilidad de aprobación de visa del estudiante
    """
    from database.models import Estudiante as EstudianteModel
    from api.calculadora_visa import CalculadoraProbabilidadVisa
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Preparar datos para el cálculo
    estudiante_data = {
        'nombre': estudiante.nombre,
        'email': estudiante.email,
        'telefono': estudiante.telefono,
        'pasaporte': estudiante.pasaporte,
        'edad': estudiante.edad,
        'nacionalidad': estudiante.nacionalidad,
        'ciudad_origen': estudiante.ciudad_origen,
        'especialidad': estudiante.especialidad,
        'nivel_espanol': estudiante.nivel_espanol,
        'tipo_visa': estudiante.tipo_visa
    }
    
    # Calcular probabilidad
    analisis = CalculadoraProbabilidadVisa.calcular_probabilidad(estudiante_data)
    
    return {
        'estudiante_id': estudiante_id,
        'estudiante_nombre': estudiante.nombre,
        'analisis': analisis
    }


@app.post("/api/documentos/{documento_id}/validar-ocr", tags=["Documentos - OCR"])
async def validar_documento_ocr(
    documento_id: int,
    db: Session = Depends(get_db)
):
    """
    Valida documento usando OCR inteligente
    Extrae información y detecta errores automáticamente
    """
    try:
        from api.ocr_processor import OCRProcessor
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Obtener documento
        cursor.execute("""
            SELECT tipo_documento, nombre_archivo, url_archivo
            FROM documentos
            WHERE id = %s
        """, (documento_id,))
        
        documento = cursor.fetchone()
        
        if not documento:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        tipo_doc, nombre_archivo, url_archivo = documento
        
        # Extraer base64 de la URL (formato: data:image/jpeg;base64,...)
        if not url_archivo or 'base64,' not in url_archivo:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Documento no contiene imagen válida")
        
        imagen_base64 = url_archivo.split('base64,')[1]
        
        # Procesar con OCR
        ocr = OCRProcessor()
        resultado = ocr.procesar_documento(imagen_base64, tipo_doc)
        
        if not resultado.get('exito'):
            cursor.close()
            conn.close()
            return {
                'exito': False,
                'error': resultado.get('error', 'Error desconocido'),
                'documento_id': documento_id
            }
        
        # Guardar resultados en DB
        validacion = resultado.get('validacion', {})
        
        cursor.execute("""
            UPDATE documentos
            SET 
                ocr_procesado = TRUE,
                ocr_texto_extraido = %s,
                ocr_datos_extraidos = %s,
                ocr_valido = %s,
                ocr_advertencias = %s,
                ocr_errores = %s,
                estado = CASE 
                    WHEN %s THEN 'aprobado'
                    WHEN array_length(%s, 1) > 0 THEN 'rechazado'
                    ELSE 'en_revision'
                END,
                updated_at = NOW()
            WHERE id = %s
        """, (
            resultado.get('texto_extraido', ''),
            str(validacion.get('datos_extraidos', {})),
            validacion.get('valido', False),
            str(validacion.get('advertencias', [])),
            str(validacion.get('errores', [])),
            validacion.get('valido', False),
            validacion.get('errores', []),
            documento_id
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Generar reporte legible
        reporte = ocr.generar_reporte_validacion(resultado)
        
        return {
            'exito': True,
            'documento_id': documento_id,
            'tipo_detectado': resultado.get('tipo_detectado'),
            'valido': validacion.get('valido', False),
            'datos_extraidos': validacion.get('datos_extraidos', {}),
            'advertencias': validacion.get('advertencias', []),
            'errores': validacion.get('errores', []),
            'reporte': reporte,
            'tiempo_procesamiento': resultado.get('tiempo_procesamiento', 0)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en validación OCR: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documentos/batch-validar-ocr", tags=["Documentos - OCR"])
async def validar_documentos_batch(
    estudiante_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """
    Valida todos los documentos de un estudiante en lote
    Útil para procesamiento masivo
    """
    verificar_token(credentials.credentials)
    
    try:
        from api.ocr_processor import OCRProcessor
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Obtener documentos no procesados
        cursor.execute("""
            SELECT id, tipo_documento
            FROM documentos
            WHERE estudiante_id = %s 
            AND (ocr_procesado IS NULL OR ocr_procesado = FALSE)
        """, (estudiante_id,))
        
        documentos = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not documentos:
            return {
                'exito': True,
                'mensaje': 'No hay documentos pendientes de validación',
                'procesados': 0
            }
        
        # Procesar cada documento
        resultados = []
        exitosos = 0
        
        for doc_id, tipo_doc in documentos:
            try:
                resultado = await validar_documento_ocr(doc_id, db)
                if resultado.get('exito'):
                    exitosos += 1
                resultados.append({
                    'documento_id': doc_id,
                    'tipo': tipo_doc,
                    'resultado': resultado
                })
            except Exception as e:
                resultados.append({
                    'documento_id': doc_id,
                    'tipo': tipo_doc,
                    'error': str(e)
                })
        
        return {
            'exito': True,
            'procesados': exitosos,
            'total': len(documentos),
            'resultados': resultados
        }
        
    except Exception as e:
        print(f"Error en validación batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/documentos/{documento_id}/ocr-report", tags=["Admin - Documentos"])
def obtener_reporte_ocr(
    documento_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """
    Obtiene reporte detallado de validación OCR de un documento
    """
    verificar_token(credentials.credentials)
    
    try:
        import os
        import psycopg2
        import ast
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                d.tipo_documento,
                d.nombre_archivo,
                d.estado,
                d.ocr_procesado,
                d.ocr_texto_extraido,
                d.ocr_datos_extraidos,
                d.ocr_valido,
                d.ocr_advertencias,
                d.ocr_errores,
                e.nombre as estudiante_nombre
            FROM documentos d
            JOIN estudiantes e ON d.estudiante_id = e.id
            WHERE d.id = %s
        """, (documento_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        (tipo_doc, nombre_archivo, estado, ocr_procesado, texto_extraido, 
         datos_extraidos, ocr_valido, advertencias, errores, estudiante) = row
        
        if not ocr_procesado:
            return {
                'documento_id': documento_id,
                'procesado': False,
                'mensaje': 'Documento no ha sido procesado por OCR'
            }
        
        # Parsear strings a objetos Python
        try:
            datos_dict = ast.literal_eval(datos_extraidos) if datos_extraidos else {}
            advertencias_list = ast.literal_eval(advertencias) if advertencias else []
            errores_list = ast.literal_eval(errores) if errores else []
        except:
            datos_dict = {}
            advertencias_list = []
            errores_list = []
        
        return {
            'documento_id': documento_id,
            'estudiante': estudiante,
            'tipo_documento': tipo_doc,
            'nombre_archivo': nombre_archivo,
            'estado': estado,
            'procesado': True,
            'valido': ocr_valido,
            'datos_extraidos': datos_dict,
            'advertencias': advertencias_list,
            'errores': errores_list,
            'texto_completo': texto_extraido
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error obteniendo reporte OCR: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/estudiantes/{estudiante_id}/documentos", tags=["Estudiantes"])
async def subir_documento(
    estudiante_id: int,
    tipo_documento: str,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Sube un documento para el estudiante
    """
    import base64
    from datetime import datetime
    
    # Verificar que el estudiante existe
    from database.models import Estudiante as EstudianteModel
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Validar tipo de archivo
    allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    file_extension = archivo.filename[archivo.filename.rfind('.'):].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de archivo no permitido. Use: {', '.join(allowed_extensions)}"
        )
    
    # Leer archivo y convertir a base64
    contenido = await archivo.read()
    tamano_bytes = len(contenido)
    
    # Validar tamaño (máximo 5MB)
    if tamano_bytes > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Archivo muy grande. Máximo 5MB")
    
    # Convertir a base64 para almacenar en DB
    contenido_base64 = base64.b64encode(contenido).decode('utf-8')
    url_archivo = f"data:application/{file_extension[1:]};base64,{contenido_base64}"
    
    # Guardar en base de datos
    try:
        cursor = db.connection().connection.cursor()
        cursor.execute("""
            INSERT INTO documentos 
            (estudiante_id, tipo_documento, nombre_archivo, url_archivo, tamano_bytes, estado, created_at)
            VALUES (%s, %s, %s, %s, %s, 'pendiente', %s)
            RETURNING id
        """, (estudiante_id, tipo_documento, archivo.filename, url_archivo, tamano_bytes, datetime.utcnow()))
        
        documento_id = cursor.fetchone()[0]
        db.commit()
        
        # Actualizar estado de documentos del estudiante
        estudiante.documentos_estado = 'en_revision'
        db.commit()
        
        return {
            "mensaje": "Documento subido correctamente",
            "documento_id": documento_id,
            "nombre_archivo": archivo.filename,
            "tamano_bytes": tamano_bytes
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar documento: {str(e)}")


@app.get("/api/estudiantes/{estudiante_id}/documentos", tags=["Estudiantes"])
def listar_documentos(estudiante_id: int, db: Session = Depends(get_db)):
    """
    Lista todos los documentos de un estudiante
    """
    from database.models import Estudiante as EstudianteModel
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    try:
        cursor = db.connection().connection.cursor()
        cursor.execute("""
            SELECT id, tipo_documento, nombre_archivo, tamano_bytes, estado, notas, created_at
            FROM documentos
            WHERE estudiante_id = %s
            ORDER BY created_at DESC
        """, (estudiante_id,))
        
        documentos = []
        for row in cursor.fetchall():
            documentos.append({
                'id': row[0],
                'tipo_documento': row[1],
                'nombre_archivo': row[2],
                'tamano_bytes': row[3],
                'estado': row[4],
                'notas': row[5],
                'created_at': row[6].isoformat() if row[6] else None
            })
        
        return {
            'total': len(documentos),
            'documentos': documentos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar documentos: {str(e)}")


@app.get("/api/estudiantes/{estudiante_id}/reporte-pdf", tags=["Reportes"])
def generar_reporte_pdf(estudiante_id: int, tipo: str = 'completo', db: Session = Depends(get_db)):
    """
    Genera un PDF con el reporte del estudiante
    tipo: 'completo' o 'analisis'
    """
    from database.models import Estudiante as EstudianteModel
    from api.generador_pdf import GeneradorReportesPDF
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante_data = {
        'id': estudiante.id,
        'nombre': estudiante.nombre,
        'email': estudiante.email,
        'telefono': estudiante.telefono,
        'pasaporte': estudiante.pasaporte,
        'edad': estudiante.edad,
        'nacionalidad': estudiante.nacionalidad,
        'ciudad_origen': estudiante.ciudad_origen,
        'especialidad': estudiante.especialidad,
        'nivel_espanol': estudiante.nivel_espanol,
        'tipo_visa': estudiante.tipo_visa,
        'estado': estudiante.estado,
        'documentos_estado': estudiante.documentos_estado,
        'notas': estudiante.notas
    }
    
    if tipo == 'analisis':
        # Generar análisis de visa
        from api.calculadora_visa import CalculadoraProbabilidadVisa
        analisis = CalculadoraProbabilidadVisa.calcular_probabilidad(estudiante_data)
        pdf_buffer = GeneradorReportesPDF.generar_reporte_analisis_visa(estudiante_data, analisis)
        filename = f"analisis_visa_{estudiante.id}.pdf"
    else:
        # Generar reporte completo
        pdf_buffer = GeneradorReportesPDF.generar_reporte_completo_estudiante(estudiante_data)
        filename = f"reporte_estudiante_{estudiante.id}.pdf"
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# ============================================================================
# GENERACIÓN DE DOCUMENTOS OFICIALES (ADMIN)
# ============================================================================

@app.post("/api/admin/estudiantes/{estudiante_id}/generar-documentos", tags=["Admin - Documentos"])
def generar_documentos_estudiante(
    estudiante_id: int,
    tipos_documentos: List[str],
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """
    Genera documentos oficiales para un estudiante
    tipos_documentos: ['carta_aceptacion', 'carta_motivacion', 'formulario_solicitud', 'certificado_matricula']
    """
    verificar_token(credentials.credentials)
    
    from database.models import Estudiante as EstudianteModel
    from api.generador_documentos import GeneradorDocumentosOficiales
    import base64
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    datos_estudiante = {
        'id': estudiante.id,
        'nombre': estudiante.nombre,
        'email': estudiante.email,
        'telefono': estudiante.telefono,
        'pasaporte': estudiante.pasaporte,
        'edad': estudiante.edad,
        'nacionalidad': estudiante.nacionalidad,
        'ciudad_origen': estudiante.ciudad_origen,
        'especialidad': estudiante.especialidad,
        'nivel_espanol': estudiante.nivel_espanol,
        'tipo_visa': estudiante.tipo_visa
    }
    
    documentos_generados = []
    
    for tipo in tipos_documentos:
        try:
            # Generar PDF según tipo
            if tipo == 'carta_aceptacion':
                pdf_buffer = GeneradorDocumentosOficiales.generar_carta_aceptacion(datos_estudiante)
                nombre = f"Carta_Aceptacion_{estudiante.id}.pdf"
            elif tipo == 'carta_motivacion':
                pdf_buffer = GeneradorDocumentosOficiales.generar_carta_motivacion(datos_estudiante)
                nombre = f"Carta_Motivacion_{estudiante.id}.pdf"
            elif tipo == 'formulario_solicitud':
                pdf_buffer = GeneradorDocumentosOficiales.generar_formulario_solicitud(datos_estudiante)
                nombre = f"Formulario_Solicitud_{estudiante.id}.pdf"
            elif tipo == 'certificado_matricula':
                pdf_buffer = GeneradorDocumentosOficiales.generar_certificado_matricula(datos_estudiante)
                nombre = f"Certificado_Matricula_{estudiante.id}.pdf"
            else:
                continue
            
            # Convertir a base64 para almacenar
            pdf_content = pdf_buffer.read()
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            
            # Guardar en base de datos usando SQL directo
            import os
            import psycopg2
            conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO documentos_generados 
                (estudiante_id, tipo_documento, nombre_archivo, contenido_pdf, estado, generado_por)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (estudiante_id, tipo, nombre, pdf_base64, 'generado', 'admin'))
            
            doc_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            
            documentos_generados.append({
                'id': doc_id,
                'tipo': tipo,
                'nombre': nombre,
                'estado': 'generado'
            })
            
        except Exception as e:
            print(f"Error generando documento {tipo}: {e}")
            continue
    
    return {
        'estudiante_id': estudiante_id,
        'documentos_generados': documentos_generados,
        'total': len(documentos_generados)
    }


@app.get("/api/admin/documentos-generados", tags=["Admin - Documentos"])
def listar_documentos_generados(
    estudiante_id: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Lista todos los documentos generados con filtros opcionales"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    query = """
        SELECT dg.id, dg.estudiante_id, dg.tipo_documento, dg.nombre_archivo,
               dg.estado, dg.fecha_generacion, dg.enviado_estudiante,
               e.nombre as estudiante_nombre
        FROM documentos_generados dg
        JOIN estudiantes e ON dg.estudiante_id = e.id
        WHERE 1=1
    """
    params = []
    
    if estudiante_id:
        query += " AND dg.estudiante_id = %s"
        params.append(estudiante_id)
    
    if estado:
        query += " AND dg.estado = %s"
        params.append(estado)
    
    query += " ORDER BY dg.fecha_generacion DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    documentos = []
    for row in rows:
        documentos.append({
            'id': row[0],
            'estudiante_id': row[1],
            'tipo_documento': row[2],
            'nombre_archivo': row[3],
            'estado': row[4],
            'fecha_generacion': row[5].isoformat() if row[5] else None,
            'enviado_estudiante': row[6],
            'estudiante_nombre': row[7]
        })
    
    cursor.close()
    conn.close()
    
    return documentos


@app.get("/api/admin/documentos-generados/{documento_id}/descargar", tags=["Admin - Documentos"])
def descargar_documento_generado(
    documento_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Descarga un documento generado"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    import base64
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT nombre_archivo, contenido_pdf
        FROM documentos_generados
        WHERE id = %s
    """, (documento_id,))
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    nombre_archivo, contenido_base64 = row
    pdf_content = base64.b64decode(contenido_base64)
    
    from io import BytesIO
    buffer = BytesIO(pdf_content)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={nombre_archivo}"}
    )


@app.put("/api/admin/documentos-generados/{documento_id}/aprobar", tags=["Admin - Documentos"])
def aprobar_documento_generado(
    documento_id: int,
    enviar_a_estudiante: bool = True,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Aprueba un documento y opcionalmente lo envía al estudiante"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE documentos_generados
        SET estado = 'aprobado',
            fecha_aprobacion = CURRENT_TIMESTAMP,
            enviado_estudiante = %s,
            aprobado_por = 'admin'
        WHERE id = %s
        RETURNING estudiante_id
    """, (enviar_a_estudiante, documento_id))
    
    result = cursor.fetchone()
    if not result:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    estudiante_id = result[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    # Enviar email al estudiante con el documento adjunto
    if enviar_a_estudiante:
        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.application import MIMEApplication
            import base64
            
            # Obtener email del estudiante
            cursor2 = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require').cursor()
            cursor2.execute("""
                SELECT e.email, e.nombre, dg.nombre_archivo, dg.tipo_documento
                FROM documentos_generados dg
                JOIN estudiantes e ON dg.estudiante_id = e.id
                WHERE dg.id = %s
            """, (documento_id,))
            
            row = cursor2.fetchone()
            if row:
                estudiante_email, estudiante_nombre, nombre_archivo, tipo_doc = row
                cursor2.close()
                
                # Configurar email
                msg = MIMEMultipart()
                msg['From'] = os.getenv('SMTP_USER')
                msg['To'] = estudiante_email
                msg['Subject'] = f'Documento Aprobado: {tipo_doc.replace("_", " ").title()}'
                
                # Cuerpo del email
                body = f"""
                <html>
                <body>
                    <h2>¡Hola {estudiante_nombre}!</h2>
                    <p>Tu documento <strong>{tipo_doc.replace("_", " ").title()}</strong> ha sido aprobado y está listo.</p>
                    <p>Puedes descargarlo desde tu perfil o encontrarlo adjunto en este correo.</p>
                    <br>
                    <p>Saludos,<br>Equipo de Estudio Visa España</p>
                </body>
                </html>
                """
                msg.attach(MIMEText(body, 'html'))
                
                # Adjuntar PDF
                pdf_bytes = base64.b64decode(pdf_content)
                pdf_attachment = MIMEApplication(pdf_bytes, _subtype='pdf')
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename=nombre_archivo)
                msg.attach(pdf_attachment)
                
                # Enviar
                smtp = smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
                smtp.starttls()
                smtp.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
                smtp.send_message(msg)
                smtp.quit()
        except Exception as e:
            print(f"Error enviando email: {str(e)}")
    
    return {
        'mensaje': 'Documento aprobado correctamente',
        'enviado_estudiante': enviar_a_estudiante
    }


# ============================================================================
# GESTIÓN DE CURSOS
# ============================================================================

@app.get("/api/admin/cursos", tags=["Admin - Cursos"])
def listar_cursos(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Lista todos los cursos disponibles"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nombre, descripcion, duracion_meses, precio_eur, ciudad,
               nivel_espanol_requerido, cupos_disponibles, activo
        FROM cursos
        ORDER BY nombre
    """)
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    cursos = []
    for row in rows:
        cursos.append({
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'duracion_meses': row[3],
            'precio_eur': float(row[4]) if row[4] else None,
            'ciudad': row[5],
            'nivel_espanol_requerido': row[6],
            'cupos_disponibles': row[7],
            'activo': row[8]
        })
    
    return cursos


@app.post("/api/admin/cursos", tags=["Admin - Cursos"])
def crear_curso(
    curso: dict,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Crea un nuevo curso"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO cursos (nombre, descripcion, duracion_meses, precio_eur, ciudad,
                           nivel_espanol_requerido, cupos_disponibles, activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        curso.get('nombre'),
        curso.get('descripcion'),
        curso.get('duracion_meses'),
        curso.get('precio_eur'),
        curso.get('ciudad'),
        curso.get('nivel_espanol_requerido'),
        curso.get('cupos_disponibles', 0),
        curso.get('activo', True)
    ))
    
    curso_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    return {'id': curso_id, 'mensaje': 'Curso creado correctamente'}


@app.put("/api/admin/cursos/{curso_id}", tags=["Admin - Cursos"])
def actualizar_curso(
    curso_id: int,
    curso: dict,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Actualiza un curso"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE cursos
        SET nombre = %s, descripcion = %s, duracion_meses = %s, precio_eur = %s,
            ciudad = %s, nivel_espanol_requerido = %s, cupos_disponibles = %s,
            activo = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    """, (
        curso.get('nombre'),
        curso.get('descripcion'),
        curso.get('duracion_meses'),
        curso.get('precio_eur'),
        curso.get('ciudad'),
        curso.get('nivel_espanol_requerido'),
        curso.get('cupos_disponibles'),
        curso.get('activo'),
        curso_id
    ))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {'mensaje': 'Curso actualizado correctamente'}


@app.post("/api/admin/estudiantes/{estudiante_id}/asignar-curso", tags=["Admin - Cursos"])
def asignar_curso(
    estudiante_id: int,
    curso_id: int = Query(...),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Asigna un curso a un estudiante"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE estudiantes
        SET curso_asignado_id = %s
        WHERE id = %s
    """, (curso_id, estudiante_id))
    
    conn.commit()
    
    # Obtener datos del curso y estudiante para el email
    cursor.execute("""
        SELECT c.nombre, c.duracion_meses, c.ciudad, c.nivel_espanol_requerido, c.precio_eur,
               e.nombre, e.email
        FROM cursos c
        JOIN estudiantes e ON e.id = %s
        WHERE c.id = %s
    """, (estudiante_id, curso_id))
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # Enviar email de notificación
    if row:
        try:
            from api.email_utils import email_curso_asignado
            curso_detalles = {
                'duracion_meses': row[1],
                'ciudad': row[2],
                'nivel_espanol_requerido': row[3],
                'precio_eur': row[4]
            }
            email_curso_asignado(row[5], row[6], row[0], curso_detalles)
        except Exception as e:
            print(f"[WARN] Error enviando email: {e}")
    
    return {'mensaje': 'Curso asignado correctamente'}


@app.get("/api/admin/estudiantes/{estudiante_id}/sugerir-cursos", tags=["Admin - Cursos"])
def sugerir_cursos(
    estudiante_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Sugiere cursos basados en el perfil del estudiante"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    # Obtener datos del estudiante
    cursor.execute("""
        SELECT especialidad, nivel_idioma, fondos_disponibles
        FROM estudiantes
        WHERE id = %s
    """, (estudiante_id,))
    
    estudiante = cursor.fetchone()
    if not estudiante:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    especialidad, nivel_idioma, fondos = estudiante
    
    # Mapear nivel de idioma a nivel español requerido
    nivel_map = {
        'basico': ['A1', 'A2', 'Básico', 'Principiante'],
        'intermedio': ['A1', 'A2', 'B1', 'Intermedio', 'Básico', 'Principiante'],
        'avanzado': ['A1', 'A2', 'B1', 'B2', 'C1', 'Avanzado', 'Intermedio', 'Básico', 'Principiante']
    }
    
    niveles_aceptables = nivel_map.get(nivel_idioma.lower() if nivel_idioma else 'basico', ['A1', 'A2'])
    
    # Buscar cursos compatibles
    cursor.execute("""
        SELECT id, nombre, descripcion, duracion_meses, precio_eur, ciudad,
               nivel_espanol_requerido, cupos_disponibles
        FROM cursos
        WHERE activo = TRUE
          AND cupos_disponibles > 0
          AND precio_eur <= %s
        ORDER BY 
            CASE 
                WHEN LOWER(descripcion) LIKE %s THEN 1
                WHEN LOWER(nombre) LIKE %s THEN 2
                ELSE 3
            END,
            precio_eur ASC
        LIMIT 5
    """, (fondos, f'%{especialidad.lower()}%' if especialidad else '%%', f'%{especialidad.lower()}%' if especialidad else '%%'))
    
    cursos = []
    for row in cursor.fetchall():
        # Calcular score de compatibilidad
        score = 100
        nivel_curso = row[6] if row[6] else ''
        
        # Penalizar si el nivel no es compatible
        if nivel_curso and nivel_curso not in niveles_aceptables:
            score -= 30
        
        # Bonus si coincide con especialidad
        if especialidad and (especialidad.lower() in row[1].lower() or 
                            (row[2] and especialidad.lower() in row[2].lower())):
            score += 20
        
        # Penalizar si está cerca del límite de fondos
        if row[4] and fondos:
            ratio = row[4] / fondos
            if ratio > 0.8:
                score -= 15
        
        cursos.append({
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'duracion_meses': row[3],
            'precio_eur': float(row[4]) if row[4] else None,
            'ciudad': row[5],
            'nivel_espanol_requerido': row[6],
            'cupos_disponibles': row[7],
            'compatibilidad': max(0, min(100, score)),
            'razon': 'Compatible con tu perfil y fondos disponibles'
        })
    
    # Ordenar por compatibilidad
    cursos.sort(key=lambda x: x['compatibilidad'], reverse=True)
    
    cursor.close()
    conn.close()
    
    return {
        'estudiante_id': estudiante_id,
        'cursos_sugeridos': cursos,
        'criterios': {
            'especialidad': especialidad,
            'nivel_idioma': nivel_idioma,
            'fondos_disponibles': float(fondos) if fondos else None
        }
    }


# ============================================================================
# GESTIÓN DE ALOJAMIENTOS
# ============================================================================

@app.get("/api/admin/alojamientos", tags=["Admin - Alojamientos"])
def listar_alojamientos(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Lista todos los alojamientos"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, tipo, direccion, ciudad, precio_mensual_eur, capacidad,
               disponible, descripcion, servicios
        FROM alojamientos
        ORDER BY ciudad, tipo
    """)
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    alojamientos = []
    for row in rows:
        alojamientos.append({
            'id': row[0],
            'tipo': row[1],
            'direccion': row[2],
            'ciudad': row[3],
            'precio_mensual_eur': float(row[4]) if row[4] else None,
            'capacidad': row[5],
            'disponible': row[6],
            'descripcion': row[7],
            'servicios': row[8]
        })
    
    return alojamientos


@app.post("/api/admin/alojamientos", tags=["Admin - Alojamientos"])
def crear_alojamiento(
    alojamiento: dict,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Crea un nuevo alojamiento"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO alojamientos (tipo, direccion, ciudad, precio_mensual_eur,
                                 capacidad, disponible, descripcion, servicios)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        alojamiento.get('tipo'),
        alojamiento.get('direccion'),
        alojamiento.get('ciudad'),
        alojamiento.get('precio_mensual_eur'),
        alojamiento.get('capacidad', 1),
        alojamiento.get('disponible', True),
        alojamiento.get('descripcion'),
        alojamiento.get('servicios')
    ))
    
    alojamiento_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    return {'id': alojamiento_id, 'mensaje': 'Alojamiento creado correctamente'}


@app.put("/api/admin/alojamientos/{alojamiento_id}", tags=["Admin - Alojamientos"])
def actualizar_alojamiento(
    alojamiento_id: int,
    alojamiento: dict,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Actualiza un alojamiento"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE alojamientos
        SET tipo = %s, direccion = %s, ciudad = %s, precio_mensual_eur = %s,
            capacidad = %s, disponible = %s, descripcion = %s, servicios = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    """, (
        alojamiento.get('tipo'),
        alojamiento.get('direccion'),
        alojamiento.get('ciudad'),
        alojamiento.get('precio_mensual_eur'),
        alojamiento.get('capacidad'),
        alojamiento.get('disponible'),
        alojamiento.get('descripcion'),
        alojamiento.get('servicios'),
        alojamiento_id
    ))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {'mensaje': 'Alojamiento actualizado correctamente'}


@app.post("/api/admin/estudiantes/{estudiante_id}/asignar-alojamiento", tags=["Admin - Alojamientos"])
def asignar_alojamiento(
    estudiante_id: int,
    alojamiento_id: int = Query(...),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Asigna un alojamiento a un estudiante"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE estudiantes
        SET alojamiento_asignado_id = %s
        WHERE id = %s
    """, (alojamiento_id, estudiante_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {'mensaje': 'Alojamiento asignado correctamente'}


# ============================================================================
# REPORTES
# ============================================================================

@app.get("/api/estudiantes/{estudiante_id}/descargar-expediente", tags=["Estudiantes"])
def descargar_expediente_zip(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    """Descarga ZIP con todos los documentos del expediente"""
    import os
    import psycopg2
    import zipfile
    from io import BytesIO
    import base64
    from fastapi.responses import StreamingResponse
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    # Obtener datos del estudiante
    cursor.execute("""
        SELECT nombre, pasaporte
        FROM estudiantes
        WHERE id = %s
    """, (estudiante_id,))
    
    estudiante = cursor.fetchone()
    if not estudiante:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    nombre, pasaporte = estudiante
    
    # Obtener documentos generados
    cursor.execute("""
        SELECT nombre_archivo, contenido_pdf, tipo_documento
        FROM documentos_generados
        WHERE estudiante_id = %s AND estado = 'aprobado'
    """, (estudiante_id,))
    
    docs_generados = cursor.fetchall()
    
    # Obtener documentos subidos
    cursor.execute("""
        SELECT nombre_archivo, contenido, tipo_documento
        FROM documentos
        WHERE estudiante_id = %s
    """, (estudiante_id,))
    
    docs_subidos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Crear ZIP en memoria
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Agregar documentos generados
        for doc in docs_generados:
            nombre_archivo, contenido_b64, tipo = doc
            contenido = base64.b64decode(contenido_b64)
            zip_file.writestr(f"generados/{nombre_archivo}", contenido)
        
        # Agregar documentos subidos
        for doc in docs_subidos:
            nombre_archivo, contenido_b64, tipo = doc
            if contenido_b64:
                contenido = base64.b64decode(contenido_b64)
                zip_file.writestr(f"subidos/{nombre_archivo}", contenido)
    
    zip_buffer.seek(0)
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename=expediente_{pasaporte}_{nombre.replace(' ', '_')}.zip"
        }
    )


@app.put("/api/admin/estudiantes/{estudiante_id}/actualizar-estado", tags=["Admin"])
def actualizar_estado_estudiante(
    estudiante_id: int,
    nuevo_estado: str,
    notas: Optional[str] = None,
    fecha_evento: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Actualiza estado del estudiante (cita_consular, visa_aprobada, visa_rechazada, llegada_espana)"""
    verificar_token(credentials.credentials)
    
    from database.models import Estudiante as EstudianteModel
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estados_validos = ['pendiente', 'aprobado', 'rechazado', 'cita_consular', 'visa_aprobada', 'visa_rechazada', 'llegada_espana']
    
    if nuevo_estado not in estados_validos:
        raise HTTPException(status_code=400, detail="Estado no válido")
    
    estudiante.estado = nuevo_estado
    if notas:
        estudiante.notas = notas
    estudiante.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"mensaje": "Estado actualizado correctamente", "nuevo_estado": nuevo_estado}


@app.get("/api/admin/alertas-documentos", tags=["Admin"])
def obtener_alertas_documentos(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Obtiene lista de estudiantes con documentos faltantes o incompletos"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT e.id, e.nombre, e.email, e.estado, e.created_at,
               COUNT(d.id) as docs_subidos,
               COUNT(dg.id) as docs_generados
        FROM estudiantes e
        LEFT JOIN documentos d ON e.id = d.estudiante_id
        LEFT JOIN documentos_generados dg ON e.id = dg.estudiante_id AND dg.estado = 'aprobado'
        WHERE e.estado != 'rechazado'
        GROUP BY e.id, e.nombre, e.email, e.estado, e.created_at
        HAVING COUNT(d.id) < 3 OR COUNT(dg.id) < 4
        ORDER BY e.created_at ASC
    """)
    
    alertas = []
    for row in cursor.fetchall():
        dias_desde_registro = (datetime.now() - row[4]).days if row[4] else 0
        alertas.append({
            'estudiante_id': row[0],
            'nombre': row[1],
            'email': row[2],
            'estado': row[3],
            'docs_subidos': row[5],
            'docs_generados': row[6],
            'dias_desde_registro': dias_desde_registro,
            'urgencia': 'alta' if dias_desde_registro > 7 else 'media' if dias_desde_registro > 3 else 'baja'
        })
    
    cursor.close()
    conn.close()
    
    return {'total_alertas': len(alertas), 'alertas': alertas}


@app.post("/api/admin/enviar-recordatorios", tags=["Admin"])
def enviar_recordatorios_masivos(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Envía recordatorios por email a estudiantes con documentos pendientes"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    from api.email_utils import email_recordatorio_documentos
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    # Buscar estudiantes con documentación incompleta
    cursor.execute("""
        SELECT e.id, e.nombre, e.email, e.created_at,
               COUNT(d.id) as docs_subidos
        FROM estudiantes e
        LEFT JOIN documentos d ON e.id = d.estudiante_id
        WHERE e.estado = 'pendiente'
        GROUP BY e.id, e.nombre, e.email, e.created_at
        HAVING COUNT(d.id) < 3
    """)
    
    enviados = 0
    for row in cursor.fetchall():
        est_id, nombre, email, created_at, docs_count = row
        dias_desde_registro = (datetime.now() - created_at).days if created_at else 0
        
        # Solo enviar si han pasado más de 3 días
        if dias_desde_registro > 3:
            docs_faltantes = []
            if docs_count < 1:
                docs_faltantes.append("Título universitario")
            if docs_count < 2:
                docs_faltantes.append("Pasaporte")
            if docs_count < 3:
                docs_faltantes.append("Extracto bancario")
            
            try:
                if email_recordatorio_documentos(nombre, email, docs_faltantes):
                    enviados += 1
            except Exception as e:
                print(f"Error enviando a {email}: {e}")
    
    cursor.close()
    conn.close()
    
    return {'mensaje': f'Recordatorios enviados: {enviados}'}


@app.get("/api/admin/reportes/estudiantes", tags=["Admin - Reportes"])
def reporte_estudiantes(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Genera reporte detallado de estudiantes"""
    verificar_token(credentials.credentials)
    
    import os
    import psycopg2
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
    cursor = conn.cursor()
    
    query = """
        SELECT e.id, e.nombre, e.email, e.nacionalidad, e.especialidad,
               e.estado, e.created_at, c.nombre as curso, a.tipo as alojamiento
        FROM estudiantes e
        LEFT JOIN cursos c ON e.curso_asignado_id = c.id
        LEFT JOIN alojamientos a ON e.alojamiento_asignado_id = a.id
        WHERE 1=1
    """
    params = []
    
    if fecha_inicio:
        query += " AND e.created_at >= %s"
        params.append(fecha_inicio)
    
    if fecha_fin:
        query += " AND e.created_at <= %s"
        params.append(fecha_fin)
    
    query += " ORDER BY e.created_at DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    estudiantes = []
    for row in rows:
        estudiantes.append({
            'id': row[0],
            'nombre': row[1],
            'email': row[2],
            'nacionalidad': row[3],
            'especialidad': row[4],
            'estado': row[5],
            'fecha_registro': row[6].isoformat() if row[6] else None,
            'curso': row[7],
            'alojamiento': row[8]
        })
    
    cursor.close()
    conn.close()
    
    return {
        'total': len(estudiantes),
        'estudiantes': estudiantes,
        'fecha_generacion': datetime.now().isoformat()
    }


@app.get("/api/estudiantes/{estudiante_id}/estado", tags=["Estudiantes"])
def consultar_estado(estudiante_id: int, db: Session = Depends(get_db)):
    """
    Estudiante consulta su estado (sin auth por simplicidad en MVP)
    """
    try:
        # Query solo los campos que necesitamos
        result = db.execute(
            text("""
                SELECT id, nombre, email, tipo_visa, estado, created_at, curso_asignado_id
                FROM estudiantes 
                WHERE id = :estudiante_id
            """),
            {"estudiante_id": estudiante_id}
        ).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        return {
            "nombre": result[1] or "Estudiante",
            "estado_procesamiento": result[4] or "pendiente",
            "estado_visa": result[3] or "estudiante",
            "fecha_registro": result[5].isoformat() if result[5] else None,
            "curso_seleccionado": result[6],
            "mensaje": _obtener_mensaje_estado(result[4] or "pendiente")
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Error en consultar_estado: {e}")
        raise HTTPException(status_code=500, detail=f"Error consultando estado: {str(e)}")


def _obtener_mensaje_estado(estado: str) -> str:
    """Mensajes amigables por estado"""
    mensajes = {
        "pendiente": "Tu solicitud ha sido recibida. Estamos procesando tu información.",
        "en_revision": "Tu caso está siendo revisado por nuestro equipo.",
        "aprobado": "¡Felicidades! Tu solicitud ha sido aprobada. Te contactaremos pronto.",
        "rechazado": "Necesitamos información adicional. Te contactaremos.",
        "completado": "¡Proceso completado! Te hemos enviado toda la información."
    }
    return mensajes.get(estado, "En proceso")


# ============================================================================
# MENSAJERÍA INTERNA
# ============================================================================

@app.get("/api/estudiantes/{estudiante_id}/mensajes", tags=["Mensajería"])
def obtener_mensajes(estudiante_id: int, db: Session = Depends(get_db)):
    """Obtiene todos los mensajes de un estudiante"""
    from database.models import Estudiante as EstudianteModel
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    try:
        cursor = db.connection().connection.cursor()
        cursor.execute("""
            SELECT id, remitente, mensaje, leido, created_at
            FROM mensajes
            WHERE estudiante_id = %s
            ORDER BY created_at ASC
        """, (estudiante_id,))
        
        mensajes = []
        for row in cursor.fetchall():
            mensajes.append({
                'id': row[0],
                'remitente': row[1],
                'mensaje': row[2],
                'leido': row[3],
                'created_at': row[4].isoformat() if row[4] else None
            })
        
        return {'total': len(mensajes), 'mensajes': mensajes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/api/estudiantes/{estudiante_id}/mensajes", tags=["Mensajería"])
def enviar_mensaje(estudiante_id: int, datos: dict, db: Session = Depends(get_db)):
    """Envía un mensaje (estudiante o admin)"""
    from database.models import Estudiante as EstudianteModel
    from datetime import datetime
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    remitente = datos.get('remitente', 'estudiante')  # 'estudiante' o 'admin'
    mensaje = datos.get('mensaje', '')
    
    if not mensaje:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
    
    try:
        cursor = db.connection().connection.cursor()
        cursor.execute("""
            INSERT INTO mensajes (estudiante_id, remitente, mensaje, created_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (estudiante_id, remitente, mensaje, datetime.utcnow()))
        
        mensaje_id = cursor.fetchone()[0]
        db.commit()
        
        return {
            'mensaje_id': mensaje_id,
            'mensaje': 'Mensaje enviado correctamente'
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/api/mensajes/{mensaje_id}/marcar-leido", tags=["Mensajería"])
def marcar_mensaje_leido(mensaje_id: int, db: Session = Depends(get_db)):
    """Marca un mensaje como leído"""
    try:
        cursor = db.connection().connection.cursor()
        cursor.execute("""
            UPDATE mensajes 
            SET leido = TRUE 
            WHERE id = %s
        """, (mensaje_id,))
        
        db.commit()
        
        return {'mensaje': 'Mensaje marcado como leído'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# ENDPOINTS ADMIN (Requieren autenticación)
# ============================================================================

@app.get("/api/admin/estudiantes", response_model=List[Dict], tags=["Admin"])
def listar_estudiantes(
    estado: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Lista todos los estudiantes con filtros opcionales"""
    from database.models import Estudiante as EstudianteModel
    
    query = db.query(EstudianteModel)
    
    if estado:
        query = query.filter(EstudianteModel.estado == estado)
    
    estudiantes = query.order_by(EstudianteModel.created_at.desc()).offset(skip).limit(limit).all()
    
    return [{
        'id': e.id,
        'nombre_completo': e.nombre or f"Estudiante {e.id}",
        'email': e.email or f"estudiante{e.id}@example.com",
        'especialidad_interes': e.especialidad or e.tipo_visa or 'No especificado',
        'estado_procesamiento': e.estado,
        'prioridad': 'BAJA',  # Valor por defecto
        'documentos_subidos': 0,
        'documentos_generados': 0,
        'dias_desde_registro': (datetime.now() - e.created_at).days if e.created_at else 0,
        'created_at': e.created_at.isoformat() if e.created_at else None
    } for e in estudiantes]


@app.get("/api/admin/estudiantes/{estudiante_id}", response_model=EstudianteResponse, tags=["Admin"])
def obtener_estudiante(
    estudiante_id: int,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Detalle completo de un estudiante"""
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return EstudianteResponse.from_orm(estudiante)


@app.put("/api/admin/estudiantes/{estudiante_id}", tags=["Admin"])
def actualizar_estudiante(
    estudiante_id: int,
    datos: EstudianteUpdate,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Actualiza información de estudiante"""
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Actualizar campos
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(estudiante, campo, valor)
    
    db.commit()
    db.refresh(estudiante)
    
    return {"message": "Estudiante actualizado correctamente"}


@app.post("/api/admin/estudiantes/{estudiante_id}/aprobar", tags=["Admin"])
def aprobar_estudiante(
    estudiante_id: int,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Aprobar estudiante para envío"""
    from database.models import Estudiante as EstudianteModel
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante.estado = 'aprobado'
    estudiante.updated_at = datetime.utcnow()
    db.commit()
    
    # Enviar email de notificación
    try:
        from api.email_utils import email_aprobacion
        email_aprobacion(estudiante.nombre, estudiante.email)
    except Exception as e:
        print(f"⚠️ Error enviando email: {e}")
    
    return {"message": "Estudiante aprobado correctamente", "id": estudiante_id}


@app.post("/api/admin/estudiantes/{estudiante_id}/rechazar", tags=["Admin"])
def rechazar_estudiante(
    estudiante_id: int,
    motivo: str,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Rechazar estudiante y solicitar correcciones"""
    from database.models import Estudiante as EstudianteModel
    
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante.estado = 'rechazado'
    estudiante.notas = motivo
    estudiante.updated_at = datetime.utcnow()
    db.commit()
    
    # Enviar email de notificación
    try:
        from api.email_utils import email_rechazo
        email_rechazo(estudiante.nombre, estudiante.email, motivo)
    except Exception as e:
        print(f"⚠️ Error enviando email: {e}")
    
    return {"message": "Estudiante rechazado", "id": estudiante_id, "motivo": motivo}


@app.get("/api/admin/estadisticas", response_model=EstadisticasResponse, tags=["Admin"])
def obtener_estadisticas(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Estadísticas del dashboard"""
    from database.models import Estudiante as EstudianteModel
    
    # Contar estudiantes por estado
    total = db.query(EstudianteModel).count()
    pendientes = db.query(EstudianteModel).filter(EstudianteModel.estado == 'pendiente').count()
    aprobados = db.query(EstudianteModel).filter(EstudianteModel.estado == 'aprobado').count()
    rechazados = db.query(EstudianteModel).filter(EstudianteModel.estado == 'rechazado').count()
    
    return EstadisticasResponse(
        total_estudiantes=total,
        pendientes_revision=pendientes,
        aprobados=aprobados,
        enviados=aprobados,  # Por ahora enviados = aprobados
        por_especialidad={}  # TODO: implementar después
    )


# ============================================================================
# CURSOS - Endpoints para gestión de cursos
# ============================================================================

@app.get("/api/cursos", tags=["Cursos"])
def listar_cursos(
    especialidad: Optional[str] = None,
    ciudad: Optional[str] = None,
    precio_max: Optional[float] = None,
    nivel_idioma: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Lista cursos disponibles con filtros"""
    from modules.cursos import GestorCursos
    
    cursos = GestorCursos.filtrar_cursos(
        especialidad=especialidad,
        ciudad=ciudad,
        precio_max=precio_max,
        nivel_idioma=nivel_idioma
    )
    
    return {
        'total': len(cursos),
        'cursos': [
            {
                'id': c.id,
                'nombre': c.nombre,
                'escuela': c.escuela,
                'ciudad': c.ciudad,
                'especialidad': c.especialidad,
                'precio': c.precio,
                'duracion_meses': c.duracion_meses,
                'nivel_minimo_espanol': c.nivel_minimo_espanol,
                'fecha_inicio': c.fecha_inicio.isoformat() if c.fecha_inicio else None,
                'disponible': c.disponible
            }
            for c in cursos[skip:skip+limit]
        ]
    }


@app.get("/api/cursos/{curso_id}", tags=["Cursos"])
def obtener_curso(curso_id: int, db: Session = Depends(get_db)):
    """Obtiene detalles de un curso específico"""
    from modules.cursos import GestorCursos
    
    curso = GestorCursos.obtener_curso_por_id(curso_id)
    
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    return {
        'id': curso.id,
        'nombre': curso.nombre,
        'escuela': curso.escuela,
        'ciudad': curso.ciudad,
        'especialidad': curso.especialidad,
        'precio': curso.precio,
        'duracion_meses': curso.duracion_meses,
        'nivel_minimo_espanol': curso.nivel_minimo_espanol,
        'fecha_inicio': curso.fecha_inicio.isoformat() if curso.fecha_inicio else None,
        'descripcion': curso.descripcion,
        'requisitos': curso.requisitos,
        'url_informacion': curso.url_informacion,
        'disponible': curso.disponible
    }


# ============================================================================
# FONDOS - Verificación económica
# ============================================================================

@app.get("/api/estudiantes/{estudiante_id}/fondos", tags=["Fondos"])
def verificar_fondos(estudiante_id: int, db: Session = Depends(get_db)):
    """Verifica situación económica del estudiante"""
    from modules.fondos import GestorFondos
    
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    verificacion = GestorFondos.verificar_fondos(estudiante_id)
    return verificacion


@app.post("/api/estudiantes/{estudiante_id}/patrocinador", tags=["Fondos"])
def agregar_patrocinador(
    estudiante_id: int,
    datos_patrocinador: Dict,
    db: Session = Depends(get_db)
):
    """Agrega patrocinador para el estudiante"""
    from modules.fondos import GestorFondos
    
    resultado = GestorFondos.agregar_patrocinador(estudiante_id, datos_patrocinador)
    return resultado


# ============================================================================
# ALOJAMIENTO - Búsqueda y gestión
# ============================================================================

@app.get("/api/alojamientos", tags=["Alojamiento"])
def buscar_alojamientos(
    ciudad: Optional[str] = None,
    precio_max: Optional[float] = None,
    tipo: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Busca alojamientos disponibles"""
    from modules.alojamiento import GestorAlojamiento
    
    alojamientos = GestorAlojamiento.buscar_alojamientos(
        ciudad=ciudad,
        precio_max=precio_max,
        tipo=tipo,
        disponible=True
    )
    
    return {
        'total': len(alojamientos),
        'alojamientos': [
            {
                'id': a.id,
                'tipo': a.tipo,
                'direccion': a.direccion,
                'ciudad': a.ciudad,
                'precio_mensual': a.precio_mensual,
                'gastos_incluidos': a.gastos_incluidos,
                'num_habitaciones': a.num_habitaciones,
                'num_banos': a.num_banos,
                'metros_cuadrados': a.metros_cuadrados,
                'disponible': a.disponible
            }
            for a in alojamientos[skip:skip+limit]
        ]
    }


# ============================================================================
# DOCUMENTOS - Upload y gestión
# ============================================================================

from fastapi import UploadFile, File

@app.post("/api/estudiantes/{estudiante_id}/documentos/upload", tags=["Documentos"])
async def subir_documento(
    estudiante_id: int,
    tipo_documento: str,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Sube un documento del estudiante"""
    import os
    from pathlib import Path
    
    # Verificar estudiante existe
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Crear directorio si no existe
    upload_dir = Path(f"uploads/estudiantes/{estudiante_id}")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar archivo
    file_path = upload_dir / f"{tipo_documento}_{archivo.filename}"
    
    with file_path.open("wb") as buffer:
        content = await archivo.read()
        buffer.write(content)
    
    return {
        'mensaje': 'Documento subido correctamente',
        'tipo': tipo_documento,
        'filename': archivo.filename,
        'path': str(file_path)
    }


@app.post("/api/documentos/{documento_id}/validar-ocr", tags=["Documentos"])
async def validar_documento_ocr(
    documento_id: int,
    tipo_documento: str,
    db: Session = Depends(get_db)
):
    """
    Procesa documento con OCR y valida contenido
    
    Tipos soportados: pasaporte, dni, extracto_bancario, carta_admision, certificado_idioma
    """
    try:
        import os
        import psycopg2
        from api.validador_ocr import ValidadorOCR
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Obtener documento de BD
        cursor.execute("""
            SELECT d.id, d.estudiante_id, d.tipo, d.nombre_archivo, d.ruta_archivo
            FROM documentos d
            WHERE d.id = %s
        """, (documento_id,))
        
        doc = cursor.fetchone()
        
        if not doc:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        doc_id, estudiante_id, tipo, nombre, ruta = doc
        
        # Verificar archivo existe
        if not os.path.exists(ruta):
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Archivo no encontrado en servidor")
        
        # Procesar con OCR
        validador = ValidadorOCR()
        resultado = validador.procesar_documento(ruta, tipo_documento)
        
        if resultado['exito']:
            # Guardar resultados en BD
            cursor.execute("""
                UPDATE documentos 
                SET ocr_procesado = TRUE,
                    ocr_datos_extraidos = %s,
                    ocr_validacion = %s,
                    ocr_nivel_confianza = %s,
                    ocr_alertas = %s,
                    ocr_fecha_procesamiento = NOW()
                WHERE id = %s
            """, (
                json.dumps(resultado['datos_extraidos']),
                json.dumps(resultado['validacion']),
                resultado['nivel_confianza'],
                json.dumps(resultado['alertas']),
                documento_id
            ))
            
            conn.commit()
            
            # Registrar en historial
            cursor.execute("""
                INSERT INTO historial_acciones (estudiante_id, accion, detalles, fecha)
                VALUES (%s, %s, %s, NOW())
            """, (
                estudiante_id,
                'documento_validado_ocr',
                f"Documento {nombre} procesado con OCR - Confianza: {resultado['nivel_confianza']}%"
            ))
            
            conn.commit()
        
        cursor.close()
        conn.close()
        
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en validación OCR: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/estudiantes/{estudiante_id}/documentos/ocr-status", tags=["Documentos"])
def obtener_status_ocr(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene estado de validación OCR de todos los documentos del estudiante
    """
    try:
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT d.id, d.tipo, d.nombre_archivo, d.ocr_procesado, 
                   d.ocr_nivel_confianza, d.ocr_alertas, d.ocr_fecha_procesamiento
            FROM documentos d
            WHERE d.estudiante_id = %s
            ORDER BY d.fecha_subida DESC
        """, (estudiante_id,))
        
        documentos = cursor.fetchall()
        cursor.close()
        conn.close()
        
        resultado = []
        for doc in documentos:
            resultado.append({
                'id': doc[0],
                'tipo': doc[1],
                'nombre': doc[2],
                'ocr_procesado': doc[3] or False,
                'nivel_confianza': doc[4] or 0,
                'alertas': json.loads(doc[5]) if doc[5] else [],
                'fecha_procesamiento': doc[6].isoformat() if doc[6] else None
            })
        
        return {
            'estudiante_id': estudiante_id,
            'total_documentos': len(resultado),
            'procesados_ocr': sum(1 for d in resultado if d['ocr_procesado']),
            'confianza_promedio': sum(d['nivel_confianza'] for d in resultado) / len(resultado) if resultado else 0,
            'documentos': resultado
        }
        
    except Exception as e:
        print(f"Error obteniendo status OCR: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/estudiantes/{estudiante_id}/documentos", tags=["Documentos"])
def obtener_checklist(estudiante_id: int, db: Session = Depends(get_db)):
    """Obtiene checklist de documentos del estudiante"""
    from modules.estudiantes import GestorEstudiantes
    
    checklist = GestorEstudiantes.checklist_documentos(estudiante_id)
    return checklist


# ============================================================================
# NOTIFICACIONES WEB - Sistema interno
# ============================================================================

@app.get("/api/estudiantes/{estudiante_id}/notificaciones", tags=["Notificaciones"])
def obtener_notificaciones(
    estudiante_id: int,
    no_leidas: bool = False,
    db: Session = Depends(get_db)
):
    """Obtiene notificaciones del estudiante"""
    from modules.notificaciones import SistemaNotificaciones
    
    # Implementación simplificada - expandir según necesidades
    return {
        'notificaciones': [],
        'total': 0,
        'no_leidas': 0
    }


# ============================================================================
# MENSAJERÍA - Chat entre estudiantes y admins
# ============================================================================

@app.post("/api/mensajes", tags=["Mensajería"])
def enviar_mensaje(
    datos: Dict,
    db: Session = Depends(get_db)
):
    """Envía mensaje entre estudiante y admin"""
    # Implementación de sistema de chat
    return {
        'exito': True,
        'mensaje_id': 1,
        'fecha': datetime.now().isoformat()
    }


@app.get("/api/estudiantes/{estudiante_id}/mensajes", tags=["Mensajería"])
def obtener_mensajes(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene conversación del estudiante"""
    return {
        'mensajes': [],
        'total': 0
    }


# ============================================================================
# ADMIN - GESTIÓN DE CURSOS
# ============================================================================

@app.post("/api/admin/cursos", tags=["Admin - Cursos"])
def crear_curso(
    datos: Dict,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Crea un nuevo curso"""
    from modules.cursos import GestorCursos
    from database.models import Curso
    
    nuevo_curso = Curso(
        nombre=datos['nombre'],
        escuela=datos['escuela'],
        ciudad=datos['ciudad'],
        especialidad=datos['especialidad'],
        precio=datos['precio'],
        duracion_meses=datos['duracion_meses'],
        nivel_minimo_espanol=datos.get('nivel_minimo_espanol', 'B1'),
        descripcion=datos.get('descripcion'),
        requisitos=datos.get('requisitos'),
        url_informacion=datos.get('url_informacion'),
        disponible=True
    )
    
    db.add(nuevo_curso)
    db.commit()
    db.refresh(nuevo_curso)
    
    return {'exito': True, 'curso_id': nuevo_curso.id}


@app.put("/api/admin/cursos/{curso_id}", tags=["Admin - Cursos"])
def actualizar_curso(
    curso_id: int,
    datos: Dict,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Actualiza un curso existente"""
    from database.models import Curso
    
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    for campo, valor in datos.items():
        if hasattr(curso, campo):
            setattr(curso, campo, valor)
    
    db.commit()
    return {'exito': True, 'mensaje': 'Curso actualizado'}


@app.delete("/api/admin/cursos/{curso_id}", tags=["Admin - Cursos"])
def eliminar_curso(
    curso_id: int,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Elimina un curso"""
    from database.models import Curso
    
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    curso.disponible = False
    db.commit()
    
    return {'exito': True, 'mensaje': 'Curso desactivado'}


# ============================================================================
# ADMIN - GESTIÓN DE ALOJAMIENTOS
# ============================================================================

@app.post("/api/admin/alojamientos", tags=["Admin - Alojamiento"])
def crear_alojamiento(
    datos: Dict,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Crea nuevo alojamiento"""
    from database.models import Alojamiento
    
    nuevo = Alojamiento(
        tipo=datos['tipo'],
        direccion=datos['direccion'],
        ciudad=datos['ciudad'],
        precio_mensual=datos['precio_mensual'],
        gastos_incluidos=datos.get('gastos_incluidos', False),
        num_habitaciones=datos.get('num_habitaciones', 1),
        num_banos=datos.get('num_banos', 1),
        metros_cuadrados=datos.get('metros_cuadrados'),
        disponible=True
    )
    
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    
    return {'exito': True, 'alojamiento_id': nuevo.id}


@app.put("/api/admin/alojamientos/{alojamiento_id}", tags=["Admin - Alojamiento"])
def actualizar_alojamiento(
    alojamiento_id: int,
    datos: Dict,
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Actualiza alojamiento"""
    from database.models import Alojamiento
    
    alojamiento = db.query(Alojamiento).filter(Alojamiento.id == alojamiento_id).first()
    if not alojamiento:
        raise HTTPException(status_code=404, detail="Alojamiento no encontrado")
    
    for campo, valor in datos.items():
        if hasattr(alojamiento, campo):
            setattr(alojamiento, campo, valor)
    
    db.commit()
    return {'exito': True, 'mensaje': 'Alojamiento actualizado'}


# ============================================================================
# ADMIN - REPORTES AVANZADOS
# ============================================================================

@app.get("/api/admin/reportes/mensual", tags=["Admin - Reportes"])
def reporte_mensual(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Genera reporte mensual completo"""
    reporte = PanelAdministrativo.generar_reporte_mensual()
    return reporte


@app.get("/api/admin/reportes/especialidades", tags=["Admin - Reportes"])
def estadisticas_especialidades(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Estadísticas por especialidad"""
    stats = PanelAdministrativo.estadisticas_por_especialidad()
    return {'especialidades': stats}


@app.get("/api/admin/reportes/conversion", tags=["Admin - Reportes"])
def embudo_conversion(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Embudo de conversión de estudiantes"""
    embudo = PanelAdministrativo.embudo_conversion()
    return embudo


# ============================================================================
# ADMIN - GESTIÓN DE DOCUMENTOS
# ============================================================================

@app.get("/api/admin/documentos/pendientes", tags=["Admin - Documentos"])
def documentos_pendientes(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Lista estudiantes con documentos pendientes"""
    estudiantes = db.query(Estudiante).filter(
        Estudiante.estado_procesamiento.in_([
            'registrado',
            'procesado_automaticamente',
            'pendiente_revision_admin'
        ])
    ).all()
    
    pendientes = []
    for est in estudiantes:
        from modules.estudiantes import GestorEstudiantes
        checklist = GestorEstudiantes.checklist_documentos(est.id)
        
        if checklist['total_obligatorios'] > 0:
            pendientes.append({
                'estudiante_id': est.id,
                'nombre': est.nombre_completo,
                'documentos_obligatorios_pendientes': checklist['total_obligatorios'],
                'documentos_recomendados_pendientes': checklist['total_recomendados']
            })
    
    return {'total': len(pendientes), 'estudiantes': pendientes}


# ============================================================================
# MENSAJERÍA INTERNA - Chat entre estudiantes y admins
# ============================================================================

@app.post("/api/conversaciones", tags=["Mensajería"])
def crear_conversacion(datos: Dict, db: Session = Depends(get_db)):
    """Crea una nueva conversación"""
    from modules.mensajeria import SistemaMensajeria
    
    conversacion = SistemaMensajeria.crear_conversacion(
        estudiante_id=datos['estudiante_id'],
        admin_id=datos.get('admin_id')
    )
    
    return {'exito': True, 'conversacion_id': conversacion.id}


@app.post("/api/mensajes", tags=["Mensajería"])
def enviar_mensaje(datos: Dict, db: Session = Depends(get_db)):
    """Envía mensaje en una conversación"""
    from modules.mensajeria import SistemaMensajeria
    
    resultado = SistemaMensajeria.enviar_mensaje(
        conversacion_id=datos['conversacion_id'],
        remitente_tipo=datos['remitente_tipo'],
        remitente_id=datos['remitente_id'],
        contenido=datos['contenido']
    )
    
    return resultado


@app.get("/api/conversaciones/{conversacion_id}/mensajes", tags=["Mensajería"])
def obtener_mensajes_conversacion(
    conversacion_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Obtiene mensajes de una conversación"""
    from modules.mensajeria import SistemaMensajeria
    
    mensajes = SistemaMensajeria.obtener_mensajes(conversacion_id, limit=limit)
    return {'mensajes': mensajes, 'total': len(mensajes)}


@app.get("/api/estudiantes/{estudiante_id}/conversaciones", tags=["Mensajería"])
def obtener_conversaciones_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    """Obtiene conversaciones del estudiante"""
    from modules.mensajeria import SistemaMensajeria
    
    conversaciones = SistemaMensajeria.obtener_conversaciones_estudiante(estudiante_id)
    return {'conversaciones': conversaciones}


@app.get("/api/admin/conversaciones", tags=["Admin - Mensajería"])
def obtener_conversaciones_admin(
    usuario=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Obtiene todas las conversaciones activas para admin"""
    from modules.mensajeria import SistemaMensajeria
    
    conversaciones = SistemaMensajeria.obtener_conversaciones_admin()
    return {'conversaciones': conversaciones}


# ============================================================================
# NOTIFICACIONES EMAIL
# ============================================================================

@app.post("/api/notificaciones/test-email", tags=["Notificaciones"])
def test_email(destinatario: str):
    """Endpoint de prueba para verificar configuración de email"""
    from modules.notificaciones_email import EmailService
    import config
    
    html = EmailService.generar_template_html(
        titulo="Email de Prueba",
        mensaje="<p>Este es un email de prueba del sistema de notificaciones.</p><p>Si recibes este mensaje, la configuración SMTP está funcionando correctamente.</p>",
        boton_texto="Visitar Plataforma",
        boton_url=getattr(config, 'WEB_URL', 'http://localhost:3000')
    )
    
    resultado = EmailService.enviar_email(
        destinatario=destinatario,
        asunto="🧪 Email de Prueba - Sistema de Notificaciones",
        contenido_html=html
    )
    
    if resultado:
        return {"mensaje": "Email enviado correctamente", "destinatario": destinatario}
    else:
        raise HTTPException(status_code=500, detail="Error al enviar email")


@app.post("/api/estudiantes/{estudiante_id}/notificaciones/resend", tags=["Notificaciones"])
def reenviar_notificacion(
    estudiante_id: int,
    tipo: str,
    db: Session = Depends(get_db)
):
    """
    Reenviar notificación por email a un estudiante
    Tipos: registro, aprobacion, pendiente
    """
    from modules.notificaciones_email import NotificacionesEmail
    
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante_dict = {
        'id': estudiante.id,
        'nombre_completo': estudiante.nombre_completo,
        'email': estudiante.email,
        'especialidad_interes': estudiante.especialidad_interes,
        'nacionalidad': estudiante.nacionalidad
    }
    
    resultado = False
    
    if tipo == "registro":
        resultado = NotificacionesEmail.enviar_confirmacion_registro(estudiante_dict)
    elif tipo == "aprobacion":
        resultado = NotificacionesEmail.enviar_solicitud_aprobada(estudiante_dict)
    elif tipo == "pendiente":
        motivo = "Revisión de documentación requerida"
        resultado = NotificacionesEmail.enviar_solicitud_pendiente_revision(estudiante_dict, motivo)
    else:
        raise HTTPException(status_code=400, detail="Tipo de notificación inválido")
    
    if resultado:
        return {"mensaje": f"Notificación '{tipo}' reenviada a {estudiante.email}"}
    else:
        raise HTTPException(status_code=500, detail="Error al enviar notificación")


# ============================================================================
# INTEGRACIÓN APIS ESCUELAS
# ============================================================================

@app.get("/api/admin/sincronizar-cursos-escuelas", tags=["Admin - Escuelas"])
def sincronizar_cursos_desde_escuelas(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """
    Sincroniza cursos desde APIs/scraping de escuelas españolas
    Obtiene cursos actualizados de múltiples universidades
    """
    verificar_token(credentials.credentials)
    
    try:
        from api.integrador_escuelas import IntegradorEscuelas
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Obtener cursos de todas las fuentes
        cursos_externos = IntegradorEscuelas.sincronizar_todos_cursos()
        
        # Insertar/actualizar en base de datos
        cursos_insertados = 0
        cursos_actualizados = 0
        
        for curso_ext in cursos_externos:
            # Verificar si el curso ya existe (por nombre y ciudad)
            cursor.execute(
                """
                SELECT id, precio, cupos_disponibles 
                FROM cursos 
                WHERE nombre = %s AND ciudad = %s
                """,
                (curso_ext['nombre'], curso_ext['ciudad'])
            )
            curso_existente = cursor.fetchone()
            
            if curso_existente:
                # Actualizar precio y cupos
                cursor.execute(
                    """
                    UPDATE cursos 
                    SET precio = %s, 
                        cupos_disponibles = %s,
                        descripcion = %s,
                        activo = TRUE,
                        updated_at = NOW()
                    WHERE id = %s
                    """,
                    (curso_ext['precio_eur'], curso_ext['cupos_disponibles'], 
                     curso_ext['descripcion'], curso_existente[0])
                )
                cursos_actualizados += 1
            else:
                # Insertar nuevo curso
                cursor.execute(
                    """
                    INSERT INTO cursos (nombre, descripcion, duracion_meses, precio, 
                                       ciudad, nivel_espanol_requerido, cupos_disponibles, activo, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE, NOW(), NOW())
                    """,
                    (curso_ext['nombre'], curso_ext['descripcion'], curso_ext['duracion_meses'],
                     curso_ext['precio_eur'], curso_ext['ciudad'], curso_ext['nivel_espanol_requerido'],
                     curso_ext['cupos_disponibles'])
                )
                cursos_insertados += 1
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "exito": True,
            "cursos_encontrados": len(cursos_externos),
            "cursos_insertados": cursos_insertados,
            "cursos_actualizados": cursos_actualizados,
            "cursos_preview": cursos_externos[:5]  # Primeros 5 para preview
        }
        
    except Exception as e:
        print(f"Error sincronizando cursos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cursos/buscar-externos", tags=["Cursos"])
def buscar_cursos_externos(
    especialidad: Optional[str] = None,
    ciudad: Optional[str] = None,
    presupuesto_max: Optional[float] = None
):
    """
    Busca cursos en APIs externas sin guardar en BD
    Útil para búsqueda en tiempo real
    """
    try:
        from api.integrador_escuelas import IntegradorEscuelas
        
        # Obtener todos los cursos disponibles
        cursos = IntegradorEscuelas.sincronizar_todos_cursos()
        
        # Aplicar filtros
        if especialidad:
            cursos = IntegradorEscuelas.buscar_cursos_por_especialidad(especialidad, cursos)
        
        if ciudad:
            cursos = IntegradorEscuelas.filtrar_por_ciudad(cursos, ciudad)
        
        if presupuesto_max:
            cursos = IntegradorEscuelas.filtrar_por_presupuesto(cursos, presupuesto_max)
        
        return {
            "total": len(cursos),
            "cursos": cursos
        }
        
    except Exception as e:
        print(f"Error buscando cursos externos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cursos/{curso_id}/verificar-disponibilidad", tags=["Cursos"])
def verificar_disponibilidad_externa(
    curso_id: int,
    db: Session = Depends(get_db)
):
    """
    Verifica disponibilidad en tiempo real desde la fuente externa
    """
    try:
        from api.integrador_escuelas import IntegradorEscuelas
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Obtener curso de BD
        cursor.execute(
            "SELECT nombre, ciudad, cupos_disponibles FROM cursos WHERE id = %s",
            (curso_id,)
        )
        curso = cursor.fetchone()
        
        if not curso:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        
        # Consultar disponibilidad real
        cupos_actuales = IntegradorEscuelas.actualizar_disponibilidad_real(curso_id)
        
        # Actualizar en BD
        cursor.execute(
            "UPDATE cursos SET cupos_disponibles = %s, updated_at = NOW() WHERE id = %s",
            (cupos_actuales, curso_id)
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {
            "curso_id": curso_id,
            "nombre": curso[0],
            "cupos_disponibles": cupos_actuales,
            "disponible": cupos_actuales > 0,
            "actualizado": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error verificando disponibilidad: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/scrapers/health", tags=["Admin - Escuelas"])
def obtener_salud_scrapers(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """
    Obtiene reporte de salud de todos los scrapers
    """
    verificar_token(credentials.credentials)
    
    try:
        from api.monitor_scrapers import MonitorScrapers
        
        monitor = MonitorScrapers()
        report = monitor.get_health_report()
        
        return report
        
    except Exception as e:
        print(f"Error obteniendo salud scrapers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/scrapers/clear-alerts", tags=["Admin - Escuelas"])
def limpiar_alertas_scrapers(
    source: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """
    Limpia alertas de scrapers (después de arreglar problemas)
    """
    verificar_token(credentials.credentials)
    
    try:
        from api.monitor_scrapers import MonitorScrapers
        
        monitor = MonitorScrapers()
        monitor.clear_alerts(source)
        
        return {
            "exito": True,
            "mensaje": f"Alertas limpiadas: {source or 'todas'}"
        }
        
    except Exception as e:
        print(f"Error limpiando alertas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/cache/stats", tags=["Admin - Escuelas"])
def obtener_estadisticas_cache(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """
    Obtiene estadísticas del sistema de cache
    """
    verificar_token(credentials.credentials)
    
    try:
        from api.cache_manager import CacheManager
        
        cache = CacheManager()
        stats = cache.get_stats()
        
        return stats
        
    except Exception as e:
        print(f"Error obteniendo stats cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/cache/clear", tags=["Admin - Escuelas"])
def limpiar_cache(
    source: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """
    Limpia cache de cursos (forzar nuevo scraping)
    """
    verificar_token(credentials.credentials)
    
    try:
        from api.cache_manager import CacheManager
        
        cache = CacheManager()
        cache.clear(source)
        
        return {
            "exito": True,
            "mensaje": f"Cache limpiado: {source or 'todo'}"
        }
        
    except Exception as e:
        print(f"Error limpiando cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/estudiantes/{estudiante_id}/calcular-probabilidad", tags=["Estudiantes"])
def calcular_probabilidad_exito(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    """
    Calcula probabilidad de éxito en solicitud de visa
    Basado en múltiples factores del perfil del estudiante
    """
    try:
        from api.predictor_exito import PredictorExito
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Obtener datos del estudiante
        cursor.execute("""
            SELECT e.nombre, e.nacionalidad, e.especialidad, e.nivel_idioma, 
                   e.fondos_disponibles, e.created_at, c.nombre as curso
            FROM estudiantes e
            LEFT JOIN cursos c ON e.curso_asignado_id = c.id
            WHERE e.id = %s
        """, (estudiante_id,))
        
        estudiante = cursor.fetchone()
        
        if not estudiante:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        # Contar documentos
        cursor.execute("""
            SELECT COUNT(*) FROM documentos WHERE estudiante_id = %s
        """, (estudiante_id,))
        docs_subidos = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM documentos_generados 
            WHERE estudiante_id = %s AND estado = 'aprobado'
        """, (estudiante_id,))
        docs_generados = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        # Calcular días desde registro
        dias_registro = (datetime.now() - estudiante[5]).days if estudiante[5] else 0
        
        # Preparar datos para predictor
        datos_estudiante = {
            'nacionalidad': estudiante[1] or '',
            'fondos_disponibles': float(estudiante[4] or 0),
            'documentos_subidos': docs_subidos,
            'documentos_generados': docs_generados,
            'curso_asignado': estudiante[6] or '',
            'nivel_idioma': estudiante[3] or 'B1',
            'especialidad': estudiante[2] or '',
            'dias_desde_registro': dias_registro,
            'antecedentes': False  # Por ahora asumimos sin antecedentes
        }
        
        # Calcular probabilidad
        predictor = PredictorExito()
        resultado = predictor.calcular_probabilidad(datos_estudiante)
        
        return {
            'estudiante_id': estudiante_id,
            'nombre': estudiante[0],
            **resultado
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error calculando probabilidad: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/estudiantes/{estudiante_id}/analisis-completo", tags=["Admin"])
def obtener_analisis_completo(
    estudiante_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """
    Análisis completo de estudiante con probabilidad de éxito y recomendaciones
    """
    verificar_token(credentials.credentials)
    
    try:
        from api.predictor_exito import PredictorExito
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Obtener todos los datos del estudiante
        cursor.execute("""
            SELECT e.*, c.nombre as curso, c.precio as precio_curso,
                   a.tipo as alojamiento
            FROM estudiantes e
            LEFT JOIN cursos c ON e.curso_asignado_id = c.id
            LEFT JOIN alojamientos a ON e.alojamiento_asignado_id = a.id
            WHERE e.id = %s
        """, (estudiante_id,))
        
        estudiante = cursor.fetchone()
        
        if not estudiante:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        # Obtener documentos
        cursor.execute("""
            SELECT tipo, nombre_archivo, fecha_subida 
            FROM documentos 
            WHERE estudiante_id = %s
        """, (estudiante_id,))
        documentos = cursor.fetchall()
        
        cursor.execute("""
            SELECT tipo, estado, fecha_generacion, fecha_aprobacion
            FROM documentos_generados 
            WHERE estudiante_id = %s
        """, (estudiante_id,))
        docs_generados = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Preparar datos para predictor
        datos_estudiante = {
            'nacionalidad': estudiante[3] or '',
            'fondos_disponibles': float(estudiante[6] or 0),
            'documentos_subidos': len(documentos),
            'documentos_generados': len([d for d in docs_generados if d[1] == 'aprobado']),
            'curso_asignado': estudiante[17] or '',
            'nivel_idioma': estudiante[5] or 'B1',
            'especialidad': estudiante[4] or '',
            'dias_desde_registro': (datetime.now() - estudiante[11]).days if estudiante[11] else 0,
            'antecedentes': False
        }
        
        # Calcular probabilidad
        predictor = PredictorExito()
        analisis = predictor.calcular_probabilidad(datos_estudiante)
        
        return {
            'estudiante': {
                'id': estudiante[0],
                'nombre': estudiante[1],
                'email': estudiante[2],
                'nacionalidad': estudiante[3],
                'estado': estudiante[9]
            },
            'analisis': analisis,
            'documentacion': {
                'subidos': len(documentos),
                'generados_aprobados': len([d for d in docs_generados if d[1] == 'aprobado']),
                'generados_pendientes': len([d for d in docs_generados if d[1] == 'pendiente'])
            },
            'curso': estudiante[17],
            'alojamiento': estudiante[19]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en análisis completo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PARTNERSHIPS UNIVERSITARIOS
# ============================================================================

@app.post("/api/admin/partners/universidades", tags=["Admin - Partners"])
def crear_universidad_partner(
    datos: Dict,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Crear nueva universidad partner"""
    verificar_token(credentials.credentials)
    
    try:
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO universidades_partner 
            (nombre, codigo_referido, email_contacto, persona_contacto, telefono,
             tipo_comision, porcentaje_comision, monto_fijo_comision, logo_url, notas)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            datos.get('nombre'),
            datos.get('codigo_referido'),
            datos.get('email_contacto'),
            datos.get('persona_contacto'),
            datos.get('telefono'),
            datos.get('tipo_comision', 'porcentaje'),
            datos.get('porcentaje_comision', 15.0),
            datos.get('monto_fijo_comision', 0),
            datos.get('logo_url'),
            datos.get('notas')
        ))
        
        universidad_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'exito': True,
            'universidad_id': universidad_id,
            'mensaje': 'Universidad partner creada exitosamente'
        }
        
    except Exception as e:
        print(f"Error creando universidad partner: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/partners/universidades", tags=["Admin - Partners"])
def listar_universidades_partner(
    activo: Optional[bool] = None,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Listar todas las universidades partner"""
    verificar_token(credentials.credentials)
    
    try:
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        query = """
            SELECT u.id, u.nombre, u.codigo_referido, u.email_contacto, 
                   u.persona_contacto, u.telefono, u.tipo_comision, 
                   u.porcentaje_comision, u.monto_fijo_comision, u.activo,
                   u.logo_url, u.notas, u.created_at,
                   COUNT(DISTINCT e.id) as total_referidos,
                   COUNT(DISTINCT CASE WHEN e.estado = 'matriculado' THEN e.id END) as matriculados,
                   COALESCE(SUM(CASE WHEN c.estado = 'pagado' THEN c.monto_comision ELSE 0 END), 0) as total_pagado,
                   COALESCE(SUM(CASE WHEN c.estado = 'pendiente' THEN c.monto_comision ELSE 0 END), 0) as total_pendiente
            FROM universidades_partner u
            LEFT JOIN estudiantes e ON e.universidad_referidora_id = u.id
            LEFT JOIN comisiones c ON c.universidad_id = u.id
        """
        
        if activo is not None:
            query += " WHERE u.activo = %s"
            cursor.execute(query + " GROUP BY u.id ORDER BY u.nombre", (activo,))
        else:
            cursor.execute(query + " GROUP BY u.id ORDER BY u.nombre")
        
        universidades = cursor.fetchall()
        cursor.close()
        conn.close()
        
        resultado = []
        for u in universidades:
            resultado.append({
                'id': u[0],
                'nombre': u[1],
                'codigo_referido': u[2],
                'email_contacto': u[3],
                'persona_contacto': u[4],
                'telefono': u[5],
                'tipo_comision': u[6],
                'porcentaje_comision': float(u[7]) if u[7] else 0,
                'monto_fijo_comision': float(u[8]) if u[8] else 0,
                'activo': u[9],
                'logo_url': u[10],
                'notas': u[11],
                'created_at': u[12].isoformat() if u[12] else None,
                'stats': {
                    'total_referidos': u[13],
                    'matriculados': u[14],
                    'tasa_conversion': round((u[14] / u[13] * 100) if u[13] > 0 else 0, 1),
                    'total_pagado': float(u[15]),
                    'total_pendiente': float(u[16])
                }
            })
        
        return {
            'universidades': resultado,
            'total': len(resultado)
        }
        
    except Exception as e:
        print(f"Error listando universidades: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/admin/partners/universidades/{universidad_id}", tags=["Admin - Partners"])
def actualizar_universidad_partner(
    universidad_id: int,
    datos: Dict,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Actualizar datos de universidad partner"""
    verificar_token(credentials.credentials)
    
    try:
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE universidades_partner 
            SET nombre = %s,
                email_contacto = %s,
                persona_contacto = %s,
                telefono = %s,
                tipo_comision = %s,
                porcentaje_comision = %s,
                monto_fijo_comision = %s,
                logo_url = %s,
                notas = %s,
                activo = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (
            datos.get('nombre'),
            datos.get('email_contacto'),
            datos.get('persona_contacto'),
            datos.get('telefono'),
            datos.get('tipo_comision'),
            datos.get('porcentaje_comision'),
            datos.get('monto_fijo_comision'),
            datos.get('logo_url'),
            datos.get('notas'),
            datos.get('activo'),
            universidad_id
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {'exito': True, 'mensaje': 'Universidad actualizada'}
        
    except Exception as e:
        print(f"Error actualizando universidad: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/partners/universidades/{universidad_id}/estudiantes", tags=["Admin - Partners"])
def listar_estudiantes_referidos(
    universidad_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Lista estudiantes referidos por universidad"""
    verificar_token(credentials.credentials)
    
    try:
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT e.id, e.nombre, e.email, e.nacionalidad, e.especialidad,
                   e.estado, e.created_at, c.nombre as curso,
                   com.monto_comision, com.estado as estado_comision
            FROM estudiantes e
            LEFT JOIN cursos c ON e.curso_asignado_id = c.id
            LEFT JOIN comisiones com ON com.estudiante_id = e.id AND com.universidad_id = %s
            WHERE e.universidad_referidora_id = %s
            ORDER BY e.created_at DESC
        """, (universidad_id, universidad_id))
        
        estudiantes = cursor.fetchall()
        cursor.close()
        conn.close()
        
        resultado = []
        for est in estudiantes:
            resultado.append({
                'id': est[0],
                'nombre': est[1],
                'email': est[2],
                'nacionalidad': est[3],
                'especialidad': est[4],
                'estado': est[5],
                'created_at': est[6].isoformat() if est[6] else None,
                'curso': est[7],
                'comision': {
                    'monto': float(est[8]) if est[8] else 0,
                    'estado': est[9] or 'no_generada'
                }
            })
        
        return {
            'estudiantes': resultado,
            'total': len(resultado)
        }
        
    except Exception as e:
        print(f"Error listando estudiantes referidos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/partners/comisiones/generar", tags=["Admin - Partners"])
def generar_comision(
    datos: Dict,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Genera comisión para estudiante matriculado"""
    verificar_token(credentials.credentials)
    
    try:
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        estudiante_id = datos.get('estudiante_id')
        monto_curso = datos.get('monto_curso')
        
        # Obtener universidad referidora
        cursor.execute("""
            SELECT universidad_referidora_id FROM estudiantes WHERE id = %s
        """, (estudiante_id,))
        
        result = cursor.fetchone()
        if not result or not result[0]:
            raise HTTPException(status_code=400, detail="Estudiante no tiene universidad referidora")
        
        universidad_id = result[0]
        
        # Obtener configuración de comisión
        cursor.execute("""
            SELECT tipo_comision, porcentaje_comision, monto_fijo_comision
            FROM universidades_partner WHERE id = %s
        """, (universidad_id,))
        
        config = cursor.fetchone()
        tipo_comision, porcentaje, monto_fijo = config
        
        # Calcular comisión
        if tipo_comision == 'porcentaje':
            monto_comision = monto_curso * (porcentaje / 100)
        else:
            monto_comision = monto_fijo
        
        # Crear registro de comisión
        cursor.execute("""
            INSERT INTO comisiones 
            (universidad_id, estudiante_id, monto_curso, monto_comision, 
             estado, fecha_matricula)
            VALUES (%s, %s, %s, %s, 'pendiente', NOW())
            RETURNING id
        """, (universidad_id, estudiante_id, monto_curso, monto_comision))
        
        comision_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'exito': True,
            'comision_id': comision_id,
            'monto_comision': float(monto_comision)
        }
        
    except Exception as e:
        print(f"Error generando comisión: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/partners/comisiones", tags=["Admin - Partners"])
def listar_comisiones(
    universidad_id: Optional[int] = None,
    estado: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Lista todas las comisiones"""
    verificar_token(credentials.credentials)
    
    try:
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        query = """
            SELECT c.id, c.monto_curso, c.monto_comision, c.estado,
                   c.fecha_matricula, c.fecha_pago, c.notas,
                   u.nombre as universidad, e.nombre as estudiante
            FROM comisiones c
            JOIN universidades_partner u ON c.universidad_id = u.id
            JOIN estudiantes e ON c.estudiante_id = e.id
            WHERE 1=1
        """
        
        params = []
        if universidad_id:
            query += " AND c.universidad_id = %s"
            params.append(universidad_id)
        if estado:
            query += " AND c.estado = %s"
            params.append(estado)
        
        query += " ORDER BY c.created_at DESC"
        
        cursor.execute(query, params)
        comisiones = cursor.fetchall()
        cursor.close()
        conn.close()
        
        resultado = []
        for com in comisiones:
            resultado.append({
                'id': com[0],
                'monto_curso': float(com[1]),
                'monto_comision': float(com[2]),
                'estado': com[3],
                'fecha_matricula': com[4].isoformat() if com[4] else None,
                'fecha_pago': com[5].isoformat() if com[5] else None,
                'notas': com[6],
                'universidad': com[7],
                'estudiante': com[8]
            })
        
        return {
            'comisiones': resultado,
            'total': len(resultado),
            'total_pendiente': sum(c['monto_comision'] for c in resultado if c['estado'] == 'pendiente'),
            'total_pagado': sum(c['monto_comision'] for c in resultado if c['estado'] == 'pagado')
        }
        
    except Exception as e:
        print(f"Error listando comisiones: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/admin/partners/comisiones/{comision_id}/marcar-pagado", tags=["Admin - Partners"])
def marcar_comision_pagada(
    comision_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Marca comisión como pagada"""
    verificar_token(credentials.credentials)
    
    try:
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE comisiones 
            SET estado = 'pagado', fecha_pago = NOW()
            WHERE id = %s
        """, (comision_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {'exito': True, 'mensaje': 'Comisión marcada como pagada'}
        
    except Exception as e:
        print(f"Error marcando comisión: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/partners/dashboard", tags=["Admin - Partners"])
def dashboard_partners(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """Dashboard general de partnerships"""
    verificar_token(credentials.credentials)
    
    try:
        import os
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        cursor = conn.cursor()
        
        # Estadísticas generales
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT u.id) as total_universidades,
                COUNT(DISTINCT e.id) as total_referidos,
                COUNT(DISTINCT CASE WHEN e.estado = 'matriculado' THEN e.id END) as total_matriculados,
                COALESCE(SUM(CASE WHEN c.estado = 'pendiente' THEN c.monto_comision ELSE 0 END), 0) as comisiones_pendientes,
                COALESCE(SUM(CASE WHEN c.estado = 'pagado' THEN c.monto_comision ELSE 0 END), 0) as comisiones_pagadas
            FROM universidades_partner u
            LEFT JOIN estudiantes e ON e.universidad_referidora_id = u.id
            LEFT JOIN comisiones c ON c.universidad_id = u.id
            WHERE u.activo = TRUE
        """)
        
        stats = cursor.fetchone()
        
        # Top universidades
        cursor.execute("""
            SELECT u.nombre, COUNT(e.id) as total_referidos,
                   COALESCE(SUM(c.monto_comision), 0) as total_comisiones
            FROM universidades_partner u
            LEFT JOIN estudiantes e ON e.universidad_referidora_id = u.id
            LEFT JOIN comisiones c ON c.universidad_id = u.id
            WHERE u.activo = TRUE
            GROUP BY u.id, u.nombre
            ORDER BY total_referidos DESC
            LIMIT 5
        """)
        
        top_universidades = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            'stats': {
                'total_universidades': stats[0],
                'total_referidos': stats[1],
                'total_matriculados': stats[2],
                'tasa_conversion': round((stats[2] / stats[1] * 100) if stats[1] > 0 else 0, 1),
                'comisiones_pendientes': float(stats[3]),
                'comisiones_pagadas': float(stats[4])
            },
            'top_universidades': [
                {
                    'nombre': u[0],
                    'total_referidos': u[1],
                    'total_comisiones': float(u[2])
                }
                for u in top_universidades
            ]
        }
        
    except Exception as e:
        print(f"Error en dashboard partners: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/", tags=["Health"])
def root():
    """Health check"""
    return {
        "status": "online",
        "servicio": "Bot Visas Estudio API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", tags=["Health"])
def health():
    """Health check detallado"""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
