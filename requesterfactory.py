import json

class RequesterFactory:
    def create(self, session, type):
        if (type == "api"):
            return APIRequester(session)
        elif (type == "dummy"):
            return DummyRequester()

class APIRequester:
    def __init__(self, session):
        self.session = session

    def make_request(self, url, method, payload, verify):
        response = None
        data = None
        if method == "POST":
            response = self.session.post(url, json=payload, verify=True)
        else:
            response = self.session.get(url, params=payload, verify=True)
        if response.status_code in [200, 400]:
            data = json.loads(response.text)
        return data

class DummyRequester:
    def make_request(self, url, method, payload, verify):
        with open('json/file01.json') as f:
            text = f.read()
            data = json.loads(text)
        return data
