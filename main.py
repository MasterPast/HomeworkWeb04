import json
import logging
import os
import socket
from datetime import datetime
from flask import Flask, redirect, render_template, request
from threading import Thread

HOST = 'localhost'
SOCKET_PORT = 5000

data_dict = {}

app = Flask(__name__)

@app.errorhandler(404)
def my_error_page(error):
    return render_template('error.html')

@app.route('/')
def index_page_get():
    return render_template('index.html')

@app.route('/home')
def home_page_get():
    return render_template('index.html')

@app.route('/message', methods=['GET'])
def message_page_get():
    return render_template('message.html')

@app.route('/message', methods=['POST'])
def message_page_post():
    username = request.form['username']
    message = request.form['message']
    data_dict['username'] = username
    data_dict['message'] = message
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.connect((HOST, SOCKET_PORT))
        json_data_dict = json.dumps(data_dict).encode()
        client.sendto(json_data_dict, (HOST, SOCKET_PORT))
    
    logging.debug('Data_dict was send')
    return redirect('/')


def socket_server():

    logging.debug('socket_server starting...')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, SOCKET_PORT))

        while True:

            data, address = server.recvfrom(1024)
            decode_data = json.loads(data)
            dict_time=str(datetime.now())
            logging.debug('Start receiving')

            if not os.path.isdir("storage"):
                logging.debug('Directory STORAGE not found. Creating STORAGE...')
                os.mkdir('storage')
            if not os.path.isfile("storage/data.json"):
                null_dict = {}
                logging.debug('File not found. Creating file...')
    
                with open('storage/data.json', "w") as wf:
                    json.dump(null_dict, wf, indent=2)
            
            with open('storage/data.json', 'r') as rf:
                file_json_dict = json.load(rf)
                file_json_dict[dict_time] = decode_data
            
            logging.debug('Start reading from file')
            
            with open('storage/data.json', "w") as wf:
                json.dump(file_json_dict, wf, indent=2)
            
            logging.debug('Start saving to file')
    
def run():

    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    logging.debug('Starting app')
    logging.debug('Creating threads')

    try:
        logging.debug('Starting servers...')
        server_socket = Thread(target=socket_server)
        server_socket.start()
        server_http = Thread(target=app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000))))
        server_http.start()
    
        logging.debug('Servers sucessfully started.')
    except KeyboardInterrupt:
        server_http.server_close()
        server_socket.server_close()


if __name__ == "__main__":
    run()