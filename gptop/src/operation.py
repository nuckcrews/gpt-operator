import json
import requests
from enum import Enum


class OperationType(str, Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Operation():

    def __init__(self, id: str, type: OperationType, name: str, description: str, url: str, path: str, schema: any):
        """
        Holds the properties on an operation prepared for execution
        - id: The identifier of the operation
        - type: The type of operation
        - name: The name of the operation
        - description: The description of the operation
        - url: The url of the operation
        - path: The path to the operation
        - schema: The schema of the operation
        """

        self.id = id
        self.type = type
        self.name = name
        self.description = description
        self.url = url
        self.path = path
        self.schema = schema

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_obj(self, obj):
        """
        Returns an instance of an operation from a dict object
        """

        return Operation(obj['id'], obj['type'], obj['name'], obj['description'],
                         obj['url'], obj['path'], obj['schema'])

    def endpoint(self) -> str:
        return self.url + self.path

    def execute(self, params, body):
        """
        Executes the command.

        Returns: The response provided by the execution API
        """

        result = None

        if self.type == OperationType.POST:
            result = requests.post(
                self.endpoint(),
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                params=params,
                data=json.dumps(body).encode('utf-8')
            )

        elif self.type == OperationType.GET:
            result = requests.get(
                self.endpoint(),
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                params=params,
                data=json.dumps(body).encode('utf-8')
            )

        elif self.type == OperationType.PUT:
            result = requests.put(
                self.endpoint(),
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                params=params,
                data=json.dumps(body).encode('utf-8')
            )

        elif self.type == OperationType.PATCH:
            result = requests.patch(
                self.endpoint(),
                headers={'Accept': 'application/json'},
                params=params,
                data=json.dumps(body).encode('utf-8')
            )

        elif self.type == OperationType.DELETE:
            result = requests.delete(
                self.endpoint(),
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                params=params,
                data=json.dumps(body).encode('utf-8')
            )

        if not result:
            return None

        return result.json()
