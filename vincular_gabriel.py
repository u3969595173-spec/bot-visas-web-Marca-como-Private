import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url, sslmode='require')
cur = conn.cursor()

try:
    cur.execute("SELECT id, codigo_referido FROM inversores WHERE nombre ILIKE '%Leandro Eloy tamayo%' OR email = 'leandrosanchez@gmail.com' LIMIT 1")
    lider = cur.fetchone()
    if lider and lider[1]:
        codigo_lider = lider[1]
        cur.execute("UPDATE inversores SET referido_por = %s WHERE id = 74", (codigo_lider,))
        print(f"Gabriel ha sido exitosamente forzado bajo la sombrilla del lider {codigo_lider}")
    else:
        # Si no tiene codigo, le inyectamos uno manualmente
        cur.execute("UPDATE inversores SET codigo_referido = 'LEA1000' WHERE id = %s", (lider[0] if lider else 4,))
        cur.execute("UPDATE inversores SET referido_por = 'LEA1000' WHERE id = 74")
        print("Se creo el codigo LEA1000 para Leandro y se conecto a Gabriel a este.")
    
    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()

cur.close()
conn.close()
