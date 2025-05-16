from enum import Enum

class ServerOperation(int,Enum):

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self)

    pass