#!/usr/bin/env python3
"""
Simple HTTP server to handle photo deletion requests
Run this server and then open photo_map_openlayers.html
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import urllib.parse


class PhotoMapHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/delete-photo':
            try:
                # Read the request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                photo_path = Path(data['path'])

                # Security check - ensure the path is within our image_source directory
                if not str(photo_path.resolve()).startswith(str(Path('image_source').resolve())):
                    self.send_error(403, "Access forbidden")
                    return

                # Delete the file if it exists
                if photo_path.exists():
                    photo_path.unlink()

                    # Also delete thumbnail if it exists
                    thumb_path = Path("image_source/thumbs") / photo_path.name
                    if thumb_path.exists():
                        thumb_path.unlink()

                    print(f"Deleted photo: {photo_path}")

                    # Send success response
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success'}).encode())
                else:
                    self.send_error(404, "File not found")

            except Exception as e:
                print(f"Error deleting photo: {e}")
                self.send_error(500, str(e))
        else:
            self.send_error(404, "Not found")

    def do_OPTIONS(self):
        # Handle preflight requests for CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PhotoMapHandler)
    print(f"Starting photo map server on http://localhost:{port}")
    print(f"Open http://localhost:{port}/photo_map_openlayers.html in your browser")
    print("Press Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()


if __name__ == '__main__':
    # Change to the script directory
    os.chdir(Path(__file__).parent)
    run_server()
