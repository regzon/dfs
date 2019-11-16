import requests
import json

nameserver_address = '0.0.0.0:5000'


def main():
    pass


def init():
    r = requests.get(nameserver_address + '/init')
    response = json.loads(r.text)
    if get_status(response) == 'success':
        data = response['data']
        size = data['size']
        print('Available size: ', size)
        return size
    elif get_status(response) == 'error':
        message = response['message']
        print(message)
    return None


def create_file(path):
    json_data = dump_file_path(path)
    r = requests.post(nameserver_address + '/create_file', data=json_data)
    response = json.loads(r.text)
    if get_status(response) == 'error':
        message = response['message']
        print(message)
    elif get_status(response) == 'success':
        print('File was successfully created')


def read_file(path):
    json_data = dump_file_path(path)
    r = requests.get(nameserver_address + '/read_file', data=json_data)
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


def write_file(path):
    json_data = dump_file_path(path)
    r = requests.post(nameserver_address + '/write_file', data=json_data)
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


def delete_file(path):
    json_data = dump_file_path(path)
    r = requests.post(nameserver_address + '/delete_file', data=json_data)
    response = json.loads(r.text)
    if get_status(response) == 'error':
        message = response['message']
        print(message)
    elif get_status(response) == 'success':
        print('File was successfully deleted')


def get_file_info(path):
    json_data = dump_file_path(path)
    r = requests.get(nameserver_address + '/get_file_info', data=json_data)
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


def copy_file(source_path, destination_path):
    data = {}
    data['source_path'] = source_path
    data['destination_path'] = destination_path
    json_data = json.dumps(data)
    r = requests.post(nameserver_address + '/copy_file', data=json_data)
    response = json.loads(r.text)
    if get_status(response) == 'success':
        print('File was successfully copied')
    elif get_status(response) == 'error':
        message = response['message']
        print(message)


def read_dir(path):
    json_data = dump_file_path(path)
    r = requests.get(nameserver_address + '/read_dir', data=json_data)
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


def create_dir(path):
    json_data = dump_file_path(path)
    r = requests.post(nameserver_address + '/create_dir', data=json_data)
    response = json.loads(r.text)
    if get_status(response) == 'success':
        print('Directory was successfully created')
    elif get_status(response) == 'error':
        message = response['message']
        print(message)


def delete_dir(path):
    json_data = dump_file_path(path)
    r = requests.post(nameserver_address + '/delete_dir', data=json_data)
    response = json.loads(r.text)
    if get_status(response) == 'success':
        print('Directory was successfully deleted')
    elif get_status(response) == 'error':
        message = response['message']
        print(message)


def get_status(response):
    return response['status']


def dump_file_path(path):
    data = {}
    data['path'] = path
    json_data = json.dumps(data)
    return json_data


if __name__ == '__main__':
    main()
