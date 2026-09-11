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

# The 12 remaining items
targets = [
    'blackbird-sr71', 'miltechsim-m2k-c', 'fslabs-controlcenter',
    'gotfriends-aeroprakt-a32-vixxen', 'gotfriends-project-crosskart',
    'land3-vraas', 'maddog-xx', 'miltech-mv22osprey',
    'p42-chaseplane', 'p42-flow-pro', 'rexatmoscore', 'tritrisim-gfx'
]

print(f"=== BẮT ĐẦU QUÉT TẤT CẢ CDX VÀ SNAPSHOTS CHO 12 ADDON ===", flush=True)

for idx, slug in enumerate(targets, 1):
    print(f"\n[{idx}/12] Đang kiểm tra {slug}...", flush=True)
    # Query CDX without fl
    cdx_url = f"https://web.archive.org/cdx/search/cdx?url=skybound.cx/msfs-2024/{slug}*&output=json"
    p = subprocess.run(['curl.exe', '-s', '--connect-timeout', '6', '--max-time', '12', cdx_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        raw_cdx = json.loads(p.stdout.decode('utf-8'))
    except Exception as e:
        print(f"  -> Lỗi gọi CDX: {e}", flush=True)
        continue
        
    if len(raw_cdx) <= 1:
        print(f"  -> 0 snapshots trên Wayback.", flush=True)
        continue
        
    # Get columns
    header = raw_cdx[0]
    ts_idx = header.index('timestamp') if 'timestamp' in header else 1
    orig_idx = header.index('original') if 'original' in header else 2
    status_idx = header.index('statuscode') if 'statuscode' in header else 4
    
    rows = [r for r in raw_cdx[1:] if r[status_idx] == '200']
    print(f"  -> Tìm thấy {len(rows)} snapshots HTTP 200", flush=True)
    
    # Sort newest first
    rows_sorted = sorted(rows, key=lambda x: x[ts_idx], reverse=True)
    
    found_links = []
    found_versions = []
    
    for r in rows_sorted:
        ts = r[ts_idx]
        orig = r[orig_idx]
        
        # Check standard mp_
        test_url = f"https://web.archive.org/web/{ts}mp_/{orig}"
        fp = subprocess.run(['curl.exe', '-s', '-L', '--connect-timeout', '5', '--max-time', '10', test_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        c = fp.stdout.decode('utf-8', errors='ignore')
        
        # Extract pushes
        pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', c, re.DOTALL)
        combined = ''
        for item in pushes:
            try:
                combined += json.loads(f'"{item}"') + '\n'
            except Exception:
                combined += item + '\n'
        if not combined:
            combined = c
            
        # Extract versions
        v_match = re.search(r'"versions":\s*(\[\{.*?\}\])', combined)
        if v_match:
            try:
                varr = json.loads(v_match.group(1))
                for v in varr:
                    u = v.get('url')
                    if u and isinstance(u, str) and u.strip().startswith('http'):
                        found_versions.append(v)
            except Exception:
                pass
                
        # Find external hosts
        for host in ['modsfire.com', 'buzzheavier.com', 'mega.nz', 'vaultdrop.me', 'mediafire.com']:
            fl = re.findall(rf'https?://[^\s"\'<>\\]*{host}[^\s"\'<>\\]*', combined)
            for link in fl:
                clean_l = link.replace('\\"', '').replace('\\', '').rstrip('/.,;)')
                if clean_l.startswith('http'):
                    found_links.append(clean_l)
                    
        if len(found_versions) > 0 or len(found_links) > 0:
            print(f"  🎉 SNAPSHOT {ts} CÓ LINK!", flush=True)
            print(f"     Versions: {found_versions}", flush=True)
            print(f"     Extra links: {found_links}", flush=True)
            break
        else:
            has_clerk = 'Sign in to Download' in combined
            has_direct = 'downloadType":"direct"' in combined
            info = "Clerk Auth" if has_clerk else ("Direct internal (url: null)" if has_direct else "Trống")
            print(f"  - Snapshot {ts}: {info}", flush=True)
            
        time.sleep(0.3)
        
    # If found, update cache
    if len(found_versions) > 0 or len(found_links) > 0:
        clean_extra = list(set(found_links))
        if slug in cache:
            if found_versions:
                cache[slug]['versions'] = found_versions
            if clean_extra:
                cache[slug]['extra_links'] = clean_extra
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
            print(f"  ✅ ĐÃ CẬP NHẬT CACHE CHO {slug}!", flush=True)

print("\n=== QUÉT HOÀN TẤT ===", flush=True)
