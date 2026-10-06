from pathlib import Path
from xml.etree import ElementTree as ET
import re,sys
root=Path(__file__).parents[1]
errors=[]
for p in root.rglob('*.svg'):
 try: ET.parse(p)
 except Exception as e: errors.append(f'{p}: {e}')
for p in root.rglob('*'):
 if p.is_file() and p.stat().st_size==0: errors.append(f'empty file: {p}')
for p in root.rglob('*.md'):
 text=p.read_text(errors='replace')
 if re.search(r'utm_|utm_source|utm_medium|utm_campaign|\?ref=|chatgpt\.com',text,re.I): errors.append(f'tracking pattern in {p}')
print(f'SVG checked: {len(list(root.rglob("*.svg")))}; files checked: {sum(1 for p in root.rglob("*") if p.is_file())}')
if errors: print('\n'.join(errors));sys.exit(1)
