import os
import json
import pinecone
from openai.embeddings_utils import get_embedding
from openai import ChatCompletion
from .operation import Operation
from .operation_utils import OperationUtils
from .factory import create_operation_from_object
from .utils import llm_response, llm_json

__all__ = ["Operator"]


class Operator():

    def __init__(self, namespace: str) -> None:
        self.namespace = namespace

    def get(self, id: str) -> Operation:
        """
        Fetches a pre-determined operation
        - id: The operation identifier

        Returns: Operation
        """

        op = OperationUtils.get_operation(self.namespace, id)
        if not op:
            raise ValueError("Operation does not exist")

        return op

    def step(self, prompt: str, completed: list[str]) -> Operation:
        """
        Creates a step to execute based on the given prompt
        - prompt: The prompt to base the step off if

        Returns: The step to take
        """

        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": """
                Given a prompt and a list of completed steps,
                create the very next step to take. Be detailed and descriptive.
                """.replace("\n", " ")},
                {"role": "user", "content": f"Output just the next step and nothing else."},
                {"role": "user", "content": f"Prompt: {prompt}"},
                {"role": "user", "content": f"Completed Steps: {completed}"},
            ],
            temperature=0.0
        )

        return llm_response(response)

    def find(self, prompt: str, top_k: int = 3) -> list[Operation]:
        """
        Finds a set operations based on a provided prompt
        - prompt: The prompt to use for the search

        Returns set[Operation]
        """

        index = pinecone.Index(os.getenv("PINECONE_INDEX"))
        embedding = get_embedding(prompt, engine="text-embedding-ada-002")

        result = index.query(
            vector=embedding,
            top_k=top_k,
            namespace=self.namespace,
            include_metadata=True
        )

        operations = []
        for match in result.get('matches'):
            operations.append(
                create_operation_from_object(match.get('metadata')))

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
                {"role": "system", "content": """
                Given a list of operations, pick the minimum amount of operations that are needed for the prompt.
                """.replace("\n", " ")},
                {"role": "system",
                    "content": "Output the IDs of the operations in an array."},
                {"role": "system", "content": "If these operations are not needed to fulfill the prompt, return None."},
                {"role": "user",
                    "content": f"Operations: {json.dumps(clean_ops)}"},
                {"role": "user", "content": f"Prompt: {prompt}"},
                {"role": "user", "content": "Output the list of IDs of the operations in an array and nothing more."}
            ],
            temperature=0.0
        )

        op_ids = llm_json(response)
        if not op_ids:
            return None

        ops = []
        for op in operations:
            if op.id in op_ids:
                ops.append(op)

        return ops

    def prepare(self, prompt: str, operation: Operation):
        """
        Generates a payload for the operation
        based on the prompt and operation schema.
        - prompt: The prompt to use
        - operation: The operation to prepare for

        Returns: JSON object with params and body
        """

        messages = operation.llm_message() + [
            {"role": "user", "content": f"Operation: {operation.__dict__}"},
            {"role": "user", "content": f"Prompt: {prompt}"}
        ]

        response = ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.0
        )

        return operation.llm_modifier(response)

    def execute(self, operation: Operation, input: any):
        """
        Executes the provided operation.

        Returns: Value from operation
        """

        return operation.execute(input=input)

    def react(self, prompt: str, operation: Operation, values: str, result: str) -> str:
        """
        Reacts to the operation execution based on
        the original prompt

        Returns: The LLM reaction response
        """
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """
                Given a the original prompt and the execution result of an operation that followed,
                respond to the prompt based on the execution result.
                """.replace("\n", " ")},
                {"role": "user", "content": f"Prompt: {prompt}"},
                {"role": "user", "content": f"Operation: {operation.__dict__}"},
                {"role": "user", "content": f"Values passed to operation: {values}"},
                {"role": "user", "content": f"Execution result: {result}"}
            ],
            temperature=0.0
        )

        return llm_response(response)
