import subprocess
import re

url = 'https://web.archive.org/web/2/https://skybound.cx/msfs-2024/navigraph-airac'
p = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '10', url], stdout=subprocess.PIPE)
txt = p.stdout.decode('utf-8', errors='ignore')
print("Len:", len(txt))
m = re.search(r'<img[^>]+src=["\']([^"\']*(?:media/file|wp-content)[^"\']*)["\']', txt)
if m:
    print("Found img:", m.group(1))

main_m = re.search(r'<main[^>]*>(.*?)</main>', txt, re.DOTALL)
if main_m:
    print("Main found, len:", len(main_m.group(1)))
