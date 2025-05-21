'''
status

enum of all the posibles status
'''
from enum import Enum

class Status(int,Enum):

    OK = 1

    ERROR = 2

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

    pass