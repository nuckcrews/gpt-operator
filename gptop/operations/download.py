import urllib.request

__all__ = ["DownloadOperation"]


class DownloadOperation():
    """
    An operation that downloads data
    from a provided url..
    """

    def __init__(self, input: any):
        self.download_url = input["download_url"]

    def execute(self):
        try:
            response = urllib.request.urlopen(self.download_url)
            return response.read()
        except:
            return None
