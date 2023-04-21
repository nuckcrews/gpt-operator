import os
import json
import pinecone
from openai.embeddings_utils import get_embedding
from openai import ChatCompletion
from gptop.operation import Operation
from gptop.operation_utils import Utils


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

    def execute(self, operation: Operation):
        """
        Executes the provided operation.

        Returns: Value from operation
        """

        return operation.execute()

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
                {"role": "user", "content": prompt},
                {"role": "user", "content": "Output the ID of the operation and nothing more."}
            ],
            temperature=0.0
        )

        choice = response.get("choices")[0]
        return choice.get("message").get("content")

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
        op_id = self.pick(prompt=prompt, operations=operations)

        print(f"GPT output: {op_id}")

        operation = None
        for op in operations:
            if op.id == op_id:
                operation = op
                break

        if not operation:
            print("No operation picked")
            return

        print(f"Picked operation: {operation}")

        print(f"Executing operation...")
        output = self.execute(operation=operation)

        print(f"Execution output: {output}")
