__all__ = ["CommandOperation"]


class CommandOperation():
    """
    An operation that executes CLI commands
    in the local environment.
    """

    def __init__(self, input: any):
        self.command = input["command"]

    @classmethod
    def llm_message(self):
        return [
            {"role": "system", "content": """
                Give a CLI command operation with a predefined schema and a user prompt,
                provide the command to run in the terminal based on the prompt.
                """.replace("\n", " ")},
            {"role": "user", "content": "Output the command to run and nothing more."}
        ]

    def execute(self):
        pass
