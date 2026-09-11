import sys
import urllib.request
import re
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def extract_skybound(url):
    """
    Trích xuất tự động thông tin & link download từ snapshot Wayback Machine của skybound.cx
    """
    # Chuẩn hoá URL sang chế độ mp_ (raw snapshot không bị archive.org tiêm banner/toolbar)
    if "web.archive.org/web/" in url and "mp_/" not in url:
        url = re.sub(r'(/web/\d{14})(/)', r'\1mp_\2', url)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as resp:
        html = resp.read().decode('utf-8', errors='ignore')

    # 1. Tiêu đề Addon
    title_m = re.search(r'<title>(.*?)</title>', html, re.I)
    title = title_m.group(1).replace(' | Skybound', '').strip() if title_m else 'Unknown'

    # 2. Giải mã các đoạn chunk React Server Components (Next.js App Router)
    pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', html, re.DOTALL)
    combined = ''
    for p in pushes:
        try:
            combined += json.loads(f'"{p}"') + '\n'
        except Exception:
            combined += p + '\n'

    # 3. Trích xuất danh sách 'versions'
    versions = []
    versions_m = re.search(r'"versions":\s*(\[\{.*?\}\])', combined)
    if versions_m:
        try:
            versions = json.loads(versions_m.group(1))
        except Exception:
            pass

    # 4. Trích xuất mật khẩu giải nén nếu có
    pwd_m = re.search(r'Archive password is:\s*.*?href=["\']([^"\']+)["\']', combined, re.I)
    pwd = pwd_m.group(1) if pwd_m else 'https://skybound.cx'

    # 5. Lọc các link tải bên thứ ba xuất hiện thêm trong trang (Modsfire, Buzzheavier, Mega, v.v.)
    all_urls = re.findall(r'https?://[^\s"\'<>\\]+', combined)
    extra_links = []
    seen = {v.get('url') for v in versions if 'url' in v}
    for u in all_urls:
        u = u.replace('\\"', '').replace('\\', '').rstrip('/.,;')
        if any(host in u.lower() for host in ['modsfire.com', 'buzzheavier.com', 'mega.nz', 'mediafire.com', 'drive.google.com', 'pastebin.com', 'flightsim.to']):
            if u not in seen:
                extra_links.append(u)
                seen.add(u)

    return {
        'title': title,
        'password': pwd,
        'versions': versions,
        'extra_links': extra_links
    }

def print_result(data):
    print("\n" + "=" * 60)
    print(f"📦 Tên addon : {data['title']}")
    print(f"🔑 Mật khẩu  : {data['password']}")
    print("-" * 60)
    print("📥 Danh sách Link Download:")
    if data['versions']:
        for v in data['versions']:
            ver = v.get('versionNumber', 'N/A')
            t = v.get('downloadType', 'link')
            link = v.get('url', '')
            print(f"  • [{ver}] ({t}): {link}")
    else:
        print("  (Không tìm thấy link trong mảng versions)")

    if data['extra_links']:
        print("\n🔗 Link phụ / Tài nguyên đính kèm:")
        for l in data['extra_links']:
            print(f"  • {l}")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        target_url = sys.argv[1].strip()
        print(f"Đang phân tích: {target_url} ...")
        res = extract_skybound(target_url)
        print_result(res)
    else:
        while True:
            try:
                inp = input("Nhập link Wayback Skybound (hoặc gõ 'exit' để thoát): ").strip()
                if not inp or inp.lower() in ['exit', 'quit', 'q']:
                    break
                print(f"Đang xử lý ...")
                res = extract_skybound(inp)
                print_result(res)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Lỗi: {e}")
