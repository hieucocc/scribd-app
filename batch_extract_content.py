import subprocess
import re
import json
import sys

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

test_slugs = ['fenix-a32x', 'flysimware-learjet-35a', 'inibuilds-a350', 'bksq-tbm-850']

for slug in test_slugs:
    url = f'https://web.archive.org/web/20260806012023mp_/https://skybound.cx/msfs-2024/{slug}'
    p = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '12', url], stdout=subprocess.PIPE)
    c = p.stdout.decode('utf-8', errors='ignore')
    
    # Image
    img_m = re.search(r'<img[^>]+src=["\']([^"\']*(?:media/file|wp-content)[^"\']*)["\']', c)
    img_url = img_m.group(1) if img_m else None
    
    # Paragraphs in main
    main_m = re.search(r'<main[^>]*>(.*?)</main>', c, re.DOTALL)
    paras = []
    features = []
    if main_m:
        m_html = main_m.group(1)
        p_matches = re.findall(r'<p[^>]*>(.*?)</p>', m_html, re.DOTALL)
        for pm in p_matches:
            clean = re.sub(r'<[^>]+>', '', pm).strip()
            if len(clean) > 15 and not 'Sign in' in clean and not 'Login' in clean and not 'Discord' in clean:
                paras.append(clean)
                
        li_matches = re.findall(r'<li[^>]*>(.*?)</li>', m_html, re.DOTALL)
        for lim in li_matches:
            clean = re.sub(r'<[^>]+>', '', lim).strip()
            if len(clean) > 20 and not 'Home' in clean and not 'Microsoft' in clean:
                features.append(clean)
                
    print(f"\n=== {slug} ===")
    print('  Image:', img_url)
    print(f'  Paragraphs ({len(paras)}):')
    for p in paras[:3]:
        print('    -', p[:100] + '...')
    print(f'  Features ({len(features)}):')
    for f in features[:3]:
        print('    *', f[:100] + '...')
