import json
import subprocess
import re

with open('public/extracted_cache.json', 'r', encoding='utf-8') as f:
    cache = json.load(f)

# Helper to fetch article details from archive.org
def fetch_details(url):
    p = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '10', url], stdout=subprocess.PIPE)
    txt = p.stdout.decode('utf-8', errors='ignore')
    img_m = re.search(r'<img[^>]+src=["\']([^"\']*(?:media/file|wp-content)[^"\']*)["\']', txt)
    img_url = None
    if img_m:
        raw = img_m.group(1)
        img_url = f"https://web.archive.org{raw}" if raw.startswith('/web/') else raw

    main_m = re.search(r'<main[^>]*>(.*?)</main>', txt, re.DOTALL)
    paras, feats = [], []
    if main_m:
        m_html = main_m.group(1)
        p_matches = re.findall(r'<p[^>]*>(.*?)</p>', m_html, re.DOTALL)
        for pm in p_matches:
            clean = re.sub(r'<[^>]+>', '', pm).strip()
            clean = clean.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"').replace('&nbsp;', ' ')
            if len(clean) > 20 and not any(ign in clean for ign in ['Sign in', 'Login', 'Discord', 'Tutorial on extracting']):
                paras.append(clean)

        li_matches = re.findall(r'<li[^>]*>(.*?)</li>', m_html, re.DOTALL)
        for lim in li_matches:
            clean = re.sub(r'<[^>]+>', '', lim).strip()
            clean = clean.replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"').replace('&nbsp;', ' ')
            if len(clean) > 20 and not any(ign in clean for ign in ['Home', 'Microsoft', 'X-Plane', 'Terms', 'Privacy']):
                feats.append(clean)
    return img_url, paras, feats

# 1. Navigraph
print("Enriching Navigraph...")
nav_img, nav_paras, nav_feats = fetch_details('https://web.archive.org/web/2/https://skybound.cx/msfs-2024/navigraph-airac')
if 'navigraph-airac' in cache:
    if nav_img: cache['navigraph-airac']['image'] = nav_img
    if nav_paras: cache['navigraph-airac']['description'] = nav_paras[:5]
    if nav_feats: cache['navigraph-airac']['features'] = nav_feats[:8]

if 'navigraph-airac-2020' in cache:
    if nav_img: cache['navigraph-airac-2020']['image'] = nav_img
    if nav_paras: cache['navigraph-airac-2020']['description'] = nav_paras[:5]
    if nav_feats: cache['navigraph-airac-2020']['features'] = nav_feats[:8]

# 2. BAW Aerosoft CRJ
print("Enriching BAW CRJ...")
crj_img, crj_paras, crj_feats = fetch_details('https://web.archive.org/web/2/https://skybound.cx/msfs-2024/baw-aerosoft-crj')
if 'baw-aerosoft-crj-2020' in cache:
    if crj_img: cache['baw-aerosoft-crj-2020']['image'] = crj_img
    if crj_paras: cache['baw-aerosoft-crj-2020']['description'] = crj_paras[:5]
    if crj_feats: cache['baw-aerosoft-crj-2020']['features'] = crj_feats[:8]

# 3. PMDG 77w 2020 from pmdg-77w
print("Enriching PMDG 77W 2020...")
if 'pmdg-77w-2020' in cache and 'pmdg-77w' in cache:
    src = cache['pmdg-77w']
    cache['pmdg-77w-2020']['image'] = src.get('image')
    cache['pmdg-77w-2020']['description'] = src.get('description')
    cache['pmdg-77w-2020']['features'] = src.get('features')
    cache['pmdg-77w-2020']['changelog'] = src.get('changelog')

# 4. Fenix A320 2020 from fenix-a32x
print("Enriching Fenix A320 2020...")
if 'fenix-a32x-2020' in cache and 'fenix-a32x' in cache:
    src = cache['fenix-a32x']
    cache['fenix-a32x-2020']['image'] = src.get('image')
    cache['fenix-a32x-2020']['description'] = src.get('description')
    cache['fenix-a32x-2020']['features'] = src.get('features')
    cache['fenix-a32x-2020']['changelog'] = src.get('changelog')

# 5. TFDi MD-11 2020 from tfdi-md11
print("Enriching TFDi MD-11 2020...")
if 'tfdi-md11-2020' in cache and 'tfdi-md11' in cache:
    src = cache['tfdi-md11']
    cache['tfdi-md11-2020']['image'] = src.get('image')
    cache['tfdi-md11-2020']['description'] = src.get('description')
    cache['tfdi-md11-2020']['features'] = src.get('features')
    cache['tfdi-md11-2020']['changelog'] = src.get('changelog')

with open('public/extracted_cache.json', 'w', encoding='utf-8') as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)

print("Hoàn tất enrich MSFS 2020!")
