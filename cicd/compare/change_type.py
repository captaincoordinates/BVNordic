from enum import Enum


class ChangeType(int, Enum):
    UNCHANGED = 0
    CHANGED = 1
    REMOVED = 2
    ADDED = 3
