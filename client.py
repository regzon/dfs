import requests
import json
import urllib
import os


def get_status(response):
    return response['status']


def dump_path(path):
    data = {}
    data['path'] = path
    json_data = json.dumps(data)
    return json_data


class Client:
    def __init__(self):
        self.nameserver_address = 'http://0.0.0.0:5000'
        self.working_dir = os.path.dirname(os.path.realpath(__file__))

    def init(self):
        url = urllib.parse.urljoin(self.nameserver_address, 'init')
        r = requests.get(url)
        response = json.loads(r.text)
        if get_status(response) == 'success':
            data = response['data']
            size = data['size']
            print('Available size: ', size)
            # TODO: create new working directory
            return size
        elif get_status(response) == 'error':
            message = response['message']
            print(message)
        return None

    def create_file(self, path):
        json_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'create_file')
        r = requests.post(url, data=json_data)
        response = json.loads(r.text)
        if get_status(response) == 'error':
            message = response['message']
            print(message)
        elif get_status(response) == 'success':
            print('File was successfully created')

    def read_file(self, path):
        json_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'read_file')
        r = requests.get(url, data=json_data)
        response = json.loads(r.text)
        if get_status(response) == 'success':
            data = response['data']
            url = data['download_url']
            print('Download link: ', url)
            return url
        elif get_status(response) == 'error':
            message = response['message']
            print(message)
        return None

    def write_file(self, path):
        json_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'write_file')
        r = requests.post(url, data=json_data)
        response = json.loads(r.text)
        if get_status(response) == 'success':
            data = response['data']
            url = data['upload_url']
            print('Upload link: ', url)
            return url
        elif get_status(response) == 'error':
            message = response['message']
            print(message)
        return None

    def delete_file(self, path):
        json_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'delete_file')
        r = requests.post(url, data=json_data)
        response = json.loads(r.text)
        if get_status(response) == 'error':
            message = response['message']
            print(message)
        elif get_status(response) == 'success':
            print('File was successfully deleted')

    def get_file_info(self, path):
        json_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'get_file_info')
        r = requests.get(url, data=json_data)
        response = json.loads(r.text)
        if get_status(response) == 'success':
            data = response['data']
            size = data['size']
            print('File size: ', size)
            return size
        elif get_status(response) == 'error':
            message = response['message']
            print(message)
        return None

    def copy_file(self, source_path, destination_path):
        data = {}
        data['source_path'] = source_path
        data['destination_path'] = destination_path
        json_data = json.dumps(data)
        url = urllib.parse.urljoin(self.nameserver_address, 'copy_file')
        r = requests.post(url, data=json_data)
        response = json.loads(r.text)
        if get_status(response) == 'success':
            print('File was successfully copied')
        elif get_status(response) == 'error':
            message = response['message']
            print(message)

    def read_dir(self, path):
        json_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'read_dir')
        r = requests.get(url, data=json_data)
        response = json.loads(r.text)
        if get_status(response) == 'success':
            data = response['data']
            filenames = data['filenames']
            print('Requested filenames: ', filenames)
            return filenames
        elif get_status(response) == 'error':
            message = response['message']
            print(message)
        return None

    def create_dir(self, path):
        json_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'create_dir')
        r = requests.post(url, data=json_data)
        response = json.loads(r.text)
        if get_status(response) == 'success':
            print('Directory was successfully created')
        elif get_status(response) == 'error':
            message = response['message']
            print(message)

    def delete_dir(self, path):
        json_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'delete_dir')
        r = requests.post(url, data=json_data)
        response = json.loads(r.text)
        if get_status(response) == 'success':
            print('Directory was successfully deleted')
        elif get_status(response) == 'error':
            message = response['message']
            print(message)


if __name__ == '__main__':
    pass
