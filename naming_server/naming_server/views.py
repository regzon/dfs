import os
import logging

from django.http import JsonResponse
from django.utils import timezone

from .models import File, Directory, Storage, StoredFile

logger = logging.getLogger(__name__)


def directory_from_path(path):
    path = os.path.normpath(path)
    if path and path[0] == '/':
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
        StoredFile.objects.create(
            status=StoredFile.READY,
            storage=storage,
            file=file,
        )
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
    stored_file_queryset = StoredFile.objects.filter(
        file=file,
        status=StoredFile.READY,
    )
    if stored_file_queryset.count() == 0:
        data = {
            'status': 'error',
            'message': 'File not in READY state'
        }
        return JsonResponse(data, status=400)
    storage = stored_file_queryset[0].storage
    download_url = storage.url + '/download_file'
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

    path = request.POST['path']
    size = int(request.POST['size'])
    directory_path, filename = os.path.split(path)
    directory = directory_from_path(directory_path)
    if directory is None:
        data = {
            'status': 'error',
            'message': 'Parent directory does not exist',
        }
        return JsonResponse(data, status=400)

    file, created = File.objects.get_or_create(
        name=filename,
        parent_dir=directory,
    )
    file.size = size
    file.save()
    first_storage = None
    for storage in Storage.objects.all():
        stored_file, created = StoredFile.objects.get_or_create(
            storage=storage,
            file=file,
        )
        if first_storage is None:
            first_storage = storage
            stored_file.status = StoredFile.UPLOADING
        else:
            stored_file.status = StoredFile.WAITING
        stored_file.save()
    if first_storage is None:
        data = {
            'status': 'error',
            'message': "No storage servers available",
        }
        return JsonResponse(data, status=500)
    upload_url = first_storage.url + '/upload_file'
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
    stored_file = StoredFile.objects.filter(file=file)
    if stored_file.status != StoredFile.READY:
        data = {
            'status': 'error',
            'message': 'File not in READY state'
        }
        return JsonResponse(data, status=400)
    # stored_file.status = StoredFile.DELETING
    for storage in Storage.objects.all():
        storage.delete_file(path)
        StoredFile.objects.filter(storage=storage, file=file).delete()
    data = {'status': 'success'}
    return JsonResponse(data)


def get_file_info(request):
    if request.method != 'GET':
        data = {'status': 'error',
                'message': f'Not correct method type. Get {request.method}\
                 insted GET'
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
    size = file.size
    data = {
        'status': 'success',
        'data': {
            'size': size,
        }
    }
    return JsonResponse(data)


def copy_file(request):
    if request.method != 'POST':
        data = {
            'status': 'error',
            'message': (
                f'Not correct method type.'
                f' Get {request.method} insted POST'
            )
        }
        return JsonResponse(data, status=400)

    source_path = request.POST['source_path']
    dest_path = request.POST['destination_path']

    source_file = file_from_path(source_path)

    if source_file is None:
        data = {
            'status': 'error',
            'message': 'File does not exist'
        }
        return JsonResponse(data, status=400)

    directories, filename = os.path.split(dest_path)
    dest_parent_dir = directory_from_path(directories)

    if dest_parent_dir is None:
        data = {
            'status': 'error',
            'message': f'Destination directory does not exist',
        }
        return JsonResponse(data, status=400)

    stored_file_queryset = StoredFile.objects.filter(
        file=source_file,
        status=StoredFile.READY,
    )

    if not stored_file_queryset.exists():
        data = {
            'status': 'error',
            'message': f'No storage available for this file',
        }
        return JsonResponse(data, status=500)

    stored_file = stored_file_queryset[0]
    storage = stored_file.storage
    dest_file = File.objects.create(
        name=filename,
        parent_dir=dest_parent_dir,
    )
    StoredFile.objects.create(
        file=dest_file,
        storage=storage,
        status=StoredFile.UPLOADING,
    )
    storage.copy_file(source_path, dest_path)

    data = {'status': 'success'}
    return JsonResponse(data)


def move_file(request):
    if request.method != 'POST':
        data = {
            'status': 'error',
            'message': (
                f'Not correct method type.'
                f' Get {request.method} insted POST'
            )
        }
        return JsonResponse(data, status=400)

    source_path = request.POST['source_path']
    dest_path = request.POST['destination_path']

    source_file = file_from_path(source_path)

    if source_file is None:
        data = {
            'status': 'error',
            'message': 'File does not exist'
        }
        return JsonResponse(data, status=400)

    directories, filename = os.path.split(dest_path)
    dest_parent_dir = directory_from_path(directories)

    if dest_parent_dir is None:
        data = {
            'status': 'error',
            'message': f'Destination directory does not exist',
        }
        return JsonResponse(data, status=400)

    stored_file_queryset = StoredFile.objects.filter(
        file=source_file,
        status=StoredFile.READY,
    )

    if not stored_file_queryset.exists():
        data = {
            'status': 'error',
            'message': f'No storage available for this file',
        }
        return JsonResponse(data, status=500)

    stored_file = stored_file_queryset[0]
    main_storage = stored_file.storage

    for stored_file in stored_file_queryset.exclude(storage=main_storage):
        stored_file.storage.delete_file(source_path)
    source_file.delete()

    dest_file = File.objects.create(
        name=filename,
        parent_dir=dest_parent_dir,
    )
    StoredFile.objects.create(
        file=dest_file,
        storage=main_storage,
        status=StoredFile.UPLOADING,
    )
    main_storage.move_file(source_path, dest_path)

    data = {'status': 'success'}
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
    ip_address = request.POST['ip_address']
    port = int(request.POST['port'])
    storage_obj = Storage.objects.filter(
        ip_address=ip_address,
        service_port=port,
    )
    if not storage_obj.exists():
        logger.info(
            "Creating a storage object with"
            f" ip {ip_address}, size {request.POST['size']}, port {port}"
        )
        Storage.objects.create(
            ip_address=ip_address,
            service_port=port,
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


def storage_update_status(request):
    logger.info("Received a storage status update request")
    ip_address = request.POST['ip_address']
    port = int(request.POST['port'])
    path = request.POST['path']
    logger.info(f"Path: {path}")
    file = file_from_path(path)
    storage = Storage.objects.get(ip_address=ip_address, service_port=port)
    StoredFile.objects.filter(storage=storage, file=file) \
        .update(status=StoredFile.READY)
    waiting = file.stored_files.filter(status=StoredFile.WAITING)
    if waiting.count() == 0:
        logger.info("Zero storages are waiting for file transfer")
        return JsonResponse({})
    download_url = storage.url + '/download_file'
    logger.info(f"Transfer download url: {download_url}")
    dst_stored_file = waiting[0]
    dst_storage = dst_stored_file.storage
    dst_stored_file.status = StoredFile.UPLOADING
    dst_stored_file.save()
    dst_storage.transfer(path, download_url)
    return JsonResponse({})


def file_exists(file_path):
    return True


def get_filenames(dir_path):
    return None


def dir_exists(path):
    return True


def get_file_size(path):
    return -1
