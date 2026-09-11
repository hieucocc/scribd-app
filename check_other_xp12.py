import subprocess
import re
import json
import sys

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

other_xp12 = ['737-max', 'airac-2604', 'xp12-global-scenery', 'xp12-nodvd', 'xrotors-aw109', 'xrotors-aw139', 'xorganizer']

for name in other_xp12:
    cdx_url = f"https://web.archive.org/cdx/search/cdx?url=skybound.cx/xplane-12/{name}&output=json"
    p = subprocess.run(['curl.exe', '-s', cdx_url], stdout=subprocess.PIPE)
    try:
        raw = json.loads(p.stdout.decode('utf-8'))
        rows = [r for r in raw[1:] if r[4] == '200']
    except Exception:
        rows = []
    print(f"\n=== {name}: {len(rows)} snapshots ===")
    for r in rows:
        ts = r[1]
        url = f"https://web.archive.org/web/{ts}mp_/https://skybound.cx/xplane-12/{name}"
        fp = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '10', url], stdout=subprocess.PIPE)
        c = fp.stdout.decode('utf-8', errors='ignore')
        
        pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', c, re.DOTALL)
        combined = ''
        for item in pushes:
            try: combined += json.loads(f'"{item}"') + '\n'
            except: combined += item + '\n'
        if not combined: combined = c
        
        v_match = re.search(r'"versions":\s*(\[\{.*?\}\])', combined)
        links = re.findall(r'https?://[^\s"\'<>\\]*(?:modsfire|buzzheavier|mega\.nz|vaultdrop)[^\s"\'<>\\]*', combined)
        if v_match or links:
            print(f"  [{ts}] FOUND! Vers:", v_match.group(1)[:100] if v_match else 'None', "Links:", list(set(links)))
