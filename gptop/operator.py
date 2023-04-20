from operation import Operation


class Operator():

    def __init__(self) -> None:
        pass

    def get(id: str) -> Operation:
        """
        Fetches a pre-determined operation
        - id: The operation identifier

        Returns: Operation
        """
        


    def find(prompt: str) -> set[Operation]:
        """
        Finds a set operations based on a provided prompt
        - prompt: The prompt to use for the search

        Returns set[Operation]
        """

        pass

    def execute(operations: list[Operation]):
        """
        Executes a given transaction with the provided parameters.

        Returns: Value from operation
        """
        pass
