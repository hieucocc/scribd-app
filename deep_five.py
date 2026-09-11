import json
import subprocess
import re

five = ["maddog-xx", "fslabs-controlcenter", "tritrisim-gfx", "gotfriends-aeroprakt-a32-vixxen", "land3-vraas"]

for slug in five:
    print(f"\n================ {slug} ================")
    # Query CDX
    cdx_url = f"https://web.archive.org/cdx/search/cdx?url=skybound.cx/msfs-2024/{slug}*&output=json&fl=timestamp,original,statuscode"
    cmd = ["curl.exe", "-s", "--max-time", "8", cdx_url]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        rows = json.loads(p.stdout.decode('utf-8'))[1:]
        print(f"Snapshots found: {len(rows)}")
        for ts, orig, st in rows:
            if st != '200': continue
            u = f"https://web.archive.org/web/{ts}id_/{orig}"
            cmd2 = ["curl.exe", "-s", "-L", "--max-time", "8", u]
            p2 = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            html = p2.stdout.decode('utf-8', errors='ignore')
            # Look for any URL with modsfire, buzzheavier, mega, mediafire, drive, r2, s3, cdn, download
            all_u = re.findall(r'https?://[^\s"\'<>\\]+', html)
            links = [x for x in all_u if any(h in x.lower() for h in ['modsfire', 'buzzheavier', 'mega.nz', 'mediafire', 'pastebin', 'drive.google', 'blob', 'cdn', 'download', 'releases'])]
            if links:
                print(f"  --> ts={ts} found links: {links[:3]}")
    except Exception as e:
        print(f"err: {e}")
