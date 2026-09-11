import json
import subprocess
import re

with open('public/extracted_cache.json', 'r', encoding='utf-8') as f:
    cache = json.load(f)

# 1. Inspect what we have for counterparts
print("Checking counterparts...")
if 'pmdg-77w' in cache:
    print("pmdg-77w img:", cache['pmdg-77w'].get('image'))
if 'fenix-a32x' in cache:
    print("fenix-a32x img:", cache['fenix-a32x'].get('image'))
if 'aerosoft-crj-v2' in cache:
    print("aerosoft-crj-v2 img:", cache['aerosoft-crj-v2'].get('image'))
if 'navigraph-airac' in cache:
    print("navigraph-airac img:", cache['navigraph-airac'].get('image'))

# Test fetching TFDi MD-11
test_urls = [
    'https://web.archive.org/web/2/https://skybound.cx/msfs-2020/tfdi-md11',
    'https://web.archive.org/web/2/https://skybound.cx/msfs-2020/tfdi-design-md-11',
    'https://web.archive.org/web/2/https://skybound.cx/msfs-2024/tfdi-md-11',
    'https://web.archive.org/web/2/https://skybound.cx/msfs-2020/md11'
]

for u in test_urls:
    p = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '6', u], stdout=subprocess.PIPE)
    txt = p.stdout.decode('utf-8', errors='ignore')
    print(u, "Len:", len(txt))
    m = re.search(r'<img[^>]+src=["\']([^"\']*(?:media/file|wp-content)[^"\']*)["\']', txt)
    if m:
        print("Found img:", m.group(1))
