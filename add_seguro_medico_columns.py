#!/usr/bin/env python3
"""
Script para agregar columnas relacionadas con gestión de seguro médico
"""

import psycopg2

def main():
    try:
        print("🏥 Agregando columnas de gestión de seguro médico...")
        
        # Usar la conexión de Render directamente
        DATABASE_URL = "postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas"
        
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Verificar si las columnas ya existen
        cur.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'estudiantes' 
            AND column_name IN ('gestion_seguro_solicitada', 'comentarios_seguro_medico', 'estado_seguro_medico');
        """)
        existing_columns = [row[0] for row in cur.fetchall()]
        
        # Agregar columnas que no existen
        columns_to_add = [
            ("gestion_seguro_solicitada", "BOOLEAN DEFAULT FALSE"),
            ("comentarios_seguro_medico", "TEXT"),
            ("estado_seguro_medico", "VARCHAR(20) DEFAULT 'pendiente'")
        ]
        
        for column_name, column_def in columns_to_add:
            if column_name not in existing_columns:
                print(f"  ➕ Agregando columna {column_name}...")
                cur.execute(f"""
                    ALTER TABLE estudiantes 
                    ADD COLUMN {column_name} {column_def};
                """)
                print(f"  ✅ Columna {column_name} agregada correctamente")
            else:
                print(f"  ⚠️  Columna {column_name} ya existe")
        
        # Commit cambios
        conn.commit()
        
        # Verificar estructura final
        print("\n📊 Verificando estructura final...")
        cur.execute("""
            SELECT column_name, data_type, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'estudiantes' 
            AND column_name LIKE '%seguro%'
            ORDER BY column_name;
        """)
        
        for row in cur.fetchall():
            print(f"  - {row[0]} ({row[1]}) = {row[2] or 'NULL'}")
        
        cur.close()
        conn.close()
        
        print("\n✅ Columnas de gestión de seguro médico agregadas correctamente!")
        print("\n🎯 Nuevas columnas disponibles:")
        print("  - gestion_seguro_solicitada: Indica si solicita gestión")
        print("  - comentarios_seguro_medico: Información médica adicional")
        print("  - estado_seguro_medico: Estado de la solicitud (pendiente/aprobado/rechazado)")
        
    except psycopg2.Error as e:
        print(f"❌ Error de base de datos: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()