from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from time import sleep
from http import client
import json
import urllib.parse
import mimetypes
import pathlib
import socket

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
        print(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        data_dict = {key: value for key, value in [
            el.split('=') for el in data_parse.split('&')]}
        print(data_dict)
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

        # json.dump(response, wfile)


def echo_server(host, port):

    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                print(f'From client: {data}')
                if not data:
                    break
                conn.send(data.upper())


def simple_client(host, port):

    with socket.socket() as s:
        while True:
            try:
                s.connect((host, port))
                s.sendall(b'Hello, world')
                data = s.recv(1024)
                print(f'From server: {data}')
                break
            except ConnectionRefusedError:
                sleep(0.5)

# sleep(.5)

# h1 = client.HTTPConnection('localhost', 3000)
# h1.request("GET", "/")

# res = h1.getresponse()
# print(res.status, res.reason)

# data = res.read()
# print(data)

# # httpd.shutdown()


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = (HOST, HTTP_PORT)

    # server = Thread(target=httpd.serve_forever)
    # server.start()


# httpd = HTTPServer(('localhost', 3000), FriendsRequestHandler)
# server = Thread(target=httpd.serve_forever)
# server.start()

    server = server_class(server_address, handler_class)

    server_http = Thread(target=server.serve_forever)
    server_socket = Thread(target=echo_server, args=(HOST, SOCKET_PORT))
    client_socket = Thread(target=simple_client, args=(HOST, SOCKET_PORT))


    try:
        server_http.start()
        server_socket.start()
        client_socket.start()
        
    except KeyboardInterrupt:
        server_http.server_close()
        server_socket.server_close()


if __name__ == '__main__':
    # server = Thread(target=echo_server, args=(HOST, PORT))
    # client = Thread(target=simple_client, args=(HOST, PORT))

    # server.start()
    # client.start()
    # server.join()
    # client.join()
    # print('Done!')
    run()
