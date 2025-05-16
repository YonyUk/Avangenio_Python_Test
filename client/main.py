import socket
import json

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
client.connect(('localhost',8080))

request = json.dumps({
    'Operation':'SERVER_SPECIFICATIONS'
})

client.sendall(bytes(request,'utf-8'))
response = json.loads(client.recv(1024).decode())
print(response)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
client.connect(('localhost',8080))

request = json.dumps({
    'url':'http://localhost:8080',
    'protocol':'tcp',
    'Operation': 'STRING_PONDERATION',
    'Body':{
        'text':'uiwefw ewow ewiugf 230743b dwaAueig\naiwug weydv eyuv 9 dav'
    }
})

client.sendall(bytes(request,'utf-8'))
response = json.loads(client.recv(1024).decode())
print(response)