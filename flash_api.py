import os
import json
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

PORT = 5000
DATA_FILE = 'psx_dashboard_data.json'

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class FlashAPIRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        path = self.path.split('?')[0].rstrip('/')
        
        if path == '' or path == '/dashboard':
            self.serve_file('index.html', 'text/html; charset=utf-8')
            return

        if path == '/psx_dashboard_data.json':
            self.serve_file(DATA_FILE, 'application/json')
            return

        if path.startswith('/api/'):
            self.handle_api(path)
            return

        super().do_GET()

    def handle_api(self, path):
        if not os.path.exists(DATA_FILE):
            self.send_json({'error': 'Data not ready'}, status=503)
            return

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if path == '/api/summary':
            self.send_json(data.get('metadata', {}))
        elif path == '/api/stocks':
            self.send_json(data.get('symbols', []))
        elif path == '/api/sectors':
            self.send_json(data.get('sectors', []))
        elif path == '/api/rebased':
            self.send_json(data.get('rebased', {}))
        elif path == '/api/correlations':
            self.send_json(data.get('correlations', {}))
        elif path.startswith('/api/stock/'):
            symbol = path.split('/')[-1].upper()
            series = data.get('stock_series', {}).get(symbol)
            if series:
                self.send_json({'symbol': symbol, 'series': series})
            else:
                self.send_json({'error': f'Symbol {symbol} not found in KSE-100 universe'}, status=404)
        else:
            self.send_json({'error': 'Unknown endpoint', 'endpoints': ['/api/summary', '/api/stocks', '/api/stock/<symbol>', '/api/sectors', '/api/rebased', '/api/correlations']}, status=404)

    def serve_file(self, filepath, content_type):
        if not os.path.exists(filepath):
            self.send_error(404, f"File {filepath} not found")
            return
        with open(filepath, 'rb') as f:
            content = f.read()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, payload, status=200):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def run_server():
    server_address = ('', PORT)
    httpd = ThreadedHTTPServer(server_address, FlashAPIRequestHandler)
    print(f"================================================================")
    print(f" PSX KSE-100 Institutional Terminal running at:")
    print(f" -> http://localhost:{PORT}/")
    print(f" -> Live Endpoints active under http://localhost:{PORT}/api/")
    print(f"================================================================")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
