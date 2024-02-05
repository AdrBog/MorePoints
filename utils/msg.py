from enum import Enum

class Error(str, Enum):
    def __str__(self):
        return f'{self.value}'
        
    LOGIN_REQUIRED = "You have to login"
    FILE_EXISTS = "File already exists"
    POINT_NOT_FOUND = "Point not found"
    WRONG_PASSWORD = "Wrong password"


class Info(str, Enum):
    def __str__(self):
        return f'{self.value}'
        
    FILE_SAVED = "File saved"

    
