import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    
    cur.execute("SELECT id, nombre, codigo_referido, referido_por FROM inversores WHERE codigo_referido = 'JOS3163'")
    print('EL VERDADERO JOS3163:', cur.fetchall())

    cur.execute("UPDATE inversores SET referido_por = 'JOS3163' WHERE id = 32")
    conn.commit()
    print('ACTUALIZADO LUIS ALBERTO A JOS3163')
except Exception as e:
    print('ERROR:', e)
