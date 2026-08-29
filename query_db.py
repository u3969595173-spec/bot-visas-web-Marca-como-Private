import sys
from dotenv import dotenv_values
import psycopg2

config = dotenv_values('C:/BotVisasEstudio/.env')
db_url = config.get('DATABASE_URL')
if not db_url:
    print("No DATABASE_URL found in .env")
    sys.exit(1)

conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Find names matching Leandro or Roilan in "inversores"
cur.execute("""
    SELECT id, nombre, codigo_referido, referido_por, estado, created_at 
    FROM inversores 
    WHERE nombre ILIKE '%Leandro%' OR nombre ILIKE '%Roilan%'
""")
inversores_matches = cur.fetchall()

print("--- INVERSORES MATCHING LEANDRO OR ROILAN ---")
investor_ids = []
for row in inversores_matches:
    inv_id, nombre, codigo, sponsor, estado, created_at = row
    investor_ids.append(inv_id)
    
    # Let's count aportaciones
    cur.execute("SELECT COUNT(*) FROM aportaciones WHERE inversor_id = %s", (inv_id,))
    count_aportaciones = cur.fetchone()[0]
    
    # Let's count retiros
    cur.execute("SELECT COUNT(*) FROM retiros WHERE inversor_id = %s", (inv_id,))
    count_retiros = cur.fetchone()[0]
    
    print(f"ID: {inv_id}")
    print(f"  Nombre: {nombre}")
    print(f"  Código: {codigo}")
    print(f"  Referido por (Sponsor Code): {sponsor}")
    print(f"  Estado: {estado}")
    print(f"  Fecha Creación: {created_at}")
    print(f"  Count Aportaciones: {count_aportaciones}")
    print(f"  Count Retiros: {count_retiros}")
    print()

# Find referidos matching "nombre_inversor" matching Leandro or Roilan, or usuario_id matching the investor_ids (as string since it's character varying)
# Let's convert investor_ids to string
inv_ids_str = [str(i) for i in investor_ids]

query_referidos = """
    SELECT id, codigo, usuario_id, nombre_inversor, referido_por 
    FROM referidos 
    WHERE nombre_inversor ILIKE '%Leandro%' OR nombre_inversor ILIKE '%Roilan%'
"""
if inv_ids_str:
    placeholders = ", ".join(["%s"] * len(inv_ids_str))
    query_referidos += f" OR usuario_id IN ({placeholders})"
    cur.execute(query_referidos, tuple(inv_ids_str))
else:
    cur.execute(query_referidos)

referidos_matches = cur.fetchall()

print("--- REFERIDOS ROWS ---")
for row in referidos_matches:
    ref_id, codigo, usuario_id, nombre_inversor, referido_por = row
    print(f"ID (Referido): {ref_id}")
    print(f"  Código: {codigo}")
    print(f"  Usuario ID: {usuario_id}")
    print(f"  Nombre Inversor: {nombre_inversor}")
    print(f"  Referido Por: {referido_por}")
    print()

cur.close()
conn.close()
