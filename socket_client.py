import socket
import json
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000
a = {'1':'asd', '2':'cvb'}

message = {'username': 'Mast', 'message': 'dsfdsvds'}

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect((HOST,PORT))
print(client)
print(message)
print(f'type message>>>{type(message)}')
# while True:
json_message = json.dumps(message).encode()
client.sendto(json_message,(HOST,PORT))
print(f'type json msg>>>{type(json_message)}')



dict_time=str(datetime.now())
decode_data = json.loads(json_message)
decode_data = {'1': 'one', '2': 'two'}
print(f'type of decode data>>>{type(decode_data)}')
print(f'conv mess>>> {decode_data}')

with open('data.json', 'r') as rf:
    file_json_dict = json.load(rf)
    print(f'we load>>>{file_json_dict}')
    file_json_dict[dict_time] = decode_data

    print(f'we have>>> {file_json_dict}')

with open('data.json', "w") as fw:
    json.dump(file_json_dict, fw, indent=2)

# with open('data.json', 'r') as rf:
#     finish_msg = json.load(rf)

# print(f'>>>Itogo: >>> {type(finish_msg)}')
client.close()

# b = {'3':'qwe', '4':'ffdgd'}
# a.update(b)

# print(a)