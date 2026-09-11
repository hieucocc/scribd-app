import subprocess
import re
import json

snapshots = [
    ("20260629220917", "https://web.archive.org/web/20260629220917mp_/https://skybound.cx/msfs-2024/ifly-737max8"),
    ("20260701214041", "https://web.archive.org/web/20260701214041mp_/https://skybound.cx/msfs-2024/ifly-737max8"),
    ("20260713163450", "https://web.archive.org/web/20260713163450id_/https://skybound.cx/msfs-2024/ifly-737max8?_rsc=10iaq"),
    ("20260713163451", "https://web.archive.org/web/20260713163451id_/https://skybound.cx/msfs-2024/ifly-737max8?_rsc=xbrhb"),
]

for ts, url in snapshots:
    p = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '15', url], stdout=subprocess.PIPE)
    txt = p.stdout.decode('utf-8', errors='ignore')
    print(f"\n==================== Snapshot: {ts} (Length: {len(txt)}) ====================")
    
    # 1. Any download hosts
    hosts_pattern = r'https?://(?:modsfire\.com|buzzheavier\.com|drive\.google\.com|mega\.nz|pixeldrain\.com|1fichier\.com|mediafire\.com|fileditchfiles\.st|gofile\.io|qiwi\.gg|pastebin\.com)[^\s"\'<>\\]+'
    found = re.findall(hosts_pattern, txt)
    print("Found external host links:", list(set(found)))
    
    # 2. Any magnet or torrent
    magnets = re.findall(r'magnet:\?[^\s"\'<>\\]+', txt)
    torrents = re.findall(r'https?://[^\s"\'<>\\]+\.torrent', txt)
    print("Found magnets:", list(set(magnets)))
    print("Found torrents:", list(set(torrents)))
    
    # 3. Look for versions / download buttons
    btns = re.findall(r'<button[^>]*>([^<]+)</button>', txt)
    print("Buttons:", btns)
    
    # 4. Check for any urls in script or JSON objects
    all_urls = re.findall(r'https?://[^\s"\'<>\\]+', txt)
    filtered = [u for u in all_urls if not any(x in u for x in ['archive.org', 'w3.org', 'schema.org', 'skybound.cx/api/media', 'fonts.'])]
    print("Other candidate URLs:", list(set(filtered))[:10])

