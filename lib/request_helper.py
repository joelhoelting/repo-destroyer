import requests


class RequestHelper:
    def __init__(self, url: str, method: str = "get", data: dict = None):
        self.url = url
        self.method = method
        self.data = data

    def request_to_json(self):
        print(self.method, self.url)
        response = requests.request(self.method, url=self.url, data=self.data)
        print(response.headers)
        response_to_json = response.json()
        return response_to_json
