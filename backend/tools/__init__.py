import json

def serialize(**data):
    return bytes(json.dumps(data),'utf-8')

def dserialize(data:bytes):
    return json.loads(data.decode())