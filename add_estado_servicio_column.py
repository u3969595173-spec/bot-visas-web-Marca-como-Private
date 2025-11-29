"""
Script para agregar columna estado_servicio a la tabla presupuestos
"""
import psycopg2
from config import DATABASE_URL

def agregar_columna_estado_servicio():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("🔧 Agregando columna estado_servicio a presupuestos...")
        
        # Agregar columna estado_servicio
        cursor.execute("""
            ALTER TABLE presupuestos 
            ADD COLUMN IF NOT EXISTS estado_servicio VARCHAR(50) DEFAULT 'pendiente';
        """)
        
        print("✅ Columna estado_servicio agregada")
        
        # Actualizar estados existentes basados en el estado actual
        print("🔄 Actualizando estados existentes...")
        
        # Si está aceptado y NO pagó inicial → pendiente
        cursor.execute("""
            UPDATE presupuestos 
            SET estado_servicio = 'pendiente'
            WHERE estado = 'aceptado' 
            AND (pagado_al_empezar = FALSE OR pagado_al_empezar IS NULL);
        """)
        
        # Si está aceptado y pagó inicial → en_proceso
        cursor.execute("""
            UPDATE presupuestos 
            SET estado_servicio = 'en_proceso'
            WHERE estado = 'aceptado' 
            AND pagado_al_empezar = TRUE;
        """)
        
        # Si está completamente pagado → mantener en_proceso (hasta que completes proceso visa)
        cursor.execute("""
            UPDATE presupuestos 
            SET estado_servicio = 'en_proceso'
            WHERE pagado = TRUE;
        """)
        
        print("✅ Estados actualizados")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        raise

if __name__ == "__main__":
    agregar_columna_estado_servicio()
