from enum import Enum

class ServerOperation(str,Enum):

    PONDERATION = 'STRING_PONDERATION'

    START_FILE_PONDERATION = 'START_FILE_PONDERATION'

    END_FILE_PONDERATION = 'END_FILE_PONDERATION'

    SEND_FILE = 'SEND_FILE'
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self)

    pass