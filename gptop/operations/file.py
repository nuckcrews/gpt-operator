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
        try:
            if self.type == FileOperationType.READ:
                with open(self.path, "r") as file:
                    content = file.read()
                return content
            elif self.type == FileOperationType.DIRECTORY:
                return os.listdir(self.path)
            elif self.type == FileOperationType.WRITE:
                with open(self.path, "a") as f:
                    f.write(self.content)
                return f"Wrote to file: {self.path}"
            else:
                return "Invalid operation type"
        except FileNotFoundError:
            return f"File not found: {self.path}"
        except PermissionError:
            return f"Permission denied: {self.path}"
        except Exception as e:
            return f"An error occurred: {str(e)}"