
with open('api_simple.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_retiros_get = False
skip = False
for line in lines:
    if '@app.get(' in line and '/api/retiros' in line:
        in_retiros_get = True
    
    if in_retiros_get and 'CREATE TABLE IF NOT EXISTS retiros' in line:
        skip = True
        if len(new_lines) > 0 and 'cur.execute' in new_lines[-1]:
            new_lines.pop()
        continue
    
    if skip and 'conn.commit()' in line:
        skip = False
        continue
        
    if not skip:
        new_lines.append(line)

with open('api_simple.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

