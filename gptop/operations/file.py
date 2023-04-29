import os
from enum import Enum

__all__ = ["FileOperation"]

class FileOperationType(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    DIRECTORY = "DIRECTORY"


class FileOperation():
    """
    An operation that works with files.
    """

    def __init__(self, input: any):
        self.type = input["type"]
        self.path = input["path"]
        self.content = input.get("content")

    @classmethod
    def llm_message(self):
        return [
            {"role": "system", "content": """
                Given a file operation with a predefined schema and a user prompt,
                provide the file path and operation type based on the prompt.
                """.replace("\n", " ")},
            {"role": "user", "content": "Output in JSON format and nothing more."}
        ]

    def execute(self):

        if self.type == FileOperationType.READ:
            file = open(self.path, "r")
            content = file.read()
            file.close()
            return content
        elif self.type == FileOperationType.DIRECTORY:
            return os.listdir(self.path)
        elif self.type == FileOperationType.WRITE:
            f = open(self.path, "a")
            f.write(self.content)
            f.close()
            return f"Wrote to file: {self.path}"


        return "Could not perform operation"
