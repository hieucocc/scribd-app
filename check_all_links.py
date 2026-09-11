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

# Extract all links
items_to_check = []
for k, v in cache.items():
    title = v.get('title', k)
    sim = v.get('sim', 'msfs-2024')
    for ver in v.get('versions', []):
        u = ver.get('url')
        if u and isinstance(u, str) and u.startswith('http'):
            items_to_check.append({
                'slug': k,
                'title': title,
                'sim': sim,
                'version': ver.get('versionNumber', 'Latest'),
                'url': u,
                'source': 'version'
            })
    for u in v.get('extra_links', []):
        if u and isinstance(u, str) and u.startswith('http'):
            if not any(x['url'] == u for x in items_to_check):
                items_to_check.append({
                    'slug': k,
                    'title': title,
                    'sim': sim,
                    'version': 'Extra Link',
                    'url': u,
                    'source': 'extra'
                })

print(f"Bắt đầu kiểm tra toàn bộ {len(items_to_check)} link download...", flush=True)

alive_links = []
dead_links = []
cf_links = [] # buzzheavier/cloudflare

for idx, item in enumerate(items_to_check, 1):
    u = item['url']
    slug = item['slug']
    title = item['title']
    ver = item['version']
    
    cmd = [
        'curl.exe', '-s', '-L', '--connect-timeout', '6', '--max-time', '12',
        '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        '-w', '\nHTTP_CODE:%{http_code}',
        u
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    c = p.stdout.decode('utf-8', errors='ignore')
    
    code = '000'
    if 'HTTP_CODE:' in c:
        parts = c.split('HTTP_CODE:')
        code = parts[-1].strip()
        body = parts[0]
    else:
        body = c
        
    title_m = re.search(r'<title>(.*?)</title>', body, re.I)
    page_title = title_m.group(1).strip() if title_m else ''
    
    is_dead = False
    dead_reason = ''
    filename = ''
    
    # 1. Modsfire check
    if 'modsfire.com' in u:
        if code == '404' or 'Page Not Found' in page_title or 'File Not Found' in body:
            is_dead = True
            dead_reason = f'HTTP {code} - Page Not Found'
        elif 'Download file' in page_title:
            is_dead = False
            fn_m = re.search(r'Download file (.*?) - ', page_title)
            filename = fn_m.group(1) if fn_m else ''
        elif code == '200':
            is_dead = False
        else:
            is_dead = True
            dead_reason = f'HTTP {code}'
            
    # 2. Buzzheavier check
    elif 'buzzheavier.com' in u:
        if code == '404':
            is_dead = True
            dead_reason = 'HTTP 404 - File Not Found'
        elif code == '403' or 'Just a moment' in page_title:
            # Cloudflare bot challenge, needs browser check
            cf_links.append(item)
            print(f"[{idx}/{len(items_to_check)}] 🛡️ CF: {title} ({ver}) -> {u}", flush=True)
            continue
        elif code == '200':
            is_dead = False
        else:
            is_dead = True
            dead_reason = f'HTTP {code}'
            
    # 3. Other hosts
    else:
        if code in ['404', '410', '000']:
            is_dead = True
            dead_reason = f'HTTP {code}'
        elif 'not found' in page_title.lower() or 'deleted' in page_title.lower() or 'removed' in body.lower():
            is_dead = True
            dead_reason = f'Deleted/Removed ({page_title})'
        elif code in ['200', '302', '301']:
            is_dead = False
        else:
            dead_reason = f'HTTP {code}'
            is_dead = True

    if is_dead:
        item['dead_reason'] = dead_reason
        dead_links.append(item)
        print(f"[{idx}/{len(items_to_check)}] ❌ DEAD: {title} ({ver}) -> {u} [{dead_reason}]", flush=True)
    else:
        item['filename'] = filename
        alive_links.append(item)
        print(f"[{idx}/{len(items_to_check)}] ✅ ALIVE: {title} ({ver}) [{filename or page_title or code}]", flush=True)

    time.sleep(0.1)

print("\n=======================================================", flush=True)
print(f"TỔNG KẾT KIỂM TRA LINK DOWNLOAD:", flush=True)
print(f"  - Tổng số link kiểm tra: {len(items_to_check)}", flush=True)
print(f"  - Link hoạt động tốt (ALIVE): {len(alive_links)}", flush=True)
print(f"  - Link chết / 404 / đã bị xóa (DEAD): {len(dead_links)}", flush=True)
print(f"  - Link có Cloudflare (Buzzheavier): {len(cf_links)}", flush=True)
print("=======================================================", flush=True)

# Save dead links to json for easy inspection & removal
with open("dead_links_report.json", "w", encoding="utf-8") as f:
    json.dump({
        'total': len(items_to_check),
        'alive_count': len(alive_links),
        'dead_count': len(dead_links),
        'cf_count': len(cf_links),
        'dead_links': dead_links,
        'cf_links': cf_links
    }, f, ensure_ascii=False, indent=2)

print("Đã lưu chi tiết vào dead_links_report.json", flush=True)
