from enum import StrEnum

class Priority(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskStatus(StrEnum):
    ToDo = "ToDo"
    InProgress = "InProgress"
    Done = "Done"