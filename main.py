from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import json
import urllib.parse
import mimetypes
import pathlib
import socket
from datetime import datetime

HOST = '127.0.0.1'
SOCKET_PORT = 5000
HTTP_PORT = 3000


class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html')


    def do_POST(self):

        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {key: value for key, value in [
            el.split('=') for el in data_parse.split('&')]}
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
            client.connect((HOST, SOCKET_PORT))
            json_data_dict = json.dumps(data_dict).encode()
            client.sendto(json_data_dict, (HOST, SOCKET_PORT))
        
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


    def send_html_file(self, filename, status=200):

        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())


    def send_static(self):

        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def socket_server():

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, SOCKET_PORT))

        while True:
            data, address = server.recvfrom(1024)
            decode_data = json.loads(data)
            dict_time=str(datetime.now())

            with open('storage\data.json', 'r') as rf:
                file_json_dict = json.load(rf)
                file_json_dict[dict_time] = decode_data

            with open('storage\data.json', "w") as wf:
                json.dump(file_json_dict, wf, indent=2)


def run(server_class=HTTPServer, handler_class=HttpHandler):

    server_address = (HOST, HTTP_PORT)
    server = server_class(server_address, handler_class)
    server_http = Thread(target=server.serve_forever)
    server_socket = Thread(target=socket_server)

    try:
        server_http.start()
        server_socket.start()
    except KeyboardInterrupt:
        server_http.server_close()
        server_socket.server_close()


if __name__ == '__main__':
    
    run()
