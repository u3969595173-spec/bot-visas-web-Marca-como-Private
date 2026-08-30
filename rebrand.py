import os
import re

directories = ['frontend/src', 'frontend/public', 'frontend']
extensions = ('.jsx', '.html', '.css', '.json', '.py', '.js')

# Also include top level files
top_files = ['api_simple.py']

for d in directories:
    for root, dirs, files in os.walk(d):
        if 'node_modules' in root or '.git' in root or 'dist' in root:
            continue
        for f in files:
            if f.endswith(extensions):
                top_files.append(os.path.join(root, f))

for path in top_files:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if not re.search(r'(?i)Capital Trade|CapitalTrade|capitaltradeiberia', content):
            continue
            
        content = content.replace('Capital Trade Iberia', 'Capital Iberia')
        content = content.replace('Capital Trade', 'Capital Iberia')
        content = content.replace('CapitalTrade', 'CapitalIberia')
        content = content.replace('capitaltradeiberia.com', 'capitaliberia.com')
        
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Rebranded: {path}")
    except Exception as e:
        # Ignore decoding errors on binary or strange files
        pass
print("Done!")
