import os, glob

search_dirs = [
    'e:/ReconX/Reconx_V_2.0.0/modules/**/*.py',
    'e:/ReconX/Reconx_V_2.0.0/tests/**/*.py'
]

files = []
for sd in search_dirs:
    files.extend(glob.glob(sd, recursive=True))

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace('type="', 'category="').replace("type='", "category='").replace('.type ==', '.category ==').replace('f.type', 'f.category')
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {file_path}')
    except Exception as e:
        print(f'Error processing {file_path}: {e}')
