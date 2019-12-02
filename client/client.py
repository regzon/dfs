import os
import json
import urllib
import requests


def get_status(response_json):
    return response_json['status']


def dump_path(path):
    data = {}
    data['path'] = path
    return data


def check_path(working_dir, path):
    if './' in path:
        new_path = {x.replace('./', '') for x in path}
        return working_dir + new_path
    else:
        return None


def create_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)


class ResponseError(Exception):
    def __init__(self, response):
        super.__init__(response)


class Client:
    def __init__(self, nameserver_addr):
        self.nameserver_address = nameserver_addr
        self.working_dir = './DFS'

    def init(self):
        url = urllib.parse.urljoin(self.nameserver_address, 'init')
        print(url)
        response = requests.post(url)
        response_json = json.loads(response.text)
        if get_status(response_json) == 'success':
            data = response_json['data']
            size = data['size']
            print('Available size: ', size)
            create_dir(self.working_dir)
            return size
        elif get_status(response_json) == 'error':
            message = response_json['message']
            print(message)
            return None

    def create_file(self, path):
        request_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'create_file')
        response = requests.post(url, data=request_data)
        response_json = json.loads(response.text)
        if get_status(response_json) == 'error':
            message = response_json['message']
            print(message)
        elif get_status(response_json) == 'success':
            print('File was successfully created')

    def read_file(self, path):
        request_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'read_file')
        response = requests.get(url, params=request_data)
        response_json = json.loads(response.text)
        if get_status(response_json) == 'success':
            data = response_json['data']
            url = data['download_url']
            response = requests.get(url, params=request_data)
            filename = os.path.basename(path)
            with open('DFS/' + filename, 'wb') as f:
                f.write(response.content)
            print('Download link: ', url)
            return url
        elif get_status(response_json) == 'error':
            message = response_json['message']
            print(message)
        return None

    def write_file(self, path, real_path):
        if not os.path.exists(real_path):
            raise Exception(f"File {real_path} does not exist")
        request_data = dump_path(path)
        request_data['size'] = os.path.getsize(real_path)
        url = urllib.parse.urljoin(self.nameserver_address, 'write_file')
        response = requests.post(url, data=request_data)
        response_json = json.loads(response.text)
        if get_status(response_json) == 'success':
            data = response_json['data']
            url = data['upload_url']
            print('Upload link: ', url)
            with open(real_path, 'rb') as file:
                requests.post(url, data=request_data, files={'file': file})
            return url
        elif get_status(response_json) == 'error':
            message = response_json['message']
            print(message)
        return None

    def delete_file(self, path):
        request_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'delete_file')
        response = requests.post(url, data=request_data)
        response_json = json.loads(response.text)
        if get_status(response_json) == 'error':
            message = response_json['message']
            print(message)
        elif get_status(response_json) == 'success':
            print('File was successfully deleted')

    def get_file_info(self, path):
        request_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'get_file_info')
        response = requests.get(url, params=request_data)
        response_json = json.loads(response.text)
        if get_status(response_json) == 'success':
            data = response_json['data']
            size = data['size']
            print('File size: ', size)
            return size
        elif get_status(response_json) == 'error':
            message = response_json['message']
            print(message)
        return None

    def copy_file(self, source_path, destination_path):
        data = {}
        data['source_path'] = source_path
        data['destination_path'] = destination_path
        url = urllib.parse.urljoin(self.nameserver_address, 'copy_file')
        response = requests.post(url, data=data)
        response_json = json.loads(response.text)
        if get_status(response_json) == 'success':
            print('File was successfully copied')
        elif get_status(response_json) == 'error':
            message = response_json['message']
            print(message)

    def move_file(self, source_path, destination_path):
        data = {}
        data['source_path'] = source_path
        data['destination_path'] = destination_path
        url = urllib.parse.urljoin(self.nameserver_address, 'move_file')
        response = requests.post(url, data=data)
        response_json = json.loads(response.text)
        if get_status(response_json) == 'success':
            print('File was successfully moved')
        elif get_status(response_json) == 'error':
            message = response_json['message']
            print(message)

    def read_dir(self, path):
        request_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'read_dir')
        response = requests.get(url, params=request_data)
        response_json = response.json()
        if get_status(response_json) == 'success':
            data = response_json['data']
            filenames = data['filenames']
            print('Requested filenames: ', filenames)
            return filenames
        elif get_status(response_json) == 'error':
            message = response_json['message']
            print(message)
        return None

    def create_dir(self, path):
        request_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'create_dir')
        response = requests.post(url, data=request_data)
        response_json = json.loads(response.text)
        if get_status(response_json) == 'success':
            print('Directory was successfully created')
        elif get_status(response_json) == 'error':
            message = response_json['message']
            print(message)

    def delete_dir(self, path):
        request_data = dump_path(path)
        url = urllib.parse.urljoin(self.nameserver_address, 'delete_dir')
        response = requests.post(url, data=request_data)
        response_json = json.loads(response.text)
        if get_status(response_json) == 'success':
            print('Directory was successfully deleted')
        elif get_status(response_json) == 'error':
            message = response_json['message']
            print(message)
