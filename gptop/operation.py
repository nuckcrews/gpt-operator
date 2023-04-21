from enum import Enum
import json


class OperationType(Enum):
    POST = 1
    GET = 2
    PUT = 3
    PATCH = 4
    DELETE = 5


class Operation():

    def __init__(self, id: str, type: OperationType, url: str, path: str, params: str, body: any):
        """
        Holds the properties on an operation prepared for execution
        - id: The identifier of the operation
        - type: The type of operation
        - url: The url of the operation
        - path: The path to the operation
        - params: The params of the operation
        - body: The body of the operation
        """

        self.id = id
        self.type = type
        self.url = url
        self.path = path
        self.params = params
        self.body = body

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_obj(self, obj):
        return Operation(obj['id'], obj['type'], obj['url'], obj['path'], obj.get('params'), obj.get('body'))
