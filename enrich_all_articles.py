import json
import subprocess
import re
import sys
import time

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

CACHE_FILE = "public/extracted_cache.json"
with open(CACHE_FILE, 'r', encoding='utf-8') as f:
    cache = json.load(f)

print(f"Bắt đầu enrich bài viết còn thiếu trong {len(cache)} addons...", flush=True)

success_count = 0

for slug, item in list(cache.items()):
    # Skip if already has description and image
    if item.get('description') and item.get('image') and len(item.get('description', [])) > 0:
        continue

    sim = item.get('sim', 'msfs-2024')
    # Try web/2/ URL
    fetch_url = f"https://web.archive.org/web/2/https://skybound.cx/{sim}/{slug}"
    
    cmd = ['curl.exe', '-s', '-L', '--connect-timeout', '5', '--max-time', '10', fetch_url]
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    c = p.stdout.decode('utf-8', errors='ignore')
    
    if len(c) < 1000:
        # If sim is msfs-2020 or xplane-12, try msfs-2024 or vice versa if applicable
        continue

    # 1. Extract cover image
    img_m = re.search(r'<img[^>]+src=["\']([^"\']*(?:media/file|wp-content)[^"\']*)["\']', c)
    image_url = None
    if img_m:
        raw_src = img_m.group(1)
        if raw_src.startswith('/web/'):
            image_url = f"https://web.archive.org{raw_src}"
        elif raw_src.startswith('http'):
            image_url = raw_src
        elif raw_src.startswith('/'):
            ts_m = re.search(r'web/(\d+)', fetch_url)
            ts = ts_m.group(1) if ts_m else '20260713163505'
            image_url = f"https://web.archive.org/web/{ts}im_/https://skybound.cx{raw_src}"

    # 2. Extract description paragraphs and features from main
    main_m = re.search(r'<main[^>]*>(.*?)</main>', c, re.DOTALL)
    paras = []
    features = []
    changelog = []
    
    if main_m:
        m_html = main_m.group(1)
        
        # Paragraphs
        p_matches = re.findall(r'<p[^>]*>(.*?)</p>', m_html, re.DOTALL)
        for pm in p_matches:
            clean = re.sub(r'<[^>]+>', '', pm).strip()
            clean = clean.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"').replace('&nbsp;', ' ')
            if len(clean) > 20 and not any(ign in clean for ign in ['Sign in', 'Login', 'Discord', 'Tutorial on extracting']):
                if 'Changelog' in clean:
                    changelog.append(clean)
                else:
                    paras.append(clean)
                    
        # Feature bullets
        li_matches = re.findall(r'<li[^>]*>(.*?)</li>', m_html, re.DOTALL)
        for lim in li_matches:
            clean = re.sub(r'<[^>]+>', '', lim).strip()
            clean = clean.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"').replace('&nbsp;', ' ')
            if len(clean) > 20 and not any(ign in clean for ign in ['Home', 'Microsoft', 'X-Plane', 'Terms', 'Privacy']):
                features.append(clean)

    if image_url or paras:
        success_count += 1
        if image_url and not item.get('image'): item['image'] = image_url
        if paras and not item.get('description'): item['description'] = paras[:5]
        if features and not item.get('features'): item['features'] = features[:8]
        if changelog and not item.get('changelog'): item['changelog'] = changelog
        print(f"[{success_count}] Đã lấy bài viết cho: {slug} (Ảnh: {bool(image_url)}, Đoạn: {len(paras)}, Feat: {len(features)})", flush=True)

        # Save immediately so UI gets it
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)

print(f"Hoàn thành! Thêm thành công {success_count} bài viết.", flush=True)
