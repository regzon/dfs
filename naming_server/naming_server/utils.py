import requests
import urllib.parse


def send_request(host, port, uri, method='get', data=None):
    if data is None:
        data = {}
    request_function = requests.get if method == 'get' else requests.post
    url = urllib.parse.urljoin(f'http://{host}:{port}', uri)
    response = request_function(url, data, timeout=3)
    return response.json()
