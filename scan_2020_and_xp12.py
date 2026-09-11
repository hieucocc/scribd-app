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

print("=== BẮT ĐẦU QUÉT CHI TIẾT TẤT CẢ SNAPSHOT CHO MSFS 2020 VÀ X-PLANE 12 ===", flush=True)

# 1. First, get all snapshots for MSFS 2020 and X-Plane 12
for sim_prefix, sim_name in [('skybound.cx/msfs-2020/*', 'msfs-2020'), ('skybound.cx/xplane-12/*', 'xplane-12')]:
    print(f"\n=======================================================", flush=True)
    print(f"Đang quét danh mục: {sim_name.upper()}", flush=True)
    print(f"=======================================================", flush=True)
    
    cdx_url = f"https://web.archive.org/cdx/search/cdx?url={sim_prefix}&output=json"
    p = subprocess.run(['curl.exe', '-s', '--connect-timeout', '6', '--max-time', '15', cdx_url], stdout=subprocess.PIPE)
    try:
        raw_cdx = json.loads(p.stdout.decode('utf-8'))
        rows = [r for r in raw_cdx[1:] if r[4] == '200']
    except Exception as e:
        print(f"Lỗi đọc CDX: {e}", flush=True)
        continue

    # Group by original URL
    by_orig = {}
    for r in rows:
        ts = r[1]
        orig = r[2]
        # Clean query params if any
        base_orig = orig.split('?')[0].rstrip('/')
        if base_orig not in by_orig:
            by_orig[base_orig] = []
        by_orig[base_orig].append((ts, orig))

    print(f"Tìm thấy {len(by_orig)} trang độc lập trong {sim_name}:", flush=True)
    for orig_url, snap_list in by_orig.items():
        slug = orig_url.split('/')[-1]
        if slug in [sim_name, '']:
            continue
            
        print(f"\n-> Addon [{slug}]: {len(snap_list)} bản lưu", flush=True)
        
        # Sort newest first
        snap_list_sorted = sorted(snap_list, key=lambda x: x[0], reverse=True)
        found_for_slug = False
        
        for ts, full_orig in snap_list_sorted:
            fetch_url = f"https://web.archive.org/web/{ts}mp_/{full_orig}"
            fp = subprocess.run(['curl.exe', '-s', '-L', '--connect-timeout', '5', '--max-time', '10', fetch_url], stdout=subprocess.PIPE)
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
                    
            # Find external hosts
            ext_links = []
            for host in ['modsfire.com', 'buzzheavier.com', 'mega.nz', 'vaultdrop.me', 'mediafire.com']:
                fl = re.findall(rf'https?://[^\s"\'<>\\]*{host}[^\s"\'<>\\]*', combined)
                for l in fl:
                    cl = l.replace('\\"', '').replace('\\', '').rstrip('/.,;)')
                    if cl.startswith('http'):
                        ext_links.append(cl)

            if vers or ext_links:
                title_m = re.search(r'<title>(.*?)</title>', c, re.I)
                t_str = title_m.group(1).replace(' | Skybound', '').strip() if title_m else slug
                pwd_m = re.search(r'Archive password is:\s*.*?href=["\']([^"\']+)["\']', combined, re.I)
                pwd = pwd_m.group(1) if pwd_m else 'https://skybound.cx'
                
                print(f"  🎉 [THÀNH CÔNG] {slug} @ {ts}: {len(vers)} versions, {len(ext_links)} links!", flush=True)
                
                # Check cache
                cache_key = f"{slug}-2020" if sim_name == 'msfs-2020' and not slug.endswith('-2020') else slug
                if cache_key not in cache:
                    cache[cache_key] = {
                        'title': t_str,
                        'slug': slug,
                        'sim': sim_name,
                        'category': 'Airbus' if 'a3' in slug.lower() else ('Boeing' if '73' in slug.lower() or '74' in slug.lower() else 'Other'),
                        'versions': vers,
                        'extra_links': list(set(ext_links)),
                        'password': pwd,
                        'url': full_orig
                    }
                else:
                    if vers:
                        cache[cache_key]['versions'] = vers
                    if ext_links:
                        cache[cache_key]['extra_links'] = list(set(cache[cache_key].get('extra_links', []) + ext_links))
                    if t_str and t_str != slug:
                        cache[cache_key]['title'] = t_str
                        
                with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(cache, f, ensure_ascii=False, indent=2)
                    
                found_for_slug = True
                break
            time.sleep(0.2)
            
        if not found_for_slug:
            print(f"  🔒 {slug}: Không có link tải hợp lệ trong toàn bộ {len(snap_list)} snapshots.", flush=True)

print("\n=== HOÀN TẤT QUÉT MSFS 2020 VÀ X-PLANE 12 ===", flush=True)
