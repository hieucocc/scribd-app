import subprocess
import re

p = subprocess.run(['curl.exe', '-s', '-L', 'https://modsfire.com/k6Ri8xiZ7NklhL9'], stdout=subprocess.PIPE)
txt = p.stdout.decode('utf-8', errors='ignore')
title = re.search(r'<title>(.*?)</title>', txt)
print('Title:', title.group(1) if title else 'No title')
desc = re.search(r'<meta name="description" content="(.*?)"', txt)
print('Desc:', desc.group(1) if desc else 'No desc')
for line in txt.splitlines():
    if any(k in line.lower() for k in ['filename', '.rar', '.zip', '.7z', 'file-name', 'download-button', 'size', 'ifly', 'mb', 'gb']):
        print('  >', line.strip()[:120])
