# import requests
# from http import client


# h1 = client.HTTPConnection('localhost', 3000)
# h1.request("GET", "/")

# res = h1.getresponse()
# print(res.status, res.reason)

# data = res.read()
# print(data)



# json_body = {'friends_id': '1'}
# # response = requests.post('http://127.0.0.1:8000/friends', json=json_body)
# response = requests.delete('http://127.0.0.1:8000/friends')
# print(response.status_code)
# print(response.text)


import requests

response = requests.get(
    'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11')
exchange_rate = response.json()
print(exchange_rate)
