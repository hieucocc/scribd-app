import urllib.request
import json
import re
import subprocess

# 1. Search CDX API for ifly
queries = [
    'https://web.archive.org/cdx/search/cdx?url=skybound.cx/*ifly*&output=json',
    'https://web.archive.org/cdx/search/cdx?url=*skybound.cx/msfs-2024/ifly-737max8*&output=json',
    'https://web.archive.org/cdx/search/cdx?url=*skybound.cx/msfs-2020/ifly-737max8*&output=json'
]

snapshots = set()
for q in queries:
    try:
        req = urllib.request.Request(q, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if len(data) > 1:
                # header is data[0]: [urlkey, timestamp, original, mimetype, statuscode, digest, length]
                for row in data[1:]:
                    ts = row[1]
                    orig = row[2]
                    status = row[4]
                    if status in ['200', '301', '302']:
                        snapshots.add((ts, orig))
    except Exception as e:
        print(f"Error querying {q}: {e}")

print(f"Total snapshots found: {len(snapshots)}")
for ts, orig in sorted(snapshots):
    print(f"  {ts} -> {orig}")

# Let's inspect each snapshot for download links, torrent links, buzzheavier, modsfire, mega, google drive, fileditch, etc.
found_links = {}

for ts, orig in sorted(snapshots):
    raw_url = f"https://web.archive.org/web/{ts}mp_/{orig}"
    p = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '10', raw_url], stdout=subprocess.PIPE)
    txt = p.stdout.decode('utf-8', errors='ignore')
    
    # Search for links in html
    # 1. Look for hrefs
    urls = re.findall(r'href=["\'](https?://[^"\']+)["\']', txt)
    # 2. Look for any download hosts
    all_dl = re.findall(r'https?://(?:modsfire\.com|buzzheavier\.com|drive\.google\.com|mega\.nz|pixeldrain\.com|1fichier\.com|mediafire\.com|fileditchfiles\.st|gofile\.io|qiwi\.gg)[^\s"\'<>]+', txt)
    
    # 3. Look for magnet links or torrent links
    magnets = re.findall(r'magnet:\?[^\s"\'<>]+', txt)
    torrents = re.findall(r'https?://[^\s"\'<>]+\.torrent', txt)
    
    candidates = list(set(urls + all_dl + magnets + torrents))
    valid_candidates = []
    for c in candidates:
        if any(h in c for h in ['modsfire', 'buzzheavier', 'drive.google', 'mega.nz', 'pixeldrain', '1fichier', 'mediafire', 'fileditch', 'gofile', 'qiwi', 'pastebin', 'magnet:']) or c.endswith('.torrent'):
            valid_candidates.append(c)
            
    # Check versions
    ver_matches = re.findall(r'(?:Version|v)[\s:]*([0-9\.]+)', txt, re.IGNORECASE)
    
    print(f"\n[Snapshot {ts}] Length: {len(txt)} - Candidates: {len(valid_candidates)}")
    for vc in valid_candidates:
        print(f"   -> {vc}")
        if vc not in found_links:
            found_links[vc] = []
        found_links[vc].append(ts)

print("\n--- SUMMARY OF ALL FOUND LINKS ---")
for l, tss in found_links.items():
    print(f"Link: {l} (Found in {len(tss)} snapshots: {tss})")
