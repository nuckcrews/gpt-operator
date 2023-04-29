import os
import json
from enum import Enum
from .operations import CommandOperation, FileOperation, HTTPOperation, DownloadOperation
from .utils import llm_response, llm_json

__all__ = ["OperationType", "Operation"]


class OperationType(str, Enum):
    HTTP = "HTTP"
    DOWNLOAD = "DOWNLOAD"
    COMMAND = "COMMAND"
    FILE = "FILE"


class Operation():

    def __init__(self, id: str, type: OperationType, name: str, description: str, metadata: any, schema: any):
        """
        Holds the properties on an operation prepared for execution
        - id: The identifier of the operation
        - type: The type of operation
        - name: The name of the operation
        - description: The description of the operation
        - metadata: Metadata defined in the manifest file
        - schema: Schema to be hydrated by the LLM
        """

        self.id = id
        self.type = type
        self.name = name
        self.description = description
        self.metadata = metadata
        self.schema = schema
        self.auth_token = os.getenv(id + "_token")

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_obj(self, obj):
        """
        Returns an instance of an operation from a dict object
        """

        return Operation(obj['id'], obj['type'], obj['name'], obj['description'], obj['metadata'], obj['schema'])

    def vector_metadata(self):
        d = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "metadata": self.metadata,
            "schema": self.schema
        }
        return {k: v for k, v in d.items() if v is not None}

    def embedding_obj(self):
        return "; ".join([
            f"Name: {self.name}",
            f"Description: {self.description}",
            f"Type: {self.type}",
            f"Metadata: {self.metadata}",
            f"Schema: {self.schema}"
        ])

    def llm_message(self):
        if self.type == OperationType.COMMAND:
            return CommandOperation.llm_message()
        elif self.type == OperationType.DOWNLOAD:
            return DownloadOperation.llm_message()
        elif self.type == OperationType.FILE:
            return FileOperation.llm_message()
        elif self.type == OperationType.HTTP:
            return HTTPOperation.llm_message()

    def llm_modifier(self, response):
        if self.type == OperationType.COMMAND:
            return llm_response(response)
        elif self.type == OperationType.DOWNLOAD:
            return llm_json(response)
        elif self.type == OperationType.FILE:
            return llm_json(response)
        elif self.type == OperationType.HTTP:
            return llm_json(response)

    def execute(self, input: any):
        """
        Executes the operations.

        Returns: The response provided by the execution API
        """

        if self.type == OperationType.COMMAND:
            command_op = CommandOperation(input=input)
            return command_op.execute()

        elif self.type == OperationType.DOWNLOAD:
            download_op = DownloadOperation(input=input)
            return download_op.execute()

        elif self.type == OperationType.FILE:
            file_op = FileOperation(input=input)
            return file_op.execute()

        elif self.type == OperationType.HTTP:
            http_op = HTTPOperation(metadata=self.metadata, input=input)
            return http_op.execute()

        return "Did not execute operation"
