import json
import subprocess
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Specifically test all known snapshots of p42-chaseplane and others
targets = {
    'p42-chaseplane': ['20260522073342', '20260526220714', '20260719040927', '20260814113430'],
    'rexatmoscore': ['20260719040845', '20260806012038', '20260814113430'],
    'tritrisim-gfx': ['20260526220714', '20260719040927', '20260814113430'],
    'maddog-xx': ['20260526220714', '20260719040927', '20260814113430'],
    'land3-vraas': ['20260526220714', '20260719040927', '20260814113430'],
}

CACHE_FILE = "public/extracted_cache.json"
with open(CACHE_FILE, 'r', encoding='utf-8') as f:
    cache = json.load(f)

for slug, snaps in targets.items():
    print(f"\nKiểm tra chi tiết cho {slug} với các snapshots: {snaps}")
    found = False
    for ts in snaps:
        url = f"https://web.archive.org/web/{ts}mp_/https://skybound.cx/msfs-2024/{slug}"
        p = subprocess.run(['curl.exe', '-s', '-L', '--connect-timeout', '5', '--max-time', '10', url], stdout=subprocess.PIPE)
        c = p.stdout.decode('utf-8', errors='ignore')
        
        pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', c, re.DOTALL)
        combined = ''
        for item in pushes:
            try:
                combined += json.loads(f'"{item}"') + '\n'
            except Exception:
                combined += item + '\n'
        if not combined:
            combined = c
            
        links = []
        for host in ['modsfire.com', 'buzzheavier.com', 'mega.nz', 'vaultdrop.me', 'mediafire.com']:
            fl = re.findall(rf'https?://[^\s"\'<>\\]*{host}[^\s"\'<>\\]*', combined)
            links.extend(fl)
            
        v_match = re.search(r'"versions":\s*(\[\{.*?\}\])', combined)
        vers = []
        if v_match:
            try:
                varr = json.loads(v_match.group(1))
                for v in varr:
                    u = v.get('url')
                    if u and str(u).startswith('http'):
                        vers.append(v)
            except Exception:
                pass
                
        if vers or links:
            print(f"  🎉 [{slug} @ {ts}] TÌM THẤY LINK: vers={vers}, links={links}")
            cache[slug]['versions'] = vers if vers else [{'versionNumber': 'Latest', 'downloadType': 'link', 'url': links[0]}]
            if links:
                cache[slug]['extra_links'] = list(set(links))
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
            found = True
            break
        else:
            has_clerk = 'Sign in to Download' in combined
            has_direct = 'downloadType":"direct"' in combined
            print(f"  - Snapshot {ts}: {'Clerk Auth' if has_clerk else ('Direct internal download' if has_direct else 'No links')}")
