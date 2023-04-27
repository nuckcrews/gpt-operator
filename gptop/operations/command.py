__all__ = ["CommandOperation"]


class CommandOperation():
    """
    An operation that executes CLI commands
    in the local environment.
    """

    def __init__(self, input: any):
        self.command = input["command"]

    def execute(self):
        pass
