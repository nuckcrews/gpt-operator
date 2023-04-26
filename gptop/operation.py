import os
import json
import requests
import urllib.request
from enum import Enum

__all__ = ["OperationType", "Operation"]


class OperationType(str, Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    DOWNLOAD = "DOWNLOAD"


class Operation():

    def __init__(self, id: str, type: OperationType, name: str, description: str,
                 url: str, path: str, requires_auth: bool, schema: any):
        """
        Holds the properties on an operation prepared for execution
        - id: The identifier of the operation
        - type: The type of operation
        - name: The name of the operation
        - description: The description of the operation
        - url: The url of the operation
        - path: The path to the operation
        - requires_auth: If the operation requires authentication
        - schema: The schema of the operation
        """

        self.id = id
        self.type = type
        self.name = name
        self.description = description
        self.url = url
        self.path = path
        self.requires_auth = requires_auth
        self.schema = schema
        self.token = os.getenv(id + "_token")

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_obj(self, obj):
        """
        Returns an instance of an operation from a dict object
        """

        return Operation(obj['id'], obj['type'], obj['name'], obj['description'],
                         obj.get('url'), obj.get('path'), obj['auth'], obj['schema'])

    def metadata(self):
        d = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "url": self.url,
            "path": self.path,
            "auth": self.requires_auth,
            "schema": self.schema
        }
        return {k: v for k, v in d.items() if v is not None}

    def embedding_obj(self):
        return "; ".join([
            f"Name: {self.name}",
            f"Description: {self.description}",
            f"Type: {self.type}",
            f"URL: {self.url}",
            f"Path: {self.path}",
            f"Requires Auth: {self.requires_auth}",
            f"Schema: {self.schema}"
        ])

    def endpoint(self) -> str:
        return self.url + self.path

    def execute(self, params, body, headers):
        """
        Executes the command.

        Returns: The response provided by the execution API
        """

        result = None
        data = json.dumps(body).encode('utf-8')

        if self.type == OperationType.DOWNLOAD:
            response = urllib.request.urlopen(params["download_url"])
            return response.read()

        if self.type == OperationType.POST:
            result = requests.post(
                self.endpoint(),
                headers=headers,
                params=params,
                data=data
            )

        elif self.type == OperationType.GET:
            result = requests.get(
                self.endpoint(),
                headers=headers,
                params=params,
                data=data
            )

        elif self.type == OperationType.PUT:
            result = requests.put(
                self.endpoint(),
                headers=headers,
                params=params,
                data=data
            )

        elif self.type == OperationType.PATCH:
            result = requests.patch(
                self.endpoint(),
                headers=headers,
                params=params,
                data=data
            )

        elif self.type == OperationType.DELETE:
            result = requests.delete(
                self.endpoint(),
                headers=headers,
                params=params,
                data=data
            )

        if not result:
            return None

        return result.json()
