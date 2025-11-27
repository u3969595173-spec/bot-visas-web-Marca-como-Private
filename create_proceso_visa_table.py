"""
Crear tabla de tracking del proceso completo de visa
Desde inscripción hasta día de entrevista
"""

import psycopg2
from config import DATABASE_URL

def create_proceso_visa_table():
    """Crea tabla para tracking completo del proceso de visa"""
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    # Tabla de pasos del proceso
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proceso_visa_pasos (
            id SERIAL PRIMARY KEY,
            estudiante_id INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
            
            -- FASE 1: INSCRIPCIÓN Y DOCUMENTACIÓN INICIAL
            paso_inscripcion BOOLEAN DEFAULT FALSE,
            fecha_inscripcion TIMESTAMP,
            paso_pago_inicial BOOLEAN DEFAULT FALSE,
            fecha_pago_inicial TIMESTAMP,
            paso_documentos_personales BOOLEAN DEFAULT FALSE,
            fecha_documentos_personales TIMESTAMP,
            
            -- FASE 2: UNIVERSIDAD Y CARTA ACEPTACIÓN
            paso_seleccion_universidad BOOLEAN DEFAULT FALSE,
            fecha_seleccion_universidad TIMESTAMP,
            paso_solicitud_universidad BOOLEAN DEFAULT FALSE,
            fecha_solicitud_universidad TIMESTAMP,
            paso_carta_aceptacion BOOLEAN DEFAULT FALSE,
            fecha_carta_aceptacion TIMESTAMP,
            
            -- FASE 3: DOCUMENTOS LEGALES
            paso_antecedentes_solicitados BOOLEAN DEFAULT FALSE,
            fecha_antecedentes_solicitados TIMESTAMP,
            paso_antecedentes_recibidos BOOLEAN DEFAULT FALSE,
            fecha_antecedentes_recibidos TIMESTAMP,
            paso_apostilla_haya BOOLEAN DEFAULT FALSE,
            fecha_apostilla_haya TIMESTAMP,
            paso_traduccion_documentos BOOLEAN DEFAULT FALSE,
            fecha_traduccion_documentos TIMESTAMP,
            
            -- FASE 4: SEGURO Y FONDOS
            paso_seguro_medico BOOLEAN DEFAULT FALSE,
            fecha_seguro_medico TIMESTAMP,
            paso_comprobante_fondos BOOLEAN DEFAULT FALSE,
            fecha_comprobante_fondos TIMESTAMP,
            paso_carta_banco BOOLEAN DEFAULT FALSE,
            fecha_carta_banco TIMESTAMP,
            
            -- FASE 5: FORMULARIOS Y PREPARACIÓN
            paso_formulario_visa BOOLEAN DEFAULT FALSE,
            fecha_formulario_visa TIMESTAMP,
            paso_fotos_biometricas BOOLEAN DEFAULT FALSE,
            fecha_fotos_biometricas TIMESTAMP,
            paso_pago_tasa_visa BOOLEAN DEFAULT FALSE,
            fecha_pago_tasa_visa TIMESTAMP,
            
            -- FASE 6: CITA EMBAJADA
            paso_cita_agendada BOOLEAN DEFAULT FALSE,
            fecha_cita_agendada TIMESTAMP,
            fecha_cita_embajada TIMESTAMP,
            paso_documentos_revisados BOOLEAN DEFAULT FALSE,
            fecha_documentos_revisados TIMESTAMP,
            paso_simulacro_entrevista BOOLEAN DEFAULT FALSE,
            fecha_simulacro_entrevista TIMESTAMP,
            
            -- FASE 7: DÍA DE LA ENTREVISTA
            paso_entrevista_completada BOOLEAN DEFAULT FALSE,
            fecha_entrevista_completada TIMESTAMP,
            resultado_entrevista VARCHAR(50),  -- aprobada, rechazada, pendiente_documentos
            
            -- FASE 8: POST-ENTREVISTA
            paso_pasaporte_recogido BOOLEAN DEFAULT FALSE,
            fecha_pasaporte_recogido TIMESTAMP,
            paso_visa_otorgada BOOLEAN DEFAULT FALSE,
            fecha_visa_otorgada TIMESTAMP,
            
            -- NOTAS Y OBSERVACIONES
            notas_admin TEXT,
            ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            UNIQUE(estudiante_id)
        );
    """)
    
    print("✅ Tabla proceso_visa_pasos creada")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n✅ TABLA DE PROCESO DE VISA CREADA")
    print("\n📋 PASOS DEL PROCESO:")
    print("""
    FASE 1: INSCRIPCIÓN (3 pasos)
    FASE 2: UNIVERSIDAD (3 pasos)
    FASE 3: DOCUMENTOS LEGALES (4 pasos)
    FASE 4: SEGURO Y FONDOS (3 pasos)
    FASE 5: FORMULARIOS (3 pasos)
    FASE 6: CITA EMBAJADA (4 pasos)
    FASE 7: ENTREVISTA (2 pasos)
    FASE 8: POST-ENTREVISTA (2 pasos)
    
    TOTAL: 24 pasos rastreables
    """)

if __name__ == "__main__":
    create_proceso_visa_table()
