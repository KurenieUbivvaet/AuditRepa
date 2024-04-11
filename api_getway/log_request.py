import requests


class LogRequest(object):
    def __init__(self, method, url, headers, body):
        self._method = method
        self._url = url
        self._headers = headers
        self._body = body

    def post_request(self):
        response = requests.post(self._url, headers=self._headers, data=self._body)
        status = response.status_code
        return status
