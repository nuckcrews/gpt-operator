import os
import pinecone
from openai.embeddings_utils import get_embedding
from gptop.operation import Operation
from gptop.operation_utils import Utils

INDEX_NAME = os.getenv("INDEX_NAME")

index = pinecone.Index(INDEX_NAME)


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

    def execute(self, operations: list[Operation]):
        """
        Executes a given transaction with the provided parameters.

        Returns: Value from operation
        """
        pass

    def handle(self, prompt: str):
        print("Finding operations...")
        operations = self.find(prompt=prompt)
        if not operations:
            print("Found no operations")
            return

        print(f"Found {operations} operations")


