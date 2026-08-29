import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    
    cur.execute("SELECT id, nombre, codigo_referido, referido_por FROM inversores WHERE nombre ILIKE '%Alejandro%'")
    print('POTENCIALES REFERIDOS ALEJANDRO:', cur.fetchall())

    # Update luis alberto (id 32) -> Jose Candido (JOS3199)
    cur.execute("UPDATE inversores SET referido_por = 'JOS3199' WHERE id = 32")
    
    conn.commit()
    print('Updated Luis Alberto -> Jose Candido (JOS3199)')

except Exception as e:
    print('SQL ERROR:', repr(e))
