import requests
import json


BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE + "helloworld/Jojo")
# print(response.json())

# headers = {'Content-Type': 'application/json'}
# payload = {'likes': 333, 'name': 'Tester3', 'views': 3333333}
# response = requests.put(f"{BASE}video/3", data=json.dumps(payload), headers=headers)
#
# print(response.json())
# input()

# payload['name'] = "TwoTester"
# payload['views'] = 555
# response = requests.put(BASE + "video/2", data=json.dumps(payload), headers=headers)
# print(response.json())
# input()

# response = requests.get(BASE + "video/2")
# print(response.json())
#

# response = requests.delete(f"{BASE}video/3")
# print(response)

for i in range(6):
    response = requests.get(f"{BASE}video/{str(i)}")
    print(i, response.json())

response = requests.delete(f"{BASE}video/3")
# print(response)
print(response, response.json())

headers = {'Content-Type': 'application/json'}
payload = {'likes': 111}
response = requests.patch(f"{BASE}video/1", data=json.dumps(payload), headers=headers)
print(response.json())
