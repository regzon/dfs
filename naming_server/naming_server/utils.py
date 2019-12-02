import requests
import urllib.parse


def send_request(host, uri, method='get', data=None):
    if data is None:
        data = {}
    request_function = requests.get if method == 'get' else requests.post
    url = urllib.parse.urljoin('http://' + host + ':5000', uri)
    response = request_function(url, data, timeout=3)
    return response.json()
