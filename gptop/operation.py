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
