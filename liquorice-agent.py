from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import json
import time
from docker_stuff import DockerStuff


class _RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        self.instance = DockerStuff()
        BaseHTTPRequestHandler.__init__(self, *args)

    def _set_headers(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        docker_stuff = self.instance.docker_get_stuff()
        data = docker_stuff
        self._set_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_POST(self):
        data = []
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        message['date_ms'] = int(time.time()) * 1000
        data.append(message)
        method = getattr(self.instance, data[0]['task'])
        method(**data[0]['params'])
        self._set_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))

    def do_OPTIONS(self):
        # Send allow-origin header for preflight POST XHRs.
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.end_headers()


def run_server():
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
