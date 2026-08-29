import psycopg2

DATABASE_URL = 'postgresql://botvisas_user:8q6BPglcnhp480QMTukf5L9wq4AwBAd7@dpg-d4jap4qli9vc738bm830-a.oregon-postgres.render.com/botvisas'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM aportaciones WHERE moneda IN ('MLC', 'CUP')")
total = cur.fetchone()[0]
print(f'Aportaciones MLC/CUP a eliminar: {total}')

cur.execute("DELETE FROM aportaciones WHERE moneda IN ('MLC', 'CUP')")
conn.commit()
print(f'Eliminadas {total} aportaciones en MLC/CUP.')

cur.execute('SELECT COUNT(*) FROM aportaciones')
restantes = cur.fetchone()[0]
print(f'Aportaciones restantes: {restantes}')

cur.close()
conn.close()
