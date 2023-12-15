import socket

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
# server.listen(1)

# connection, address = server.accept()


while True:

    # data = connection.recv(1024).decode()
    data, address = server.recvfrom(1024)
    print(f'<<< {data.decode()}')

    if not data:
        break

    user_input = input('>>> ')
    server.sendto(user_input.encode(), address)

server.close()
