import json
import sys
import os
import socket

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from protocol import Request,Response

def sendto(host:str,port:int,request:Request):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    client.connect((host,port))
    client.sendall(serialize(**request.to_dict()))
    response = client.recv(134217728)
    while True:
        try:
            response = Response(**dserialize(response))
            break
        except Exception as ex:
            response += client.recv(134217728)
            pass
        pass
    return response

def serialize(**data):
    return bytes(json.dumps(data),'utf-8')

def dserialize(data:bytes):
    return json.loads(data.decode())