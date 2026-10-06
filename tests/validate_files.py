from pathlib import Path
from xml.etree import ElementTree as ET
import re
import sys

root=Path(__file__).parents[1]
skip={'.git','__pycache__'}
files=[p for p in root.rglob('*') if p.is_file() and not any(part in skip for part in p.parts)]
errors=[]
for path in files:
    if path.suffix.lower()=='.svg':
        try:
            tree=ET.parse(path); node=tree.getroot()
            if not node.attrib.get('viewBox'): errors.append(f'missing viewBox: {path.relative_to(root)}')
            if node.find('.//{http://www.w3.org/2000/svg}script') is not None: errors.append(f'script element: {path.relative_to(root)}')
        except Exception as exc: errors.append(f'{path.relative_to(root)}: {exc}')
    if path.stat().st_size==0: errors.append(f'empty file: {path.relative_to(root)}')
    if path.suffix.lower() in {'.md','.py','.yml'} and path.name != 'validate_files.py':
        text=path.read_text(errors='replace')
        if re.search(r'(?i)(?:u(?:tm)?(?:_source|_medium|_campaign)?_|\?ref=|chatgpt\.com)',text,re.I): errors.append(f'tracking pattern in {path.relative_to(root)}')
print(f'Checked {len(files)} files; XML-validated {sum(p.suffix.lower()==".svg" for p in files)} SVGs.')
if errors:
    print('\n'.join(errors));sys.exit(1)
