import subprocess
import re
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

timestamps = ['20260731203823', '20260827114334', '20260719040927', '20260725231522', '20260511202522']
sample_slugs = ['fss-727-series', 'pmdg-737', 'tfdi-md11', 'maddog-xx', 'ifly-737max8', 'inibuilds-a300-600r-premium']

for slug in sample_slugs:
    print(f"\nTesting {slug}:")
    found = False
    for ts in timestamps:
        u = f"https://web.archive.org/web/{ts}mp_/https://skybound.cx/msfs-2024/{slug}"
        cmd = ["curl.exe", "-s", "-L", "--max-time", "6", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", u]
        res = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8', errors='ignore')
        m = re.search(r'"versions":\s*(\[\{.*?\}\])', res)
        if m:
            print(f"  ✅ Found on {ts}: {m.group(1)[:120]}")
            found = True
            break
    if not found:
        print(f"  ❌ No versions on any of the 5 snapshot dates")
