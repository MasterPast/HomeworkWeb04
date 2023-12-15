import json

data = {'username': 'l;qkfmjiowk', 'message': 'ekfnmowj'}

# with open('storage/data.json', "w") as fw:
#     json.dump(data, fw)

# with open('storage/data.json', "r") as fr:
#     data = json.load(fr)
#     print(data)
q={}
a = {'1': 'one', '2': 'two'}
b = {'1': 'uno', '2': 'dos'}
q['eng'] = a
q['span'] = b
print(q)
