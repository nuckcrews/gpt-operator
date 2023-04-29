import subprocess

__all__ = ["CommandOperation"]


class CommandOperation():
    """
    An operation that executes CLI commands
    in the local environment.
    """

    def __init__(self, input: any):
        self.command = input
        self.prefix_cmd = "mkdir -p ./tmp_ai && cd ./tmp_ai"

    @classmethod
    def llm_message(self):
        return [
            {"role": "system", "content": """
                Given a CLI command operation with a predefined schema and a user prompt,
                provide the command to run in the terminal based on the prompt.
                """.replace("\n", " ")},
            {"role": "user", "content": "Output the command to run and nothing more."}
        ]

    def execute(self):
        subprocess.run(self.prefix_cmd + " && " + self.command,
                       shell=True)
        return f"Executed command: {self.command}"
