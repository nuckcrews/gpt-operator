import urllib.request

__all__ = ["DownloadOperation"]


class DownloadOperation():
    """
    An operation that downloads data
    from a provided url..
    """

    def __init__(self, input: any):
        self.download_url = input["download_url"]

    @classmethod
    def llm_message(self):
        return [
            {"role": "system", "content": """
                Given a download operation with a predefined schema and a user prompt,
                provide the download url to download based on the prompt.
                """.replace("\n", " ")},
            {"role": "system", "content": "Output in JSON format"},
            {"role": "system", "content": 'Example: {"download_url": "<URL>"}'},
            {"role": "user", "content": "Output in JSON format and nothing more."}
        ]

    def execute(self):
        try:
            response = urllib.request.urlopen(self.download_url)
            return response.read()
        except:
            return None
