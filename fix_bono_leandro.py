import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

bono_retroactivo = 459 * 0.10

cur.execute("SELECT id, nombre FROM inversores WHERE nombre ILIKE '%Leandro%' ORDER BY id ASC LIMIT 1")
leandro = cur.fetchone()

if leandro:
    l_id = leandro[0]
    print(f"Leandro encontrado (ID: {l_id})")
    
    cur.execute("""
        SELECT id FROM aportaciones 
        WHERE inversor_id = %s AND (estado = 'Activa' OR estado = 'Validada')
        ORDER BY created_at ASC LIMIT 1
    """, (l_id,))
    pa = cur.fetchone()
    
    if pa:
        cur.execute("UPDATE aportaciones SET ganancia_acelerada = COALESCE(ganancia_acelerada, 0) + %s WHERE id = %s", (bono_retroactivo, pa[0]))
        conn.commit()
        print(f"Bono retroactivo de {bono_retroactivo} aplicado a la aportacion {pa[0]} de Leandro.")
        
cur.close()
conn.close()
