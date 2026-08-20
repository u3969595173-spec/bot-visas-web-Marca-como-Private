
with open('api_simple.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if 'CREATE TABLE IF NOT EXISTS' in line:
        skip = True
        # remove the previous cur.execute
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

