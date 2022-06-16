import requests
import json
from time import sleep


BASE = "http://127.0.0.1:5000/"

headers = {'Content-Type': 'application/json'}

# Add some users
payloads = [
    {'name': "Chris", 'role': 'client'},
    {'name': "Calvin", 'role': 'client'},
    {'name': "Alan", 'role': 'analyst'},
    {'name': "Adam", 'role': 'analyst'},
    ]

clients = []
analysts = []
for payload in payloads:
    response = requests.post(f"{BASE}user/", data=json.dumps(payload), headers=headers)
    print(response.json())
    if response.json()['role'] == 'client':
        clients.append(response.json()['user_id'])
    else:
        analysts.append(response.json()['user_id'])
    sleep(1)

# print(clients, analysts)

# Make some sessions
payloads = [
    {'client_id': '1', 'analyst_id': '3'},
    {'client_id': '1', 'analyst_id': '3'},
    ]

sessions = []
for payload in payloads:
    payload['client_id'] = clients.pop()
    payload['analyst_id'] = analysts.pop()
    response = requests.post(f"{BASE}session/", data=json.dumps(payload), headers=headers)
    print(response.json())
    sessions.append((response.json()['session_id'], response.json()['client_id']))
    sleep(1)

print(sessions)

# Make some messages
payloads = [
    {'session_id': '1', 'author_id': '2', 'text': 'Your messages is here.'},
    {'session_id': '2', 'author_id': '1', 'text': 'Your messages is here again.'},
    ]

messages = []
for payload in payloads:
    session, author = sessions.pop()
    payload['session_id'] = session
    payload['author_id'] = author
    response = requests.post(f"{BASE}message/", data=json.dumps(payload), headers=headers)
    print(response.json())
    messages.append(response.json()['message_id'])
    sleep(1)

print(messages)

# Retrieve said messages and delete them
for message in messages:
    response = requests.get(f"{BASE}/message/{message}")
    print(response.json())
    sleep(1)
    response = requests.delete(f"{BASE}/message/{message}")
    print(response)
    sleep(1)

    # try to get it after it is deleted
    response = requests.get(f"{BASE}/message/{message}")
    print(response.json())
