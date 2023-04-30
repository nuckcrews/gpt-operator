import json
import requests
from enum import Enum
from gptop.operation import Operation
from gptop.utils import llm_json

class HTTPType(str, Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class HTTP(Operation):
    """
    An operation that executes an HTTP request.
    """

    def __init__(self, id: str, type: str, name: str, description: str, metadata: any, schema: any):
        super().__init__(id, type, name, description, metadata, schema)
        metadata = json.loads(metadata)
        self.request_type = metadata["type"]
        self.url = metadata["url"]
        self.path = metadata["path"]

    @classmethod
    def TYPE(self):
        return "HTTP"

    def llm_modifier(self, response):
        return llm_json(response)

    def llm_message(self):
        return [
            {"role": "system", "content": """
                Given an HTTP operation with a predefined schema and a user prompt,
                provide parameter, body, and header values to send to the operation based on the prompt.
                """.replace("\n", " ")},
            {"role": "system", "content": "If an authentication token is present, please use it as defined by the schema."},
            {"role": "system", "content": "Output in JSON format"},
            {"role": "user", "content": "Output the params, body, and header in JSON format and nothing more."}
        ]

    def execute(self, input: any):
        params = input.get("params")
        body = input.get("body")
        headers = input.get("headers")
        response = None

        endpoint = self.url + self.path
        data = None
        if body:
            data = json.dumps(body).encode('utf-8')

        # Execute the appropriate HTTP request based on the request type
        if self.request_type == HTTPType.POST:
            response = requests.post(
                url=endpoint,
                headers=headers,
                params=params,
                data=data
            )

        elif self.request_type == HTTPType.GET:
            response = requests.get(
                url=endpoint,
                headers=headers,
                params=params,
                data=data
            )

        elif self.request_type == HTTPType.PUT:
            response = requests.put(
                url=endpoint,
                headers=headers,
                params=params,
                data=data
            )

        elif self.request_type == HTTPType.PATCH:
            response = requests.patch(
                url=endpoint,
                headers=headers,
                params=params,
                data=data
            )

        elif self.request_type == HTTPType.DELETE:
            response = requests.delete(
                url=endpoint,
                headers=headers,
                params=params,
                data=data
            )

        # Return None if no response is received
        if not response:
            return None

        # Return the JSON response
        return response.json()