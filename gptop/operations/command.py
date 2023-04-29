import subprocess

__all__ = ["CommandOperation"]


class CommandOperation():
    """
    An operation that executes CLI commands
    in the local environment.
    """

    def __init__(self, input: any):
        self.command = input["command"]
        self.base_path = input.get("base_path")
        self.prefix_cmd = "mkdir -p ./tmp_ai && cd ./tmp_ai"

    @classmethod
    def llm_message(self):
        return [
            {"role": "system", "content": """
                Given a CLI command operation with a predefined schema and a user prompt,
                provide the command to run in the terminal and at what base path based on the prompt.
                """.replace("\n", " ")},
            {"role": "user", "content": "Output the JSON for the command to run and the base_path and nothing more."}
        ]

    def execute(self):
        try:
            if self.base_path:
                result = subprocess.run(f"cd {self.base_path} && " + self.command,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        check=True)
            else:
                result = subprocess.run(self.command,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        check=True)
            return result.stdout.decode('utf-8')
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            return e.stderr.decode('utf-8')