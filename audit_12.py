import json
import subprocess
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

targets = [
    'blackbird-sr71', 'miltechsim-m2k-c', 'fslabs-controlcenter',
    'gotfriends-aeroprakt-a32-vixxen', 'gotfriends-project-crosskart',
    'land3-vraas', 'maddog-xx', 'miltech-mv22osprey',
    'p42-chaseplane', 'p42-flow-pro', 'rexatmoscore', 'tritrisim-gfx'
]

print("=== BẮT ĐẦU QUÉT TẤT CẢ TIMESTAMPS CỦA 12 ADDON CHƯA CÓ LINK ===", flush=True)

for idx, t in enumerate(targets, 1):
    cdx_cmd = ['curl.exe', '-s', '--connect-timeout', '6', '--max-time', '10', f'https://web.archive.org/cdx/search/cdx?url=skybound.cx/msfs-2024/{t}*&output=json&fl=timestamp,original,statuscode']
    p = subprocess.run(cdx_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        data = json.loads(p.stdout.decode('utf-8'))
        rows = [r for r in data[1:] if r[2] == '200']
    except Exception:
        rows = []
    
    print(f"\n[{idx}/12] {t}: có {len(rows)} bản lưu 200 OK", flush=True)
    if not rows:
        print("  -> Không có bất kỳ snapshot nào trên Archive.org.", flush=True)
        continue

    # Take unique timestamps
    seen_ts = set()
    uniq_rows = []
    for r in rows:
        if r[0] not in seen_ts:
            seen_ts.add(r[0])
            uniq_rows.append(r)

    for r_idx, r in enumerate(uniq_rows, 1):
        ts = r[0]
        orig = r[1]
        test_url = f"https://web.archive.org/web/{ts}mp_/{orig}"
        fetch_cmd = ['curl.exe', '-s', '-L', '--connect-timeout', '5', '--max-time', '8', test_url]
        fp = subprocess.run(fetch_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        c = fp.stdout.decode('utf-8', errors='ignore')
        
        has_clerk = 'Sign in to Download' in c
        has_direct = 'downloadType":"direct"' in c
        
        # Check versions and external hosts
        found_links = []
        for host in ['modsfire.com', 'buzzheavier.com', 'mega.nz', 'vaultdrop.me', 'mediafire.com']:
            fl = re.findall(rf'https?://[^\s"\'<>\\]*{host}[^\s"\'<>\\]*', c)
            found_links.extend(fl)
            
        v_match = re.search(r'"versions":\s*(\[\{.*?\}\])', c)
        if v_match:
            try:
                varr = json.loads(v_match.group(1))
                for item in varr:
                    u = item.get('url')
                    if u and str(u).startswith('http'):
                        found_links.append(u)
            except Exception:
                pass

        uniq_links = list(set(found_links))
        if uniq_links:
            print(f"  * Snapshot {ts}: 🎉 TÌM THẤY LINK: {uniq_links}", flush=True)
        elif has_direct:
            print(f"  - Snapshot {ts}: [Internal direct] url=null (cần tài khoản skybound)", flush=True)
        elif has_clerk:
            print(f"  - Snapshot {ts}: [Clerk Auth] Sign in to Download", flush=True)
        else:
            print(f"  - Snapshot {ts}: Không có link tải", flush=True)

print("\n=== HOÀN THÀNH QUÉT TOÀN BỘ BẢN LƯU ===", flush=True)
