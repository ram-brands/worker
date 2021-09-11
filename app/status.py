from enum import Enum


class Status(Enum):
    WARNING = 1
    OK = 2
    CLIENT_ERROR = 4
    SERVER_ERROR = 5
