import subprocess
import re

for u in [
    'https://web.archive.org/web/2/https://skybound.cx/msfs-2020/baw-aerosoft-crj',
    'https://web.archive.org/web/2/https://skybound.cx/msfs-2020/aerosoft-crj',
    'https://web.archive.org/web/2/https://skybound.cx/msfs-2024/baw-aerosoft-crj'
]:
    p = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '6', u], stdout=subprocess.PIPE)
    txt = p.stdout.decode('utf-8', errors='ignore')
    m = re.search(r'<img[^>]+src=["\']([^"\']*(?:media/file|wp-content)[^"\']*)["\']', txt)
    print(u, "Len:", len(txt), "Img:", m.group(1) if m else None)
