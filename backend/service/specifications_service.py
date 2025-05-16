from .service import Service
from protocol import ServerOperation,Status

class SpecificationsService(Service):

    def __init__(self,**specifications):
        result = {
            'Status':Status.OK,
            'StatusMessage':'OK',
            'Body':{
                'specifications':specifications
            }
        }
        self._handlers[ServerOperation.SPECIFICATIONS] = lambda request: result 
        pass

    pass