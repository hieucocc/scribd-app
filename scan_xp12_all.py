import json
import subprocess
import re
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CACHE_FILE = "public/extracted_cache.json"
with open(CACHE_FILE, 'r', encoding='utf-8') as f:
    cache = json.load(f)

xp12_pages = [
    'toliss-a319', 'toliss-a320', 'toliss-a321', 'toliss-a32n', 'toliss-a339', 'toliss-a346',
    'flightfactor-a350', '737-max', 'airac-2604', 'navigraph-airac', 'xp12-global-scenery',
    'xp12-nodvd', 'xrotors-aw109', 'xrotors-aw139', 'xorganizer', 'skybound-boeing-747-mini-x'
]

print(f"=== QUÉT TOÀN BỘ {len(xp12_pages)} TRANG X-PLANE 12 TRÊN ARCHIVE.ORG ===", flush=True)

for idx, slug in enumerate(xp12_pages, 1):
    cdx_url = f"https://web.archive.org/cdx/search/cdx?url=skybound.cx/xplane-12/{slug}*&output=json"
    p = subprocess.run(['curl.exe', '-s', '--connect-timeout', '6', '--max-time', '10', cdx_url], stdout=subprocess.PIPE)
    try:
        raw = json.loads(p.stdout.decode('utf-8'))
        rows = [r for r in raw[1:] if r[4] == '200']
    except Exception:
        rows = []
        
    print(f"\n[{idx}/{len(xp12_pages)}] {slug}: {len(rows)} snapshots", flush=True)
    if not rows:
        continue
        
    rows_sorted = sorted(rows, key=lambda x: x[1], reverse=True)
    for r in rows_sorted:
        ts = r[1]
        orig = r[2]
        fetch_url = f"https://web.archive.org/web/{ts}mp_/{orig}"
        fp = subprocess.run(['curl.exe', '-s', '-L', '--connect-timeout', '5', '--max-time', '10', fetch_url], stdout=subprocess.PIPE)
        c = fp.stdout.decode('utf-8', errors='ignore')
        
        pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', c, re.DOTALL)
        combined = ''
        for item in pushes:
            try:
                combined += json.loads(f'"{item}"') + '\n'
            except Exception:
                combined += item + '\n'
        if not combined:
            combined = c
            
        vers = []
        v_match = re.search(r'"versions":\s*(\[\{.*?\}\])', combined)
        if v_match:
            try:
                varr = json.loads(v_match.group(1))
                for v in varr:
                    u = v.get('url')
                    if u and str(u).startswith('http'):
                        vers.append(v)
            except Exception:
                pass
                
        ext_links = []
        for host in ['modsfire.com', 'buzzheavier.com', 'mega.nz', 'vaultdrop.me', 'mediafire.com']:
            fl = re.findall(rf'https?://[^\s"\'<>\\]*{host}[^\s"\'<>\\]*', combined)
            for l in fl:
                cl = l.replace('\\"', '').replace('\\', '').rstrip('/.,;)')
                if cl.startswith('http'):
                    ext_links.append(cl)
                    
        if vers or ext_links:
            title_m = re.search(r'<title>(.*?)</title>', c, re.I)
            real_t = title_m.group(1).replace(' | Skybound', '').strip() if title_m else slug
            pwd_m = re.search(r'Archive password is:\s*.*?href=["\']([^"\']+)["\']', combined, re.I)
            pwd = pwd_m.group(1) if pwd_m else 'https://skybound.cx'
            
            print(f"  🎉 [{slug} @ {ts}] TÌM THẤY: {len(vers)} vers, {len(ext_links)} links! ({real_t})", flush=True)
            for v in vers:
                print(f"     -> {v.get('versionNumber')}: {v.get('url')}", flush=True)
            for l in ext_links:
                print(f"     -> extra: {l}", flush=True)
                
            # Add or update cache
            cache_key = f"xp12-{slug}" if not slug.startswith('xp12-') and slug in cache else slug
            if cache_key not in cache:
                cache[cache_key] = {
                    'title': real_t,
                    'slug': slug,
                    'sim': 'xplane-12',
                    'category': 'Airbus' if 'a3' in slug else ('Boeing' if '73' in slug or '74' in slug else 'Other'),
                    'versions': vers,
                    'extra_links': list(set(ext_links)),
                    'password': pwd,
                    'url': orig
                }
            else:
                if vers: cache[cache_key]['versions'] = vers
                if ext_links: cache[cache_key]['extra_links'] = list(set(cache[cache_key].get('extra_links', []) + ext_links))
                if real_t: cache[cache_key]['title'] = real_t
                
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
            break
        else:
            print(f"  - {slug} @ {ts}: Không có link tải hợp lệ", flush=True)
        time.sleep(0.2)

print("\n=== HOÀN TẤT QUÉT X-PLANE 12 ===", flush=True)
