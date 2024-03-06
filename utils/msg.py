"""
This module stores error or information messages.
"""
from enum import Enum

class Error(str, Enum):
    def __str__(self):
        return f'{self.value}'
        
    LOGIN_REQUIRED = "You have to login"
    FILE_EXISTS = "File already exists"
    POINT_NOT_FOUND = "Point not found\nMake sure:\n1. You entered the correct data\n2. server.py is running if you are trying to access to your local host"
    WRONG_PASSWORD = "Wrong password\nMake sure:\n1. You entered the correct data\n2. server.py is running if you are trying to access to your local host"


class Info(str, Enum):
    def __str__(self):
        return f'{self.value}'
        
    FILE_SAVED = "File saved"

    
