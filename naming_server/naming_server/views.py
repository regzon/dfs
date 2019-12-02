import os
import json
import logging

from ipware import get_client_ip
from django.http import JsonResponse
from django.utils import timezone

from .models import File, Directory, Storage, StoredFile

logger = logging.getLogger(__name__)


def directory_from_path(path):
    path = os.path.normpath(path)
    if path[0] == '/':
        path = path[1:]
    parent_dir = Directory.objects.get(parent_dir=None)
    if not path:
        return parent_dir
    directories = path.split('/')
    for directory in directories:
        try:
            parent_dir = parent_dir.subdirs.get(name=directory)
        except Directory.DoesNotExist:
            return None
    return parent_dir


def file_from_path(path):
    path = os.path.normpath(path)
    if path[0] == '/':
        path = path[1:]
    directories, filename = os.path.split(path)
    directory = directory_from_path(directories)
    if directory is None:
        return None
    try:
        file = directory.files.get(name=filename)
    except File.DoesNotExist:
        return None
    return file


def filenames_from_path(directory):
    filenames = []
    for file in directory.files.all():
        filenames.append(file.name)
    for sub_dir in directory.subdirs.all():
        filenames.append(sub_dir.name + '/')
    return filenames


def init(request):
    if request.method != 'POST':
        data = {
            'status': 'error',
            'message': (
                f'Not correct method type.'
                f'Get {request.method} insted POST'
            )
        }
        return JsonResponse(data, status=400)
    # Delete existing files
    File.objects.all().delete()
    Directory.objects.all().delete()
    # Initialize storage servers
    total_size = 0
    for storage in Storage.objects.all():
        total_size += storage.initialize()
    # Create root directory
    Directory.objects.create(name='root', parent_dir=None)
    data = {
        'status': 'success',
        'data': {'size': total_size}
    }
    return JsonResponse(data)


def create_file(request):
    if request.method != 'POST':
        data = {
            'status': 'error',
            'message': (
                f'Not correct method type.'
                f' Get {request.method} insted POST'
            )
        }
        return JsonResponse(data, status=400)
    path = request.POST['path']
    if file_from_path(path) is not None:
        data = {
            'status': 'error',
            'message': 'File already exists',
        }
        return JsonResponse(data, status=400)
    directory_path, filename = os.path.split(path)
    directory = directory_from_path(directory_path)
    if directory is None:
        data = {
            'status': 'error',
            'message': 'Parent directory does not exist',
        }
        return JsonResponse(data, status=400)
    file = File.objects.create(name=filename, parent_dir=directory)
    for storage in Storage.objects.all():
        storage.create_file(path)
        StoredFile.objects.create(storage=storage, file=file)
    data = {'status': 'success'}
    return JsonResponse(data)


def read_file(request):
    if request.method != 'GET':
        data = {
            'status': 'error',
            'message': (
                f'Not correct method type.'
                f' Get {request.method} insted GET'
            )
        }
        return JsonResponse(data, status=400)

    path = request.GET['path']
    file = file_from_path(path)
    if file is None:
        data = {'status': 'error', 'message': 'File does not exist'}
        return JsonResponse(data, status=400)

    storage = file.storages.all()[0]
    download_url = 'http://' + storage.ip_address + ':5000/download_file'
    data = {
        'status': 'success',
        'data': {'download_url': download_url},
    }
    return JsonResponse(data)


def write_file(request):
    if request.method != 'POST':
        data = {
            'status': 'error',
            'message': (
                f'Not correct method type.'
                f' Get {request.method} insted POST'
            )
        }
        return JsonResponse(data, status=400)

    storage = Storage.objects.all()[0]
    upload_url = 'http://' + storage.ip_address + ':5000/upload_file'
    data = {
        'status': 'success',
        'data': {'upload_url': upload_url}
    }
    return JsonResponse(data)


def delete_file(request):
    if request.method != 'POST':
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                 insted POST'
                }
        return JsonResponse(data, status=400)

    path = request.POST['path']
    file = file_from_path(path)
    if file is None:
        data = {
            'status': 'error',
            'message': 'File does not exist'
        }
        return JsonResponse(data, status=400)
    for storage in Storage.objects.all():
        storage.delete_file(path)
        StoredFile.objects.filter(storage=storage, file=file).delete()
    data = {'status': 'success'}
    return JsonResponse(data)


def get_file_info(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        path = body['path']

        if file_exists(path):
            size = get_file_size(path)
            # TODO: send request to Storage server to delete
            data = {
                'status': 'success',
                'data': {
                    'size': size,
                }
            }
        else:
            data = {
                'status': 'error',
                'message': 'File does not exist'
            }
    else:
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                 insted GET'
                }
    return JsonResponse(data)


def copy_file(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        source = body['source_path']
        dest = body['destination_path']

        if dir_exists(source) and dir_exists(dest):
            data = {'status': 'success'}
        else:
            data = {
                'status': 'error',
                'message': 'Directory does not exist'
            }
    else:
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                 insted POST'
                }
    return JsonResponse(data)


def read_dir(request):
    if request.method != 'GET':
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                insted GET'
                }

        return JsonResponse(data, status=400)
    path = os.path.normpath(request.GET['path'])
    directory = directory_from_path(path)
    if directory is not None:
        filenames = filenames_from_path(directory)
        data = {
            'status': 'success',
            'data': {
                'filenames': filenames
            }
        }
    else:
        data = {
            'status': 'error',
            'message': 'Directory does not exist'
        }
        return JsonResponse(data, status=400)
    return JsonResponse(data)


def create_dir(request):
    if request.method != 'POST':
        data = {
            'status': 'error',
            'message': (
                f'Not correct method type.'
                f' Get {request.method} insted POST'
            )
        }
        return JsonResponse(data, status=400)
    path = os.path.normpath(request.POST['path'])
    directory = directory_from_path(path)
    if directory is not None:
        data = {
            'status': 'error',
            'message': 'Directory already exists',
        }
        return JsonResponse(data, status=400)
    parent_path, directory = os.path.split(path)
    parent_dir = directory_from_path(parent_path)
    if parent_dir is None:
        data = {
            'status': 'error',
            'message': 'Parent directory does not exist',
        }
        return JsonResponse(data, status=400)
    Directory.objects.create(name=directory, parent_dir=parent_dir)
    data = {'status': 'success'}
    return JsonResponse(data)


def delete_dir(request):
    if request.method != 'POST':
        data = {
            'status': 'error',
            'message': (
                f'Not correct method type.'
                f'Get {request.method} insted POST'
            )
        }
        return JsonResponse(data, status=400)
    path = os.path.normpath(request.POST['path'])
    directory = directory_from_path(path)
    if directory is None:
        data = {
            'status': 'error',
            'message': 'Directory does not exist'
        }
        return JsonResponse(data, status=400)
    directory.delete()
    for storage in Storage.objects.all():
        storage.delete_dir(path)
    data = {'status': 'success'}
    return JsonResponse(data)


def storage_heartbeat(request):
    logger.info("Received a storage heartbeat request")
    storage_ip, _ = get_client_ip(request)
    storage_obj = Storage.objects.filter(ip_address=storage_ip)
    if not storage_obj.exists():
        logger.info(
            "Creating a storage object with"
            f" ip address {storage_ip} and size {request.POST['size']}"
        )
        Storage.objects.create(
            ip_address=storage_ip,
            available_size=request.POST['size'],
            last_heartbeat=timezone.now(),
        )
    else:
        storage_obj.update(
            available_size=request.POST['size'],
            last_heartbeat=timezone.now(),
        )
    logger.info("Finished a storage heartbeat successfully")
    return JsonResponse({})


def file_exists(file_path):
    return True


def get_filenames(dir_path):
    return None


def dir_exists(path):
    return True


def get_file_size(path):
    return -1
