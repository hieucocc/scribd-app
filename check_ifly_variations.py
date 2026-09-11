import subprocess
import re

urls = [
    'https://skybound.cx/msfs-2024/ifly-737max8',
    'https://skybound.cx/msfs-2024/ifly-737-max8',
    'https://skybound.cx/msfs-2024/ifly-737-max-8',
    'https://skybound.cx/msfs-2024/ifly-max8',
    'https://skybound.cx/msfs-2024/ifly-jets-737-max8',
    'https://skybound.cx/msfs-2024/ifly-aircraft-737max8',
    'https://skybound.cx/msfs-2020/ifly-737max8',
    'https://skybound.cx/msfs-2020/ifly-737-max8',
    'https://skybound.cx/msfs-2020/ifly-max8'
]

hosts_pattern = r'https?://(?:modsfire\.com|buzzheavier\.com|drive\.google\.com|mega\.nz|pixeldrain\.com|1fichier\.com|mediafire\.com|fileditchfiles\.st|gofile\.io|qiwi\.gg|pastebin\.com)[^\s"\'<>\\]+'

for u in urls:
    fetch_url = f"https://web.archive.org/web/2/{u}"
    p = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '10', fetch_url], stdout=subprocess.PIPE)
    txt = p.stdout.decode('utf-8', errors='ignore')
    if len(txt) > 2000 and "Temporarily Offline" not in txt and "Wayback Machine has not archived" not in txt:
        title = re.search(r'<title>(.*?)</title>', txt)
        links = re.findall(hosts_pattern, txt)
        print(f"MATCH: {u} | Title: {title.group(1) if title else 'No title'} | Len: {len(txt)} | Links: {set(links)}")
    else:
        print(f"No snapshot for {u} (len={len(txt)})")
