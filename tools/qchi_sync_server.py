import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# The file we want to auto-save to
HTML_FILE = "QCHI_PROJECT_FLOW.html"

class SaveHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle CORS for local requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            new_inner_html = data['content']

            if not os.path.exists(HTML_FILE):
                self.send_error(404, "HTML file not found")
                return

            with open(HTML_FILE, 'r', encoding='utf-8') as f:
                html = f.read()

            # Identify the markers
            start_marker = "<!-- USER_START -->"
            end_marker = "<!-- USER_END -->"
            
            start_idx = html.find(start_marker)
            if start_idx == -1:
                self.send_error(500, "Start marker not found")
                return
            start_idx += len(start_marker)
            
            end_idx = html.find(end_marker)
            if end_idx == -1:
                self.send_error(500, "End marker not found")
                return

            # Surgically update the content between markers
            updated_html = html[:start_idx] + "
            " + new_inner_html.strip() + "
            " + html[end_idx:]

            with open(HTML_FILE, 'w', encoding='utf-8') as f:
                f.write(updated_html)

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
            print(f"[QCHI Sync] Auto-saved changes to {HTML_FILE}")

        except Exception as e:
            print(f"[QCHI Sync] Error: {e}")
            self.send_error(500, str(e))

def run(port=8888):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, SaveHandler)
    print(f"QCHI Auto-save Sync Server started on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
