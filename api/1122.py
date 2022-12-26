import json

file = open('user.json')
data = json.load(file)
print(data)

print(data[0].items())