import subprocess
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

url = 'https://web.archive.org/web/20260806012023mp_/https://skybound.cx/msfs-2024/pmdg-738'
p = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '15', url], stdout=subprocess.PIPE)
c = p.stdout.decode('utf-8', errors='ignore')

pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', c, re.DOTALL)
combined = ''
for item in pushes:
    try: combined += json.loads(f'"{item}"') + '\n'
    except: combined += item + '\n'

# Check Payload CMS structure (Skybound uses Payload CMS with Lexical Editor or Slate Editor!)
# Let's search for "description" or "content"
m_desc = re.search(r'"description":\s*(\{"root":.*?\})', combined)
if m_desc:
    print("Found Payload CMS Lexical root for description!")
    try:
        desc_obj = json.loads(m_desc.group(1))
        def extract_lexical_text(node):
            res = []
            if isinstance(node, dict):
                if node.get('type') == 'text':
                    res.append(node.get('text', ''))
                for v in node.values():
                    res.extend(extract_lexical_text(v))
            elif isinstance(node, list):
                for item in node:
                    res.extend(extract_lexical_text(item))
            return res
        
        all_text = extract_lexical_text(desc_obj)
        print("Extracted Lexical paragraphs:")
        print("\n".join(all_text[:10]))
    except Exception as e:
        print("Error parsing Lexical:", e)
else:
    print("No Lexical root found, checking regex text matches:")
    texts = re.findall(r'"text":\s*"([^"\\]*(?:\\.[^"\\]*)*)"', combined)
    for idx, t in enumerate(texts[:15], 1):
        if len(t) > 20:
            print(f"  {idx}. {t}")

# Check image URLs
img_match = re.search(r'"thumbnail":\s*\{.*?"url":\s*"([^"]+)"', combined)
if img_match:
    print("Thumbnail relative URL:", img_match.group(1))

# Check full-size cover image
cover_match = re.search(r'"image":\s*\{.*?"url":\s*"([^"]+)"', combined)
if cover_match:
    print("Cover image relative URL:", cover_match.group(1))
