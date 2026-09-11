import http.server
import socketserver
import json
import urllib.request
import re
import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PORT = 5050
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

SLUGS_MSFS_2024 = [
  {"slug": "pmdg-738", "title": "PMDG 737-800", "cat": "PMDG"},
  {"slug": "pmdg-77w", "title": "PMDG 777-300ER", "cat": "PMDG"},
  {"slug": "pmdg-737", "title": "PMDG 737-700", "cat": "PMDG"},
  {"slug": "pmdg-736", "title": "PMDG 737-600", "cat": "PMDG"},
  {"slug": "pmdg-739", "title": "PMDG 737-900", "cat": "PMDG"},
  {"slug": "pmdg-77er", "title": "PMDG 777-200ER", "cat": "PMDG"},
  {"slug": "pmdg-77f", "title": "PMDG 777F", "cat": "PMDG"},
  {"slug": "pmdg-77l", "title": "PMDG 777-200LR", "cat": "PMDG"},
  {"slug": "pmdg-dc6", "title": "PMDG DC-6", "cat": "PMDG"},
  {"slug": "fenix-a32x", "title": "Fenix Simulations A319, A320, A321 Bundle", "cat": "Airbus"},
  {"slug": "bksq-caravan-amph-cargo", "title": "Black Square Caravan Amphibian and Cargo", "cat": "Aircraft"},
  {"slug": "ifly-737max8", "title": "iFly 737 MAX 8", "cat": "Airliner"},

  {"slug": "flysimware-learjet-35a", "title": "FlySimWare Learjet 35A", "cat": "Business Jet"},
  {"slug": "bksq-tbm-850", "title": "Black Square TBM 850", "cat": "Turboprop"},
  {"slug": "bksq-turbine-duke", "title": "Black Square Turbine Duke", "cat": "Turboprop"},
  {"slug": "bksq-piston-duke", "title": "Black Square Piston Duke", "cat": "GA"},
  {"slug": "bksq-baron", "title": "Black Square Baron 58", "cat": "GA"},
  {"slug": "bksq-bonanza", "title": "Black Square Bonanza A36", "cat": "GA"},
  {"slug": "bksq-starship", "title": "Black Square Starship", "cat": "Turboprop"},
  {"slug": "bksq-caravan-passenger", "title": "Black Square Analog Caravan", "cat": "Turboprop"},
  {"slug": "bksq-velocity-xl", "title": "Black Square Velocity XL", "cat": "GA"},
  {"slug": "inibuilds-a300-600r-premium", "title": "iniBuilds A300-600R Premium", "cat": "Airbus"},
  {"slug": "inibuilds-a340", "title": "iniBuilds A340", "cat": "Airbus"},
  {"slug": "inibuilds-a350", "title": "iniBuilds A350", "cat": "Airbus"},
  {"slug": "inibuilds-tristar", "title": "iniBuilds L-1011 TriStar", "cat": "Airliner"},
  {"slug": "inibuilds-f406-caravan", "title": "iniBuilds F406 Caravan II", "cat": "Turboprop"},
  {"slug": "inibuilds-eglc", "title": "iniBuilds London City EGLC", "cat": "Scenery"},
  {"slug": "aerosoft-crj-v2", "title": "Aerosoft CRJ 550/700/900/1000 v2", "cat": "Airliner"},
  {"slug": "aerosoft-a346", "title": "Aerosoft A340-600", "cat": "Airbus"},
  {"slug": "a2a-comanche-250", "title": "A2A Simulations Comanche 250", "cat": "GA"},
  {"slug": "a2a-aerostar-600", "title": "A2A Simulations Aerostar 600", "cat": "GA"},
  {"slug": "jf-146-professional", "title": "Just Flight 146 Professional", "cat": "Airliner"},
  {"slug": "jf-rj-professional", "title": "Just Flight RJ Professional", "cat": "Airliner"},
  {"slug": "jf-f28-professional", "title": "Just Flight F28 Professional", "cat": "Airliner"},
  {"slug": "jf-f70-professional", "title": "Just Flight F70/F100", "cat": "Airliner"},
  {"slug": "jf-f100-professional", "title": "Just Flight F100 Professional", "cat": "Airliner"},
  {"slug": "jf-pa28-arrow-bundle", "title": "Just Flight PA-28 Arrow Bundle", "cat": "GA"},
  {"slug": "jf-pa28-warrior-ii", "title": "Just Flight PA-28-161 Warrior II", "cat": "GA"},
  {"slug": "jf-hawk-t1a-trainer", "title": "Just Flight Hawk T1/A", "cat": "Military"},
  {"slug": "jf-vulcan", "title": "Just Flight Avro Vulcan", "cat": "Military"},
  {"slug": "fss-727-series", "title": "FlightSim Studio 727 Series", "cat": "Airliner"},
  {"slug": "fss-ejets-17x", "title": "FlightSim Studio E-Jets 170/175", "cat": "Airliner"},
  {"slug": "fss-ejets-19x", "title": "FlightSim Studio E-Jets 190/195", "cat": "Airliner"},
  {"slug": "fss-ejets-19x-freighter", "title": "FlightSim Studio E-Jets Freighter", "cat": "Airliner"},
  {"slug": "fsdt-gsx-pro", "title": "FSDreamTeam GSX Pro", "cat": "Utility"},
  {"slug": "maddog-xx", "title": "Fly the Maddog X MD-82", "cat": "Airliner"},
  {"slug": "tfdi-md11", "title": "TFDi Design MD-11", "cat": "Airliner"},
  {"slug": "sws-kodiak-100", "title": "SimWorks Studios Kodiak 100", "cat": "Turboprop"},
  {"slug": "blackbird-c130", "title": "Blackbird C-130 Hercules", "cat": "Military"},
  {"slug": "blackbird-sr71", "title": "Blackbird SR-71 Blackbird", "cat": "Military"},
  {"slug": "cows-da42", "title": "COWS DA42 Series", "cat": "GA"},
  {"slug": "cows-da40", "title": "COWS DA40 XLS", "cat": "GA"},
  {"slug": "azurpoly-jaguar", "title": "AzurPoly SEPECAT Jaguar", "cat": "Military"},
  {"slug": "virga-studio-dassault-alpha-jet", "title": "Virga Studio Dassault Alpha Jet", "cat": "Military"},
  {"slug": "ffx-hjet", "title": "FlightFX HondaJet HJet", "cat": "Business Jet"},
  {"slug": "flysimware-lancair-legacy", "title": "FlySimWare Lancair Legacy", "cat": "GA"},
  {"slug": "skyward-citation-c680", "title": "Skyward Cessna Citation Sovereign", "cat": "Business Jet"},
  {"slug": "skyward-da50", "title": "Skyward Diamond DA50 RG", "cat": "GA"},
  {"slug": "livtoair-cessna-citation-cj3plus", "title": "LivToAir Citation CJ3+", "cat": "Business Jet"},
  {"slug": "bluesky-grumman-aa5", "title": "Blue Sky Grumman AA-5", "cat": "GA"},
  {"slug": "gotfriends-aeroprakt-a32-vixxen", "title": "Got Friends Aeroprakt A-32 Vixxen", "cat": "Ultralight"},
  {"slug": "gotfriends-project-crosskart", "title": "Got Friends Crosskart", "cat": "Fun"},
  {"slug": "microprose-b-17g-flying-fortress", "title": "MicroProse B-17G Flying Fortress", "cat": "Warbird"},
  {"slug": "miltech-ch47d", "title": "Miltech Simulations CH-47D Chinook", "cat": "Helicopter"},
  {"slug": "miltech-mv22osprey", "title": "Miltech Simulations MV-22B Osprey", "cat": "Military"},
  {"slug": "miltech-stratoware-bo105", "title": "Miltech BO-105 Helicopter", "cat": "Helicopter"},
  {"slug": "miltechsim-mh60", "title": "Miltech Simulations MH-60 Seahawk", "cat": "Helicopter"},
  {"slug": "miltechsim-m2k-c", "title": "Miltech Simulations Mirage 2000C", "cat": "Military"},
  {"slug": "miltech-missionhub", "title": "Miltech Simulations Mission Hub", "cat": "Utility"},
  {"slug": "p42-chaseplane", "title": "Parallel 42 ChasePlane", "cat": "Utility"},
  {"slug": "p42-flow-pro", "title": "Parallel 42 Flow Pro", "cat": "Utility"},
  {"slug": "navigraph-airac", "title": "Navigraph AIRAC Cycle", "cat": "Navigation"},
  {"slug": "rexatmoscore", "title": "REX AtmosCore Global Weather", "cat": "Weather"},
  {"slug": "bijan-earthfx", "title": "Bijan Studio EarthFX", "cat": "Scenery"},
  {"slug": "bijan-seasons", "title": "Bijan Studio 4 Season Pack", "cat": "Scenery"},
  {"slug": "orbx-katl", "title": "Orbx Atlanta KATL Airport", "cat": "Scenery"},
  {"slug": "fsxcenery-lcen", "title": "FSXcenery LCEN Airport", "cat": "Scenery"},
  {"slug": "ss-vessels-global-shipping", "title": "Seafront Simulations Global Shipping", "cat": "Scenery"},
  {"slug": "simfocus-autogen-helipads", "title": "SimFocus Global Helipads", "cat": "Scenery"},
  {"slug": "css-737-classics", "title": "Captain Sim 737 Classics", "cat": "Airliner"},
  {"slug": "baw-pmdg-737ng", "title": "BAW PMDG 737NG Soundpack", "cat": "Sound"},
  {"slug": "baw-pmdg-777", "title": "BAW PMDG 777 Soundpack", "cat": "Sound"},
  {"slug": "baw-aerosoft-crj", "title": "BAW Aerosoft CRJ Soundpack", "cat": "Sound"},
  {"slug": "fslabs-controlcenter", "title": "FSLabs A321ceo & A321neo", "cat": "Airbus"},
  {"slug": "fsltl-downgraded-textures", "title": "FSLTL Downgraded Textures", "cat": "Utility"},
  {"slug": "land3-vraas", "title": "Land3 Virtual RAAS", "cat": "Utility"},
  {"slug": "nextgen-simulations-emb100", "title": "NextGen Simulations EMB-110", "cat": "Turboprop"},
  {"slug": "tritrisim-gfx", "title": "TriTriSim Graphics Enhancer", "cat": "Utility"}
]

# Cache to store extracted results in memory
CACHE_FILE = os.path.join(DIRECTORY, "extracted_cache.json")
EXTRACTED_CACHE = {}

def load_cache():
    global EXTRACTED_CACHE
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                EXTRACTED_CACHE = json.load(f)
        except Exception:
            EXTRACTED_CACHE = {}

def save_cache():
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(EXTRACTED_CACHE, f, ensure_ascii=False, indent=2)
    except Exception as e:
        sys.stderr.write(f"Cache save error: {e}\n")

load_cache()

def fetch_addon_data(slug_or_url):
    if slug_or_url.startswith("http"):
        url = slug_or_url
        # extract slug
        m = re.search(r'/msfs-2024/([a-zA-Z0-9_-]+)', url)
        slug = m.group(1) if m else url
    else:
        slug = slug_or_url
        url = f"https://web.archive.org/web/20260806012023/https://skybound.cx/msfs-2024/{slug}"

    if slug in EXTRACTED_CACHE:
        return EXTRACTED_CACHE[slug]

    cmd = ["curl.exe", "-s", "-L", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", url]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    content = p.stdout.decode('utf-8', errors='ignore')

    title_m = re.search(r'<title>(.*?)</title>', content, re.I)
    title = title_m.group(1).replace(' | Skybound', '').strip() if title_m else slug.replace('-', ' ').title()

    pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', content, re.DOTALL)
    combined = ''
    for item in pushes:
        try:
            combined += json.loads(f'"{item}"') + '\n'
        except Exception:
            combined += item + '\n'

    versions = []
    versions_m = re.search(r'"versions":\s*(\[\{.*?\}\])', combined)
    if versions_m:
        try:
            versions = json.loads(versions_m.group(1))
        except Exception:
            pass

    pwd_m = re.search(r'Archive password is:\s*.*?href=["\']([^"\']+)["\']', combined, re.I)
    pwd = pwd_m.group(1) if pwd_m else 'https://skybound.cx'

    all_urls = re.findall(r'https?://[^\s"\'<>\\]+', combined)
    extra_links = []
    seen = {v.get('url') for v in versions if 'url' in v}
    for u in all_urls:
        clean_u = u.replace('\\"', '').replace('\\', '').rstrip('/.,;')
        if any(h in clean_u.lower() for h in ['modsfire.com', 'buzzheavier.com', 'mega.nz', 'mediafire.com', 'drive.google.com', 'pastebin.com', 'flightsim.to']):
            if clean_u not in seen:
                extra_links.append(clean_u)
                seen.add(clean_u)

    result = {
        'url': url,
        'slug': slug,
        'title': title,
        'password': pwd,
        'versions': versions,
        'extra_links': extra_links
    }
    EXTRACTED_CACHE[slug] = result
    save_cache()
    return result

class SkyboundHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/api/catalog/msfs-2024':
            load_cache()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            data = {
                'total': len(SLUGS_MSFS_2024),
                'addons': SLUGS_MSFS_2024,
                'cachedCount': len(EXTRACTED_CACHE)
            }
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/api/catalog/cached-all':
            load_cache()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({'results': list(EXTRACTED_CACHE.values())}, ensure_ascii=False).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/extract':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                targets = []
                if 'slug' in data:
                    targets = [data['slug']]
                elif 'urls' in data and isinstance(data['urls'], list):
                    targets = data['urls']
                elif 'url' in data:
                    u = data['url'].strip()
                    # Check if it's the main catalog URL
                    if 'skybound.cx/msfs-2024' in u and not re.search(r'/msfs-2024/[a-zA-Z0-9_-]+', u.split('?')[0].rstrip('/')):
                        targets = [item['slug'] for item in SLUGS_MSFS_2024]
                    else:
                        targets = [u]

                results = []
                max_w = 4 if len(targets) > 2 else 1
                with ThreadPoolExecutor(max_workers=max_w) as executor:
                    futures = [executor.submit(self._process_single, t) for t in targets]
                    for f in futures:
                        results.append(f.result())

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'results': results}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint Not Found")

    def _process_single(self, target):
        try:
            res = fetch_addon_data(target)
            return {'success': True, 'data': res}
        except Exception as e:
            return {'success': False, 'url': target, 'error': str(e)}

    def log_message(self, format, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {args[0]} - {args[1]}\n")
        sys.stdout.flush()

def start_server():
    os.makedirs(DIRECTORY, exist_ok=True)
    server_address = ('127.0.0.1', PORT)
    httpd = socketserver.TCPServer(server_address, SkyboundHandler)
    print(f"🚀 Skybound Web Extractor đang chạy tại: http://127.0.0.1:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng máy chủ.")

if __name__ == '__main__':
    start_server()
