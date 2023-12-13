from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class FriendsRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'Application/json')
        self.wfile.write('hello epta')

        json.dump(response, wfile)


HTTPServer(('localhost',))