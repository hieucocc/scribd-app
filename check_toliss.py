import subprocess
import re
import json
import sys

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

snaps = {
    'toliss-a319': ['20260511202657', '20260815220531'],
    'toliss-a320': ['20260511202657', '20260815220531'],
    'toliss-a321': ['20260511202657', '20260815220531'],
    'toliss-a346': ['20260511202657', '20260815220531'],
    'flightfactor-a350': ['20260511202657', '20260815220531'],
    '737-max': ['20260511202657', '20260815220531']
}

for name, ts_list in snaps.items():
    print(f"\n=== Kiểm tra {name} ===")
    for ts in ts_list:
        url = f"https://web.archive.org/web/{ts}mp_/https://skybound.cx/xplane-12/{name}"
        p = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '12', url], stdout=subprocess.PIPE)
        c = p.stdout.decode('utf-8', errors='ignore')
        
        pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', c, re.DOTALL)
        combined = ''
        for item in pushes:
            try:
                combined += json.loads(f'"{item}"') + '\n'
            except Exception:
                combined += item + '\n'
        if not combined: combined = c
        
        v_match = re.search(r'"versions":\s*(\[\{.*?\}\])', combined)
        if v_match:
            print(f"  [{ts}] Versions:", v_match.group(1)[:200])
            
        links = []
        for host in ['modsfire.com', 'buzzheavier.com', 'mega.nz', 'vaultdrop.me']:
            fl = re.findall(rf'https?://[^\s"\'<>\\]*{host}[^\s"\'<>\\]*', combined)
            links.extend(fl)
            
        if links:
            print(f"  [{ts}] Links:", list(set(links)))
