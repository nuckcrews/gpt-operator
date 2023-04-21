import os
import json
import pinecone
from openai.embeddings_utils import get_embedding
from openai import ChatCompletion
from gptop.operation import Operation
from gptop.operation_utils import Utils
from gptop.utils import llm_response, llm_json


index = pinecone.Index(os.getenv("INDEX_NAME"))


class Operator():

    def __init__(self, namespace: str) -> None:
        self.namespace = namespace

    def get(self, id: str) -> Operation:
        """
        Fetches a pre-determined operation
        - id: The operation identifier

        Returns: Operation
        """

        op = Utils.get_operation(self.namespace, id)
        if not op:
            raise ValueError("Operation does not exist")

        return Operation.from_obj(op)

    def find(self, prompt: str) -> list[Operation]:
        """
        Finds a set operations based on a provided prompt
        - prompt: The prompt to use for the search

        Returns set[Operation]
        """

        embedding = get_embedding(prompt, engine="text-embedding-ada-002")

        result = index.query(
            vector=embedding,
            top_k=3,
            namespace=self.namespace,
            include_metadata=True
        )

        operations = []
        for match in result.get('matches'):
            operations.append(Operation.from_obj(match.get('metadata')))

        return operations

    def pick(self, prompt: str, operations: list[Operation]) -> list[Operation]:
        """
        Given a prompt and a list of operations, the LLM selects
        the operation that best fits the prompt.
        - prompt: The prompt to base the selection off of
        - operations: The list of operations to choose from.

        Returns: The identifier of the operation.
        """

        clean_ops = [op.__dict__ for op in operations]
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Given a list of operations, pick one that would best contribute to the user's prompt."},
                {"role": "system", "content": "Output the ID of the operation."},
                {"role": "user", "content": f"Operations: {json.dumps(clean_ops)}"},
                {"role": "user", "content": f"Prompt: {prompt}"},
                {"role": "user", "content": "Output the ID of the operation and nothing more."}
            ],
            temperature=0.0
        )

        op_id = llm_response(response)
        operation = None
        for op in operations:
            if op.id == op_id:
                operation = op
                break

        return operation

    def prepare(self, prompt: str, operation: Operation):
        """
        Generates a payload for the operation
        based on the prompt and operation schema.
        - prompt: The prompt to use
        - operation: The operation to prepare for

        Returns: JSON object with params and body
        """

        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """
                Give an operation with a predefined schema and a user prompt,
                provide parameter and body values to send to the operation based on the prompt.
                """.replace("\n", " ")},
                {"role": "system", "content": "Output in JSON format"},
                {"role": "user", "content": f"Operation: {operation.__dict__}"},
                {"role": "user", "content": f"Prompt: {prompt}"},
                {"role": "user", "content": "Output the params and body in JSON format and nothing more."}
            ],
            temperature=0.0
        )

        return llm_json(response)


    def execute(self, operation: Operation, params: any, body: any):
        """
        Executes the provided operation.

        Returns: Value from operation
        """

        return operation.execute(params=params, body=body)

    def handle(self, prompt: str):
        """
        Asks the operator to find and execute relevant
        operations based on the provided prompt.
        - prompt: The prompt the operator should handle

        Returns: The output generated from the executed operation(s)
        """

        print("Finding operations...")
        operations = self.find(prompt=prompt)
        if not operations:
            print("Found no operations")
            return
        print(f"Found {operations} operations")

        print("Picking an operation...")
        operation = self.pick(prompt=prompt, operations=operations)
        if not operation:
            print("No operation picked")
            return
        print(f"Picked operation: {operation}")

        print(f"Preparing for execution...")
        data = self.prepare(prompt=prompt, operation=operation)
        print(f"Operation prepared with data: {data}")

        print(f"Executing operation...")
        output = self.execute(operation=operation, params=data.get("params"), body=data.get("body"))
        print(f"Execution output: {output}")

        return output
