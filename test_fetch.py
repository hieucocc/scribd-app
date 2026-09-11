import subprocess
import re
import json

cmd = ['curl.exe', '-s', '-L', '--max-time', '10', 'https://web.archive.org/web/2/https://skybound.cx/msfs-2024/bksq-bonanza']
res = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8', errors='ignore')
print('Length:', len(res))
m = re.search(r'<main[^>]*>(.*?)</main>', res, re.DOTALL)
if m:
    print('Found main! Length:', len(m.group(1)))
img = re.search(r'<img[^>]+src=["\']([^"\']*(?:media/file|wp-content)[^"\']*)["\']', res)
if img:
    print('Found img:', img.group(1))
