"""
Endpoint temporal para crear las columnas faltantes en la base de datos
Agregar esto temporalmente al main.py
"""

# Agregar al final del archivo main.py, antes del if __name__ == "__main__":

@app.post("/api/admin/fix-database-columns", tags=["Admin - Database"])
async def fix_database_columns():
    """TEMPORAL: Agregar columnas faltantes de aprobación a la base de datos"""
    
    try:
        # Lista de columnas a agregar
        columnas = [
            # Estados de aprobación
            ("estado_patrocinio", "VARCHAR(20) DEFAULT 'pendiente'"),
            ("comentarios_patrocinio", "TEXT"),
            ("estado_alojamiento", "VARCHAR(20) DEFAULT 'pendiente'"), 
            ("comentarios_alojamiento", "TEXT"),
            ("estado_seguro_medico", "VARCHAR(20) DEFAULT 'pendiente'"),
            ("comentarios_seguro_medico", "TEXT"),
            
            # Campos de solicitudes (algunos pueden ya existir)
            ("patrocinio_solicitado", "BOOLEAN DEFAULT FALSE"),
            ("gestion_alojamiento_solicitada", "BOOLEAN DEFAULT FALSE"), 
            ("gestion_seguro_solicitada", "BOOLEAN DEFAULT FALSE"),
            
            # Campos adicionales de alojamiento
            ("tiene_alojamiento", "BOOLEAN"),
            ("tipo_alojamiento", "VARCHAR(100)"),
            ("direccion_alojamiento", "TEXT"),
            ("contacto_alojamiento", "VARCHAR(200)"),
            ("telefono_alojamiento", "VARCHAR(50)"),
            ("precio_mensual", "DECIMAL(10,2)"),
            ("moneda_alojamiento", "VARCHAR(10) DEFAULT 'EUR'"),
            ("gestion_solicitada", "BOOLEAN DEFAULT FALSE"),
            
            # Campos adicionales financieros  
            ("fondos_patrocinador", "DECIMAL(15,2)"),
            ("moneda_patrocinador", "VARCHAR(10) DEFAULT 'EUR'"),
            ("patrocinador_nombre", "VARCHAR(200)"),
            ("patrocinador_relacion", "VARCHAR(100)"),
            ("moneda_fondos", "VARCHAR(10) DEFAULT 'EUR'")
        ]
        
        columnas_agregadas = 0
        columnas_existentes = 0
        errores = 0
        resultados = []
        
        # Usar una nueva sesión de DB
        from database.models import get_db
        db = next(get_db())
        
        for nombre_columna, definicion in columnas:
            try:
                db.execute(text(f"""
                    ALTER TABLE estudiantes 
                    ADD COLUMN {nombre_columna} {definicion}
                """))
                db.commit()
                resultados.append(f"✅ Agregada: {nombre_columna}")
                columnas_agregadas += 1
                
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e).lower():
                    resultados.append(f"ℹ️  Ya existe: {nombre_columna}")
                    columnas_existentes += 1
                    db.rollback()
                else:
                    resultados.append(f"❌ Error con {nombre_columna}: {e}")
                    errores += 1
                    db.rollback()
        
        return {
            "success": True,
            "message": "Migración de columnas completada",
            "columnas_agregadas": columnas_agregadas,
            "columnas_existentes": columnas_existentes,
            "errores": errores,
            "detalles": resultados
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Error ejecutando migración"
        }