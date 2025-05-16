from enum import Enum

class ServerOperation(str,Enum):

    PONDERATION = 'STRING_PONDERATION'

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self)

    pass