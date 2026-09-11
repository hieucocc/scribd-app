import subprocess
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

url = 'https://web.archive.org/web/20260806012023mp_/https://skybound.cx/msfs-2024/pmdg-738'
p = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '15', url], stdout=subprocess.PIPE)
c = p.stdout.decode('utf-8', errors='ignore')

# 1. Check images in HTML
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', c)
print('Images in HTML count:', len(imgs))
for img in imgs[:5]:
    print('  Image:', img)

# 2. Extract pushes
pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', c, re.DOTALL)
combined = ''
for item in pushes:
    try: combined += json.loads(f'"{item}"') + '\n'
    except: combined += item + '\n'

print('Combined Next.js stream length:', len(combined))

# Find keys like description, content, body, summary, image, coverImage, etc.
for key in ['description', 'content', 'summary', 'body', 'overview', 'image', 'cover', 'thumbnail', 'features']:
    matches = re.findall(rf'"{key}":\s*("[^"]+"|\{{.*?\}}|\[.*?\])', combined)
    if matches:
        print(f'Key "{key}" has {len(matches)} matches:')
        for m in matches[:2]:
            print(f'   -> {m[:150]}...')

# Let us also look at HTML text paragraphs or article body
paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', c, re.DOTALL)
print(f'HTML <p> tags count: {len(paragraphs)}')
for p_text in paragraphs[:5]:
    clean_p = re.sub(r'<[^>]+>', '', p_text).strip()
    if clean_p:
        print('  Paragraph:', clean_p[:120])
