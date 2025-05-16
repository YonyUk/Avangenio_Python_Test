from enum import Enum

class ServerOperation(str,Enum):

    PONDERATION = 'STRING_PONDERATION'

    START_FILE_PROCESS = 'START_FILE_PROCESS'
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self)

    pass