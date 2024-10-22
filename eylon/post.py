from urllib.request import Request, urlopen
import json

def post(url, data):
    payload = json.dumps(data)
    request = Request(url, payload.encode())
    with urlopen(request) as response:
        data = response.read().decode()
        return json.loads(data)
