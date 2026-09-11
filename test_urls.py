import urllib.request
import re

urls = [
    'https://scribd.vdownloaders.com/doc/36341/Business-Plan-Template',
    'https://scribd.vdownloaders.com/doc/10301747/Bumble-Boogie-Sheet-Music',
    'https://scribd.vdownloaders.com/document/559864273/Sample-Document',
    'https://scribd.vdownloaders.com/vdoc/'
]

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            title = re.search(r'<title>(.*?)</title>', content, re.I)
            title_text = title.group(1) if title else 'No title'
            print(f"URL: {u}\n  Status: {resp.status}\n  Final: {resp.geturl()}\n  Title: {title_text}\n  Length: {len(content)}")
            # Find any interesting links or buttons
            links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', content)
            forms = re.findall(r'<form[^>]*action=[\'"]([^\'"]+)[\'"]', content)
            print("  Forms:", forms)
            interesting = [l for l in links if any(k in l.lower() for k in ['download', 'file', 'pdf', 'doc', 'api', 'get'])]
            print("  Interesting links:", interesting[:5])
    except Exception as e:
        print(f"URL: {u} Error: {e}")
