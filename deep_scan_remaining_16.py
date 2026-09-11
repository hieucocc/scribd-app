import json
import re
import subprocess
import time
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CACHE_FILE = "public/extracted_cache.json"
with open(CACHE_FILE, 'r', encoding='utf-8') as f:
    cache = json.load(f)

# The remaining locked addons in MSFS 2024
locked_slugs = []
for k, v in cache.items():
    if v.get('sim') == 'msfs-2024':
        valid_v = [x for x in v.get('versions', []) if x.get('url') and isinstance(x.get('url'), str) and x.get('url').startswith('http')]
        valid_extra = [x for x in v.get('extra_links', []) if isinstance(x, str) and x.startswith('http')]
        if len(valid_v) == 0 and len(valid_extra) == 0:
            locked_slugs.append(k)

print(f"Tổng cộng có {len(locked_slugs)} addons đang bị khóa cần kiểm tra TOÀN BỘ timestamps:")
for idx, s in enumerate(locked_slugs, 1):
    print(f"  {idx}. {s} - {cache[s].get('title')}")

recovered = 0

for idx, slug in enumerate(locked_slugs, 1):
    print(f"\n=======================================================")
    print(f"[{idx}/{len(locked_slugs)}] Đang quét toàn bộ lịch sử cho: {slug}")
    print(f"=======================================================")
    
    # 1. Query CDX for all snapshots of this slug
    cdx_url = f"https://web.archive.org/cdx/search/cdx?url=skybound.cx/msfs-2024/{slug}*&output=json&fl=timestamp,original,statuscode"
    cmd = ["curl.exe", "-s", "--max-time", "12", cdx_url]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        raw_cdx = json.loads(p.stdout.decode('utf-8'))
        if len(raw_cdx) <= 1:
            print(f"  -> Archive.org KHÔNG CÓ bất kỳ bản lưu nào cho: {slug}")
            continue
        snapshots = [r for r in raw_cdx[1:] if r[2] == '200']
    except Exception as e:
        print(f"  -> Lỗi đọc CDX: {e}")
        continue

    print(f"  -> Tìm thấy {len(snapshots)} bản lưu trong lịch sử.")
    
    # Sort snapshots by timestamp (check newest first, but check ALL)
    snapshots_sorted = sorted(snapshots, key=lambda x: x[0], reverse=True)
    
    found_for_this = False
    
    for s_idx, (ts, orig_url, _) in enumerate(snapshots_sorted, 1):
        print(f"    [{s_idx}/{len(snapshots_sorted)}] Thử timestamp {ts} ({orig_url})...")
        
        # Try both mp_ and standard id_ mode
        for mode in ["mp_", "id_"]:
            fetch_url = f"https://web.archive.org/web/{ts}{mode}/{orig_url}"
            fetch_cmd = [
                "curl.exe", "-s", "-L", "--retry", "2", "--retry-delay", "1", "--max-time", "12",
                "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                fetch_url
            ]
            fp = subprocess.run(fetch_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            content = fp.stdout.decode('utf-8', errors='ignore')
            
            if '<title>Wayback Machine</title>' in content or len(content) < 400:
                continue

            # Extract Next.js stream
            pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', content, re.DOTALL)
            combined = ''
            for item in pushes:
                try:
                    combined += json.loads(f'"{item}"') + '\n'
                except Exception:
                    combined += item + '\n'
            
            if not combined:
                combined = content

            # Check versions
            versions = []
            versions_m = re.search(r'"versions":\s*(\[\{.*?\}\])', combined)
            if versions_m:
                try:
                    v_raw = json.loads(versions_m.group(1))
                    for v in v_raw:
                        u = v.get('url')
                        if u and isinstance(u, str) and u.strip().startswith('http'):
                            versions.append(v)
                except Exception:
                    pass

            # Check raw external links
            all_urls = re.findall(r'https?://[^\s"\'<>\\]+', combined)
            extra_links = []
            seen = {v.get('url') for v in versions}
            for u in all_urls:
                clean_u = u.replace('\\"', '').replace('\\', '').rstrip('/.,;)')
                if any(h in clean_u.lower() for h in ['modsfire.com', 'buzzheavier.com', 'mega.nz', 'mediafire.com', 'drive.google.com', 'pastebin.com', 'flightsim.to']):
                    if clean_u not in seen:
                        extra_links.append(clean_u)
                        seen.add(clean_u)

            if len(versions) > 0 or len(extra_links) > 0:
                found_for_this = True
                recovered += 1
                title_m = re.search(r'<title>(.*?)</title>', content, re.I)
                real_title = title_m.group(1).replace(' | Skybound', '').strip() if title_m else cache[slug].get('title')
                pwd_m = re.search(r'Archive password is:\s*.*?href=["\']([^"\']+)["\']', combined, re.I)
                pwd = pwd_m.group(1) if pwd_m else 'https://skybound.cx'

                cache[slug]['versions'] = versions
                cache[slug]['extra_links'] = extra_links
                cache[slug]['title'] = real_title
                cache[slug]['password'] = pwd
                cache[slug]['url'] = fetch_url

                with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(cache, f, ensure_ascii=False, indent=2)

                print(f"    🎉 [THÀNH CÔNG] Tìm thấy {len(versions)} versions, {len(extra_links)} extra links tại timestamp {ts}!")
                break
        
        if found_for_this:
            break
        time.sleep(0.4)

    if not found_for_this:
        print(f"  🔒 [KẾT LUẬN] {slug}: Đã duyệt toàn bộ {len(snapshots_sorted)} timestamps nhưng 100% đều bị khóa Clerk / không có link.")

    time.sleep(0.5)

print("\n=======================================================")
print(f"HOÀN TẤT! Đã cứu thêm {recovered} addons.")
print("=======================================================")
