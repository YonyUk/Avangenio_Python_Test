from .status import Status
from .request import Request
from .response import Response
from tools import dserialize,serialize

def ToRequest(**data):
    result = Request()
    for key in data.keys():
        result.__setattr__(key,data[key])
        pass
    return result

def ToResponse(**data):
    result = Response()
    for key in data.keys():
        result.__setattr__(key,data[key])
        pass
    return result